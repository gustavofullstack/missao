#!/bin/bash
# baixa.sh ID... : vídeo (até 1440p) + legenda automática pt-orig (json3, com tempo por palavra) em ~/cortes
cd ~/cortes
for id in "$@"; do
  ~/.ytdlp/bin/yt-dlp -q --no-warnings -f "bv*[height<=1440][ext=mp4]+ba[ext=m4a]/bv*[height<=1440]+ba/b" --merge-output-format mp4 \
    --write-auto-subs --sub-langs pt-orig --sub-format json3 --sleep-requests 3 --sleep-subtitles 30 \
    -o "%(id)s.%(ext)s" "https://www.youtube.com/watch?v=$id" && mv -f "$id.pt-orig.json3" "$id.pt.json3" 2>/dev/null
  ls "$id.mp4" "$id.pt.json3" 2>&1 | tr '\n' ' '; echo; sleep 60
done; echo FIM_BAIXA
