"""
MST vs K-Means Robustness Analysis
==================================
Compares MST-based clustering (Zahn-style edge cutting) with K-Means under:
  1. Gaussian noise            (feature jitter of increasing strength)
  2. Outliers                  (increasing % of uniform random points)
  3. Non-linear distributions  (moons, circles, blobs, anisotropic blobs)
Plus a small runtime-scalability test.

Algorithms
  - K-Means          : sklearn KMeans (n_init=10)
  - MST (plain)      : build MST, cut the k-1 heaviest edges
  - MST (min-size)   : cut heaviest edges but ignore pieces smaller than
                       `min_size` (they are treated as noise, label -1)

Robustness measures (all quantitative)
  - ARI / NMI        : agreement with ground truth (scored on inliers only)
  - Silhouette       : internal quality (no ground truth needed)
  - Retention ratio  : ARI(perturbed) / ARI(clean)
  - Robustness AUC   : mean ARI over all perturbation levels (trapezoid, 0..1)
  - Stability index  : ARI between labels on clean vs perturbed data
  - Runtime          : seconds vs dataset size

Run:  python mst_vs_kmeans.py            (full run, ~1-2 min)
      python mst_vs_kmeans.py --quick    (fewer trials, for a fast check)
"""
import argparse
import os
import time
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, minimum_spanning_tree
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.metrics import (adjusted_rand_score, normalized_mutual_info_score,
                             silhouette_score)
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
OUT = "results"
_trapz = getattr(np, "trapezoid", None) or np.trapz
ALGOS = ["K-Means", "MST (plain)", "MST (min-size)"]
COLORS = {"K-Means": "#d95f02", "MST (plain)": "#1b9e77", "MST (min-size)": "#7570b3"}


# --------------------------------------------------------------------------
# Clustering algorithms
# --------------------------------------------------------------------------
def mst_cluster(X, k, min_size=1):
    """MST clustering: remove heaviest MST edges until k 'big' components exist.

    min_size=1  -> classic Zahn: cut exactly the k-1 heaviest edges.
    min_size>1  -> components smaller than min_size are labelled -1 (noise)
                   and do NOT count toward k, so outliers stop eating cuts.
    """
    n = len(X)
    D = squareform(pdist(X))
    T = minimum_spanning_tree(D).tocoo()
    order = np.argsort(-T.data)
    rows, cols = T.row[order], T.col[order]
    n_edges = len(rows)

    labels = np.zeros(n, dtype=int)
    for m in range(k - 1, n_edges + 1):          # m = number of edges cut
        keep = slice(m, n_edges)
        G = coo_matrix((np.ones(n_edges - m), (rows[keep], cols[keep])), shape=(n, n))
        _, labels = connected_components(G, directed=False)
        sizes = np.bincount(labels)
        if (sizes >= min_size).sum() >= k:
            break

    if min_size > 1:
        sizes = np.bincount(labels)
        labels = np.where(sizes[labels] < min_size, -1, labels)
    return labels


def run_algo(name, X, k, seed):
    if name == "K-Means":
        return KMeans(n_clusters=k, n_init=10, random_state=seed).fit_predict(X)
    if name == "MST (plain)":
        return mst_cluster(X, k, min_size=1)
    if name == "MST (min-size)":
        return mst_cluster(X, k, min_size=max(5, int(0.03 * len(X))))
    raise ValueError(name)


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
DATASETS = {          # name -> (k, generator)
    "Blobs":       3,
    "Anisotropic": 3,
    "Moons":       2,
    "Circles":     2,
}


def make_data(name, n, seed):
    if name == "Blobs":
        X, y = make_blobs(n, centers=3, cluster_std=1.0, random_state=seed)
    elif name == "Anisotropic":
        X, y = make_blobs(n, centers=3, cluster_std=0.8, random_state=seed)
        X = X @ np.array([[0.6, -0.65], [-0.2, 0.85]])
    elif name == "Moons":
        X, y = make_moons(n, noise=0.06, random_state=seed)
    elif name == "Circles":
        X, y = make_circles(n, noise=0.04, factor=0.5, random_state=seed)
    else:
        raise ValueError(name)
    return StandardScaler().fit_transform(X), y


def add_noise(X, sigma, rng):
    return X + rng.normal(0, sigma, X.shape)


def add_outliers(X, y, frac, rng):
    """Append frac*n uniform random points in the (expanded) bounding box."""
    m = int(round(frac * len(X)))
    if m == 0:
        return X.copy(), y.copy(), np.ones(len(X), bool)
    lo, hi = X.min(0), X.max(0)
    pad = 0.25 * (hi - lo)
    out = rng.uniform(lo - pad, hi + pad, size=(m, X.shape[1]))
    Xo = np.vstack([X, out])
    yo = np.concatenate([y, -np.ones(m, dtype=int)])
    return Xo, yo, yo >= 0                      # mask of true inliers


