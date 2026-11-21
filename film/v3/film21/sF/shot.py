#!/usr/bin/env python3
"""shot.py -- film 21 segment F (FALSE PAYOFF, camp_bank): g 1044..1141, CUT in, no handles, ONE travelling camera.
The English on the south bank laugh and point across the river, bouncing out of phase, while the camera side-tracks along them (east -> west) and settles on
Cressingham; CU2 = a fast push into his smug face (thumbs in his belt), lip-sync "เห็นไหม กลัวจนขยับไม่ได้!" (narration 36.32-37.89 = g 1093..1140 only).
World: K.build_world(['camp_bank']).
    python3 shot.py probe|draft|final <a:b[:step]> [out_dir] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C
import numpy as np, bpy
import stirling as K
import cast21
ST = cast21.STORY21
G0, G1 = 1044, 1141
VIV = (float(os.environ.get("VIVG", "1.52")), 1.3, float(os.environ.get("EXPO", "0.75")))      # lower VIVID gamma for the bright camp_bank sand (API.md §9: toward 2.1 when luma > 115)
G_SPEAK = (1093, 1140)          # narration 36.32-37.89 (+0.10 s, x30)
G_LAUGH_END = 1096
WORK = os.path.join(HERE, "work")

# --- staging in the frame of the camp_bank preset: f = the preset's horizontal view direction (ENE, toward the bridge and Abbey Craig), r = screen-right.
PR = K.PRESETS["camp_bank"]
_c0, _l0 = np.array(PR["cam"][:2], float), np.array(PR["look"][:2], float)
F = (_l0 - _c0) / np.linalg.norm(_l0 - _c0); R = np.array([F[1], -F[0]])
SCALE = {"cressingham": 0.551, "surrey": 0.519, "footman_a": 0.553, "footman_b": 0.519, "knight_b": 0.546, "knight_a": 0.546}
PPD = {"cress": 320}
VIV = (float(os.environ.get("VIVG", "1.52")), 1.3, float(os.environ.get("EXPO", "0.75")))      # camp_bank VIVID with the 3-value exposure (API §13), constant


def rel(xc, f_, r_):
    """world xy at f_ m along the view direction and r_ m to the screen-right of the point xc."""
    return np.array(xc[:2], float) + F * f_ + R * r_


def layout(M):
    """(name, cast, story, variant, phase, f_, r_, flip): 3-4 big laughers beside Cressingham (25-35 % of the frame at the start), two of them pointing at the crag (flip = point screen-left), a column in depth behind."""
    return [("n1", "footman_a", "footman_a_point_laugh", 0, 0.0, 0.1, -1.05, True), ("n2", "footman_b", "footman_b_laughing", 0, 1.7, 0.4, 1.1, False),
            ("n3", "knight_b", "knight_b_point_laugh", 0, 3.1, 1.6, -1.35, True), ("n4", "footman_a", "footman_a_laughing", 1, 4.4, 1.9, 1.4, False),
            ("m1", "footman_b", "footman_b_point_laugh", 0, 5.3, 4.2, -1.4, True), ("m2", "footman_a", "footman_a_laughing", 1, 2.2, 4.8, 1.3, False),
            ("m3", "footman_b", "footman_b_laughing", 0, 0.9, 6.4, -0.2, False), ("m4", "footman_a", "footman_a_point_laugh", 0, 3.8, 7.6, -1.0, True)]


def cam_keys(xc, gz):
    """one travelling move: from behind-right of the group, sliding left and pushing in, ending low and slightly off-axis on Cressingham's face (CU2)."""
    def P(f_, r_, z): c = rel(xc, f_, r_); return (c[0], c[1], z)
    def Lk(f_, r_, z): c = rel(xc, f_, r_); return (c[0], c[1], z)
    return [(1044, P(-4.7, 0.5, gz + 1.5), Lk(3.0, 0.0, gz + 1.5), 30.0),
            (1098, P(-4.1, 0.2, gz + 1.45), Lk(3.0, -0.3, gz + 1.5), 30.0),
            (1141, P(-1.9, 0.55, gz + 1.15), Lk(1.0, -0.75, gz + 1.5), 30.0)]


def pose_of(mark, cast, story, var, phase, g):
    p = dict(ST[story][1]); dy = 0.0
    if var: p["variant21"] = var
    if mark == "cress":
        p["lean"] = 1.2 * math.sin(g * 0.11); p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.07)
        if 1093 <= g <= 1095: p["head_dy"] = -0.05 * (1 - abs(g - 1094))          # a 2-frame chin-lift on "เห็นไหม"
        if G_SPEAK[0] <= g <= G_SPEAK[1]: p = cast21.speak(p, g)
    else:
        if g <= G_LAUGH_END or mark in ("surrey",): p, dy = cast21.laugh(p, g, phase=phase)
        else:
            p["lean"] = 2.0 * math.sin(g * 0.13 + phase); p["head_roll"] = 3.0 * math.sin(g * 0.1 + phase)
    p["blink"] = C.blink(g, [1060 + int(phase * 7), 1115 + int(phase * 3)])
    p["t"] = g / 30.0
    return p, dy


