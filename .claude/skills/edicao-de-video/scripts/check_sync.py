"""Confere sincronia de voz e imagem. Rodar com numpy: `uv run --with numpy python check_sync.py ...`

Modos:
  render <final.mp4> <base.mp4> [--shift-at T --shift D]
      Compara o vídeo renderizado com o vídeo base que entrou na composição: áudio (envelope de fala,
      decodificado de uma vez, sem seek) e imagem (miniatura cinza) a cada poucos segundos, do começo
      ao fim. Tudo deve dar 0 ms / 0 quadros (diferença pontual de imagem = texto por cima, normal).
      --shift-at/--shift: se o final tem um clipe encaixado (vinheta) que a base não tem.
  source <segments.json>
      Compara o cut.mp4 com os brutos, trecho a trecho (áudio por correlação, imagem por casamento
      de quadro). Diferença aceitável: até 1 quadro (33 ms). O 1º trecho de cada arquivo pode dar
      falso alarme quando começa no segundo 0.

Por que não usar `-ss` por janela: o seek no AAC dá offsets falsos; decodificar inteiro é confiável.
"""
import json, subprocess, sys
import sys as _sys; _sys.stdout.reconfigure(encoding="utf-8"); _sys.stderr.reconfigure(encoding="utf-8")
from pathlib import Path
import numpy as np

TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")


def env(args):
    b = subprocess.run(["ffmpeg", "-v", "error"] + args + ["-vn", "-ac", "1", "-ar", "16000", "-af", "highpass=f=200,lowpass=f=3000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(b, np.int16).astype(float)
    return np.sqrt(np.convolve(x * x, np.ones(16) / 16, "same"))[::16]  # 1 kHz


def frames(args, vf="", size=(64, 36)):
    w, h = size
    b = subprocess.run(["ffmpeg", "-v", "error"] + args + ["-vf", vf + f"fps=30,scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    x = np.frombuffer(b, np.uint8).reshape(-1, w * h).astype(float)
    x = x - x.mean(1, keepdims=True)
    return x / (x.std(1, keepdims=True) + 1e-6)


def corr(a, b):
    n = min(len(a), len(b))
    if n < 50 or a[:n].std() == 0 or b[:n].std() == 0:
        return -1
    return float(np.corrcoef(a[:n], b[:n])[0, 1])


def mode_render(final, base, shift_at=None, shift=0.0):
    fa, ba = env(["-i", final]), env(["-i", base])
    fv, bv = frames(["-i", final]), frames(["-i", base])
    dur = len(ba) / 1000
    for t in np.arange(2, dur - 3, max(4, dur / 25)):
        tf = t + shift if shift_at is not None and t >= shift_at else t
        i, j = int(t * 1000), int(round(tf * 1000))
        y = ba[i:i + 2000]
        c, L = max((corr(fa[j + L:j + L + 2000], y), L) for L in range(-300, 301, 2) if j + L >= 0)
        f, g = round(t * 30), round(tf * 30)
        e, V = min((float(np.abs(fv[g + k:g + k + 30] - bv[f:f + 30]).mean()), k) for k in range(-6, 7) if g + k >= 0 and g + k + 30 <= len(fv))
        flag = "" if (abs(L) <= 20 and V == 0) or c < 0.5 else "   <-- conferir"
        print(f"{t:7.1f}s  áudio {L:+4d} ms (r {c:.2f})  imagem {V:+d} quadros{flag}")


def mode_source(seg_json):
    cfg = json.load(open(seg_json, encoding="utf-8"))
    cut = str(Path(seg_json).parent / "cut.mp4")
    for s in cfg["segments"]:
        if s["speed"] != 1 or s["t1"] - s["t0"] < 1.0:
            continue
        src = str(Path(cfg["src_dir"]) / (s["src"] + cfg.get("src_ext", ".MOV")))
        d = min(2.0, s["t1"] - s["t0"] - 0.3)
        A = env(["-ss", f"{s['t0'] + 0.15:.3f}", "-i", cut, "-t", f"{d:.3f}"])
        B = env(["-ss", f"{max(0, s['s0'] - 0.05):.3f}", "-i", src, "-t", f"{d + 0.4:.3f}"])
        la = max((corr(A, B[k:k + len(A)]), k) for k in range(0, len(B) - len(A)))
        F = frames(["-ss", f"{s['t0'] + 0.15:.3f}", "-i", cut, "-t", f"{d:.3f}"], size=(96, 54))
        G = frames(["-ss", f"{max(0, s['s0'] - 0.05):.3f}", "-i", src, "-t", f"{d + 0.4:.3f}"], TONEMAP, size=(96, 54))
        lv = np.median([int((G @ F[j] / F.shape[1]).argmax()) - j for j in range(0, len(F), 5)]) / 30
        a_ms = (la[1] / 1000 - 0.2) * 1000
        v_ms = (lv - 0.2) * 1000
        print(f"trecho {s['i']:2d} {s['src']} @ {s['t0']:6.2f}s  áudio {a_ms:+5.0f} ms  imagem {v_ms:+5.0f} ms  A-V {a_ms - v_ms:+4.0f} ms")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "render":
        sa = float(sys.argv[sys.argv.index("--shift-at") + 1]) if "--shift-at" in sys.argv else None
        sh = float(sys.argv[sys.argv.index("--shift") + 1]) if "--shift" in sys.argv else 0.0
        mode_render(sys.argv[2], sys.argv[3], sa, sh)
    elif len(sys.argv) == 3 and sys.argv[1] == "source":
        mode_source(sys.argv[2])
    else:
        sys.exit(__doc__)
