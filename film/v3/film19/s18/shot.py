#!/usr/bin/env python3
"""shot.py -- film 19 take s18 = shot 18: "ลูกชายเขาพกมันข้ามทะเลไปจาไมกา" -- the ship under full sail with bow wave and wake, swell crest in the foreground;
snap on "จาไมกา" (caption "ไปจาไมกา" 47.68 s -> g 1433, the word heard ~g 1438).
SHIP ship_hero / NOON, no actors.  g 1384..1467 (46.12-48.92 s) + 9 handle frames each side (dissolve 11 in from shot 17, dissolve 13 out to shot 19): g 1375..1476.
The ship sits at the origin (it 'sails' by the sea moving: set_sea(g/30) and set_roll(g/30) keyed on EVERY frame; the wake is part of the set).
Camera (c19.CamPath): push 8 %/s + slide + small arc from the hero preset pose; moving on the first frame, decay 0.1; SNAP push on "จาไมกา".  NO depth of field, NO text, NO caption_shade.

    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
    python3 deliver.py [draft]
"""
import math, os, sys, json, random as _random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
bpy = C.bpy

H, K, cast19 = C.H, C.K, C.cast19
blink = C.blink
lerp = C.lerp
WORK = os.path.join(HERE, "work")
TAKE = "s18"
PRESET, LIGHT = "ship_hero", "NOON"
SHOT_T0, SHOT_T1 = 46.12, 48.92
H_IN, H_OUT = 9, 9
G0, G1 = C.g_bound(SHOT_T0), C.g_bound(SHOT_T1)          # shot = g G0..G1-1
FIRST_G, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(FIRST_G, G_LAST + 1))
FINAL_SPP = 12                                           # H.STATE['samples'] of ship_hero (cost_report): Take() checks it

SEAK = float(os.environ.get("SEAK", "2"))                    # sea clock rate (1 = real time)
S = 1.85                                                 # metres -> world D
# hero preset pose, pulled back (DS x the preset distance) so the WHOLE ship fits the frame with a margin; the ship then travels across the frame
# (slide + orbit) and a snap pushes in x1.33 with a pan on the word.  Values from a random search (scratchpad plan18.py) under the constraint:
# every key point of the ship's bbox (bow, stern, mast tops, flanks) inside the frame with >= 30 px margin on EVERY frame.
_loc, _look = Vector((-30.200786086416148, 60.27572081495611, 4.2)) * S, Vector((24.26311741508658, -23.591335979586283, 9.440777928304122)) * S
DS = float(os.environ.get("DS", "1.15"))
_z0 = _loc.z
_loc = _look - (_look - _loc) * DS
_loc.z = _z0                                          # pull back horizontally at the preset's own height
_L = (_look - _loc).length
_f = (_look - _loc).normalized(); _r = Vector((_f.y, -_f.x, 0.0)).normalized(); _u = _r.cross(_f).normalized()
_o = _r * (float(os.environ.get("OX", "-7.81")) * _L / C.F_PX) + _u * (float(os.environ.get("OY", "6.99")) * _L / C.F_PX)
CAM_LOC0, CAM_LOOK0 = _loc + _o, _look + _o
G_WORD = C.cap_g("ไปจาไมกา") + 5                         # ~1438: the word จาไมกา (the caption phrase starts at ไป, 1433)
_S = [float(v) for v in os.environ.get("SNP", "1428,17,1.22,-2.86,-0.9").split(",")]   # snap: start g, frames, k, shift right/up (D)
SNAP = (int(_S[0]), int(_S[0] + _S[1]))                                     # 17 f, x1.33 with a pan, landing on the word
_P = [float(v) for v in os.environ.get("CAMP", "-0.01,12.25,12.26,-5.59").split(",")]      # push, slide px/s, rise px/s, arc deg/s
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, FIRST_G, G_LAST, push=_P[0], slide_px=_P[1], rise_px=_P[2], arc_deg_s=_P[3], decay=0.1,
                snaps=[dict(g=SNAP, k=_S[2], peak=2.0, shift=(_S[3], _S[4])),
                       dict(g=(1446, 1476), k=1.05, peak=1.0, shift=(0.8, 0.0))])      # a gentle second move so the camera never parks after the snap (g 1444-1467)


