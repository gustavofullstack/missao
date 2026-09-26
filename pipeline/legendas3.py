#!/usr/bin/env python3
"""legendas3.py — legendas dos posts da leva 3 (14–18). Mesmas travas da leva 1: >= 500 caracteres, 3–5 hashtags,
sem travessão; e, onde há música ou imagem gerada por IA, o aviso por escrito (TSE, Res. 23.610/2019 art. 9-B)."""
import json, os, re

L = {
"14_quantos_deles_apoiaram": """“Quantos deles apoiaram?” … “Nenhum!”

Em Uberlândia, na noite de 25 de setembro, o Renan contou que esteve ao lado da elite e dos grandes empresários do país ao longo dos últimos seis meses.

Segundo ele, nenhum disse que o projeto não é brilhante e todos concordaram que é o que o Brasil precisa. A pergunta que fecha o trecho ficou no ar por alguns segundos antes da resposta.

A legenda acompanha a fala palavra por palavra, com o áudio original da praça. Aviso: a batida por baixo é uma faixa instrumental criada com IA no Google Flow Music, indicada também na tela.

Manda pra quem acha que só apoio de cima resolve.

📍 Praça Rui Barbosa, Uberlândia

#uberlandia #renansantos #partidomissao #eleicoes2026""",

"15_o_que_a_the_economist_escreveu": """O que a The Economist escreveu e o que o Renan disse sobre isso em Uberlândia.

No palanque, na noite de 25 de setembro, ele citou o editorial que diz que “o Brasil está virando as costas para o futuro”. É o título do texto da revista britânica publicado no dia 24: “Brazil turns its back on the future”.

No fim do vídeo está o que a revista escreveu, com as fontes: segundo a BBC News Brasil, a candidatura dele é a que mais se aproxima do que o momento exige; segundo o Estadão, a revista o chamou de “libertário combativo”, que defende reformas para transformar o Brasil em uma grande potência.

Aviso: trilha de fundo criada com IA no Google Flow Music, indicada também na tela.

Salva e compartilha com a fonte junto.

#theeconomist #renansantos #partidomissao #eleicoes2026""",

"16_mercadores_da_miseria_clipe": """MERCADORES DA MISÉRIA · o clipe inteiro, 2 minutos e 48 segundos.

Começa com a fala da noite de 25 de setembro em Uberlândia: “Minas Gerais, o segundo estado do Brasil, o estado mais politizado do Brasil.” Depois entra o rap, cortado na batida com as imagens reais do ato na Praça Rui Barbosa: sinalizador, fumaça, bandeira e o coro.

Aviso: a música (letra, voz e batida) foi criada com IA no Google Flow Music, e as vinhetas da onça, do olho em chamas e da bandeira sob a lua são imagens geradas por IA no Google Flow, marcadas na tela. As cenas do povo, do palco e da praça são reais, gravadas no iPhone.

Assiste com som alto.

📍 Uberlândia, MG

#rapnacional #partidomissao #uberlandia #eleicoes2026""",

"17_a_rua_ta_gritando": """“Quantos deles apoiaram?” … “Nenhum!” E aí entra o rap.

Trinta segundos do ato de 25 de setembro em Uberlândia: a pergunta do palanque, a pausa e o refrão do rap “Mercadores da Miséria” (“Missão! Fora ladrões! Fora corrupção!”) em cima das imagens reais da praça.

Aviso: o rap, com letra, voz e coro, foi criado com IA no Google Flow Music; o coro é da música, não do público. O olho da onça, a onça na fumaça e a bandeira sob a lua são imagens geradas por IA no Google Flow e aparecem marcadas na tela. A fala do palanque e as cenas da praça são gravação real do ato.

Manda pra quem precisa ouvir isso hoje.

📍 Praça Rui Barbosa, Uberlândia

#rapnacional #partidomissao #renansantos #uberlandia""",

"18_terras_raras_com_ia": """Terras raras, ímãs, baterias e drones: a proposta que o Renan apresentou em Minas, ilustrada.

É o mesmo trecho do discurso de 25 de setembro em Uberlândia, com a fala e a legenda originais. Nas palavras-chave entram ilustrações geradas por IA no Google Flow: cristais de terras raras, ímãs flutuando, a fábrica de baterias e o enxame de drones. Cada ilustração aparece marcada na tela como imagem gerada por IA.

Na fala, ele cita zonas econômicas especiais em parceria com outros países e empresas, para fazer a extração e o processamento de terras raras e fabricar ímãs, baterias e drones, e diz que a fábrica de baterias tem que ser em Minas Gerais.

Trilha de fundo criada com IA no Google Flow Music.

Salva pra acompanhar esse debate.

#terrasraras #minasgerais #partidomissao #uberlandia""",
}

if __name__ == "__main__":
    for k, v in L.items():
        tags = re.findall(r"#\w+", v)
        assert len(v) >= 500, (k, len(v))
        assert 3 <= len(tags) <= 5, (k, tags)
        assert "—" not in v and "–" not in v, k
        if k.startswith(("16", "17", "18")):
            assert "IA" in v, k
        print(f"{k}: {len(v)} caracteres, {len(tags)} hashtags")
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(L, open(f"{here}/legendas3.json", "w"), ensure_ascii=False, indent=1)
    with open(f"{here}/LEGENDAS_LEVA3.txt", "w") as f:
        for k, v in L.items():
            f.write(f"===== {k}.mp4 =====\n\n{v}\n\n\n")
