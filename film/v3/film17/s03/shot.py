#!/usr/bin/env python3
"""shot.py -- film 17 take s03: shots 7-8, narration 11.10-14.72 s.  g0 336 (shot 7), cut at g 390 (shot 8), g1 445; 6 handle frames each side
=> take.mkv holds g 330..450 (121 frames), transition_in = dissolve 11.
  shot 7  g 336..389  records_aisle / DAY_INT: high, off-centre down the cabinet canyon; cards spill over the runner, a card stack fg,
                      two clerks lost among the drawers.  Pull-out ~9 %/s (dolly back 1.0 m + lift) and a lateral slide ~50 px/s.
  shot 8  g 390..444  records_desk / DAY_INT: insert on the clerk's desk, two photo cards of the same face, one with a big moustache
                      (drawn, no text); the clerk behind scratches his head.  Drift across + push ~8 %/s.
Mouths: nobody speaks (no quote window).
    python3 shot.py probe a:b[:s]            # head / camera numbers
    python3 shot.py stills a:b[:s] out_dir [scale] [samples]
    python3 shot.py final  a:b[:s] [scale] [samples] [raw_dir]
"""
import math, os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c17 as C                                   # noqa: E402
from c17 import K, bpy, Vector, actors, camrig, cast17, lerp   # noqa: E402

FIRST_G, G0, G_CUT, G1, H = 330, 336, 390, 445, 6
LAST_G = G1 + H - 1                                # 450
TMP = os.path.join(HERE, "work")
SPR = os.path.join(TMP, "sprites")
SN7, SN8 = 364, 418
SNAP8 = (-0.30, -0.30, -0.02)
ORB8 = (-20.0, -14.0)
def bf(g): return g - FIRST_G + 1
def shot_of(g): return 7 if g < G_CUT else 8

# ---------------------------------------------------------------- cameras (22 mm, roll 0)
def aim(a, b, u):
    return Vector([lerp(a[i], b[i], u) for i in range(3)])
# shot 7: preset records_aisle camera (0.75,-3.2,3.9)->(-0.2,6.5,2.0); pull back along the aisle + rise + slide to the left
S7 = dict(c0=(0.95, -1.7, 3.5), c1=(0.30, -3.2, 3.85), l0=(-0.35, 6.5, 2.05), l1=(-0.45, 6.3, 1.95))
# shot 8: records_desk insert, drifting right-to-left across the cards with a push
S8 = dict(c0=(0.50, 1.10, 1.55), c1=(0.38, 0.98, 1.50), l0=(-0.74, 2.33, 1.42), l1=(-0.76, 2.35, 1.40))

def cam_of(g):
    if shot_of(g) == 7:
        u = (g - G0) / float(G_CUT - G0); s = S7
    else:
        u = (g - G_CUT) / float(G1 - G_CUT); s = S8
    sway = 0.012 * math.sin(g * 0.9)
    loc = aim(s["c0"], s["c1"], u); look = aim(s["l0"], s["l1"], u)
    loc.z += sway
    if shot_of(g) == 7:
        x = min(1.0, max(0.0, (g - 344) / 12.0)); k1 = x * x * (3 - 2 * x)
        x = min(1.0, max(0.0, (g - SN7) / 12.0)); k = x * x * (3 - 2 * x)
        loc += Vector((0.2, 0.4, -0.2)) * k1 + Vector((0.25, 0.5, -0.3)) * k; look += Vector((1.4, 0.0, -0.05)) * k1 + Vector((0.6, 0.0, -0.05)) * k
    else:
        piv = Vector((-0.74, 2.33, 0.0)); rel = Vector(S8["c0"]) - piv
        x = min(1.0, max(0.0, (g - SN8) / 13.0)); k = x * x * (3 - 2 * x)
        ang = math.radians(ORB8[0] * (g - G_CUT) / float(G1 - G_CUT) + ORB8[1] * k)
        c, sn = math.cos(ang), math.sin(ang)
        loc = Vector((piv.x + c * rel.x - sn * rel.y, piv.y + sn * rel.x + c * rel.y, S8["c0"][2] - 0.06 * (g - G_CUT) / 55.0 + 0.012 * math.sin(g * 0.9)))
        look = Vector((-0.74, 2.33, 1.42))
    return loc, look

