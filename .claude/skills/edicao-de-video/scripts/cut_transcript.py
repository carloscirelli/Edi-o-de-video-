"""Gera a transcrição palavra a palavra no tempo do cut.mp4 (para legendas e para sincronizar textos).

uso: python cut_transcript.py <segments.json> <pasta transcripts/> <saida transcript.json> [--fix "Avantnel=Avant Neo" ...]
  Usa só os trechos de fala (speed 1). Cada palavra: {"text","start","end"} no tempo do corte.
  --fix corrige palavras que o Scribe erra (marcas, nomes): "errado=certo".
"""
import argparse, json
import sys as _sys; _sys.stdout.reconfigure(encoding="utf-8"); _sys.stderr.reconfigure(encoding="utf-8")
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("segments", type=Path); ap.add_argument("tdir", type=Path); ap.add_argument("out", type=Path)
ap.add_argument("--fix", action="append", default=[])
o = ap.parse_args()
fixes = [f.split("=", 1) for f in o.fix]
segs = json.loads(o.segments.read_text(encoding="utf-8"))["segments"]
cache, words = {}, []
for s in segs:
    if s["speed"] != 1:
        continue
    if s["src"] not in cache:
        cache[s["src"]] = json.loads((o.tdir / f"{s['src']}.json").read_text(encoding="utf-8"))["words"]
    for w in cache[s["src"]]:
        if w.get("type") != "word" or w["start"] < s["s0"] - 1e-3 or w["end"] > s["s1"] + 1e-3:
            continue
        t = w["text"]
        for a, b in fixes:
            t = t.replace(a, b)
        words.append({"text": t, "start": round(s["t0"] + w["start"] - s["s0"], 3), "end": round(s["t0"] + w["end"] - s["s0"], 3)})
o.out.write_text(json.dumps(words, ensure_ascii=False, indent=0), encoding="utf-8")
print(len(words), "palavras →", o.out)