def main():
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "raw")
    samples = int(sys.argv[4]) if len(sys.argv) > 4 else 32
    os.makedirs(out, exist_ok=True)
    T = C.Take(["camp_bank"], WORK, fg=True, hide=("fg_bank_barrel", "fg_bank_iron"))
    K.scots_wide_line(n=26, banners=5, scale=3.0, toward=(-92.0, -13.0))          # the Scots line on the crag facing the camp, readable at 30 mm (figures about 20 px, big saltire banners)
    M = T.A["marks"]["camp_bank"]; mode = "draft" if cmd in ("draft", "probe", "ground") else "final"
    xc = np.array(M["cress"][:3], float); gz = xc[2]; KEYS = cam_keys(xc, gz)
    # camp life on the bare foreground sand (left of the camera path, out of frame by g1078): a supply cart, sacks and a weapon rack
    rs_ = np.random.RandomState(4); Bp = K.Batch(99)
    for kind_, f_, r_, yaw_ in (("sacks", -2.2, -1.7, 0), ("sacks", -1.2, 2.3, 0), ("cart", 5.5, -3.4, 20.0), ("sacks", 3.0, 2.9, 0)):
        p_ = rel(xc, f_, r_); z_ = float(K.ground(p_[0], p_[1]))
        if kind_ == "sacks": K.sacks(Bp, (p_[0], p_[1], z_), 4, rs_)
        else: K.cart(Bp, (p_[0], p_[1], z_), yaw_, rs_)
    Bp.finalize("f_props")
    K.hide_near_banners([K.cam_path(None, KEYS, g)["loc"] for g in range(G0, G1 + 1, 3)], 2.5)
    K.setup_render(T.scene, "final" if cmd == "probe" else mode, 8)
    cast = [("cress", "cressingham", "cressingham_smug_belt", 0, 0.0, None, False), ("surrey", "surrey", "surrey_standing", 0, 2.6, (2.2, 0.8), False)]
    for nm, c, st, var, ph, f_, r_, fl_ in layout(M): cast.append((nm, c, st, var, ph, (f_, r_), fl_))
    pos = {}
    for nm, c, st, var, ph, fr, fl_ in cast:
        if nm == "cress": pos[nm] = xc.copy()
        else: p_ = rel(xc, *fr); pos[nm] = np.array([p_[0], p_[1], float(K.ground(p_[0], p_[1]))])
        T.actor("c_" + nm, c, ppd=PPD.get(nm, 176))
    viv = {}
    for g in gs:
        f = g + 1; r = K.cam_path(None, KEYS, g); K.STATE["vivid"] = VIV; viv[f] = (VIV[0], VIV[2])
        for nm, c, st, var, ph, fr, fl_ in cast:
            p, dy = pose_of(nm, c, st, var, ph, g)
            T.place("c_" + nm, f, (pos[nm][0], pos[nm][1], pos[nm][2] + dy * SCALE[c]), scale=SCALE[c], flip=fl_); T.pose("c_" + nm, f, p)
    if cmd == "ground":                                                    # QA §K ground check on every card (frames every 10)
        import ground_check21 as GC
        def set_frame(g):
            T.scene.frame_set(g + 1); K.cam_path(None, KEYS, g)
        items = [(n, a.card, -a.canvas[3] * T.actors[n].root.scale[0]) for n, a in T.actors.items()]
        air = {n: range(G0, G_LAUGH_END + 1) for n in T.actors if n != "c_cress"}          # the laughers hop 0.06 D at 3 Hz (cast21.laugh)
        rep = GC.check(items, gs, set_frame, airborne=air, out=os.path.join(HERE, "GROUND.md")); print("ground:", rep["fail"], "fail", rep["sunk"], "sunk"); return
    T.sprites_for({n: [g + 1 for g in gs] for n in T.actors}, vivid=lambda f: viv[f])
    used = list(T.actors)
    for g in gs:
        f = g + 1; r = K.cam_path(None, KEYS, g); K.STATE["vivid"] = VIV
        K.set_flow(g / 30.0); K.set_smoke(g / 30.0); K.set_flutter(g / 30.0)
        if cmd == "probe":
            print(g, np.round(r["loc"], 1), T.heads(f), flush=True); continue
        path = os.path.join(out, "g_%04d.png" % g)
        if mode == "final" and os.path.exists(path): continue
        dt = T.render(f, path, samples=samples, mode=mode, used=used)
        json.dump(dict(g=g, wall=round(dt, 1), heads=T.heads(f), cam=[round(v, 2) for v in r["loc"]]), open(path[:-4] + ".json", "w"))
        print("g %d %.1f s heads %s" % (g, dt, T.heads(f)), flush=True)


if __name__ == "__main__":
    main()
