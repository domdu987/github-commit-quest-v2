#!/usr/bin/env python3
"""shot.py -- film 16 take s23 = shot 23, THE CALLBACK of shot 1 (g 1455..1539 + 9 handle frames each side; hard CUT in at 1455 and out at 1540), AFTER_RAIN.
"เขาเลยคว่ำ คอขวดเบียร์ บนหัวเสา แล้วพาดลวด ไว้บนขวด" -- so he turned the beer-bottle neck over the pole top and draped the wire on the glass.
Same camera + marks as s01 (the reuse of its bottle-hand method), now with the reason.

LINE line_close / DAY (the plan's light; the approved hook tiles L01 AFTER_RAIN / L02 DAY share the camera and set state, and
shot 23 repeats this framing in AFTER_RAIN).  Morse stands on the leaning ladder at mark morse_ladder (rung 12) beside hero pole 1.
    g  0..21  he holds the big inverted green bottle up over the bare pole top; camera already moving (push + slide + arc)
    g 22..35  SNAP push x2.8 with a sideways pan on "คอขวดเบียร์" (event g 24): the held bottle flashes a sun glint (g 24..31)
    g 34..47  he lowers the bottle mouth-down onto the pole top; g 47 CONTACT (glass clink): the set's peg + bottle switch on
              (peg1_wood / peg1_glass / peg1_glintm visible), the hand-held copy switches off, a star glint flashes (g 47..56)
    g 51..53  blink; the pose switches cap -> drape (morse_drape_wire, coil on the other arm)
    g 52..64  the raised hand takes the wire at the coil on his other arm (the slack wire runs pole 0 -> coil -> pole 2 until
              then) and flicks it up over the glass; it overshoots and settles
    g 65      the set's wire spans 0 + 1 and the wrap ring (peg1_wiremat) switch on, the per-frame slack wire off
    g 66..74  pleased look (behind the blink at g 65), idle sway; the camera keeps moving through the handle (cut at g 69)
Mouths: nobody speaks (no quote): expression mouths only.  NO depth of field, NO text.

The camera (c16.CamPath): low, on the road side of the ladder looking up 33 deg past the ladder rails (lower right of the frame)
at Morse and the pole top; the trees and the wheat fill the bottom.  Drift push 10 %/s + slide 60 px/s + arc 14 deg/s round the
subject, decaying to 75 % (still moving on the last frame: hard cut), plus the snap.  The values were tuned on drafts for the
frame-diff target (QA.md): x1.35 / 16 f snaps and pure pushes gave median 2.3 / p90 4.3.

    python3 shot.py probe a:b[:step]                       numbers only (camera, heads, hand errors), no render
    python3 shot.py camreport                              CamPath corner speed per frame (never parked check), no bpy scene
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]     -> raw/g_%04d.png + .json (resumable; run 2 processes, e.g. 0:74:2 / 1:74:2)
    python3 shot.py final 0:74:2 0.5 6                     DRAFT (360x640, 6 spp) -> work/draft/ (same loop)
    python3 deliver.py                                     -> frames/, take.mkv, meta.json, cues.json, contact.jpg, framediff numbers
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402  (paths, cast16 first, bpy, telegraph, stage)
from mathutils import Vector, Matrix, Euler              # noqa: E402

TG, K, LN, actors, cast16 = C.TG, C.K, C.LN, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing (film frames g)
G0, G1 = C.g_bound(48.51), C.g_bound(51.32)   # 1455, 1540: shot 23 = g 1455..1539; shot 24 (hard cut) starts at 1540
H_IN = H_OUT = 9                               # handles g 1446..1454 and 1540..1548 (rendered in 3D)
G_FIRST = G0 - H_IN
G_LAST = G1 + H_OUT - 1                        # 1548
GS = list(range(G_FIRST, G_LAST + 1))
G_WORD = 1475                                  # caption "คอขวดเบียร์" (49.08 s)
G_INV = 1495                                   # "บนหัวเสา"
SNAP = (G_WORD - 2, G_WORD + 11)
G_GLINT1 = (G_WORD, G_WORD + 7)                # sun glint on the held bottle
G_LOWER = (1484, 1494)
G_CAP = 1494
G_GLINT2 = (G_CAP, G_CAP + 9)
G_SWAP = 1499
G_PICK = (1503, 1507)
G_FLICK = (1507, 1513)
G_SETTLE = (1513, 1523)
G_WIRE = 1524
HAND_DOWN = (G_CAP + 1, G_PICK[0])                  # after the cap the free hand comes down the pole side to chest height (never across the face)
BLINKS = [1465, G_SWAP - 1, G_WIRE]              # blink(g, starts): half, closed, half
G_HAPPY = G_SWAP                           # expression change on the closed frame of the last blink

# ----------------------------------------------------------------------------- staging (world D; set authored in sb metres, K.W converts)
LIGHT = "AFTER_RAIN"
PRESET = "line_close"
POLE = 1                                       # hero pole (pole 0 hides behind this camera)
PX = LN.px(LN.POLES_Y[POLE]) + 0.03            # pole axis, sb metres (build_poles uses px(y) + 0.03)
PY = LN.POLES_Y[POLE]
# world points are FUNCTIONS: K.W() depends on the location's frame rotation, which TG.build sets (LINE: -90 deg) -- a module-level
# K.W() call at import time silently gives the wrong place (s01's first probe missed by 20 D).
TOP = lambda: K.W((PX, PY, LN.POLE_H + 0.01))  # bottle mouth on the pole top (world D, z 9.27)
BOTTLE_TOP_SB = lambda i: (LN.px(LN.POLES_Y[i]) + 0.03, LN.POLES_Y[i], LN.POLE_H + 0.01 + LN.BOT_TOP * LN.BS + 0.03)   # wire end points (= build_poles top_b)
COIL_LOCAL = (0.42, 0.72)                      # puppet-local centre of the wire coil on his (mirrored) lower arm, both poses
NECK = 0.32                                    # hand on the neck: D above the mouth
LIFT = Vector((0.14, 0.12, -0.05))           # held bottle mouth offset from TOP before lowering (toward Morse, up)
FLICK_UP = 0.42                                # wire overshoot above the bottle top (D)
PPD = 256                                      # sprite px per D (head ~90 px at g 0, ~280 px after the snap: 256 keeps it sharp enough)
CANVAS = (-2.25, -4.75, 2.25, 0.125)           # taller than CANVAS16['morse16'] (top -3.875): arm up + the low-angle upper_k stretch
                                               # (~1.2 here) clipped his hair flat in the first close drafts

CAM_LOC0 = (2.3, -2.6, 5.3)                    # low, SW of the ladder, looking up ~38 deg (card limit: 50 deg)
CAM_LOOK0 = (7.4, -7.9, 8.8)                 # subject point: Morse's raised hand / the pole top (lower = less empty sky)
CAM_START = 1.0                               # frame 0 starts 0.92 of the way from the look point to CAM_LOC0 (head ~92 px; the snap takes it to ~190)
CAM = C.CamPath(Vector(CAM_LOOK0).lerp(Vector(CAM_LOC0), CAM_START), CAM_LOOK0, G0, G_LAST, push=0.06, slide_px=60.0, rise_px=0.0,
                arc_deg_s=18.0, decay=0.25, snaps=[dict(g=SNAP, k=2.5, peak=2.3, shift=(-0.3, 0.0)), dict(g=(1522, 1536), k=1.0, peak=1.9, shift=(-0.45, 0.55))])


MARK_SHIFT = Vector((-0.25, -0.22, -0.6))      # Morse stands ~1 rung lower ALONG the ladder: his head clears the bottle body (QA-art: bottle merged with his head)


def tune_look(wet_pole):
    """runtime material tuning (the set's modules are untouched): clear dense bottle-green glass (alpha 1 + transmission: no hashed-alpha grain),
    and for AFTER_RAIN a dark wet pole (QA-art: salmon pole)."""
    M = TG.STATE["M"]
    bs = [n for n in M["glass"].node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
    bs.inputs["Alpha"].default_value = 1.0
    bs.inputs["Transmission Weight"].default_value = 0.8
    bs.inputs["Base Color"].default_value = (0.02, 0.30, 0.07, 1.0)
    bs.inputs["Emission Strength"].default_value = 0.22
    if wet_pole:
        darken(M["pole"], (0.27, 0.25, 0.31), 0.20)


def darken(mat, tint, rough):
    """multiply the (texture-driven) base colour of a material by `tint` and make it glossier (wet)."""
    nt = mat.node_tree
    bs = [n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"][0]
    bs.inputs["Roughness"].default_value = rough
    lk = [l for l in nt.links if l.to_socket == bs.inputs["Base Color"]]
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type, mix.blend_type = "RGBA", "MULTIPLY"
    mix.inputs[0].default_value = 1.0
    mix.inputs[7].default_value = (tint[0], tint[1], tint[2], 1.0)
    if lk:
        src = lk[0].from_socket
        nt.links.remove(lk[0])
        nt.links.new(src, mix.inputs[6])
    else:
        mix.inputs[6].default_value = tuple(bs.inputs["Base Color"].default_value)
    nt.links.new(mix.outputs[2], bs.inputs["Base Color"])


def bottle_xf(g):
    """(mouth world point, tilt deg) of the hand-held bottle copy at film frame g (it is on the pole from G_CAP on)."""
    if g >= G_CAP:
        return Vector(TOP()), 0.0
    u = u_of(g, *G_LOWER)
    hover = 0.05 * math.sin(g * 0.35) * (1.0 - u)                       # held up: a small live bob
    m = Vector(TOP()) + LIFT * (1.0 - u) + Vector((0, 0, hover))
    return m, lerp(9.0, 0.0, u)


def wire_point(g, coil):
    """world point the slack wire is held at (where its two half spans meet) at frame g.  Until G_FLICK it runs pole 0 -> coil (on his
    arm, chest height) -> pole 2.  The flick lifts it in an arc up and over the glass; it then FALLS onto the glass and bounces twice
    (damped) before the wrap ring appears."""
    top = Vector(K.W(BOTTLE_TOP_SB(POLE)))
    if g < G_FLICK[0]:
        return Vector(coil)
    if g < G_FLICK[1]:
        u = u_of(g, *G_FLICK, kind="sine")
        over = top + Vector((0, 0, FLICK_UP))
        mid = Vector(coil).lerp(over, u)
        mid.z += 0.35 * math.sin(math.pi * u)                           # arcs up and over, not through the glass
        return mid
    t = g - G_FLICK[1]
    h = FLICK_UP * math.exp(-0.45 * t) * abs(math.cos(0.55 * math.pi * t))
    return top + Vector((0, 0, h))


def wire_sag(g):
    """extra sag of the slack wire (sb metres, as LN.SAG) easing to the set's 0.55 when it settles."""
    return lerp(0.75, LN.SAG, u_of(g, G_PICK[0], G_SETTLE[1]))


# ----------------------------------------------------------------------------- poses (cast16 STORY16 hook poses, mirrored: he faces the pole)
CAP = cast16.STORY16["morse_cap_peg"][1]
DRAPE = cast16.STORY16["morse_drape_wire"][1]


def pose_of(g):
    """the drawn pose of frame g; the raised hand is pinned in hands_of().  Mirror: in this camera the pole is screen-LEFT of him."""
    if g < G_SWAP:
        p = dict(CAP)
        p.pop("prop_r", None)                                          # the bottle is the 3D copy of the set's glass (c16 GOTCHAS)
        p["glint"] = 0.0
        p["prop_l"] = "wire_coil"                                      # he carries the coil all along (it is on his arm in the drape)
        p["arm_l"] = dict(hand=(-0.50, 0.70), bend=0.6)
        p["legs"] = dict(stride=0.45, lift_l=0.85, crouch=0.06 + 0.08 * u_of(g, *G_LOWER))   # dips with the lowering
    else:
        p = dict(DRAPE)
    p["mirror"] = True
    p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.21)
    p["head_roll"] = 2.0 * math.sin(g * 0.15 + 0.6)
    p["blink"] = blink(g, BLINKS)
    if g >= G_HAPPY:
        p["expr"], p["mouth"] = "happy", "smile"
        p["gaze"] = (0.5, -0.4)
    elif g >= G_SWAP:
        p["gaze"] = (0.55, -0.9)                                       # up at the glass while flicking the wire
    p["t"] = g / 30.0
    return p


