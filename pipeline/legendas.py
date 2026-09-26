#!/usr/bin/env python3
"""legendas.py — legenda de post de cada reel; confere tamanho (>= 500) e ausência de travessão."""
import json

L = {
"01_voce_tinha_que_estar_aqui": """Tem coisa que o celular não consegue mostrar direito. Essa noite chegou perto.

Sexta, 25 de setembro, 20h48. A praça em frente à igreja tomada de gente, sinalizador aceso, fumaça subindo, bandeira pra todo lado e o jingle tocando alto.

Tudo gravado no iPhone e cortado no tempo da música: do primeiro sinalizador até a igreja sumindo na névoa rosa no final.

Se você estava lá, sabe como foi.

Salva pra lembrar dessa noite e manda pra quem estava com você na praça.

📍 Uberlândia, MG

#uberlandia #uberlandiamg #eleicoes2026 #shotoniphone""",

"02_tem_noite_que_merece_camera_lenta": """Cada bandeira subindo devagar na frente da igreja iluminada.

Gravado a 120 quadros por segundo e desacelerado até quatro vezes, então nenhum quadro foi inventado: é o movimento real, só que mais lento.

O som é a praça inteira cantando junto, no tempo normal.

A névoa rosa do começo é a fumaça dos sinalizadores iluminada pela fachada.

Qual desses quadros você colocaria de papel de parede? Comenta o número de 1 a 5.

Salva pra assistir de novo com som.

📍 Uberlândia, MG · 25.09.2026

#uberlandia #cameralenta #slowmotion #shotoniphone""",

"03_isso_nao_e_filme": """Parece cena de cinema, mas foi em Uberlândia, na sexta à noite.

Sinalizador aceso, fumaça laranja cobrindo a praça e a igreja aparecendo e sumindo no meio da névoa.

Os estouros que você ouve são do próprio vídeo, gravados na hora. Cada corte cai em cima de um estouro, pra imagem e som baterem juntos.

No final, a fachada some por alguns segundos dentro da névoa dourada.

Assiste com som.

Manda pra alguém que precisa ver isso e salva pra rever depois.

📍 Uberlândia, MG · 25.09.2026

#uberlandia #uberlandiamg #shotoniphone #cinematografia""",

"04_olha_o_tamanho_disso": """A câmera vai abrindo e a praça não acaba.

Esse é o plano geral de sexta, 25 de setembro, gravado do fundo, no meio do povo, com o coro vindo lá da frente.

Sem drone: o recuo é só a imagem 4K sendo aberta aos poucos, até aparecer a fachada inteira iluminada e o mar de celulares apontados pra ela.

Do palco até o fundo, era celular aceso até onde a vista alcançava.

Marca alguém que estava nesse meio.

Salva esse pra comparar com os próximos.

📍 Uberlândia, MG

#uberlandia #uberlandiamg #eleicoes2026 #shotoniphone""",

"05_o_brasil_que_importa_esta_aqui": """“O Brasil que importa está aqui na minha frente, em Uberlândia.”

Dois momentos da noite de sexta, 25 de setembro: a praça respondendo em coro “O Brasil é nosso!” e um trecho do discurso em frente à igreja.

Legendado palavra por palavra pra quem assiste sem som. Áudio original, sem corte dentro das frases.

Repara no fundo: a porta vermelha da igreja, toda iluminada, atrás do palanque.

Dá o play com som: o coro é o próprio áudio do vídeo, gravado no meio da praça.

Salva e manda pra quem não conseguiu ir.

📍 Uberlândia, MG

#uberlandia #uberlandiamg #eleicoes2026 #discurso""",

"06_loop_lua": """Deixa rodar mais uma vez. 🌙

A lua apareceu do lado da torre bem na hora em que as bandeiras subiram na frente da igreja.

Câmera lenta de verdade, gravada a 100 quadros por segundo, com a praça cantando ao fundo.

O céu ficou limpo, azul-marinho, sem nenhuma nuvem na frente da lua.

O vídeo não tem fim: tenta achar o ponto em que ele volta pro começo e comenta o segundo exato.

Salva pra quando precisar de um respiro.

📍 Uberlândia, MG · 25.09.2026

#uberlandia #fotografianoturna #shotoniphone #loop""",

"07_a_luz_dessa_noite": """Antes de tudo, repara na luz.

A fachada inteira acesa em tom quente, a lua do lado da torre, a fumaça branca cruzando o céu azul-marinho e, no fim, a igreja envolta numa névoa rosa.

Tudo gravado no iPhone à noite, com a cor ajustada pra ficar do jeito que o olho viu na hora.

Cada plano fica três segundos na tela, no tempo do jingle, pra dar tempo de reparar nos detalhes da fachada.

Salva pra ver de novo com calma e manda pra quem gosta de arquitetura.

📍 Uberlândia, MG · 25.09.2026

#uberlandia #arquitetura #fotografianoturna #shotoniphone""",
"08_e_14_ou_nada": """“É 14 ou nada!”

Foi assim em Uberlândia, na sexta, 25 de setembro: o Renan falou do palanque em frente à igreja e a Praça Rui Barbosa respondeu em coro, várias vezes seguidas.

O som é o áudio real do meio da praça, com a voz do palanque na frente e a multidão por trás.

Assiste com som: primeiro o palanque, depois a praça respondendo.

Legenda palavra por palavra pra quem assiste sem som.

Compartilha com quem estava lá e salva pra lembrar desse momento.

📍 Praça Rui Barbosa (Bicota), Uberlândia

#uberlandia #partidomissao #eleicoes2026 #renansantos""",

"09_ei_globo_chama_o_renan": """“Ei, Globo, chama o Renan!”

Um dos coros da noite de 25 de setembro, em Uberlândia: a praça pedindo que a emissora chame o candidato do 14 para o debate.

Gravado no meio do povo, com o som original, do jeito que aconteceu, sem trilha por cima.

Nove segundos que mostram o clima do ato em frente à igreja.

Repara no fundo: a porta vermelha da igreja e as bandeiras passando na frente do palanque.

Compartilha pra esse coro chegar longe e salva pra rever quando quiser.

📍 Praça Rui Barbosa, Uberlândia

#uberlandia #partidomissao #debate #renansantos""",

"10_quem_ta_aqui_com_o_livro_amarelo": """Quem tá aqui com o livro amarelo?

Foi com essa pergunta que o Renan abriu um dos trechos do discurso em Uberlândia, em 25 de setembro, e contou que a campanha é financiada com a venda do livro de propostas.

Meio ambiente, segurança, saúde, educação, enfrentamento ao crime e reforma do Estado: os temas que ele citou estão legendados no vídeo, palavra por palavra.

Salva pra rever o trecho e manda pra quem ainda não conhece o livro.

📍 Praça Rui Barbosa, Uberlândia

#livroamarelo #uberlandia #partidomissao #renansantos""",

"11_o_plano_das_terras_raras": """Terras raras, ímãs, baterias e drones.

Esse foi o assunto de um dos trechos do discurso do Renan em Uberlândia, em 25 de setembro. Ele apresentou a proposta de zonas econômicas especiais em Minas, com parcerias com outros países e empresas para produzir aqui a cadeia inteira, da extração até a bateria do carro elétrico.

O trecho está legendado palavra por palavra, com o áudio original da praça.

Salva pra acompanhar esse debate e compartilha com quem é de Minas.

📍 Praça Rui Barbosa, Uberlândia

#terrasraras #minasgerais #uberlandia #partidomissao""",

"12_o_final_do_discurso": """O fim do discurso em Uberlândia, na noite de 25 de setembro.

Minas, as terras raras e o futuro do estado foram os temas do encerramento, que termina com o número do partido e um “muito obrigado” para a praça.

A legenda acompanha a fala palavra por palavra. Um trecho curto sem transcrição confiável ficou sem legenda, marcado com reticências, pra nada ser colocado na boca de ninguém.

Compartilha com quem não conseguiu ir e salva pra rever.

📍 Praça Rui Barbosa, Uberlândia

#uberlandia #minasgerais #partidomissao #renansantos""",

"13_o_que_a_praca_gritou": """Missão. Eu voto 14. Renan. O Brasil é nosso. 14 ou nada.

Cinco coros gravados no meio da Praça Rui Barbosa, em Uberlândia, na noite de 25 de setembro, em sequência e cada um com o som original do próprio momento.

Nada de trilha por cima: é só a voz da praça, do jeito que chegou no celular.

Cada coro aparece escrito na tela, em amarelo, pra quem está vendo sem som, e as imagens são do mesmo instante de cada grito.

Assiste com som, salva e compartilha com quem estava lá com você.

📍 Praça Rui Barbosa, Uberlândia

#uberlandia #partidomissao #eleicoes2026 #renansantos""",
}

GENERICOS = {"#fitness", "#motivation", "#instagood", "#reels", "#viral", "#fyp", "#love"}
for k, t in L.items():
    tags = [w for w in t.split() if w.startswith("#")]
    assert "—" not in t and "–" not in t, f"{k}: travessão"
    assert not GENERICOS & set(tags), f"{k}: hashtag genérica"
    assert 3 <= len(tags) <= 5, f"{k}: {len(tags)} hashtags"
    assert len(t) >= 500, f"{k}: {len(t)} caracteres"
    print(f"{k}: {len(t)} caracteres, {len(tags)} hashtags")
json.dump(L, open("legendas.json", "w"), ensure_ascii=False, indent=1)
