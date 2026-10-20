"""Encaixa um clipe (ex.: a vinheta da Nexo) dentro de um vídeo, num ponto exato, num arquivo contínuo.

Por que existe: dividir o vídeo em dois <video> com data-media-start no HyperFrames atrasou a voz
~0,1–0,2 s depois do encaixe. Aqui tudo vira um vídeo base único; corte por quadro (end_frame) e por
amostra (end_sample), então voz e imagem continuam presas.

uso: python splice_clip.py <base.mp4> <clipe.mp4> <em_segundos> <saida.mp4> [--fps 30]
  <em_segundos> é arredondado para o quadro mais próximo; escolha um ponto de silêncio entre frases
  (de preferência uma emenda do corte, ex.: o fim do trecho "bora pro vídeo!").
Depois do encaixe, tudo o que vinha depois desse ponto anda a duração do clipe.
"""
import argparse, subprocess
import sys as _sys; _sys.stdout.reconfigure(encoding="utf-8"); _sys.stderr.reconfigure(encoding="utf-8")

SR = 48000

ap = argparse.ArgumentParser()
ap.add_argument("base"); ap.add_argument("clip"); ap.add_argument("at", type=float); ap.add_argument("out")
ap.add_argument("--fps", type=int, default=30)
o = ap.parse_args()
fr = round(o.at * o.fps)
smp = fr * (SR // o.fps)
nclip = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries",
                                     "stream=nb_read_packets", "-of", "csv=p=0", o.clip]).decode().strip().strip(","))
cs = nclip * (SR // o.fps)
fc = (f"[0:v]trim=end_frame={fr},setpts=PTS-STARTPTS[a];[0:a]aresample={SR},atrim=end_sample={smp},asetpts=PTS-STARTPTS[aa];"
      f"[1:v]fps={o.fps},trim=end_frame={nclip},setpts=PTS-STARTPTS[b];[1:a]aresample={SR},apad,atrim=end_sample={cs},asetpts=PTS-STARTPTS[ba];"
      f"[0:v]trim=start_frame={fr},setpts=PTS-STARTPTS[c];[0:a]aresample={SR},atrim=start_sample={smp},asetpts=PTS-STARTPTS[ca];"
      f"[a][aa][b][ba][c][ca]concat=n=3:v=1:a=1[v][au]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", o.base, "-i", o.clip, "-filter_complex", fc, "-map", "[v]", "-map", "[au]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-r", str(o.fps), "-g", str(o.fps),
                "-keyint_min", str(o.fps), "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", o.out], check=True)
print(f"clipe de {nclip / o.fps:.3f}s encaixado em {fr / o.fps:.4f}s → {o.out}")
