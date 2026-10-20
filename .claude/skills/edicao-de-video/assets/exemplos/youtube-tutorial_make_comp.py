"""Gera hf-v2/index.html a partir de hf-tipo/index.html (mesma edição) para o corte novo (edit_v2).

Tempos do template estão no corte antigo; um mapa palavra a palavra (knots.json) converte para o
corte novo, e tudo depois do "bora pro vídeo!" anda mais 4,6 s (vinheta). Música mais baixa.
"""
import bisect, json, re, subprocess

D = 'C:/Users/lscir/Edição de video/videos/nexo-lampada-avant/'
h = open(D + 'hf-tipo/index.html', encoding='utf-8').read()
knots = json.load(open(D + 'hf-v2/knots.json'))
OLD_END, NEW_END, P, V, END_CARD = 106.66, 106.7333, 23.9333, 4.6, 3.54
K = sorted(set((round(a, 4), round(b, 4)) for a, b in [(0.0, 0.0)] + knots + [(OLD_END, NEW_END), (110.2, NEW_END + END_CARD)]))
xs = [a for a, _ in K]; ys = [b for _, b in K]


def m(s):
    i = bisect.bisect_right(xs, s) - 1
    if i < 0: return s
    if i >= len(xs) - 1: return ys[-1] + (s - xs[-1])
    x0, x1, y0, y1 = xs[i], xs[i + 1], ys[i], ys[i + 1]
    return y0 + (s - x0) * (y1 - y0) / (x1 - x0) if x1 > x0 else y0


def T(s):
    return m(s) + V if s >= 24.0 - 1e-6 else m(s)


TOTAL = round(NEW_END + V + END_CARD, 4)


def rep(a, b):
    global h
    assert a in h, a[:80]
    h = h.replace(a, b)


rep('data-composition-id="youtube" data-start="0" data-duration="114.8"', f'data-composition-id="youtube" data-start="0" data-duration="{TOTAL}"')
h = re.sub(r'<video id="bg-video" src="input-com-vinheta.mp4"[^>]*></video>',
           f'<video id="bg-video" src="base-com-vinheta.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{round(NEW_END + V, 4)}" data-track-index="1"></video>', h)
rep('<div class="clip" id="fx" data-start="0" data-duration="114.8"', f'<div class="clip" id="fx" data-start="0" data-duration="{TOTAL}"')
rep('<div id="end" class="clip" data-start="111.26" data-duration="3.54"', f'<div id="end" class="clip" data-start="{round(NEW_END + V, 4)}" data-duration="{END_CARD}"')

js_k = json.dumps([[a, b] for a, b in K])
rep('      const T = (s) => (s >= 24.0 ? s + 4.6 : s);',
    f'''      // re-edição v2: tempos escritos no corte antigo → corte novo (mapa palavra a palavra) + vinheta de {V} s
      const K = {js_k};
      const M = (s) => {{ let lo = 0, hi = K.length - 1; if (s <= K[0][0]) return s; if (s >= K[hi][0]) return K[hi][1] + (s - K[hi][0]);
        while (hi - lo > 1) {{ const mid = (lo + hi) >> 1; if (K[mid][0] <= s) lo = mid; else hi = mid; }}
        const [x0, y0] = K[lo], [x1, y1] = K[hi]; return x1 > x0 ? y0 + (s - x0) * (y1 - y0) / (x1 - x0) : y0; }};
      const T = (s) => (s >= 24.0 ? M(s) + {V} : M(s));''')
rep('tl.set("#wm", { opacity: 0 }, 24.0); tl.set("#wm", { opacity: 0.75 }, 28.6);',
    f'tl.set("#wm", {{ opacity: 0 }}, {P}); tl.set("#wm", {{ opacity: 0.75 }}, {round(P + V, 4)});')
rep('tl.set("#shade", { opacity: 0 }, 24.0); tl.set("#shade", { opacity: 1 }, 28.6);',
    f'tl.set("#shade", {{ opacity: 0 }}, {P}); tl.set("#shade", {{ opacity: 1 }}, {round(P + V, 4)});')

# selos de velocidade: tempos exatos dos trechos acelerados no corte novo
seg = json.load(open(D + 'edit_v2/segments.json', encoding='utf-8'))['segments']
sp = [(s['t0'] + V, s['t1'] + V, f"{s['speed']}×") for s in seg if s['speed'] != 1]
old_list = re.search(r'\[\[32\.1, 33\.83, "3×"\].*?\]\]', h).group(0)
h = h.replace(old_list, '[' + ', '.join(f'[{a:.4f}, {b:.4f}, "{c}"]' for a, b, c in sp) + ']')
rep('{ opacity: 1, x: 0, duration: 0.25, ease: "power3.out", immediateRender: false }, q(a));',
    '{ opacity: 1, x: 0, duration: 0.25, ease: "power3.out", immediateRender: false }, Math.round(a * 30) / 30);')
rep('tl.to(sp, { opacity: 0, x: 30, duration: 0.18 }, q(b - 0.18));', 'tl.to(sp, { opacity: 0, x: 30, duration: 0.18 }, Math.round((b - 0.18) * 30) / 30);')

