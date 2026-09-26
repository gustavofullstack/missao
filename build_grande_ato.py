#!/usr/bin/env python3
"""build_grande_ato.py — Gera o Reel 23: O DISCURSO COMPLETO DE RENAN SANTOS EM UBERLÂNDIA (~2m15s).
Vídeo longo, denso, contextualizado, pegando a narrativa de ponta a ponta:
1. Abertura: O Brasil que importa está aqui (IMG_8455) + praça em chamas (IMG_8453)
2. The Economist: O Brasil vira as costas pro futuro, mas há um caminho (IMG_8463)
3. Livro Amarelo: Propostas reais, campanha do povo (IMG_8464)
4. Coragem: Nenhum grande empresário apoiou, a força vem de quem produz (IMG_8464)
5. Terras Raras & Soberania: A riqueza de Minas servindo o povo brasileiro (IMG_8465)
6. Combate ao Sistema: O Centrão e os ladrões do Estado (IMG_8452)
7. Clímax: É 14 ou nada! A rua acordou! Fora ladrões! (IMG_8457 + IMG_8468 + praça)
"""
import json, os, sys

HERE = '/root/reels'
AMARELO = '#FCBE26'
BLACK_FONT = '/usr/share/fonts/truetype/marca/BarlowCondensed-Black.ttf'
MONTSERRAT = '/usr/share/fonts/opentype/montserrat/Montserrat-ExtraBold.otf'

# Segmentos estruturados com [src, in, dur, zoom, focus, is_voice]
SEGMENTS = [
    # 1. Abertura
    {'src': 'IMG_8455', 'in': 0.0, 'dur': 5.4, 'zoom': [1.2, 1.2], 'focus': [0.5, 0.45], 'voz': True, 'title': 'O BRASIL QUE IMPORTA ESTÁ AQUI'},
    {'src': 'IMG_8453', 'in': 15.5, 'dur': 3.2, 'zoom': [1.0, 1.0], 'focus': [0.5, 0.5], 'voz': False, 'grade': 'fogo'},
    
    # 2. The Economist
    {'src': 'IMG_8463', 'in': 3.8, 'dur': 18.0, 'zoom': [1.35, 1.35], 'focus': [0.48, 0.42], 'voz': True, 'title': 'EDITORIAL THE ECONOMIST'},
    {'src': 'IMG_8449', 'in': 25.0, 'dur': 3.2, 'zoom': [1.0, 1.0], 'focus': [0.5, 0.5], 'voz': False, 'grade': 'noite_clara'},
    
    # 3. O Livro Amarelo
    {'src': 'IMG_8464', 'in': 10.4, 'dur': 22.0, 'zoom': [1.4, 1.4], 'focus': [0.5, 0.45], 'voz': True, 'title': 'O LIVRO AMARELO'},
    {'src': 'IMG_8446', 'in': 28.0, 'dur': 2.8, 'zoom': [1.0, 1.0], 'focus': [0.5, 0.5], 'voz': False, 'grade': 'noite'},
    {'src': 'IMG_8464', 'in': 41.0, 'dur': 5.2, 'zoom': [1.45, 1.45], 'focus': [0.5, 0.45], 'voz': True, 'title': 'PROPOSTAS PARA O BRASIL'},
    
    # 4. Nenhum empresário apoiou
    {'src': 'IMG_8464', 'in': 88.1, 'dur': 5.2, 'zoom': [1.6, 1.6], 'focus': [0.5, 0.42], 'voz': True, 'flash': True, 'title': 'NENHUM EMPRESÁRIO APOIOU'},
    {'src': 'IMG_8445', 'in': 29.0, 'dur': 3.0, 'zoom': [1.0, 1.0], 'focus': [0.5, 0.5], 'voz': False, 'grade': 'noite'},
    
    # 5. Terras Raras
    {'src': 'IMG_8465', 'in': 51.5, 'dur': 26.5, 'zoom': [1.35, 1.35], 'focus': [0.48, 0.47], 'voz': True, 'title': 'TERRAS RARAS & SOBERANIA'},
    {'src': 'IMG_8449', 'in': 75.0, 'dur': 3.2, 'zoom': [1.0, 1.0], 'focus': [0.5, 0.5], 'voz': False, 'grade': 'noite_clara'},
    
    # 6. Enfrentamento ao Sistema
    {'src': 'IMG_8452', 'in': 18.0, 'dur': 10.2, 'zoom': [1.35, 1.35], 'focus': [0.5, 0.45], 'voz': True, 'title': 'COMBATE AO CENTRÃO'},
    
    # 7. Clímax & 14 ou Nada
    {'src': 'IMG_8468', 'in': 29.0, 'dur': 7.5, 'zoom': [1.3, 1.3], 'focus': [0.5, 0.45], 'voz': True, 'title': 'MEU NOME É RENAN SANTOS'},
    {'src': 'IMG_8457', 'in': 0.5, 'dur': 8.0, 'zoom': [1.45, 1.45], 'focus': [0.5, 0.48], 'voz': True, 'flash': True, 'title': 'É 14 OU NADA!'},
    {'src': 'IMG_8453', 'in': 17.5, 'dur': 4.0, 'zoom': [1.0, 1.0], 'focus': [0.5, 0.5], 'voz': False, 'grade': 'fogo'},
    {'src': 'IMG_8457', 'in': 23.0, 'dur': 5.2, 'zoom': [1.0, 1.0], 'focus': [0.5, 0.5], 'voz': False, 'grade': 'noite'}
]

