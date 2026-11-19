import sys, os, time
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d18')
import jimo as J
import bpy
from PIL import Image, ImageDraw
# usage: look.py loc LIGHT out.jpg name:x,y,z,lx,ly,lz,lens ...   (or name only = shot camera start)
loc, light, out = sys.argv[1:4]; specs = sys.argv[4:]
A = J.build(loc, loc, light); sc = bpy.context.scene
J.MN.setup_render(sc, 'preview'); sc.cycles.samples = 6; sc.render.threads = 2
tiles = []
for sp in specs:
    nm, _, v = sp.partition(':'); v = [float(x) for x in v.split(',')]
    cam = dict(loc=tuple(v[0:3]), look_at=tuple(v[3:6]), lens=v[6]); J.make_camera(cam)
    p = '/tmp/claude-0/look_%s.png' % nm; J.T.render(p); tiles.append((nm, Image.open(p).convert('RGB')))
W, H = tiles[0][1].size; sheet = Image.new('RGB', (W * len(tiles), H + 16), (20, 20, 30)); d = ImageDraw.Draw(sheet)
for i, (nm, im) in enumerate(tiles): sheet.paste(im, (i * W, 0)); d.text((i * W + 4, H + 2), nm, fill=(255, 255, 255))
sheet.save(out, quality=88)
