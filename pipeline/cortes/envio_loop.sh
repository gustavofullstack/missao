#!/bin/bash
# Traz do vaio os cortes que ainda não estão aqui e sobe no Drive. Roda até não haver nada novo.
cd /root/reels/cortes
for f in $(ssh vaio 'ls ~/cortes/out/*.mp4' | xargs -n1 basename); do
  [ -s out/$f ] && [ "$(stat -c%s out/$f)" = "$(ssh vaio stat -c%s cortes/out/$f)" ] && continue
  scp -q vaio:cortes/out/$f out/$f && echo "trazido $f"
done
rclone copy out "gdrive:REELS PRONTOS (Claude) 26.09/CORTES 27.09 (Sorocaba)" --drive-root-folder-id 1UvWtAw9xCjOfhxWfkVE9EerrimsZ3zC6 --drive-chunk-size 16M --timeout 60s && echo DRIVE_OK $(ls out | wc -l)
