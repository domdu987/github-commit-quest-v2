"""hue20.py : hue check on REAL cast-shadow pixels of a set3d20 frame (same method as styleboard/hue_check.py): a sun-only render (white override material, no bounces, sky / clouds /
hills / shafts / rain / sparks hidden) and the same without shadows tell which pixels are truly blocked from the key; over those pixels (saturation > 0.1) we report the circular
mean hue (band 225-265, client shade 240-260), the share of cast-shadow pixels in the band and the magenta share of the whole frame (hue 290-340, saturation > 0.25, limit 10 %).
Call measure(png) AFTER the frame was rendered in the same scene (it restores the scene)."""
import os, numpy as np
import bpy
from PIL import Image, ImageFilter

def _rd(sc, path, samples, transp):
    cy = sc.cycles; cy.samples = samples; cy.use_denoising = False; sc.render.film_transparent = transp; sc.render.filepath = path
    bpy.ops.render.render(write_still=True); a = np.asarray(Image.open(path).convert('RGBA'), dtype=np.float32) / 255.0; os.remove(path); return a

def measure(png, tmp=None):
    sc = bpy.context.scene; cy = sc.cycles; tmp = tmp or png[:-4]
    saved = dict(samples=cy.samples, den=cy.use_denoising, mb=cy.max_bounces, db=cy.diffuse_bounces, gb=cy.glossy_bounces, comp=sc.render.use_compositing, tr=sc.render.film_transparent,
                 cm=sc.render.image_settings.color_mode, exp=sc.view_settings.exposure)
    sc.render.image_settings.color_mode = 'RGBA'; sc.render.use_compositing = False; sc.view_settings.exposure = 0.0
    lights = [(l, l.data.energy) for l in bpy.data.objects if l.type == 'LIGHT' and l.name != 'key']
    for l, e in lights: l.data.energy = 0.0
    nt = bpy.data.worlds['sky'].node_tree; wb = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeBackground']; wv = [n.inputs['Strength'].default_value for n in wb]
    for n in wb: n.inputs['Strength'].default_value = 0.0
    hid = [o for o in bpy.data.objects if o.name.startswith(('hills', 'clouds', 'stars', 'shafts', 'rain', 'spk_', 'toss', 'ring_', 'sg_', 'actor_', 'sun'))]; hv = [o.hide_render for o in hid]
    for o in hid: o.hide_render = True
    wm = bpy.data.materials.new('ovr'); wm.use_nodes = True; bs = wm.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (1, 1, 1, 1); bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    cy.max_bounces = 0; cy.diffuse_bounces = 0; cy.glossy_bounces = 0; bpy.context.view_layer.material_override = wm
    D = _rd(sc, tmp + '_D.png', 24, True); bpy.context.view_layer.material_override = None
    lD = 0.3 * D[..., 0] + 0.59 * D[..., 1] + 0.11 * D[..., 2]
    vs = [(o, o.visible_shadow) for o in bpy.data.objects if o.type == 'MESH']
    for o, _ in vs: o.visible_shadow = False
    bpy.context.view_layer.material_override = wm
    D2 = _rd(sc, tmp + '_D2.png', 8, True); bpy.context.view_layer.material_override = None
    for o, v in vs: o.visible_shadow = v
    lD2 = 0.3 * D2[..., 0] + 0.59 * D2[..., 1] + 0.11 * D2[..., 2]
    # restore
    for l, e in lights: l.data.energy = e
    for n, v in zip(wb, wv): n.inputs['Strength'].default_value = v
    for o, v in zip(hid, hv): o.hide_render = v
    bpy.data.materials.remove(wm)
    cy.samples = saved['samples']; cy.use_denoising = saved['den']; cy.max_bounces = saved['mb']; cy.diffuse_bounces = saved['db']; cy.glossy_bounces = saved['gb']
    sc.render.use_compositing = saved['comp']; sc.render.film_transparent = saved['tr']; sc.render.image_settings.color_mode = saved['cm']; sc.view_settings.exposure = saved['exp']
    cast = (D[..., 3] > 0.99) & (lD < 0.02) & (lD2 > 0.08)
    mask = np.asarray(Image.fromarray((cast * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)), dtype=np.float32) > 127
    im = Image.open(png).convert('RGB'); hsv = np.asarray(im.convert('HSV'), dtype=np.float32).reshape(-1, 3)
    h = hsv[:, 0] * 360 / 255; s = hsv[:, 1] / 255; v = hsv[:, 2] / 255
    m = mask.reshape(-1); sel = m & (s > 0.1) & (v > 0.06)
    mag = float(((h >= 290) & (h <= 340) & (s > 0.25)).mean() * 100)
    if sel.sum() < 200: return dict(shade_hue=None, cast_pct=float(m.mean() * 100), in_band=None, magenta=mag, ok=mag <= 10)
    ang = np.deg2rad(h[sel]); mh = float((np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) + 360) % 360)
    inb = float(((h >= 225) & (h <= 265))[sel].mean() * 100)
    return dict(shade_hue=round(mh, 1), median=round(float(np.median(h[sel])), 1), cast_pct=round(float(m.mean() * 100), 1), in_band=round(inb, 1), magenta=round(mag, 2), ok=(225 <= mh <= 265) and mag <= 10)