def self_mark():
    return Vector(TG.STATE['marks']['morse_ladder']) + MARK_SHIFT


def hands_of(g, coil):
    """pinned raised hand (arm_r of the UNMIRRORED figure): world targets.  The hand never goes above his chin after the cap: it comes
    down the pole side to W1, takes the wire at the coil (chest height) and the wire flies up by itself."""
    mk = self_mark()
    w1 = mk + Vector((0.60, 0.52, 2.2))
    if g < HAND_DOWN[0]:
        m, _ = bottle_xf(min(g, G_CAP))
        return {"r": {"hand": tuple(m + Vector((0, 0, NECK)))}}         # the fist round the neck
    neck = Vector(TOP()) + Vector((0, 0, NECK))
    if g < G_PICK[0]:
        return {"r": {"hand": tuple(neck.lerp(w1, u_of(g, *HAND_DOWN)))}}
    if g < G_PICK[1]:
        return {"r": {"hand": tuple(w1.lerp(Vector(coil), u_of(g, *G_PICK)))}}
    c = Vector(coil)
    if g < G_FLICK[1]:
        c = c + Vector((0, 0, 0.30 * math.sin(math.pi * u_of(g, *G_FLICK))))      # a small lift of the hand, still below the chin
    rest = mk + Vector((-0.55, -0.5, 1.75))                           # then down to his side (away from the face and the pole)
    return {"r": {"hand": tuple(c.lerp(rest, u_of(g, G_FLICK[1], G_FLICK[1] + 8)))}}


