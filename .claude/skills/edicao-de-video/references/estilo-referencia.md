# Estilo de referência (padrão a partir de out/2026)

O usuário mandou três vídeos de TikTok e pediu que **todos os vídeos dele saiam parecidos com eles**. Folhas de
quadros em `assets/referencias/`. São de outros criadores (@altralab.br, @duraesxz, @zenzu.visuals): copiar a
linguagem, nunca o conteúdo, a marca, o @ ou a voz deles.

## A fórmula comum aos três
- **"Tela gravada com o celular"**: a animação roda numa tela (notebook/monitor) e o vídeo é filmado de perto, com o
  teclado aparecendo embaixo, perspectiva leve, reflexo e um pouco de ruído. Isso é a assinatura: o conteúdo parece
  "feito agora pelo Claude/IA, olha aqui na minha tela".
- **Fundo escuro** com gradiente difuso (manchas de luz desfocadas, tipo aurora/bokeh) numa cor só da marca:
  laranja/âmbar quente (ref1, ref3) ou azul elétrico (ref2). Nada de branco chapado, salvo em telas cheias de impacto.
- **Texto entra palavra por palavra no ritmo da narração**, com desfoque → nítido, e a palavra-chave em outra cor,
  em negrito ou maior (`nunca` em laranja, `estratégia` em azul claro, `dissesse...` grande).
- **Interface de IA como cenário**: caixa de prompt ("I want a website for…", "Você descreve o vídeo…"), botões
  em pill com brilho (Create, Write, Code…), cursor clicando, chips (`Sonnet 5`), cards de vidro (glassmorphism).
- **Blocos de prova**: números gigantes contando (`+90`, `+R$11M`), cards numerados 01–04, passos 1-2-3 numa linha,
  uma palavra em tela cheia (`Cores`, `Tipografia`, `E` serifado) — cada bloco 1,5–3 s.
- **Fecho com logo** grande no centro (ex.: wordmark com brilho) ou frase de assinatura ("Built with Claude.").
- **Legenda fixa no topo** (fora da animação, sobre o vídeo, em branco, fonte sans média, 2 linhas + emoji):
  gancho no começo ("Talvez esse seja o fim dos motion designers🤯 (feito 100% com o Claude)") e troca para a
  chamada no final ("Passo a passo completo na nossa bio👇"). Ou caixa branca com texto preto (ref2).

## Ritmo e som
- Duração: 15–60 s. Quase sem cortes secos: é um plano contínuo da tela; a mudança vem da animação (troca de tela a
  cada 2–4 s).
- Narração em off, calma e confiante, frases curtas; texto na tela acompanha cada palavra. Música eletrônica/ambiente
  baixa por baixo; no vídeo só de música (ref3) a música manda e os cortes caem na batida.
- Volume final perto de −16 a −14 LUFS (as referências estão entre −22 e −15, mais baixas do que o ideal).

## Como produzir (pipeline)
1. Composição HyperFrames 16:9 (a "tela do notebook") com o fundo de manchas, a tipografia e a UI de IA —
   seguir `tipografia.md` para as entradas (Poppins/sans apertada, itálico pequeno puxando palavra grande).
2. Render dessa tela e **montar a "gravação"**: colocar o render dentro de um quadro de notebook/monitor em
   perspectiva (filmagem real do usuário apontando para a tela, ou mockup gerado), com teclado embaixo, leve
   tremida de mão, granulação e reflexo. Formato final 9:16 (ou 16:9 para YouTube).
3. Legenda fixa no topo por cima de tudo + chamada final ("na bio👇").
4. Narração: voz do próprio usuário (gravada ou clone autorizado dele) ou uma voz de biblioteca parecida em clima.
   **Nunca clonar a voz dos criadores das referências.** TTS/clone pago só depois de dizer o custo.
