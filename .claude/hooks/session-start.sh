#!/bin/bash
# Prepara a sessão na nuvem para a skill edicao-de-video: HyperFrames CLI, Chrome de render e skills hyperframes-*.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

HF_VERSION=0.8.181

if [ "$(hyperframes --version 2>/dev/null || true)" != "$HF_VERSION" ]; then
  npm install -g "hyperframes@$HF_VERSION" --silent
fi

# Chrome Headless Shell usado no render (fica em ~/.cache/hyperframes)
hyperframes browser ensure >/dev/null

# O init sincroniza as skills hyperframes-* em ~/.claude/skills; o projeto descartável é apagado depois
if [ ! -f "$HOME/.claude/skills/hyperframes/SKILL.md" ]; then
  tmp=$(mktemp -d)
  (cd "$tmp" && hyperframes init sync --example blank --non-interactive >/dev/null 2>&1) || true
  rm -rf "$tmp"
fi
