#!/bin/bash
# postx.sh ARQUIVO TEXTO : publica um vídeo no X (@gustavo_devx) pelo Brave "Missão Postagem".
cd ~/postar
P=$(curl -s -X PUT "127.0.0.1:9222/json/new?https://x.com/compose/post" | grep -oE "\"id\": \"[A-F0-9]+" | cut -d\" -f4 | cut -c1-8)
for i in $(seq 1 20); do [ "$(timeout 15 node cdpd.mjs eval $P "document.querySelectorAll(\"[role=dialog] input[data-testid=fileInput]\").length" 2>/dev/null)" = 1 ] && break; sleep 2; done
timeout 90 node cdpd.mjs upload $P "[role=dialog] input[data-testid=fileInput]" "$1" >/dev/null
timeout 20 node cdpd.mjs eval $P "document.querySelector(\"[role=dialog] [data-testid=tweetTextarea_0]\").focus(); 1" >/dev/null
timeout 20 node cdpd.mjs type $P "$2" >/dev/null
for i in $(seq 1 90); do s=$(timeout 20 node cdpd.mjs eval $P "(()=>{const b=document.querySelector(\"[role=dialog] [data-testid=tweetButton]\");return b?(b.getAttribute(\"aria-disabled\")||\"false\"):\"sem\"})()" 2>/dev/null); [ "$s" = "false" ] && break; sleep 10; done
[ "$s" = "false" ] || { echo "FALHOU botao=$s $1"; exit 1; }
timeout 20 node cdpd.mjs eval $P "document.querySelector(\"[role=dialog] [data-testid=tweetButton]\").click(); 1" >/dev/null
sleep 10; ok=$(timeout 20 node cdpd.mjs eval $P "document.querySelectorAll(\"[role=dialog] [data-testid=tweetButton]\").length")
curl -s "127.0.0.1:9222/json/close/$(curl -s 127.0.0.1:9222/json/list | grep -oE "\"id\": \"$P[A-F0-9]+" | cut -d\" -f4)" >/dev/null
[ "$ok" = 0 ] && echo "POSTADO X $(basename $1)" || echo "INCERTO X $(basename $1)"