# ----------------------------------------------------------------------------- runtime set pieces
def make_bottle_copy():
    """a copy of the set's inverted bottle (LN.ins_bottle, the set's own 'glass' material, BS 3.3) built with its MOUTH at the
    object origin, so location = mouth point and rotation tilts about the mouth.  Shown until G_CAP."""
    S = TG.STATE
    mb = K.MB("s23_bottle")
    LN.ins_bottle(mb, S["M"], (0.0, 0.0, 0.0), LN.BS)
    obs = mb.finish()
    return obs


def make_flash():
    """a sun star (LN.glint geometry, the set's glintm material) built at the origin: located per frame, scale keyed for the flash."""
    mb = K.MB("s23_flash")
    LN.glint(mb, TG.STATE["M"], (0.0, 0.0, 0.0), 0.32)
    ob = mb.finish()[0]
    ob.visible_shadow = False
    return ob


STAR_OFF = lambda: K.Wd(Vector((-0.06 * LN.BS * 0.4, -0.064 * LN.BS, 0.27 * LN.BS))) * K.SC   # set star position relative to the mouth (world D)


def flash_scale(g):
    """0..1.4 star size: a quick flare and fade for each glint window."""
    s = 0.0
    for a, b in (G_GLINT1, G_GLINT2):
        if a <= g <= b:
            u = (g - a) / float(b - a)
            s = max(s, 1.4 * math.sin(math.pi * min(1.0, u * 1.6)) if u < 0.62 else 1.4 * (1 - u) / 0.38 * 0.5)
    return s


