# Estilo de referência (padrão a partir de out/2026)

O usuário mandou três vídeos de TikTok e pediu que **todos os vídeos dele saiam parecidos com eles**. Folhas de
quadros em `assets/referencias/`. São de outros criadores (@altralab.br, @duraesxz, @zenzu.visuals): copiar a
linguagem, nunca o conteúdo, a marca, o @ ou a voz deles.

## A fórmula comum aos três
- **ATENÇÃO — o que copiar é a animação que roda DENTRO da tela.** Nas referências o criador filmou o próprio
  computador mostrando a edição; o usuário quer o **vídeo que estava no computador**, em tela cheia. Não fazer
  mockup de notebook, teclado, câmera na mão nem granulação de filmagem (isso foi feito e recusado).
- **Fundo escuro** com gradiente difuso (manchas de luz desfocadas, tipo aurora/bokeh) numa cor só da marca:
  laranja/âmbar quente (ref1, ref3) ou azul elétrico (ref2). Nada de branco chapado, salvo em telas cheias de impacto.
- **Texto entra palavra por palavra no ritmo da narração**, com desfoque → nítido, e a palavra-chave em outra cor,
  em negrito ou maior (`nunca` em laranja, `estratégia` em azul claro, `dissesse...` grande).
- **Interface de IA como cenário**: caixa de prompt ("I want a website for…", "Você descreve o vídeo…"), botões
  em pill com brilho (Create, Write, Code…), cursor clicando, chips (`Sonnet 5`), cards de vidro (glassmorphism).
- **Blocos de prova**: números gigantes contando (`+90`, `+R$11M`), cards numerados 01–04, passos 1-2-3 numa linha,
  uma palavra em tela cheia (`Cores`, `Tipografia`, `E` serifado) — cada bloco 1,5–3 s.
- **Fecho com logo** grande no centro (ex.: wordmark com brilho) ou frase de assinatura ("Built with Claude.").
- A legenda branca fixa no topo das referências é do post do TikTok (por cima da filmagem), não da animação: não usar
  por padrão.

## Ritmo e som
- Duração: 15–60 s. Quase sem cortes secos: é um plano contínuo da tela; a mudança vem da animação (troca de tela a
  cada 2–4 s).
- Narração em off, calma e confiante, frases curtas; texto na tela acompanha cada palavra. Música eletrônica/ambiente
  baixa por baixo; no vídeo só de música (ref3) a música manda e os cortes caem na batida.
- Volume final perto de −16 a −14 LUFS (as referências estão entre −22 e −15, mais baixas do que o ideal).

## Como produzir (pipeline)
1. Composição HyperFrames no formato final (9:16 Reels / 16:9 YouTube) em tela cheia: fundo de manchas, tipografia
   palavra por palavra e UI de IA — seguir `tipografia.md` para as entradas.
2. Logo pequeno no topo (y ≈ 255) e grande no CTA. Exemplo pronto: `videos/new-sistemas-elan/` (Reels narrado).
3. Narração: voz do próprio usuário (gravada ou clone autorizado dele) ou uma voz de biblioteca parecida em clima.
   **Nunca clonar a voz dos criadores das referências.** TTS/clone pago só depois de dizer o custo.
