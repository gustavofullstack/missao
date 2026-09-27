#!/bin/bash
# postyt.sh ARQUIVO TITULO ARQ_DESCRICAO : publica no YouTube (canal Missão/gusmatrix) pelo Brave "Missão Postagem".
cd ~/postar; C=UCfl3RZupMRdktXfkB1Fparg; E="timeout 30 node cdpd.mjs eval"
[ ${#2} -le 100 ] || { echo "FALHOU titulo>100 $1"; exit 1; }
P=$(curl -s -X PUT "127.0.0.1:9222/json/new?https://studio.youtube.com/channel/$C/videos/upload?d=ud" | grep -oE "\"id\": \"[A-F0-9]+" | cut -d\" -f4 | cut -c1-8)
fecha(){ curl -s "127.0.0.1:9222/json/close/$(curl -s 127.0.0.1:9222/json/list | grep -oE "\"id\": \"$P[A-F0-9]+" | cut -d\" -f4)" >/dev/null; }
for i in $(seq 1 30); do [ "$($E $P "document.querySelectorAll(\"ytcp-uploads-dialog input[type=file]\").length" 2>/dev/null)" = 1 ] && break; sleep 2; done
timeout 120 node cdpd.mjs upload $P "ytcp-uploads-dialog input[type=file]" "$1" >/dev/null
for i in $(seq 1 30); do [ "$($E $P "!!document.querySelector(\"#title-textarea #textbox\")" 2>/dev/null)" = true ] && break; sleep 2; done
sleep 3
T=$(node -e "console.log(JSON.stringify(process.argv[1]))" "$2"); D=$(node -e "console.log(JSON.stringify(require(\"fs\").readFileSync(process.argv[1],\"utf8\").trim()))" "$3")
$E $P "(()=>{const s=(q,v)=>{const t=document.querySelector(q);t.focus();document.execCommand(\"selectAll\");document.execCommand(\"insertText\",false,v)};s(\"#title-textarea #textbox\",$T);s(\"#description-textarea #textbox\",$D);document.querySelector(\"tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]\").click();return 1})()" >/dev/null
$E $P "(()=>{document.querySelector(\"#toggle-button\").click();return 1})()" >/dev/null; sleep 2
$E $P "(()=>{for(const n of [\"VIDEO_AGE_RESTRICTION_NONE\",\"VIDEO_PAID_PRODUCT_PLACEMENT_NO\",\"VIDEO_HAS_ALTERED_CONTENT_NO\"]){const r=document.querySelector(\"tp-yt-paper-radio-button[name=\"+n+\"]\");r&&r.click()}return 1})()" >/dev/null
tl=$($E $P "document.querySelector(\"#title-textarea #textbox\").innerText.length")
[ "$tl" -gt 0 ] 2>/dev/null || { echo "FALHOU titulo vazio $1"; exit 1; }
for i in 1 2 3; do $E $P "document.querySelector(\"#next-button\").click(); 1" >/dev/null; sleep 3; done
$E $P "document.querySelector(\"tp-yt-paper-radio-button[name=PUBLIC]\").click(); 1" >/dev/null; sleep 2
# espera o envio acabar (botão Publicar habilitado)
for i in $(seq 1 90); do s=$($E $P "(()=>{const b=document.querySelector(\"#done-button\");return b?String(b.hasAttribute(\"disabled\")):\"sem\"})()" 2>/dev/null); [ "$s" = false ] && break; sleep 10; done
$E $P "document.querySelector(\"#done-button\").click(); 1" >/dev/null
for i in $(seq 1 60); do u=$($E $P "(()=>{const a=document.querySelector(\"a[href*='youtube.com/shorts/'], a[href*='youtu.be/'], ytcp-video-share-dialog a[href*=youtu]\");return a?a.href:\"\"})()" 2>/dev/null); [ -n "$u" ] && break; sleep 3; done
# não fecha a aba com envio em andamento (vídeo grande): espera até 60 min
for i in $(seq 1 360); do $E $P "/Enviando|Uploading|carregad[oa] \\d|\\d+% /.test(document.body.innerText)" 2>/dev/null | grep -q true || break; sleep 10; done
fecha
[ -n "$u" ] && echo "POSTADO YT $(basename $1) $u" || echo "INCERTO YT $(basename $1)"
