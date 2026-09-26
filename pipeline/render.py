#!/usr/bin/env python3
"""render.py EDL.json [...] — monta reels 1080x1920/30p a partir dos originais HDR do iPhone.

EDL = {"name", "grade": "noite",
       "shots": [{"src", "in", "dur", "speed": 1, "zoom": [1, 1], "grade": ..., "flash": false}],
       "audio": [{"src", "in", "gain": 0}, ...]   # cama contínua, trechos emendados com crossfade
                | "sync",                          # áudio do próprio plano (só com speed 1)
       "texts": [{"lines": [...], "start", "end", "y": 520, "size": 84, "color": "white"}],
       "cover": 1.0, "loop": 0}                    # loop = segundos de crossfade fim->início
"in" é o tempo no arquivo original; "dur" é a duração NA TELA (a fonte consome dur*speed)."""
import hashlib, json, os, subprocess, sys

ROOT = "/root/reels"
FPS = 30
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
# HLG BT.2020 -> SDR BT.709: mobius com npl=203 (branco de referência do HLG) venceu o teste de 6 variantes
TONEMAP = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=pc,format=gbrp16le")
GRADES = {
    "neutro": "null",  # vinheta gerada por IA: já vem graduada
    "noite": "vibrance=intensity=0.18,curves=master='0/0 0.07/0.045 0.5/0.5 0.88/0.9 1/1',"
             "colorbalance=bs=0.035:bm=0.01:rh=0.025:bh=-0.015",
    # plano geral escuro: mesma cor da "noite", sombras erguidas para a multidão aparecer
    "noite_clara": "vibrance=intensity=0.18,curves=master='0/0 0.06/0.07 0.25/0.3 0.5/0.55 0.88/0.9 1/1',"
                   "colorbalance=bs=0.035:bm=0.01:rh=0.025:bh=-0.015",
    # sinalizador/fumaça: laranja sem o verde que o amarelo das luzes puxava (teste F2)
    "fogo": "vibrance=intensity=0.15,curves=master='0/0 0.1/0.055 0.5/0.52 1/1',"
            "colorbalance=rs=-0.03:gs=-0.01:bs=0.06:rm=0.05:gm=-0.025:bm=-0.02:rh=0.05:gh=-0.02:bh=-0.02,hue=h=-6",
    # névoa dourada: laranja-pêssego (teste F3)
    "fogo_quente": "vibrance=intensity=0.12,curves=master='0/0 0.1/0.05 0.5/0.5 1/1',"
                   "colorbalance=rs=-0.03:bs=0.07:rm=0.07:gm=-0.035:bm=-0.03:rh=0.04:gh=-0.03,hue=h=-10:s=1.05",
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"falhou: {' '.join(cmd)}\n{r.stderr[-3000:]}")
    return r.stdout


def src_path(stem):
    for ext in (".MOV", ".mov", ".mp4", ".m4a", ".wav"):
        p = f"{ROOT}/src/{stem}{ext}"
        if os.path.exists(p):
            return p
    sys.exit(f"fonte não encontrada: {stem}")


def is_hdr(p):
    trc = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=color_transfer", "-of", "csv=p=0", p]).strip()
    return trc in ("arib-std-b67", "smpte2084")


