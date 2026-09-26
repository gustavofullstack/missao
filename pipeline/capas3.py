#!/usr/bin/env python3
"""capas3.py — capas 1080x1920 dos posts 16–18: fundo gerado no Nano Banana Pro (Google Flow) + título na fonte
da marca + selo de imagem gerada por IA (a capa também é propaganda: o rótulo vai junto)."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BLACK = "/usr/share/fonts/truetype/marca/BarlowCondensed-Black.ttf"
XBOLD = "/usr/share/fonts/truetype/marca/BarlowCondensed-ExtraBold.ttf"
AMARELO, BRANCO = (252, 190, 38), (255, 255, 255)
W, H = 1080, 1920


def capa(fundo, linhas, destaque, sub, out):
    im = Image.open(fundo).convert("RGB").resize((W, H), Image.LANCZOS)
    grad = Image.new("L", (1, H))  # topo escurecido para o título ler em qualquer fundo
    for y in range(H):
        grad.putpixel((0, y), int(200 * max(0.0, 1 - y / (H * 0.46))))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, grad.resize((W, H)))
    d = ImageDraw.Draw(im)
    y = 150
    f = ImageFont.truetype(BLACK, 150)
    for l in linhas:
        while d.textlength(l, font=f) > 960:
            f = ImageFont.truetype(BLACK, f.size - 6)
        d.text((W / 2, y), l, font=f, fill=BRANCO, anchor="ma", stroke_width=4, stroke_fill=(0, 0, 0))
        y += int(f.size * 1.0)
    if destaque:
        fd = ImageFont.truetype(BLACK, 190)
        tw = d.textlength(destaque, font=fd)
        d.rectangle([W / 2 - tw / 2 - 30, y + 10, W / 2 + tw / 2 + 30, y + 10 + 205], fill=AMARELO)
        d.text((W / 2, y + 16), destaque, font=fd, fill=(0, 0, 0), anchor="ma")
        y += 240
    fs = ImageFont.truetype(XBOLD, 54)
    d.text((W / 2, y + 20), sub, font=fs, fill=AMARELO, anchor="ma", stroke_width=3, stroke_fill=(0, 0, 0))
    fl = ImageFont.truetype(XBOLD, 30)
    selo = "IMAGEM DE FUNDO GERADA POR IA · GOOGLE FLOW"
    tw = d.textlength(selo, font=fl)
    d.rounded_rectangle([W / 2 - tw / 2 - 20, H - 150, W / 2 + tw / 2 + 20, H - 100], 24, fill=(0, 0, 0))
    d.text((W / 2, H - 143), selo, font=fl, fill=(235, 235, 235), anchor="ma")
    im.save(out, quality=92)
    print(out)


capa("/root/reels/ia/nb_3.jpg", ["QUANTOS DELES", "APOIARAM?"], "NENHUM!", "UBERLÂNDIA · 25/09", "/root/reels/out/17_a_rua_ta_gritando_capa_ia.jpg")
capa("/root/reels/ia/nb_1.jpg", ["MERCADORES", "DA MISÉRIA"], "", "CLIPE · UBERLÂNDIA 25/09", "/root/reels/out/16_mercadores_da_miseria_clipe_capa_ia.jpg")
capa("/root/reels/ia/nb_2.jpg", ["O PLANO DAS", "TERRAS RARAS"], "", "ÍMÃS · BATERIAS · DRONES", "/root/reels/out/18_terras_raras_com_ia_capa_ia.jpg")
