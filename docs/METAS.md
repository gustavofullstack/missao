# Metas, plano e progresso — série de reels do Gustavo (@gusmatrix)

Atualizado em 27/09/2026, 20h BRT. Eleição em 04/10: nada é postado nesse dia.

## Objetivo

Apoio do Gustavo à Missão e ao Renan Santos com conteúdo vertical (9:16) bem feito e com contexto completo. A fonte é a gravação dele do ato de Uberlândia (25/09) mais cortes dos canais oficiais do partido e dos candidatos, sempre creditados.

## Metas

| Meta | Alvo | Situação |
|---|---|---|
| Posts por dia no X | 10 | 10 em 27/09; agenda de 28 a 30/09 montada |
| Posts por dia no YouTube Shorts | 10 | 9 em 27/09 (mais a íntegra); agenda até 30/09 |
| Posts por dia no Instagram | 6 (rede mais sensível a volume) | 7 em 27/09; agenda até 30/09 |
| Posts por dia no TikTok | até 4 | feito pela sessão do MacBook (único navegador logado) |
| Discurso completo de Uberlândia | 8 partes + íntegra | partes prontas; parte 1 e íntegra no ar; uma parte por dia até 03/10 |
| Cortes novos por dia | 8 a 10 | 27/09: 40 a 45, 82 a 123 |

## Regras que não mudam

- Nada de repost integral de vídeo de terceiros: só corte com legenda, título e crédito do canal oficial.
- Nada de trecho com xingamento, ataque pessoal ou acusação de crime contra pessoa nomeada.
- Afirmação de fato fica atribuída a quem falou ("segundo o Renan…").
- IA sempre rotulada na tela e na legenda. Sem voz sintética de pessoa real.
- Login e senha são sempre do Gustavo. Senha colada no chat não é usada.
- Nada é postado em 04/10.

## Plano (3 frentes)

| Frente | Papel |
|---|---|
| MACRIX | orquestra; triagem com agentes (Sonnet para transcrição longa, Laya para tema, Gemini Flash para revisar legenda, Codex para revisar código); render das gravações 4K do Gustavo (`render.py`, dentro do limite de CPU) |
| vaio (Arch) | baixa as fontes do YouTube (a MACRIX é bloqueada); renderiza os cortes (`cortes.py`); posta X, YouTube e Instagram pelo Brave "Missão Postagem" (`postx.sh`, `postyt.sh`, `postig.sh`, `agenda.sh`) |
| MacBook | TikTok, pelo Chrome logado |

## Tarefas

- [x] Discurso em 8 partes + íntegra (13:40)
- [x] Postagem automática no X, YouTube e Instagram com fila por dia
- [x] Cortes de Kim, Amanda, Guto, Renan (Paresi, RS), Livro Amarelo, formação do partido
- [x] Gritos da multidão das gravações do Gustavo (120 a 123), som original, sem IA
- [x] Trilha abaixada sob a fala com rótulo "trilha gerada por IA"
- [ ] TikTok: login feito só no MacBook; a sessão de lá posta
- [ ] Versões 4K SDR das gravações do Gustavo (120 a 123) para o YouTube
- [ ] Mais fontes oficiais: Rafa Minato, Guto (2026), Arthur do Val (vídeos de proposta, não debate)
- [ ] Conferir o Facebook do Gustavo: a parte 1 pode ter saído lá (o IG liga o compartilhamento por padrão; já desligado no script)

## Descartados, e por quê

- "Tutorial haters" do Arthur: é reação a debate de outro canal, quase todo xingamento.
- Entrevista da Jovem Pan: material da emissora e layout de TV que muda.
- 84, 85, 112: o enquadramento cortava quem falava, ou o tema era sagrado para o povo Paresi.
- 114: pessoal demais, fraco como post político.
