#!/usr/bin/env python3
"""titulo.py OUT.png "LINHA 1|LINHA 2" ["SUBLINHA"] — título do topo do reel: caixa preta arredondada,
Montserrat ExtraBold branca, sublinha amarela (paleta preto/amarelo/branco dos perfis do Missão)."""
import sys

from PIL import Image, ImageDraw, ImageFont

out, texto = sys.argv[1], sys.argv[2]
sub = sys.argv[3] if len(sys.argv) > 3 else ""
F = "/usr/share/fonts/opentype/montserrat/Montserrat-ExtraBold.otf"
FS = "/usr/share/fonts/opentype/montserrat/Montserrat-Bold.otf"
PX, PY, MAXW = 38, 28, 900  # 900 px = zona segura com 90 px de margem de cada lado
lines = texto.split("|")
size = 66
while True:  # encolhe até a linha mais larga caber
    f = ImageFont.truetype(F, size)
    widths = [f.getlength(l) for l in lines]
    if max(widths) + 2 * PX <= MAXW or size <= 36:
        break
    size -= 2
lh = int(size * 1.2)
fs = ImageFont.truetype(FS, int(size * 0.56))
sh = int(size * 0.56 * 1.55) if sub else 0
w = int(max(max(widths), fs.getlength(sub) if sub else 0)) + 2 * PX
h = 2 * PY + lh * len(lines) + sh
img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle([0, 0, w - 1, h - 1], radius=28, fill=(0, 0, 0, 218))
y = PY
for l in lines:
    d.text((w / 2, y), l, font=f, fill=(255, 255, 255, 255), anchor="ma")
    y += lh
if sub:
    d.text((w / 2, y + int(size * 0.12)), sub, font=fs, fill=(255, 225, 26, 255), anchor="ma")
img.save(out)
print(out, img.size, "fonte", size)
