from style import *
fig, ax = canvas(11, 6.0)
T(ax, 5.5, 5.65, "Wave quantization：A100 有 108 个 SM，一批（wave）最多同时跑 108 个 tile", fontsize=14)
def grid(x0, y0, filled, c, label):
    s = 0.2
    for i in range(108):
        r, col = divmod(i, 18)
        cell(ax, x0 + col*s, y0 - r*s, s, s, c if i < filled else "#e4e7eb", ec="white", lw=0.8)
    T(ax, x0 + 1.8, y0 - 1.25, label, fontsize=11, color=MUTE)
# left
box(ax, 0.3, 0.3, 4.6, 4.9, "white", LINE, r=0.12)
T(ax, 2.6, 4.85, "边长 1792", fontsize=13.5)
T(ax, 2.6, 4.45, "7 × 14 = 98 个 tile", fontsize=12, color=B1)
grid(0.8, 3.95, 98, B1, "wave 1：98 个 SM 在工作")
T(ax, 2.6, 0.75, "总时间约 1 个 wave", fontsize=12.5, color=OK)
# right
box(ax, 5.2, 0.3, 5.5, 4.9, "white", LINE, r=0.12)
T(ax, 7.95, 4.85, "边长 1793（只大了 1）", fontsize=13.5)
T(ax, 7.95, 4.45, "8 × 15 = 120 个 tile", fontsize=12, color=B2)
grid(6.15, 3.95, 108, B2, "wave 1：108 个 SM 全满")
grid(6.15, 2.35, 12, B2, "wave 2：只有 12 个在工作，96 个空闲")
T(ax, 7.95, 0.62, "总时间约 2 个 wave，计算量几乎没变", fontsize=12.5, color=B2)
save(fig, "15-wave-quantization.png")
