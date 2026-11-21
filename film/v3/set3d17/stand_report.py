#!/usr/bin/env python3
"""stand_report.py: where do the stand points land on screen (720x1280)?  python3 stand_report.py <preset> [light]
Prints head centre / radius / chin per mark (placeholder head = 0.3 of the card height), flags: OFF (head outside 30..690 x 60..1240), LOW (chin > 880),
BAND (head cy outside 450..760), and OVERLAP between marks (centres closer than 1.0 head diameter). Also lists the gas globes (glow_gas lamp lights) in frame."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bertillon as K, bpy
def report(preset, light=None, marks=None, quiet=False):
    A = K.build(preset=preset, light=light); bpy.context.view_layer.update(); cam = bpy.context.scene.camera; res = {}
    for nm, (x, y, z, fz, who) in (marks or A['marks']).items():
        key = 'seated' if nm == 'chair' else who; H = K.HEIGHT[key]; hd = H * 0.3; hc = z + H - hd * 0.52
        px, py, dz = K.project(cam, (x, y, hc))
        if dz <= 0: continue
        R = hd * 0.5 * 782.2 / dz; flags = []
        if not (30 <= px <= 690 and 60 <= py <= 1240): flags.append('OFF')
        if py + R > 880: flags.append('LOW')
        if not (450 <= py <= 760): flags.append('BAND')
        res[nm] = dict(cx=px, cy=py, R=R, chin=py + R, flags=flags)
    if not quiet:
        for nm, v in res.items(): print('%-16s cx %4.0f cy %5.0f R %3.0f chin %5.0f %s' % (nm, v['cx'], v['cy'], v['R'], v['chin'], ' '.join(v['flags'])))
        names = list(res)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = res[names[i]], res[names[j]]; d = math.hypot(a['cx'] - b['cx'], a['cy'] - b['cy']) / (a['R'] + b['R'])
                if d < 1.0: print('OVERLAP %s / %s  (%.2f head D apart)' % (names[i], names[j], d * 1.0))
        for o in bpy.context.scene.objects:
            if o.type == 'LIGHT' and o.data.type == 'POINT':
                px, py, dz = K.project(cam, tuple(o.location))
                if dz > 0 and -50 < px < 770 and -50 < py < 1330: print('LAMP %-10s px %4.0f %4.0f  dz %.1f' % (o.name, px, py, dz))
    return A, res
if __name__ == '__main__': report(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
def hood_cover(preset=None, cam=None):
    """fraction of the frame covered by the convex hull of the tripod's black cloth (projected vertices), and which staged heads it touches (measure presets)."""
    from PIL import Image, ImageDraw
    import numpy as np
    A = K.build(preset=preset); bpy.context.view_layer.update(); cm = bpy.context.scene.camera
    ob = [o for o in bpy.data.objects if o.name.endswith('_cloth')][0]; M = ob.matrix_world; pts = []
    for v in ob.data.vertices:
        p = M @ v.co; x, y, z = K.project(cm, tuple(p))
        if z > 0.05: pts.append((x, y))
    if len(pts) < 3: return 0.0, []
    P = np.array(pts); idx = np.argsort(P[:, 0]); P = P[idx]
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in map(tuple, P):
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in map(tuple, P[::-1]):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    hull = lo[:-1] + up[:-1]; im = Image.new('L', (720, 1280), 0); ImageDraw.Draw(im).polygon(hull, fill=255); m = np.asarray(im) > 0
    frac = m.mean(); hit = []
    yy, xx = np.mgrid[0:1280, 0:720]
    for nm in K.PRESETS[preset].get('stage', []):
        x, y, z, fz, who = A['marks'][nm]; key = 'seated' if nm == 'chair' else who; H = K.HEIGHT[key]; hd = H * 0.3; hc = z + H - hd * 0.52
        px, py, dz = K.project(cm, (x, y, hc)); R = hd * 0.5 * 782.2 / dz; disc = (xx - px) ** 2 + (yy - py) ** 2 < R * R
        if (m & disc).sum() > 0.02 * disc.sum(): hit.append((nm, round(float((m & disc).sum() / disc.sum()), 2)))
    return float(frac), hit
def hood_mask(preset, cam=None, look=None, out='/tmp/claude-0/sp/hood.png'):
    """true coverage: the tripod's cloth is repainted flat magenta and the frame is rendered (draft); returns (fraction of the frame, [(stand mark, fraction of its head disc covered)])."""
    import numpy as np
    from PIL import Image
    pr = K.PRESETS[preset]; old = (pr['cam'], pr['look'])
    if cam: pr['cam'] = cam
    if look: pr['look'] = look
    A = K.build(preset=preset); bpy.context.view_layer.update(); cm = bpy.context.scene.camera
    m = bpy.data.materials.new('mag'); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (1, 0, 1, 1); o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0])
    for ob in bpy.data.objects:
        if ob.name.endswith('_cloth') and ob.type == 'MESH':
            ob.data.materials.clear(); ob.data.materials.append(m)
        elif ob.type == 'MESH' and 'ink' in ob.modifiers: ob.modifiers['ink'].show_render = False
    sc = bpy.context.scene; K.setup_render(sc, 'draft', 4); sc.cycles.use_denoising = False; sc.view_settings.view_transform = 'Standard'; sc.render.filepath = out; bpy.ops.render.render(write_still=True)
    pr['cam'], pr['look'] = old
    im = np.asarray(Image.open(out).convert('RGB').resize((720, 1280)), dtype=int); mg = (im[..., 0] > 200) & (im[..., 2] > 200) & (im[..., 1] < 90)
    yy, xx = np.mgrid[0:1280, 0:720]; hit = []
    for nm in pr.get('stage', []):
        x, y, z, fz, who = A['marks'][nm]; key = 'seated' if nm == 'chair' else who; H = K.HEIGHT[key]; hd = H * 0.3; hc = z + H - hd * 0.52
        px, py, dz = K.project(cm, (x, y, hc)); R = hd * 0.5 * 782.2 / dz; disc = (xx - px) ** 2 + (yy - py) ** 2 < R * R
        hit.append((nm, round(float((mg & disc).sum() / max(disc.sum(), 1)), 3)))
    return float(mg.mean()), hit