# ---------------------------------------------------------------- the cast
A7 = {"aisle1": ("bertillon_holding_card", {}), "aisle_far": ("prisoner_standing_a", {"expr": "worried"})}
A8 = {"desk_clerk": ("bertillon_neutral", {"expr": "worried", "dx": 0.05, "dy": 0.3, "dz": 0.28})}

def pose_for(who, base, g):
    p = dict(base)
    p["blink"] = C.blink(g, 84 + 13 * (hash(who) % 3), 7 * (hash(who) % 5))
    p["t"] = g / 30.0
    p["lean"] = 1.3 * math.sin(g * 0.11 + len(who)) ; p["head_roll"] = 2.0 * math.sin(g * 0.07 + len(who) * 2)
    p["squash"] = (1.0 + 0.008 * math.sin(g * 0.2), 1.0 - 0.008 * math.sin(g * 0.2))
    return cast17.silent(p)

def scratch_pose(base, g):
    """shot 8: the right hand scratches the head (small circles), the other hand on the desk; looks at the cards."""
    p = pose_for("clerk8", base, g)
    u = min(1.0, max(0.0, (g - G_CUT) / 8.0))
    sx, sy = -0.55 + 0.05 * math.sin(g * 0.9), -0.20 + 0.06 * math.cos(g * 0.9)
    hx, hy = lerp(-0.30, sx, u), lerp(1.0, sy, u)
    p["arm_l"] = dict(hand=(hx, hy), bend=lerp(0.2, -1.0, u), stretch=1.0, layer="front")
    p["gaze"] = (0.3, 0.5); p["pitch"] = 0.25; p["yaw"] = 0.15
    p["expr"] = "worried"
    return cast17.silent(p)

# ---------------------------------------------------------------- photo cards (drawn, no text)
def make_photo(path, moustache):
    from PIL import Image, ImageDraw, ImageFilter
    W, Hh = 640, 480
    im = Image.new("RGB", (W, Hh), "#e6d7ae"); d = ImageDraw.Draw(im)
    d.rectangle([10, 10, W - 10, Hh - 10], outline="#b39a64", width=4)
    d.rectangle([20, 20, 140, 62], fill="#a8332c")                        # red tab
    px0, py0, px1, py1 = 70, 80, 420, 440                                 # photo frame
    d.rectangle([px0 - 8, py0 - 8, px1 + 8, py1 + 8], fill="#2c2324"); d.rectangle([px0, py0, px1, py1], fill="#7d776c")
    cx, cy = (px0 + px1) // 2, 255
    d.ellipse([cx - 120, py1 - 90, cx + 120, py1 + 150], fill="#3b3a40")  # shoulders
    d.rectangle([cx - 28, 320, cx + 28, 380], fill="#d7a98c")             # neck
    d.ellipse([cx - 112, cy - 40, cx - 92, cy + 20], fill="#d29f84"); d.ellipse([cx + 92, cy - 40, cx + 112, cy + 20], fill="#d29f84")   # ears
    d.ellipse([cx - 95, cy - 110, cx + 95, cy + 110], fill="#e2b99d")     # face
    d.pieslice([cx - 100, cy - 125, cx + 100, cy + 20], 180, 360, fill="#4a2f22")   # hair
    d.rectangle([cx - 100, cy - 70, cx - 90, cy - 5], fill="#4a2f22"); d.rectangle([cx + 90, cy - 70, cx + 100, cy - 5], fill="#4a2f22")
    for ex in (-38, 38):
        d.ellipse([cx + ex - 17, cy - 38, cx + ex + 17, cy - 12], fill="#f7efe2"); d.ellipse([cx + ex - 7, cy - 35, cx + ex + 7, cy - 15], fill="#2d2420")
        d.line([cx + ex - 24, cy - 52, cx + ex + 22, cy - 56], fill="#3a261c", width=7)
    d.polygon([(cx, cy - 20), (cx - 14, cy + 28), (cx + 14, cy + 28)], fill="#cf977c")
    d.arc([cx - 35, cy + 40, cx + 35, cy + 72], 20, 160, fill="#8a3b34", width=5)   # mouth
    if moustache:
        for sgn in (-1, 1):
            pts = [(cx, cy + 30)]
            for k in range(1, 15):
                t = k / 14.0
                pts.append((cx + sgn * (t * 118), cy + 30 + 8 * math.sin(t * 3.0) - 28 * (t ** 2.2) * (1 if t > 0.75 else 0.2)))
            d.line(pts, fill="#2a1a14", width=26, joint="curve")
            d.ellipse([pts[-1][0] - 16, pts[-1][1] - 20, pts[-1][0] + 16, pts[-1][1] + 10], fill="#2a1a14")
    # right side: ruled greeked rows (no letters) + a fingerprint
    for k in range(6):
        d.rectangle([450, 100 + k * 46, 450 + 140 - 20 * (k % 3), 108 + k * 46], fill="#a99869")
    fx, fy = 520, 390
    for r in range(6, 44, 7):
        d.ellipse([fx - r, fy - int(r * 1.25), fx + r, fy + int(r * 1.25)], outline="#6d5c3e", width=3)
    im = im.filter(ImageFilter.GaussianBlur(0.6)); im.save(path)

