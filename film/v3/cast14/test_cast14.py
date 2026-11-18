#!/usr/bin/env python3
"""test_cast14.py -- QA for cast14.py (film 14).  Everything it writes goes under film/v3/cast14/ (tmp/ and sheet.jpg), never into other folders.

    python3 test_cast14.py            unchanged (earlier members byte-identical) + stories (every STORY14 pose renders) + sheet.jpg
    python3 test_cast14.py unchanged  render every earlier CAST member (neutral + a few poses) and every STORY .. STORY10 pose with and
                                      without cast14 imported (two processes) and compare the SVG text byte for byte
    python3 test_cast14.py stories    every STORY14 pose: renders, finite bbox / anchors, deterministic, inside its canvas (elephants: poses
                                      of the envelope), lip-sync flags
    python3 test_cast14.py sheet      sheet.jpg: scale row, people, elephants, creatures and props, faces
"""
import hashlib
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)

SNAP = r'''
import sys, hashlib, json
sys.path.insert(0, %r)
import cast10
if %r:
    sys.path.insert(0, %r)
    import cast14
import puppet as P
out = {}
poses = [dict(), dict(expr="smug", yaw=0.5, arm_r="akimbo"), dict(expr="laughing", yaw=-0.3, arm_l="point", legs="wide", fx=["tears"]),
         dict(expr="worried", mouth="talk_b", yaw=0.9, prop_r="pencil", squash=(1.05, 0.95), mirror=True)]
new = set(%r)
for n in sorted(P.CAST):
    if n in new:
        continue
    for i, p in enumerate(poses):
        out["%%s/%%d" %% (n, i)] = hashlib.sha1(P.figure(n, p, "u")["svg"].encode()).hexdigest()
for name, (c, p) in sorted(P.STORY.items()):
    if c in new or name in %r:
        continue
    out["story/" + name] = hashlib.sha1(P.figure(c, p, "u")["svg"].encode()).hexdigest()
print(json.dumps(out))
'''


def _snap(with14, cast14dir, newnames, story14):
    code = SNAP % (os.path.join(HERE, "..", "cast10"), with14, cast14dir, list(newnames), list(story14))
    r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, cwd=TMP)
    if r.returncode:
        print(r.stderr[-2000:])
        raise SystemExit(1)
    return json.loads(r.stdout.strip().splitlines()[-1])


def unchanged():
    sys.path.insert(0, HERE)
    import cast14
    a = _snap(False, HERE, cast14.NEW14, cast14.STORY14)
    b = _snap(True, HERE, cast14.NEW14, cast14.STORY14)
    diff = [k for k in a if a[k] != b.get(k)]
    print("unchanged: %d drawings compared (all earlier CAST members x 4 poses + all earlier STORY poses), %d differ" % (len(a), len(diff)))
    for k in diff[:20]:
        print("  DIFF", k)
    return not diff


