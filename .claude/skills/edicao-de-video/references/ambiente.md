# Ambiente (Windows do usuário)

## Pastas
- Projeto: `C:\Users\lscir\Edição de video\` — `CLAUDE.md` (regras do projeto), `videos/<nome>/` (um por vídeo),
  `Resultados/` (todas as entregas), `referencias/` (vídeos de referência + folhas de contato), `scripts/`, `tools/`.
- Por vídeo: brutos intocados na raiz, `edit/` (transcripts, ranges.json, segs/, cut.mp4, segments.json),
  `hf/` ou `hf-<versão>/` (composição: index.html, fonts/, sfx/, music/, vendor/gsap.min.js, vídeo base).
- Se o usuário mandar um arquivo de fora, copiar para `videos/<nome-curto-sem-espaços>/` antes de começar.

## Ferramentas
- FFmpeg 9 (gyan full, com zscale/tonemap), Node 24, Python 3.12, uv, yt-dlp, Git.
- HyperFrames CLI: `npx -y hyperframes lint|snapshot|render <pasta>`; clone em `tools/hyperframes` e plugin
  `hyperframes` no Claude Code (skills `hyperframes:*`). `snapshot --at 1.5,3.0 --no-end -o snaps` gera PNGs e
  folhas de contato para conferir; `render . -o saida.mp4 --quiet`.
- video-use (`tools/video-use`, Scribe/ElevenLabs) via `scripts\vu.ps1 <helper> [args]` (transcribe,
  transcribe_batch, pack_transcripts, timeline_view, render, grade). Patch local no render.py (legenda `as_posix()`).
- Scripts do projeto via `scripts\py.ps1 <nome> [args]` (ambiente do video-use): ambient, music_bed, sfx, seams,
  segments, retime, captions, fix_words, edl_words, words, yt_subs_text, print_words; `scripts\speedup.ps1`.
- Python com numpy/pillow: `uv run --with numpy --with pillow python -I script.py`.
- Higgsfield conectado (geração de imagem/vídeo por IA, créditos pagos; conta gratuita com poucos créditos) — só
  usar se o usuário pedir e depois de dizer o custo.

## Shell
- Ferramenta Bash (Git Bash) funciona bem com caminhos `/c/Users/lscir/Edição de video/...` entre aspas.
  PowerShell 5.1: atualizar PATH antes de ffmpeg/uv
  (`$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')`),
  não usar `2>&1` em ffmpeg/uv, números com vírgula no pt-BR (escrever listas de tempos à mão).
- Gravar JSON/HTML com a ferramenta Write (UTF-8 sem BOM); `Set-Content` grava BOM.
- Python que imprime acentos: `PYTHONIOENCODING=utf-8`. Heredoc com aspas e `'''` pode quebrar o Bash — com
  scripts longos, gravar um `.py` e rodar.
- Kaspersky inspeciona HTTPS: o `vu.ps1` exporta as raízes do Windows para `tools/.certs/windows-roots.pem`
  (`REQUESTS_CA_BUNDLE`/`SSL_CERT_FILE`). Fora do wrapper, setar essas variáveis.
- Disco C: quase cheio (~24 GB livres): apagar temporários grandes que você criou (ex.: `segs/` antigos) quando
  não forem mais úteis, avisando.
