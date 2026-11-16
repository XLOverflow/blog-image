from style import *
fig, ax = canvas(11, 6.4)
T(ax, 5.5, 6.05, "GPU 和 TPU 的层级对照：按功能对齐，而不是按名字", fontsize=15)
rows = [("顶层单元", 4.75), ("通用运算", 3.75), ("矩阵乘", 2.75), ("片上快内存", 1.75), ("大容量内存", 0.6)]
for name, y in rows:
    T(ax, 5.5, y, name, fontsize=11.5, color=MUTE)
def side(x, title, top, items, n):
    T(ax, x+2.1, 5.5, title, fontsize=13, color=INK)
    box(ax, x, 1.3, 4.2, 3.85, GR, LINE, r=0.12)
    T(ax, x+2.1, 4.85, top[0], fontsize=12.5)
    T(ax, x+2.1, 4.52, top[1], fontsize=9.5, color=MUTE)
    for (txt, sub, y, hot) in items:
        box(ax, x+0.25, y-0.36, 3.7, 0.72, BG2 if hot else "white", B2 if hot else B1, lw=1.6)
        T(ax, x+2.1, y+0.12, txt, fontsize=12, color=B2 if hot else B1)
        T(ax, x+2.1, y-0.17, sub, fontsize=9.5, color=MUTE)
    box(ax, x, 0.25, 4.2, 0.7, "white", MUTE, lw=1.4)
    T(ax, x+2.1, 0.6, n, fontsize=12)
side(0.3, "NVIDIA GPU", ("SM · A100 上有 108 个", "Streaming Multiprocessor，一个 block 跑在一个 SM 上"), [
  ("CUDA core", "加法、比较、ReLU 等逐元素运算", 3.75, False),
  ("Tensor Core", "专用的小块矩阵乘加电路", 2.75, True),
  ("L1 cache / shared memory", "在 SM 内部", 1.75, False)], "HBM（global memory）")
side(6.5, "Google TPU", ("Tensor Core · 通常只有 1 到 2 个", "名字和 NVIDIA 的 Tensor Core 相同，但地位等于 SM"), [
  ("VPU", "通用向量运算", 3.75, False),
  ("MXU", "大的矩阵乘单元", 2.75, True),
  ("VMEM", "片上向量内存", 1.75, False)], "HBM")
for _, y in rows[:4]:
    ax.plot([4.55, 4.85], [y, y], color=LINE, lw=1.2); ax.plot([6.15, 6.45], [y, y], color=LINE, lw=1.2)
save(fig, "04-gpu-tpu-hierarchy.png")
