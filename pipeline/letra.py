#!/usr/bin/env python3
"""letra.py MUSICA OUT.json — tempos por palavra do vocal da faixa (large-v3), para pôr o coro na tela no tempo certo."""
import json, sys
import mlx_whisper
r = mlx_whisper.transcribe(sys.argv[1], path_or_hf_repo="mlx-community/whisper-large-v3-mlx", language="pt",
                           word_timestamps=True, condition_on_previous_text=False, temperature=0.0,
                           initial_prompt="Missão! Missão! Fora ladrões! Fora corrupção! Rap nacional.")
json.dump([{"start": s["start"], "end": s["end"], "text": s["text"].strip(),
            "words": [{"w": w["word"].strip(), "s": round(w["start"], 2), "e": round(w["end"], 2)} for w in s.get("words", [])]}
           for s in r["segments"]], open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
for s in r["segments"]:
    print(f'{s["start"]:6.1f}-{s["end"]:6.1f} {s["text"].strip()}')