def shot(s, grade, S=1):
    """Renderiza (ou reaproveita do cache) um plano já graduado em (1080*S)x(1920*S)/30p; S=2 é o master 4K."""
    W, H = 1080 * S, 1920 * S
    p, speed = src_path(s["src"]), s.get("speed", 1)
    z0, z1 = s.get("zoom", [1, 1])
    g = GRADES[s.get("grade", grade)]
    key = hashlib.sha1(json.dumps([s["src"], s["in"], s["dur"], speed, z0, z1, g, TONEMAP,
                                   s.get("focus"), S]).encode()).hexdigest()[:10]
    out = f"{ROOT}/seg/{s['src']}_{key}.mp4"
    if os.path.exists(out):
        return out
    n = round(s["dur"] * FPS)
    vf = [f"setpts=(PTS-STARTPTS)/{speed}", f"fps={FPS}"]
    fx, fy = s.get("focus", [0.5, 0.5])
    if z0 == z1 != 1:  # enquadramento fixo (corte seco de fala): crop simples, sem o custo do zoompan em 4K
        vf.append(f"crop=w=iw/{z0}:h=ih/{z0}:x='max(0,min(iw-iw/{z0},{fx}*iw-iw/{z0}/2))':"
                  f"y='max(0,min(ih-ih/{z0},{fy}*ih-ih/{z0}/2))',scale={W}:{H}:flags=lanczos")
    elif (z0, z1) != (1, 1):  # zoom feito na resolução 4K: sem o tremido do zoompan em 1080
        vf.append(f"zoompan=z='{z0}+({z1}-{z0})*on/{max(n - 1, 1)}':"
                  f"x='max(0,min(iw-iw/zoom,{fx}*iw-iw/zoom/2))':"
                  f"y='max(0,min(ih-ih/zoom,{fy}*ih-ih/zoom/2))':d=1:s={W}x{H}:fps={FPS}")
    else:
        vf.append(f"scale={W}:{H}:flags=lanczos")
    vf += [TONEMAP if is_hdr(p) else "format=gbrp16le", g,
           "scale=out_color_matrix=bt709:out_range=tv:flags=lanczos", "format=yuv420p"]
    os.makedirs(f"{ROOT}/seg", exist_ok=True)
    # sem o filtro de deblocagem na decodificação: ~30% mais rápido e invisível depois de reduzir 4K para 1080
    run(["ffmpeg", "-v", "error", "-y", "-skip_loop_filter", "all", "-ss", f"{s['in']:.3f}", "-t", f"{s['dur'] * speed + 0.3:.3f}",
         "-i", p, "-an", "-vf", ",".join(vf), "-frames:v", str(n), "-c:v", "libx264", "-crf", "12",
         "-preset", "veryfast", "-pix_fmt", "yuv420p", out])
    got = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                   "stream=nb_read_frames", "-of", "csv=p=0", out]).strip())
    if got != n:  # fonte curta demais para o trecho pedido: melhor falhar do que dessincronizar
        os.remove(out)
        sys.exit(f"{s['src']} @ {s['in']}: {got} quadros, esperava {n}")
    return out


def alpha(a, b, f=0.2):
    if not f:
        return "1"
    return (f"if(lt(t,{a}),0,if(lt(t,{a + f}),(t-{a})/{f},"
            f"if(lt(t,{b - f}),1,if(lt(t,{b}),({b}-t)/{f},0))))")


def texts(edl, name, S=1):
    vf = []
    for i, tx in enumerate(edl.get("texts", [])):
        size, y0 = tx.get("size", 84) * S, tx.get("y", 520) * S
        for j, line in enumerate(tx["lines"]):
            tf = f"{ROOT}/seg/{name}_t{i}_{j}.txt"
            open(tf, "w").write(line)
            box = (f"box=1:boxcolor={tx.get('boxcolor') or 'black@' + str(tx['box'])}:boxborderw={tx.get('pad', 18) * S}:"
                   if tx.get("box") or tx.get("boxcolor") else "")
            xl = "(w-text_w)/2"
            if tx.get("shake"):  # batida do coro: treme 0,25 s na entrada
                xl = f"'(w-text_w)/2+{9 * S}*sin(t*95)*lt(t-{tx['start']},0.25)'"
            yl = y0 + j * int(size * 1.18)
            if tx.get("anim") == "pop":  # entra subindo 26 px em 0,12 s: o "pulo" das legendas dos cortes grandes
                yl = f"'{yl}+{26 * S}*max(0,1-(t-{tx['start']})/0.12)'"
            vf.append(f"drawtext=fontfile={tx.get('font', FONT)}:textfile={tf}:expansion=none:"
                      f"fontsize={size}:fontcolor={tx.get('color', 'white')}:x={xl}:"
                      f"y={yl}:shadowx=0:shadowy={tx.get('shadow', 4) * S}:shadowcolor=black@0.6:"
                      f"borderw={tx.get('border', 0) * S}:bordercolor={tx.get('bordercolor', 'black@0.35')}:{box}"
                      f"alpha='{alpha(tx['start'], tx['end'], tx.get('fade', 0.2))}':"
                      f"enable='gte(t,{tx['start']})*lt(t,{tx['end']})'")  # meio-aberto: sem quadro duplo na troca
    return vf


# voz do orador pelo som da praça: tira grave de palco, dá presença, segura picos. Sem redutor de ruído:
# ponytail: sem ouvir, denoise arrisca artefato; ligar afftdn só depois de alguém ouvir
VOZ = ("highpass=f=80,lowpass=f=14000,equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.4:g=3,"
       "acompressor=threshold=0.089:ratio=2.5:attack=10:release=150:makeup=1.5")


