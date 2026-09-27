# clk P TEXTO: clica no botão do diálogo com esse texto exato (último)
clk(){ timeout 30 node ~/postar/cdpd.mjs eval $1 "(()=>{const b=[...document.querySelectorAll(\"[role=dialog] [role=button], [role=dialog] button\")].filter(x=>x.innerText.trim()===\"$2\").pop();if(!b)return \"sem\";b.click();return \"ok\"})()"; }
btns(){ timeout 30 node ~/postar/cdpd.mjs eval $1 "[...document.querySelectorAll(\"[role=dialog] [role=button], [role=dialog] button\")].map(b=>b.innerText.trim()).filter(Boolean).join(\" | \")"; }
