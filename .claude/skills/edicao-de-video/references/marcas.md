# Marcas e canais

## Nexo — "Automação Faça Você Mesmo" (apresentador: Luca)
- Tutoriais de automação residencial (YouTube 16:9) e o **Desafio 30 dias de automação** (Reels, um por dia).
- Destaque azul `#4d7cff`; legenda: palavra falada em `#6f95ff`.
- Logo "nexo" em SVG (viewBox 0 0 230 90; o PNG do cliente tem só 150 px — usar o SVG):
  ```html
  <svg viewBox="0 0 230 90"><g fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14 72 V48 a20 20 0 0 1 40 0 V72" /><path d="M72 52 H112 A20 20 0 0 0 72 52 A20 20 0 0 0 92 72 H110" />
    <path d="M128 36 L140 48 M128 68 L140 56 M152 56 L164 68" /><circle cx="196" cy="52" r="20" /></g>
    <path d="M152 48 L164 36" fill="none" stroke="#4d7cff" stroke-width="9" stroke-linecap="round" /></svg>
  ```
  Marca d'água no canto (16:9 inferior direito; 9:16 superior direito), no card "canal da Nexo" e na tela final
  (logo desenhando + "automação faça você mesmo" + "+ inscreva-se").
- **Vinheta** (`Edição de video/videos/vinheta-nexo/vinheta-nexo_youtube.mp4`, 4,6 s): nos vídeos do YouTube, logo
  depois da intro (no tutorial, após "bora pro vídeo!"). Encaixar com `scripts/splice_clip.py` num ponto de emenda;
  esconder marca d'água e degradê durante ela. Nos Reels, só se pedirem.
- Produto citado: lâmpada da linha "Avant Neo" (`img/avant-neo.jpg` nos projetos do tutorial).
- Desafio 30 dias: selo "DIA NN/30" em caixa tracejada no canto superior esquerdo (y ≈ 262), marca d'água no superior
  direito; se ele anunciar o próximo, fechar com "amanhã, no dia NN+1: …".

## New Sistemas Inteligentes — automação e tecnologia de ambientes (Instagram)
- **Empresa diferente da Nexo.** (Na primeira vez, a transcrição veio "New"; confirmar a marca quando não for óbvio.)
- Logo **original do cliente** — usar sempre este arquivo, nunca redesenhar (um redesenho foi recusado):
  `assets/marcas/new-sistemas-logo.png` (círculo recortado, fundo transparente, ~360 px) e o original com fundo branco
  `assets/marcas/new-sistemas-logo-original.png`. Pedir versão em alta (SVG/PDF) se for usar muito grande.
- Paleta: fundo verde-oliva quase preto `#0e1307`, destaque dourado `#dcae1f`, texto escuro `#1a2309`; cartão de
  impacto dourado com texto escuro.
- CTA usado: "quer uma casa assim?" + logo + "New Sistemas Inteligentes" + botão "chama no direct ✉️" +
  "automação e tecnologia de ambientes". Não inventar @, site ou telefone.

## Marca nova
Perguntar uma vez nome, logo (arquivo) e cor; anotar aqui e na memória. Sem logo: nome em tipografia e paleta neutra,
avisando que troca quando chegar o arquivo.
