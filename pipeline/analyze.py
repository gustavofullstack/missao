#!/usr/bin/env python3
"""analyze.py SRC OUTDIR — mede cada keyframe do vídeo (luz, cor, nitidez, movimento, rostos)
e o áudio (volume, ataques, andamento). Grava OUTDIR/<nome>/analysis.json + thumbs/*.jpg."""
import json, os, re, subprocess, sys

import cv2
import numpy as np

src, outdir = sys.argv[1], sys.argv[2]
name = os.path.splitext(os.path.basename(src))[0]
od = os.path.join(outdir, name)
os.makedirs(os.path.join(od, "thumbs"), exist_ok=True)

pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json",
                                "-show_format", "-show_streams", src],
                               capture_output=True, text=True).stdout)
v = next(s for s in pr["streams"] if s["codec_type"] == "video")
a = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
W, H = int(v["width"]), int(v["height"])
rot = 0
for sd in v.get("side_data_list", []):
    if "rotation" in sd:
        rot = int(sd["rotation"])
if abs(rot) % 180 == 90:
    W, H = H, W
if H >= W:
    sw, sh = 360, int(round(360 * H / W / 2) * 2)
else:
    sw, sh = int(round(360 * W / H / 2) * 2), 360
hdr = v.get("color_transfer") in ("arib-std-b67", "smpte2084")
num, den = (int(x) for x in v.get("avg_frame_rate", "30/1").split("/"))
fps = num / den if den else 30.0
dur = float(pr["format"].get("duration", 0))

vf = f"scale={sw}:{sh}:flags=area"
if hdr:  # ponytail: tonemap só para medir/ver; a graduação final é decidida à parte
    vf += (",zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv")
vf += ",format=rgb24,showinfo"
errlog = os.path.join(od, "ffmpeg.log")
with open(errlog, "w") as ef:
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-nostats", "-loglevel", "info",
                          "-skip_frame", "nokey", "-i", src, "-an", "-sn", "-dn", "-vf", vf,
                          "-fps_mode", "passthrough", "-f", "rawvideo", "pipe:1"],
                         stdout=subprocess.PIPE, stderr=ef)
    fsz = sw * sh * 3
    frames, prev = [], None
    i = 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(sh, sw, 3)
        f = rgb.astype(np.float32)
        R, G, B = f[..., 0], f[..., 1], f[..., 2]
        Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
        rg, yb = R - G, 0.5 * (R + G) - B
        colorful = float(np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean()))
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        S = hsv[..., 1].astype(np.float32) / 255
        Vv = hsv[..., 2].astype(np.float32) / 255
        hue_hist, _ = np.histogram(hsv[..., 0].astype(np.float32) * 2, bins=12, range=(0, 360),
                                   weights=S * Vv)
        hs = hue_hist.sum()
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        small = cv2.GaussianBlur(cv2.resize(gray, (sw // 2, sh // 2), interpolation=cv2.INTER_AREA),
                                 (5, 5), 0).astype(np.float32)
        frames.append({
            "i": i,
            "luma": round(float(Y.mean()) / 255, 4),
            "contrast": round(float(Y.std()) / 255, 4),
            "clip_hi": round(float((f.max(axis=2) >= 250).mean()), 4),
            "clip_lo": round(float((Y <= 8).mean()), 4),
            "colorful": round(colorful, 2),
            "sat": round(float(S.mean()), 4),
            "hue": [round(float(x / hs), 3) if hs else 0 for x in hue_hist],
            "warm": round(float((R - B).mean()) / 255, 4),
            "sharp": round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 1),
            "motion": round(float(np.abs(small - prev).mean()), 3) if prev is not None else None,
        })
        cv2.imwrite(os.path.join(od, "thumbs", f"{i:05d}.jpg"),
                    cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 82])
        prev = small
        i += 1
    p.wait()

times = [float(m.group(1)) for m in re.finditer(r"pts_time:\s*([0-9.]+)", open(errlog).read())]
for fr, t in zip(frames, times):
    fr["t"] = round(t, 3)

audio = None
if a:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "pipe:1"], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    win = 8000  # 0,5 s
    n = len(x) // win
    rms = [round(float(20 * np.log10(np.sqrt((x[k * win:(k + 1) * win] ** 2).mean()) + 1e-9)), 1)
           for k in range(n)]
    # ataques (fluxo espectral) e andamento por autocorrelação
    hop, nfft = 256, 1024
    frames_a = np.lib.stride_tricks.sliding_window_view(x, nfft)[::hop] * np.hanning(nfft)
    mag = np.abs(np.fft.rfft(frames_a, axis=1))
    flux = np.maximum(np.diff(np.log1p(mag), axis=0), 0).sum(axis=1)
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    fr_rate = 16000 / hop
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    lo, hi = int(fr_rate * 60 / 180), int(fr_rate * 60 / 70)
    lag = lo + int(np.argmax(ac[lo:hi])) if hi < len(ac) else 0
    tempo = round(60 * fr_rate / lag, 1) if lag else None
    beat_strength = round(float(ac[lag] / ac[0]), 3) if lag else 0
    # fala: energia 300–3400 Hz sobre o total
    freqs = np.fft.rfftfreq(nfft, 1 / 16000)
    band = (freqs >= 300) & (freqs <= 3400)
    speech_ratio = float((mag[:, band] ** 2).sum() / ((mag ** 2).sum() + 1e-9))
    audio = {"rms_db_05s": rms, "tempo": tempo, "beat_strength": beat_strength,
             "speech_band_ratio": round(speech_ratio, 3),
             "codec": a.get("codec_name"), "channels": a.get("channels")}

meta = {"name": name, "file": os.path.basename(src), "duration": round(dur, 2), "fps": round(fps, 3),
        "w": W, "h": H, "rotation": rot, "hdr": hdr, "codec": v.get("codec_name"),
        "pix_fmt": v.get("pix_fmt"), "color_transfer": v.get("color_transfer"),
        "color_primaries": v.get("color_primaries"), "bit_rate": pr["format"].get("bit_rate"),
        "creation_time": pr["format"].get("tags", {}).get("creation_time"),
        "thumb_size": [sw, sh], "keyframes": len(frames)}
json.dump({"meta": meta, "frames": frames, "audio": audio}, open(os.path.join(od, "analysis.json"), "w"))
print(json.dumps(meta))