def widen_sea(preset, k, nu, nv):
    """the sea is ONE grid fitted to the preset camera's footprint; a pull-back would show its edge.  Runtime patch (set modules stay
    untouched): fit the grid to a virtual camera k times farther from the look point on the same axis (a k times wider footprint)."""
    import h19_ship as SH
    P = SH.PRESETS[preset]
    global PRESET_CAM0
    PRESET_CAM0 = dict(P['cam'])                                              # the preset's own camera (metres), before the widening patch
    loc, look = Vector(P["cam"]["loc"]), Vector(P["cam"]["look"])
    v = look + (loc - look) * k
    v.z = loc.z + (k - 1.0) * float(os.environ.get("ZUP", "6.0"))          # a farther AND higher virtual camera (the hero camera is low: scaling z down would put it under the sea)
    P["cam"] = dict(P["cam"], loc=tuple(v))
    P["sea_nu"], P["sea_nv"] = nu, nv


def whitecaps_in_front(n=int(os.environ.get("WC", "28")), seed=int(os.environ.get("WCSEED", "3"))):
    """foreground swell crests: the hero preset's floating_spar() also places the preset's two foam streaks relative to P['cam'] (our widen_sea patched it): wrap it,
    keep the spar where the preset puts it (original camera) and add broken foam lines (the set's 'streaks' hook) between our camera and the ship, so crests
    sweep across the frame as the camera slides (frame-diff)."""
    import random as _rnd
    import h19_ship_land as LD
    orig = LD.floating_spar
    cam0 = dict(PRESET_CAM0)

    def fs(S_, P, sea_P):
        P2 = dict(P, cam=cam0)
        orig(S_, P2, sea_P)
        rg = _rnd.Random(seed)
        c = Vector(cam0["loc"]); lk = Vector(cam0["look"])
        c = lk - (lk - c) * DS                                              # our (pulled back) camera, metres
        f = Vector((lk.x - c.x, lk.y - c.y, 0)).normalized(); r = Vector((f.y, -f.x, 0))
        for _ in range(n):
            d, lat = rg.uniform(8.0, 60.0), rg.uniform(-22.0, 22.0)
            m = c + f * d + r * lat
            a = rg.uniform(-0.6, 0.6); ln = rg.uniform(7.0, 20.0)
            dirv = r * math.cos(a) + f * math.sin(a)
            p0, p1 = m - dirv * (ln / 2), m + dirv * (ln / 2)
            sea_P["streaks"].append(((p0.x, p0.y), (p1.x, p1.y), rg.uniform(0.8, 1.4), rg.uniform(0.8, 1.0)))
    LD.floating_spar = fs


ISLAND_AT = (float(os.environ.get("ISX", "250")), float(os.environ.get("ISY", "699")), 1452)   # screen px (x, y) of the island base at g 1452
ISLAND_W = float(os.environ.get("ISW", "34"))                                                   # metres (~10 % of the frame width at ~330 m)