def audio_bed(edl, total, name):
    """WAV da cama de áudio com a duração exata do reel."""
    wav = f"{ROOT}/seg/{name}_audio.wav"
    parts = []
    if edl["audio"] == "sync":
        t = 0
        for k, s in enumerate(edl["shots"]):
            pw = f"{ROOT}/seg/{name}_a{k}.wav"
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['in']:.3f}", "-t", f"{s['dur']:.3f}",
                 "-i", src_path(s["src"]), "-vn", "-ac", "2", "-ar", "48000",
                 "-af", (VOZ + "," if s.get("voz", edl.get("voz")) else "") +
                 f"afade=t=in:d=0.02,afade=t=out:st={s['dur'] - 0.02:.3f}:d=0.02", pw])
            parts.append(pw)
        cmd = ["ffmpeg", "-v", "error", "-y"] + sum((["-i", p] for p in parts), [])
        cmd += ["-filter_complex", "".join(f"[{k}:a]" for k in range(len(parts))) +
                f"concat=n={len(parts)}:v=0:a=1[a]", "-map", "[a]", wav]
        run(cmd)
        return wav
    xf, left = edl.get("xfade", 0.4), total
    for k, a in enumerate(edl["audio"]):
        last = k == len(edl["audio"]) - 1
        d = left if last else a["dur"]  # trechos do meio precisam de "dur" (inclui o crossfade)
        pw = f"{ROOT}/seg/{name}_b{k}.wav"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a['in']:.3f}", "-t", f"{d:.3f}",
             "-i", src_path(a["src"]), "-vn", "-ac", "2", "-ar", "48000",
             "-af", f"volume={a.get('gain', 0)}dB" + ("," + VOZ if a.get("voz") else ""), pw])
        parts.append(pw)
        left -= d - xf
    if len(parts) == 1:
        os.replace(parts[0], wav)
        return wav
    cmd = ["ffmpeg", "-v", "error", "-y"] + sum((["-i", p] for p in parts), [])
    chain, prev = [], "[0:a]"
    for k in range(1, len(parts)):
        chain.append(f"{prev}[{k}:a]acrossfade=d={xf}:c1=tri:c2=tri[x{k}]")
        prev = f"[x{k}]"
    run(cmd + ["-filter_complex", ";".join(chain), "-map", prev, wav])
    return wav


