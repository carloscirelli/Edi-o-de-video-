# Recorta fundo branco ligado à borda (flood fill), mantendo brancos internos. uso: python -I cutout_white.py <entrada> <saida.png> <limiar 30-40>
import sys
from PIL import Image, ImageDraw, ImageFilter
src, out, thr = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert("RGBA")
w, h = im.size
# flood fill a partir das bordas: só o branco ligado à borda vira transparente
mark = im.convert("RGB").copy()
KEY = (255, 0, 255)
for x in range(0, w, 4):
    for y in (0, h - 1):
        if mark.getpixel((x, y)) != KEY and min(mark.getpixel((x, y))) > 255 - thr:
            ImageDraw.floodfill(mark, (x, y), KEY, thresh=thr)
for y in range(0, h, 4):
    for x in (0, w - 1):
        if mark.getpixel((x, y)) != KEY and min(mark.getpixel((x, y))) > 255 - thr:
            ImageDraw.floodfill(mark, (x, y), KEY, thresh=thr)
a = Image.new("L", (w, h), 255)
px, pa = mark.load(), a.load()
for y in range(h):
    for x in range(w):
        if px[x, y] == KEY: pa[x, y] = 0
a = a.filter(ImageFilter.GaussianBlur(1.2))
im.putalpha(a)
bb = a.getbbox(); im = im.crop(bb)
im.save(out); print(out, im.size)
