"""Lista as palavras do Scribe com tempos e marca as pausas — é o que se lê para decidir os cortes.

uso: python words_pauses.py <pasta com transcripts/*.json> [--gap 0.25]
Saída por clipe:  Fala@0.00-0.12 pessoal,@0.16-0.52 |0.38| Sejam@2.12-2.34 ...
  |x.xx| = pausa maior que --gap (candidata a corte).
"""
import argparse, json
import sys as _sys; _sys.stdout.reconfigure(encoding="utf-8"); _sys.stderr.reconfigure(encoding="utf-8")
from pathlib import Path

ap = argparse.ArgumentParser(); ap.add_argument("dir", type=Path); ap.add_argument("--gap", type=float, default=0.25)
o = ap.parse_args()
for f in sorted(o.dir.glob("*.json")):
    ws = [w for w in json.loads(f.read_text(encoding="utf-8"))["words"] if w.get("type") != "spacing"]
    out, prev = [], None
    for w in ws:
        if prev is not None and w["start"] - prev > o.gap:
            out.append(f"|{w['start'] - prev:.2f}|")
        out.append(f"{w['text']}@{w['start']:.2f}-{w['end']:.2f}")
        prev = w["end"]
    print("##", f.stem); print(" ".join(out)); print()
