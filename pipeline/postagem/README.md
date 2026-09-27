# Postagem por CDP (Brave dedicado "Missão Postagem", no vaio)

O login é feito à mão pelo dono da conta nessa janela; nenhum script digita senha.
`cdpd.mjs` (ponte CDP local, 127.0.0.1) não está aqui porque depende do token local.

| Script | O quê |
|---|---|
| `postx.sh ARQ TEXTO` | X: compositor em diálogo, espera o botão habilitar |
| `postyt.sh ARQ TITULO DESC` | YouTube Studio: título ≤ 100, não é para crianças, sem conteúdo alterado, público; devolve o link |
| `postig.sh ARQ LEGENDA [LOCAL]` | Instagram: proporção Original, legenda, local; **desliga o compartilhamento com o Facebook, que vem ligado por padrão** |
| `fila_*.sh` | publica `fila_*.json` com intervalo `INTERVALO` (s) |

Filas geradas por `pipeline/cortes/fila_yt.py <números>` a partir das legendas.
