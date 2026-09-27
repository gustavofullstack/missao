#!/bin/bash
# Publica a fila no Instagram, um post a cada INTERVALO segundos (padrão 40 min).
cd ~/postar; N=$(node -e "console.log(require(\"${FILA:-./fila_ig.json}\").length)")
for i in $(seq 0 $((N-1))); do
  f=$(node -e "console.log(require(\"${FILA:-./fila_ig.json}\")[$i][0])"); t=$(node -e "console.log(require(\"${FILA:-./fila_ig.json}\")[$i][1])"); d=$(node -e "console.log(require(\"${FILA:-./fila_ig.json}\")[$i][2])")
  echo "$(date +%H:%M) $(./postig.sh "$f" "$t")"
  [ $i -lt $((N-1)) ] && sleep ${INTERVALO:-2400}
done; echo FIM_FILA
