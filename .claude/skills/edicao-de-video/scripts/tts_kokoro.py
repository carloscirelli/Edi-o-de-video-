# Narração local grátis (Kokoro, voz pm_alex pt-BR). uso: python -I tts_kokoro.py <pasta com kokoro-v1.0.onnx e voices-v1.0.bin> <pasta com lines.json>
# lines.json: [{"say": "texto (grafia fonética para marcas: Élan, Niú)", "gap": 0.35}, ...] → vo.wav + vo.json (t0/t1 por frase)
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
d, out = sys.argv[1], sys.argv[2]
k = Kokoro(d + "/kokoro-v1.0.onnx", d + "/voices-v1.0.bin")
L = json.load(open(out + "/lines.json", encoding="utf-8"))
sr = 24000; parts = []; t = 0.35; meta = []
parts.append(np.zeros(int(sr * t)))
for i, ln in enumerate(L):
    a, sr = k.create(ln["say"], voice="pm_alex", speed=1.08, lang="pt-br")
    # tira silêncio das pontas
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(nz[0] - 240, 0): nz[-1] + 480]
    meta.append({"i": i, "t0": round(t, 3), "t1": round(t + len(a) / sr, 3), "text": ln["say"]})
    parts.append(a); t += len(a) / sr
    gap = ln.get("gap", 0.35); parts.append(np.zeros(int(sr * gap))); t += gap
v = np.concatenate(parts).astype(np.float32)
sf.write(out + "/vo.wav", v, sr)
json.dump(meta, open(out + "/vo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for m in meta: print(m["t0"], m["t1"], m["text"])
print("total", round(t, 2))
