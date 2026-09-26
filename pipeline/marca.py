#!/usr/bin/env python3
"""marca.py — artes da identidade do Missão para os reels (1080x1920 e @2x para o master 4K).
Cores e fontes tiradas do site oficial: amarelo #FCBE26, preto, branco; Barlow Condensed / Fjalla One.
Vetores oficiais: wordmark "missão" e mapa do Brasil (marca/*.svg); onça: imagem de compartilhamento do site."""
import subprocess, sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

M = "/root/reels/marca"
T = "/root/reels/titles"
AMARELO, PRETO, BRANCO = (252, 190, 38), (0, 0, 0), (255, 255, 255)
BLACK = "/usr/share/fonts/truetype/marca/BarlowCondensed-Black.ttf"
XBOLD = "/usr/share/fonts/truetype/marca/BarlowCondensed-ExtraBold.ttf"
WORDMARK = f"{M}/K5kHScSNSRSu3QX9zBzxfyjmh4.svg"  # "missão" branco, 742x198
MAPA = f"{M}/FEhCpqElkjRX2qY3KuBiTIauLU.svg"      # Brasil com divisas, 712x705
ONCA = f"{M}/kznCcPtI72eM4Qlypdik16T0A.jpg"       # og:image 1200x630: onça + "missão" vertical


def svg(path, w, cor=None):
    out = f"/tmp/marca_{w}.png"
    subprocess.run(["rsvg-convert", "-w", str(w), path, "-o", out], check=True)
    im = Image.open(out).convert("RGBA")
    if cor:  # pinta o desenho inteiro de uma cor, mantendo o alfa
        im = Image.merge("RGBA", (*Image.new("RGB", im.size, cor).split(), im.getchannel("A")))
    return im


def fonte(p, s):
    return ImageFont.truetype(p, s)


