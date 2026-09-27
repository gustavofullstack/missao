#!/bin/bash
# Publica a fila no X, um post a cada INTERVALO segundos (padrão 40 min).
cd ~/postar; N=$(node -e "console.log(require(\"${FILA:-./fila_x.json}\").length)")
for i in $(seq 0 $((N-1))); do
  f=$(node -e "console.log(require(\"${FILA:-./fila_x.json}\")[$i][0])"); t=$(node -e "console.log(require(\"${FILA:-./fila_x.json}\")[$i][1])")
  echo "$(date +%H:%M) $(./postx.sh "$f" "$t")"
  [ $i -lt $((N-1)) ] && sleep ${INTERVALO:-2400}
done; echo FIM_FILA
