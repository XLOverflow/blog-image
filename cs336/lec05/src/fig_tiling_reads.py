from style import *
N, Tt = 8, 4
fig, ax = canvas(11, 5.2)
T(ax, 5.5, 4.85, f"Tiling 前后，同一个输入元素被读取的次数（示意：N = {N}，T = {Tt}）", fontsize=14.5)
def strip(y, kinds):
    x = 3.0
    for k in kinds:
        c, bg = (B2, BG2) if k == "g" else (B1, BG1)
        box(ax, x, y-0.3, 0.6, 0.6, bg, c, lw=1.5, r=0.06); T(ax, x+0.3, y, "G" if k == "g" else "S", color=c, fontsize=11.5)
        x += 0.72
# naive
T(ax, 1.5, 3.75, "不做 tiling", fontsize=13)
strip(3.75, "g"*N)
T(ax, 3.0, 3.2, f"N = {N} 次，全部读 global memory", ha="left", fontsize=11.5, color=B2)
# tiled
T(ax, 1.5, 2.3, "做 tiling", fontsize=13)
strip(2.3, "g"*(N//Tt)); 
x0 = 3.0 + 0.72*(N//Tt) + 0.5
x = x0
for g in range(N//Tt):
    for j in range(Tt):
        box(ax, x, 2.0, 0.6, 0.6, BG1, B1, lw=1.5, r=0.06); T(ax, x+0.3, 2.3, "S", color=B1, fontsize=11.5); x += 0.72
    x += 0.25
T(ax, 3.0, 1.75, f"N/T = {N//Tt} 次 global", ha="left", fontsize=11.5, color=B2)
T(ax, x0, 1.75, f"N = {N} 次 shared memory（每次载入后用 T = {Tt} 次）", ha="left", fontsize=11.5, color=B1)
box(ax, 0.3, 0.25, 10.4, 1.0, GR, LINE, r=0.12)
box(ax, 0.55, 0.78, 0.36, 0.3, BG2, B2, lw=1.3, r=0.04); T(ax, 0.73, 0.93, "G", color=B2, fontsize=9.5)
T(ax, 1.05, 0.93, "读 global memory（慢）", ha="left", fontsize=11)
box(ax, 3.6, 0.78, 0.36, 0.3, BG1, B1, lw=1.3, r=0.04); T(ax, 3.78, 0.93, "S", color=B1, fontsize=9.5)
T(ax, 4.1, 0.93, "读 shared memory（在 SM 内部，快得多）", ha="left", fontsize=11)
T(ax, 0.55, 0.5, "数据被用到的总次数没有变。变的是从哪里读：对 global memory 的读取降到原来的 1/T。", ha="left", fontsize=11.5, color=OK)
save(fig, "12-tiling-reads.png")
