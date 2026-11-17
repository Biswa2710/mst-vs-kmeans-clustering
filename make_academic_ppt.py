"""
Generate a publication-grade, human-crafted academic presentation (.pptx)
Aesthetic: Nature / Science / Stanford CS Research Briefing style.
No AI emojis, no generic fluff cards, clean editorial typography.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

# ── Palette: Clean Academic Editorial ─────────────────────────────
BG_LIGHT    = RGBColor(0xFA, 0xFA, 0xF9)   # pristine gallery paper (#fafaf9)
BG_WHITE    = RGBColor(0xFF, 0xFF, 0xFF)   # pure white card
INK_PRIMARY = RGBColor(0x18, 0x1A, 0x1E)   # deep charcoal ink (#181a1e)
INK_MUTED   = RGBColor(0x5E, 0x66, 0x72)   # slate secondary text (#5e6672)
INK_FAINT   = RGBColor(0x8E, 0x97, 0xA4)   # metadata / rule color
ACCENT_BLUE = RGBColor(0x00, 0x47, 0xAB)   # International Klein / Cobalt Blue
ACCENT_DARK = RGBColor(0x0D, 0x1A, 0x30)   # deep navy
RULE_COLOR  = RGBColor(0xE2, 0xE5, 0xEA)   # subtle hairline rule
ORANGE_DARK = RGBColor(0xB8, 0x47, 0x00)   # K-Means identifier
GREEN_DARK  = RGBColor(0x13, 0x73, 0x54)   # MST identifier
CARD_BG     = RGBColor(0xF2, 0xF4, 0xF7)   # soft neutral card

W = Inches(13.333)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
blank = prs.slide_layouts[6]

RESULTS_DIR = "results"

# ── Helper Functions ──────────────────────────────────────────────
def set_slide_bg(slide, color=BG_LIGHT):
    shape = slide.shapes.add_shape(1, 0, 0, W, H)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()

def add_header(slide, section_tag, slide_number, title, subtitle=None):
    # Top rule
    rule = slide.shapes.add_shape(1, Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.015))
    rule.fill.solid()
    rule.fill.fore_color.rgb = RULE_COLOR
    rule.line.fill.background()

    # Section Tag & Slide Number
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.35))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = section_tag.upper()
    r1.font.size = Pt(9.5)
    r1.font.bold = True
    r1.font.color.rgb = ACCENT_BLUE

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.RIGHT
    r2 = p2.add_run()
    r2.text = f"{slide_number:02d} / 10"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = INK_FAINT

    # Main Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.733), Inches(0.6))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title
    r_t.font.size = Pt(24)
    r_t.font.bold = True
    r_t.font.color.rgb = INK_PRIMARY

    if subtitle:
        p_sub = tf_t.add_paragraph()
        r_sub = p_sub.add_run()
        r_sub.text = subtitle
        r_sub.font.size = Pt(13)
        r_sub.font.color.rgb = INK_MUTED

def add_card(slide, x, y, w, h, bg_color=BG_WHITE, border_color=RULE_COLOR):
    shape = slide.shapes.add_shape(1, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

# ══════════════════════════════════════════════════════════════════
# SLIDE 1: TITLE / COVER (Academic Monograph Style)
# ══════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(blank)
set_slide_bg(s1, BG_WHITE)

# Blue accent header bar
bar = s1.shapes.add_shape(1, Inches(0.8), Inches(1.1), Inches(1.2), Inches(0.06))
bar.fill.solid()
bar.fill.fore_color.rgb = ACCENT_BLUE
bar.line.fill.background()

tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True

p_sub = tf.paragraphs[0]
r_sub = p_sub.add_run()
r_sub.text = "RESEARCH MONOGRAPH · PATTERN RECOGNITION & UNSUPERVISED LEARNING"
r_sub.font.size = Pt(11)
r_sub.font.bold = True
r_sub.font.color.rgb = ACCENT_BLUE

p_title = tf.add_paragraph()
p_title.space_before = Pt(14)
r_title = p_title.add_run()
r_title.text = "Comparative Robustness of MST Clustering vs. K-Means"
r_title.font.size = Pt(36)
r_title.font.bold = True
r_title.font.color.rgb = INK_PRIMARY

p_lead = tf.add_paragraph()
p_lead.space_before = Pt(14)
r_lead = p_lead.add_run()
r_lead.text = "An empirical dissection of graph-theoretic edge cutting versus centroid optimization under Gaussian feature jitter, uniform outliers, and non-linear manifold geometry."
r_lead.font.size = Pt(16)
r_lead.font.color.rgb = INK_MUTED

# Divider rule
rule = s1.shapes.add_shape(1, Inches(0.8), Inches(4.7), Inches(11.733), Inches(0.015))
rule.fill.solid(); rule.fill.fore_color.rgb = RULE_COLOR; rule.line.fill.background()

# Metadata Footer Grid
meta_items = [
    ("AUTHORS", "Biswa & Anurag"),
    ("DISCIPLINE", "Machine Learning / Pattern Mining"),
    ("CORE CONTRIBUTION", "Min-Size Pruning Heuristic (+803% Outlier AUC)"),
    ("CODE & DATA", "github.com/Biswa2710/mst-vs-kmeans-clustering"),
]
for i, (label, val) in enumerate(meta_items):
    col_x = Inches(0.8 + i * 2.95)
    tb_m = s1.shapes.add_textbox(col_x, Inches(5.0), Inches(2.8), Inches(1.5))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p1 = tf_m.paragraphs[0]
    r1 = p1.add_run()
    r1.text = label
    r1.font.size = Pt(9)
    r1.font.bold = True
    r1.font.color.rgb = INK_FAINT
    
    p2 = tf_m.add_paragraph()
    p2.space_before = Pt(4)
    r2 = p2.add_run()
    r2.text = val
    r2.font.size = Pt(12)
    r2.font.bold = (i == 0 or i == 2)
    r2.font.color.rgb = ACCENT_BLUE if i == 2 else INK_PRIMARY

# ══════════════════════════════════════════════════════════════════
# SLIDE 2: THE THEORETICAL PROBLEM (Convexity vs. Topology)
# ══════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(blank)
set_slide_bg(s2, BG_LIGHT)
add_header(s2, "Theoretical Foundations", 2, "Convexity Bias vs. Topological Neighborhood Continuity", 
           "Why standard clustering algorithms fail when data departs from idealized spherical Gaussian assumptions.")

cards_s2 = [
    ("PARADIGM 1", "K-Means (Lloyd's Optimization)", ORANGE_DARK,
     "Minimizes within-cluster sum of squares (WCSS) around k geometric centroids.\n\n"
     "• Mathematical Assumption: Clusters are convex, isotropic, and linearly separable.\n"
     "• Decision Boundary: Planar Voronoi polyhedra (flat hyperplanes).\n"
     "• Structural Flaw: Cannot envelop non-convex structures (concentric rings or interlocking arcs)."),
    
    ("PARADIGM 2", "Zahn's Classic MST (Plain Graph Cut)", GREEN_DARK,
     "Builds the Minimum Spanning Tree of pairwise distances, then severs the k-1 heaviest edges.\n\n"
     "• Mathematical Assumption: Clusters are high-density components separated by empty gaps.\n"
     "• Decision Boundary: Non-parametric graph connected components.\n"
     "• Structural Flaw: Fragile to peripheral outliers; a single noise point monopolizes a cut."),
    
    ("PARADIGM 3", "Noise-Pruned MST (MST min-size)", ACCENT_BLUE,
     "Continues cutting edges past k-1 until k clusters with cardinality >= 3% N exist.\n\n"
     "• Innovation: Isolates micro-fragments smaller than 3% N as background noise (-1).\n"
     "• Decision Boundary: Manifold-adaptive with outlier rejection.\n"
     "• Empirical Advantage: Combines non-linear manifold discovery with robust outlier immunity.")
]

for i, (tag, name, col, body) in enumerate(cards_s2):
    cx = Inches(0.8 + i * 3.95)
    add_card(s2, cx, Inches(1.8), Inches(3.75), Inches(5.0))
    
    # Colored top indicator
    top_bar = s2.shapes.add_shape(1, cx, Inches(1.8), Inches(3.75), Inches(0.06))
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = col; top_bar.line.fill.background()
    
    tb_c = s2.shapes.add_textbox(cx + Inches(0.25), Inches(2.05), Inches(3.25), Inches(4.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    
    p_tag = tf_c.paragraphs[0]
    r_tag = p_tag.add_run()
    r_tag.text = tag
    r_tag.font.size = Pt(9)
    r_tag.font.bold = True
    r_tag.font.color.rgb = col
    
    p_name = tf_c.add_paragraph()
    p_name.space_before = Pt(4)
    r_name = p_name.add_run()
    r_name.text = name
    r_name.font.size = Pt(15)
    r_name.font.bold = True
    r_name.font.color.rgb = INK_PRIMARY
    
    p_body = tf_c.add_paragraph()
    p_body.space_before = Pt(12)
    r_body = p_body.add_run()
    r_body.text = body
    r_body.font.size = Pt(11.5)
    r_body.font.color.rgb = INK_MUTED

# ══════════════════════════════════════════════════════════════════
# SLIDE 3: BENCHMARK SUITE (Four Synthetic Topologies)
# ══════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(blank)
set_slide_bg(s3, BG_LIGHT)
add_header(s3, "Experimental Design", 3, "Four Benchmark Topologies & Controlled Perturbations",
           "Standardized 2D testbeds evaluated across 10 randomized Monte-Carlo trials (N = 300 points).")

# Left Column: Image embedding
add_card(s3, Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.0))
img_path = os.path.join(RESULTS_DIR, "clusters_clean.png")
if os.path.exists(img_path):
    s3.shapes.add_picture(img_path, Inches(0.95), Inches(1.95), Inches(6.5), Inches(4.7))

# Right Column: Analytical Description
add_card(s3, Inches(7.8), Inches(1.8), Inches(4.733), Inches(5.0))
tb_r = s3.shapes.add_textbox(Inches(8.05), Inches(2.0), Inches(4.2), Inches(4.5))
tf_r = tb_r.text_frame
tf_r.word_wrap = True

sections_s3 = [
    ("ISOTROPIC BLOBS (k = 3)", "Three symmetric Gaussian distributions (std = 1.0). Serves as the optimal baseline domain for K-Means."),
    ("ANISOTROPIC BLOBS (k = 3)", "Rotated and sheared ellipsoidal clusters with non-diagonal covariance matrices to test orientation sensitivity."),
    ("INTERLEAVING MOONS (k = 2)", "Two intertwined non-convex crescent manifolds. Demonstrates local density connectivity requirements."),
    ("CONCENTRIC CIRCLES (k = 2)", "Nested circular rings. Mathematically impossible for linear hyperplanes to separate without misclassification.")
]

for i, (title_t, desc_t) in enumerate(sections_s3):
    p1 = tf_r.paragraphs[0] if i == 0 else tf_r.add_paragraph()
    if i > 0: p1.space_before = Pt(14)
    r1 = p1.add_run()
    r1.text = title_t
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = INK_PRIMARY
    
    p2 = tf_r.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = desc_t
    r2.font.size = Pt(11)
    r2.font.color.rgb = INK_MUTED

# ══════════════════════════════════════════════════════════════════
# SLIDE 4: THE VORONOI FAILURE (Clean Baseline Quantitative Findings)
# ══════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(blank)
set_slide_bg(s4, BG_LIGHT)
add_header(s4, "Empirical Results", 4, "Clean Baseline: The Failure of Planar Voronoi Partitioning",
           "Mean quantitative scores across 10 randomized trials on uncorrupted manifolds.")

# Metric Table
add_card(s4, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.8))
tb_tbl = s4.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.333), Inches(2.5))
tf_tbl = tb_tbl.text_frame
tf_tbl.word_wrap = True

table_header = tf_tbl.paragraphs[0]
r_th = table_header.add_run()
r_th.text = f"{'DATASET':<22}{'K-MEANS (ARI)':<22}{'MST PLAIN (ARI)':<22}{'MST MIN-SIZE (ARI)':<24}{'VERDICT'}"
r_th.font.size = Pt(10.5)
r_th.font.bold = True
r_th.font.color.rgb = INK_FAINT

table_rows = [
    ("Concentric Circles", "-0.003 ± 0.002", "1.000 ± 0.000", "1.000 ± 0.000", "K-Means Fails Completely (ARI = 0)"),
    ("Intertwining Moons", "0.476 ± 0.012", "1.000 ± 0.000", "1.000 ± 0.000", "MST Achieves Perfect Recovery"),
    ("Gaussian Blobs", "0.907 ± 0.021", "0.626 ± 0.045", "0.767 ± 0.038", "K-Means Outperforms on Spherical"),
    ("Anisotropic Blobs", "0.820 ± 0.035", "0.683 ± 0.052", "0.770 ± 0.041", "K-Means Maintains Advantage")
]

for row in table_rows:
    p_r = tf_tbl.add_paragraph()
    p_r.space_before = Pt(8)
    r_r = p_r.add_run()
    r_r.text = f"{row[0]:<22}{row[1]:<22}{row[2]:<22}{row[3]:<24}{row[4]}"
    r_r.font.size = Pt(11.5)
    r_r.font.bold = ("Concentric" in row[0] or "Moons" in row[0])
    r_r.font.color.rgb = ACCENT_BLUE if ("1.000" in row[2]) else INK_PRIMARY

# Bottom Takeaway Cards
add_card(s4, Inches(0.8), Inches(4.9), Inches(5.7), Inches(1.9))
tb_t1 = s4.shapes.add_textbox(Inches(1.0), Inches(5.05), Inches(5.3), Inches(1.6))
tf_t1 = tb_t1.text_frame; tf_t1.word_wrap = True
p = tf_t1.paragraphs[0]; r = p.add_run(); r.text = "INSIGHT: THE CONCENTRIC PARADOX"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = ACCENT_BLUE
p2 = tf_t1.add_paragraph(); p2.space_before = Pt(4); r2 = p2.add_run()
r2.text = "Because concentric rings share identical cluster centers, K-Means produces an ARI of -0.003 (statistical noise). Yet, its Silhouette score remains high (0.353), proving that internal cluster metrics are biased toward spherical shapes."
r2.font.size = Pt(10.5); r2.font.color.rgb = INK_MUTED

add_card(s4, Inches(6.833), Inches(4.9), Inches(5.7), Inches(1.9))
tb_t2 = s4.shapes.add_textbox(Inches(7.033), Inches(5.05), Inches(5.3), Inches(1.6))
tf_t2 = tb_t2.text_frame; tf_t2.word_wrap = True
p = tf_t2.paragraphs[0]; r = p.add_run(); r.text = "TOPOLOGICAL TRACING MECHANIC"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = GREEN_DARK
p2 = tf_t2.add_paragraph(); p2.space_before = Pt(4); r2 = p2.add_run()
r2.text = "Minimum Spanning Tree edges link nearest neighbors along continuous curves. The longest tree edges naturally occur across the void between rings, allowing simple edge cutting to yield zero-error clustering."
r2.font.size = Pt(10.5); r2.font.color.rgb = INK_MUTED

# ══════════════════════════════════════════════════════════════════
# SLIDE 5: STRESS TEST 1 (Feature Noise Perturbation)
# ══════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(blank)
set_slide_bg(s5, BG_LIGHT)
add_header(s5, "Robustness Evaluation", 5, "Stress Test 1: Progressive Gaussian Feature Noise",
           "Evaluating Adjusted Rand Index retention as noise std dev sweeps from sigma = 0.00 to 0.30.")

add_card(s5, Inches(0.8), Inches(1.8), Inches(7.5), Inches(5.0))
img_path2 = os.path.join(RESULTS_DIR, "noise_robustness.png")
if os.path.exists(img_path2):
    s5.shapes.add_picture(img_path2, Inches(0.95), Inches(1.95), Inches(7.2), Inches(4.7))

add_card(s5, Inches(8.5), Inches(1.8), Inches(4.033), Inches(5.0))
tb_s5 = s5.shapes.add_textbox(Inches(8.75), Inches(2.0), Inches(3.5), Inches(4.5))
tf_s5 = tb_s5.text_frame; tf_s5.word_wrap = True

p = tf_s5.paragraphs[0]; r = p.add_run(); r.text = "OVERALL NOISE AUC"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = INK_FAINT
scores_noise = [
    ("MST (min-size)", "0.618", ACCENT_BLUE, "Highest robustness overall"),
    ("K-Means", "0.534", ORANGE_DARK, "Stable on blobs, failed on rings"),
    ("MST (plain)", "0.463", GREEN_DARK, "Spurious bridge degradation")
]
for name_s, val_s, col_s, note_s in scores_noise:
    p_n = tf_s5.add_paragraph(); p_n.space_before = Pt(6)
    r_n = p_n.add_run(); r_n.text = f"{name_s}: {val_s}"; r_n.font.size = Pt(15); r_n.font.bold = True; r_n.font.color.rgb = col_s
    p_sub = tf_s5.add_paragraph(); r_sub = p_sub.add_run(); r_sub.text = note_s; r_sub.font.size = Pt(10.5); r_sub.font.color.rgb = INK_MUTED

p_div = tf_s5.add_paragraph(); p_div.space_before = Pt(14)
r_div = p_div.add_run(); r_div.text = "CRITICAL PHENOMENON:\nGaussian noise pushes peripheral points into low-density zones. Plain MST misinterprets these peripheral points as cluster boundaries, causing early degradation. Min-size pruning buffers against this by ignoring small perimeter fragments."
r_div.font.size = Pt(10.5); r_div.font.color.rgb = INK_PRIMARY

# ══════════════════════════════════════════════════════════════════
# SLIDE 6: STRESS TEST 2 (Catastrophic Outlier Collapse)
# ══════════════════════════════════════════════════════════════════
s6 = prs.slides.add_slide(blank)
set_slide_bg(s6, BG_LIGHT)
add_header(s6, "Robustness Evaluation", 6, "Stress Test 2: Catastrophic Collapse Under Uniform Outliers",
           "Evaluating outlier contamination from 0% to 20% uniform random points in bounding box.")

add_card(s6, Inches(0.8), Inches(1.8), Inches(7.5), Inches(5.0))
img_path3 = os.path.join(RESULTS_DIR, "outlier_robustness.png")
if os.path.exists(img_path3):
    s6.shapes.add_picture(img_path3, Inches(0.95), Inches(1.95), Inches(7.2), Inches(4.7))

add_card(s6, Inches(8.5), Inches(1.8), Inches(4.033), Inches(5.0))
tb_s6 = s6.shapes.add_textbox(Inches(8.75), Inches(2.0), Inches(3.5), Inches(4.5))
tf_s6 = tb_s6.text_frame; tf_s6.word_wrap = True

p = tf_s6.paragraphs[0]; r = p.add_run(); r.text = "OUTLIER RESISTANCE AUC"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = INK_FAINT
scores_outlier = [
    ("MST (min-size)", "0.867", ACCENT_BLUE, "+803% recovery over plain MST"),
    ("K-Means", "0.540", ORANGE_DARK, "Moderate centroid displacement"),
    ("MST (plain)", "0.096", RGBColor(0xBA, 0x1A, 0x1A), "Complete algorithmic collapse")
]
for name_s, val_s, col_s, note_s in scores_outlier:
    p_n = tf_s6.add_paragraph(); p_n.space_before = Pt(6)
    r_n = p_n.add_run(); r_n.text = f"{name_s}: {val_s}"; r_n.font.size = Pt(15); r_n.font.bold = True; r_n.font.color.rgb = col_s
    p_sub = tf_s6.add_paragraph(); r_sub = p_sub.add_run(); r_sub.text = note_s; r_sub.font.size = Pt(10.5); r_sub.font.color.rgb = INK_MUTED

p_div = tf_s6.add_paragraph(); p_div.space_before = Pt(14)
r_div = p_div.add_run(); r_div.text = "THE ZAHN HIJACKING DILEMMA:\nBecause outliers sit far away from primary clusters, their connecting MST edges have enormous weights. A classic k-1 cut algorithm wastes all of its cuts isolating solitary outlier points, leaving real clusters completely fused together!"
r_div.font.size = Pt(10.5); r_div.font.color.rgb = INK_PRIMARY

# ══════════════════════════════════════════════════════════════════
# SLIDE 7: GLOBAL ROBUSTNESS HEATMAP (Synthesis Matrix)
# ══════════════════════════════════════════════════════════════════
s7 = prs.slides.add_slide(blank)
set_slide_bg(s7, BG_LIGHT)
add_header(s7, "Comprehensive Synthesis", 7, "Robustness Integral Matrix (Mean AUC Across Levels)",
           "Numerical area under the curve (trapezoidal integration) evaluating stability across all perturbations.")

add_card(s7, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
img_path4 = os.path.join(RESULTS_DIR, "robustness_heatmap.png")
if os.path.exists(img_path4):
    s7.shapes.add_picture(img_path4, Inches(0.95), Inches(1.95), Inches(5.7), Inches(4.7))

add_card(s7, Inches(7.0), Inches(1.8), Inches(5.533), Inches(5.0))
tb_s7 = s7.shapes.add_textbox(Inches(7.25), Inches(2.0), Inches(5.0), Inches(4.5))
tf_s7 = tb_s7.text_frame; tf_s7.word_wrap = True

p_h = tf_s7.paragraphs[0]; r_h = p_h.add_run(); r_h.text = "SUMMARY OF EXPERIMENTAL METRICS"; r_h.font.size = Pt(11); r_h.font.bold = True; r_h.font.color.rgb = INK_PRIMARY

points_s7 = [
    ("MST (min-size) achieves highest overall robustness", "Wins in both noise (0.618) and outlier (0.867) scenarios by dynamic thresholding."),
    ("Retention on non-linear manifolds is 100%", "Moons and Circles retain a flawless 1.000 ARI under 20% uniform noise, where other models fail."),
    ("Plain MST is unsafe for production deployment", "With an outlier AUC of only 0.096, unpruned Zahn edge cutting cannot be trusted in noisy real-world systems."),
    ("K-Means provides consistent, bounded behavior", "Achieves 0.540 AUC under outliers, remaining viable whenever clusters are known to be spherical.")
]

for title_p, desc_p in points_s7:
    p_t = tf_s7.add_paragraph(); p_t.space_before = Pt(10)
    r_t = p_t.add_run(); r_t.text = f"• {title_p}: "; r_t.font.size = Pt(11); r_t.font.bold = True; r_t.font.color.rgb = INK_PRIMARY
    r_d = p_t.add_run(); r_d.text = desc_p; r_d.font.size = Pt(10.5); r_d.font.color.rgb = INK_MUTED

# ══════════════════════════════════════════════════════════════════
# SLIDE 8: ASYMPTOTIC COMPLEXITY & RUNTIME SCALING
# ══════════════════════════════════════════════════════════════════
s8 = prs.slides.add_slide(blank)
set_slide_bg(s8, BG_LIGHT)
add_header(s8, "Computational Complexity", 8, "Asymptotic Scaling: Linear Efficiency vs. Quadratic Graph Overhead",
           "Profiling execution latency across dataset sizes from N = 200 to N = 2000 points.")

add_card(s8, Inches(0.8), Inches(1.8), Inches(6.5), Inches(5.0))
img_path5 = os.path.join(RESULTS_DIR, "runtime.png")
if os.path.exists(img_path5):
    s8.shapes.add_picture(img_path5, Inches(0.95), Inches(1.95), Inches(6.2), Inches(4.7))

add_card(s8, Inches(7.5), Inches(1.8), Inches(5.033), Inches(5.0))
tb_s8 = s8.shapes.add_textbox(Inches(7.75), Inches(2.0), Inches(4.5), Inches(4.5))
tf_s8 = tb_s8.text_frame; tf_s8.word_wrap = True

p_c1 = tf_s8.paragraphs[0]; r_c1 = p_c1.add_run(); r_c1.text = "K-MEANS ASYMPTOTIC COMPLEXITY"; r_c1.font.size = Pt(10); r_c1.font.bold = True; r_c1.font.color.rgb = ORANGE_DARK
p_c1_b = tf_s8.add_paragraph(); r_c1_b = p_c1_b.add_run()
r_c1_b.text = "O(k · N · d · i)\nScales strictly linearly with sample size N. Executes in ~0.015 seconds for N = 2000, making it ideal for streaming or high-throughput batch pipelines."
r_c1_b.font.size = Pt(10.5); r_c1_b.font.color.rgb = INK_MUTED

p_c2 = tf_s8.add_paragraph(); p_c2.space_before = Pt(14); r_c2 = p_c2.add_run(); r_c2.text = "MST ASYMPTOTIC COMPLEXITY"; r_c2.font.size = Pt(10); r_c2.font.bold = True; r_c2.font.color.rgb = ACCENT_BLUE
p_c2_b = tf_s8.add_paragraph(); r_c2_b = p_c2_b.add_run()
r_c2_b.text = "O(N² · d) + O(N² log N)\nDense distance matrix computation and edge sorting induce quadratic growth (~0.12 seconds at N = 2000)."
r_c2_b.font.size = Pt(10.5); r_c2_b.font.color.rgb = INK_MUTED

p_c3 = tf_s8.add_paragraph(); p_c3.space_before = Pt(14); r_c3 = p_c3.add_run(); r_c3.text = "ENGINEERING MITIGATION"; r_c3.font.size = Pt(10); r_c3.font.bold = True; r_c3.font.color.rgb = GREEN_DARK
p_c3_b = tf_s8.add_paragraph(); r_c3_b = p_c3_b.add_run()
r_c3_b.text = "To scale MST to millions of observations, replace dense pairwise distance with an Approximate Nearest Neighbor graph (HNSW / Annoy) to reduce complexity to O(N log N)."
r_c3_b.font.size = Pt(10.5); r_c3_b.font.color.rgb = INK_MUTED

# ══════════════════════════════════════════════════════════════════
# SLIDE 9: PRACTITIONER ARCHITECTURAL RULES
# ══════════════════════════════════════════════════════════════════
s9 = prs.slides.add_slide(blank)
set_slide_bg(s9, BG_LIGHT)
add_header(s9, "Engineering Guidelines", 9, "Architectural Decision Framework for Practitioners",
           "Concrete, actionable criteria for selecting clustering algorithms in production systems.")

rules = [
    ("RULE 01", "Never Deploy Plain Zahn MST Without Cardinality Thresholding",
     "Unfiltered MST edge cutting collapses catastrophically (AUC = 0.096) when peripheral noise is present. Always enforce a minimum component filter (e.g. min_size >= 3% N) to quarantine rogue outliers as noise."),
    
    ("RULE 02", "Beware the Silhouette Coefficient Bias on Manifolds",
     "Internal validation metrics like Silhouette and Davies-Bouldin assume spherical convex clusters. They mathematically penalize curved manifolds—even when partitions match ground truth perfectly."),
    
    ("RULE 03", "Select Model by Domain Topology, Not Habit",
     "• Use K-Means if clusters are isotropic Gaussian blobs, latency is paramount, or sample size exceeds 500,000 observations.\n• Use Noise-Pruned MST if features describe physical manifolds, trajectory streams, or non-linear spatial geometry."),
]

for i, (tag_r, title_r, desc_r) in enumerate(rules):
    ry = Inches(1.8 + i * 1.65)
    add_card(s9, Inches(0.8), ry, Inches(11.733), Inches(1.45))
    
    tb_r = s9.shapes.add_textbox(Inches(1.0), ry + Inches(0.12), Inches(11.333), Inches(1.2))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    
    p1 = tf_r.paragraphs[0]; r1 = p1.add_run(); r1.text = tag_r; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = ACCENT_BLUE
    
    p2 = tf_r.add_paragraph(); p2.space_before = Pt(2); r2 = p2.add_run(); r2.text = title_r; r2.font.size = Pt(13); r2.font.bold = True; r2.font.color.rgb = INK_PRIMARY
    
    p3 = tf_r.add_paragraph(); p3.space_before = Pt(3); r3 = p3.add_run(); r3.text = desc_r; r3.font.size = Pt(10.5); r3.font.color.rgb = INK_MUTED

# ══════════════════════════════════════════════════════════════════
# SLIDE 10: CONCLUSION & REPRODUCIBILITY
# ══════════════════════════════════════════════════════════════════
s10 = prs.slides.add_slide(blank)
set_slide_bg(s10, BG_WHITE)
add_header(s10, "Conclusion", 10, "Summary of Findings & Open-Source Reproducibility",
           "Complete experimental codebase, Jupyter notebook, and data suites are publicly available.")

add_card(s10, Inches(0.8), Inches(1.8), Inches(7.5), Inches(5.0))
tb_s10 = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(6.9), Inches(4.5))
tf_s10 = tb_s10.text_frame; tf_s10.word_wrap = True

p_f = tf_s10.paragraphs[0]; r_f = p_f.add_run(); r_f.text = "EXECUTIVE SUMMARY"; r_f.font.size = Pt(11); r_f.font.bold = True; r_f.font.color.rgb = ACCENT_BLUE

bullets_s10 = [
    "No single clustering algorithm dominates across all geometric configurations.",
    "K-Means excels at convex spherical density estimation with minimal latency, but fails fundamentally on non-convex manifolds.",
    "Graph-theoretic MST cutting possesses extraordinary geometric flexibility, but requires cardinality pruning to survive realistic noise.",
    "Noise-Pruned MST (`MST min-size`) is the premier all-around model, achieving 0.867 outlier AUC and 1.000 non-linear ARI."
]
for b in bullets_s10:
    p_b = tf_s10.add_paragraph(); p_b.space_before = Pt(8)
    r_b = p_b.add_run(); r_b.text = f"• {b}"; r_b.font.size = Pt(11); r_b.font.color.rgb = INK_PRIMARY

p_note = tf_s10.add_paragraph(); p_note.space_before = Pt(18)
r_note = p_note.add_run()
r_note.text = "RESEARCHERS: Biswa & Anurag\nPattern Recognition & Unsupervised Learning · November 2026"
r_note.font.size = Pt(10.5); r_note.font.bold = True; r_note.font.color.rgb = INK_MUTED

# Right Column: Access & Colab Box
add_card(s10, Inches(8.5), Inches(1.8), Inches(4.033), Inches(5.0), bg_color=CARD_BG, border_color=None)
tb_acc = s10.shapes.add_textbox(Inches(8.8), Inches(2.2), Inches(3.4), Inches(4.2))
tf_acc = tb_acc.text_frame; tf_acc.word_wrap = True

p_a = tf_acc.paragraphs[0]; r_a = p_a.add_run(); r_a.text = "REPRODUCIBILITY ARTIFACTS"; r_a.font.size = Pt(10); r_a.font.bold = True; r_a.font.color.rgb = ACCENT_BLUE

artifacts = [
    ("GitHub Repository", "github.com/Biswa2710/mst-vs-kmeans-clustering"),
    ("Google Colab", "One-click interactive execution badge"),
    ("Jupyter Notebook", "mst_vs_kmeans.ipynb (all figures reproducible)"),
    ("NotebookLM Ready", "NotebookLM_Source_Document.md included for instant AI podcasts")
]
for title_a, link_a in artifacts:
    p_ar = tf_acc.add_paragraph(); p_ar.space_before = Pt(10)
    r_ar = p_ar.add_run(); r_ar.text = title_a; r_ar.font.size = Pt(11); r_ar.font.bold = True; r_ar.font.color.rgb = INK_PRIMARY
    p_l = tf_acc.add_paragraph(); r_l = p_l.add_run(); r_l.text = link_a; r_l.font.size = Pt(9.5); r_l.font.color.rgb = INK_MUTED

# Save presentation
OUT_PPTX = "MST_vs_KMeans_Academic_Deck.pptx"
prs.save(OUT_PPTX)
print(f"Successfully generated: {OUT_PPTX} ({len(prs.slides)} slides)")
