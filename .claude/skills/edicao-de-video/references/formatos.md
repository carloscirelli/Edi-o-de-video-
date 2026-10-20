# Formatos

## Índice
- Reels falado (9:16)
- YouTube / tutorial (16:9)
- Reels só motion (sem gravação)
- Stories (sequência de telas)
- Corte de vídeo longo (podcast/live) → Reels

## Reels falado (9:16, 1080×1920) — exemplo `assets/exemplos/reels-falado_desafio-dia09.html`
- Textos no terço de baixo (y ≈ 1050–1450), legenda em y ≈ 1640, nunca sobre o rosto (rosto costuma ficar
  em y ≈ 350–800).
- Zona segura do Instagram/TikTok: nada importante nos 250 px de cima, abaixo de y ≈ 1700, nem nos ~140 px da
  direita (botões).
- Fonte horizontal 16:9 → reenquadrar no HyperFrames: `#cam` com o vídeo em 3413×1920 (cover da altura) e
  `tl.set("#cam", {x}, t)` a cada troca de plano; `x = clamp(540 − cx·3413, −2333, 0)` (cx = posição do rosto
  0–1, lida numa folha de contato por plano; trocas de plano por detecção de cena). Nunca barras pretas.
- Transições de câmera (giro, produto na lente) reforçadas com desfoque/zoom (ver corte.md §4).
- Saída: `videos/<nome>/<nome>_reels.mp4`.

## YouTube / tutorial (16:9, 1920×1080) — exemplo `assets/exemplos/youtube-tutorial_nexo-lampada.html`
- Textos no terço do lado oposto ao rosto (normalmente esquerdo, x ≈ 110); com o celular em close, no alto
  entre o celular e o rosto (bloco centrado numa largura de ~1560 px). Margem 80 px. Legenda 54 px em y ≈ 930.
- Fonte vertical → 9:16 centralizado e laterais com a própria imagem ampliada e desfocada.
- Tutorial: tela cheia de 1 s por passo + etiqueta tracejada no canto superior esquerdo; selo de velocidade
  tracejado (⏩ 3×) no canto superior direito durante os trechos acelerados (tempos exatos do `segments.json`).
- Canal Nexo: vinheta logo depois da intro (marcas.md) e tela final de 3,5 s (fundo escuro com grade, logo
  desenhando, tagline em itálico, botão "+ inscreva-se").
- Vídeos longos: renderizar antes 20–30 s para validar; > 10 min → sub-composições por capítulo.
- Saída: `videos/<nome>/<nome>_youtube.mp4`.

## Reels só motion (sem gravação) — exemplo `assets/exemplos/reels-so-motion_new-casa-ja-sabe.html`
Quando o usuário dá só um tema ("Sua casa já sabe o que você vai fazer"):
1. Confirmar marca (logo/cores) se não for óbvio — ver marcas.md.
2. Roteiro de ~20–25 s: gancho (0–3 s) → 3–4 cenas concretas do tema → virada de impacto ("Não é mágica." →
   "É automação.") → CTA ("chama no direct", sem inventar @ nem telefone).
3. Cenas com ilustração animada em SVG/HTML (cortina abrindo, interruptores desligando, pino no mapa, contador
   de temperatura, lua) + texto lead/bold. Logo pequeno no topo (y ≈ 255) e grande no CTA.
4. Música original sintetizada (som.md) em volume cheio (~0,5) + efeitos; normalizar −14 LUFS no fim.

## Stories (sequência) — exemplo `assets/exemplos/stories_indico-nao-indico.html`
- Uma composição longa (capa 5 s + telas de 6 s) e depois cortar em arquivos separados com ffmpeg, um por
  story, numerados na ordem de postagem (`01-capa.mp4`…), + um `.png` do quadro final de cada (versão estática).
- Zona segura: nada acima de y = 250 nem abaixo de y ≈ 1600 (barra de resposta).
- Sem música (o usuário põe música do Instagram), só efeitos. Última tela com caixa tracejada "responde aqui 👇"
  para a figurinha de enquete/caixa de perguntas.
- Formato "Indico x Não indico": situação (lead + bold palavra a palavra) → carimbo verde ✓ INDICO / vermelho
  ✗ NÃO INDICO com tremidinho e fundo tingido → "por quê?". Conteúdo escrito por você: avisar que a equipe pode
  trocar qualquer situação.
- Saída: `Resultados/<nome-da-sequencia>/`.

## Corte de vídeo longo → Reels
- Fonte do YouTube: não baixar o vídeo inteiro. Legenda automática primeiro
  (`yt-dlp --skip-download --write-auto-subs --sub-langs pt-orig --sub-format json3`, `scripts/yt_subs_text.py`),
  escolher o trecho, baixar só ele com margem (`--download-sections "*MM:SS-MM:SS" --force-keyframes-at-cuts`) e
  transcrever no Scribe só ele.
- Para achar os melhores momentos e montar o arco (gancho → setup → tensão → clímax → payoff), usar a skill
  `edit-labs-ai:corte-viral` (só decupagem, escolha e enquadramento vertical). Não usar o estilo Vox do
  `motion-vox` nem B-roll do Higgsfield sem o usuário pedir.
- Pessoas reais: nunca gerar o rosto delas em IA; não ilustrar letra/conteúdo +18 — deixar no rosto.