def build_island():
    """JAMAICA on the snap: a green dome with a sand rim and 5 palms, built at runtime (the set's own headland / palm builders, no set edit), placed on the sea
    ahead of the ship so that the snap's pan carries the camera TOWARD it and it ends beside the bow (QA-art round 11)."""
    import h19_ship_land as LD
    import h19_ship as SH
    from h19_kit import mat as kmat, MB as KMB
    sx, sy, gref = ISLAND_AT
    loc, look = CAM.at(gref)
    f, r, u = C._cam_basis(loc, look)
    d = (f + r * ((sx - 360) / C.F_PX) + u * ((640 - sy) / C.F_PX)).normalized()
    t = (0 - loc.z) / d.z
    P = (loc + d * t) / S                                                       # the base point on the sea, metres
    LT = SH.LIGHTS["NOON"]
    orig_lm = LD.land_mat
    LD.land_mat = lambda name, LT_, **kw: orig_lm(name, LT_, top=kw.get("top", "#4aa25c"), low=kw.get("low", "#34794c"), beach=kw.get("beach", "#efe0b4"),
                                                  hmax=kw.get("hmax", 60.0), dist=(700.0, 4000.0), kmax=0.22)
    yaw = math.atan2(r.y, r.x)
    c = (P.x, P.y)
    H_ = 0.55 * ISLAND_W / 4.0                                                  # dome height ~ 4.7 m
    LD.headland(LT, c, yaw, ISLAND_W * 1.35, 1.0, ISLAND_W * 0.62, seed=21, nx=60, ny=14, name="jamaica_sand")        # the sand shelf / rim
    dome = LD.headland(LT, (c[0] + f.x * 1.5, c[1] + f.y * 1.5), yaw, ISLAND_W, H_, ISLAND_W * 0.42, seed=22, nx=60, ny=14, name="jamaica")
    for o in (bpy.data.objects.get("jamaica"), bpy.data.objects.get("jamaica_sand")):
        if o is not None:
            o.parent = K.ROOT
    LD.land_mat = orig_lm
    M = dict(trunk=kmat("jtrunk", "#8a6a48", "#6f5438", scale=6, aniso=(0.3, 0.3, 1.0)), frond=kmat("jfrond", "#3f9a3c", "#2f8a34", scale=3, rough=0.9),
             frond2=kmat("jfrond2", "#52aa44", "#3e9a3c", scale=3))
    mb = KMB("jpalms")
    rr = _random.Random(11)
    fx, fy = f.x, f.y
    for i, (a, b, h, ln) in enumerate(((-0.30, 0.10, 8.5, 0.5), (-0.10, 0.18, 10.5, 0.7), (0.10, 0.12, 9.0, 0.9), (0.28, 0.16, 7.5, 0.4), (0.02, 0.30, 8.0, 0.6))):
        px = c[0] + r.x * ISLAND_W * a + f.x * (3.0 + ISLAND_W * 0.42 * b)
        py = c[1] + r.y * ISLAND_W * a + f.y * (3.0 + ISLAND_W * 0.42 * b)
        LD.palm(mb, M, (px, py, H_ * 0.62), h, ln, 31 + i)
    mb.finish(shadow=False)


def tame_bow_wave():
    """QA-art round 11: the glossy glowing blue bow-wave tube reads as plastic: cut its emission and specular by ~70 %"""
    for nm in ("bow_fx", "foam_wave"):
        ob = bpy.data.objects.get(nm)
        if ob is None:
            continue
        objs = [ob] + list(ob.children_recursive)
        for o in objs:
            for sl in getattr(o, "material_slots", []):
                m = sl.material
                if m is None or not m.use_nodes:
                    continue
                for n in m.node_tree.nodes:
                    if n.type == "BSDF_PRINCIPLED":
                        for k_, fct in (("Emission Strength", 0.3), ("Specular IOR Level", 0.3), ("Coat Weight", 0.3)):
                            if k_ in n.inputs:
                                n.inputs[k_].default_value *= fct
                        if "Roughness" in n.inputs:
                            n.inputs["Roughness"].default_value = max(n.inputs["Roughness"].default_value, 0.6)


def deepen_sky():
    """deepen the pale horizon band of the NOON sky (QA-art round 10): runtime edit of the light table, no set file touched"""
    import h19_ship as SH
    sky = [(0.0, '#5f92dc'), (0.46, '#82aee2'), (0.5, '#7ca8e0'), (0.56, '#6f9fe0'), (0.66, '#5c8ede'), (0.78, '#4a7bd6'), (0.88, '#3a67cb'), (1.0, '#2c54b6')]
    SH.LIGHTS['NOON'] = dict(SH.LIGHTS['NOON'], sky=sky, haze='#86aede')


# ----------------------------------------------------------------------------- william19 small at the bow holding the watch (QA-art: "his son carried it")
WILL_XYZ = tuple(float(v) for v in os.environ.get("WXYZ", "-6.5,36.0,12.0").split(","))   # forecastle, port side, in front of the foremast (visible between the jibs and the foresail)
WS = float(os.environ.get("WSCALE", "4.0"))              # readability scale (a 3.3 D man is ~15 px tall from here)
PPD = 224


