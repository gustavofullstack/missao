#!/usr/bin/env python3
"""transcribe2.py OUT.json — retranscreve só as janelas candidatas a corte com o large-v3 completo
(mais preciso que o turbo) e vocabulário do evento; tempos por palavra já no relógio do arquivo original."""
import json, os, subprocess, sys, tempfile

import mlx_whisper

AUDIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
PROMPT = ("Discurso em Uberlândia, Minas Gerais. Partido Missão, número 14, Renan Santos. Terras raras, "
          "zonas econômicas especiais, ímãs, baterias, drones, livro amarelo, propostas, Centrão, Estado, "
          "estrada de ferro, infraestrutura, superpotência. Coro: Missão! O Brasil é nosso!")
JANELAS = [("IMG_8464", 9.5, 47.0), ("IMG_8465", 26.0, 38.0), ("IMG_8465", 50.0, 132.0),
           ("IMG_8465", 174.0, 182.2), ("IMG_8468", 0.0, 39.5), ("IMG_8452", 0.0, 28.5),
           ("IMG_8463", 0.0, 32.8), ("IMG_8460", 0.0, 4.0), ("IMG_8457", 0.0, 25.0),
           ("IMG_8455", 83.0, 94.9), ("IMG_8445", 29.0, 35.0), ("IMG_8448", 27.0, 33.0)]
out = []
for name, a, b in JANELAS:
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i",
                        f"{AUDIO}/{name}.flac", "-ac", "1", "-ar", "16000", t.name], check=True)
        r = mlx_whisper.transcribe(t.name, path_or_hf_repo="mlx-community/whisper-large-v3-mlx",
                                   language="pt", word_timestamps=True, initial_prompt=PROMPT,
                                   condition_on_previous_text=False, temperature=0.0)
    for s in r["segments"]:
        out.append({"src": name, "start": round(a + s["start"], 2), "end": round(a + s["end"], 2),
                    "text": s["text"].strip(),
                    "words": [{"w": w["word"].strip(), "s": round(a + w["start"], 2), "e": round(a + w["end"], 2),
                               "p": round(w.get("probability", 0), 2)} for w in s.get("words", [])]})
    print(name, a, b, "ok", flush=True)
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
