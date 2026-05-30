"""Cut the VidSnag VS monogram off its navy background using a saturation matte.

The source is an AI-generated PNG on a desaturated navy gradient; the logo is
vividly saturated, so saturation (max-min channel) separates them cleanly where
color-distance fails on a gradient. Exports transparent PNGs + .ico.
"""
import numpy as np
from PIL import Image, ImageFilter

SRC = r"C:\Users\ME\Downloads\logo_vidsnag\Gemini_Generated_Image_d91g1td91g1td91g.png"

im = Image.open(SRC).convert("RGBA")
a = np.asarray(im).astype(np.float32)
h, w, _ = a.shape
rgb = a[:, :, :3]
mx = rgb.max(2)
mn = rgb.min(2)
sat = mx - mn

print("corner sat:", round(float(sat[:50, :50].mean()), 1),
      "center sat:", round(float(sat[h // 2 - 50:h // 2 + 50, w // 2 - 50:w // 2 + 50].mean()), 1),
      "max:", int(sat.max()))

solid_t, feather_lo = 80.0, 45.0
alpha = np.zeros((h, w), np.float32)
alpha[sat >= solid_t] = 1.0
band = (sat >= feather_lo) & (sat < solid_t)
alpha[band] = (sat[band] - feather_lo) / (solid_t - feather_lo)
alpha[int(h * 0.84):, int(w * 0.84):] = 0  # remove Gemini sparkle watermark

am = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
alpha = np.asarray(am).astype(np.float32) / 255.0
alpha[alpha < 0.08] = 0
alpha255 = (alpha * 255).astype(np.uint8)
print("coverage%:", round((alpha255 > 40).mean() * 100, 1))

out = np.dstack([rgb.astype(np.uint8), alpha255])
img = Image.fromarray(out, "RGBA")

ys, xs = np.where(alpha255 > 40)
top, bot, left, right = ys.min(), ys.max(), xs.min(), xs.max()
pad = int(0.06 * max(bot - top, right - left))
top = max(0, top - pad); left = max(0, left - pad)
bot = min(h, bot + pad); right = min(w, right + pad)
img = img.crop((left, top, right, bot))

cw, ch = img.size
side = max(cw, ch)
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(img, ((side - cw) // 2, (side - ch) // 2), img)
print("final size:", canvas.size)

canvas.save("app/web/assets/logo.png")
canvas.save("website/assets/logo.png")
for s in (512, 256, 128, 64, 48, 32, 16):
    canvas.resize((s, s), Image.LANCZOS).save(f"app/web/assets/logo-{s}.png")
canvas.resize((256, 256), Image.LANCZOS).save("website/assets/logo-256.png")
canvas.resize((256, 256), Image.LANCZOS).save(
    "app/web/assets/vidsnag.ico",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("DONE")
