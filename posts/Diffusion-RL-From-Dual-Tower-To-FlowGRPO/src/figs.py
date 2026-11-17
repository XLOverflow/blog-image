"""Generate the code-drawn figures as SVG; render with: rsvg-convert -z 2 X.svg -o X.png"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent
GRAY, BLUE, WHITE = "#F2F2F2", "#DCEAF5", "#FFFFFF"
VERM, GREEN = "#D55E00", "#009E73"
FONT = "Arial, Helvetica, 'Liberation Sans', sans-serif"


class Fig:
    def __init__(self, w, h):
        self.w, self.h, self.el = w, h, []

    def rect(self, x, y, w, h, fill=WHITE, stroke="#000", dash=False):
        d = ' stroke-dasharray="5 4"' if dash else ""
        self.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1"{d}/>')

    def box(self, x, y, w, h, title, sub=None, fill=WHITE, stroke="#000"):
        self.rect(x, y, w, h, fill, stroke)
        cx = x + w / 2
        if sub is None:
            self.text(cx, y + h / 2 + 5, title)
        else:
            self.text(cx, y + h / 2 - 4, title)
            self.text(cx, y + h / 2 + 15, sub, small=True)

    def text(self, x, y, s, small=False, anchor="middle"):
        size, fill = (12.5, "#666") if small else (14.5, "#000")
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        self.el.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{s}</text>')

    def arrow(self, x1, y1, x2, y2):
        self.el.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="1" marker-end="url(#a)"/>')

    def line(self, x1, y1, x2, y2):
        self.el.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="1"/>')

    def save(self, name):
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
            f'font-family="{FONT}"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#000"/></marker></defs>'
            f'<rect width="{self.w}" height="{self.h}" fill="#fff"/>'
        )
        (OUT / f"{name}.svg").write_text(head + "".join(self.el) + "</svg>")


L, R, W, H = 40, 380, 260, 54  # two-column layout: left x, right x, box width, box height
LC, RC = L + W / 2, R + W / 2


def three_architectures():
    f = Fig(960, 430)
    # (a) encoder + diffusion transformer
    f.box(20, 250, 120, 60, "text encoder", "separate model", GRAY)
    f.box(170, 70, 120, 240, "DiT blocks", "N layers", BLUE)
    f.box(20, 350, 120, 40, "text tokens")
    f.box(170, 350, 120, 40, "noisy image")
    f.arrow(80, 350, 80, 310)
    f.arrow(230, 350, 230, 310)
    f.line(80, 250, 80, 190)
    f.arrow(80, 190, 170, 190)
    f.text(20, 178, "last-layer features", small=True, anchor="start")
    f.arrow(230, 70, 230, 40)
    f.text(230, 30, "velocity", small=True)
    f.text(155, 418, "(a) Encoder + DiT, e.g. SD3, Flux")
    # (b) single tower: MiniMax-H3
    f.box(340, 250, 110, 60, "Qwen3-VL", "separate encoder", GRAY)
    f.box(470, 70, 140, 240, "shared blocks", "one set of weights", BLUE)
    f.box(340, 350, 110, 40, "text tokens")
    f.box(470, 350, 65, 40, "video")
    f.box(545, 350, 65, 40, "audio")
    f.arrow(395, 350, 395, 310)
    f.arrow(502, 350, 502, 310)
    f.arrow(577, 350, 577, 310)
    f.line(395, 250, 395, 190)
    f.arrow(395, 190, 470, 190)
    f.text(340, 178, "text embeddings", small=True, anchor="start")
    f.arrow(502, 70, 502, 40)
    f.arrow(577, 70, 577, 40)
    f.text(502, 30, "video v", small=True)
    f.text(577, 30, "audio v", small=True)
    f.text(475, 418, "(b) Single tower: MiniMax-H3")
    # (c) dual tower: Cosmos3
    f.box(660, 70, 120, 240, "understanding", "tower, frozen", GRAY)
    f.box(820, 70, 120, 240, "generation", "tower", BLUE)
    f.box(660, 350, 120, 40, "text tokens")
    f.box(820, 350, 120, 40, "noisy image")
    f.arrow(720, 350, 720, 310)
    f.arrow(880, 350, 880, 310)
    for y in (120, 190, 260):
        f.arrow(780, y, 820, y)
    f.text(800, 110, "K, V", small=True)
    f.arrow(880, 70, 880, 40)
    f.text(880, 30, "velocity", small=True)
    f.text(800, 418, "(c) Dual tower: Cosmos3")
    f.save("01-three-architectures")


def forward_shapes():
    f = Fig(680, 880)
    ys = [20, 104, 188, 272, 356]
    f.box(L, ys[0], W, H, "text token ids", "[L_text], integers")
    f.box(R, ys[0], W, H, "noisy image latent", "[48, 1, 30, 52]")
    f.box(L, ys[1], W, H, "embed_tokens", "vocab 151936 -> 4096-d", GRAY)
    f.box(R, ys[1], W, H, "2x2 patchify", "390 patches, 192-d each", BLUE)
    f.box(R, ys[2], W, H, "proj_in", "192-d -> 4096-d", BLUE)
    f.box(R, ys[3], W, H, "add timestep embedding", "sigma x 1000 via time_embedder", BLUE)
    f.box(L, ys[4], W, H, "und_seq", "[L_text, 4096]", GRAY)
    f.box(R, ys[4], W, H, "gen_seq", "[390, 4096]", BLUE)
    f.arrow(LC, ys[0] + H, LC, ys[1])
    f.arrow(LC, ys[1] + H, LC, ys[4])
    for a, b in zip(ys, ys[1:]):
        f.arrow(RC, a + H, RC, b)
    cy = 440
    f.rect(20, cy, 640, 150, dash=True)
    f.text(340, cy + 22, "36 x Cosmos3VLTextMoTDecoderLayer")
    f.text(340, cy + 41, "32 query heads, 8 key-value heads, MLP width 12288", small=True)
    iy = cy + 70
    f.box(L, iy, W, H, "understanding-tower weights", "causal: text sees earlier text", GRAY)
    f.box(R, iy, W, H, "generation-tower weights", "sees all text and all image", BLUE)
    f.arrow(L + W, iy + H / 2, R, iy + H / 2)
    f.text(340, iy + H / 2 - 8, "K, V", small=True)
    f.arrow(LC, ys[4] + H, LC, iy)
    f.arrow(RC, ys[4] + H, RC, iy)
    oy = [630, 714, 798]
    f.box(L, oy[0], W, H, "norm", "lm_head exists, not called here", GRAY)
    f.box(R, oy[0], W, H, "norm_moe_gen", "[390, 4096]", BLUE)
    f.box(R, oy[1], W, H, "proj_out", "[390, 192]", BLUE)
    f.box(R, oy[2], W, H, "unpatchify: velocity v", "[48, 1, 30, 52]")
    f.arrow(LC, iy + H, LC, oy[0])
    f.arrow(RC, iy + H, RC, oy[0])
    f.arrow(RC, oy[0] + H, RC, oy[1])
    f.arrow(RC, oy[1] + H, RC, oy[2])
    f.save("02-cosmos3-forward-shapes")


def one_layer():
    f = Fig(680, 410)
    f.box(L, 20, W, 40, "text und_seq", None, GRAY)
    f.box(R, 20, W, 40, "image gen_seq", None, BLUE)
    f.box(L, 90, W, 40, "input_layernorm", None, GRAY)
    f.box(R, 90, W, 40, "layernorm (_moe_gen copy)", None, BLUE)
    f.rect(20, 160, 640, 130, dash=True)
    f.text(340, 182, "Cosmos3PackedMoTAttention")
    f.box(L, 206, W, H, "pass 1: text attends to text", "to_q, to_k, to_v, to_out", GRAY)
    f.box(R, 206, W, H, "pass 2: image attends to all", "add_q/k/v_proj, to_add_out", BLUE)
    f.arrow(L + W, 233, R, 233)
    f.text(340, 225, "K, V", small=True)
    f.box(L, 330, W, H, "mlp", "+ residual, to next layer", GRAY)
    f.box(R, 330, W, H, "mlp_moe_gen", "+ residual, to next layer", BLUE)
    for c in (LC, RC):
        f.arrow(c, 60, c, 90)
        f.arrow(c, 130, c, 206)
        f.arrow(c, 260, c, 330)
    f.save("03-one-layer-two-passes")


def timeline():
    f = Fig(680, 180)
    f.text(46, 30, "pure noise, sigma = 1", small=True, anchor="start")
    f.text(631, 30, "clean latent, sigma = 0", small=True, anchor="end")
    f.rect(338.5, 42, 148, 52, dash=True)
    for i in range(16):
        sde = i in (9, 11)
        f.box(46 + 37 * i, 50, 30, 36, str(i), None, "#F6D9C8" if sde else WHITE, VERM if sde else "#000")
    f.text(413, 114, "candidate pool: steps 8 to 11", small=True)
    f.rect(46, 140, 16, 16)
    f.text(70, 153, "deterministic Euler step", small=True, anchor="start")
    f.rect(270, 140, 16, 16, "#F6D9C8", VERM)
    f.text(294, 153, "SDE step drawn this rollout (example: 9 and 11)", small=True, anchor="start")
    f.save("06-rollout-timeline")


def sde_step():
    f = Fig(680, 454)
    f.box(210, 20, 260, H, "current latent x (state)", "step k, noise level sigma")
    f.box(L, 110, W, H, "forward: positive prompt + x", "velocity v_cond", BLUE)
    f.box(R, 110, W, H, "forward: negative prompt + x", "velocity v_uncond", BLUE)
    f.box(150, 200, 380, H, "guided velocity v", "v = v_uncond + 4 x (v_cond - v_uncond)")
    f.box(150, 290, 380, H, "Gaussian mean and std (policy)", "from x, v, sigma, eta", WHITE, VERM)
    f.box(150, 380, 380, H, "x_next = mean + std x noise (action)", "store x and x_next", WHITE, VERM)
    f.arrow(290, 74, LC, 110)
    f.arrow(390, 74, RC, 110)
    f.arrow(LC, 164, 290, 200)
    f.arrow(RC, 164, 390, 200)
    f.arrow(340, 254, 340, 290)
    f.arrow(340, 344, 340, 380)
    f.save("07-one-sde-step")


def advantage():
    f = Fig(680, 320)
    f.box(170, 20, 340, H, "prompt: a red fox in snow", "same prompt, 16 different noise seeds")
    scores = ["21.2", "21.8", "20.6", "21.4"]
    advs = [("-0.1", False), ("+1.1", True), ("-1.3", False), ("+0.3", True)]
    for i, x in enumerate([40, 195, 350, 505]):
        c = x + 67.5
        f.arrow(340 + (i - 1.5) * 40, 74, c, 120)
        f.box(x, 120, 135, H, f"image {i + 1}", f"score {scores[i]}", GRAY)
        f.arrow(c, 174, c, 214)
        a, up = advs[i]
        f.box(x, 214, 135, H, f"advantage {a}", "raise probability" if up else "lower probability", WHITE, GREEN if up else VERM)
    f.text(340, 298, "example numbers: group mean 21.25, batch-wide std taken as 0.5", small=True)
    f.save("09-group-advantage")


def replay():
    f = Fig(680, 364)
    f.box(170, 20, 340, H, "stored x and x_next", "plus the same prompt tokens as in rollout")
    f.box(L, 110, W, H, "replay 1: no gradient", "old log-prob, kept fixed", GRAY)
    f.box(R, 110, W, H, "replay 2: with gradient", "new log-prob", BLUE)
    f.box(150, 200, 380, H, "ratio = exp(new - old)", "loss = -advantage x ratio, then clip")
    f.box(150, 290, 380, H, "backward: only LoRA is updated", "add_q/k/v_proj, to_add_out", BLUE)
    f.arrow(290, 74, LC, 110)
    f.arrow(390, 74, RC, 110)
    f.arrow(LC, 164, 290, 200)
    f.arrow(RC, 164, 390, 200)
    f.arrow(340, 254, 340, 290)
    f.save("10-replay-and-loss")


if __name__ == "__main__":
    for fn in (three_architectures, forward_shapes, one_layer, timeline, sde_step, advantage, replay):
        fn()
