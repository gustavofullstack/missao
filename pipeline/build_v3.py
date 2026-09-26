#!/usr/bin/env python3
"""build_v3.py — leva 3: identidade do Missão (amarelo #FCBE26, Barlow Condensed, bandeira, onça), trilha
do Flow Music por baixo da fala e cortes novos. Legenda só com texto que passou na votação (vote3.log)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v2 as b2  # chunks/karaoke/coro/cabe e as palavras do large-v3 (V3); regrava edl2 igual

V4 = json.load(open(f"{HERE}/transcripts_v4.json"))
AMARELO = "#FCBE26"
BLACK = "/usr/share/fonts/truetype/marca/BarlowCondensed-Black.ttf"


def palavras(fonte, src, a, b, fix=None):
    """Palavras com tempo dentro de [a, b); fix troca (ou apaga, com "") palavras dentro de uma janela."""
    out = []
    for s in fonte:
        if s["src"] != src:
            continue
        for w in s["words"]:
            if a <= w["s"] < b:
                w = dict(w)
                for de, (para, f0, f1) in (fix or {}).items():
                    if w["w"] == de and f0 <= w["s"] < f1:
                        w["w"] = para
                if w["w"]:
                    out.append(w)
    return out


def legenda(ws, to_reel, stop=None):
    tx = b2.karaoke(ws, to_reel, stop=stop)
    for t in tx:
        t["color"] = AMARELO
    return tx


def grito(txt, a, b, y=1120, size=110):
    """Coro/golpe final: caixa amarela, letra preta Barlow Condensed, pulo + tremida na entrada."""
    return {"lines": [txt], "start": round(a, 3), "end": round(b, 3), "y": y, "size": size, "color": "black",
            "font": BLACK, "boxcolor": "0xFCBE26", "pad": 22, "border": 0, "shadow": 0, "fade": 0.04,
            "anim": "pop", "shake": True}


def topo(n):
    return [{"png": f"titles/{n}.png", "start": 0, "y": 200}]


E = []

# 14 — "Quantos deles apoiaram? Nenhum!" (8464 65,3–93,3): empresariado elogiou, ninguém apoiou
A0 = 65.3
r14 = lambda t: t - A0
spk = {"zoom": [1.4, 1.4], "focus": [0.5, 0.45]}
close = {"zoom": [1.75, 1.75], "focus": [0.5, 0.42]}  # punch-in nas frases de golpe
w14 = palavras(V4, "IMG_8464", 65.3, 92.1)
tx14 = legenda(w14, r14, stop=r14(89.8))
tx14.append(grito("NENHUM!", r14(92.1), r14(93.3) + 0.0))
E.append({"name": "14_quantos_deles_apoiaram", "cover": 26.9, "overlays": topo("14"), "film": True,
          "shots": [dict(src="IMG_8464", **{"in": 65.3, "dur": 6.3}, **spk),
                    {"src": "IMG_8449", "in": 25.0, "dur": 1.5, "grade": "noite_clara"},
                    dict(src="IMG_8464", **{"in": 73.1, "dur": 7.2}, **spk),
                    {"src": "IMG_8446", "in": 28.0, "dur": 0.8},
                    dict(src="IMG_8464", **{"in": 81.1, "dur": 7.1}, **spk),
                    dict(src="IMG_8464", **{"in": 88.2, "dur": 1.6}, **close),
                    {"src": "IMG_8453", "in": 34.0, "dur": 2.3, "speed": 0.3},
                    dict(src="IMG_8464", **{"in": 92.1, "dur": 1.2, "flash": True}, **close)],
          "audio": [{"src": "IMG_8464", "in": A0, "voz": True}],
          "musica": {"src": "MUS_protesto_boom_bap_92", "in": 0.0, "gain": -19},
          "texts": tx14})

# 15 — o editorial da The Economist nas palavras dele + card com o que a revista escreveu (fontes)
S1, S2 = (3.7, 12.3), (16.7, 30.6)
L1 = S1[1] - S1[0]
r15 = lambda t: t - S1[0] if t < 14 else L1 + (t - S2[0])
fix15 = {"delas": ("", 4, 5), "deixa": ("deixou", 4.9, 5.2), "ó.": ("", 10, 10.6), "Virando": ("virando", 10.5, 11),
         "vocês": ("vocês.", 12.0, 12.1), "eles": ("Eles", 16.8, 16.9)}
w15a = palavras(b2.V3, "IMG_8463", 3.8, 12.3, fix15)   # blocos não atravessam o corte entre os dois trechos
w15b = palavras(b2.V3, "IMG_8463", 16.8, 24.4, fix15)
fim15 = r15(24.4)
spk15 = {"zoom": [1.35, 1.35], "focus": [0.48, 0.42]}
E.append({"name": "15_o_que_a_the_economist_escreveu", "cover": 3.0, "film": True,
          "overlays": topo("15") + [{"png": "titles/card_economist.png", "start": round(fim15 + 0.2, 2),
                                     "y": 640, "fade_in": 0.35}],
          "shots": [dict(src="IMG_8463", **{"in": 3.7, "dur": 4.3}, **spk15),
                    {"src": "IMG_8449", "in": 40.0, "dur": 1.2, "grade": "noite_clara"},
                    dict(src="IMG_8463", **{"in": 9.2, "dur": 3.1}, **spk15),
                    dict(src="IMG_8463", **{"in": 16.7, "dur": 7.7}, **spk15),
                    {"src": "IMG_8453", "in": 37.8, "dur": 6.2, "speed": 0.3, "zoom": [1.0, 1.06]}],
          "audio": [{"src": "IMG_8463", "in": S1[0], "dur": L1 + 0.12, "voz": True},
                    {"src": "IMG_8463", "in": S2[0], "voz": True}], "xfade": 0.12,
          "musica": {"src": "MUS_futuro_soberano_mpb_rock", "in": 6.0, "gain": -21},
          "texts": legenda(w15a, r15) + legenda(w15b, r15, stop=fim15 + 0.15)})

# ---- música: planos escolhidos na batida (planos_clipe.json, subagente) + vinhetas de IA do Google Flow ----
PL = json.load(open(f"{HERE}/planos_clipe.json"))
LETRA = json.load(open(f"{HERE}/musica/mercadores_letra.json"))
MW = [w for seg in LETRA for w in seg["words"]]


def canto(palavra, depois, antes=999):
    """Início (s, na música) da primeira ocorrência de `palavra` entre depois e antes."""
    return next(w["s"] for w in MW if w["w"].lower().strip(",.!?") == palavra and depois <= w["s"] < antes)


def limpa(sh):
    return {k: v for k, v in sh.items() if k != "nota"}


def ia(src, inn, dur, speed=1.0):
    return {"src": src, "in": inn, "dur": dur, "speed": speed, "grade": "neutro"}


def selo_img(a, b):
    return {"png": "titles/marca_selo_img_ia.png", "start": round(a, 2), "end": round(b, 2), "y": 1650,
            "fade_in": 0.1, "fade_out": 0.1}


def gritos(off, pares):
    """Coros na tela no tempo da música: [(texto, início_música, fim_música)] -> legendas grito()."""
    return [grito(t, a + off, b + off, size=118 if len(t) <= 8 else 96) for t, a, b in pares]


# 17 — "A rua tá gritando": pausa dramática do "Nenhum!" preenchida pelo olho da onça (IA), depois o coro
M0 = 113.25             # entrada da música (início de "A rua tá gritando" menos a antecipação)
F17 = 4.8               # fim da fala no reel
off17 = F17 - M0        # tempo da música -> tempo do reel
r17 = [limpa(x) for x in PL["reel"]]
r17[4] = ia("IA_onca_fumaca", 2.2, r17[4]["dur"])           # 5º plano do coro: a onça atravessa a fumaça
r17[8] = ia("IA_bandeira_lua", 1.5, r17[8]["dur"], 0.8)     # bandeira amarela e preta sob a lua
r17[-1]["dur"] = round(r17[-1]["dur"] + 2.0, 3)             # espaço do card final
t_ia = [F17 + sum(x["dur"] for x in r17[:4]), F17 + sum(x["dur"] for x in r17[:8])]
tx17 = legenda(palavras(V4, "IMG_8464", 88.3, 89.6), lambda t: t - 88.1, stop=1.75)
tx17 += [grito("NENHUM!", 92.1 - 88.1, F17 - 0.02)]
tx17 += [grito("A RUA TÁ GRITANDO", 113.38 + off17, 116.28 + off17, size=92)]
tx17 += gritos(off17, [("MISSÃO!", 116.80, 118.30), ("FORA CORRUPÇÃO!", 118.30, 119.92),
                       ("MISSÃO!", 119.92, 121.34), ("FORA LADRÕES!", 121.34, 122.88),
                       ("MISSÃO!", 122.88, 123.64), ("FORA CORRUPÇÃO!", 123.64, 125.28),
                       ("MISSÃO!", 125.28, 126.40), ("A MISSÃO CONTINUA", 134.84, 136.54),
                       ("FORA LADRÕES!", 136.54, 137.64), ("FORA CORRUPÇÃO!", 137.64, 138.9)])
dur17 = F17 + sum(x["dur"] for x in r17)
E.append({"name": "17_a_rua_ta_gritando", "cover": 9.0, "film": True,
          "shots": [dict(src="IMG_8464", **{"in": 88.1, "dur": 1.7}, **spk),
                    ia("IA_olho_onca", 4.2, 2.2),
                    dict(src="IMG_8464", **{"in": 92.0, "dur": 0.9, "flash": True}, **close)] + r17,
          "overlays": [selo_img(1.7, 3.9), selo_img(t_ia[0], t_ia[0] + r17[4]["dur"]),
                       selo_img(t_ia[1], t_ia[1] + r17[8]["dur"]),
                       {"png": "titles/marca_selo_ia.png", "start": F17, "end": F17 + 4.0, "y": 1720},
                       {"png": "titles/marca_bandeira.png", "start": round(116.80 + off17, 2),
                        "end": round(117.36 + off17, 2), "y": 0, "slam": True, "fade_in": 0.02, "fade_out": 0.05},
                       {"png": "titles/marca_fim.png", "start": round(dur17 - 2.0, 2), "y": 0, "fade_in": 0.3}],
          "audio": [{"src": "IMG_8464", "in": 88.1, "dur": F17 + 0.15, "voz": True, "gain": 4},
                    {"src": "MUS_mercadores_da_miseria", "in": M0, "gain": -2}], "xfade": 0.15,
          "texts": tx17})

# 16 — clipe completo "Mercadores da Miséria" com a marca: abertura com a fala de Minas + mapa
A16 = 5.35
m16 = lambda t: t + A16  # música -> reel
c16 = [limpa(x) for x in PL["clipe"]]


def troca(tm, novo):
    """Troca o plano que está tocando no tempo tm (da música) pela vinheta, mantendo a duração."""
    t = 0.0
    for i, sh in enumerate(c16):
        if t <= tm < t + sh["dur"]:
            c16[i] = dict(novo, dur=sh["dur"])
            return m16(t), sh["dur"]
        t += sh["dur"]


ins = [troca(0.2, ia("IA_olho_onca", 5.8, 1)), troca(118.0, ia("IA_onca_fumaca", 1.0, 1)),
       troca(150.0, ia("IA_bandeira_lua", 0.5, 1, 0.8)), troca(95.0, ia("IA_onca_fumaca", 6.0, 1))]
tx16 = legenda(palavras(V4, "IMG_8455", 0.0, 5.3, {"Estado": ("estado", 0, 6)}), lambda t: t, stop=A16)
tx16 += gritos(A16, [("MISSÃO!", 2.22, 2.78), ("FORA LADRÕES!", 3.88, 5.14), ("FORA CORRUPÇÃO!", 6.52, 8.12),
                     ("FORA LADRÕES!", 71.5, 72.5), ("FORA CORRUPÇÃO!", 72.5, 73.6),
                     ("MISSÃO!", 116.80, 118.30), ("FORA CORRUPÇÃO!", 118.30, 119.92),
                     ("MISSÃO!", 119.92, 121.34), ("FORA LADRÕES!", 121.34, 122.88),
                     ("MISSÃO!", 122.88, 123.64), ("FORA CORRUPÇÃO!", 123.64, 125.28),
                     ("MISSÃO!", 125.28, 126.40), ("A MISSÃO CONTINUA", 134.84, 136.54),
                     ("FORA LADRÕES!", 136.54, 137.64), ("FORA CORRUPÇÃO!", 137.64, 138.9)])
dur16 = A16 + sum(x["dur"] for x in c16)
E.append({"name": "16_mercadores_da_miseria_clipe", "cover": 14.5, "film": True,
          "shots": [{"src": "IMG_8455", "in": 0.0, "dur": A16}] + c16,
          "overlays": [{"png": "titles/marca_mapa.png", "start": 0.4, "end": A16, "y": 330},
                       {"png": "titles/16.png", "start": m16(8.2), "end": m16(16.0), "y": 200},
                       {"png": "titles/marca_selo_ia.png", "start": A16, "end": A16 + 6.0, "y": 1720},
                       {"png": "titles/marca_bandeira.png", "start": round(m16(1.64), 2), "end": round(m16(2.20), 2),
                        "y": 0, "slam": True, "fade_in": 0.02, "fade_out": 0.05},
                       {"png": "titles/marca_fim.png", "start": round(dur16 - 5.0, 2), "y": 0, "fade_in": 0.5}]
                      + [selo_img(a, a + d) for a, d in ins],
          "audio": [{"src": "IMG_8455", "in": 0.0, "dur": A16 + 0.1, "voz": True, "gain": 4},
                    {"src": "MUS_mercadores_da_miseria", "in": 0.0, "gain": -2}], "xfade": 0.1,
          "texts": tx16})

# 18 — o plano das terras raras com ilustração de IA nas palavras-chave (mesma fala e legenda do 11)
e11 = json.load(open(f"{HERE}/edl2/11_o_plano_das_terras_raras.json"))
tx18 = [dict(t, color=AMARELO) for t in e11["texts"]]
spk11 = {"zoom": [1.4, 1.4], "focus": [0.48, 0.47]}
S11 = lambda a, d: dict(src="IMG_8465", **{"in": a, "dur": d}, **spk11)
sh18 = [S11(51.5, 5.2), ia("IA_terras_raras", 0.4, 3.5),                   # "...reserva de terras raras"
        S11(71.3, 4.0), {"src": "IMG_8449", "in": 25.0, "dur": 3.0},       # zonas econômicas; parcerias
        S11(78.3, 3.6), ia("IA_terras_raras", 6.0, 3.0),                   # "processamento de terras raras, os ímãs"
        ia("IA_fabrica", 1.0, 1.1),                                        # "as baterias"
        ia("IA_drones", 1.0, 2.0), S11(88.0, 2.6),                         # "os drones", cadeia produtiva
        {"src": "IMG_8453", "in": 34.0, "dur": 3.35, "speed": 0.3},        # "com o país que for"
        S11(96.8, 1.6), ia("IA_fabrica", 4.0, 1.5), ia("IA_drones", 5.0, 1.3),  # "fábrica de bateria para drone"
        S11(101.2, 4.0), ia("IA_mapa_ouro", 2.0, 2.6)]                     # fecho: Minas em ouro
t = 0.0
selos18 = []
for sh in sh18:
    if sh["src"].startswith("IA_"):
        selos18.append(selo_img(t, t + sh["dur"]))
    t += sh["dur"]
E.append({"name": "18_terras_raras_com_ia", "cover": 7.0, "film": True,
          "shots": sh18, "overlays": topo("18") + selos18
          + [{"png": "titles/marca_mapa.png", "start": round(t - 3.85, 2), "end": round(t - 2.6, 2), "y": 330,
              "fade_in": 0.15}],
          "audio": e11["audio"], "xfade": e11.get("xfade", 0.12),
          "musica": {"src": "MUS_futuro_soberano_mpb_rock", "in": 20.0, "gain": -22},
          "texts": tx18})

os.makedirs(f"{HERE}/edl3", exist_ok=True)
ROTULO = {"14": "marca_ia_musica", "15": "marca_ia_musica", "16": "marca_ia_total", "17": "marca_ia_total",
          "18": "marca_ia_total"}
for e in E:
    e["overlays"].append({"png": f"titles/{ROTULO[e['name'][:2]]}.png", "start": 0, "y": 112, "fade_in": 0.2})
    T = sorted(e["texts"], key=lambda t: t["start"])
    for a, b in zip(T, T[1:]):
        a["end"] = min(a["end"], b["start"])
    e["texts"] = [t for t in T if t["end"] - t["start"] >= 0.1]
    e["crf"] = 20
    tot = sum(s["dur"] for s in e["shots"])
    json.dump(e, open(f"{HERE}/edl3/{e['name']}.json", "w"), ensure_ascii=False, indent=1)
    print(f"{e['name']}: {tot:.2f}s, {len(e['shots'])} planos, {len(e['texts'])} legendas")
    for t in e["texts"]:
        print(f"   {t['start']:6.2f}-{t['end']:6.2f} {t['lines'][0]}")
