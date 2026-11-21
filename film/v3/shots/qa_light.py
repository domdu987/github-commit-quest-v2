#!/usr/bin/env python3
"""qa_light.py -- light measurements on our own frames (bpy; renders measurement passes of chosen output frames).

    python3 qa_light.py <out_dir> <g,g,...> [samples=16] [threads=4]

For every frame g five passes at 720x1280: graded with the key (the film frame), graded with the key at zero energy
(the same pixels in shade), and without the grade: key on, key on without any shadow casting, key on without the
actors' shadows.  From them:
  visibility v = (on - off) / (unshadowed - off) per pixel; sunny = the key would reach the surface if nothing stood
  in the way; lit = sunny and v > 0.97; cast shadow = sunny and v < 0.03;
  same surface in shadow / lit: median over the lit pixels of (graded key-off / graded key-on), linear luminance from
  the displayed values, and the same as display luma; hue of the lit and of the shaded colour;
  cast-shadow edge width: 10-90 percent width of v across the v = 0.5 contour (set3d/review/review_analyze.edge_widths);
  actor shadow: pixels whose visibility drops by more than 0.5 because of the actors' shadow casters.
Writes <out_dir>/light_g<g>.json and the passes as PNG.
"""
import json, os, sys, colorsys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "set3d", "review"))


