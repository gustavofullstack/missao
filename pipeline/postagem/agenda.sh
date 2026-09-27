#!/bin/bash
# agenda.sh DATA SUFIXO : dispara as três filas do dia (X 09:00, YT 09:10, IG 09:20; 80 min entre posts)
cd ~/postar; D=$1; S=$2
for r in "x 09:00" "yt 09:10" "ig 09:20"; do set -- $r
  espera=$(( $(date -d "$D $2" +%s) - $(date +%s) ))
  [ $espera -gt 0 ] || { echo "horário $D $2 já passou"; continue; }
  setsid bash -c "sleep $espera; FILA=./fila_$1$S.json INTERVALO=4800 ./fila_$1.sh" >> fila_$1.log 2>&1 < /dev/null &
  echo "fila $1$S agendada para $D $2"
done
