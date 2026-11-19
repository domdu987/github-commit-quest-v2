#!/usr/bin/env python3
"""shot.py -- film 16 take s30 = shot 30 (CHAMBER chamber_table_night / NIGHT, candles): the ENDING.  The mocker alone on the stool beside the clicking
register, candle in hand, yawning with sleep Z, tape piled round his boots; Morse grins in the lit side doorway; slow pull back, snap push on
'นั่งเฝ้าลวด'; HARD CUT on 'เอง' (g 2096).  Shot g 1980..2095 (66.01-69.85 s), 9 f handle in (17 f dissolve), 4 f out.  Mouths still (yawn = held expression mouth).
    python3 shot.py probe a:b | camreport | stills a:b[:s] out [scale] [spp] | final a:b[:s] [scale] [spp]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector, Matrix                             # noqa: E402
import tg_chamber as CH                                  # noqa: E402
TG, K, actors, cast16 = C.TG, C.K, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(66.01), C.g_bound(69.85)             # 1980, 2096 (shot = g 1980..2095; the hard cut falls on 'เอง')
H_IN, H_OUT = 9, 4                                       # 17 f dissolve in (9 f handle), 4 f out handle (the film ends at g 2099)
GS = list(range(G0 - H_IN, G1 + H_OUT))
G_LAST = GS[-1]
G_WORD = C.cap_g("นั่งเฝ้าลวด")                           # 2026: snap push on 'sit and guard the wire'
SNAP = (2058, 2070)                                      # SNAP OUT (pull-back reveal) on "ของไอ้บ้าลวด" (68.22 s -> g 2056): the wide empty chamber
PPD = 256
import re as _re
_orig_candle = cast16._candle_body
def _candle_solid(k, t=0.0):
    """cast16 candle without the two translucent glow discs (they read as an un-composited sprite at the cuff)"""
    return _re.sub(r'^<circle[^>]*/><circle[^>]*/>', '', _orig_candle(k, t))
cast16._candle_body = _candle_solid
LIGHT, PRESET = "NIGHT", "chamber_table"                 # the preset camera at NIGHT = chamber_table_night
CAST = dict(moc=dict(cast="mocker", mark="mocker_stool", mirror=False), mor=dict(cast="morse16", mark="morse_door", mirror=False))
NOD = [(1992, 2004), (2030, 2044), (2062, 2078)]         # head-nod windows between the yawns (alternate poses)

def P(name):
    return dict(cast16.STORY16[name][1])

def pose_of(k, g):
    t = g / 30.0
    if k == "moc":
        nod = any(a <= g < b for a, b in NOD)
        p = P("mocker_stool_candle_nod" if nod else "mocker_stool_candle")
        p["hat_off"] = 0                                             # the black stovepipe stays on (continuity with shots 26-29)
        p["blink"] = blink(g, [a - 1 for a, b in NOD] + [b - 1 for a, b in NOD])
        p["lean"] = p.get("lean", 0) + 1.5 * math.sin(t * 2.2)
        p["squash"] = (1.0, 1.0 + 0.012 * math.sin(t * 5.0))     # slow breathing
        p["fx"] = [dict(type="zzz", t=(g / 40.0) % 1.0)]          # the sleep Z
    else:
        p = P("morse_peek_door")
        p["blink"] = blink(g, [2010, 2058])
        p["head_roll"] = p.get("head_roll", 0) + 3.0 * math.sin(t * 4.0)
        p["lean"] = p.get("lean", 0) + 2.0 * math.sin(t * 3.0)
    p["mirror"] = CAST[k]["mirror"]
    p["t"] = t
    return p

class Cam3(C.CamPath):
    """subject-locked: CamPath gives the zoom (drift + snaps -> distance); the look point sways about the mocker (+-0.5 D) and the heading swings +-14 deg, so the
    background has parallax but he never leaves the frame; the snap-out also pans (reveal)."""
    def at(self, g):
        loc, look = C.CamPath.at(self, g)
        dist = (look - loc).length
        t = (g - GS[0]) / 30.0
        fwd0 = (self.look0 - self.loc0)
        fwd0.z = 0
        fwd0.normalize()
        ang = math.radians(14.0 * math.sin(2 * math.pi * t / 5.2 + 0.4))
        fwd = Matrix.Rotation(ang, 3, "Z") @ fwd0
        right = Vector((fwd.y, -fwd.x, 0.0))
        uo = 0.0 if g <= SNAP[0] else min(1.0, C.camrig.ease_peak((g - SNAP[0]) / float(SNAP[1] - SNAP[0]), 1.7))
        L = Vector(self.look0) + right * (0.3 * math.sin(2 * math.pi * t / 4.1)) + Vector((0, 0, 0.35 * uo)) + right * (0.45 * uo)
        pitch = Vector((fwd.x, fwd.y, (self.look0.z - self.loc0.z) / max(1e-6, fwd0.length)))
        pitch.normalize()
        return L - pitch * dist, L

CAM = None

class Take(C.Take):
    def __init__(self, quality="preview"):
        global CAM
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s30")
        c0 = Vector(self.A["cam"]["loc"]); l0 = Vector(self.A["cam"]["look_at"])
        d = c0 - l0; d.z = 0; d.normalize(); self.dir = (d.x, d.y)         # the preset night axis: register right, lit doorway + Morse left
        mx, my, mz = self.A["marks"]["mocker_stool"]
        look0 = Vector((mx, my, 2.45)) + Vector((-0.5, 0.85, 0.0)) * 0.9
        loc0 = look0 + d * 4.3 + Vector((0, 0, -0.05))
        CAM = Cam3(loc0, look0, G0 - H_IN, G_LAST, push=-0.07, slide_px=0.0, arc_deg_s=0.0, decay=0.2,
                   snaps=[dict(g=(G_WORD - 2, G_WORD + 11), k=1.5, peak=1.7, shift=(0.0, 0.0)), dict(g=SNAP, k=0.68, peak=1.7, shift=(0.0, 0.0))])
        self.night_look()
        self.key_cam(bf(GS[0]), *CAM.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        for k, v in CAST.items():
            self.actors[k] = C.make_actor(k, v["cast"], os.path.join(WORK, "sprites"), canvas=cast16.CANVAS16[v["cast"]], contact=True, cam=self.cam)
    def night_look(self):
        """candle-pool night: ambient / window fill about 45 % down, candle + lamp pools up; the set's evenly spread tape loops are
        hidden (tape clip short of the floor loops) and replaced by a heap of crumpled paper round the stool"""
        import bpy, random
        P = TG.STATE["P"]
        for ob, e in TG.STATE["lamps"]["win"]:
            ob.data.energy = e * 0.35
        w = bpy.context.scene.world
        if w and w.node_tree:
            for n in w.node_tree.nodes:
                if n.type == "BACKGROUND":
                    n.inputs["Strength"].default_value *= 0.35
        P["lamp"] = P.get("lamp", 1.0) * 1.0
        for ob, e in TG.STATE["lamps"]["nightc"]:
            ob.data.energy = e * 2.2
        self.scene.view_settings.exposure -= 0.4
        M = TG.STATE["M"]
        rr = random.Random(11)
        sx, sy = CH.STOOL
        mb = K.MB("s30_pile")
        for i in range(46):
            a = rr.uniform(0, 6.283); r = rr.uniform(0.12, 0.62) * (1.0 - 0.0 * i)
            z = 0.012 + 0.28 * (1.0 - r / 0.7) ** 1.5 * rr.uniform(0.3, 1.0)
            mb.box(M["paper"], (sx + 0.27 * self.dir[0] + r * math.cos(a), sy + 0.27 * self.dir[1] + r * math.sin(a) * 0.9, z),
                   (rr.uniform(0.30, 0.55), 0.085, 0.012), rz=rr.uniform(0, 3.14), rx=rr.uniform(-0.5, 0.5), ry=rr.uniform(-0.5, 0.5))
        # a paper ribbon from where the set's tape reaches the floor (table front) over the carpet edge into the heap
        p0 = Vector((-0.12, 3.14)); p1 = Vector((sx + 0.27 * self.dir[0] - 0.1, sy + 0.27 * self.dir[1] + 0.05))
        n = 26
        for i in range(n):
            u0, u1 = i / float(n), (i + 1) / float(n)
            pts = []
            for u in (u0, u1):
                c = p0.lerp(p1, u)
                w = 0.28 * math.sin(u * 7.0) * (1 - u * 0.5)
                pts.append(Vector((c.x, c.y + w)))
            t = (pts[1] - pts[0]); t.normalize(); nrm = Vector((-t.y, t.x)) * 0.075
            zz0 = 0.02 + 0.03 * math.sin(u0 * 11.0) + 0.14 * u0 ** 3; zz1 = 0.02 + 0.03 * math.sin(u1 * 11.0) + 0.14 * u1 ** 3
            mb.quad(M["paper"], [(pts[0].x - nrm.x, pts[0].y - nrm.y, zz0), (pts[0].x + nrm.x, pts[0].y + nrm.y, zz0),
                                 (pts[1].x + nrm.x, pts[1].y + nrm.y, zz1), (pts[1].x - nrm.x, pts[1].y - nrm.y, zz1)])
        self.pile = mb.finish()

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            for k, a in self.actors.items():
                x, y, z = self.A["marks"][CAST[k]["mark"]]
                if k == "moc":                                    # a little toward the lens so the set's stool does not hide his legs
                    x, y = x + 0.5 * self.dir[0], y + 0.5 * self.dir[1]
                C.place(a, f, (x, y, z))
            click = 1 if (g % 9) < 3 else 0
            self.key_set(f, tape=(0.27, click), flames=(1.0,))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, a in self.actors.items():
                a.pose(f, pose_of(k, g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])
    def report(self, g):
        f = bf(g)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))
    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        Take("preview")
        rows, worst = CAM.report(GS[:-1])
        print(rows[::5]); print("longest run under 0.25 px/frame: %d" % worst); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GS[0] <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; spp = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=spp)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["chamber"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
