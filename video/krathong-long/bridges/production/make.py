"""Assemble the HyperFrames project for the episode from the template, libraries and schedule."""
import json
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "hf", "lib")
PROJ = os.path.join(HERE, "..", "hf", "kb")

os.makedirs(os.path.join(PROJ, "assets"), exist_ok=True)
for f in ("package.json", "hyperframes.json", "meta.json"):
    if not os.path.exists(os.path.join(PROJ, f)):
        shutil.copy(os.path.join(HERE, "..", "hf", "rig", f), PROJ)
if not os.path.exists(os.path.join(PROJ, "assets", "fonts")):
    shutil.copytree(os.path.join(HERE, "..", "hf", "rig", "assets", "fonts"), os.path.join(PROJ, "assets", "fonts"))
for f in ("rig.js", "sets.js", "camp.js", "koi.js", "zom.js", "hands.js", "mok.js", "pov.js", "phrai.js", "ui.js", "gameui.js", "mokui.js", "phraiui.js", "pop.js", "grain.js", "pop2.js", "pop2kok.js", "pop2kitchen.js", "pop2room.js", "pop2ui.js", "pop2more.js", "pop2hosp.js", "pop2end.js", "rig2.js", "popcast.js", "mm.js", "mm2.js", "mapsdata.js", "maps.js", "mmui.js", "mmui2.js", "mmui3.js", "qkmat.js", "quake.js", "quake2.js", "quakeui.js", "quakemap.js", "tide.js", "tidemap.js", "tideui.js", "mmcast.js", "quakecast.js", "tidecast.js", "fx.js", "engine.js", "cine.js", "opener.js", "openers.js"):
    shutil.copy(os.path.join(LIB, f), os.path.join(PROJ, "assets", f))


def css(lib, name):
    js = f"global.window={{}};require('{os.path.join(LIB, lib)}');process.stdout.write(window.{name}.CSS)"
    return subprocess.check_output(["node", "-e", js]).decode()


sched = json.load(open(os.path.join(HERE, "schedule.json")))
html = open(os.path.join(HERE, "ep.tmpl.html")).read()
html = html.replace("/*__SCHEDULE__*/", json.dumps(sched, ensure_ascii=False))
html = html.replace("/*__TOTAL__*/", str(sched["total"]))
# the CINEMA BIBLE plans (shotlist, colorscript) and the one switch for cine's camera (parallax, handheld, dutch, whip, shake):
# CINE_CAM = 0 turns it off for the whole episode in one place; the grade, vignette and grain stay on
def _plan(f):
    p = os.path.join(HERE, f)
    return json.load(open(p)) if os.path.exists(p) else {}
html = html.replace("/*__CINE__*/", json.dumps({"shotlist": _plan("shotlist.json"), "colorscript": _plan("colorscript.json")}, ensure_ascii=False))
html = html.replace("/*__CINECAM__*/", "false" if os.environ.get("CINE_CAM") == "0" else "true")
html = html.replace("/*__UICSS__*/", css("ui.js", "Ui"))
html = html.replace("/*__GAMECSS__*/", css("gameui.js", "GameUI"))
open(os.path.join(PROJ, "index.html"), "w").write(html)
print("built", PROJ, "total", sched["total"])