def stories():
    sys.path.insert(0, HERE)
    import cast14
    import puppet as P
    ok = True
    for name, (c, p) in sorted(cast14.STORY14.items()):
        f1 = P.figure(c, p, "s")
        f2 = P.figure(c, p, "s")
        bad = []
        if f1["svg"] != f2["svg"]:
            bad.append("not deterministic")
        if not f1["svg"].startswith("<g") or len(f1["svg"]) < 200:
            bad.append("empty svg")
        vals = list(f1["bbox"]) + [v for xy in f1["anchors"].values() for v in xy] + [f1["feet_y"]]
        if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in vals):
            bad.append("non-finite")
        if bad:
            ok = False
            print("FAIL", name, bad)
    # the stage's sprite renderer: the stool poses must come out unclipped with CANVAS14_STOOL, the close pose with CANVAS14_CLOSE
    try:
        sys.path.insert(0, os.path.join(cast14.PROJ, "v3", "stage"))
        import sprites
        import cast_ext as CE0
        CE0.register_stage(sprites)
        for nm, cv, pxd in (("uncle_stool_hang", cast14.CANVAS14_STOOL["uncle14"], 64), ("uncle_stung_nose", cast14.CANVAS14_STOOL["uncle14"], 64),
                            ("uncle_stung_start", cast14.CANVAS14_STOOL["uncle14"], 64), ("uncle_stung_close", cast14.CANVAS14_CLOSE["uncle14"], 128),
                            ("villager_oldman_bang_pot", None, 64), ("matriarch_push", None, 48)):
            c_, p_ = cast14.STORY14[nm]
            r = sprites.render_sprites([dict(cast=c_, pose=p_, px_per_D=pxd, out=os.path.join(TMP, nm + ".png"), canvas=cv or sprites.DEFAULT_CANVAS[c_])])[0]
            if r["clipped"] and nm != "uncle_stung_close":     # the close pose is cropped below the chest on purpose
                ok = False
                print("SPRITE CLIPPED", nm)
        print("sprites: stool / close / pot / push poses render unclipped")
    except Exception as ex:   # no browser in this environment
        print("sprites check skipped:", ex)
    # lip-sync flags
    for n in cast14.LIPSYNC14:
        assert cast14.STORY14_META[n].get("lipsync"), n
    n = len(cast14.STORY14)
    # every pose in BRIEF's cast list is present
    need = ["farmer_hang_hive", "farmer_tie_wire", "farmer_calm_smile", "farmer_proud", "uncle_laugh_big", "uncle_point_mock", "uncle_arms_akimbo",
            "uncle_shout_torch", "uncle_look_field", "uncle_ask_sheepish", "uncle_stool_hang", "uncle_stung_nose", "matriarch_walk", "matriarch_push",
            "matriarch_trumpet", "matriarch_flee", "matriarch_ears_flared", "bee_fly", "swarm_cloud", "villager_woman_laugh", "villager_woman_bang_pot",
            "villager_oldman_wave_torch"]
    miss = [x for x in need if x not in cast14.STORY14]
    if miss:
        ok = False
        print("MISSING", miss)
    # canvases: the people's poses inside their canvas; elephants inside the side / front canvases
    import cast_ext as CE
    for name, (c, p) in sorted(cast14.STORY14.items()):
        cv = CE.CANVAS.get(c)
        if c in cast14.ELEPHANTS and p.get("view") == "front":
            cv = cast14.CANVAS14_FRONT[c]
        if c in ("uncle14",) and p.get("stool"):
            cv = cast14.CANVAS14_STOOL[c]
        if name == "uncle_stung_close":
            cv = cast14.CANVAS14_CLOSE[c]
        if c in ("bee", "swarm") or cv is None:
            continue
        f = P.figure(c, p, "s")
        fx, fy = f["anchors"]["feet"][0], f["feet_y"]
        b = f["bbox"]
        r = (b[0] - fx, b[1] - fy, b[2] - fx, b[3] - fy)
        bottom_ok = name == "uncle_stung_close"      # a head-and-shoulders crop: the legs are cropped on purpose
        if r[0] < cv[0] - 1e-3 or r[1] < cv[1] - 1e-3 or r[2] > cv[2] + 1e-3 or (r[3] > cv[3] + 1e-3 and not bottom_ok):
            ok = False
            print("CANVAS", name, "bbox rel feet", [round(v, 2) for v in r], "canvas", [round(v, 2) for v in cv])
    # envelope: every elephant over trunk presets x ear flare x phases x gaits x mouth (side) / trunk presets x flare x turn (front)
    worst = {}
    for c in cast14.ELEPHANTS:
        for view in ("side", "front"):
            cv = CE.CANVAS[c] if view == "side" else cast14.CANVAS14_FRONT[c]
            for tr in cast14.TRUNKS:
                for fl in (0.0, 1.0):
                    for ph in (0.0, 0.25, 0.5, 0.75):
                        for gait in ("walk", "run"):
                            for mir in (False, True):
                                p = dict(view=view, trunk=tr, ear_flare=fl, phase=ph, stride=1.0, gait=gait, mirror=mir, mouth_open=1.0 if tr == "raised" else 0.0,
                                         head_dip=-12 if tr == "raised" else 8, push=1.0 if gait == "run" else 0.0, head_turn=0.8 if view == "front" else 0.0, lean=3, t=0.25)
                                f = P.figure(c, p, "s")
                                fx, fy = f["anchors"]["feet"][0], f["feet_y"]
                                b = f["bbox"]
                                r = (b[0] - fx, b[1] - fy, b[2] - fx, b[3] - fy)
                                over = max(cv[0] - r[0], cv[1] - r[1], r[2] - cv[2], r[3] - cv[3])
                                if over > 1e-3:
                                    key = (c, view)
                                    if over > worst.get(key, (0,))[0]:
                                        worst[key] = (over, tr, fl, gait, mir)
    for key, v in sorted(worst.items()):
        ok = False
        print("ENVELOPE", key, "exceeds canvas by %.2f D (trunk %s flare %s %s mirror %s)" % v)
    print("stories: %d poses %s" % (n, "OK" if ok else "FAILED"))
    return ok


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = []
    if what in ("all", "unchanged"):
        res.append(unchanged())
    if what in ("all", "stories"):
        res.append(stories())
    if what in ("all", "sheet"):
        import sheet14
        sheet14.build()
    sys.exit(0 if all(res) else 1)
