#!/usr/bin/env python3
"""transcribe_v5.py — large-v3 (não turbo) com tempo por palavra nos clipes de fala, para o discurso completo.
Vocabulário no prompt só com nomes próprios que aparecem na fala (o prompt antigo vazou no 8459)."""
import json, os, sys
import mlx_whisper

AUDIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
PROMPT = ("Renan Santos, Missão, Lula, Flávio Bolsonaro, Cleitinho, Faria Lima, ChatGPT, The Economist, "
          "PCC, Comando Vermelho, Juiz de Fora, Triângulo, Uberlândia.")
CLIPES = ["IMG_8452", "IMG_8453", "IMG_8455", "IMG_8457", "IMG_8460", "IMG_8463", "IMG_8464", "IMG_8465", "IMG_8468", "IMG_8472"]
out = []
for name in CLIPES:
    r = mlx_whisper.transcribe(f"{AUDIO}/{name}.flac", path_or_hf_repo="mlx-community/whisper-large-v3-mlx", language="pt",
                               word_timestamps=True, initial_prompt=PROMPT, condition_on_previous_text=False, temperature=0.0)
    for s in r["segments"]:
        out.append({"src": name, "start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip(),
                    "no_speech": round(s.get("no_speech_prob", 0), 2), "logprob": round(s.get("avg_logprob", 0), 2),
                    "words": [{"w": w["word"].strip(), "s": round(w["start"], 2), "e": round(w["end"], 2),
                               "p": round(w.get("probability", 0), 2)} for w in s.get("words", [])]})
    print(name, "ok", flush=True)
    json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
