#!/usr/bin/env python3
"""sheets.py WORKDIR OUTDIR — folha de contato por vídeo (tempo em cada quadro) + visão geral."""
import glob, json, os, sys

from PIL import Image, ImageDraw, ImageFont

work, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
font = ImageFont.load_default(size=22)
small = ImageFont.load_default(size=18)
TW, TH, COLS, MAXT = 180, 320, 8, 40


def label(img, text, f=font):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 30], fill=(0, 0, 0))
    d.text((6, 3), text, fill=(255, 255, 0), font=f)


overview = []
for aj in sorted(glob.glob(f"{work}/*/analysis.json")):
    d = json.load(open(aj))
    m, fr = d["meta"], d["frames"]
    if not fr:
        continue
    thumbs = os.path.join(os.path.dirname(aj), "thumbs")
    step = max(1, -(-len(fr) // MAXT))
    pick = fr[::step]
    rows = -(-len(pick) // COLS)
    sheet = Image.new("RGB", (COLS * TW, rows * TH + 40), (20, 20, 20))
    ImageDraw.Draw(sheet).text((8, 6), f'{m["name"]}  {m["duration"]:.0f}s  {m["fps"]:.0f}fps  '
                               f'{"HDR" if m["hdr"] else "SDR"}  (1 quadro a cada {step} keyframe)',
                               fill=(255, 255, 255), font=font)
    for k, f in enumerate(pick):
        im = Image.open(f'{thumbs}/{f["i"]:05d}.jpg').resize((TW, TH))
        label(im, f'{f.get("t", 0):.0f}s', small)
        sheet.paste(im, ((k % COLS) * TW, 40 + (k // COLS) * TH))
    sheet.save(f'{out}/{m["name"]}.jpg', quality=80)
    mid = fr[len(fr) // 2]
    im = Image.open(f'{thumbs}/{mid["i"]:05d}.jpg').resize((TW, TH))
    label(im, f'{m["name"][-4:]} {m["duration"]:.0f}s {m["fps"]:.0f}p', small)
    overview.append(im)

rows = -(-len(overview) // 9)
ov = Image.new("RGB", (9 * TW, rows * TH), (20, 20, 20))
for k, im in enumerate(overview):
    ov.paste(im, ((k % 9) * TW, (k // 9) * TH))
ov.save(f"{out}/_overview.jpg", quality=82)
print(len(overview), "vídeos")