def normalize(wav):
    """Loudnorm em duas passadas (linear): -14 LUFS integrado, pico real <= -1,5 dBTP."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    out = wav.replace(".wav", "_norm.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af",
         f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
         f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:"
         "linear=true,aresample=48000", "-ar", "48000", out])
    return out


def render(edl):
    S = edl.get("escala", 1)
    name, grade = edl["name"] + ("_4k" if S == 2 else ""), edl.get("grade", "noite")
    segs = [shot(s, grade, S) for s in edl["shots"]]
    if os.environ.get("SO_PLANOS"):  # adianta só a parte pesada (planos no cache); a montagem roda depois
        return
    total = round(sum(s["dur"] for s in edl["shots"]), 3)
    lst = f"{ROOT}/seg/{name}.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    wav = audio_bed(edl, total, name)
    if edl.get("musica"):
        m = edl["musica"]
        mixed = wav.replace(".wav", "_mix.wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-ss", f"{m.get('in', 0):.3f}", "-i", src_path(m["src"]),
             "-filter_complex", f"[1:a]atrim=duration={total:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
             f"volume={m.get('gain', -16)}dB,afade=t=in:d={m.get('fade_in', 0.8)},"
             f"afade=t=out:st={max(total - 1.5, 0):.3f}:d=1.5[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]",
             "-map", "[a]", "-ac", "2", "-ar", "48000", mixed])
        wav = mixed
    wav = normalize(wav)

    vf, t = [], 0.0
    for s in edl["shots"]:  # flash de 3 quadros no corte marcado
        if s.get("flash") and t > 0:
            for k, a in enumerate((0.8, 0.4, 0.12)):
                t0 = t + k / FPS
                vf.append(f"drawbox=x=0:y=0:w=iw:h=ih:color=white@{a}:t=fill:"
                          f"enable='between(t,{t0:.4f},{t0 + 1 / FPS - 0.002:.4f})'")
        t += s["dur"]
    if edl.get("film"):  # textura de cinema: grão temporal fino e vinheta suave
        vf += [f"noise=alls={2 + S}:allf=t", "vignette=angle=PI/5"]  # 6 dava 30 Mbps em 1080p
    vf += texts(edl, name, S) + ["format=yuv420p"]
    fo = min(0.8, total / 4)
    af = f"afade=t=in:d=0.15,afade=t=out:st={total - fo:.3f}:d={fo:.3f}"
    ovs = edl.get("overlays", [])
    for o in ovs:  # título já desenhado na escala do master (titles/08@2x.png) ANTES de montar o filtro:
        alt = o["png"].replace(".png", f"@{S}x.png")  # antes a troca vinha depois e o @2x era ampliado 2x de novo
        if S > 1 and os.path.exists(f"{ROOT}/{alt}"):
            o["png"] = alt
    if ovs:
        chain, prev = [f"[0:v]{','.join(vf[:-1]) or 'null'}[b0]"], "[b0]"
        for k, o in enumerate(ovs):
            a, b = o.get("start", 0), o.get("end", total)
            up = "" if S == 1 or "@" in o["png"] else f"scale=iw*{S}:ih*{S}:flags=lanczos,"
            fi, fo_ = o.get("fade_in", 0.25), o.get("fade_out", 0.25)
            slam = (f"scale=w='iw*(1+0.35*max(0,1-(t-{a})/0.18))':h=-1:eval=frame," if o.get("slam") else "")
            chain.append(f"[{2 + k}:v]format=rgba,{up}{slam}fade=t=in:st={a}:d={fi}:alpha=1,"
                         f"fade=t=out:st={b - fo_:.3f}:d={fo_}:alpha=1[o{k}]")
            oy = o.get("y", 250)
            oy = oy * S if isinstance(oy, (int, float)) else oy  # expressão ('(H-h)/2') vale como está
            chain.append(f"{prev}[o{k}]overlay=x={o.get('x', '(W-w)/2')}:y={oy}:"
                         f"enable='between(t,{a},{b})'[b{k + 1}]")
            prev = f"[b{k + 1}]"
        fc = ";".join(chain) + f";{prev}format=yuv420p[v];[1:a]{af}[a]"
    else:
        fc = f"[0:v]{','.join(vf)}[v];[1:a]{af}[a]"
    if edl.get("loop"):  # fim funde no começo: o último quadro vira o primeiro
        x = edl["loop"]
        L = total - x
        # acrossfade depois de asplit sai vazio no ffmpeg 6.1: fade + atraso + mix faz o mesmo
        fc = (f"[0:v]split[p][q];[p]trim=start={x},setpts=PTS-STARTPTS[a0];[q]trim=end={x},setpts=PTS-STARTPTS[b0];"
              f"[a0][b0]xfade=transition=fade:duration={x}:offset={L - x:.3f},{','.join(vf)}[v];"
              f"[1:a]asplit[m][n];[m]atrim=start={x},asetpts=PTS-STARTPTS,afade=t=out:st={L - x:.3f}:d={x}[c0];"
              f"[n]atrim=end={x},asetpts=PTS-STARTPTS,afade=t=in:d={x},adelay={int((L - x) * 1000)}:all=1[d0];"
              f"[c0][d0]amix=inputs=2:duration=first:normalize=0[a]")
    out = f"{ROOT}/out/{name}.mp4"
    os.makedirs(f"{ROOT}/out", exist_ok=True)
    extra = sum((["-loop", "1", "-t", f"{total:.3f}", "-i", f"{ROOT}/{o['png']}"] for o in ovs), [])
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav, *extra,
         "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264",
         "-preset", edl.get("preset", "slow" if S == 1 else "medium"), "-crf", str(edl.get("crf", 17) if S == 1 else 18),
         "-profile:v", "high", "-level", "4.2" if S == 1 else "5.1", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-g", str(FPS * 2), "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
         "-shortest", out])
    got = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]).strip() or 0)
    want = total - (edl.get("loop") or 0)
    if abs(got - want) > 0.1:  # já saiu um MP4 vazio sem erro: a duração é a prova
        sys.exit(f"{name}: duração {got:.2f}s, esperava {want:.2f}s")
    cover = edl.get("cover", 0.5)
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(cover), "-i", out, "-frames:v", "1", "-q:v", "2",
         f"{ROOT}/out/{name}_capa.jpg"])
    # folha de QA: 1 quadro a cada 0,5 s
    run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", "fps=2,scale=216:384,tile=10x5",
         "-frames:v", "1", "-q:v", "4", f"{ROOT}/out/{name}_qa.jpg"])
    info = run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate", "-of",
                "csv=p=0", out]).strip()
    print(f"{name}: {info}")


if __name__ == "__main__":
    for f in sys.argv[1:]:
        render(json.load(open(f)))
