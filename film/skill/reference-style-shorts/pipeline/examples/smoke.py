#!/usr/bin/env python3
"""smoke.py : smoke test of the example shots at draft quality (360x640, 6 samples).

    python3 smoke.py                       probe + 3 draft frames of every example -> smoke_sheet.jpg, smoke.json
    python3 smoke.py office_day beach      only these examples
    python3 smoke.py --chain [names]       also the worker's chain on a WHOLE take at draft quality: draft every frame,
                                           use the drafts (scaled to 720x1280) as the take's raw frames, then post,
                                           contact, qa (writes frames/, meta.json, cues.json, contact.jpg like a finished take)
    python3 smoke.py --clean [names]       delete every output the examples wrote (work/, raw/, frames/, plate/, matte/, ...)

A frame fails when it is missing, nearly black (mean < 12) or shows the magenta of a missing texture (> 1 % of pixels).
Each example runs in its own process, as a worker runs it.  Times are wall seconds on this machine.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
# name: (commands to run, where the draft frames land, draft file pattern of film frame g, chain recipe)
EX = {
    "office_day": dict(probe=["probe", "27:68:20"], draft=["draft", "27,47,67"], ddir="work/draft", pat="f_%04d.png", off=1,
                       raw="work/raw", rpat="f_%04d.png", meta="work/draft/meta", rmeta="work/raw/meta", after=["post", "contact", "qa"]),
    "office_grey": dict(probe=["probe", "27:68:20"], draft=["draft", "27,47,67"], ddir="work/draft", pat="f_%04d.png", off=1,
                        raw="work/raw", rpat="f_%04d.png", meta="work/draft/meta", rmeta="work/raw/meta", after=["post", "contact", "qa"]),
    "beach": dict(probe=["probe", "27:68:20"], draft=["draft", "27:68:20"], ddir="work/draft", pat="g_%04d.png", off=0,
                  raw="raw", rpat="g_%04d.png", meta=None, rmeta="raw/meta", after=["post", "qa"]),
    "kitchen": dict(probe=None, draft=["draft", "27:68:20"], ddir="work/draft", pat="g_%04d.png", off=0,
                    raw="raw", rpat="g_%04d.png", meta=None, rmeta="raw/meta", after=["post", "qa"]),
    "map_mech": dict(probe=["probe", "27:68", "20"], draft=["draft", "27:68:20"], ddir="work/draft", pat="g_%04d.png", off=0,
                     raw="frames", rpat="g_%04d.png", meta="work/draft/meta", rmeta="work/meta", after=["post"]),
}
R0, R1 = 27, 69                       # every example renders film frames 27..68 (G0 30, G1 66, handles 3 + 3)
OUTPUTS = ["work", "raw", "frames", "plate", "matte", "meta.json", "cues.json", "contact.jpg"]


def run(name, args, log):
    t0 = time.time()
    r = subprocess.run([sys.executable, "shot.py"] + args, cwd=os.path.join(HERE, name), capture_output=True, text=True)
    dt = round(time.time() - t0, 1)
    log.append(dict(cmd=" ".join(args), rc=r.returncode, s=dt, tail=(r.stdout + r.stderr).strip().splitlines()[-3:]))
    print("  %-10s %-28s rc %d  %6.1f s" % (name, " ".join(args), r.returncode, dt), flush=True)
    return r.returncode == 0


def check(path):
    from PIL import Image
    import numpy as np
    if not os.path.exists(path):
        return "missing"
    a = np.asarray(Image.open(path).convert("RGB"), np.float32)
    if a.mean() < 12:
        return "black"
    mag = ((a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] > 200)).mean()
    return "magenta %.1f%%" % (100 * mag) if mag > 0.01 else "ok"


def frames_of(spec):
    a = spec["draft"][1]
    if ":" in a:
        p = [int(x) for x in a.split(":")]
        return list(range(p[0], p[1], p[2] if len(p) > 2 else 1))
    return [int(x) for x in a.split(",")]


def chain(name, spec, log):
    d = os.path.join(HERE, name)
    a = spec["draft"][0]
    if not run(name, [a, "%d:%d" % (R0, R1 - 1) if spec["off"] else "%d:%d:1" % (R0, R1)], log):
        return False
    os.makedirs(os.path.join(d, spec["raw"]), exist_ok=True)
    from PIL import Image
    for g in range(R0, R1):                                    # the drafts, scaled to 720x1280, stand in for the final frames
        Image.open(os.path.join(d, spec["ddir"], spec["pat"] % (g + spec["off"]))).convert("RGB").resize((720, 1280), Image.BICUBIC).save(
            os.path.join(d, spec["raw"], spec["rpat"] % (g + spec["off"])), compress_level=1)
    if spec["meta"] and spec["rmeta"]:
        shutil.copytree(os.path.join(d, spec["meta"]), os.path.join(d, spec["rmeta"]), dirs_exist_ok=True)
    elif spec["rmeta"]:
        os.makedirs(os.path.join(d, spec["rmeta"]), exist_ok=True)
    ok = True
    for c in spec["after"]:
        ok = run(name, [c], log) and ok
    return ok


def main():
    argv = sys.argv[1:]
    do_chain, do_clean = "--chain" in argv, "--clean" in argv
    names = [a for a in argv if not a.startswith("--")] or list(EX)
    if do_clean:
        for n in names:
            for o in OUTPUTS:
                p = os.path.join(HERE, n, o)
                shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))
        print("cleaned", names)
        return
    res = {}
    tiles = []
    for n in names:
        spec, log = EX[n], []
        print(n, flush=True)
        ok = True
        if spec["probe"]:
            ok = run(n, spec["probe"], log) and ok
        ok = run(n, spec["draft"], log) and ok
        st = {}
        for g in frames_of(spec):
            p = os.path.join(HERE, n, spec["ddir"], spec["pat"] % (g + spec["off"]))
            st[g] = check(p)
            tiles.append((n, g, p))
        ok = ok and all(v == "ok" for v in st.values())
        if do_chain:
            ok = chain(n, spec, log) and ok
            for f in ("frames", "meta.json", "cues.json", "contact.jpg"):
                st[f] = "ok" if os.path.exists(os.path.join(HERE, n, f)) else "missing"
        res[n] = dict(ok=ok, frames=st, log=log)
        print("  -> %s %s" % ("PASS" if ok else "FAIL", st), flush=True)
    json.dump(res, open(os.path.join(HERE, "smoke.json"), "w"), indent=1)
    from PIL import Image, ImageDraw
    w, h, s = 180, 320, 18
    cols = 6
    sheet = Image.new("RGB", (cols * w, ((len(tiles) + cols - 1) // cols) * (h + s)), (16, 16, 16))
    dr = ImageDraw.Draw(sheet)
    for i, (n, g, p) in enumerate(tiles):
        x, y = (i % cols) * w, (i // cols) * (h + s)
        if os.path.exists(p):
            sheet.paste(Image.open(p).convert("RGB").resize((w, h)), (x, y + s))
        dr.text((x + 3, y + 3), "%s g%d" % (n, g), fill=(255, 255, 255))
    sheet.save(os.path.join(HERE, "smoke_sheet.jpg"), quality=85)
    print("smoke:", "ALL PASS" if all(r["ok"] for r in res.values()) else "FAILURES", "-> smoke.json, smoke_sheet.jpg")
    sys.exit(0 if all(r["ok"] for r in res.values()) else 1)


if __name__ == "__main__":
    main()
