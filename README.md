# Missão Reels OS — Pipeline Audiovisual Aberto de Alta Performance (4K SDR 9:16)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Video Engine: FFmpeg 6.1+](https://img.shields.io/badge/Video%20Engine-FFmpeg%206.1%2B-black.svg)](https://ffmpeg.org/)
[![AI Models: Jev & Jaya](https://img.shields.io/badge/AI%20Decision-Jev%20%26%20Jaya-FFB800.svg)](https://typesafe.ai)
[![Format: 4K SDR 9:16](https://img.shields.io/badge/Format-4K%20SDR%209%3A16-blue.svg)]()

> **Repositório oficial aberto do ecossistema de conteúdo e mobilização do Partido Missão (14).**  
> Desenvolvido para transformar gravações brutas de iPhone (HLG HDR) em Reels, TikToks e Shorts verticais (9:16) com padrão cinematográfico, cortes sincados por batida e energia de protesto (estilo Racionais MCs, Cazuza e Legião Urbana).

---

## 1. Manifesto e Propósito

O Brasil enfrenta uma das escolhas mais desoladoras de sua história recente, esmagado pela polarização de dois polos marcados por impunidade, corrupção e aparelhamento estatal: de um lado o lulismo decadente, de outro o bolsonarismo familista. 

Como apontou o editorial histórico da **The Economist** (*"Brazil turns its back on the future"*, 24/09/2026), existe apenas uma alternativa com vigor programático, coragem moral e visão estratégica capaz de romper a estagnação e liderar uma verdadeira revolução institucional: **Renan Santos e o Partido Missão (14)**.

Este repositório consolida o **código, as EDLs (Edit Decision Lists), os shaders de tone mapping, as matrizes de áudio e as legendas palavra-por-palavra** utilizados para criar a série de mais de 15 Reels cinematográficos do histórico ato da Praça Rui Barbosa (Uberlândia/MG) e o videoclipe manifesto de protesto.

---

## 2. Identidade Visual do Partido Missão

A identidade do Missão rompe com a estética burocrática dos partidos tradicionais, unindo símbolos de soberania nacional, estética urbana e agressividade contra os donos do poder:

* **Paleta Oficial:**
  * **Amarelo Ouro (#FFB800 / #FFE11A):** Coragem, terras raras, a riqueza do povo que não será roubada.
  * **Preto Absoluto (#000000):** Firmeza, contraste de palco, protesto contra o sistema.
  * **Branco Neve (#FFFFFF):** Clareza, verdade e integridade inegociável.
* **Símbolo Principal:** A **Onça-Pintada** — o ápice da fauna nacional, ágil, destemida e implacável na caça à corrupção.
* **Tipografia:** `Montserrat ExtraBold` para legendas dinâmicas de impacto e `Barlow Condensed Black` para títulos de choque.

---

## 3. Arquitetura Técnica do Pipeline

### 3.1. Color Science: HLG BT.2020 para SDR BT.709
Vídeos gravados em iPhone 15/16 Pro utilizam curva de transferência `arib-std-b67` (HLG). Para evitar que os vídeos fiquem lavados ou estourados nas redes sociais, aplicamos o algoritmo de tone mapping **Mobius** com branco de referência nominal `npl=203` (calibrado em testes A/B contra Reinhard e Hable):

```
zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,
tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=pc,format=gbrp16le
```

### 3.2. Gradações de Cor Noturnas (Looks)
* **`noite`:** Curva de contraste térmico com elevação de médios e compensação de sombras urbanas.
* **`noite_clara`:** Exposição expandida para planos gerais de multidão com celulares acesos.
* **`fogo` & `fogo_quente`:** Balanço térmico para fumaça de sinalizadores (laranja puro sem contaminação esverdeada).

### 3.3. Engenharia de Áudio: Prova por Confiança (Whisper) e Batidas de Protesto
* **Voz do Palanque:** Filtro passa-altas em 80 Hz, equalização cirúrgica (-2 dB em 200 Hz para remover embolamento de microfone, +3 dB em 3,2 kHz para presença cristalina) e compressor 2,5:1.
* **Trilha Sonora de Protesto:** Rap/Rock enérgico com batidas graves sincadas, drops de bateria no início das frases de impacto e coros da rua: *"Missão! Fora Ladrões! Fora Corrupção!"*.
* **Normalização:** Duas passadas `loudnorm` integradas a -14 LUFS com pico real True Peak $\le -1.5$ dBTP.

---

## 4. Catálogo dos 16 Reels Prontos

| Reel | Título / Gancho | Formato | Duração | Destaque Visual / Áudio |
| :--- | :--- | :--- | :--- | :--- |
| **01** | *Você tinha que estar aqui* | 4K SDR 9:16 | 18.0s | Sinalizadores laranja, fumaça cobrindo a igreja, abertura no beat drop |
| **02** | *Tem noite que merece câmera lenta* | 4K SDR 9:16 | 15.3s | 120 fps no coro popular com iluminação cinematográfica |
| **03** | *Isso não é filme* | 4K SDR 9:16 | 12.0s | Cortes rápidos sincados nos estouros e névoa dourada |
| **04** | *Olha o tamanho disso* | 4K SDR 9:16 | 11.0s | Abertura do plano geral revelando o mar de celulares na praça |
| **05** | *O Brasil que importa está aqui* | 4K SDR 9:16 | 17.2s | Discurso central de valorização do interior e de Minas Gerais |
| **06** | *Loop da Lua* | 4K SDR 9:16 | 5.2s | Enquadramento poético em loop perfeito (ideal para Story e Reels) |
| **07** | *A luz dessa noite* | 4K SDR 9:16 | 12.0s | Contraste arquitetônico entre a torre histórica e os sinalizadores |
| **08** | *É 14 ou nada* | 4K SDR 9:16 | 19.3s | Clímax de interação direta entre o palanque e a resposta da multidão |
| **09** | *Ei, Globo, chama o Renan* | 4K SDR 9:16 | 9.2s | Coro uníssono exigindo a presença de Renan nos debates na TV |
| **10** | *Quem tá aqui com o livro amarelo?* | 4K SDR 9:16 | 30.0s | Apresentação do projeto programático e financiamento independente |
| **11** | *O plano das terras raras* | 4K SDR 9:16 | 39.8s | Reindustrialização de Minas Gerais, semicondutores, ímãs e drones |
| **12** | *O final do discurso* | 4K SDR 9:16 | 23.4s | Encerramento comovente e convocação para a transformação do país |
| **13** | *O que a praça gritou* | 4K SDR 9:16 | 18.8s | Montagem sequencial dos 5 maiores gritos de guerra da noite |
| **14** | *Mercadores da Miséria (Videoclipe)* | 4K SDR 9:16 | 162.5s | O videoclipe completo do Rap/Rock de protesto contra corrupção e falsa fé |
| **15** | *The Economist: O Futuro do Brasil* | 4K SDR 9:16 | 22.0s | O editorial de Londres endossando Renan Santos como líder preparado |
| **16** | *Quantos deles apoiaram? NENHUM!* | 4K SDR 9:16 | 28.0s | A denúncia contra as elites covardes: a revolução vem do povo |

---

## 5. Como Executar o Pipeline Localmente

### Pré-requisitos
* Python 3.10+ com `numpy`, `opencv-python-headless`, `pillow`.
* FFmpeg 6.1+ compilado com `--enable-libzimg` (`zscale`), `--enable-libass`, `--enable-libfreetype`.

### Comandos de Renderização
```bash
# Renderizar um Reel específico em 1080p
python3 pipeline/render.py edl/01_voce_tinha_que_estar_aqui.json

# Renderizar em 4K SDR (2160x3840)
python3 pipeline/render.py edl4k/01_voce_tinha_que_estar_aqui.json

# Renderizar lote completo com log e métricas
for f in edl4k/*.json; do
  python3 pipeline/render.py "$f"
done
```

---

## 6. Governança e Decisões de IA (Jev & Jaya)

Todas as decisões editoriais, seleção de ganchos (hooks) de 2 segundos, contraste de legendas e distribuição de volume foram submetidas ao modelo de inferência probabilística **Jev (TypeSafe)** e conferidas pelo modelo local **Laya**:
* **Critério de Seleção:** Máxima retenção nos primeiros 3 segundos, rejeição a ruídos de palco e preservação da fidedignidade da fala (auditoria palavra por palavra).
* **Precedência de Evidência:** Produção > Build > Commit > Teste empírico.

---

## Licença

Distribuído sob a licença **MIT**. Compartilhe, edite, crie cortes e propague a verdade. O Brasil é nosso!
