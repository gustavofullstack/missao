#!/usr/bin/env python3
"""beats.py FLAC INICIO FIM — andamento e grade de batidas (Ellis 2007: autocorrelação + programação dinâmica)."""
import subprocess, sys

import numpy as np

path, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", path, "-ac", "1",
                      "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop, nfft, sr = 256, 1024, 16000
fr = np.lib.stride_tricks.sliding_window_view(x, nfft)[::hop] * np.hanning(nfft)
mag = np.log1p(10 * np.abs(np.fft.rfft(fr, axis=1)))
env = np.maximum(np.diff(mag, axis=0), 0).mean(axis=1)
env = np.convolve(env, np.hanning(5) / 2, "same")
env = (env - env.mean()) / (env.std() + 1e-9)
fps = sr / hop

ac = np.correlate(env, env, "full")[len(env) - 1:]
lags = np.arange(len(ac))
bpm = np.where(lags > 0, 60 * fps / np.maximum(lags, 1), 0)
w = np.exp(-0.5 * (np.log2(np.maximum(bpm, 1) / 120) / 0.9) ** 2) * (bpm >= 70) * (bpm <= 180)
period = int(np.argmax(ac * w))
tempo = 60 * fps / period

score, back = env.copy(), np.full(len(env), -1)
for t in range(len(env)):
    lo, hi = t - 2 * period, t - period // 2
    if hi <= 0:
        continue
    prev = np.arange(max(lo, 0), hi)
    pen = -100 * np.log((t - prev) / period) ** 2
    k = int(np.argmax(score[prev] + pen))
    score[t] += score[prev[k]] + pen[k]
    back[t] = prev[k]
t = int(np.argmax(score[-period:])) + len(score) - period
beats = []
while t >= 0:
    beats.append(t)
    t = back[t]
beats = np.array(beats[::-1]) / fps + a
strength = [round(float(env[int((bt - a) * fps)]), 2) for bt in beats]
print(f"tempo≈{tempo:.1f} BPM  período={period / fps:.3f}s  batidas={len(beats)}")
print(" ".join(f"{bt:.2f}({s:+.1f})" for bt, s in zip(beats, strength)))