# --------------------------------------------------------------------------
# Experiments
# --------------------------------------------------------------------------
def safe_sil(X, lab):
    mask = lab >= 0
    if len(np.unique(lab[mask])) < 2 or mask.sum() < 3:
        return np.nan
    return silhouette_score(X[mask], lab[mask])


def perturbation_experiment(kind, levels, n, trials):
    rows = []
    for ds, k in DATASETS.items():
        for t in range(trials):
            X0, y0 = make_data(ds, n, seed=t)
            base = {a: run_algo(a, X0, k, t) for a in ALGOS}
            for lvl in levels:
                rng = np.random.default_rng(1000 * t + int(lvl * 1000))
                if kind == "noise":
                    X, y, inl = add_noise(X0, lvl, rng), y0, np.ones(len(X0), bool)
                else:
                    X, y, inl = add_outliers(X0, y0, lvl, rng)
                for a in ALGOS:
                    lab = run_algo(a, X, k, t)
                    # stability: compare with clean-run labels on the shared points
                    shared = np.arange(len(X0))
                    stab = adjusted_rand_score(base[a], lab[shared])
                    rows.append(dict(
                        experiment=kind, dataset=ds, algo=a, level=lvl, trial=t,
                        ARI=adjusted_rand_score(y[inl], lab[inl]),
                        NMI=normalized_mutual_info_score(y[inl], lab[inl]),
                        silhouette=safe_sil(X, lab),
                        stability=stab))
    return pd.DataFrame(rows)


def clean_experiment(n, trials):
    rows = []
    for ds, k in DATASETS.items():
        for t in range(trials):
            X, y = make_data(ds, n, seed=t)
            for a in ALGOS:
                lab = run_algo(a, X, k, t)
                rows.append(dict(dataset=ds, algo=a, trial=t,
                                 ARI=adjusted_rand_score(y, lab),
                                 NMI=normalized_mutual_info_score(y, lab),
                                 silhouette=safe_sil(X, lab)))
    return pd.DataFrame(rows)


def runtime_experiment(sizes, reps=3):
    rows = []
    for n in sizes:
        X, _ = make_data("Blobs", n, seed=0)
        for a in ALGOS:
            ts = []
            for r in range(reps):
                t0 = time.perf_counter()
                run_algo(a, X, 3, r)
                ts.append(time.perf_counter() - t0)
            rows.append(dict(n=n, algo=a, seconds=np.mean(ts)))
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Robustness summary
# --------------------------------------------------------------------------
def summarise(df):
    """One row per (experiment, dataset, algo) with the robustness measures."""
    out = []
    for (e, ds, a), g in df.groupby(["experiment", "dataset", "algo"]):
        m = g.groupby("level")[["ARI", "stability"]].mean()
        lv = m.index.values
        auc = _trapz(m["ARI"].values, lv) / (lv[-1] - lv[0])
        clean = m["ARI"].iloc[0]
        worst = m["ARI"].iloc[-1]
        out.append(dict(
            experiment=e, dataset=ds, algo=a,
            ARI_clean=round(clean, 3),
            ARI_worst=round(worst, 3),
            retention=round(worst / clean, 3) if clean > 0.05 else np.nan,
            robustness_AUC=round(auc, 3),
            mean_stability=round(m["stability"].mean(), 3)))
    return pd.DataFrame(out)


# --------------------------------------------------------------------------
# Plots
# --------------------------------------------------------------------------
def plot_curves(df, kind, xlabel, fname):
    fig, axes = plt.subplots(1, len(DATASETS), figsize=(4.2 * len(DATASETS), 3.6), sharey=True)
    for ax, ds in zip(axes, DATASETS):
        for a in ALGOS:
            g = df[(df.dataset == ds) & (df.algo == a)].groupby("level")["ARI"]
            mu, sd = g.mean(), g.std()
            ax.plot(mu.index, mu.values, "o-", color=COLORS[a], label=a, lw=2, ms=4)
            ax.fill_between(mu.index, mu - sd, mu + sd, color=COLORS[a], alpha=0.15)
        ax.set_title(ds); ax.set_xlabel(xlabel); ax.grid(alpha=0.3)
        ax.set_ylim(-0.1, 1.05)
    axes[0].set_ylabel("ARI (vs ground truth)")
    axes[0].legend(fontsize=8)
    fig.suptitle(f"Robustness to {kind} (mean ± std over trials)", y=1.02)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), dpi=140, bbox_inches="tight")
    plt.close(fig)


