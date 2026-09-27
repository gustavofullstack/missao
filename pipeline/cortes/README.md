# Cortes 9:16 de vídeos do YouTube

`cortes.py <plano.json> <saída>` gera, para cada corte do plano, um `.ass` (título e legenda palavra a palavra) e um `render.sh` com o ffmpeg.

- **Legenda:** vem da legenda automática do YouTube (`--write-auto-subs --sub-format json3`, trilha `pt-orig`). Não precisa de Whisper.
- **Trechos:** marcados por frase inicial e frase final, copiadas literalmente da transcrição.
- **Layout:** faixa de título no topo, vídeo em 3:4 recortado do 16:9 (`fx` define o centro horizontal do recorte) e crédito embaixo.

## Onde roda

O YouTube bloqueia download a partir do IP da VPS ("confirm you're not a bot"). Por isso o download e o render rodam no notebook (`ssh vaio`), e o `envio_loop.sh` traz os MP4 e sobe no Drive.

## Regras de escolha

- Só fonte oficial: canal do candidato ou vídeo oficial da campanha. Canais de cortes de terceiros, com marca e QR code na tela, ficam de fora.
- Sem xingamento a pessoa nomeada, sem acusação de crime a pessoa identificável, sem teoria não comprovada apresentada como fato e sem incitação à violência.
- Crédito da fonte sempre na tela.
