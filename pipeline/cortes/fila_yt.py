#!/usr/bin/env python3
"""Monta as filas de X, YouTube e Instagram a partir das legendas.
uso: fila_yt.py SUFIXO ITEM...   (ITEM = número do corte, ou pN para a parte N do discurso)
saída: yt/fila_ytSUF.json, ig/fila_igSUF.json, x/fila_xSUF.json + um .txt de legenda por item"""
import json, re, sys, os
suf, itens = sys.argv[1], sys.argv[2:]
txt = open("out/LEGENDAS_CORTES_SOROCABA.txt").read()
fonte, posts = "Vídeo oficial da campanha (Renan Santos e Kim Kataguiri em Sorocaba).", {}
for bloco in re.split(r"\n\s*\n", txt):
    b = bloco.strip()
    if m := re.match(r"--- (.+) ---$", b):
        fonte = m.group(1).replace(" (", ", ").rstrip(")") + "."
    elif m := re.match(r"(\d+) · (.+)\n(.+)\n(#.+)$", b, re.S):
        posts[m.group(1)] = (m.group(2), m.group(3).strip(), m.group(4), fonte)
vids = os.popen("ssh vaio ls /home/admin/missao-videos").read().split()
V = "/home/admin/missao-videos/"
for d in ("yt", "ig", "x"):
    os.makedirs(d, exist_ok=True)
fy, fi, fx = [], [], []
for n in itens:
    if n.startswith("p"):  # parte do discurso: legenda pronta em /root/reels/out
        leg = open(f"/root/reels/out/30_discurso_parte{n[1:]}_LEGENDA.txt").read().strip()
        cab, resto = leg.split("\n", 1)
        frase = cab.split(":", 1)[1].strip().strip('"')
        arq = f"30_discurso_parte{n[1:]}.mp4"
        titulo = f"Renan Santos em Uberlândia · Parte {n[1:]}/8: {frase} #missao"[:100]
        desc = resto.strip()
        ig = leg
        tags = re.findall(r"#\w+", leg)
        xt = f"{cab}\n\nRenan Santos, Uberlândia, 25/09. Discurso completo em 8 partes, sem IA.\n\n{' '.join(tags[:3])}"
    else:
        h, corpo, tags, f = posts[n]
        arq = next(v for v in vids if v.startswith(n + "_") and v.endswith(".mp4"))
        titulo = f"{h} #missao #shorts"[:100]
        desc = f"{corpo}\n\nFonte: {f} Corte vertical com legenda, sem IA.\n\n{tags} #shorts"
        ig = f"{h}\n\n{corpo}\n\nFonte: {f} Corte vertical com legenda, sem IA.\n\n{tags}"
        xt = f"{h}\n\n{corpo}\n\n{' '.join(tags.split()[:3])}"
        if len(xt) > 280:
            xt = f"{h}\n\n{' '.join(tags.split()[:3])}"
    open(f"yt/{n}.txt", "w").write(desc + "\n")
    open(f"ig/{n}.txt", "w").write(ig + "\n")
    fy.append([V + arq, titulo, f"/root/postar/yt/{n}.txt"])
    fi.append([V + arq, f"/root/postar/ig/{n}.txt"])
    fx.append([V + arq, xt])
    assert arq in vids, arq
for nome, fila in (("yt/fila_yt", fy), ("ig/fila_ig", fi), ("x/fila_x", fx)):
    json.dump(fila, open(f"{nome}{suf}.json", "w"), ensure_ascii=False, indent=1)
for a, b in zip(fy, fx):
    print(len(a[1]), a[1], "| X", len(b[1]))