# Monta shots
shots = []
audio = []
XF = 0.1
t_curr = 0.0

for s in SEGMENTS:
    dur = s['dur']
    sh = {'src': s['src'], 'in': s['in'], 'dur': dur}
    if 'zoom' in s: sh['zoom'] = s['zoom']
    if 'focus' in s: sh['focus'] = s['focus']
    if 'grade' in s: sh['grade'] = s['grade']
    if s.get('flash'): sh['flash'] = True
    shots.append(sh)
    
    # audio
    audio.append({
        'src': s['src'],
        'in': s['in'],
        'dur': round(dur + XF, 3),
        'voz': s.get('voz', False)
    })
    t_curr += dur

tot_dur = round(sum(s['dur'] for s in shots), 2)
print(f'Duração Total: {tot_dur}s ({tot_dur/60:.2f} min)')

# Monta textos dinâmicos (marcações capitulares e gritos antissistema)
texts = []

def add_title_card(txt, start, end, y=1180, size=74):
    texts.append({
        'lines': [txt], 'start': round(start, 2), 'end': round(end, 2),
        'y': y, 'size': size, 'color': AMARELO, 'font': MONTSERRAT,
        'border': 5, 'bordercolor': 'black', 'fade': 0.06, 'anim': 'pop'
    })

def add_grito(txt, start, end, y=1120, size=115):
    texts.append({
        'lines': [txt], 'start': round(start, 2), 'end': round(end, 2),
        'y': y, 'size': size, 'color': 'black', 'font': BLACK_FONT,
        'boxcolor': '0xFCBE26', 'pad': 24, 'border': 0, 'shadow': 0,
        'fade': 0.04, 'anim': 'pop', 'shake': True
    })

# Posições de tempo baseadas nos segmentos
t = 0.0
# 1. Abertura
add_title_card('O BRASIL QUE IMPORTA ESTÁ AQUI', t + 0.3, t + 5.2)
t += 5.4
add_grito('MISSÃO! MISSÃO!', t + 0.1, t + 3.1)
t += 3.2

# 2. The Economist
add_title_card('O BRASIL DÁ AS COSTAS PRO FUTURO', t + 0.5, t + 6.0)
add_title_card('VIRANDO AS COSTAS PRA VOCÊS!', t + 6.2, t + 12.0)
add_title_card('A CANDIDATURA DA ESPERANÇA', t + 12.2, t + 17.8)
t += 18.0
add_grito('PRAÇA RUI BARBOSA · UBERLÂNDIA', t + 0.1, t + 3.1, size=88)
t += 3.2

# 3. Livro Amarelo
add_title_card('QUEM TÁ AQUI COM O LIVRO AMARELO?', t + 0.5, t + 5.5)
add_title_card('FINANCIAMOS CAMPANHA VENDENDO LIVRO!', t + 5.8, t + 12.0)
add_title_card('PROPOSTAS REAIS PRA TODAS AS ÁREAS!', t + 12.2, t + 18.0)
add_title_card('PROPOSTAS QUE NINGUÉM DERRUBOU!', t + 18.2, t + 21.8)
t += 22.0
t += 2.8 # crowd
add_title_card('NINGUÉM DERRUBOU UMA PROPOSTA!', t + 0.2, t + 5.0)
t += 5.2

# 4. Nenhum empresário apoiou
add_title_card('QUANTOS EMPRESÁRIOS APOIARAM?', t + 0.2, t + 3.8)
add_grito('NENHUM!', t + 3.9, t + 5.1, size=130)
t += 5.2
add_grito('A FORÇA VEM DO POVO!', t + 0.1, t + 2.9, size=105)
t += 3.0

