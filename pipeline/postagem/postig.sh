#!/bin/bash
# postig.sh ARQUIVO ARQ_LEGENDA [LOCAL] : publica um reel no Instagram (@gusmatrix) pelo Brave "Missão Postagem".
cd ~/postar; . igclk.sh; E="timeout 30 node cdpd.mjs eval"
P=$(curl -s -X PUT "127.0.0.1:9222/json/new?https://www.instagram.com/gusmatrix/" | grep -oE "\"id\": \"[A-F0-9]+" | cut -d\" -f4 | cut -c1-8)
fecha(){ curl -s "127.0.0.1:9222/json/close/$(curl -s 127.0.0.1:9222/json/list | grep -oE "\"id\": \"$P[A-F0-9]+" | cut -d\" -f4)" >/dev/null; }
falha(){ echo "FALHOU IG $1 $(basename $ARQ)"; node cdpd.mjs shot $P /tmp/ig_falha.png 0.5 >/dev/null; [ -n "$DEBUG" ] && echo ABA=$P || fecha; exit 1; }
ARQ=$1
for i in $(seq 1 20); do [ "$($E $P "!!document.querySelector(\"svg[aria-label=\\\"New post\\\"]\")" 2>/dev/null)" = true ] && break; sleep 2; done
$E $P "document.querySelector(\"svg[aria-label=\\\"New post\\\"]\").closest(\"a,div[role=button],span\").click();1" >/dev/null; sleep 3
$E $P "(()=>{const p=[...document.querySelectorAll(\"a,div[role=button],span\")].filter(e=>/^(Post|Postar)$/.test(e.innerText)).pop();p&&p.click();return 1})()" >/dev/null; sleep 3
timeout 120 node cdpd.mjs upload $P "[role=dialog] input[type=file]" "$1" >/dev/null || falha upload
sleep 8; [ "$(clk $P OK)" = ok ] && sleep 3
$E $P "document.querySelector(\"[role=dialog] svg[aria-label=\\\"Select crop\\\"]\").closest(\"button,[role=button]\").click();1" >/dev/null || falha crop; sleep 2
$E $P "(()=>{const s=[...document.querySelectorAll(\"[role=dialog] span\")].find(x=>x.innerText.trim()===\"Original\");(s.closest(\"[role=button],button\")||s).click();return 1})()" >/dev/null || falha original; sleep 2
[ "$(clk $P Next)" = ok ] || falha next1; sleep 4
[ "$(clk $P Next)" = ok ] || falha next2; sleep 4
$E $P "document.querySelector(\"[role=dialog] [contenteditable=true][aria-label^=\\\"Add a caption\\\"]\").focus();1" >/dev/null || falha legenda
timeout 60 node cdpd.mjs type $P "$(cat "$2")" >/dev/null
[ "$($E $P "document.querySelector(\"[role=dialog] [contenteditable=true]\").innerText.length")" -gt 20 ] 2>/dev/null || falha legenda_vazia
if [ -n "$3" ]; then
  $E $P "document.querySelector(\"[role=dialog] input[placeholder=\\\"Add location\\\"]\").focus();1" >/dev/null
  timeout 30 node cdpd.mjs type $P "$3" >/dev/null; sleep 4; clk $P "$3 - MG" >/dev/null
  $E $P "(()=>{const h=[...document.querySelectorAll(\"[role=dialog] div\")].find(x=>x.innerText===\"New reel\");h&&h.click();return 1})()" >/dev/null; sleep 1
fi
# rótulo de IA e agendamento ficam desligados; compartilhar no Facebook vem LIGADO por padrão: desliga
$E $P "(()=>{for(const c of document.querySelectorAll(\"[role=dialog] input[type=checkbox]\"))if(c.checked)c.click();return 1})()" >/dev/null; sleep 1
[ "$($E $P "[...document.querySelectorAll(\"[role=dialog] input[type=checkbox]\")].some(c=>c.checked)")" = false ] || { $E $P "[...document.querySelectorAll(\"[role=dialog] input[type=checkbox]\")].map(c=>c.checked+\":\"+(c.closest(\"label,div\").parentElement.innerText||\"\").slice(0,50).replace(/\\n/g,\"/\")).join(\" ; \")"; falha switch_ligado; }
[ "$(clk $P Share)" = ok ] || falha share
for i in $(seq 1 60); do s=$($E $P "(document.querySelector(\"[role=dialog]\")||{innerText:\"\"}).innerText" 2>/dev/null); echo "$s" | grep -q "has been shared" && break; sleep 5; done
fecha
echo "$s" | grep -q "has been shared" && echo "POSTADO IG $(basename $1)" || echo "INCERTO IG $(basename $1)"
