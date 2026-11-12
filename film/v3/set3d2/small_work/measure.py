"""measure.py vault|room preset cam : shade/lit ratio on the lit surfaces (key on vs key off, same frame), hue of lit and shade,
final-quality timing, written to small_work/measure_<set>_<preset>_<cam>.json"""
import sys, os, json, numpy as np, colorsys, bpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import smallkit as K
from PIL import Image
setname, preset, cam = sys.argv[1:4]
M = __import__(setname)
A = M.build(preset); sc = bpy.context.scene; K.setup_render(sc, 'preview'); sc.cycles.samples = 32
K.make_camera(A['cams'][cam]); M.stage(A, cam)
on = os.path.join(HERE, 'meas_%s_%s_on.png' % (setname, cam)); off = os.path.join(HERE, 'meas_%s_%s_off.png' % (setname, cam))
K.render(on); K.ST['key'].hide_render = True; K.render(off); K.ST['key'].hide_render = False
def lin(a): a = a / 255.0; return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
a = np.asarray(Image.open(on).convert('RGB'), float); b = np.asarray(Image.open(off).convert('RGB'), float)
la = (lin(a) * [0.2126, 0.7152, 0.0722]).sum(-1); lb = (lin(b) * [0.2126, 0.7152, 0.0722]).sum(-1)
r = la / np.maximum(lb, 1e-4) - 1
sel = sys.argv[4] if len(sys.argv) > 4 else None                 # optional region x0,y0,x1,y1 (fractions) = the one surface
mask = r > 1.2
if sel:
    x0, y0, x1, y1 = [float(v) for v in sel.split(',')]; H, W = mask.shape; reg = np.zeros_like(mask); reg[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = True; mask &= reg
ratio = lb[mask] / la[mask]
def hue(img, m): c = img[m].mean(0) / 255; h, s, v = colorsys.rgb_to_hsv(*c); return [int(h * 360), round(s, 2), round(v, 2)]
res = dict(set=setname, preset=preset, cam=cam, region=sel, lit_px=int(mask.sum()), ratio_linear_median=round(float(np.median(ratio)), 3),
           ratio_p10_p90=[round(float(np.percentile(ratio, 10)), 3), round(float(np.percentile(ratio, 90)), 3)],
           ratio_display_luma=round(float(np.median((b[mask] @ [0.299, 0.587, 0.114]) / np.maximum(a[mask] @ [0.299, 0.587, 0.114], 1))), 3),
           lit_hsv=hue(a, mask), shade_hsv_same_pixels=hue(b, mask))
print(json.dumps(res)); json.dump(res, open(os.path.join(HERE, 'measure_%s_%s_%s.json' % (setname, preset, cam)), 'w'), indent=1)
