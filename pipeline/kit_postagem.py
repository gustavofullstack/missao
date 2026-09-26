#!/usr/bin/env python3
"""kit_postagem.py — KIT_DE_POSTAGEM.txt: por peça, legenda (IG/TikTok), texto do X (<= 280), título do Shorts (<= 100),
capa e horário. Trava: aviso de IA nas peças com IA, sem travessão, limites de tamanho."""
import json

L1 = json.load(open("legendas.json"))
L3 = json.load(open("legendas3.json"))
IA = {"14": "Trilha criada com IA (Google Flow Music).", "15": "Trilha criada com IA (Google Flow Music).",
      "16": "Música e vinhetas criadas com IA (Google Flow), imagens do ato reais.",
      "17": "Rap e vinhetas criados com IA (Google Flow); o coro é da música. Fala e praça reais.",
      "18": "Ilustrações e trilha criadas com IA (Google Flow). Fala real.",
      "19": "Vinhetas da onça geradas por IA (Google Flow); som e coro reais da praça.",
      "20": "Rap e vinhetas criados com IA (Google Flow); o coro é da música. Cenas da praça reais.",
      "21": "Trilha e vinhetas criadas com IA (Google Flow), marcadas na tela; falas e coros reais."}
X = {
 "17": "“Quantos deles apoiaram?” … “Nenhum!” Uberlândia, 25/09. {ia} #Missão14",
 "15": "O que a The Economist escreveu sobre Renan Santos, com as fontes (BBC News Brasil e Estadão), e o que ele disse em Uberlândia. {ia}",
 "18": "Terras raras, ímãs, baterias e drones: a proposta que o Renan apresentou em Uberlândia, ilustrada. {ia}",
 "16": "MERCADORES DA MISÉRIA, o clipe com as imagens reais do ato de Uberlândia. {ia}",
 "14": "Renan em Uberlândia: seis meses com a elite do país. “Quantos deles apoiaram? Nenhum!” {ia}",
 "09": "“Ei, Globo, chama o Renan!” A praça em Uberlândia pedindo o 14 no debate. Som original.",
 "01": "Uberlândia, 25/09. Sinalizador, fumaça, bandeira e o jingle. Você tinha que estar aqui.",
 "08": "“É 14 ou nada!” O palanque falou e a Praça Rui Barbosa respondeu. Uberlândia, 25/09.",
 "03": "Parece cena de filme, mas foi em Uberlândia na sexta à noite. Som original dos estouros.",
 "10": "“Quem tá aqui com o livro amarelo?” Renan em Uberlândia, legendado palavra por palavra.",
 "02": "Cada bandeira subindo devagar na frente da igreja. 120 quadros por segundo, nada inventado.",
 "13": "Missão. Eu voto 14. Renan. O Brasil é nosso. 14 ou nada. Cinco coros reais da praça.",
 "07": "Antes de tudo, repara na luz. Uberlândia, 25/09.",
 "11": "Terras raras, ímãs, baterias e drones: o trecho do discurso do Renan em Uberlândia sobre Minas.",
 "04": "A câmera vai abrindo e a praça não acaba. Uberlândia, 25/09.",
 "12": "O final do discurso em Uberlândia, legendado palavra por palavra.",
 "05": "“O Brasil que importa está aqui na minha frente, em Uberlândia.”",
 "06": "Deixa rodar mais uma vez. 🌙",
 "19": "“MISSÃO!” e “EU VOTO 14!”: o coro real da Praça Rui Barbosa, em Uberlândia. {ia}",
 "20": "MISSÃO! FORA LADRÕES! FORA CORRUPÇÃO! Uberlândia, 25/09. {ia}",
 "21": "O ato de Uberlândia em 1 minuto. {ia}",
}
YT = {"17": "Quantos deles apoiaram? NENHUM! #Shorts", "15": "O que a The Economist escreveu sobre Renan Santos #Shorts",
      "18": "O plano das terras raras, ilustrado #Shorts", "16": "Mercadores da Miséria (clipe) · Uberlândia 25/09",
      "14": "Renan: quantos empresários apoiaram? Nenhum! #Shorts", "09": "Ei, Globo, chama o Renan! #Shorts",
      "01": "Você tinha que estar aqui · Uberlândia 25/09 #Shorts", "08": "É 14 ou nada! · Uberlândia #Shorts",
      "03": "Isso não é filme · Uberlândia 25/09 #Shorts", "10": "Quem tá aqui com o livro amarelo? #Shorts",
      "02": "Tem noite que merece câmera lenta #Shorts", "13": "O que a praça gritou em Uberlândia #Shorts",
      "07": "A luz dessa noite · Uberlândia #Shorts", "11": "O plano das terras raras · Renan em Uberlândia #Shorts",
      "04": "Olha o tamanho disso · Uberlândia #Shorts", "12": "O final do discurso · Uberlândia #Shorts",
      "05": "O Brasil que importa está aqui #Shorts", "06": "Lua na torre, sem fim #Shorts",
      "19": "MISSÃO! EU VOTO 14! · Uberlândia #Shorts",
      "20": "MISSÃO! Fora ladrões, fora corrupção #Shorts",
      "21": "O ato de Uberlândia em 1 minuto #Shorts"}
ORDEM = [("09", "já publicado no Instagram 10:25"), ("17", "12:30"), ("21", "13:30"), ("15", "14:15"), ("18", "15:30"), ("01", "16:30"),
         ("08", "17:30"), ("19", "18:15"), ("16", "19:00"), ("10", "20:00"), ("20", "20:45"), ("13", "21:30"), ("03", "22:15"),
         ("02", "sáb 27, 10:00"), ("11", "sáb 27, 12:00"), ("07", "sáb 27, 15:00"), ("14", "sáb 27, 18:00 (TikTok/Shorts)"),
         ("04", "dom 28, 10:00"), ("12", "dom 28, 13:00"), ("05", "dom 28, 17:00"), ("06", "Story, qualquer hora")]
nomes = {k[:2]: k for k in list(L1) + list(L3)}
out = ["KIT DE POSTAGEM · @gusmatrix · Instagram, TikTok, X e YouTube Shorts",
       "Arquivos: pasta REELS PRONTOS (Claude) 26.09 no Drive (1080p) e subpastas 4K SDR e LEVA 3 (IA + marca).",
       "Regra: não impulsionar pago; no dia 4/10 (votação) não postar. Nas peças com IA, mantenha o aviso do texto.", ""]
for n, quando in ORDEM:
    k = nomes[n]
    leg = L3.get(k) or L1[k]
    x = X[n].format(ia=IA.get(n, "")).strip()
    assert len(x) <= 280, (n, len(x))
    assert len(YT[n]) <= 100, n
    for t in (leg, x, YT[n]):
        assert "—" not in t and "–" not in t, n
    if n in IA:
        assert "IA" in x and "IA" in leg, n
    capa = f"{k}_capa_ia.jpg" if n in ("16", "17", "18") else f"{k}_capa.jpg"
    out += [f"================ {n} · {k}.mp4 · postar: {quando}", f"Capa: {capa}", "",
            "[Instagram / TikTok]", leg, "", f"[X] ({len(x)} caracteres)", x, "",
            f"[YouTube Shorts] título: {YT[n]}", "descrição: " + leg.split("\n")[0] + (" " + IA[n] if n in IA else ""), "", ""]
open("KIT_DE_POSTAGEM.txt", "w").write("\n".join(out))
print("KIT_DE_POSTAGEM.txt", len("\n".join(out)), "caracteres,", len(ORDEM), "peças")
