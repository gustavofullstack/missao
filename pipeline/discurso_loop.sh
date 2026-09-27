#!/bin/bash
# Monta as 8 partes do discurso e a íntegra, uma de cada vez.
cd /root/reels
for n in 1 2 3 4 5 6 7 8 integra; do
  e=edl_discurso/30_discurso_parte$n.json; [ $n = integra ] && e=edl_discurso/30_discurso_integra.json
  venv/bin/python valida_planos.py $e
  /usr/bin/time -f "%e s parte $n" venv/bin/python render.py $e && echo "PRONTA parte $n $(date +%H:%M)"
done
echo FIM
