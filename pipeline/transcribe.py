#!/usr/bin/env python3
"""transcribe.py AUDIODIR OUTDIR — Whisper large-v3-turbo local (MLX), pt, tempo por palavra."""
import glob, json, os, sys

import mlx_whisper

audio_dir, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(f"{audio_dir}/*.flac")):
    name = os.path.splitext(os.path.basename(f))[0]
    dst = f"{out}/{name}.json"
    if os.path.exists(dst):
        continue
    r = mlx_whisper.transcribe(f, path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                               language="pt", word_timestamps=True,
                               condition_on_previous_text=False)
    segs = [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip(),
             "no_speech": round(s.get("no_speech_prob", 0), 2),
             "logprob": round(s.get("avg_logprob", 0), 2),
             "words": [{"w": w["word"], "s": round(w["start"], 2), "e": round(w["end"], 2),
                        "p": round(w.get("probability", 0), 2)} for w in s.get("words", [])]}
            for s in r["segments"]]
    json.dump({"name": name, "segments": segs}, open(dst, "w"), ensure_ascii=False)
    print(name, len(segs), "segmentos", flush=True)
