import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams["font.family"] = ["WenQuanYi Zen Hei","DejaVu Sans"]; plt.rcParams["axes.unicode_minus"]=False
plt.rcParams["mathtext.fontset"] = "dejavusans"
INK="#1f2933"; MUTE="#627d98"; B1="#2f6fde"; B2="#d9622b"; BG1="#e8f0fe"; BG2="#fdeee6"; GR="#f3f5f7"; OK="#1f8a4c"

fig, ax = plt.subplots(figsize=(11, 6.6), dpi=200)
ax.set_xlim(0, 11); ax.set_ylim(0, 6.6); ax.axis("off")

def box(x, y, w, h, fc, ec, lw=1.4, r=0.08):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
def T(x, y, s, **k):
    k.setdefault("color", INK); k.setdefault("ha", "center"); k.setdefault("va", "center"); k.setdefault("fontsize", 12)
    ax.text(x, y, s, **k)

T(5.5, 6.25, "Online softmax：一个 query 的 score 被切成两个 tile，逐块处理", fontsize=15, weight="bold")

# score row
scores=[1,3,5,2]; xs=[3.1,4.1,5.9,6.9]
T(1.7, 5.3, "score（一行）", fontsize=12, color=MUTE)
for i,(s,x) in enumerate(zip(scores,xs)):
    c,bg = (B1,BG1) if i<2 else (B2,BG2)
    box(x, 4.95, 0.9, 0.7, bg, c)
    T(x+0.45, 5.3, str(s), fontsize=17, weight="bold", color=c)
T(4.05, 5.85, "tile 1", color=B1, fontsize=12, weight="bold")
T(6.85, 5.85, "tile 2", color=B2, fontsize=12, weight="bold")
ax.plot([5.45,5.45],[4.85,5.75], color=MUTE, lw=1.2, ls=(0,(4,3)))

# panels
def panel(x, title, c, bg, lines):
    box(x, 1.55, 4.65, 3.0, "white", c, lw=1.6, r=0.12)
    box(x, 4.05, 4.65, 0.5, bg, c, lw=1.6, r=0.12)
    T(x+2.32, 4.3, title, color=c, weight="bold", fontsize=12.5)
    y=3.65
    for name, expr, val in lines:
        T(x+0.25, y, name, ha="left", fontsize=12, weight="bold")
        T(x+1.0, y, expr, ha="left", fontsize=11.5, color=MUTE)
        T(x+4.45, y, val, ha="right", fontsize=12.5, weight="bold")
        y-=0.5
e=math.exp
l1=e(-2)+1; a=e(-2); l2=a*l1+1+e(-3)
panel(0.3, "处理 tile 1：score = [1, 3]", B1, BG1, [
 ("m", "= max(-∞, 1, 3)", "3"),
 ("α", "= exp(m旧 - m新)，首块没有旧值", "—"),
 ("p", "= exp([1, 3] - 3)", f"[{e(-2):.3f}, 1]"),
 ("$\\ell$", "= 0 + sum(p)", f"{l1:.3f}"),
])
panel(6.05, "处理 tile 2：score = [5, 2]", B2, BG2, [
 ("m", "= max(3, 5, 2)", "5"),
 ("α", "= exp(3 - 5)，旧值换新基准", f"{a:.3f}"),
 ("p", "= exp([5, 2] - 5)", f"[1, {e(-3):.3f}]"),
 ("$\\ell$", f"= {a:.3f} × {l1:.3f} + sum(p)", f"{l2:.3f}"),
])
ax.add_patch(FancyArrowPatch((5.05,2.9),(5.95,2.9), arrowstyle="-|>", mutation_scale=16, color=MUTE, lw=1.6))
T(5.5, 3.3, "只带走\nm 和 $\\ell$", fontsize=10.5, color=MUTE)

# result
box(0.3, 0.25, 10.4, 1.0, GR, "#cbd2d9", lw=1.2, r=0.12)
w=[e(s-5)/l2 for s in scores]
T(0.65, 0.92, "最后统一除以 $\\ell$：", ha="left", fontsize=12, weight="bold")
T(3.0, 0.92, "权重 = exp(score - 5) / 1.203 = [" + ", ".join(f"{v:.3f}" for v in w) + "]", ha="left", fontsize=12)
T(0.65, 0.52, "和一次性算 softmax([1, 3, 5, 2]) 完全一致，但任何时刻只需要当前 tile 的 score 和两个标量 m、$\\ell$。", ha="left", fontsize=11.5, color=OK)
fig.savefig(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "..", "17-online-softmax.png"), bbox_inches="tight", facecolor="white", pad_inches=0.15)
import numpy as np; x=np.array(scores,float); print(np.exp(x-x.max())/np.exp(x-x.max()).sum(), w)