def build_wire(g, coil):
    """the slack wire of frame g: two sagging half spans pole 0 -> held point -> pole 2 (sb metres -> MB -> world), the same rods,
    radius and material as the set's spans, so at G_WIRE the swap to STATE['spans_bottle'][0..1] does not jump."""
    inv = K.frame_mat().inverted()
    mid = tuple(inv @ wire_point(g, coil))
    sag = wire_sag(g)
    mb = K.MB("s23_wire_%04d" % g)
    M = TG.STATE["M"]
    for a, b in ((BOTTLE_TOP_SB(POLE - 1), mid), (mid, BOTTLE_TOP_SB(POLE + 1))):
        pts = LN.span(a, b, sag, 14)
        for p, q in zip(pts[:-1], pts[1:]):
            mb.rod(M["wiremat"], p, q, 0.03, 0.03, 5, caps=False)
    return mb.finish()


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s23")
        tune_look(LIGHT == "AFTER_RAIN")
        self.key_cam(bf(G0), *CAM.at(G0))
        self.scene.frame_set(bf(G0))
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", os.path.join(WORK, "sprites"), canvas=CANVAS, contact=False, cam=self.cam)
        self.peg = C.peg_parts(POLE)
        self.spans = TG.STATE["spans_bottle"][POLE - 1] + TG.STATE["spans_bottle"][POLE]
        self.bottle = make_bottle_copy()
        self.flash = make_flash()
        self.wires = {}
        self.hand_err = {}

    def pose(self, gs):
        mark = self.A["marks"]["morse_ladder"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.mor, f, Vector(mark) + MARK_SHIFT)
            capped, wired = g >= G_CAP, g >= G_WIRE
            # the set's pole-1 state switches on the beat (key EVERY frame: CONSTANT visibility keys)
            C.key_vis([self.peg["wood"], self.peg["glass"], self.peg["glintm"]], capped, f)
            C.key_vis(self.peg["wiremat"], wired, f)
            C.key_vis(self.spans, wired, f)
            m, tilt = bottle_xf(g)
            for ob in self.bottle:
                ob.location = m
                ob.rotation_euler = Euler((0.0, math.radians(tilt), 0.0))     # leans away from the pole, upright at contact
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("rotation_euler", frame=f)
            C.key_vis(self.bottle, not capped, f)
            s = flash_scale(g)
            rot = Matrix.Rotation(math.radians(tilt), 3, "Y")
            self.flash.location = m + rot @ STAR_OFF()
            self.flash.scale = (max(s, 1e-3),) * 3
            self.flash.keyframe_insert("location", frame=f)
            self.flash.keyframe_insert("scale", frame=f)
            C.key_vis(self.flash, s > 0.02, f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            coil = self.coil_at(g)
            _, info = self.mor.pose(f, pose_of(g), hands=hands_of(g, coil), camera=self.cam)
            self.hand_err[g] = round(max([v.get("error", 0.0) for v in info.values()] or [0.0]), 3)
            if g < G_WIRE:                                  # one slack-wire mesh per frame, visible on that frame only
                obs = self.wires[g] = build_wire(g, coil)
                for ob in obs:
                    ob.hide_render = True
                    if f > 1:
                        C.key_vis(ob, False, f - 1)
                    C.key_vis(ob, True, f)
                    C.key_vis(ob, False, f + 1)
        self.sprites_for([(self.mor, PPD)], [bf(g) for g in gs])

    def coil_at(self, g):
        """world point of the drawn coil at frame g (on the card plane, so the wire end lands exactly on the drawing).
        Uses the pose's feet point and the same upper-body stretch the sprite gets (stage API 3.3)."""
        f = bf(g)
        p = pose_of(g)
        k = actors.upper_stretch(self.mor, self.cam, f, p)
        hip = C.sprites.hip_y("morse16", p)
        lx, ly = COIL_LOCAL
        return actors.local_to_world(self.mor, (lx, C.sprites.warp_y(ly, hip, k)), f, feet=C.sprites.feet_of("morse16", p), camera=self.cam)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), hand_err=self.hand_err.get(g), capped=g >= G_CAP, wired=g >= G_WIRE,
                    bottle_px=TG.project(tuple(bottle_xf(g)[0] + Vector((0, 0, 1.1)))))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
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
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")       # drafts never mix with finals
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
