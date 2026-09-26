#!/usr/bin/env python3
"""vote5.py — trechos em dúvida do discurso completo, transcritos 12 vezes (2 modelos x com/sem vocabulário x 3 recortes).
A legenda do discurso completo só usa a versão que vencer por maioria (ou a de 2 modelos concordando)."""
import collections, os, subprocess, tempfile
import mlx_whisper

AUDIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
PROMPT = ("Renan Santos, Missão, Lula, Flávio Bolsonaro, Cleitinho, Zema, Centrão, Faria Lima, ChatGPT, "
          "The Economist, livro amarelo, terras raras, ímãs, Uberlândia.")
MODELOS = ["mlx-community/whisper-large-v3-turbo", "mlx-community/whisper-large-v3-mlx"]
DISPUTAS = [("IMG_8452", 1.6, 10.6), ("IMG_8452", 11.4, 17.4), ("IMG_8452", 18.0, 24.3), ("IMG_8452", 24.9, 28.46),
            ("IMG_8453", 0.0, 6.4), ("IMG_8453", 6.2, 12.4), ("IMG_8455", 10.6, 16.7), ("IMG_8455", 70.2, 80.7),
            ("IMG_8455", 85.4, 93.6), ("IMG_8457", 32.9, 46.3), ("IMG_8457", 46.9, 55.5), ("IMG_8457", 55.1, 61.9),
            ("IMG_8460", 20.8, 31.7), ("IMG_8460", 38.9, 42.5), ("IMG_8464", 18.5, 23.7), ("IMG_8464", 28.9, 36.1),
            ("IMG_8464", 138.9, 144.0), ("IMG_8464", 143.6, 153.2), ("IMG_8464", 152.8, 162.8), ("IMG_8465", 7.7, 17.0),
            ("IMG_8465", 17.3, 24.2), ("IMG_8465", 60.7, 71.0), ("IMG_8465", 71.3, 76.0), ("IMG_8465", 107.9, 116.0),
            ("IMG_8465", 145.2, 156.0), ("IMG_8465", 163.8, 173.4), ("IMG_8468", 0.0, 12.3), ("IMG_8468", 13.2, 24.1),
            ("IMG_8468", 23.9, 30.1), ("IMG_8468", 30.0, 36.5)]
for name, a, b in DISPUTAS:
    votos = collections.Counter()
    for m in MODELOS:
        for prompt in (None, PROMPT):
            for d in (-0.3, 0.0, 0.3):
                with tempfile.NamedTemporaryFile(suffix=".wav") as t:
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(max(0, a + d)), "-t", str(b - a),
                                    "-i", f"{AUDIO}/{name}.flac", "-ac", "1", "-ar", "16000", t.name], check=True)
                    txt = mlx_whisper.transcribe(t.name, path_or_hf_repo=m, language="pt", initial_prompt=prompt,
                                                 condition_on_previous_text=False, temperature=0.0)["text"].strip()
                votos[txt[:300]] += 1
    print(f"\n== {name} {a}-{b}", flush=True)
    for txt, n in votos.most_common(5):
        print(f"  {n:2d}x  {txt}", flush=True)
