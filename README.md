# Missão Reels — pipeline aberto de cortes verticais 4K SDR (9:16)

> **Projeto independente de um apoiador** (Gustavo Mendes Almeida Rodrigues, [@gusmatrix](https://www.instagram.com/gusmatrix/)), feito com agentes de IA.
> **Não é canal oficial do Partido Missão** e não fala em nome do partido nem do candidato.
> Ativos oficiais da marca (logo, bandeira, fotos) **não** estão neste repositório: baixe-os em [missao.org.br](https://missao.org.br/).

Transforma gravações brutas de iPhone (HLG HDR) de um ato público em reels, TikToks e Shorts verticais (9:16), guiados pelo áudio: a fala e o coro decidem o corte, a legenda só mostra texto confirmado por votação de transcrição, e cada peça sai em 1080p e em master 4K SDR.

## Por que existe

O ato de 25/09/2026 na Praça Rui Barbosa, em Uberlândia (MG), foi gravado de dentro da multidão. Este código documenta como virou uma série de reels com fidelidade de áudio e de fonte.
Sobre o editorial citado no palanque: a The Economist publicou em 24/09/2026 "Brazil turns its back on the future"; segundo a BBC News Brasil, a revista escolheu a candidatura de Renan Santos como a que mais se aproxima do que o momento exige, e, segundo o Estadão, o descreveu como "libertário combativo". Qualquer texto que cite a revista deve usar essas fontes, não paráfrases.

## Regras do pipeline (valem para qualquer contribuição)

1. **Legenda de fala só com consenso**: cada trecho é transcrito 12 vezes (2 modelos Whisper × com/sem vocabulário × 3 recortes); entra na tela a versão que vence a votação. Trecho sem consenso fica sem legenda ou fora do corte.
2. **IA sempre rotulada** (TSE, Res. 23.610/2019, art. 9º-B): música criada com IA e vinhetas geradas por IA levam rótulo fixo na tela durante o vídeo inteiro, selo nos planos sintéticos e aviso por escrito na legenda do post.
3. **Nada de deepfake**: nenhuma imagem, voz ou vídeo sintético de pessoa real. Vinhetas de IA são simbólicas (onça, bandeira, terras raras, drones) e nunca simulam multidão.
4. **Coro sintético não é coro do público**: quando a música de IA tem coro, a legenda do post diz que o coro é da música.
5. **Evidência antes de promessa**: duração, loudness e frames de cada saída são medidos (`ffprobe`, `loudnorm`) antes de entregar.

## Arquitetura

- **Cor**: HLG BT.2020 → SDR BT.709 com `tonemap=mobius`, `npl=203` (venceu teste A/B de 6 variantes). Looks noturnos `noite`, `noite_clara`, `fogo`, `fogo_quente`; `neutro` para vinhetas de IA já graduadas.
- **Áudio**: voz do palanque com passa-altas 80 Hz, −2 dB em 200 Hz, +3 dB em 3,2 kHz e compressor 2,5:1; cama musical opcional sob a fala (`"musica"` na EDL, −19 a −22 dB); `loudnorm` em duas passadas para −14 LUFS e pico real ≤ −1,5 dBTP.
- **Legendas**: blocos de até 3 palavras medidos com a própria fonte (zona segura de 900 px), animação "pop" de 0,12 s, intervalos meio-abertos (sem quadro duplo).
- **Marca**: `marca.py` gera títulos (Barlow Condensed), bandeira, mapa com pino, card final e rótulos de IA a partir dos ativos oficiais que você baixar do site.
- **4K**: EDL com `"escala": 2` gera 2160×3840; títulos desenhados direto em @2x (o `render.py` troca para o arquivo @2x antes de montar o filtro, então não há ampliação dupla).

```
pipeline/render.py      motor: EDL JSON → MP4 (planos em cache, legendas, overlays, cama musical, grão de filme)
pipeline/build_v2.py    leva 2: cortes de fala e coro (EDLs em edl/)
pipeline/build_v3.py    leva 3: marca, trilha do Flow Music, vinhetas de IA (EDLs em edl3/)
pipeline/marca.py       artes da identidade visual a partir dos ativos oficiais
pipeline/titulo.py      títulos da leva 2
pipeline/vote*.py       votação de transcrição (mlx-whisper, Apple Silicon)
pipeline/transcribe*.py transcrição com tempo por palavra (large-v3)
pipeline/letra.py       tempos por palavra do vocal de uma música (para o texto do coro cair no tempo)
pipeline/beats.py       andamento e grade de batidas (autocorrelação + programação dinâmica)
pipeline/legendas*.py   legendas dos posts com travas (≥ 500 caracteres, 3–5 hashtags, sem travessão, aviso de IA)
pipeline/upload.sh      cópia ≤ 9,5 MB em 2 passes para envio pelo navegador
```

## Catálogo (26/09/2026)

| # | Peça | Duração | Observação |
|---|---|---|---|
| 01–07 | clima do ato (sinalizador, câmera lenta, plano geral, lua, luz) | 5–18 s | áudio original |
| 08 | É 14 ou nada | 19 s | fala + coro |
| 09 | Ei, Globo, chama o Renan | 9 s | coro |
| 10 | Quem tá aqui com o livro amarelo? | 30 s | fala |
| 11 | O plano das terras raras | 40 s | fala |
| 12 | O final do discurso | 23 s | fala |
| 13 | O que a praça gritou | 19 s | 5 coros reais |
| 14 | Quantos deles apoiaram? Nenhum! | 28 s | fala + trilha de IA (rotulada) |
| 15 | O que a The Economist escreveu | 22,5 s | fala + card com as fontes |
| 16 | Mercadores da Miséria (clipe) | 2 min 48 s | rap criado com IA + imagens reais + vinhetas de IA, tudo rotulado |
| 17 | A rua tá gritando | 33 s | fala + refrão do rap de IA + vinhetas de IA, rotulados |
| 18 | Terras raras com IA | 42 s | fala do 11 ilustrada com vinhetas de IA nas palavras-chave |

## Como rodar

Requisitos: Python 3.10+ com `pillow` e `numpy`; FFmpeg 6.1+ com `zscale` (libzimg) e `drawtext` (libfreetype); `rsvg-convert` para os SVGs da marca; `mlx-whisper` só para transcrever (Apple Silicon).

```bash
python3 pipeline/render.py edl/01_voce_tinha_que_estar_aqui.json      # 1080x1920
python3 pipeline/render.py edl4k/01_voce_tinha_que_estar_aqui.json    # 2160x3840
```

Os caminhos de trabalho (`/root/reels/src`, `seg/`, `out/`, `titles/`) ficam no topo de `render.py` e `marca.py`.

## Licença

Código sob licença MIT (veja `LICENSE`). Marcas, logos e fotos do Partido Missão e do candidato pertencem aos respectivos titulares e não estão incluídos.
