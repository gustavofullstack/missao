#!/usr/bin/env python3
"""transcribe_v6.py — os dois clipes que faltavam no discurso (IMG_8454 e IMG_8458), mesmo método do v5; junta no v5."""
import json, os
import mlx_whisper

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT = ("Renan Santos, Missão, Lula, Flávio Bolsonaro, Cleitinho, Zema, Centrão, Faria Lima, ChatGPT, "
          "The Economist, livro amarelo, terras raras, Uberlândia.")
v5 = json.load(open(f"{HERE}/transcripts_v5.json"))
for name in ["IMG_8454", "IMG_8458"]:
    r = mlx_whisper.transcribe(f"{HERE}/audio/{name}.flac", path_or_hf_repo="mlx-community/whisper-large-v3-mlx", language="pt",
                               word_timestamps=True, initial_prompt=PROMPT, condition_on_previous_text=False, temperature=0.0)
    v5 = [s for s in v5 if s["src"] != name]
    for s in r["segments"]:
        v5.append({"src": name, "start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip(),
                   "no_speech": round(s.get("no_speech_prob", 0), 2), "logprob": round(s.get("avg_logprob", 0), 2),
                   "words": [{"w": w["word"].strip(), "s": round(w["start"], 2), "e": round(w["end"], 2),
                              "p": round(w.get("probability", 0), 2)} for w in s.get("words", [])]})
        print(f"{name} [{s['start']:6.1f}-{s['end']:6.1f}] {s['text'].strip()}", flush=True)
json.dump(v5, open(f"{HERE}/transcripts_v5.json", "w"), ensure_ascii=False, indent=1)