def plot_qualitative(condition, n, fname):
    fig, axes = plt.subplots(len(DATASETS), len(ALGOS), figsize=(3.6 * len(ALGOS), 3.1 * len(DATASETS)))
    for i, (ds, k) in enumerate(DATASETS.items()):
        X0, y0 = make_data(ds, n, seed=0)
        rng = np.random.default_rng(7)
        if condition == "clean":
            X, y, inl = X0, y0, np.ones(len(X0), bool)
        elif condition == "noise":
            X, y, inl = add_noise(X0, 0.15, rng), y0, np.ones(len(X0), bool)
        else:
            X, y, inl = add_outliers(X0, y0, 0.10, rng)
        for j, a in enumerate(ALGOS):
            lab = run_algo(a, X, k, 0)
            ari = adjusted_rand_score(y[inl], lab[inl])
            ax = axes[i, j]
            ax.scatter(X[:, 0], X[:, 1], c=lab, cmap="tab10", s=10)
            if condition == "outliers":
                ax.scatter(X[~inl, 0], X[~inl, 1], facecolors="none", edgecolors="k", s=22, lw=0.6)
            ax.set_title(f"{ds} | {a}\nARI={ari:.2f}", fontsize=9)
            ax.set_xticks([]); ax.set_yticks([])
    titles = {"clean": "clean data", "noise": "noise σ=0.15", "outliers": "10% outliers (circled)"}
    fig.suptitle(f"Cluster assignments — {titles[condition]}", y=1.0)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), dpi=130, bbox_inches="tight")
    plt.close(fig)


def plot_runtime(df, fname):
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    for a in ALGOS:
        g = df[df.algo == a]
        ax.plot(g.n, g.seconds, "o-", color=COLORS[a], label=a, lw=2)
    ax.set_xlabel("number of points"); ax.set_ylabel("seconds")
    ax.set_title("Runtime scaling"); ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), dpi=140)
    plt.close(fig)


def plot_heatmap(summary, fname):
    s = summary.copy()
    s["case"] = s.experiment + " | " + s.dataset
    piv = s.pivot(index="case", columns="algo", values="robustness_AUC")[ALGOS]
    fig, ax = plt.subplots(figsize=(6, 0.45 * len(piv) + 1.5))
    im = ax.imshow(piv.values, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(ALGOS))); ax.set_xticklabels(ALGOS, fontsize=8)
    ax.set_yticks(range(len(piv))); ax.set_yticklabels(piv.index, fontsize=8)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            ax.text(j, i, f"{piv.values[i, j]:.2f}", ha="center", va="center", fontsize=8)
    ax.set_title("Robustness AUC (mean ARI across levels)")
    fig.colorbar(im, ax=ax, fraction=0.04)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, fname), dpi=140)
    plt.close(fig)


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--n", type=int, default=300, help="points per dataset")
    args = ap.parse_args()
    trials = 3 if args.quick else 10
    os.makedirs(OUT, exist_ok=True)

    noise_levels = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    out_levels = [0.0, 0.02, 0.05, 0.10, 0.15, 0.20]

    print("[1/4] Noise experiment ...")
    df_noise = perturbation_experiment("noise", noise_levels, args.n, trials)
    print("[2/4] Outlier experiment ...")
    df_out = perturbation_experiment("outliers", out_levels, args.n, trials)
    print("[3/4] Clean / non-linear experiment ...")
    df_clean = clean_experiment(args.n, trials)
    print("[4/4] Runtime experiment ...")
    df_rt = runtime_experiment([200, 500, 1000, 2000] if not args.quick else [200, 500])

    raw = pd.concat([df_noise, df_out])
    raw.to_csv(os.path.join(OUT, "raw_results.csv"), index=False)
    summary = summarise(raw)
    summary.to_csv(os.path.join(OUT, "robustness_summary.csv"), index=False)
    clean_tbl = (df_clean.groupby(["dataset", "algo"])[["ARI", "NMI", "silhouette"]]
                 .agg(["mean", "std"]).round(3))
    clean_tbl.to_csv(os.path.join(OUT, "nonlinear_clean_results.csv"))
    df_rt.to_csv(os.path.join(OUT, "runtime.csv"), index=False)

    plot_curves(df_noise, "Gaussian noise", "noise σ (standardised units)", "noise_robustness.png")
    plot_curves(df_out, "outliers", "outlier fraction", "outlier_robustness.png")
    for c in ["clean", "noise", "outliers"]:
        plot_qualitative(c, args.n, f"clusters_{c}.png")
    plot_runtime(df_rt, "runtime.png")
    plot_heatmap(summary, "robustness_heatmap.png")

    pd.set_option("display.width", 200)
    print("\n=== Non-linear / clean performance (mean over trials) ===")
    print(df_clean.groupby(["dataset", "algo"])[["ARI", "NMI", "silhouette"]].mean().round(3))
    print("\n=== Robustness summary ===")
    print(summary.to_string(index=False))
    overall = summary.groupby(["experiment", "algo"])["robustness_AUC"].mean().round(3).unstack()
    print("\n=== Mean Robustness AUC (higher = more robust) ===")
    print(overall[ALGOS])
    print(f"\nAll files written to ./{OUT}/")


if __name__ == "__main__":
    main()
