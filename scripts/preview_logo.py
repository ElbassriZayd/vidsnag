"""Composite the cut logo on dark + light + checker to inspect halo/edges."""
from PIL import Image

logo = Image.open("app/web/assets/logo-512.png").convert("RGBA")
w, h = logo.size

# dark, light, and checker panels side by side
panel = Image.new("RGBA", (w * 3 + 40, h), (0, 0, 0, 0))

dark = Image.new("RGBA", (w, h), (11, 13, 18, 255))
dark.alpha_composite(logo)
panel.paste(dark, (0, 0))

light = Image.new("RGBA", (w, h), (240, 240, 245, 255))
light.alpha_composite(logo)
panel.paste(light, (w + 20, 0))

checker = Image.new("RGBA", (w, h), (255, 255, 255, 255))
c = 32
for y in range(0, h, c):
    for x in range(0, w, c):
        if (x // c + y // c) % 2 == 0:
            for yy in range(y, min(y + c, h)):
                for xx in range(x, min(x + c, w)):
                    checker.putpixel((xx, yy), (200, 200, 205, 255))
checker.alpha_composite(logo)
panel.paste(checker, (w * 2 + 40, 0))

panel.convert("RGB").resize((panel.width // 2, panel.height // 2)).save("scripts/_preview.png")
print("saved scripts/_preview.png")
