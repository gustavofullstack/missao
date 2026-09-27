#!/bin/bash
# agenda.sh DATA SUFIXO : dispara as três filas do dia (X e YT a cada 80 min, IG a cada 150 min — 6/dia, a rede mais sensível a volume)
cd ~/postar; D=$1; S=$2
for r in "x 09:00 4800" "yt 09:10 4800" "ig 09:20 9000"; do set -- $r
  espera=$(( $(date -d "$D $2" +%s) - $(date +%s) ))
  [ $espera -gt 0 ] || { echo "horário $D $2 já passou"; continue; }
  setsid bash -c "sleep $espera; FILA=./fila_$1$S.json INTERVALO=$3 ./fila_$1.sh" >> fila_$1.log 2>&1 < /dev/null &
  echo "fila $1$S agendada para $D $2"
done
