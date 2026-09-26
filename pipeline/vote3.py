#!/usr/bin/env python3
"""vote.py — trechos em disputa transcritos várias vezes (2 modelos x com/sem vocabulário x 3 recortes);
a legenda só entra com a versão que vencer por maioria."""
import collections, os, subprocess, tempfile

import mlx_whisper

AUDIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
PROMPT = "Discurso de Renan Santos em Uberlândia, Minas Gerais. Terras raras, zonas econômicas especiais, livro amarelo."
MODELOS = ["mlx-community/whisper-large-v3-turbo", "mlx-community/whisper-large-v3-mlx"]
DISPUTAS = [("IMG_8463", 0.0, 4.2, "abertura: quem lê o editorial"), ("IMG_8463", 3.6, 8.4, "o editorial deixa claro"),
            ("IMG_8463", 8.2, 14.0, "virando as costas pra vocês"), ("IMG_8463", 13.5, 20.8, "eles afirmam: candidato"),
            ("IMG_8463", 20.2, 26.6, "tornar o Brasil potência"), ("IMG_8463", 26.4, 30.5, "coro: superpotência"),
            ("IMG_8464", 65.3, 72.9, "estive com o empresariado"), ("IMG_8464", 72.6, 80.6, "estive ao lado da elite"),
            ("IMG_8464", 80.9, 88.0, "ninguém disse que não é brilhante"), ("IMG_8464", 87.7, 95.0, "quantos apoiaram? nenhum"),
            ("IMG_8455", 0.0, 5.6, "estado mais politizado")]
for name, a, b, tema in DISPUTAS:
    votos = collections.Counter()
    for m in MODELOS:
        for prompt in (None, PROMPT):
            for d in (-0.4, 0.0, 0.4):
                with tempfile.NamedTemporaryFile(suffix=".wav") as t:
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a + d), "-t", str(b - a),
                                    "-i", f"{AUDIO}/{name}.flac", "-ac", "1", "-ar", "16000", t.name], check=True)
                    txt = mlx_whisper.transcribe(t.name, path_or_hf_repo=m, language="pt", initial_prompt=prompt,
                                                 condition_on_previous_text=False, temperature=0.0)["text"].strip()
                votos[txt] += 1
    print(f"\n== {name} {a}-{b} ({tema})")
    for txt, n in votos.most_common():
        print(f"  {n:2d}x  {txt}")
