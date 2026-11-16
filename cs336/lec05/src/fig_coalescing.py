from style import *
fig, ax = canvas(11, 6.0)
T(ax, 5.5, 5.65, "一个 warp 的 4 个 thread 同时读内存：三种情况", fontsize=15)
BURST = ["#f6e7b0", "#f7c9b8", "#c5d4f3", "#c7e6cf"]
def strip(y, hit, title, res, c):
    T(ax, 0.3, y+0.62, title, ha="left", fontsize=12.5)
    used = sorted({h//4 for h in hit})
    for i in range(16):
        b = i//4; x = 0.3 + i*0.42 + b*0.12
        on = i in hit
        cell(ax, x, y-0.2, 0.42, 0.5, B1 if on else (BURST[b] if b in used else "#eef0f2"), ec="white", lw=1.2)
        T(ax, x+0.21, y+0.05, str(i), fontsize=10, color="white" if on else (INK if b in used else "#9aa5b1"))
    T(ax, 7.75, y+0.05, res, ha="left", fontsize=12, color=c)
strip(4.3, [0,1,2,3], "① 连续且对齐（coalesced）", "1 次 burst，读回 4 个，4 个有用\n利用率 100%", OK)
strip(2.8, [2,3,4,5], "② 连续但没对齐", "2 次 burst，读回 8 个，4 个有用\n利用率 50%", B2)
strip(1.3, [0,4,8,12], "③ 不连续（比如沿着列读一个按行存储的矩阵）", "4 次 burst，读回 16 个，4 个有用\n利用率 25%", B2)
cell(ax, 0.3, 0.3, 0.3, 0.3, B1); T(ax, 0.72, 0.45, "thread 真正要的元素", ha="left", fontsize=10.5)
cell(ax, 3.2, 0.3, 0.3, 0.3, BURST[0]); T(ax, 3.62, 0.45, "同一个 burst 里被一起读回来的元素（每 4 个一段，仅为示意）", ha="left", fontsize=10.5)
save(fig, "10-coalescing-alignment.png")