def lin(a):
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def analyse(d, g):
    import cv2
    import review_analyze as RA
    ld = lambda n: cv2.cvtColor(cv2.imread(os.path.join(d, "g%03d_%s.png" % (g, n))), cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    gon, goff, on, un, off, noact = ld("graded_on"), ld("graded_off"), ld("on"), ld("unshadowed"), ld("off"), ld("noactor")
    lon, loff, lun, lno = lin(on).sum(2), lin(off).sum(2), lin(un).sum(2), lin(noact).sum(2)
    den = lun - loff
    sunny = den > 0.03
    v = np.clip((lon - loff) / np.maximum(den, 1e-4), 0, 1)
    vno = np.clip((lno - loff) / np.maximum(den, 1e-4), 0, 1)
    lit = sunny & (v > 0.97)
    cast = sunny & (v < 0.03)
    W = np.array([0.2126, 0.7152, 0.0722])
    Yon, Yoff = lin(gon) @ W, lin(goff) @ W
    luma = lambda a: a @ np.array([0.299, 0.587, 0.114])
    res = dict(g=g, sunny_share=float(sunny.mean()), lit_share=float(lit.mean()), cast_shadow_share=float(cast.mean()))
    if lit.sum() > 400:
        r = Yoff[lit] / np.maximum(Yon[lit], 1e-4)
        rd = luma(goff)[lit] / np.maximum(luma(gon)[lit], 1e-3)
        res["shadow_over_lit_linear"] = [float(np.percentile(r, q)) for q in (10, 50, 90)]
        res["shadow_over_lit_display"] = [float(np.percentile(rd, q)) for q in (10, 50, 90)]
        L = np.median(gon[lit], axis=0); S = np.median(goff[lit], axis=0)
        hx = lambda c: "#%02x%02x%02x" % tuple(int(round(float(x) * 255)) for x in c)
        res["lit_colour"], res["shade_colour"] = hx(L), hx(S)
        res["hue_lit"] = colorsys.rgb_to_hsv(*[float(x) for x in L])[0] * 360
        res["hue_shade"] = colorsys.rgb_to_hsv(*[float(x) for x in S])[0] * 360
    if cast.sum() > 200 and lit.sum() > 400:       # what is actually on screen: shadowed pixels against lit pixels
        C = np.median(gon[cast], axis=0); L = np.median(gon[lit], axis=0)
        res["cast_region_over_lit_region_linear"] = float((lin(C) @ W) / (lin(L) @ W))
    ew = RA.edge_widths(v, sunny)
    if ew:
        w = np.array([e[0] for e in ew])
        res["edge_width_px"] = dict(n=len(ew), p10=float(np.percentile(w, 10)), median=float(np.median(w)), p90=float(np.percentile(w, 90)), max=float(w.max()))
    act = sunny & ((vno - v) > 0.5)
    res["actor_shadow_px"] = int(act.sum())
    res["actor_shadow_share"] = float(act.mean())
    if act.sum() > 300:
        ewa = [e for e in ew if act[max(0, e[2] - 6):e[2] + 7, max(0, e[1] - 6):e[1] + 7].any()]
        if ewa:
            w = np.array([e[0] for e in ewa])
            res["actor_shadow_edge_px"] = dict(n=len(ewa), p10=float(np.percentile(w, 10)), median=float(np.median(w)), p90=float(np.percentile(w, 90)))
    tp = os.path.join(d, "g%03d_track.json" % g)
    if os.path.exists(tp):
        tr = json.load(open(tp))
        inside = [(int(round(x)), int(round(y))) for x, y in tr["px"] if 2 <= x < 718 and 2 <= y < 1278]
        hit = sum(1 for x, y in inside if act[y - 2:y + 3, x - 2:x + 3].any())
        low = sum(1 for x, y in inside if sunny[y, x] and v[y - 1:y + 2, x - 1:x + 2].mean() < 0.5)
        res["track_under_actor_shadow"] = "%d of %d visible samples (any cast shadow: %d)" % (hit, len(inside), low)
    cv2.imwrite(os.path.join(d, "g%03d_vis.png" % g), (v * 255).astype(np.uint8))
    cv2.imwrite(os.path.join(d, "g%03d_actorshadow.png" % g), (act * 255).astype(np.uint8))
    json.dump(res, open(os.path.join(d, "light_g%03d.json" % g), "w"), indent=1)
    return res


def main(argv):
    out = argv[0]
    gs = [int(v) for v in argv[1].split(",")]
    samples = int(argv[2]) if len(argv) > 2 else 16
    threads = int(argv[3]) if len(argv) > 3 else 4
    os.makedirs(out, exist_ok=True)
    import bpy, film
    for take in ("A", "B"):
        g0, g1 = film.TAKES[take]
        mine = [g for g in gs if g0 <= g <= g1]
        if not mine:
            continue
        F = film.Film(take)
        F.pose(mine)
        sc = F.scene
        sun = bpy.data.objects["key_sun"]
        e0 = sun.data.energy

        def shot(g, name):
            F.render([g], out, threads=threads, samples=samples, verbose=False)
            os.replace(os.path.join(out, "f_%04d.png" % (g + 1)), os.path.join(out, "g%03d_%s.png" % (g, name)))

        for g in mine:
            # where the visible part of the red track is on screen (to test whether an actor's shadow lies on it)
            u1 = film.line_at(g) if take == "A" else 1.0 - film.erase_at(g)
            sc.frame_set(g + 1)
            pts = [film.render.world_to_screen(F.cam, film.S.track_point(u), g + 1)[:2] for u in np.linspace(0.0, max(u1, 0.0), 41)] if u1 > 0.01 else []
            json.dump(dict(u1=u1, px=[[float(x), float(y)] for x, y in pts]), open(os.path.join(out, "g%03d_track.json" % g), "w"))
            sc.render.use_compositing = True
            shot(g, "graded_on")
            sun.data.energy = 0.0; shot(g, "graded_off"); sun.data.energy = e0
            sc.render.use_compositing = False
            shot(g, "on")
            sun.data.energy = 0.0; shot(g, "off"); sun.data.energy = e0
            sun.data.use_shadow = False; shot(g, "unshadowed"); sun.data.use_shadow = True
            keep = [(ob, ob.visible_shadow) for a in F.actors for ob in (a.card, a.proxy) if ob is not None]
            apply0 = F.apply

            def apply_noshadow(gg):                  # Film.apply() sets the casters per frame: switch them off after it
                apply0(gg)
                for ob, vs in keep:
                    ob.visible_shadow = False
            F.apply = apply_noshadow
            shot(g, "noactor")
            F.apply = apply0
            for ob, vs in keep:
                ob.visible_shadow = vs
            sc.render.use_compositing = True
    for g in gs:
        r = analyse(out, g)
        print(json.dumps(r))


if __name__ == "__main__":
    main(sys.argv[1:])
