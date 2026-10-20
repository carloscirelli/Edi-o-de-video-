# Trilha ambiente original: pad (Am–F–C–G) + baixo + pulso suave, 96 bpm.
import sys, numpy as np, soundfile as sf
dur, out = float(sys.argv[1]), sys.argv[2]
sr = 44100; n = int(dur * sr); t = np.arange(n) / sr
bpm = 96; beat = 60 / bpm; bar = beat * 4
f = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]
bass = [45, 41, 48, 43]
y = np.zeros(n); rng = np.random.default_rng(7)
for i in range(int(dur / bar) + 1):
    s, e = int(i * bar * sr), min(int((i + 1) * bar * sr + sr * 0.6), n)
    if s >= n: break
    tt = t[s:e] - t[s]; env = np.minimum(1, tt / 0.8) * np.exp(-np.maximum(0, tt - bar) * 4)
    c = chords[i % 4]
    for m in c:
        for det in (-0.06, 0.06):
            y[s:e] += 0.05 * env * np.sin(2 * np.pi * f(m + det) * tt + rng.random() * 6)
    y[s:e] += 0.12 * env * np.sin(2 * np.pi * f(bass[i % 4] - 12) * tt)
    for b in range(8):  # pulso em colcheias (arpejo)
        bs = s + int(b * beat / 2 * sr); be = min(bs + int(0.35 * sr), n)
        if bs >= n: break
        tb = t[bs:be] - t[bs]; m = c[b % 4] + 12
        y[bs:be] += 0.035 * np.exp(-tb * 9) * np.sin(2 * np.pi * f(m) * tb)
    for b in range(4):  # kick leve
        ks = s + int(b * beat * sr); ke = min(ks + int(0.25 * sr), n)
        if ks >= n: break
        tk = t[ks:ke] - t[ks]
        y[ks:ke] += 0.22 * np.exp(-tk * 18) * np.sin(2 * np.pi * (50 + 90 * np.exp(-tk * 30)) * tk)
# reverb simples
for d, g in ((0.11, 0.3), (0.23, 0.2), (0.37, 0.12)):
    k = int(d * sr); y[k:] += g * y[:-k]
y *= np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5)
y = y / np.abs(y).max() * 0.8
sf.write(out, np.stack([y, y], 1).astype(np.float32), sr)
print(out, dur)