# efeitos sonoros (tempos do corte antigo → novo); sem o whoosh por cima do "fui"
cues = [(1.42, 'pop', .25), (4.0, 'whoosh-short', .3), (7.74, 'whoosh-short', .3), (10.78, 'pop', .3), (11.32, 'impact-bass-1', .4), (11.9, 'sparkle', .3),
        (14.16, 'pop', .3), (15.6, 'pop', .3), (18.96, 'pop', .3), (20.26, 'whoosh-short', .2), (21.8, 'click-soft', .25), (22.1, 'click-soft', .25),
        (22.4, 'click-soft', .25), (22.98, 'whoosh', .35)]
for t in [24.8, 33.86, 43.7, 56.23, 74.94, 91.1]:
    cues += [(t, 'whoosh', .35), (t + 0.05, 'impact-bass-1', .3)]
cues += [(29.1, 'click', .35), (31.27, 'whoosh-short', .25), (36.31, 'whoosh-short', .2), (37.67, 'whoosh-short', .25), (42.54, 'ping', .3),
         (46.34, 'impact-bass-1', .3), (48.5, 'whoosh-short', .2), (49.96, 'click', .4), (50.26, 'click', .4), (50.83, 'click', .4),
         (53.11, 'whoosh-short', .2), (55.35, 'ping', .3), (57.65, 'pop', .3), (60.75, 'pop', .28), (63.74, 'pop', .28), (67.35, 'ping', .28),
         (68.66, 'whoosh-short', .2), (71.67, 'impact-bass-1', .3), (73.31, 'click', .4), (77.02, 'whoosh-short', .2), (77.46, 'pop', .28),
         (80.18, 'pop', .28), (81.75, 'pop', .28), (84.25, 'pop', .28), (84.9, 'pop', .28), (86.56, 'impact-bass-1', .3), (88.34, 'sparkle', .3),
         (96.93, 'whoosh-short', .25), (100.12, 'pop', .3), (101.92, 'pop', .3), (102.7, 'pop', .3), (103.5, 'pop', .3), (106.7, 'whoosh', .35),
         (107.5, 'chime', .35)]
cues = sorted((round(round(T(t) * 30) / 30, 4), n, v) for t, n, v in cues)
dur = {n: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', D + f'hf-v2/sfx/{n}.mp3']).decode().strip())
       for n in set(c[1] for c in cues)}
lines = [f'  <audio id="sfx{i:02d}" src="sfx/{n}.mp3" data-start="{t:.4f}" data-duration="{min(dur[n], TOTAL - t):.2f}" data-track-index="{10 + i % 6}" data-volume="{v}"></audio>'
         for i, (t, n, v) in enumerate(cues)]
h = re.sub(r'  <!-- SFX:BEGIN -->.*?<!-- SFX:END -->', lambda _: '  <!-- SFX:BEGIN -->\n' + '\n'.join(lines) + '\n  <!-- SFX:END -->', h, flags=re.S)

# música mais baixa: 0.08 sob a fala (antes 0.14), 0.28 sem fala (antes 0.5), 0.35 na tela final; muda durante a vinheta
new = json.load(open(D + 'hf-v2/transcript.json', encoding='utf-8'))
LO, HI = 0.08, 0.28


def bed(t_from, t_to):
    gaps, prev = [], t_from
    for w in new:
        if w['end'] <= t_from or w['start'] >= t_to: continue
        if w['start'] - prev > 0.9: gaps.append((prev, w['start']))
        prev = max(prev, w['end'])
    if t_to - prev > 0.9: gaps.append((prev, t_to))
    pts = [(0.0, LO)]
    for g0, g1 in gaps:
        a0, a1 = max(g0 - t_from, 0.0), g1 - t_from
        pts += [(a0 + 0.1, LO), (a0 + 0.45, HI), (a1 - 0.45, HI), (a1 - 0.1, LO)]
    return pts


p1 = sorted(set((round(a, 3), v) for a, v in bed(0.0, P) + [(P - 0.3, LO), (P, 0.0)] if 0 <= a <= P))
p2 = [(0.0, 0.0), (0.4, LO)] + [(round(a, 3), v) for a, v in bed(P, NEW_END)[1:] if a > 0.4]
p2 += [(round(NEW_END - P - 0.05, 3), LO), (round(NEW_END - P + 0.3, 3), 0.35), (round(NEW_END - P + END_CARD, 3), 0.35)]
auto = lambda L: json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": a, "v": v} for a, v in L]}]}, separators=(',', ':'))
music = (f'''  <audio id="bgm" src="music/bgm.wav" data-start="0" data-duration="{P}" data-media-start="0" data-track-index="9" data-automation='{auto(p1)}'></audio>\n'''
         f'''  <audio id="bgm-2" src="music/bgm.wav" data-start="{round(P + V, 4)}" data-duration="{round(TOTAL - P - V, 4)}" data-media-start="{P}" data-track-index="9" data-automation='{auto(p2)}'></audio>''')
h, n = re.subn(r'  <audio id="bgm" [^\n]*\n  <audio id="bgm-2" [^\n]*', lambda _: music, h)
assert n == 1
open(D + 'hf-v2/index.html', 'w', encoding='utf-8').write(h)
print('total', TOTAL, 'sfx', len(lines), 'T(24.8)=', round(T(24.8), 3), 'T(106.3)=', round(T(106.3), 3))
