#!/usr/bin/env python3
"""summary.py WORKDIR — uma linha por vídeo com as medianas das métricas e o áudio."""
import glob, json, statistics as st, sys

for aj in sorted(glob.glob(f"{sys.argv[1]}/*/analysis.json")):
    d = json.load(open(aj))
    m, fr, a = d["meta"], d["frames"], d["audio"] or {}

    def med(k):
        return st.median([f[k] for f in fr if f.get(k) is not None] or [0])

    r = a.get("rms_db_05s") or [-99]
    print(f'{m["name"][-8:]:>8} {m["duration"]:6.1f}s {m["fps"]:4.0f}fps luma={med("luma"):.2f} '
          f'ctr={med("contrast"):.2f} color={med("colorful"):5.1f} sat={med("sat"):.2f} '
          f'warm={med("warm"):+.2f} sharp={med("sharp"):5.0f} mot={med("motion"):5.1f} | '
          f'tempo={a.get("tempo")} beat={a.get("beat_strength")} speech={a.get("speech_band_ratio")} '
          f'rms_med={st.median(r):.0f} max={max(r):.0f} | {(m["creation_time"] or "")[11:19]}')
