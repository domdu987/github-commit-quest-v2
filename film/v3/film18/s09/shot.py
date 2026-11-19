#!/usr/bin/env python3
"""shot.py -- film 18 take s09 (shot 9, g 674..736): yan_camp DUSK.  QUOTE 1a "จะเอาวัวมาสู้ทัพข้างั้นเหรอ!" (22.45 s = g 676): the general, arms wide, LIP-SYNC (cast18.talk_mouth) from g 676;
the soldiers behind him laugh (constant laugh mouths, bounce 0.06 D at 3 Hz, lean toggling).  Camera: set camera s09 (medium push 9 %/s) blended with a linear ease.
Set patch: cloud base bars shortened.   python3 shot.py draft|final a:b[:step] [outdir]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                         # noqa: E402

SHOT = "s09"; G0, G1 = 674, 737; H_IN, H_OUT = 0, 0
CAMLIN = 0.5
PARAMS = (0.12, 80, 0.7, 2.6, 0.8, -1.0, -0.6)      # extra push, slide px/s, sway D, sway Hz, look wobble D, dz, dz/t  (c18.make_mod)


def patches(T):
    C.patch_sky()


def stage_factory(T):
    def stage(g, cam):
        marks = C.S.marks_for(SHOT)
        gen = marks["general"][0]; sol = marks["soldier"]
        talk = C.QUOTE1[0] <= g < C.QUOTE1[1]
        mouth = C.cast18.talk_mouth(g, 1.0) if talk else "flat"
        card = C.pcard("general_arms_wide", mouth=mouth, blink=C.cast18.blink_at(g, 90, 11))
        C.place(card, gen[:3], cam, C.J.HEIGHT["general"], g, "general", roll_deg=1.5 * C.sway(g, 0.0, 0.8))
        poses = ["soldier_laugh_point_a", "soldier_laugh_point_b", "soldier_laugh_point_c"]
        for i, m in enumerate(sol):
            tog = ((g + 3 * i) // 5) % 2
            card = C.pcard(poses[i % 3], lean=-5 if tog else -1)
            C.place(card, m[:3], cam, C.J.HEIGHT["soldier"], g, "sol%d" % i, bounce_amp=0.06, ph=1.3 * i, roll_deg=1.5 * C.sway(g, i, 1.5))
    return stage


def parse(rng):
    a, b = rng.split(":")[:2]
    step = int(rng.split(":")[2]) if rng.count(":") == 2 else 1
    return list(range(int(a), int(b) + 1, step))


if __name__ == "__main__":
    mode = sys.argv[1]
    gs = parse(sys.argv[2]) if len(sys.argv) > 2 else list(range(G0 - H_IN, G1 + H_OUT))
    if mode == "draft":
        out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "work", "draft"); T = C.Take(SHOT, "preview", patches=[patches])
    else:
        out = os.path.join(HERE, "raw"); T = C.Take(SHOT, "final", patches=[patches])
    T.render_frames(gs, out, stage_factory(T), lin=CAMLIN, mod=C.make_mod(T.sh["dur"], *PARAMS))
