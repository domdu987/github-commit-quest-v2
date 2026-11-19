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
        p["blink"] = blink(g, [2010, 2058, 2084])
        if g >= 2085:
            p["expr"] = "laughing"                           # grin pop on a blink
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
        L = Vector(self.look0) + right * (-0.15 + 0.3 * math.sin(2 * math.pi * t / 4.1)) + Vector((0, 0, 0.35 * uo)) + right * (-0.5 * uo)
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
                   snaps=[dict(g=(G_WORD - 2, G_WORD + 11), k=1.5, peak=1.7, shift=(0.0, 0.0)), dict(g=SNAP, k=0.6, peak=1.7, shift=(0.0, 0.0))])
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
        wm = TG.STATE["M"]["wall"]                                  # ceiling + walls 40 % darker
        for n in wm.node_tree.nodes:
            if n.type == "VALTORGB":
                for el in n.color_ramp.elements:
                    el.color = (el.color[0] * 0.45, el.color[1] * 0.45, el.color[2] * 0.45, el.color[3])
            elif n.type == "BSDF_PRINCIPLED":
                bc = n.inputs["Base Color"].default_value
                n.inputs["Base Color"].default_value = (bc[0] * 0.45, bc[1] * 0.45, bc[2] * 0.45, bc[3])
        self.scene.view_settings.exposure -= 0.4
        M = TG.STATE["M"]
        self.build_register_corner()
        # the set's brass urn / spittoon standing at the stool (room_brass): a gourd in the foreground that covers the paper heap -> cut it out
        import bmesh, bpy
        ob = bpy.data.objects.get("room_brass")
        if ob is not None:
            mx_, my_, _ = self.A["marks"]["mocker_stool"]
            bm = bmesh.new(); bm.from_mesh(ob.data)
            dead = [v for v in bm.verts if abs(v.co.x - mx_) < 2.2 and abs(v.co.y - my_) < 2.2 and v.co.z < 1.6]
            bmesh.ops.delete(bm, geom=dead, context="VERTS")
            bm.to_mesh(ob.data); bm.free()

    def build_register_corner(self):
        """a small table with the register at his elbow (a copy of the set's instrument, scale 1.1), one continuous paper ribbon (the set's
        dot-dash tape material) from its slot over the table edge into a heap of curled ribbon at his boots"""
        import bpy, random
        M = TG.STATE["M"]
        inv = K.frame_mat().inverted()
        T = K.frame_mat()
        mx, my, mz = self.A["marks"]["mocker_stool"]
        dirx, diry = self.dir
        rx, ry = -diry, dirx                                   # screen-right on the floor
        moc = Vector((mx + 0.5 * dirx, my + 0.5 * diry, 0.0))
        tab = moc + Vector((rx, ry, 0.0)) * 1.25 + Vector((dirx, diry, 0.0)) * 0.1
        c = inv @ Vector((tab.x, tab.y, 0.0))                   # sb metres on the floor
        top = 0.50
        mb = K.MB("s30_regtable")
        mb.box(M["walnut"], (c.x, c.y, top - 0.025), (1.15, 0.62, 0.05))
        mb.box(M["baize"], (c.x, c.y, top + 0.002), (1.05, 0.52, 0.012))
        for sx in (-0.5, 0.5):
            for sy in (-0.24, 0.24):
                mb.rod(M["walnut"], (c.x + sx, c.y + sy, 0.0), (c.x + sx, c.y + sy, top - 0.05), 0.035, 0.028, 8, smooth=True)
        S = 1.1
        CH.tg_arm_parts(mb, M, (c.x, c.y, top + 0.008), S)
        self.regtable = mb.finish()
        slot = Vector((c.x + S * 0.36, c.y + S * 0.10, top + 0.008 + S * 0.172))
        tape_mat = TG.STATE["tape"].data.materials[0]
        rsb = (inv.to_3x3() @ Vector((rx, ry, 0.0))).normalized()        # screen-right in sb
        csb = inv @ Vector((moc.x, moc.y, 0.0))
        def strip(name, pts, width, vertical=False):
            """a ribbon mesh along pts (sb metres), flat (width along the floor-plane normal to the path) or as a curled band (width along z)"""
            verts, uv1, faces, cum, tot = [], [], [], [0.0], 0.0
            for i in range(1, len(pts)):
                tot += (pts[i] - pts[i - 1]).length; cum.append(tot)
            for i, p in enumerate(pts):
                t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]); t.normalize()
                w = Vector((0, 0, 1.0)) if vertical else t.cross(Vector((0, 0, 1.0)))
                if w.length < 0.2:
                    w = Vector((1.0, 0, 0))
                w = w.normalized()
                verts += [tuple(T @ (p - w * width / 2)), tuple(T @ (p + w * width / 2))]
                uv1 += [(cum[i] / 0.8, 0.0), (cum[i] / 0.8, 1.0)]
            for i in range(len(pts) - 1):
                a_ = 2 * i; faces.append((a_, a_ + 1, a_ + 3, a_ + 2))
            me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
            u1 = me.uv_layers.new(name="UVMap"); u2 = me.uv_layers.new(name="CLIP")
            for poly in me.polygons:
                for li, vi in zip(poly.loop_indices, poly.vertices):
                    u1.data[li].uv = uv1[vi]; u2.data[li].uv = (0.0, 0.0)
            me.materials.append(tape_mat)
            ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = True
            return ob
        def cr(pp, n=10):
            out = []
            for i in range(len(pp) - 1):
                p0, p1, p2, p3 = pp[max(0, i - 1)], pp[i], pp[i + 1], pp[min(len(pp) - 1, i + 2)]
                for k in range(n):
                    t = k / float(n)
                    out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
            out.append(pp[-1]); return out
        edge = c - rsb * 0.58
        heap = csb + rsb * 0.12
        path = cr([slot, slot + Vector((-0.1, -0.22, -0.03)) + rsb * -0.05, Vector((c.x, c.y, top + 0.014)) - rsb * 0.3 + Vector((0.0, -0.2, 0.0)),
                   Vector((edge.x, edge.y - 0.12, top + 0.01)), Vector((edge.x - rsb.x * 0.08, edge.y - 0.12 - rsb.y * 0.08, top - 0.12)),
                   Vector((edge.x - rsb.x * 0.2, edge.y - rsb.y * 0.2, 0.30)), Vector((heap.x + 0.15, heap.y, 0.04)), Vector((heap.x, heap.y + 0.1, 0.03))])
        self.ribbon = [strip("s30_ribbon", path, 0.11)]
        rr = random.Random(21)
        for i in range(12):                                  # curled paper heap round his boots
            cx, cy = heap.x + rr.uniform(-0.4, 0.4), heap.y + rr.uniform(-0.28, 0.28)
            r0, turns, h0 = rr.uniform(0.07, 0.17), rr.uniform(1.0, 2.2), rr.uniform(0.01, 0.07)
            pts = []
            for k in range(26):
                u = k / 25.0; ang = rr.uniform(0, 0) + u * turns * 6.283 + i
                pts.append(Vector((cx + r0 * (1 - 0.3 * u) * math.cos(ang), cy + r0 * (1 - 0.3 * u) * math.sin(ang), h0 + 0.12 * u * (1 + 0.5 * math.sin(i)))))
            self.ribbon.append(strip("s30_curl%d" % i, pts, 0.075, vertical=True))
        for i in range(5):                                   # a few loose flat strips
            cx, cy, ang = heap.x + rr.uniform(-0.5, 0.5), heap.y + rr.uniform(-0.35, 0.35), rr.uniform(0, 6.28)
            pts = [Vector((cx + k * 0.06 * math.cos(ang) + 0.03 * math.sin(k), cy + k * 0.06 * math.sin(ang), 0.012 + 0.01 * k)) for k in range(9)]
            self.ribbon.append(strip("s30_loose%d" % i, pts, 0.1))
        # candle light at chest height between his hand and the register
        tl = moc + Vector((rx, ry, 0.0)) * 0.55
        for ob, e in TG.STATE["lamps"]["nightc"]:
            ob.location = Vector((tl.x, tl.y, 2.05))
            ob.data.energy = e * 3.6

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            for k, a in self.actors.items():
                x, y, z = self.A["marks"][CAST[k]["mark"]]
                if k == "moc":                                    # a little toward the lens so the set's stool does not hide his legs
                    x, y = x + 0.5 * self.dir[0], y + 0.5 * self.dir[1]
                if k == "mor":                                    # 0.9 D further into the lit opening, 15 % bigger
                    _o = [float(v) for v in os.environ.get('MOFF', '-0.35,0').split(',')]
                    x, y = x + _o[0], y + _o[1]
                    C.place(a, f, (x, y, z), scale=1.15)
                else:
                    C.place(a, f, (x, y, z))
            click = 1 if (g % 9) < 3 else 0
            self.key_set(f, tape=(0.0, click), flames=(1.0,), moneybag=(False,), mailsacks=(False,))
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