def make_photo_cards():
    os.makedirs(TMP, exist_ok=True)
    pa, pb = os.path.join(TMP, "photo_plain.png"), os.path.join(TMP, "photo_tache.png")
    make_photo(pa, False); make_photo(pb, True)
    K.STATE["cardpaths"]["card_photo_a"] = pa; K.STATE["cardpaths"]["card_photo_b"] = pb

# ---------------------------------------------------------------- runtime set dressing
def objs_snapshot():
    return set(o.name for o in bpy.data.objects)

def spill_cards(A):
    """piles of record cards spilling over the runner + two stacks as foreground; returns the new object names"""
    before = objs_snapshot(); rnd = random.Random(17)
    B = K.Batch(41)
    piles = [(-0.65, -0.55), (0.45, 0.25), (-0.5, 1.7), (0.55, 2.7), (-0.6, 3.9), (0.35, 5.0)]
    for (px, py) in piles:
        for i in range(26):
            a = rnd.uniform(0, 360); r = abs(rnd.gauss(0, 0.22)); x = px + r * math.cos(math.radians(a)); y = py + 0.8 * r * math.sin(math.radians(a))
            z = 0.02 + 0.0035 * (i % 9) + 0.003 * rnd.random()
            B.box("cream", (x, y, z), (0.27, 0.19, 0.004), rot=(rnd.uniform(-5, 5), rnd.uniform(-5, 5), rnd.uniform(0, 360)), tint=rnd.uniform(0.86, 1.04))
            if i % 5 == 0:
                B.box(["oxblood", "baize", "navy"][i // 5 % 3], (x + 0.07, y + 0.05, z + 0.003), (0.07, 0.025, 0.003), rot=(0, 0, 0))
    for (sx, sy, n, rt) in ((-0.15, -0.3, 34, 8), (0.9, 0.0, 24, -14)):         # foreground card stacks (aisle fg)
        for i in range(n):
            B.box("cream", (sx + rnd.uniform(-0.012, 0.012), sy + rnd.uniform(-0.012, 0.012), 0.0035 + 0.0075 * i), (0.27, 0.19, 0.007), rot=(0, 0, rt + rnd.uniform(-3, 3)), tint=rnd.uniform(0.88, 1.03))
            if i % 6 == 0:
                B.box("oxblood", (sx + 0.1, sy + 0.03, 0.0075 * i + 0.008), (0.06, 0.02, 0.003), rot=(0, 0, rt))
    B.finalize("spill", ink_t=K.STATE["ink_t"] * 0.5)
    n = 0
    for (px, py) in piles + [(-0.15, -0.3), (0.9, 0.0)]:
        for j in range(2):
            n += 1; a = rnd.uniform(0, 360)
            K.card_plane("pf%d" % n, (px + rnd.uniform(-0.12, 0.12), py + rnd.uniform(-0.1, 0.1), (0.26 if px == -0.15 else 0.185 if px == 0.9 else 0.055) + 0.002 * j), (0.27, 0.2), rot=(90, 0, a), key="card_photo_%s" % "ab"[(n // 2) % 2], ink_t=0.0, thick=0.004)
    return [o for o in bpy.data.objects if o.name not in before]

def desk_cards():
    """two big photo cards on the clerk's desk, each on a small block, leaning back, facing the shot-8 camera; returns the root empties"""
    roots = []
    cen = Vector((-0.74, 2.33)); perp = Vector((0.52, 0.85)); w, h = 0.60, 0.45
    for k, key in enumerate(("card_photo_a", "card_photo_b")):
        c = cen + perp * (0.35 * (k - 0.5) * 2.0)
        B = K.Batch(60 + k); B.box("walnut", (c.x, c.y, 0.915 + 0.13), (0.5, 0.12, 0.26), rot=(0, 0, math.degrees(math.atan2(-perp.x, perp.y)) * 0 + 58)); B.finalize("blk%d" % k, ink_t=0.004)
        root = K.card_plane("photo%d" % k, (c.x, c.y, 0.915 + 0.26 + h / 2 * 0.80), (w, h), rot=(0, 0, 0), key=key, ink_t=0.0, thick=0.006)
        d = Vector((0.7, 0.9, 0.0)) - Vector((c.x, c.y, 0.0)); root.rotation_euler = (math.radians(34), 0, math.atan2(-d.x, d.y))
        roots.append(root)
    return roots

# ---------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="draft"):
        self.A = K.build(preset="records_aisle")
        aisle_fg = [o for o in bpy.data.objects if o.name.startswith("fg")]
        before = objs_snapshot()
        K.fg_records_desk(self.A)
        self.desk_fg = [o for o in bpy.data.objects if o.name not in before]
        self.aisle_fg = aisle_fg
        K.apply_state(self.A, {"fan": 1.0})
        make_photo_cards()
        self.spill = spill_cards(self.A)
        self.photos = desk_cards()
        self.photo_objs = [o for r in self.photos for o in [r] + list(r.children_recursive)]
        self.beams = [o for o in bpy.data.objects if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or []))]
        K.clear_keys()
        sc = bpy.context.scene
        sc.frame_start, sc.frame_end = 1, 9000
        self.cam = camrig.make_camera(sc, name="cam_s03", lens=22.0)
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 600
        self.cam.data.dof.use_dof = False
        os.makedirs(SPR, exist_ok=True)
        self.cast = {}
        self.base = {}

    def cast_for(self, shot, assign):
        out = {}
        for mk, (story, opts) in assign.items():
            a, cast, pose, sc, pos = C.make_cast(self.A["marks"][mk], story, opts, self.cam, SPR)
            out[mk] = (a, cast, pose, sc, pos)
        return out

    def setup(self, gs):
        self.c7 = self.cast_for(7, A7); self.c8 = self.cast_for(8, A8)
        for g in gs:
            f = bf(g); sh = shot_of(g)
            loc, look = cam_of(g)
            camrig.key_camera(f, loc, look, cam=self.cam, lens=22.0, interp="LINEAR", easing="AUTO")
            K.set_flicker(1.0, frame=f); K.set_smoke(1.0, frame=f); K.set_dust(0.5, frame=f)
            if sh == 8:
                for r in self.photos:
                    d = loc - Vector((r.location.x, r.location.y, 0.0)); d.z = 0
                    r.rotation_euler = (math.radians(34), 0, math.atan2(-d.x, d.y)); r.keyframe_insert("rotation_euler", frame=f)
            for o in self.beams:
                o.hide_render = sh == 8; o.keyframe_insert('hide_render', frame=f)
            for o in self.aisle_fg + self.spill:
                o.hide_render = sh != 7; o.keyframe_insert("hide_render", frame=f)
            for o in self.desk_fg + self.photo_objs:
                o.hide_render = sh != 8; o.keyframe_insert("hide_render", frame=f)
            for mk, (a, cast, pose, sc, pos) in list(self.c7.items()) + list(self.c8.items()):
                is7 = mk in self.c7 and self.c7[mk][0] is a
                a.set_hidden(False) if False else None
                a.place(f, pos, scale=sc)
        for g in gs:
            f = bf(g); sh = shot_of(g)
            bpy.context.scene.frame_set(f)
            for mk, (a, cast, pose, sc, pos) in self.c7.items():
                a.card.hide_render = sh != 7; a.card.keyframe_insert("hide_render", frame=f)
                a.contact.hide_render = sh != 7; a.contact.keyframe_insert("hide_render", frame=f)
                a.proxy.hide_render = sh != 7; a.proxy.keyframe_insert("hide_render", frame=f)
                a.pose(f, pose_for(mk, pose, g), camera=self.cam)
            for mk, (a, cast, pose, sc, pos) in self.c8.items():
                a.card.hide_render = sh != 8; a.card.keyframe_insert("hide_render", frame=f)
                a.contact.hide_render = sh != 8; a.contact.keyframe_insert("hide_render", frame=f)
                a.proxy.hide_render = sh != 8; a.proxy.keyframe_insert("hide_render", frame=f)
                a.pose(f, scratch_pose(pose, g), camera=self.cam)
        for grp in (self.c7, self.c8):
            for mk, (a, cast, pose, sc, pos) in grp.items():
                a.render_sprites(256)

    def report(self, g):
        f = bf(g); bpy.context.scene.frame_set(f)
        loc, look = cam_of(g); heads = {}
        sh = shot_of(g)
        for mk, (a, cast, pose, sc, pos) in (self.c7 if sh == 7 else self.c8).items():
            w = actors.local_to_world(a, (0.0, 0.0), f, camera=self.cam); px, py, dz = K.project(self.cam, tuple(w))
            w2 = actors.local_to_world(a, (0.5, 0.0), f, camera=self.cam); qx, qy, _ = K.project(self.cam, tuple(w2))
            R = math.hypot(qx - px, qy - py); heads[mk] = dict(x=round(px), y=round(py), R=round(R), chin=round(py + R))
        cards = {}
        if sh == 8:
            bpy.context.view_layer.update()
            for i, r in enumerate(self.photos):
                pts = [K.project(self.cam, tuple(r.matrix_world @ Vector(p))) for p in ((-0.3, 0, -0.225), (0.3, 0, -0.225), (-0.3, 0, 0.225), (0.3, 0, 0.225))]
                cards["card%d" % i] = [round(min(p[0] for p in pts)), round(max(p[0] for p in pts)), round(min(p[1] for p in pts)), round(max(p[1] for p in pts))]
        return dict(g=g, shot=sh, cards=cards, cam=[round(v, 3) for v in loc], heads=heads)

    def render(self, g, path, scale, samples, threads=2):
        f = bf(g); bpy.context.scene.frame_set(f); bpy.context.scene.camera = self.cam
        return C.render_frame(path, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if FIRST_G <= g <= LAST_G]
    Tk = Take()
    Tk.setup(gs)
    if cmd in ("probe", "stills"):
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; os.makedirs(out, exist_ok=True); scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                dt = Tk.render(g, os.path.join(out, "g_%04d.png" % g), scale, samples); print("g %d %.1f s" % (g, dt), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 24
        out = sys.argv[5] if len(sys.argv) > 5 else os.path.join(HERE, "raw")
        os.makedirs(out, exist_ok=True)
        for g in gs:
            png = os.path.join(out, "g_%04d.png" % g)
            if os.path.exists(png + ".ok"): continue
            dt = Tk.render(g, png, scale, samples); rep = Tk.report(g); rep.update(wall=round(dt, 1), scale=scale, samples=samples)
            json.dump(rep, open(png[:-4] + ".json", "w")); open(png + ".ok", "w").write("1")
            print("g %d %.1f s" % (g, dt), flush=True)
