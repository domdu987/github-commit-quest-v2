#!/usr/bin/env python3
"""shot.py -- film 18 take s08 (shot 8, g 597..673 + 9 in-handle frames 588..596): yan_camp DUSK.  "ขุนพลเยียนมองจากค่ายแล้วหัวเราะลั่น"
The general on the camp rampart (mark rampart, z 2.6) looks toward Jimo, then bursts out laughing on "หัวเราะ" (21.24 s -> g 640): belly bounce 0.06 D at 3 Hz, lean
toggling, two soldiers beside him laugh a few frames later.  Mouths are STILL (the first quote starts at 22.45 s = g 676): a constant laughing mouth, never lip-sync.
Camera: set camera s08 (eye, push 8 %/s, fg spear rack on the left) blended with a linear ease so no frame sits still.
Set patches (QA_ART_SET_R2 13): red slab toned to #8a2a20, the cut beam top-left hidden, cloud base bars shortened.

    python3 shot.py draft  a:b[:step] [outdir]      (360x640, 6 samples)
    python3 shot.py final  a:b[:step]               (720x1280, 12 samples, raw/g_%04d.png)
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c18 as C                                                         # noqa: E402

SHOT = "s08"
G0, G1 = 597, 674                                                       # shot range [G0, G1)
H_IN, H_OUT = 9, 0                                                      # dissolve 13 in: half + 2 = 9 handle frames
G_LAUGH = C.g_of(21.24) - 4                                             # 636: the burst starts just before "หัวเราะ"
G_SOLD = (G_LAUGH + 6, G_LAUGH + 12)                                    # the soldiers catch the laugh
LAUGH_MOUTH = ("open", 0.34, 0.22)                                      # constant (not lip-sync)
CAMLIN = 0.5
PARAMS = (0.0, 0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.6, 2.2)      # extra push, slide px/s, sway D, sway Hz, look wobble D, dz, dz/t  (c18.make_mod)


CAM = ((1.8, -53.2, 4.7), (-4.0, -47.5, 4.5), 24.0)   # reframed (director round 4): general ~30 % of the frame height, above the rail; env CAM8 overrides.  Format of the env: (loc, look_at, lens) override of the set camera, e.g. "2.5,-54.5,4.4:-4,-47.5,4.4:24" in env CAM8
if os.environ.get("CAM8"):
    a, b, c = os.environ["CAM8"].split(":")
    CAM = (tuple(float(x) for x in a.split(",")), tuple(float(x) for x in b.split(",")), float(c))
if CAM:
    C.S.SHOTS[SHOT]["cam"] = dict(loc=CAM[0], look_at=CAM[1], lens=CAM[2])
    C.S.SHOTS[SHOT]["move"] = dict(push=float(os.environ.get("PUSH8", "0.08")), slide=float(os.environ.get("SLIDE8", "0")))


def patches(T):
    n = C.tone_red(gain=0.35)
    # director round 4: the red gate lintel (palisade b82c20 faces at z >= 7.9) is the bright slab with the cut end -> remove it; hide the stump (logs) and the fire-ring stones lump
    pal = C.J.STATE["objects"]["palisade"]
    import bmesh
    bm = bmesh.new(); bm.from_mesh(pal.data); mw = pal.matrix_world
    red = [i for i, m in enumerate(pal.data.materials) if m and "b82c20" in m.name]
    dl = [f for f in bm.faces if f.material_index in red and (mw @ f.calc_center_median()).z >= 7.9]
    for f in dl:
        bm.faces.remove(f)
    bm.to_mesh(pal.data); bm.free(); pal.data.update()
    print("lintel faces removed", len(dl))
    for nm in ("logs", "firestone"):
        if nm in C.J.STATE["objects"]:
            C.J.STATE["objects"][nm].hide_render = True
    C.patch_sky()
    ob = C.J.STATE["objects"]
    for nm in ("cloth",):
        if nm in ob:
            ob[nm].hide_render = True
    # the near brazier fire4 (-4, -57) blows out the caption band when the camera sways toward it: dim it and drop its halo faces
    for fi in C.J.STATE["fires"]:
        if abs(fi["ob"].location.x + 4.0) < 0.1 and abs(fi["ob"].location.y + 57.0) < 0.1:
            fi["E0"] *= 0.45
            fi["k"] = fi.get("k", 1.0) * 0.6
    h = ob.get("halos")
    if h is not None:
        import bmesh
        from mathutils import Vector as V
        bm = bmesh.new(); bm.from_mesh(h.data); mw = h.matrix_world
        dl = [f for f in bm.faces if (mw @ f.calc_center_median() - V((-4.0, -57.0, 1.5))).length < 4.0]
        for f in dl:
            bm.faces.remove(f)
        bm.to_mesh(h.data); bm.free(); h.data.update()
        print("halo faces removed", len(dl))
    print("patches: red materials toned", n)


def stage_factory(T):
    def stage(g, cam):
        marks = C.S.marks_for(SHOT)
        gen = marks["general"][0]
        sol = marks["soldier"]
        # general
        laugh = g >= G_LAUGH
        if not laugh:
            card = C.pcard("general_stand", mouth="dash", expr="smug", blink=C.cast18.blink_at(g, 72, 10))
            C.place(card, gen[:3], cam, C.J.HEIGHT["general"], g, "general", roll_deg=1.2 * C.sway(g, 0.0, 0.7))
        else:
            tog = ((g - G_LAUGH) // 5) % 2                                # belly toggles every 5 frames (3 Hz)
            card = C.pcard("general_laugh", mouth=LAUGH_MOUTH, lean=-8 if tog == 0 else -3, blink=0)
            C.place(card, gen[:3], cam, C.J.HEIGHT["general"], g, "general", bounce_amp=0.06, ph=0.0, roll_deg=2.0 * C.sway(g, 0, 1.5))
        # soldiers
        for i, m in enumerate(sol):
            pose = ["soldier_laugh_point_a", "soldier_laugh_point_b"][i % 2]
            if g < G_SOLD[i % 2]:
                card = C.pcard(pose.replace("laugh_point", "stand"), blink=C.cast18.blink_at(g, 80, 7 * i))
                C.place(card, m[:3], cam, C.J.HEIGHT["soldier"], g, "sol%d" % i, roll_deg=0.8 * C.sway(g, i, 0.6))
            else:
                tog = ((g - G_SOLD[i % 2]) // 5 + i) % 2
                card = C.pcard(pose, lean=-5 if tog else -1)
                C.place(card, m[:3], cam, C.J.HEIGHT["soldier"], g, "sol%d" % i, bounce_amp=0.06, ph=1.1 * i, roll_deg=1.5 * C.sway(g, i, 1.5))
    return stage


def parse(rng):
    a, b = rng.split(":")[:2]
    step = int(rng.split(":")[2]) if rng.count(":") == 2 else 1
    return list(range(int(a), int(b) + 1, step))


if __name__ == "__main__":
    mode = sys.argv[1]
    gs = parse(sys.argv[2]) if len(sys.argv) > 2 else list(range(G0 - H_IN, G1 + H_OUT))
    if mode == "draft":
        out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "work", "draft")
        T = C.Take(SHOT, "preview", patches=[patches])
    else:
        out = os.path.join(HERE, "raw")
        T = C.Take(SHOT, "final", patches=[patches])
    T.render_frames(gs, out, stage_factory(T), lin=CAMLIN, mod=C.make_mod(T.sh["dur"], *PARAMS))
