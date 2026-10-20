# Conferência e entrega

## Antes do render
1. `npx -y hyperframes lint .` — 0 erros (avisos de "arquivo grande"/"subcomposição" podem ficar).
2. `npx -y hyperframes snapshot . -o snaps --no-end --at <um tempo por bloco de texto>` e **olhar as folhas de
   contato**: texto em cima do rosto, cortado na borda, sobrepondo selo/logo, tela cheia sem fundo, legenda
   duplicando o texto grande, contraste ruim (texto azul sobre parede clara → mais sombra/escurecer).
3. Corrigir e tirar snapshot só dos pontos alterados.

## Depois do render
1. Duração e streams (`ffprobe`).
2. **Sincronia:** `uv run --with numpy python <skill>/scripts/check_sync.py render final.mp4 base.mp4` (base = o vídeo
   que entrou na composição). Tudo 0 ms / 0 quadros. Diferença de imagem pontual = texto por cima, normal.
3. Volume (som.md) e, se for Reels de motion, `loudnorm` −14 LUFS.
4. Abrir 1–2 quadros finais em tamanho real se houver logo/detalhe fino.

## Entrega
- Copiar para `C:\Users\lscir\Edição de video\Resultados\` (sequências de stories numa subpasta).
- **Correção de algo já entregue → nome novo** (`_v2`, `_v3`…) e tirar o antigo de `Resultados`. Com o mesmo
  nome, o player/app do usuário mostrou a versão antiga e ele achou que nada tinha mudado.
- Mandar com `SendUserFile` (`display: attach` para ele poder salvar; vários arquivos de uma vez na ordem certa).
- Resposta curta em pt-BR: o que foi feito, duração antes → depois, o que foi cortado/acelerado, o que entrou na
  tela, números de volume se relevante, e o que você assumiu (ex.: conteúdo que você escreveu).
- Não afirmar que algo está "corrigido" sem ter medido; dizer como conferiu.

## Comunicação com o usuário
- Ele fala português, é direto, prefere resultado a explicação longa; quando reclama, olhe o vídeo de verdade
  (quadros, áudio no ponto exato que ele citou) antes de responder.
- Não insistir em B-roll pago (Higgsfield/Seedance/fal): ele recusou pagar. Se algo exigir pagamento, dizer o custo
  e esperar o ok. Nunca digitar chaves em sites; chaves que ele colar no chat: usar só em arquivo temporário,
  apagar depois e sugerir trocar.
