# Reels New Sistemas × ELAN (33 s, 9:16) — v2: animação em tela cheia (sem mockup de notebook)
Montar para render: copiar `fonts/` e `vendor/gsap.min.js` da skill, `sfx/` do media-use (`~/.claude/skills/media-use/audio/assets/sfx`)
e gerar a trilha: `python -I .claude/skills/edicao-de-video/scripts/music_ambient.py 33 music/bgm.wav`.
Voz: `vo/lines.json` → `scripts/tts_kokoro.py` → `vo/vo.wav` + `vo/vo.json` (tempos usados em `LINES` no index.html).
Render: `hyperframes render . -o elan_reels.mp4`, depois loudnorm −14 LUFS.
