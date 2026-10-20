---
name: edicao-de-video
description: Edição de vídeo completa do usuário (pt-BR) para a Nexo, a New Sistemas Inteligentes e outros — corte com voz sincronizada, tipografia animada no estilo aprovado (Poppins, entradas desfocadas, pills, caixas tracejadas, números gigantes), música baixa, vinheta e entrega na pasta Resultados. Use sempre que o usuário pedir para editar, cortar, reeditar ou corrigir um vídeo; fazer Reels, TikTok, Shorts, vídeo de YouTube, tutorial, stories, vídeo só com animação a partir de um tema, ou cortes de podcast; mexer em legenda, música, vinheta, logo ou sincronia de áudio de um vídeo — mesmo sem dizer "skill" e mesmo quando ele usar /reels ou /youtube.
---

# Edição de vídeo (Nexo / New Sistemas / outros)

Tudo o que foi aprendido editando os vídeos deste usuário: o fluxo, o estilo que ele aprovou e os erros que já
custaram retrabalho. Projeto em `C:\Users\lscir\Edição de video` (ler o `CLAUDE.md` de lá também — tem detalhes
de ferramentas). Responder sempre em português.

## Escolha o caminho

| O usuário quer… | Caminho |
|---|---|
| Editar um vídeo gravado vertical (Reels/TikTok/Shorts) | Etapa 1 + Etapa 2, formato **Reels falado** |
| Editar um vídeo gravado horizontal (YouTube, tutorial) | Etapa 1 + Etapa 2, formato **YouTube/tutorial** |
| Um Reels a partir de um tema, sem gravação | Só Etapa 2, formato **Reels só motion** |
| Stories (sequência de telas) | Só Etapa 2, formato **Stories** |
| Cortes de um podcast/live/link longo | `edit-labs-ai:corte-viral` para achar os trechos → Etapa 1 → Etapa 2 Reels |
| Corrigir algo de um vídeo já entregue | Mexer só no necessário, re-render, **nome novo** (`_v2`) |

Detalhes de cada formato: `references/formatos.md`. Não pergunte estilo nem formato quando o pedido já diz
(/reels = 9:16, /youtube = 16:9); pergunte só o que for ambíguo de verdade (ex.: qual marca, se há vídeo gravado).

## Etapa 1 — corte (ler `references/corte.md`)
1. Transcrever com Scribe (cacheado) e ler as palavras com as pausas (`scripts/words_pauses.py`).
2. Decidir os trechos com agressividade alta: sem pausas, vícios, falsos começos e repetições (fica a última
   versão completa). Demonstração sem fala é acelerada 2–3×, não cortada. Respeitar transições gravadas na câmera.
3. Montar com `scripts/build_cut.py` — cada trecho com o mesmo número de quadros e de amostras, áudio emendado
   uma vez só. **Não usar o render.py do video-use para cortes com muitos trechos**: ele fez a voz sair da boca
   no tutorial da lâmpada e foram várias rodadas até achar a causa.
4. Conferir com `scripts/check_sync.py source` antes de seguir.

## Etapa 2 — HyperFrames (ler `references/tipografia.md`)
Carregue as skills do plugin quando for usá-las: `hyperframes:hyperframes` (mapa), `hyperframes:talking-head-recut`
+ `hyperframes:hyperframes-core` (composição sobre quem fala), `hyperframes:hyperframes-animation` /
`hyperframes:hyperframes-keyframes`, `hyperframes:media-use` / `hyperframes:hyperframes-audio`, `hyperframes:hyperframes-cli`.

- **Comece de um exemplo aprovado** em `assets/exemplos/` em vez de do zero — eles já têm os helpers, o layout
  seguro e as legendas: Reels falado (`reels-falado_desafio-dia09.html`), tutorial 16:9
  (`youtube-tutorial_nexo-lampada.html` + `youtube-tutorial_make_comp.py`), Reels só motion
  (`reels-so-motion_new-casa-ja-sabe.html`), Stories (`stories_indico-nao-indico.html`). Copie também
  `assets/fontes/` (Poppins) e `vendor/gsap.min.js` / `sfx/` de um projeto existente.
- Estilo: Poppins com letras apertadas; frase pequena em itálico puxando palavra grande em negrito; CAIXA ALTA com
  brilho; pills 3D; caixas tracejadas; números gigantes; telas cheias curtas de impacto. Uma cor de destaque da
  marca (`references/marcas.md`). Texto fora do rosto e dentro da zona segura do formato.
- Vídeo de fundo: o `cut.mp4` (ou o vídeo base com vinheta) reencodado com keyframes a cada 1 s.
- Vinheta/clipe no meio: `scripts/splice_clip.py` gera um vídeo base contínuo — nunca dois `<video>` com
  `data-media-start` (atrasou a voz).
- Som: `references/som.md` — um efeito por evento visível, nunca sobre palavra importante; música baixa
  (0,08 sob a fala, 0,28 sem fala).

## Conferir e entregar (ler `references/entrega.md`)
lint → snapshot em todos os blocos de texto (olhar as folhas) → render → `check_sync.py render` (final × base) →
volume (−16 LUFS YouTube, −14 Reels de motion) → copiar para `Resultados\` (correção = nome novo, tirar o antigo)
→ `SendUserFile` → resumo curto do que foi feito e de como foi conferido.

## Coisas que este usuário já decidiu
- Não pagar por B-roll de IA (Higgsfield/Seedance/fal); só usar se ele pedir, dizendo o custo antes.
- New Sistemas Inteligentes ≠ Nexo; usar o logo original dela (`assets/marcas/`), nunca um redesenho.
- Vinheta da Nexo depois da intro nos vídeos do YouTube.
- Ambiente, caminhos e manias do Windows: `references/ambiente.md`.
