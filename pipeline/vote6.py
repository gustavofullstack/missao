#!/usr/bin/env python3
"""vote5.py — trechos em dúvida do discurso completo, transcritos 12 vezes (2 modelos x com/sem vocabulário x 3 recortes).
A legenda do discurso completo só usa a versão que vencer por maioria (ou a de 2 modelos concordando)."""
import collections, os, subprocess, tempfile
import mlx_whisper

AUDIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
PROMPT = ("Renan Santos, Missão, Lula, Flávio Bolsonaro, Cleitinho, Zema, Centrão, Faria Lima, ChatGPT, "
          "The Economist, livro amarelo, terras raras, ímãs, Uberlândia.")
MODELOS = ["mlx-community/whisper-large-v3-turbo", "mlx-community/whisper-large-v3-mlx"]
DISPUTAS = [("IMG_8454", 60.2, 68.2), ("IMG_8454", 70.6, 81.9), ("IMG_8454", 81.6, 92.5), ("IMG_8454", 95.9, 107.5),
            ("IMG_8454", 130.0, 145.0), ("IMG_8454", 185.3, 205.2), ("IMG_8458", 0.0, 8.5), ("IMG_8458", 36.5, 50.2),
            ("IMG_8458", 58.0, 74.2), ("IMG_8458", 86.0, 102.8), ("IMG_8458", 102.6, 118.6), ("IMG_8458", 118.2, 128.4),
            ("IMG_8458", 155.0, 162.5), ("IMG_8458", 180.5, 195.6)]
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
