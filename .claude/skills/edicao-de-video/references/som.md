# Som: efeitos, música e volume

## Efeitos (SFX)
- Biblioteca local livre de direitos (media-use do HyperFrames): `Edição de video/tools/hyperframes/skills/media-use/audio/assets/sfx`
  (também já copiada em cada `hf/sfx/` dos exemplos): whoosh, whoosh-short, pop, click, click-soft, ping, chime,
  sparkle, impact-bass-1/2, error, notification.
- **Um efeito por evento visível**, nunca por palavra. Mapa: bloco/tela entrando → whoosh-short; troca de cena/passo →
  whoosh (+ impact-bass-1 em tela cheia); pill/card → pop; interruptor/botão/máquina de escrever → click(-soft);
  ✓ concluído → ping/chime; brilho/estrela → sparkle; "?" → error (baixo).
- Volumes 0,2–0,45. **Nunca um efeito em cima de uma palavra importante** — um whoosh sobre o "fui!" final fez o
  usuário achar que a palavra tinha sumido.
- Os `<audio id="sfxNN">` ficam entre `<!-- SFX:BEGIN -->` e `<!-- SFX:END -->`; trilhas 10–15 em rodízio.
  Alternativa: `scripts\py.ps1 sfx <cues.json> <public>` (adianta cada efeito pelo próprio ataque).

## Música
- Trilha original sintetizada, sem direitos autorais e sem download (o usuário não quer login na HeyGen):
  `scripts\py.ps1 ambient -o <hf>/music/bgm.wav --duration <dur> [--key A --bpm 100 --seed 11]`.
- **Volumes (pedido do usuário — música baixa em relação à voz):**
  | Situação | Volume |
  |---|---|
  | debaixo da fala | 0,08 |
  | trechos sem fala (acelerações, b-roll) | 0,28 |
  | tela final | 0,35 |
  | vídeo sem fala nenhuma (só motion) | ~0,5 |
  Rampas de ~0,35 s (`data-automation` com pontos `{t, v}` em segundos **do próprio clipe de áudio**).
  `scripts\py.ps1 music_bed <transcript> <public> --src music/bgm.wav --duration <dur> --merge 0.9` gera a
  automação (ajustar os níveis para os da tabela).
- Vinheta encaixada: a música desce a 0 antes dela, fica parada durante e volta suave depois (dois `<audio>`:
  `bgm` até o encaixe e `bgm-2` depois, com `data-media-start`).
- Stories: sem música.

## Volume final
- Medir com `ffmpeg -i final.mp4 -af ebur128=peak=true -f null NUL`.
- Alvo: YouTube ≈ −16 LUFS, Reels/motion ≈ −14 LUFS, pico ≤ −1,5 dB. Ajustar com
  `-c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11:linear=true` — muda o volume geral sem mudar a proporção voz/música.
- Não dá para ouvir: reportar os números ao usuário (voz sozinha vs. mistura) quando o assunto for volume.
