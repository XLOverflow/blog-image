"""Shared style for CS336 note figures. Run each fig_*.py from this folder; output goes to ../"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
plt.rcParams["font.family"] = ["WenQuanYi Zen Hei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "dejavusans"
INK="#1f2933"; MUTE="#627d98"; LINE="#cbd2d9"; GR="#f3f5f7"
B1="#2f6fde"; BG1="#e8f0fe"; B2="#d9622b"; BG2="#fdeee6"; OK="#1f8a4c"; BGOK="#e6f4ec"

def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    return fig, ax
def box(ax, x, y, w, h, fc="white", ec=LINE, lw=1.4, r=0.08, **k):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, **k))
def cell(ax, x, y, w, h, fc, ec="white", lw=1.0):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw))
def T(ax, x, y, s, **k):
    k.setdefault("color", INK); k.setdefault("ha", "center"); k.setdefault("va", "center"); k.setdefault("fontsize", 12)
    ax.text(x, y, s, **k)
def arrow(ax, p, q, color=MUTE, lw=1.6, ms=14):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw))
def save(fig, name):
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", name)
    fig.savefig(out, bbox_inches="tight", facecolor="white", pad_inches=0.15)
    plt.close(fig)
