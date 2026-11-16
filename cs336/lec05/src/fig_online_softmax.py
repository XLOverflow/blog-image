"""Worked example of online softmax, English labels so one image serves both language versions."""
import math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams["font.family"] = ["DejaVu Sans"]
INK = "#222222"; MUTE = "#777777"; A = "#3b82c4"; B = "#e07b39"

fig, ax = plt.subplots(figsize=(10, 4.3), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.3); ax.axis("off")
e = math.exp
scores = [1, 3, 5, 2]
l1 = e(-2) + 1; a = e(-2); l2 = a * l1 + 1 + e(-3)

# score row
ax.text(0.2, 3.55, "scores of one query", fontsize=12, color=INK, va="center")
xs = [3.2, 4.0, 5.6, 6.4]
for i, (s, x) in enumerate(zip(scores, xs)):
    c = A if i < 2 else B
    ax.add_patch(Rectangle((x, 3.2), 0.8, 0.7, fc=c, ec="white", lw=2))
    ax.text(x + 0.4, 3.55, str(s), fontsize=16, color="white", ha="center", va="center")
ax.text(4.0, 4.08, "tile 1", fontsize=11.5, color=A, ha="center")
ax.text(6.4, 4.08, "tile 2", fontsize=11.5, color=B, ha="center")

# table
cols = [0.2, 3.2, 6.6]
ax.text(cols[1], 2.65, "after tile 1", fontsize=12, color=A, weight="bold")
ax.text(cols[2], 2.65, "after tile 2", fontsize=12, color=B, weight="bold")
ax.plot([0.2, 9.8], [2.42, 2.42], color="#bbbbbb", lw=1)
rows = [
    ("m   running max",        "3",                         "max(3, 5) = 5"),
    ("α = exp(m_old − m_new)", "—",                         f"exp(3 − 5) = {a:.3f}"),
    ("p = exp(s − m)",         f"[{e(-2):.3f}, 1]",         f"[1, {e(-3):.3f}]"),
    ("ℓ = α·ℓ_old + sum(p)",   f"{l1:.3f}",                 f"{a:.3f}·{l1:.3f} + {1+e(-3):.3f} = {l2:.3f}"),
]
y = 2.1
for name, v1, v2 in rows:
    ax.text(cols[0], y, name, fontsize=11.5, color=INK, va="center")
    ax.text(cols[1], y, v1, fontsize=11.5, color=INK, va="center")
    ax.text(cols[2], y, v2, fontsize=11.5, color=INK, va="center")
    y -= 0.42
ax.plot([0.2, 9.8], [0.62, 0.62], color="#bbbbbb", lw=1)
w = [e(s - 5) / l2 for s in scores]
ax.text(0.2, 0.3, "weights = exp(s − 5) / ℓ = [" + ", ".join(f"{v:.3f}" for v in w) + "]   = softmax([1, 3, 5, 2])",
        fontsize=11.5, color=INK, va="center")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "17-online-softmax-example.png")
fig.savefig(out, bbox_inches="tight", facecolor="white", pad_inches=0.12)
