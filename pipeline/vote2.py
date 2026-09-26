#!/usr/bin/env python3
"""vote.py — trechos em disputa transcritos várias vezes (2 modelos x com/sem vocabulário x 3 recortes);
a legenda só entra com a versão que vencer por maioria."""
import collections, os, subprocess, tempfile

import mlx_whisper

AUDIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
PROMPT = "Discurso de Renan Santos em Uberlândia, Minas Gerais. Terras raras, zonas econômicas especiais, livro amarelo."
MODELOS = ["mlx-community/whisper-large-v3-turbo", "mlx-community/whisper-large-v3-mlx"]
DISPUTAS = [("IMG_8464", 35.6, 41.4, "rodamos / roubamos"), ("IMG_8464", 18.4, 23.6, "não leem / livro"),
            ("IMG_8465", 91.6, 96.4, "servir o / no Brasil"), ("IMG_8465", 96.8, 105.0, "Tesla / BYD"),
            ("IMG_8465", 51.5, 60.2, "abertura terras raras"), ("IMG_8468", 30.0, 33.0, "votar em ___"),
            ("IMG_8457", 0.4, 6.4, "deixar claro / 14 ou nada"), ("IMG_8460", 0.0, 4.0, "Globo chama o Renan")]
for name, a, b, tema in DISPUTAS:
    votos = collections.Counter()
    for m in MODELOS:
        for prompt in (None, PROMPT):
            for d in (-0.4, 0.0, 0.4):
                with tempfile.NamedTemporaryFile(suffix=".wav") as t:
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a + d), "-t", str(b - a),
                                    "-i", f"{AUDIO}/{name}.flac", "-ac", "1", "-ar", "16000", t.name], check=True)
                    txt = mlx_whisper.transcribe(t.name, path_or_hf_repo=m, language="pt", initial_prompt=prompt,
                                                 condition_on_previous_text=False, temperature=0.0)["text"].strip()
                votos[txt] += 1
    print(f"\n== {name} {a}-{b} ({tema})")
    for txt, n in votos.most_common():
        print(f"  {n:2d}x  {txt}")
