"""Sheet proportion measurement for Kong / James / Khun Tos (character_sheet.webp, 1448x1086).
Segmentation: |rgb - cream(253,243,232)| > 28, connected components, hole-filled silhouettes (v2/seg.py, v2/crops.py).
Head circle fit + face features: v2/face2.py -> v2/face2.json.  Landmarks below marked (grid) were read from
5x / 3x gridded zooms (v2/*_grid3.png); all others are computed here.  Writes annotated crops + sheet_measure.json."""
import json, os, numpy as np, cv2
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.join(H, 'v2')
SRC = os.path.join(H, '..', '..', 'uploads', 'character_sheet.webp')
A = np.asarray(Image.open(SRC).convert('RGB'))
face = json.load(open(os.path.join(V2, 'face2.json')))
# landmarks in local crop px (origin = silhouette bbox top-left)
L = {
 'kong':  dict(crotch=330, belt=(283, 300), boot_top=463, glove=(20, 300, 62, 340), shoulder=(15, 183, 240),
               backpack=(1, 184), sole_w=(57, 68), head_w_meas=125, hair_low=92, hair_w=157,
               leg_w=56, forearm=(17, 23)),
 'james': dict(crotch=297, belt=(280, 290), boot_top=443, glove=(161, 110, 194, 170), shoulder=(48, 152, 170),
               backpack=(1, 184), sole_w=(56, 71), head_w_meas=110, hair_low=100, hair_w=140,
               leg_w=37, forearm=None),
 'tos':   dict(crotch=300, belt=(262, 275), boot_top=470, glove=None, shoulder=(31, 130, 170),
               backpack=None, sole_w=(55, 68), head_w_meas=123, hair_low=95, hair_w=142,
               leg_w=37, forearm=None),
}
out = {}
for k, l in L.items():
    x0, y0, x1, y1 = map(int, open(os.path.join(V2, f'{k}_box.txt')).read().split())
    sil = np.load(os.path.join(V2, f'{k}_sil.npy')); ys, xs = np.nonzero(sil)
    top, sole = int(ys.min()), int(ys.max()); Htot = sole - top + 1
    f = face[k]; D = round((f['D_outer'] + l['head_w_meas']) / 2, 1); chin = f['chin']
    skull = chin - D
    r = dict(total_h=Htot, head_D=D, head_D_fit=f['D_outer'], head_w_meas=l['head_w_meas'], chin=chin,
             head_over_total=D / Htot, head_with_hair_over_total=(chin - top) / Htot, heads_tall=Htot / D,
             hair_above_skull_over_D=(skull - top) / D, hair_extent_over_D=l['hair_low'] / D, hair_w_over_D=l['hair_w'] / D,
             shoulder_over_D=(l['shoulder'][1] - l['shoulder'][0]) / D,
             backpack_span_over_D=(l['backpack'][1] - l['backpack'][0]) / D if l['backpack'] else None,
             torso_over_total=(l['crotch'] - chin) / Htot, leg_over_total=(sole - l['crotch']) / Htot,
             torso_over_D=(l['crotch'] - chin) / D, leg_over_D=(sole - l['crotch']) / D,
             hand_w_over_D=(l['glove'][2] - l['glove'][0]) / D if l['glove'] else None,
             hand_h_over_D=(l['glove'][3] - l['glove'][1]) / D if l['glove'] else None,
             boot_h_over_D=(sole - l['boot_top']) / D, boot_w_over_D=[w / D for w in l['sole_w']],
             leg_w_over_D=l['leg_w'] / D, outline_med_px=f['outline_med'], outline_over_D=f['outline_med'] / D,
             outline_max_px=f['outline_max'])
    out[k] = {kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in r.items()}
    # annotated crop
    crop = A[y0:y1, x0:x1].copy(); s = 2
    im = Image.fromarray(crop).resize((crop.shape[1] * s, crop.shape[0] * s), Image.LANCZOS); d = ImageDraw.Draw(im)
    W = im.size[0]
    for y, c, t in [(top, (255, 0, 0), 'hair top'), (skull, (255, 128, 0), 'skull top (fit)'), (chin, (255, 0, 255), 'chin'),
                    (l['crotch'], (0, 160, 0), 'crotch'), (l['boot_top'], (0, 0, 255), 'boot top'), (sole, (255, 0, 0), 'sole')]:
        d.line([(0, y * s), (W, y * s)], fill=c, width=2); d.text((4, y * s - 12), t, fill=c)
    cx, cy, R = f['cx'], f['cy'], f['R_outer']
    d.ellipse([(cx - R) * s, (cy - R) * s, (cx + R) * s, (cy + R) * s], outline=(0, 200, 255), width=2)
    sh = l['shoulder']; d.line([(sh[0] * s, sh[2] * s), (sh[1] * s, sh[2] * s)], fill=(0, 200, 200), width=3)
    if l['glove']: d.rectangle([v * s for v in l['glove']], outline=(255, 200, 0), width=2)
    for c in f['comps']:
        d.rectangle([c['bx'] * s, c['by'] * s, (c['bx'] + c['w']) * s, (c['by'] + c['h']) * s], outline=(0, 220, 0))
    im.save(os.path.join(H, f'{k}_measured.png'))
    cut = crop.copy(); cut[sil == 0] = (253, 243, 232); Image.fromarray(cut).save(os.path.join(H, f'{k}_cut.png'))
json.dump(out, open(os.path.join(H, 'sheet_measure.json'), 'w'), indent=1)
for k, v in out.items(): print(k, v)
