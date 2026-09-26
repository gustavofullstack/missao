#!/usr/bin/env python3
"""build_v2.py — leva 2, guiada pelo áudio: cortes de fala com legenda amarela palavra por palavra
(estilo dos perfis grandes do Missão) e coros da praça. Só entra na legenda texto confirmado por votação
(vote.py/vote2.py); trecho sem consenso fica com áudio e sem legenda, ou fora do corte."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = json.load(open(f"{HERE}/transcripts_v3.json"))
MONT = "/usr/share/fonts/opentype/montserrat/Montserrat-ExtraBold.otf"
AMARELO = "#FFE11A"

# correções decididas pela votação (palavra do Whisper -> palavra da legenda); None apaga
FIX = {  # palavra: (nova, início, fim) — a correção só vale dentro da janela de tempo
    "IMG_8464": {"nele": ("dele", 0, 99), "leiam.": ("leem,", 0, 99), "Nós": ("nós", 18, 24),
                 "esse,": ("esse", 13.5, 16)},  # revisão do Codex: sem vírgula antes de "em que"
    "IMG_8465": {"Estado": ("estado", 51, 60), "terras": ("terra", 51, 60), "raras.": ("rara.", 51, 60),
                 "sabiam": ("sabem", 51, 61), "BID,": ("BYD,", 96, 106)},
    "IMG_8468": {"tem": ("têm", 15, 25), "mineiros": ("mineiros…", 26, 28)},
}
JUNTAR = {(a, b) for a, bs in {"Estados": ["Unidos,", "Unidos"], "terra": ["rara.", "rara"], "terras": ["raras,"],
                                 "Minas": ["Gerais", "Gerais.", "Gerais,"], "União": ["Europeia,"],
                                 "meio": ["ambiente,"], "carro": ["elétrico"]}.items() for b in bs}


def words(src, a, b):
    """Palavras do large-v3 dentro de [a, b], com as correções; 'Nós estaremos em' vira 'Nós teremos'."""
    out = []
    for s in V3:
        if s["src"] != src:
            continue
        for w in s["words"]:
            if a <= w["s"] < b:
                out.append(dict(w))
    fix = FIX.get(src, {})
    res, skip = [], False
    for i, w in enumerate(out):
        if skip:
            skip = False
            continue
        t = w["w"]
        if src == "IMG_8465" and t == "estaremos":
            if res and res[-1]["w"] == "Nós":
                res.pop()
            t = "Nós teremos"
            skip = i + 1 < len(out) and out[i + 1]["w"] == "em"
        elif t in fix and fix[t][1] <= w["s"] < fix[t][2]:
            t = fix[t][0]
        if res and (res[-1]["w"], t) in JUNTAR:
            res[-1]["w"] += " " + t
            res[-1]["e"] = w["e"]
            continue
        if t:
            w["w"] = t
            res.append(w)
    return res


from PIL import ImageFont

_FONTE = ImageFont.truetype(f"{HERE}/Montserrat-ExtraBold.otf", 100)


def cabe(txt, size, maxw=900):
    """Maior tamanho <= size em que o texto cabe na zona segura (medido com a própria fonte)."""
    return min(size, int(size * maxw / (_FONTE.getlength(txt) * size / 100)))


def chunks(ws, max_words=3, max_chars=22):
    """Blocos de até 3 palavras / 18 caracteres, quebrando depois de pontuação."""
    cur, out = [], []
    for w in ws:
        if cur and (len(cur) >= max_words or len(" ".join(x["w"] for x in cur + [w])) > max_chars):
            out.append(cur)
            cur = []
        cur.append(w)
        if re.search(r"[.,!?…]$", w["w"]):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    # bloco não termina em palavra de ligação: ela desce para o bloco seguinte (se couber)
    LIG = {"a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "na", "no", "em", "com", "pra", "para",
           "que", "um", "uma", "por", "ou", "ao", "aos", "à", "às", "num", "numa", "pelo", "pela"}
    for i in range(len(out) - 1):
        while (len(out[i]) > 1 and out[i][-1]["w"].lower() in LIG
               and len(" ".join(x["w"] for x in [out[i][-1]] + out[i + 1])) <= max_chars):
            out[i + 1].insert(0, out[i].pop())
    return out


def karaoke(ws, to_reel, y=1180, size=76, caps=False, gap=0.35, stop=None):
    """Legenda por blocos no relógio do reel; cada bloco fica até o próximo começar (ou 0,35 s após o fim)."""
    cs = chunks(ws)
    texts = []
    for i, c in enumerate(cs):
        a = to_reel(c[0]["s"])
        b = to_reel(cs[i + 1][0]["s"]) if i + 1 < len(cs) else to_reel(c[-1]["e"]) + gap
        b = min(b, to_reel(c[-1]["e"]) + 0.6)
        if stop is not None:
            b = min(b, stop)
        txt = " ".join(x["w"] for x in c)
        txt = txt.upper() if caps else txt
        texts.append({"lines": [txt], "start": round(a, 3), "end": round(b, 3),
                      "y": y, "size": cabe(txt, size), "color": AMARELO, "font": MONT, "border": 5,
                      "bordercolor": "black", "fade": 0})
    return texts


def coro(txt, a, b, y=1100, size=96):
    return {"lines": [txt], "start": round(a, 3), "end": round(b, 3), "y": y, "size": cabe(txt, size), "color": AMARELO,
            "font": MONT, "border": 6, "bordercolor": "black", "fade": 0}


def titulo(nome):
    return [{"png": f"titles/{nome}.png", "start": 0, "y": 230}]


E, TITULOS = [], {}

# 08 — "É 14 ou nada": a fala e o coro que responde (8457), com recorte do trecho morto entre os dois
p1a, p1d, p2a = 0.5, 8.1, 13.8  # parte 1: 0,5–8,6; parte 2 a partir de 13,8 no reel 8,1
def r08(t):
    return t - p1a if t < 10 else p1d + (t - p2a)
w08 = words("IMG_8457", 0.5, 8.6) + words("IMG_8457", 13.8, 25.0)
fala = [w for w in w08 if w["s"] < 4.3]
tx08 = karaoke(fala, r08)
# o orador fala duas vezes (legenda por repetição); depois a praça canta sem parar e o Whisper espreme os
# tempos das palavras: uma legenda fixa no coro inteiro em vez de piscar a cada repetição
q = [w for w in w08 if w["w"].startswith("14") and w["s"] < 10]
for i, w in enumerate(q):
    a = r08(w["s"]) - 0.35
    b = min(a + 1.6, r08(q[i + 1]["s"]) - 0.4) if i + 1 < len(q) else a + 1.6
    tx08.append(coro("É 14 OU NADA!", a, b))
tx08.append(coro("14 OU NADA!", r08(13.95), 19.3))
TITULOS["08"] = ("RENAN EM UBERLÂNDIA:|“É 14 OU NADA!”", "PRAÇA RUI BARBOSA · 25/09")
E.append({"name": "08_e_14_ou_nada", "cover": 5.0, "overlays": titulo("08"),
          "shots": [{"src": "IMG_8457", "in": 0.5, "dur": 8.1, "zoom": [1.35, 1.35], "focus": [0.5, 0.5]},
                    {"src": "IMG_8457", "in": 13.8, "dur": 3.7, "zoom": [1.3, 1.3], "focus": [0.5, 0.55]},
                    {"src": "IMG_8470", "in": 12.5, "dur": 2.5, "speed": 0.5, "flash": True},
                    {"src": "IMG_8444", "in": 26.5, "dur": 2.5, "speed": 0.5},
                    {"src": "IMG_8457", "in": 22.5, "dur": 2.5}],
          "audio": [{"src": "IMG_8457", "in": 0.5, "dur": 8.5, "voz": True}, {"src": "IMG_8457", "in": 13.8}],
          "texts": tx08})

# 09 — "Ei, Globo, chama o Renan!": o coro do ato (8448 + 8460)
def r09(src, t):
    return (t - 26.8) if src == "IMG_8448" else 2.2 + (t - 0.0)
tx09 = []
for src, a, b in [("IMG_8448", 26.8, 29.0), ("IMG_8460", 0.0, 4.0)]:
    ws = words(src, a, b)
    for i, w in enumerate(ws):
        if w["w"].lower().strip(",!") == "globo":
            cham = next(x for x in ws[i + 1:] if x["w"].lower().startswith("chama"))
            fim = next(x for x in ws[i + 1:] if x["w"].lower().startswith("renan"))
            tx09.append(coro("EI, GLOBO,", r09(src, max(a, w["s"] - 0.3)), r09(src, cham["s"]), y=1060))
            tx09.append(coro("CHAMA O RENAN!", r09(src, cham["s"]), r09(src, min(b, fim["e"] + 0.3)), y=1060))
TITULOS["09"] = ("A PRAÇA PEDIU:|“EI, GLOBO,|CHAMA O RENAN!”", "UBERLÂNDIA · 25/09")
E.append({"name": "09_ei_globo_chama_o_renan", "cover": 3.0, "overlays": titulo("09"), "audio": "sync",
          "shots": [{"src": "IMG_8448", "in": 26.8, "dur": 2.2},
                    {"src": "IMG_8460", "in": 0.0, "dur": 7.0}],
          "texts": tx09})

# 10 — "Quem tá aqui com o livro amarelo?" (8464); frase "rodamos/roubamos" (empate 7x5) fica fora
A1, A2, J = 10.4, 41.4, 25.55  # parte 1 10,4–36,0; parte 2 a partir de 41,4 no reel 25,6
def r10(t):
    return t - A1 if t < 38 else J + (t - A2)
w10 = words("IMG_8464", 10.4, 35.91) + words("IMG_8464", 41.4, 46.2)
spk = {"zoom": [1.4, 1.4], "focus": [0.5, 0.45]}
TITULOS["10"] = ("RENAN EM UBERLÂNDIA:|“QUEM TÁ AQUI COM|O LIVRO AMARELO?”", "PRAÇA RUI BARBOSA · 25/09")
E.append({"name": "10_quem_ta_aqui_com_o_livro_amarelo", "cover": 1.0, "overlays": titulo("10"),
          "shots": [dict(src="IMG_8464", **{"in": 10.4, "dur": 1.8}, **spk),
                    {"src": "IMG_8468", "in": 14.0, "dur": 1.8},
                    dict(src="IMG_8464", **{"in": 14.0, "dur": 4.4}, **spk),
                    {"src": "IMG_8446", "in": 28.0, "dur": 2.5},
                    {"src": "IMG_8445", "in": 4.0, "dur": 2.5, "speed": 0.5},
                    dict(src="IMG_8464", **{"in": 23.4, "dur": 5.6}, **spk),
                    dict(src="IMG_8464", **{"in": 29.0, "dur": 2.0}, **spk),
                    {"src": "IMG_8470", "in": 16.0, "dur": 1.5, "speed": 0.5},
                    dict(src="IMG_8464", **{"in": 32.5, "dur": 1.7}, **spk),
                    {"src": "IMG_8453", "in": 35.0, "dur": 1.75, "speed": 0.3},
                    dict(src="IMG_8464", **{"in": 41.4, "dur": 4.4}, **spk)], "xfade": 0.12,
          "audio": [{"src": "IMG_8464", "in": A1, "dur": J + 0.12, "voz": True},
                    {"src": "IMG_8464", "in": A2, "voz": True}],
          "texts": karaoke(w10, r10)})

# 11 — terras raras (8465): abertura + plano; "vão servir o/no Brasil" (dividido) fica fora
P = [(51.5, 60.2), (71.3, 93.95), (96.8, 105.2)]
starts = [0.0, 8.7, 8.7 + 22.65]
def r11(t):
    for (a, b), s0 in zip(P, starts):
        if a - 0.5 <= t <= b + 0.5:
            return s0 + (t - a)
    raise ValueError(t)
w11 = sum((words("IMG_8465", a, b) for a, b in P), [])
w11 = [w for w in w11 if not (93.9 < w["s"] < 96.8)]
spk = {"zoom": [1.4, 1.4], "focus": [0.48, 0.47]}
TITULOS["11"] = ("RENAN EM UBERLÂNDIA:|O PLANO DAS|TERRAS RARAS", "PRAÇA RUI BARBOSA · 25/09")
total11 = 8.7 + 22.65 + 8.4
E.append({"name": "11_o_plano_das_terras_raras", "cover": 2.0, "overlays": titulo("11"),
          "shots": [dict(src="IMG_8465", **{"in": 51.5, "dur": 8.7}, **spk),
                    dict(src="IMG_8465", **{"in": 71.3, "dur": 4.0}, **spk),
                    {"src": "IMG_8449", "in": 25.0, "dur": 3.0},
                    dict(src="IMG_8465", **{"in": 78.3, "dur": 5.2}, **spk),
                    {"src": "IMG_8444", "in": 26.4, "dur": 2.5, "speed": 0.5},
                    dict(src="IMG_8465", **{"in": 86.0, "dur": 4.6}, **spk),
                    {"src": "IMG_8453", "in": 34.0, "dur": 3.35, "speed": 0.3},
                    dict(src="IMG_8465", **{"in": 96.8, "dur": 8.4}, **spk)], "xfade": 0.12,
          "audio": [{"src": "IMG_8465", "in": 51.5, "dur": 8.7 + 0.12, "voz": True},
                    {"src": "IMG_8465", "in": 71.3, "dur": 22.65 + 0.12, "voz": True},
                    {"src": "IMG_8465", "in": 96.8, "voz": True}],
          "texts": karaoke(w11, r11)})

# 12 — encerramento (8468): trecho incerto depois de "mineiros" fica sem legenda; "votar em ___" fora
def r12(t):
    return t - 13.2 if t < 31 else 16.8 + (t - 32.88)
w12 = [w for w in words("IMG_8468", 13.2, 30.0) + words("IMG_8468", 32.88, 39.45)
       if not (27.25 < w["s"] < 28.6)]
spk = {"zoom": [1.45, 1.45], "focus": [0.55, 0.5]}
TITULOS["12"] = ("O FINAL DO DISCURSO|DE RENAN EM UBERLÂNDIA", "PRAÇA RUI BARBOSA · 25/09")
E.append({"name": "12_o_final_do_discurso", "cover": 3.0, "overlays": titulo("12"),
          "shots": [dict(src="IMG_8468", **{"in": 13.2, "dur": 5.0}, **spk),
                    {"src": "IMG_8443", "in": 27.0, "dur": 2.5, "speed": 0.25, "grade": "fogo_quente"},
                    dict(src="IMG_8468", **{"in": 20.7, "dur": 5.3}, **spk),
                    {"src": "IMG_8470", "in": 12.5, "dur": 2.0, "speed": 0.5},
                    dict(src="IMG_8468", **{"in": 28.0, "dur": 2.0}, **spk),
                    dict(src="IMG_8468", **{"in": 32.88, "dur": 3.7}, **spk),
                    {"src": "IMG_8453", "in": 37.8, "dur": 2.85, "speed": 0.3}], "xfade": 0.12,
          "audio": [{"src": "IMG_8468", "in": 13.2, "dur": 16.8 + 0.12, "voz": True},
                    {"src": "IMG_8468", "in": 32.88, "voz": True}],
          "texts": karaoke(w12, r12)})

# 13 — o que a praça gritou: coros em sequência, cada um com o próprio áudio e imagem
tx13, t0 = [], 0.0
COROS = [("IMG_8453", 17.5, 21.6, "MISSÃO!", None), ("IMG_8445", 29.0, 33.7, "EU VOTO 14!", None),
         ("IMG_8465", 176.2, 180.2, "RENAN!", None), ("IMG_8465", 49.8, 51.8, "O BRASIL É NOSSO!", None),
         ("IMG_8457", 19.0, 23.0, "14 OU NADA!", None)]
shots13 = []
for src, a, b, txt, _ in COROS:
    shots13.append({"src": src, "in": a, "dur": round(b - a, 2)})
    tx13.append(coro(txt, t0 + 0.15, t0 + (b - a) - 0.1, y=1080,
                     size=96 if len(txt) < 10 else 84 if len(txt) < 14 else 70))
    t0 += b - a
TITULOS["13"] = ("O QUE A PRAÇA|GRITOU EM UBERLÂNDIA", "25/09 · PRAÇA RUI BARBOSA")
E.append({"name": "13_o_que_a_praca_gritou", "cover": 1.0, "overlays": titulo("13"), "audio": "sync",
          "shots": shots13, "texts": tx13})

os.makedirs(f"{HERE}/edl2", exist_ok=True)
for e in E:
    T = sorted(e["texts"], key=lambda t: t["start"])
    for a, b in zip(T, T[1:]):  # legenda nunca invade a seguinte
        a["end"] = min(a["end"], b["start"])
    e["texts"] = [t for t in T if t["end"] - t["start"] >= 0.1]
    e["crf"] = 24 if e["name"].startswith("11") else 20  # o 11 tem 40 s: 24 para caber em 30 MiB  # zoom 4K + legenda sobem o bitrate: 20 mantém abaixo do limite de 30 MiB do app
    json.dump(e, open(f"{HERE}/edl2/{e['name']}.json", "w"), ensure_ascii=False, indent=1)
    tot = sum(s["dur"] for s in e["shots"])
    print(f"{e['name']}: {tot:.1f}s, {len(e['shots'])} planos, {len(e['texts'])} legendas")
with open(f"{HERE}/edl2/titulos.sh", "w") as f:
    for k, (t, sub) in TITULOS.items():
        f.write(f'venv/bin/python titulo.py titles/{k}.png "{t}" "{sub}"\n')