# 5. Terras Raras
add_title_card('MINAS GERAIS: O CENTRO DAS TERRAS RARAS', t + 0.5, t + 6.5)
add_title_card('ZONAS ECONÔMICAS ESPECIAIS', t + 6.8, t + 13.0)
add_title_card('OS SUPER-ÍMÃS E BATERIAS FEITOS AQUI!', t + 13.2, t + 20.0)
add_title_card('AS RIQUEZAS SERVINDO O BRASIL!', t + 20.2, t + 26.2)
t += 26.5
add_grito('O BRASIL É NOSSO!', t + 0.1, t + 3.1, size=120)
t += 3.2

# 6. Enfrentamento ao Sistema
add_title_card('O CENTRÃO PRECISA DE RÉGUA!', t + 0.5, t + 5.0)
add_title_card('PARAR DE ROUBAR A POPULAÇÃO!', t + 5.2, t + 10.0)
t += 10.2

# 7. Clímax
add_title_card('VOCÊ NÃO PRECISA VOTAR EM LADRÃO!', t + 0.2, t + 4.5)
add_grito('MEU NOME É RENAN SANTOS!', t + 4.6, t + 7.3, size=100)
t += 7.5
add_grito('É 14 OU NADA!', t + 0.2, t + 3.8, size=125)
add_grito('É 14 OU NADA!', t + 4.0, t + 7.8, size=125)
t += 8.0
add_grito('FORA LADRÕES! FORA CORRUPÇÃO!', t + 0.1, t + 3.9, size=95)
t += 4.0
add_grito('A RUA É A NOSSA REVOLUÇÃO!', t + 0.1, t + 5.0, size=98)
t += 5.2

# Overlays institucionais e conformidade eleitoral
overlays = [
    {'png': 'titles/marca_ia_trilha_vinhetas.png', 'start': 0.0, 'y': 112, 'fade_in': 0.2},
    {'png': 'titles/21.png', 'start': 0.5, 'end': 8.0, 'y': 200},
    {'png': 'titles/marca_bandeira.png', 'start': 8.0, 'end': 8.6, 'y': 0, 'slam': True, 'fade_in': 0.02, 'fade_out': 0.05},
    {'png': 'titles/card_economist.png', 'start': 9.0, 'end': 26.0, 'y': 230},
    {'png': 'titles/marca_mapa.png', 'start': 55.0, 'end': 70.0, 'y': 220},
    {'png': 'titles/marca_fim.png', 'start': round(tot_dur - 3.5, 2), 'y': 0, 'fade_in': 0.3}
]

edl = {
    'name': '23_o_discurso_historico_completo',
    'cover': 15.0,
    'film': True,
    'shots': shots,
    'overlays': overlays,
    'audio': audio,
    'xfade': XF,
    'musica': {'src': 'MUS_energia_de_luta_rap_rock', 'in': 5.0, 'gain': -21},
    'texts': texts,
    'crf': 22
}

# Salva EDL 1080p
os.makedirs(f'{HERE}/edl3', exist_ok=True)
json.dump(edl, open(f'{HERE}/edl3/23_o_discurso_historico_completo.json', 'w'), ensure_ascii=False, indent=1)

# Monta versão 4K (edl3k)
shots_4k = []
for s in shots:
    s4k = dict(s)
    shots_4k.append(s4k)

overlays_4k = []
for ov in overlays:
    ov4k = dict(ov)
    p = ov4k['png']
    if p.endswith('.png') and not p.endswith('@2x.png'):
        ov4k['png'] = p[:-4] + '@2x.png'
    if 'y' in ov4k: ov4k['y'] = ov4k['y'] * 2
    overlays_4k.append(ov4k)

texts_4k = []
for tx in texts:
    t4k = dict(tx)
    if 'size' in t4k: t4k['size'] = t4k['size'] * 2
    if 'y' in t4k: t4k['y'] = t4k['y'] * 2
    if 'pad' in t4k: t4k['pad'] = t4k['pad'] * 2
    if 'border' in t4k: t4k['border'] = t4k['border'] * 2
    texts_4k.append(t4k)

edl_4k = {
    'name': '23_o_discurso_historico_completo_4k',
    'cover': 15.0,
    'film': True,
    'shots': shots_4k,
    'overlays': overlays_4k,
    'audio': audio,
    'xfade': XF,
    'musica': {'src': 'MUS_energia_de_luta_rap_rock', 'in': 5.0, 'gain': -21},
    'texts': texts_4k,
    'crf': 22
}
os.makedirs(f'{HERE}/edl3k', exist_ok=True)
json.dump(edl_4k, open(f'{HERE}/edl3k/23_o_discurso_historico_completo.json', 'w'), ensure_ascii=False, indent=1)

print('EDLs 1080p e 4K geradas com sucesso para 23_o_discurso_historico_completo!')
