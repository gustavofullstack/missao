#!/usr/bin/env python3
"""valida_planos.py EDL — confere os planos já no cache (seg/) contra a contagem de quadros esperada e apaga os
truncados (render interrompido deixa arquivo pela metade, e o cache o reaproveitaria em silêncio)."""
import hashlib, json, os, subprocess, sys

import render

e = json.load(open(sys.argv[1]))
ok = ruim = falta = 0
for s in e["shots"]:
    z0, z1 = s.get("zoom", [1, 1])
    g = render.GRADES[s.get("grade", e.get("grade", "noite"))]
    key = hashlib.sha1(json.dumps([s["src"], s["in"], s["dur"], s.get("speed", 1), z0, z1, g, render.TONEMAP,
                                   s.get("focus"), 1]).encode()).hexdigest()[:10]
    out = f"{render.ROOT}/seg/{s['src']}_{key}.mp4"
    if not os.path.exists(out):
        falta += 1
        continue
    n = round(s["dur"] * render.FPS)
    got = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    if got != str(n):
        os.remove(out)
        ruim += 1
        print("removido", out, got, n)
    else:
        ok += 1
print(f"ok {ok}  truncados {ruim}  faltam {falta}")
