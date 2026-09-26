#!/usr/bin/env python3
"""ab_voz.py — inteligibilidade como prova: confiança média do Whisper no áudio original x com a cadeia de voz."""
import subprocess, tempfile, statistics as st
import mlx_whisper
VOZ = ("highpass=f=80,lowpass=f=14000,equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.4:g=3,"
       "acompressor=threshold=0.089:ratio=2.5:attack=10:release=150:makeup=1.5")
for src, a, b in [("IMG_8464", 10.4, 36.0), ("IMG_8465", 71.3, 94.0), ("IMG_8468", 13.2, 30.0)]:
    res = {}
    for nome, af in [("original", "anull"), ("voz", VOZ)]:
        with tempfile.NamedTemporaryFile(suffix=".wav") as t:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", f"audio/{src}.flac",
                            "-af", af, "-ac", "1", "-ar", "16000", t.name], check=True)
            r = mlx_whisper.transcribe(t.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="pt",
                                       word_timestamps=True, condition_on_previous_text=False, temperature=0.0)
        ps = [w["probability"] for s in r["segments"] for w in s.get("words", [])]
        res[nome] = (st.mean(ps), sum(p < 0.5 for p in ps), len(ps))
    o, v = res["original"], res["voz"]
    print(f"{src} {a}-{b}: original p̄={o[0]:.3f} baixas={o[1]}/{o[2]}  |  voz p̄={v[0]:.3f} baixas={v[1]}/{v[2]}")
