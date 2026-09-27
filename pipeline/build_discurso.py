#!/usr/bin/env python3
"""build_discurso.py — o discurso do Renan em Uberlândia (25/09/2026) inteiro e em ordem, com legenda palavra a palavra:
5 partes de até 2:20 (cabem em Reels, Shorts, TikTok e no X sem Premium) + a íntegra. Só imagem e som reais: sem trilha e sem IA.
Silêncio de mais de 1 s vira 0,65 s (corte seco, alternando o enquadramento para esconder o pulo).
Fora do corte, de propósito (risco de remoção e de direito de resposta): xingamento pessoal a adversário nomeado
("bêbado", "bandido", "burro"), "destruir aquelas pessoas que comandam o STF, o Senado e a Presidência" e a frase do
CDB do Banco Master. O resto está na ordem em que foi gravado (IMG_8452 → IMG_8468, com 8454 e 8458).
Também fora: o coro "prendeu, matou" com "a gente só quer matar uns bandidos" (IMG_8454 0–68 s: política de
violência das plataformas) e "Dias Toffoli… vagabundo… ladrão" (IMG_8458 162–179 s: injúria a ministro nomeado)."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v2 as b2  # karaoke/chunks/cabe (legenda em blocos de até 3 palavras)

V5 = json.load(open(f"{HERE}/transcripts_v5.json"))  # large-v3 com tempo por palavra, todos os clipes de fala
AMARELO, BLACK = "#FCBE26", "/usr/share/fonts/truetype/marca/BarlowCondensed-Black.ttf"
GAP, ANTES, DEPOIS = 1.0, 0.25, 0.4  # silêncio que vira corte; folga antes da 1ª palavra e depois da última
PUNCH = 1.12  # corte seco no mesmo plano: alterna o zoom base e o zoom base x 1,12
# enquadramento de cada fonte (o mesmo dos reels anteriores): zoom base e ponto de foco
QUADRO = {"IMG_8452": (1.3, [0.5, 0.62]), "IMG_8453": (1.3, [0.5, 0.65]), "IMG_8455": (1.3, [0.5, 0.58]),
          "IMG_8454": (1.3, [0.5, 0.55]), "IMG_8458": (1.3, [0.5, 0.55]),
          "IMG_8457": (1.35, [0.5, 0.5]), "IMG_8460": (1.2, [0.5, 0.5]), "IMG_8463": (1.35, [0.48, 0.42]),
          "IMG_8464": (1.4, [0.5, 0.45]), "IMG_8465": (1.4, [0.48, 0.47]), "IMG_8468": (1.45, [0.55, 0.5])}
DURACAO = {"IMG_8452": 28.46, "IMG_8453": 71.79, "IMG_8454": 205.21, "IMG_8455": 94.89, "IMG_8457": 62.69,
           "IMG_8458": 196.5, "IMG_8460": 86.88, "IMG_8463": 32.77, "IMG_8464": 174.43, "IMG_8465": 182.23,
           "IMG_8468": 39.49}  # ffprobe: plano que passa do fim do arquivo derruba o render (contagem de quadros)
norm = lambda t: re.sub(r"[^0-9a-zà-ÿ]", "", t.lower())

# correções de transcrição (texto errado do large-v3 -> o que foi dito), conferidas na votação (vote5.log)
TROCAS = {  # "…" = trecho que nem a votação resolveu: a legenda não inventa palavra
    "IMG_8452": [("de estrada em estrada de ferro", "de estrada a estrada de ferro"),
                 ("escolar pelo som de vocês", "escoar…"),
                 ("esse sistema maldito para que ele siga os brasileiros e não se siga os brasileiros?",
                  "esse sistema maldito pra que ele sirva os brasileiros e não se sirva dos brasileiros?"),
                 ("o Santana maldiçoado precisa de regra para ele parar de roubar gente e administrar mal essas cidades?",
                  "o Centrão é amaldiçoado e precisa de regra pra ele parar de roubar a gente e administrar mal nossas cidades?"),
                 ("Há crime em dizer que nós estamos cometendo para ser a campanha...",
                  "Que crime nós estamos cometendo nessa campanha?")],
    "IMG_8453": [("pra Rede Globo no Diário dos Debates, pro senhor Flávio Bolsonaro falando pra BNCBP, ele não paga o debate CV. "
                  "Quem quer fixe pra merecer isso? Nessinha quer fixe.",
                  "com a Rede Globo no dia dos debates, com o senhor Flávio Bolsonaro falando com a Band… "
                  "O que eu fiz pra merecer isso? …")],
    "IMG_8455": [("o luva de pedreiro", "o Luva de Pedreiro"), ("ver. Ele não vai fazer", "Ele não vai fazer"),
                 ("com o nome vermelho", "o Comando Vermelho"), ("Minas gereste de solução.", "Minas Gerais tem solução."),
                 ("estão voltando até um", "estão votando até num"), ("minha frente, no Belândia.", "minha frente, em Uberlândia."),
                 ("Recense o Brasil que importa.", "… o Brasil que importa."),
                 ("Ao mesmo tempo, a classe", "Ao mesmo tempo, A classe")],
    "IMG_8454": [("a seguinte notícia no globo.", "a seguinte notícia no Globo:"),
                 ("Um gente, pessoa assaltada na hora da copa -cabeira", "Urgente: pessoa assaltada na orla de Copacabana."),
                 ("assaltada a mão armada", "assaltada à mão armada."), ("foi barril na mata", "foi varrido do mapa."),
                 ("Os especialistas da governança", "Os especialistas…"), ("assalto a mão armada", "assalto à mão armada"),
                 ("Este Renan", "Esse Renan"), ("nos próximos dois anos", "nos próximos 10 anos"),
                 ("Ele acha que vai, mas ele é precioso", "Ele acha que vai…"),
                 ("como a gente viu nos dias de fora,", "como a gente viu…,")],
    "IMG_8458": [("nas unhas.", "nas urnas."), ("na seleção,", "nessa eleição,"), ("Apenas na seleção.", "Apenas nessa eleição."),
                 ("o tempo de tempo que", "o tempo de TV que"), ("14 de cabarrado", "14 de cabo a rabo"),
                 ("o que eu revelei hoje", "o que eu revelo hoje"),
                 ("daquela glem, daquele mando negro de bolsonaristas.", "daquela…, daquele… de bolsonaristas."),
                 ("retiraram agora o nosso direito", "Retiraram agora o nosso direito")],
    "IMG_8457": [("muito glória para todo mundo.", "muito claro para todo mundo."), ("Vieira, eu contei", "Eu contei"),
                 ("liberou os candidatos do novo Apoio ao Flávio.", "liberou os candidatos do Novo: apoio ao Flávio."),
                 ("Pois bem, Vieira ofereceu isso pro conhecido Nevo Ramião.", "Pois bem, …")],
    "IMG_8460": [("destruir o crime organizado", "destruir o crime organizado.")],
    "IMG_8463": [("que trabalham, que vocês que trabalham.", "que trabalham.")],
    "IMG_8464": [("Não foi a mesma coisa", "não fez a mesma coisa"), ("da Econômios", "da The Economist"),
                 ("nós pudermos.", "nós pudemos."), ("andando na farianina,", "andando na Faria Lima,"),
                 ("não andam,", "não leem,"), ("abrir teu livro amanhã,", "abrir o teu livro,"),
                 ("A elite vai dar com eles", "A elite vai andar com eles."), ("Canalha liderando", "canalha liderando")],
    "IMG_8465": [("Não queremos ver,", "Não queremos…"), ("Nós estaremos em zonas", "Nós teremos zonas"), ("da BID,", "da BYD,"),
                 ("Se os super -humans, se os humans", "Se os superímãs, se os ímãs"),
                 ("feito nas Minas Gerais.", "feito em Minas Gerais."), ("no nível amarelo.", "no Livro Amarelo."),
                 ("que o Estado é mais errobado nos próximos anos se a gente não ganhasse a vocês, né?",
                  "que o estado… nos próximos anos, se a gente não ganhar, né?"),
                 ("um parceiro melhor que as terras raras.", "um parceiro melhor para as terras raras."),
                 ("mulher e prado", "mulher e brabo")],
    "IMG_8468": [("fazendo limão,", "fazendo ímã,"), ("estão que usufruem disso.", "têm que usufruir disso."),
                 ("e para a nossa eleição o nosso número é 14.", "e pra vencer a eleição, o nosso número é 14."),
                 ("você não precisa votar em ladrão.", "")],  # nome disputado na votação (ladrão/Abram): sem legenda
}


def palavras(src, corrige=True):
    ws = [dict(w) for s in V5 if s["src"] == src for w in s["words"] if w["w"].strip()]
    for velho, novo in (TROCAS.get(src, []) if corrige else []):
        ws = troca(ws, velho, novo)
    return ws


def acha(ws, frase, depois=-1.0):
    f = [norm(x) for x in frase.split()]
    for i in range(len(ws) - len(f) + 1):
        if ws[i]["s"] >= depois and [norm(w["w"]) for w in ws[i:i + len(f)]] == f:
            return i
    sys.exit(f"não achei '{frase}'")


def troca(ws, velho, novo):
    """Troca a sequência `velho` por `novo`, repartindo o tempo da original entre as palavras novas."""
    i, n = acha(ws, velho), len(velho.split())
    s, e, nv = ws[i]["s"], ws[i + n - 1]["e"], novo.split()
    p = (e - s) / max(len(nv), 1)
    return ws[:i] + [{"w": t, "s": round(s + k * p, 3), "e": round(s + (k + 1) * p, 3)} for k, t in enumerate(nv)] + ws[i + n:]


def grito(txt, a, b, y=1120, size=110):
    return {"lines": txt if isinstance(txt, list) else [txt], "start": round(a, 3), "end": round(b, 3), "y": y,
            "size": size, "color": "black", "font": BLACK, "boxcolor": "0xFCBE26", "pad": 22, "border": 0, "shadow": 0,
            "fade": 0.04, "anim": "pop", "shake": True}


def fala(src, de=None, ate=None, a=None, b=None, protege=()):
    """Bloco de fala: do início de `de` ao fim de `ate` (ou a/b em segundos), cortando silêncios longos fora de `protege`."""
    ws = palavras(src)
    i = acha(ws, de) if de else next(k for k, w in enumerate(ws) if w["s"] >= a)
    j = (acha(ws, ate, ws[i]["s"]) + len(ate.split()) - 1) if ate else max(k for k, w in enumerate(ws) if w["s"] < b)
    a = max(0.0, ws[i]["s"] - ANTES) if a is None else a
    fim = ws[j]["e"] + DEPOIS if b is None else b
    if j + 1 < len(ws):
        fim = min(fim, ws[j + 1]["s"] - 0.05)
    fim = min(fim, DURACAO[src] - 0.1)
    # cortes e trocas de enquadramento saem das palavras BRUTAS: legenda omitida não pode virar corte de áudio
    br = [w for w in palavras(src, corrige=False) if a <= w["s"] < fim]
    cortes = [(w0["e"] + DEPOIS, w1["s"] - ANTES) for w0, w1 in zip(br, br[1:])
              if w1["s"] - w0["e"] > GAP and not any(p0 <= w0["e"] and w1["s"] <= p1 for p0, p1 in protege)]
    trechos, ini = [], a
    for c0, c1 in cortes:
        trechos.append((ini, c0))
        ini = c1
    trechos.append((ini, fim))
    return {"src": src, "trechos": divide(trechos, br), "ws": ws[i:j + 1], "coros": []}


def divide(trechos, ws, alvo=7.0):
    """Tomada longa sem corte: troca o enquadramento (sem tirar tempo) no respiro depois de pontuação, a cada ~7 s.
    O corte cai no meio da pausa entre palavras, onde o fade de 20 ms do áudio de cada plano não se ouve."""
    out = []
    for x0, x1 in trechos:
        ini = x0
        for w0, w1 in zip(ws, ws[1:]):
            if (ini < w0["e"] < x1 and w1["s"] - w0["e"] >= 0.12 and re.search(r"[.,!?]$", w0["w"])
                    and w0["e"] - ini >= alvo and x1 - w1["s"] >= 3.0):
                m = round((w0["e"] + w1["s"]) / 2, 3)
                out.append((ini, m))
                ini = m
        out.append((ini, x1))
    return out


def coro(src, a, b, gritos):
    """Bloco de coro do público: plano inteiro, sem legenda de fala; `gritos` = [(texto, t0, t1)] no tempo da fonte."""
    return {"src": src, "trechos": [(a, b)], "ws": [], "coros": gritos}


PARTES = [  # partes de até 2:20: cabem no limite do X sem Premium, além de Reels, Shorts e TikTok
    ("QUE CRIME NÓS ESTAMOS COMETENDO?", ["QUE CRIME NÓS", "ESTAMOS COMETENDO?"], [
        fala("IMG_8452", de="Há crime em dizer que nós vamos investir", b=28.4),
        fala("IMG_8453", de="Com o senhor Lula", ate="a porra da verdade."),
        fala("IMG_8454", de="Eu vou falar, sabe qual é o futuro", ate="Mas não é só esse crime organizado."),
    ]),
    ("A VIDA DE VOCÊS ESTÁ SE TORNANDO IMPOSSÍVEL", ["A VIDA DE VOCÊS ESTÁ", "SE TORNANDO IMPOSSÍVEL"], [
        fala("IMG_8454", de="Pessoal, a vida de vocês", ate="desabamento, deslizamento."),
        fala("IMG_8455", de="Minas Gerais, o segundo estado", ate="o Brasil está virando?"),
    ]),
    ("É 14 OU NADA", ["É 14 OU NADA"], [
        fala("IMG_8455", de="A classe política de Minas sabe", b=93.6),
        fala("IMG_8457", a=0.5, b=6.4),
        coro("IMG_8457", 6.4, 13.0, [("É 14 OU NADA!", 6.6, 13.0)]),
        fala("IMG_8457", a=32.9, b=61.9),
        fala("IMG_8458", a=0.0, ate="aceitou essa proposta indecente."),
        coro("IMG_8458", 10.4, 14.3, [("MISSÃO!", 10.5, 14.3)]),
    ]),
    ("NÓS ESTAMOS DE PÉ", ["NÓS ESTAMOS DE PÉ"], [
        fala("IMG_8458", de="E por que eu digo isso? Eu não admito", ate="nas urnas."),
        fala("IMG_8458", de="Exatamente, quem vota 14,", ate="é 14 ou nada."),
        coro("IMG_8458", 74.5, 80.5, [("14 OU NADA!", 74.6, 80.5)]),
        fala("IMG_8458", de="E porque eu digo isso, meus amigos, foi muito difícil", ate="em todos os momentos"),
    ]),
    ("NÓS JÁ ESTÁVAMOS CONVIDADOS", ["NÓS JÁ ESTÁVAMOS", "CONVIDADOS"], [
        fala("IMG_8458", de="Retiraram agora o nosso direito", ate="a pedido do Lula e do Flávio."),
        coro("IMG_8460", 0.0, 2.0, [("GLOBO, CHAMA O RENAN!", 0.0, 2.0)]),
        fala("IMG_8460", de="Nós temos o direito", ate="destruir o crime organizado."),
        coro("IMG_8460", 56.6, 61.0, [("MISSÃO!", 56.8, 61.0)]),
        fala("IMG_8463", de="O editorial delas", ate="uma grande potência."),
        fala("IMG_8464", de="Não conseguiram ver o óbvio", ate="Ninguém derrubou uma proposta nossa."),
    ]),
    ("A ELITE TRAIU VOCÊS", ["A ELITE", "TRAIU VOCÊS"], [
        fala("IMG_8464", de="Por que diabos as pessoas em posição", ate="vai ser muito duro.", protege=[(87.5, 96.5)]),
        fala("IMG_8465", de="Eu vou pra cima dessa elite.", ate="nós vamos pra cima deles."),
    ]),
    ("AS TERRAS RARAS SÃO DE MINAS", ["AS TERRAS RARAS", "SÃO DE MINAS"], [
        fala("IMG_8465", de="Não queremos", ate="porque o Brasil é nosso."),
        coro("IMG_8465", 31.4, 36.9, [("O BRASIL É NOSSO!", 31.5, 36.9)]),
        fala("IMG_8465", de="Amigos, vocês sabem que Minas Gerais", ate="feito em Minas Gerais."),
    ]),
    ("O BRASIL É DOS BRASILEIROS", ["O BRASIL É", "DOS BRASILEIROS"], [
        fala("IMG_8465", de="Agora, hoje, o governo do PT", ate="para vagabundo nenhum."),
        fala("IMG_8468", de="Minas é a terra das terras raras.", b=39.45),
    ]),
]


def monta(nome, partes, rotulo, fim_card, continua=None):
    shots, texts, overlays, t = [], [], [], 0.0
    for p, (titulo, linhas, blocos) in enumerate(partes):
        texts.append(grito(linhas, t + 0.3, t + 3.8, y=330, size=92))  # título do capítulo
        for bl in blocos:
            z, foco = QUADRO[bl["src"]]
            mapa = []
            for k, (x0, x1) in enumerate(bl["trechos"]):
                d = round(x1 - x0, 3)
                zz = round(z * (PUNCH if k % 2 else 1), 3)
                shots.append({"src": bl["src"], "in": round(x0, 3), "dur": d, "zoom": [zz, zz], "focus": foco})
                mapa.append((x0, x1, t))
                t = round(t + d, 3)

            def to_reel(x, mapa=mapa):
                for x0, x1, off in mapa:
                    if x < x1:
                        return round(off + max(x, x0) - x0, 3)
                x0, x1, off = mapa[-1]
                return round(off + x1 - x0, 3)

            if bl["ws"]:
                for tx in b2.karaoke(bl["ws"], to_reel, stop=t):
                    tx["color"] = AMARELO
                    texts.append(tx)
            for g, g0, g1 in bl["coros"]:
                texts.append(grito(g, to_reel(g0), min(to_reel(g1), t)))
            if bl["src"] == "IMG_8463":  # o trecho começa no meio da frase sobre a revista: contexto em uma linha
                texts.append({"lines": ["Sobre o editorial da The Economist (24/09)"], "start": to_reel(bl["trechos"][0][0]),
                              "end": round(to_reel(bl["trechos"][0][0]) + 4.5, 3), "y": 1500, "size": 44,
                              "color": "white", "font": BLACK, "box": 0.45, "pad": 14, "shadow": 0})
    total = t
    texts.insert(0, {"lines": rotulo, "start": 0, "end": total, "y": 92, "size": 34, "color": "white", "font": BLACK,
                     "box": 0.4, "pad": 10, "shadow": 0, "fade": 0.3})
    if continua:
        texts.append(grito(continua, total - 2.6, total, y=1480, size=84))
    if fim_card:
        overlays.append({"png": "titles/marca_fim_sem_ia.png", "start": round(total - 3.0, 3), "end": total, "y": 0,
                         "fade_in": 0.3, "fade_out": 0.01})
    return {"name": nome, "grade": "noite", "shots": shots, "audio": "sync", "voz": True, "texts": texts,
            "overlays": overlays, "cover": 2.0, "crf": 19, "preset": "medium"}


E = []
N = len(PARTES)
for n, parte in enumerate(PARTES, 1):
    E.append(monta(f"30_discurso_parte{n}", [parte],
                   [f"DISCURSO COMPLETO · PARTE {n}/{N}", "RENAN SANTOS · UBERLÂNDIA, 25/09"],
                   fim_card=(n == N), continua=(f"CONTINUA NA PARTE {n + 1}" if n < N else None)))
E.append(monta("30_discurso_integra", PARTES, ["DISCURSO COMPLETO", "RENAN SANTOS · UBERLÂNDIA, 25/09"], fim_card=True))

os.makedirs(f"{HERE}/edl_discurso", exist_ok=True)
for e in E:
    dur = sum(s["dur"] for s in e["shots"])
    json.dump(e, open(f"{HERE}/edl_discurso/{e['name']}.json", "w"), ensure_ascii=False, indent=1)
    print(f"{e['name']}: {dur:.1f}s  {len(e['shots'])} planos  {len(e['texts'])} textos" + ("  <-- PASSA DE 2:20" if dur > 139.5 and "parte" in e["name"] else ""))
if "--texto" in sys.argv:  # revisão: o texto corrido de cada bloco
    for titulo, _, blocos in PARTES:
        print(f"\n## {titulo}")
        for bl in blocos:
            print(f"[{bl['src']} {bl['trechos'][0][0]:.1f}-{bl['trechos'][-1][1]:.1f}]", " ".join(w["w"] for w in bl["ws"]) or
                  " / ".join(g for g, _, _ in bl["coros"]))
