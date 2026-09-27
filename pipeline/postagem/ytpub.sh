# ytpub.sh (source): do diálogo de upload aberto em $P até "Vídeo publicado". Define $u (link) ou deixa vazio.
ytpub(){
  u=""
  for i in $(seq 1 20); do
    c=$($E $P "(()=>{const r=document.querySelector(\"tp-yt-paper-radio-button[name=PUBLIC]\");if(r&&r.offsetParent){r.click();return r.getAttribute(\"aria-checked\")}document.querySelector(\"#next-button\").click();return \"next\"})()" 2>/dev/null)
    [ "$c" = true ] && break; sleep 3
  done
  [ "$c" = true ] || { echo "sem radio Publico"; return 1; }
  for i in $(seq 1 90); do s=$($E $P "(()=>{const b=document.querySelector(\"#done-button\");return b?String(b.hasAttribute(\"disabled\")):\"sem\"})()" 2>/dev/null); [ "$s" = false ] && break; sleep 10; done
  $E $P "document.querySelector(\"#done-button\").click(); 1" >/dev/null
  # só vale o link DENTRO do diálogo "Vídeo publicado" (a barra lateral do upload já mostra youtu.be desde o início)
  for i in $(seq 1 60); do u=$($E $P "(()=>{const d=document.querySelector(\"ytcp-video-share-dialog\");if(!d||!/publicado|published/i.test(d.innerText))return \"\";const m=d.innerText.match(/https:\\/\\/(youtube\\.com\\/shorts|youtu\\.be)\\/[\\w-]+/);return m?m[0]:\"\"})()" 2>/dev/null); [ -n "$u" ] && break; sleep 3; done
}
