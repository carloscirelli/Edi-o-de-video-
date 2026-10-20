# Etapa 2 — tipografia animada (estilo aprovado)

Estilo tirado de 3 vídeos de referência do YouTube que o usuário escolheu (baixados em
`Edição de video/referencias/`): Eidryan "Passei 45 dias…" (Kw4cdex7T6I), Thiago "7 técnicas" (vOSgyRv-FE8),
Mateus Dias "Claude Opus = vídeos de R$100k" (61u9wOT-Cds). Nas referências quase só há tipografia; nos
vídeos do usuário ele aparece na tela — o estilo é adaptado para não cobrir o rosto.
Substitui o estilo antigo "glassmorphism Apple + legenda pill/amarela" (não usar mais).

## Índice
1. Fonte e cores
2. Catálogo de elementos
3. Animação (helpers GSAP)
4. Legendas
5. Telas cheias, escurecer/desfocar o vídeo
6. Armadilhas do HyperFrames/GSAP

## 1. Fonte e cores
- **Poppins** local (`assets/fontes/`: 800, 700, 500, 300 itálico, 900 itálico) via `@font-face`; cobre acentos.
- Letras apertadas: negrito grande `letter-spacing` ≈ −3 a −5 px (ou −0,04 em); CAIXA ALTA −2 px.
- Branco + **uma** cor de destaque da marca (ver marcas.md). Sombra suave nos textos sobre vídeo
  (`text-shadow: 0 6px 22px rgba(0,0,0,.5)`), degradê escuro onde os textos ficam (`#shade`).

## 2. Catálogo de elementos (copiar CSS dos exemplos em `assets/exemplos/`)
| Elemento | Quando | Origem |
|---|---|---|
| `lead` itálico fino (300, 40–52 px) + `bold` 800 grande (90–120 px) | padrão de quase toda frase: "vou te ensinar" → **COMO INSTALAR** | Mateus Dias |
| `glow` CAIXA ALTA com brilho, empilhado | termos fortes ("NOVO / PADRÃO", "MUITO FÁCIL") | Thiago |
| Entrada palavra por palavra desfocada | frases-chave, citações | Eidryan / Mateus |
| Máquina de escrever | frase de transição ("sem mais enrolação") | Eidryan |
| Pills brancas 3D (`box-shadow: 0 6px 0 #b9bdc8`) com ícone | listas: apps, recursos, CTA (like/inscreva/compartilha) | Thiago |
| Caixa tracejada (`border: 3.5px dashed`) | rótulos, "link na descrição", selos de passo e de velocidade | Mateus Dias |
| Faixa escura com ✓ | ações concluídas ("o que funciona hoje ✓", "+ adicionar dispositivo") | Mateus Dias |
| Número gigante na cor de destaque | "em menos de **5** min", "**3** vezes", "**+5**" | Mateus Dias |
| Células acendendo (grade de dias, 1-2-3) | contagens, "dias contados" | Eidryan |
| "?" gigante 3D (text-shadow empilhado) | perguntas ("o seu também é assim?") | Eidryan |
| Palavra-fantasma vazada atrás (`-webkit-text-stroke`) | ênfase ("NUNCA", "MATTER") | Eidryan |
| Estrelinhas ✦ com brilho | acento em momentos de destaque | Mateus Dias |
| Riscado (barra animada) | negação ("ficar parado") | — |
| Barra de progresso | "em expansão", hora do dia | Mateus Dias |
| Cartão de tela cheia na cor da marca com grade | 1–1,5 s de impacto ("NÃO.", "em menos de 5 min", "é automação.") | Mateus Dias |

Densidade: um bloco de texto por frase importante, sem parágrafos. Cada bloco entra junto da palavra que
ilustra (tempo da transcrição do corte) e sai com desfoque curto (≤ 0,2 s).

## 3. Animação (helpers usados em todos os exemplos)
```js
const q = (s) => Math.round(s * 30) / 30;            // sempre alinhar ao quadro
const IN = (sel, t, o = {}) => tl.fromTo(sel,
  { opacity: 0, filter: "blur(16px)", scale: o.scale ?? 1.14, y: o.y ?? 0 },
  { opacity: 1, filter: "blur(0px)", scale: 1, y: 0, duration: o.d ?? 0.28, ease: "power3.out", immediateRender: false }, q(t));
const OUT = (sel, t) => tl.to(sel, { opacity: 0, filter: "blur(12px)", y: -12, duration: 0.18, ease: "power2.in" }, q(t - 0.18));
```
Pills/caixas entram com `back.out(2.2)` (pop); palavra de destaque com `scale 1.3–1.6`. O exemplo 16:9 tem um
construtor `BLOCK(pos, t0, t1, parts)` que cria e anima blocos a partir de uma lista — reaproveitar.

## 4. Legendas
- Poppins 700 branca com sombra, sem caixa atrás; a palavra que está sendo falada em azul claro `#6f95ff`
  (Nexo) — em outra marca, um tom claro da cor de destaque.
- 9:16: 62 px em y ≈ 1640, blocos de até 3 palavras. 16:9: 54 px em y ≈ 930, até 4 palavras.
- Blocos quebram em pontuação, pausa > 0,6 s ou palavra com maiúscula (começo de frase).
- Escondidas nas telas cheias e onde a mesma frase já está escrita grande (lista `OFF` nos exemplos).
- Geradas no próprio script da composição a partir de `WORDS` (transcrição do corte) — ver exemplos.

## 5. Telas cheias e foco
- `#dim` (radial preto) + `filter: blur()` num wrapper do vídeo (`#blurwrap`) para os momentos de impacto;
  nunca no mesmo elemento que já tem outro `filter` animado (transições de câmera usam `#frame`).
- Tutorial: cada passo abre com 1 s de tela cheia "passo **1º** desligar" sobre o vídeo desfocado; depois fica
  uma etiqueta tracejada "① Desligar" no canto.

## 6. Armadilhas
- `fromTo` cria o estado inicial na hora: usar `immediateRender: false` e esconder os filhos no fim com
  `gsap.set(hidden, {opacity: 0})`, senão tudo aparece empilhado no começo.
- `tl.call()` não roda quando o render pula para um tempo (seek): para trocar estado, usar `tl.set(...)` ou um
  tween com `onUpdate` (contadores, máquina de escrever, grade acendendo).
- `transform: translateX(-50%)` inline some quando o GSAP anima `scale`: usar `gsap.set(el, {xPercent: -50})`.
- Não animar `visibility`/`autoAlpha` num elemento `.clip`; animar um filho.
- Rotação em SVG: `svgOrigin`, não `transform-origin`.
- Vídeo de fundo precisa de keyframes densos (`-g 30 -keyint_min 30`), senão o render congela quadros.
- Áudio/música mais curto que o `data-duration` → o HyperFrames encurta (aviso, sem erro).