def bandeira(S):
    """Faixas preto/branco/amarelo com o "missão" preto no meio: a bandeira do partido em pé."""
    W, H = 1080 * S, 1920 * S
    im = Image.new("RGBA", (W, H), BRANCO + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H // 3], fill=PRETO)
    d.rectangle([0, 2 * H // 3, W, H], fill=AMARELO)
    wm = svg(WORDMARK, int(W * 0.78), PRETO)
    im.alpha_composite(wm, ((W - wm.width) // 2, (H - wm.height) // 2))
    return im


def mapa(S):
    """Brasil em branco translúcido, divisas finas, pino amarelo em Uberlândia (lat -18,9 / lon -48,3)."""
    w = 760 * S
    m = svg(MAPA, w)
    a = m.getchannel("A").point(lambda v: int(v * 0.42))
    m = Image.merge("RGBA", (*Image.new("RGB", m.size, BRANCO).split(), a))
    # posição relativa no retângulo do Brasil (lon -73,99..-34,79 / lat 5,27..-33,75), ajustada ao desenho
    px, py = int(w * 0.652), int(m.height * 0.612)
    glow = Image.new("RGBA", m.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for r, al in ((60, 50), (40, 90), (24, 160)):
        g.ellipse([px - r * S, py - r * S, px + r * S, py + r * S], fill=AMARELO + (al,))
    glow = glow.filter(ImageFilter.GaussianBlur(10 * S))
    m.alpha_composite(glow)
    d = ImageDraw.Draw(m)
    r = 13 * S
    d.ellipse([px - r, py - r, px + r, py + r], fill=AMARELO + (255,), outline=PRETO + (255,), width=3 * S)
    f = fonte(BLACK, 58 * S)
    txt = "UBERLÂNDIA · MG"
    tw = d.textlength(txt, font=f)
    tx, ty = min(px + 26 * S, w - tw - 8 * S), py - 30 * S
    d.rounded_rectangle([tx - 14 * S, ty - 6 * S, tx + tw + 14 * S, ty + 66 * S], 10 * S, fill=PRETO + (215,))
    d.text((tx, ty), txt, font=f, fill=AMARELO)
    return m


def onca():
    """Recorta o logo (onça + "missão") da imagem de compartilhamento: tudo que não é fundo preto."""
    im = Image.open(ONCA).convert("RGB")
    mask = im.convert("L").point(lambda v: 255 if v > 40 else 0)
    x0, y0, x1, y1 = mask.getbbox()
    pad = 6
    return im.crop((x0 - pad, y0 - pad, x1 + pad, y1 + pad))


def fim(S, linha_ia):
    W, H = 1080 * S, 1920 * S
    im = Image.new("RGBA", (W, H), PRETO + (255,))
    lg = onca()
    lw = int(W * 0.62)
    lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
    y = int(H * 0.30)
    im.paste(lg, ((W - lw) // 2, y))
    d = ImageDraw.Draw(im)
    y += lg.height + 90 * S
    for txt, f, cor in (("UBERLÂNDIA · 25.09.2026", fonte(BLACK, 74 * S), AMARELO),
                        ("PRAÇA RUI BARBOSA", fonte(XBOLD, 52 * S), BRANCO)):
        d.text((W / 2, y), txt, font=f, fill=cor, anchor="ma")
        y += int(f.size * 1.25)
    if linha_ia:
        f = fonte(XBOLD, 34 * S)
        d.text((W / 2, H - 170 * S), linha_ia, font=f, fill=(170, 170, 170), anchor="ma")
    return im


def selo(S, txt):
    """Selo pequeno de conteúdo com IA (exigência do TSE para propaganda com conteúdo sintético)."""
    f = fonte(XBOLD, 30 * S)
    tw = int(ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(txt, font=f))
    im = Image.new("RGBA", (tw + 40 * S, 52 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], 26 * S, fill=(0, 0, 0, 190))
    d.text((20 * S, 9 * S), txt, font=f, fill=(235, 235, 235))
    return im


def titulo(S, linhas, sub):
    """Título do topo no estilo da marca: caixa preta, Barlow Condensed Black branca, sublinha amarela."""
    f, fs = fonte(BLACK, 92 * S), fonte(XBOLD, 44 * S)
    d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    while max(d0.textlength(l, font=f) for l in linhas) > 860 * S:
        f = fonte(BLACK, f.size - 4 * S)
    lh = int(f.size * 1.02)
    w = int(max(max(d0.textlength(l, font=f) for l in linhas), d0.textlength(sub, font=fs))) + 76 * S
    h = 40 * S + lh * len(linhas) + int(fs.size * 1.5) + 24 * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22 * S, fill=(0, 0, 0, 225))
    d.rectangle([0, h - 12 * S, w, h], fill=AMARELO + (255,))  # filete amarelo embaixo
    y = 26 * S
    for l in linhas:
        d.text((w / 2, y), l, font=f, fill=BRANCO, anchor="ma")
        y += lh
    d.text((w / 2, y + 8 * S), sub, font=fs, fill=AMARELO, anchor="ma")
    return im


def card(S, blocos):
    """Card de fonte (texto sobre fundo preto translúcido): [(texto, tamanho, cor, fonte)]."""
    W = 960 * S
    d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    linhas = []
    for txt, tam, cor, fp in blocos:
        f = fonte(fp, tam * S)
        for l in txt.split("\n"):
            while d0.textlength(l, font=f) > W - 90 * S:
                f = fonte(fp, f.size - 2 * S)
            linhas.append((l, f, cor))
    h = 70 * S + sum(int(f.size * 1.28) for _, f, _ in linhas)
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, h - 1], 26 * S, fill=(0, 0, 0, 228))
    d.rectangle([0, 0, 14 * S, h], fill=AMARELO + (255,))
    y = 36 * S
    for l, f, cor in linhas:
        d.text((52 * S, y), l, font=f, fill=cor)
        y += int(f.size * 1.28)
    return im


if __name__ == "__main__":
    IA = "Música criada com IA (Google Flow Music) · imagens reais do ato"
    for S in (1, 2):
        sfx = "" if S == 1 else "@2x"
        bandeira(S).save(f"{T}/marca_bandeira{sfx}.png")
        mapa(S).save(f"{T}/marca_mapa{sfx}.png")
        fim(S, IA).save(f"{T}/marca_fim{sfx}.png")
        fim(S, "").save(f"{T}/marca_fim_sem_ia{sfx}.png")
        selo(S, "MÚSICA CRIADA COM IA · GOOGLE FLOW MUSIC").save(f"{T}/marca_selo_ia{sfx}.png")
        selo(S, "IMAGEM GERADA POR IA · GOOGLE FLOW").save(f"{T}/marca_selo_img_ia{sfx}.png")
        # rótulo fixo do vídeo inteiro (art. 9-B, §1º, II/III): diz o que é sintético e a tecnologia usada
        selo(S, "CONTÉM IA · TRILHA: GOOGLE FLOW MUSIC").save(f"{T}/marca_ia_musica{sfx}.png")
        selo(S, "CONTÉM IA · MÚSICA E VINHETAS: GOOGLE FLOW").save(f"{T}/marca_ia_total{sfx}.png")
        selo(S, "CONTÉM IA · VINHETAS: GOOGLE FLOW · ÁUDIO REAL DA PRAÇA").save(f"{T}/marca_ia_vinhetas{sfx}.png")
        selo(S, "CONTÉM IA · TRILHA E VINHETAS: GOOGLE FLOW · FALAS REAIS").save(f"{T}/marca_ia_trilha_vinhetas{sfx}.png")
        titulo(S, ["O ATO DE", "UBERLÂNDIA"], "25/09 · EM 1 MINUTO").save(f"{T}/21{sfx}.png")
        titulo(S, ["RENAN EM UBERLÂNDIA:", "“QUANTOS DELES", "APOIARAM?”"], "PRAÇA RUI BARBOSA · 25/09").save(f"{T}/14{sfx}.png")
        titulo(S, ["RENAN SOBRE O EDITORIAL", "DA THE ECONOMIST"], "UBERLÂNDIA · 25/09").save(f"{T}/15{sfx}.png")
        titulo(S, ["MERCADORES", "DA MISÉRIA"], "CLIPE · UBERLÂNDIA 25/09").save(f"{T}/16{sfx}.png")
        titulo(S, ["A RUA", "TÁ GRITANDO"], "UBERLÂNDIA · 25/09").save(f"{T}/17{sfx}.png")
        titulo(S, ["O PLANO DAS", "TERRAS RARAS"], "RENAN EM UBERLÂNDIA · 25/09").save(f"{T}/18{sfx}.png")
        fim(S, "Vinhetas geradas com IA (Google Flow) · som e cenas do ato reais").save(f"{T}/marca_fim_vinhetas{sfx}.png")
        card(S, [("O QUE A THE ECONOMIST ESCREVEU", 50, AMARELO, BLACK),
                 ("Editorial de 24/09/2026:", 40, BRANCO, XBOLD),
                 ("“Brazil turns its back on the future”", 50, BRANCO, BLACK),
                 ("(O Brasil dá as costas ao futuro)", 38, (200, 200, 200), XBOLD),
                 ("Sobre Renan Santos: a candidatura que mais se\naproxima “do que o momento exige” (BBC);\num “libertário combativo” que defende reformas\npara transformar o Brasil em uma grande potência\n(Estadão).", 40, BRANCO, XBOLD),
                 ("Fontes: BBC News Brasil (24/09) e Estadão (25/09)", 32, (170, 170, 170), XBOLD)]
             ).save(f"{T}/card_economist{sfx}.png")
    print("artes da marca geradas em", T)