def pose_william(g):
    """william19 acts (QA-tech 'one pose for 2.8 s'): g 1384-1409 looks down at the H4 on his palm; 1410-1426 glances up at the ship / the sea and turns his head;
    1427-1437 the hand starts up; on 'จาไมกา' (g 1438) he raises the watch toward the island with a delighted face; then holds it high, bobbing"""
    p = dict(cast19.STORY19["william_show_h4"][1])
    p["blink"] = blink(g, [1390, 1416, 1442, 1470])
    p["t"] = g / 30.0
    base = (0.64, 0.62)
    up = _ramp(g, 1427, 1440)
    hand = (lerp(base[0], 0.78, up), lerp(base[1], 1.65, up))
    p["arm_r"] = dict(hand=(hand[0], hand[1] + 0.05 * math.sin(g * 0.35)), bend=lerp(-0.2, -0.35, up), shape="open", stretch=1.15, layer="top")
    p["prop_r"] = dict(type="h4_watch", scale=2.0)                              # the H4 drawn at 2x so it reads as a watch
    if g < 1410:
        p["pitch"] = 0.25; p["gaze"] = (0.6, -0.7); p["expr"] = "happy"; p["head_roll"] = -3 + 2.0 * math.sin(g * 0.2)
    elif g < 1427:
        k = _ramp(g, 1410, 1416)
        p["pitch"] = lerp(0.25, -0.05, k); p["gaze"] = (lerp(0.6, -0.8, k), lerp(-0.7, 0.2, k)); p["expr"] = "happy"
        p["yaw"] = lerp(0.3, -0.2, k); p["head_roll"] = 5.0 * math.sin((g - 1410) * 0.5)
    else:
        e = _ramp(g, 1432, 1440)
        p["pitch"] = lerp(-0.05, -0.35, e); p["gaze"] = (lerp(-0.8, -1.0, e), lerp(0.2, 0.45, e))      # up and toward the island (screen-left)
        p["expr"] = "excited" if g >= 1436 else "happy"
        p["yaw"] = lerp(-0.2, -0.35, e); p["head_roll"] = -4.0 * e + 3.0 * math.sin(g * 0.45)
        if g >= 1436:
            p["mouth"] = "smile"
    p["lean"] = p.get("lean", 0) + 2.0 * math.sin(g * 0.2) - 4.0 * up
    return p


def hop_z(g):
    """a little hop of joy on the word (g 1438)"""
    return 0.9 * math.sin(math.pi * _ramp(g, 1436, 1446)) * (1.0 - _ramp(g, 1446, 1456)) + 0.04 * math.sin(g * 0.5)


def _ramp(g, a, b):
    return C.u_of(g, a, b)


class Take(C.Take):
    def __init__(self, quality="preview"):
        PRESET_CAM0 = None
        widen_sea(PRESET, float(os.environ.get('WIDEN', '1.8')), int(os.environ.get('NU', '900')), int(os.environ.get('NV', '1300')))
        whitecaps_in_front()
        deepen_sky()
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_" + TAKE)
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        root = self.A["ship_root"]
        self.will = self.actors["will"] = C.make_actor("will", "william19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        C.ride_ship(self.will, root)                                      # before place() and before any set_roll key
        self.key_cam(C.bf(FIRST_G), *CAM.at(FIRST_G))
        self.scene.view_settings.exposure -= float(os.environ.get("EXPO", "0.8"))           # QA_TEAM section G: luma 70-135 (the foam crests brighten the frame)
        build_island()
        tame_bow_wave()
        g_ = C.bpy.data.objects.get("glint")                    # tone the blown sun glint down (QA-tech): 40 -> GLINT x the set's energy
        if g_ is not None:
            g_.data.energy *= float(os.environ.get("GLINT", "0.0"))

    def pose(self, gs):
        for g in gs:
            f = C.bf(g)
            self.key_set(f, sea=g / 30.0 * SEAK, roll=g / 30.0 * SEAK)           # same t, every frame
            self.key_cam(f, *CAM.at(g))
            C.key_vis([o for o in (C.bpy.data.objects.get('gulls_gullt'), C.bpy.data.objects.get('gulls_gullw')) if o], False, f)   # no gulls (one was clipped by the edge)
            C.place(self.will, f, (WILL_XYZ[0], WILL_XYZ[1], WILL_XYZ[2] + hop_z(g)), scale=WS)
        for g in gs:
            f = C.bf(g)
            self.scene.frame_set(f)
            self.will.pose(f, pose_william(g), camera=self.cam)
        self.sprites_for([(self.will, PPD)], [C.bf(g) for g in gs])

    def report(self, g):
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, C.bf(g)), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [C.bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows[::6]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if FIRST_G <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else FINAL_SPP
        quality = "final" if scale >= 1.0 else "preview"
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
