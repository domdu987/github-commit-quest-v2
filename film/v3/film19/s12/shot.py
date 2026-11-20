#!/usr/bin/env python3
"""shot.py -- film 19 take s12 = MERGED shots 12 + 13 (WORKSHOP NIGHT, set_clock(3)), ONE continuous camera, no cut (client rule QA_TEAM §I):
"เครื่องที่สาม สิบกว่าปี จนผมหงอกทั้งหัว" (31.26-33.86 s, g 938..1015).  Take = g 929..1024: 9-frame dissolve in-handle g 929..937, shot g 938..1015,
9-frame out-handle g 1016..1024 (dissolve 11 f into shot 14).
    g 938..965   greying Harrison (default) taps a chisel at the H3 by candlelight (shop_clock spot), the camera slides along the bench
    g 955..972   the lateral WHIP PAN (SNAP, on "สิบ" of "สิบกว่าปี", caption 31.91 = g 960) travels along the bench to the shop_bench spot;
                 at the fastest frames (g 961) the SAME Harrison's look swaps default -> old=1 (white hair, spectacles, brown coat): the whip
                 hides the pop
    g 973..992   white-haired Harrison bends over the H3, tired
    g 993..1003  "จนผมหงอกทั้งหัว" (caption 32.85 = g 989; หงอก spoken ~g 996): he leans back and rubs his eyes (sweat drop), g 1003.. keeps rubbing
The bench candle stub (moved onto the foreground chest) burns down 1.0 -> 0.3 and the room lights fall over the whole take.
NO DOF, NO text, NO caption_shade.   Mouths: nobody speaks: fixed expression mouth.

    python3 shot.py probe a:b[:step]       numbers only        python3 shot.py camreport
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]     (resumable; two processes e.g. 853:946:2 / 854:946:2)
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(31.26), C.g_bound(33.86)            # 938, 1016: merged shots 12+13 = g 938..1015
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1            # 929 .. 1024
GS = list(range(G_FIRST, G_LAST + 1))
G_WORD = C.cap_g("สิบกว่าปี")                          # 960: caption start; "สิบ" spoken right at it
SNAP = (G_WORD - 8, G_WORD + 12)                       # 955..969 (14 f)
G_AGE = 996                                            # the look swap, at the fastest frames of the whip pan
G_W2 = C.cap_g("จนผมหงอกทั้งหัว")                      # 989
G_LEAN = (G_W2 + 4, G_W2 + 11)                         # 993..1000: slumps back (squash), then the eye-rub
BLINKS = [950, 980]

LIGHT, PRESET, CLOCK = "NIGHT", "shop_clock", 3
FINAL_SPP = 8
PPD = 256
CANVAS = None

MARK = "harrison_bench"
MARK_DX = float(os.environ.get("MARK_DX", 0.2))
MARK_DY = float(os.environ.get("MARK_DY", -2.8))
CAM_LOC0 = tuple(float(v) for v in os.environ.get("CAM_LOC0", "2.2,-1.6,2.4").split(","))
CAM_LOOK0 = tuple(float(v) for v in os.environ.get("CAM_LOOK0", "2.6,2.9,2.3").split(","))
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=float(os.environ.get("PUSH", 0.06)), slide_px=float(os.environ.get("SLIDE", -60)),
                rise_px=float(os.environ.get("RISE", 0)), arc_deg_s=float(os.environ.get("ARC", 0)), decay=0.25,
                snaps=[dict(g=SNAP, k=float(os.environ.get("SNAPK", 1.05)), peak=float(os.environ.get("SNAPPEAK", 3.0)), shift=(float(os.environ.get("SNAPSX", 1.4)), -0.1)),
                       dict(g=(970, 996), k=1.0, peak=1.0, shift=(float(os.environ.get("SETTLE", -0.9)), 0.0))])   # the whip overshoots, then settles back left

SWAY = float(os.environ.get("SWAY", 0.09))
TRAVEL = float(os.environ.get("TRAVEL", 0.9))              # D: look point moves right (camera turns, does not move) after the pan lands


def cam_at(g):
    loc, look = CAM.at(g)
    fwd = (look - loc).normalized()
    right = Vector((fwd.y, -fwd.x, 0.0)).normalized()
    u = u_of(g, 972, 1000, kind="sine")
    look = look + right * (TRAVEL * u)
    up = right.cross(fwd).normalized()
    ph = 2 * math.pi * g / 20.0                           # handheld sway (D): 1.5 Hz lateral + a little vertical, no net drift
    off = right * (SWAY * math.sin(ph)) + up * (0.5 * SWAY * math.sin(ph * 0.7 + 1.0))
    return loc + off, look + off


BASE = dict(cast19.STORY19["harrison_chisel"][1])


BASE_OLD = dict(cast19.STORY19["harrison_tired_rub"][1])


G_POP = (G_AGE - 1, G_AGE + 6)                          # the hair pops white on "หงอก": puff + squash


def _puff(g):
    return math.sin(math.pi * u_of(g, G_POP[0], G_POP[1]))     # 0..1..0 over g 995..1002


def pose_of(g):
    old = g >= G_AGE
    p = dict(BASE)                                        # harrison_chisel: the chisel stays in his hand the whole take
    p["mirror"] = True                                    # the H3 is at screen-left of him
    ph = 2 * math.pi * g / 14.0                           # ~2 Hz tapping
    lk = u_of(g, *G_LEAN, kind="sine")                    # 0 working -> 1 slumped back (g 993..1000), then the eye-rub
    pf = _puff(g)
    tap = 0.16 * max(0.0, math.sin(ph)) * (1.0 - lk)
    # right hand: taps the chisel; after the slump the chisel hangs low in it (angle -> pointing down), never vanishes
    p["arm_r"] = dict(hand=(lerp(0.78 + 0.5 * tap, 0.55, lk), lerp(1.0 - tap, 1.15, lk)), bend=0.2, layer="front", stretch=1.2)
    p["prop_r"] = dict(type="chisel19", angle=lerp(40 - 25 * tap * 6, 150.0, lk))
    # left hand: comes up to the eyes (the rub) after the slump
    rub = math.sin(2 * math.pi * g / 9.0)
    p["arm_l"] = dict(hand=(lerp(0.60, -0.04 + 0.05 * rub, lk), lerp(1.1, 0.06 + 0.03 * math.sin(2 * math.pi * g / 9.0 + 1.2), lk)),
                      bend=lerp(0.3, -0.5, lk), layer="top" if lk > 0.5 else "front", shape="open" if lk > 0.5 else None)
    if p["arm_l"].get("shape") is None:
        p["arm_l"].pop("shape")
    p["lean"] = lerp(8 + 1.5 * math.sin(ph), -15.0, lk) - 4.0 * pf          # real slump: 15 deg back
    p["pitch"] = lerp(0.30 + 0.05 * math.sin(ph), -0.18, lk)
    p["head_roll"] = lerp(0.0, 8.0, lk) + 1.5 * math.sin(g * 0.3) * lk
    p["yaw"] = lerp(0.5, 0.2, lk)
    p["gaze"] = (lerp(0.7, 0.0, lk), lerp(0.9, 0.0, lk))
    p["squash"] = (1.0 + 0.07 * pf + 0.03 * lk * (1 - pf), 1.0 - 0.07 * pf - 0.03 * lk * (1 - pf))
    if old:
        p["old"] = 1                                      # hair white (+ spectacles, brown coat): popped on "หงอก"
        p["expr"] = "worried"
        p["blink"] = 2 if lk > 0.8 else blink(g, BLINKS)
        p["fx"] = (["steam"] if pf > 0.15 else []) + (["sweat"] if lk > 0.9 and g > G_POP[1] else [])
    else:
        p["expr"] = "determined" if lk < 0.5 else "worried"
        p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


def bounce_z(g):
    """a little hop on the pop"""
    return 0.06 * _puff(g)


def candle_level(g):
    """the bench candle stub burns down over the whole take (1.0 -> 0.25)"""
    return lerp(1.0, 0.25, clamp((g - G0) / float(G1 - G0)))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s12m")
        self._base = {}
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        # the bench candle stub moves from the far left of the bench to the bench top at his right shoulder, so it stays in frame while it burns down
        st = H.STATE["stub"]
        st["pv"].location = (1.7, 0.8, 0.56)
        st["base"] = (1.7, 0.8, 0.56)
        for o, _b in H.STATE["lampgroups"]["candle"]:
            if o.name == "p_bench":
                o.location = (1.7 * 1.85, 0.8 * 1.85, 1.6)
        self.key_cam(bf(G_FIRST), *cam_at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", os.path.join(WORK, "sprites"), canvas=CANVAS, contact=True, cam=self.cam)

    def _make_wipe(self):
        """a dark foreground slab (a beam passing close to the lens) sweeps across the frame around the age swap (g 958..964, full cover
        at g 961), parented to the camera; emissive flat dark wood so it needs no light.  It hides the hair swap with the motion blur."""
        bpy = C.bpy
        me = bpy.data.meshes.new("wipe_m")
        w, h = 0.42, 1.6
        me.from_pydata([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], [], [(0, 1, 2, 3)])
        ob = bpy.data.objects.new("wipe", me)
        bpy.context.scene.collection.objects.link(ob)
        mat = bpy.data.materials.new("wipe_mat")
        mat.use_nodes = True
        nt = mat.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = 1.0
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (2.0, 40.0, 1.0)            # long vertical wood grain
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 6.0
        nz.inputs["Detail"].default_value = 6.0
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (0.020, 0.011, 0.006, 1.0)
        ramp.color_ramp.elements[1].color = (0.11, 0.063, 0.034, 1.0)
        nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
        nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
        me.materials.append(mat)
        ob.parent = self.cam
        ob.location = (3.0, 0.0, -0.6)
        ob.visible_shadow = False
        ob.visible_diffuse = False
        ob.visible_glossy = False
        self.wipe = ob

    def key_wipe(self, f, g):
        ob = self.wipe
        u = clamp((g - 957.0) / 8.0)
        on = 957 <= g <= 965
        x = lerp(0.7, -0.7, ez(u, "sine"))             # frame half-width at 0.6 D is 0.275 D; the 0.42 D slab hides the centre 0.42 D at g 961 (face), the frame edges stay visible
        ob.location = (x if on else 3.0, 0.0, -0.6)
        ob.keyframe_insert("location", frame=f)
        ob.hide_render = not on
        ob.keyframe_insert("hide_render", frame=f)

    def pose(self, gs):
        mark = Vector(self.A["marks"][MARK]) + Vector((MARK_DX, MARK_DY, 0))
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g))
            C.place(self.har, f, mark + Vector((0, 0, bounce_z(g))))
            self.key_set(f, clock=CLOCK, balance=g / 30.0, candles=candle_level(g))
            self.dim(f, g)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.har.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.har, PPD)], [bf(g) for g in gs])

    def dim(self, f, g):
        """the room gets darker as the candle burns down: candle lights x1 -> 0.55, other lamps / fills / moon key x1 -> 0.7, the flame
        emission follows the stub; keyed on every frame.  (set_candles resets the candle lights and flame every call, so those are
        scaled after it; the other lights are scaled from their stored base.)"""
        u = clamp((g - G0) / float(G1 - G0))
        for grp, items in H.STATE["lampgroups"].items():
            for o, _b in items:
                if grp == "candle":
                    o.data.energy = o.data.energy * lerp(1.0, 0.45, u)
                else:
                    self._base.setdefault(o.name, o.data.energy)
                    o.data.energy = self._base[o.name] * lerp(1.0, 0.45, u)
                o.data.keyframe_insert("energy", frame=f)
        em = H.STATE["M"]["flame"].node_tree.nodes["Emission"].inputs["Strength"]
        em.default_value = em.default_value * lerp(1.0, 0.5, u)
        em.keyframe_insert("default_value", frame=f)
        sun = H.STATE.get("sun")
        if sun is not None:
            self._base.setdefault("sun", sun.data.energy)
            sun.data.energy = self._base["sun"] * lerp(1.0, 0.45, u)
            sun.data.keyframe_insert("energy", frame=f)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_at(g)
        bars = C.clock_world(CLOCK, (0.0, 0.0, 0.64))
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), h1_bars_px=H.project(tuple(bars)),
                    dof=self.cam.data.dof.use_dof, caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        r = self.scene.render
        whip = False and any(958 <= g <= 964 for g in gs)   # motion blur dropped: QA_AUTO flags blurred frames; the wipe slab hides the swap
        r.use_motion_blur = bool(whip)                  # camera motion blur on the whip-pan frames only (shutter 0.5)
        r.motion_blur_shutter = 0.5
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
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
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
