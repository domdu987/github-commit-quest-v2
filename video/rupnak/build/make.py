"""Assemble the HyperFrames project for one รูพญานาค episode (build.sh sets the env): template + libraries + schedule.
TK_RANGE="a b" (seconds, multiples of 1/60) builds a render slice of the episode, same contract as video/takhian/RENDER-SPLIT.md."""
import json
import os
import shutil
import subprocess

LIB = os.environ["TK_LIB"]
PROJ = os.environ["TK_PROJ"]
os.makedirs(os.path.join(PROJ, "assets"), exist_ok=True)
for f in ("package.json", "hyperframes.json", "meta.json"):
    if not os.path.exists(os.path.join(PROJ, f)):
        shutil.copy(os.path.join(LIB, "..", "rig", f), PROJ)
if not os.path.exists(os.path.join(PROJ, "assets", "fonts")):
    shutil.copytree(os.path.join(LIB, "..", "rig", "assets", "fonts"), os.path.join(PROJ, "assets", "fonts"))
for f in ("rig.js", "sets.js", "camp.js", "koi.js", "zom.js", "hands.js", "mok.js", "pov.js", "phrai.js", "ui.js", "gameui.js", "mokui.js", "phraiui.js", "pop.js", "grain.js", "pop2.js", "pop2kok.js", "pop2kitchen.js", "pop2room.js", "pop2ui.js", "pop2more.js", "pop2hosp.js", "pop2end.js", "rig2.js", "popcast.js", "mm.js", "mm2.js", "mapsdata.js", "maps.js", "mmui.js", "mmui2.js", "mmui3.js", "qkmat.js", "quake.js", "quake2.js", "quakeui.js", "quakemap.js", "tide.js", "tidemap.js", "tideui.js", "mmcast.js", "quakecast.js", "tidecast.js", "rupnak.js", "rupcast.js", "rupui.js", "rupnak2.js", "fx.js", "engine.js", "opener.js", "openers.js"):
    shutil.copy(os.path.join(LIB, f), os.path.join(PROJ, "assets", f))


def css(lib, name):
    js = f"global.window={{}};require('{os.path.join(LIB, lib)}');process.stdout.write(window.{name}.CSS)"
    return subprocess.check_output(["node", "-e", js]).decode()


sched = json.load(open(os.environ["TK_SCHED"]))
html = open(os.environ["TK_TMPL"]).read()
html = html.replace("/*__SCHEDULE__*/", json.dumps(sched, ensure_ascii=False))
rng = os.environ.get("TK_RANGE")
if rng:
    a, b = [float(v) for v in rng.split()]
    html = html.replace("/*__TOTAL__*/", f"{b - a:.4f}").replace("</head>", f"<script>window.TK_RANGE=[{a},{b}]</script></head>", 1)
else:
    html = html.replace("/*__TOTAL__*/", str(sched["total"]))
html = html.replace("/*__UICSS__*/", css("ui.js", "Ui"))
html = html.replace("/*__GAMECSS__*/", css("gameui.js", "GameUI"))
open(os.path.join(PROJ, "index.html"), "w").write(html)
print("built", PROJ, "total", sched["total"], "range", rng or "full")
