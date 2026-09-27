#!/usr/bin/env python3
"""Cortes 9:16 de vídeos 16:9 com legenda palavra a palavra (legendas automáticas json3 do YouTube).

Gera, por corte, um .ass (título + legenda) e um .sh com o ffmpeg; o render roda onde o vídeo está
(vaio), porque o link vaio→MACRIX é ~180 KB/s.
uso: cortes.py <plano.json> <saida_dir>
"""
import json, re, sys, unicodedata, os

W, H = 1080, 1920
VY, VH = 240, 1440          # faixa do vídeo (3:4 recortado do 16:9)


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9 ]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def palavras(json3):
    out = []
    for e in json.load(open(json3))["events"]:
        t0 = e.get("tStartMs", 0)
        for s in e.get("segs", []):
            w = s.get("utf8", "").replace(">>", "").strip()
            if w and not w.startswith("[") and norm(w):
                out.append([(t0 + s.get("tOffsetMs", 0)) / 1000, w])
    return out


def acha(ws, frase, depois=0.0):
    alvo = norm(frase).split()
    toks = [norm(w) for _, w in ws]
    for i in range(len(ws)):
        if ws[i][0] < depois:
            continue
        if toks[i:i + len(alvo)] == alvo:
            return i
    raise SystemExit(f"frase não achada: {frase!r}")


def ts(t):
    t = max(t, 0)
    return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"


def ass(titulo, chunks, dur, credito):
    esc = lambda s: s.replace("{", "(").replace("}", ")")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Barlow Condensed Black,84,&H00000000,&H00000000,&H0026BEFC,&H0026BEFC,0,0,0,0,100,100,0,0,3,18,0,8,60,60,60,1
Style: Leg,Montserrat ExtraBold,76,&H0026BEFC,&H0026BEFC,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,6,3,2,50,50,330,1
Style: Cred,Montserrat ExtraBold,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,2,0,2,40,40,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 1,{ts(0)},{ts(dur)},Titulo,,0,0,0,,{{\\fad(200,200)}}{esc(titulo)}",
          f"Dialogue: 1,{ts(0)},{ts(dur)},Cred,,0,0,0,,{esc(credito)}"]
    for a, b, txt in chunks:
        ev.append(f"Dialogue: 2,{ts(a)},{ts(b)},Leg,,0,0,0,,{{\\fscx108\\fscy108\\t(0,90,\\fscx100\\fscy100)}}{esc(txt)}")
    return head + "\n".join(ev) + "\n"


def blocos(ws, t0, t1):
    """Legenda em blocos de até 3 palavras / 20 caracteres; cada bloco vai até o início do próximo."""
    sel = [(t - t0, w) for t, w in ws if t0 <= t < t1]
    out, cur = [], []
    for t, w in sel:
        if cur and (len(cur) == 3 or len(" ".join(x for _, x in cur + [(t, w)])) > 20 or t - cur[-1][0] > 0.9):
            out.append(cur); cur = []
        cur.append((t, w))
    if cur:
        out.append(cur)
    res = []
    for i, c in enumerate(out):
        a = c[0][0]
        b = out[i + 1][0][0] if i + 1 < len(out) else c[-1][0] + 0.8
        b = min(b, c[-1][0] + 1.2)
        res.append((a, b, " ".join(w for _, w in c).upper()))
    return res


def main():
    plano = json.load(open(sys.argv[1]))
    dst = sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    ws = palavras(plano["json3"])
    troca = {norm(k): v for k, v in plano.get("troca", {}).items()}  # corrige a legenda automática ("" apaga a palavra)
    ws = [[t, troca.get(norm(w), w)] for t, w in ws if troca.get(norm(w), w)]
    sh = ["set -e", "cd ~/cortes"]
    for c in plano["cortes"]:
        partes = c.get("trechos") or [[c["de"], c["ate"]]]
        segs, t_acc, chunks = [], 0.0, []
        for de, ate in partes:
            i = acha(ws, de)
            j = acha(ws, ate, ws[i][0]) + len(norm(ate).split()) - 1
            a = ws[i][0] - 0.15
            b = (ws[j + 1][0] if j + 1 < len(ws) else ws[j][0] + 1) - 0.05
            b = min(b, ws[j][0] + 1.0)
            for x, y, t in blocos(ws, a, b):
                chunks.append((x + t_acc, y + t_acc, t))
            segs.append((a, b)); t_acc += b - a
        dur = t_acc
        nome = c["nome"]
        mus = c.get("musica", plano.get("musica"))  # trilha por baixo da fala, abaixa sozinha quando há voz
        cred = plano["credito"] + (" · TRILHA GERADA POR IA" if mus else "")
        open(f"{dst}/{nome}.ass", "w").write(ass(c["titulo"], chunks, dur, cred))
        fx = c.get("fx", 0.5)
        ch = c.get("ch", 1)  # fração da altura usada a partir do topo (<1 tira legenda embutida na fonte)
        cw = f"ih*{ch}*3/4"  # 3:4 do quadro 16:9
        crop = f"crop={cw}:ih*{ch}:'max(0,min(iw-{cw},iw*{fx}-{cw}/2))':0"
        n = len(segs)
        fc = ";".join(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{k}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{k}]"
                      for k, (a, b) in enumerate(segs))
        fc += ";" + "".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]"
        fc += (f";[vc]{crop},scale=1080:{VH}:flags=lanczos,eq=contrast=1.06:saturation=1.12,"
               f"pad={W}:{H}:0:{VY}:color=0x0B0B0B,subtitles={nome}.ass:fontsdir=fonts"
               f",fade=t=out:st={dur-0.5:.2f}:d=0.5[v]"
               f";[ac]loudnorm=I=-14:TP=-1.5:LRA=9[voz]")
        if mus:
            fc += (f";[voz]asplit[voz1][sc];[1:a]atrim=0:{dur:.2f},asetpts=PTS-STARTPTS,volume={plano.get('musica_vol', 0.30)}[m]"
                   f";[m][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=500[md]"
                   f";[voz1][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[mix]")
            fc += f";[mix]afade=t=out:st={dur-0.6:.2f}:d=0.6[a]"
        else:
            fc += f";[voz]afade=t=out:st={dur-0.6:.2f}:d=0.6[a]"
        entrada_mus = f"-ss {plano.get('musica_ss', 15)} -stream_loop -1 -i {mus} " if mus else ""
        sh.append(f"nice -n 10 ffmpeg -v error -y -i {plano['video']} {entrada_mus}"
                  f"-filter_complex \"{fc}\" -map '[v]' -map '[a]' -c:v libx264 -preset medium -crf 20 "
                  f"-profile:v high -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "
                  f"-t {dur:.2f} out/{nome}.mp4 && echo PRONTO {nome} {dur:.1f}s")
        print(f"{nome}: {dur:.1f}s, {len(chunks)} blocos")
    open(f"{dst}/render.sh", "w").write("\n".join(sh) + "\n")


if __name__ == "__main__":
    main()
