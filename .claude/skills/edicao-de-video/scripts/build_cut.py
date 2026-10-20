"""Monta o corte (cut.mp4) a partir de uma lista de trechos, com sincronia exata de voz e imagem.

Por que existe: emendar trechos já codificados em AAC (como o render.py do video-use faz) acumula o
atraso inicial do AAC e o arredondamento de quadro a cada emenda — com dezenas de trechos a voz escorrega
visivelmente. Aqui cada trecho sai com N quadros de vídeo e exatamente N * (48000/fps) amostras de áudio;
o vídeo é emendado com `-c copy` e o áudio é emendado em PCM e codificado em AAC uma única vez.

Entrada (JSON):
{
  "fps": 30,                       # opcional (padrão 30)
  "src_dir": "C:/.../videos/meu-video",   # onde estão os brutos
  "src_ext": ".MOV",               # opcional (padrão .MOV)
  "pre": 0.03, "post": 0.05,       # respiro antes/depois da fala (opcional)
  "width": 1920,                   # largura de saída (1080 para vertical já na fonte)
  "ranges": [
    {"src": "IMG_3751", "a": 0.00, "b": 1.74, "label": "Fala pessoal..."},          # fala: a/b = 1ª/última palavra
    {"src": "IMG_3754", "a": 9.13, "b": 14.31, "speed": 3, "gain": 0.35, "label": "(desrosqueando 3x)"},
    {"src": "IMG_3758", "a": 0.5, "b": 10.0, "speed": 2, "gain": 0, "label": "(b-roll mudo)"}
  ]
}
Trechos com speed 1 recebem o respiro e são alinhados à grade de quadros; acelerados usam a/b crus.
Fontes HDR (HLG/PQ do iPhone) recebem tone-map para SDR automaticamente.

Saída em <out_dir>: segs/ (trechos), cut.mp4, segments.json (t0/t1 de cada trecho no corte).
uso: python build_cut.py ranges.json <out_dir> [--reuse] [--workers 4]
"""
import argparse, json, math, subprocess, sys
import sys as _sys; _sys.stdout.reconfigure(encoding="utf-8"); _sys.stderr.reconfigure(encoding="utf-8")
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SR = 48000
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg falhou: {' '.join(map(str, cmd))}\n{r.stderr[-2000:]}")


def probe(args):
    return subprocess.check_output(["ffprobe", "-v", "error"] + args).decode().strip().strip(",")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ranges", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--reuse", action="store_true", help="não reextrai trechos que já existem")
    ap.add_argument("--workers", type=int, default=4)
    o = ap.parse_args()
    cfg = json.loads(o.ranges.read_text(encoding="utf-8"))
    fps = int(cfg.get("fps", 30)); spf = SR // fps
    pre, post = cfg.get("pre", 0.03), cfg.get("post", 0.05)
    src_dir, ext, width = Path(cfg["src_dir"]), cfg.get("src_ext", ".MOV"), int(cfg.get("width", 1920))
    segdir = o.out / "segs"; segdir.mkdir(parents=True, exist_ok=True)
    hdr = {}

    segs = []
    for i, r in enumerate(cfg["ranges"]):
        sp = r.get("speed", 1)
        if sp == 1:
            s0 = max(0.0, math.floor((r["a"] - pre) * fps) / fps)
            s1 = math.ceil((r["b"] + post) * fps) / fps
            n = round((s1 - s0) * fps)
        else:
            s0, s1 = r["a"], r["b"]
            n = round((s1 - s0) / sp * fps)
        segs.append(dict(i=i, src=r["src"], s0=round(s0, 4), s1=round(s1, 4), speed=sp, gain=r.get("gain", 1.0 if sp == 1 else 0.35),
                         frames=n, label=r.get("label", "")))

    def is_hdr(src):
        if src not in hdr:
            t = probe(["-select_streams", "v:0", "-show_entries", "stream=color_transfer", "-of", "csv=p=0", str(src_dir / (src + ext))])
            hdr[src] = t in ("arib-std-b67", "smpte2084")
        return hdr[src]

    def extract(s):
        src = src_dir / (s["src"] + ext)
        v, a = segdir / f"v{s['i']:02d}.mp4", segdir / f"a{s['i']:02d}.wav"
        if o.reuse and v.exists() and a.exists():
            return
        sp, n = s["speed"], s["frames"]
        dsrc = n / fps * sp + 0.5
        vf = (TONEMAP + "," if is_hdr(s["src"]) else "") + f"scale={width}:-2,setpts=(PTS-STARTPTS)/{sp},fps={fps},tpad=stop_mode=clone:stop_duration=2"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['s0']:.4f}", "-t", f"{dsrc:.4f}", "-i", str(src), "-an", "-vf", vf,
             "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
             "-r", str(fps), "-g", str(fps), "-keyint_min", str(fps), str(v)])
        ns = n * spf
        if s["gain"] == 0:
            af = f"volume=0,aresample={SR},apad,atrim=end_sample={ns}"
        else:
            tempo, left = [], sp
            while left > 2.0:
                tempo.append("atempo=2.0"); left /= 2.0
            if sp != 1:
                tempo.append(f"atempo={left}")
            chain = ",".join(tempo + [f"volume={s['gain']}"])
            af = f"{chain},aresample={SR},apad,atrim=end_sample={ns},afade=t=in:d=0.012,afade=t=out:st={ns / SR - 0.012:.4f}:d=0.012"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['s0']:.4f}", "-t", f"{dsrc:.4f}", "-i", str(src), "-vn",
             "-af", af, "-ac", "2", "-ar", str(SR), "-c:a", "pcm_s16le", str(a)])
        print("ok", s["i"], s["label"][:40], flush=True)

    with ThreadPoolExecutor(o.workers) as ex:
        list(ex.map(extract, segs))

    t = 0.0
    for s in segs:
        nf = int(probe(["-count_packets", "-select_streams", "v", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(segdir / f"v{s['i']:02d}.mp4")]))
        ns = int(probe(["-select_streams", "a", "-show_entries", "stream=duration_ts", "-of", "csv=p=0", str(segdir / f"a{s['i']:02d}.wav")]))
        if nf != s["frames"] or ns != s["frames"] * spf:
            sys.exit(f"trecho {s['i']} com tamanho errado: {nf} quadros / {ns} amostras (esperado {s['frames']} / {s['frames'] * spf})")
        s["t0"] = round(t, 4); t += s["frames"] / fps; s["t1"] = round(t, 4)
    (segdir / "v.txt").write_text("".join(f"file 'v{s['i']:02d}.mp4'\n" for s in segs))
    (segdir / "a.txt").write_text("".join(f"file 'a{s['i']:02d}.wav'\n" for s in segs))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(segdir / "v.txt"), "-c", "copy", str(segdir / "video.mp4")])
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(segdir / "a.txt"), "-c", "copy", str(segdir / "audio.wav")])
    run(["ffmpeg", "-v", "error", "-y", "-i", str(segdir / "video.mp4"), "-i", str(segdir / "audio.wav"), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(o.out / "cut.mp4")])
    json.dump(dict(fps=fps, src_dir=str(src_dir), src_ext=ext, segments=segs), open(o.out / "segments.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"cut.mp4: {t:.3f}s em {len(segs)} trechos")


if __name__ == "__main__":
    main()
