#!/bin/bash
# upload.sh <final.mp4>... — cópia para subir pelo navegador: a extensão do Chrome aceita no máximo 10 MB por arquivo.
# Vídeo em 2 passes com o bitrate exato que cabe em 9,5 MB; o áudio (AAC 192k) é copiado, sem nova perda.
set -euo pipefail
ALVO=9500000   # bytes; margem sob o limite de 10 MB
mkdir -p upload
for f in "$@"; do
  n=$(basename "$f" .mp4); out="upload/$n.mp4"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  tam=$(stat -f %z "$f")
  if [ "$tam" -le "$ALVO" ]; then cp "$f" "$out"; echo "$n: já cabe ($tam bytes), copiado"; continue; fi
  # kbps de vídeo = orçamento total - áudio (192k) - 2% de contêiner
  vk=$(python3 -c "print(int(($ALVO*8/$dur/1000 - 192) * 0.98))")
  pre=""; [ "$vk" -lt 2600 ] && pre="-vf hqdn3d=1.2:1.2:5:5"   # longo: tira o ruído noturno antes de comprimir
  log="upload/$n.2pass"
  ffmpeg -v error -y -i "$f" $pre -c:v libx264 -preset slow -tune film -b:v ${vk}k -pass 1 -passlogfile "$log" \
    -an -f mp4 /dev/null
  ffmpeg -v error -y -i "$f" $pre -c:v libx264 -preset slow -tune film -b:v ${vk}k -maxrate $((vk*2))k -bufsize $((vk*2))k \
    -pass 2 -passlogfile "$log" -profile:v high -pix_fmt yuv420p \
    -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart "$out"
  rm -f "$log"*
  echo "$n: ${dur}s  ${vk}k  $(stat -f %z "$out") bytes ${pre:+(hqdn3d)}"
done
