# Etapa 1 — corte com sincronia exata

## Índice
1. Transcrição
2. Decidir os trechos
3. Demonstrações e b-roll (tutoriais)
4. Transições gravadas na câmera
5. Gerar o corte (build_cut.py)
6. Conferir a sincronia
7. Por que não o render.py

## 1. Transcrição
- `ffprobe` em cada bruto (duração, resolução, fps, `color_transfer` — iPhone grava HLG `arib-std-b67`, 4K, 60 fps).
- Scribe (ElevenLabs) pelo wrapper do projeto, cacheado — nunca transcrever de novo a mesma fonte:
  `scripts\vu.ps1 transcribe <video> --language pt` (um arquivo) ou `vu.ps1 transcribe_batch <pasta> --language pt`
  (vários clipes; chegam em ordem). Saída: `edit/transcripts/<clipe>.json` com `words[{text,start,end,type}]`.
- Chave em `tools/video-use/.env` (`ELEVENLABS_API_KEY=`). Se vazia, pedir ao usuário que preencha ele mesmo.
- Ler as palavras com `scripts/words_pauses.py <pasta transcripts>` (marca pausas `|0.38|`).
- O Scribe erra nomes: "Avantnel"/"Vantoneo" → "Avant Neo"; "segue anexo" → "segue a Nexo". Corrigir na
  transcrição do corte (`cut_transcript.py --fix`).

## 2. Decidir os trechos (agressividade alta — o usuário definiu, não pedir confirmação)
- **Pausas** ≥ ~0,15 s entre frases viram corte (se o visual permitir). Respiro: 30 ms antes, 50 ms depois da fala.
- **Vícios**: "é…", "éé", "hã", "ãh", "hum", "tipo", "né" de muleta, "É," solto no começo de frase.
- **Falsos começos e repetições**: ficar com a **última versão completa** (normalmente a corrigida), salvo se
  pior. Ex.: fim de um clipe "Pronto, agora que já está instalada, vamo partir pra configuração" e começo do
  seguinte "Pronto, agora partindo pra configuração" → manter só uma.
- Corte sempre em fronteira de palavra. Contagens faladas ("uma, duas, três") ficam em cortes secos.
- Só perguntar se a decisão de conteúdo for realmente ambígua.

## 3. Demonstrações e b-roll (tutoriais)
- Silêncio **com ação na tela** (desrosquear, app carregando, lâmpada piscando) NÃO é cortado: acelerar 2–3×
  (trecho com `speed` e `gain 0.35` no build_cut). Na etapa 2 leva selo de velocidade.
- B-roll do resultado: 2×, **sem áudio** (`gain 0`), logo depois da frase que o apresenta ("E esse foi o resultado").
- Nunca trocar demonstração real por IA num tutorial (a lâmpada/a tela do app seriam inventadas).

## 4. Transições gravadas na câmera
O usuário grava transições: vira o rosto no fim de um clipe e no começo do outro, sai andando de quadro,
aproxima um produto da lente e afasta no clipe seguinte. Corte apertado destrói isso.
- Antes de apertar: `scripts\py.ps1 seams <pasta> <out> --clips A.MOV B.MOV ...` e olhar fim de A ao lado do começo de B.
- Manter o movimento no corte e reforçar na etapa 2: giro/saída → desfoque ~0,1 s antes e ~0,18 s depois +
  whoosh; produto aproxima/afasta → o plano B começa ampliado sobre o produto e abre em ~0,6 s.

## 5. Gerar o corte
Escrever `edit/ranges.json` (formato no cabeçalho de `scripts/build_cut.py`; `a`/`b` = início da 1ª e fim
da última palavra do trecho) e rodar:
```
python <skill>/scripts/build_cut.py edit/ranges.json edit
```
Gera `edit/cut.mp4` + `edit/segments.json`. 4K HDR leva alguns minutos (tone-map); `--reuse` reaproveita
trechos já extraídos se só mudou a montagem. Depois:
```
python <skill>/scripts/cut_transcript.py edit/segments.json edit/transcripts hf/transcript.json --fix "Avantnel=Avant Neo"
```
Fonte horizontal para Reels: o reenquadramento 9:16 é feito na etapa 2 (ver formatos.md), não aqui.

## 6. Conferir a sincronia (antes de seguir)
`uv run --with numpy python <skill>/scripts/check_sync.py source edit/segments.json` — cada trecho deve dar
áudio ~0 ms e imagem dentro de ±33 ms. Se algo passar de 1 quadro, investigar antes da etapa 2.

## 7. Por que não o render.py
O `tools/video-use/helpers/render.py` extrai cada trecho já em AAC e emenda com `-c copy`: o atraso inicial do
AAC e o arredondamento de quadro se acumulam a cada emenda. No tutorial da lâmpada (53 trechos) a voz saiu
visivelmente fora da boca e o usuário ficou bem frustrado. Para vídeos com poucos trechos ele até serve, mas o
build_cut é o padrão.
