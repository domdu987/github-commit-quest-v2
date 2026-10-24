"""Assemble the HyperFrames project for the episode from the template, libraries and schedule."""
import json
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "hf", "lib")
PROJ = os.path.join(HERE, "..", "hf", os.environ.get("HF_PROJ", "fence1"))   # HF_PROJ=<name> builds a side-by-side variant project

os.makedirs(os.path.join(PROJ, "assets"), exist_ok=True)
for f in ("package.json", "hyperframes.json", "meta.json"):
    if not os.path.exists(os.path.join(PROJ, f)):
        shutil.copy(os.path.join(HERE, "..", "hf", "rig", f), PROJ)
if not os.path.exists(os.path.join(PROJ, "assets", "fonts")):
    shutil.copytree(os.path.join(HERE, "..", "hf", "rig", "assets", "fonts"), os.path.join(PROJ, "assets", "fonts"))
for f in ("rig.js", "hand.js", "sets.js", "camp.js", "koi.js", "zom.js", "fence.js", "sig.js", "ui.js", "gameui.js", "fx.js", "engine.js"):
    shutil.copy(os.path.join(LIB, f), os.path.join(PROJ, "assets", f))
ART = os.path.join(HERE, "..", "art")   # AI-painted plates referenced by the template as assets/art/<name>.png
os.makedirs(os.path.join(PROJ, "assets", "art"), exist_ok=True)
import re as _re
for name in sorted(set(_re.findall(r'assets/art/([\w-]+)\.png', open(os.path.join(HERE, "ep.tmpl.html")).read()) + _re.findall(r'(?:set|far|name): "([\w-]+)"', open(os.path.join(HERE, "ep.tmpl.html")).read()))):
    src = os.path.join(ART, name + ".png")
    if os.path.exists(src):
        shutil.copy(src, os.path.join(PROJ, "assets", "art", name + ".png"))


def css(lib, name):
    js = f"global.window={{}};require('{os.path.join(LIB, lib)}');process.stdout.write(window.{name}.CSS)"
    return subprocess.check_output(["node", "-e", js]).decode()


sched = json.load(open(os.path.join(HERE, "schedule.json")))
html = open(os.path.join(HERE, "ep.tmpl.html")).read()
html = html.replace("/*__SCHEDULE__*/", json.dumps(sched, ensure_ascii=False))
html = html.replace("/*__TOTAL__*/", str(sched["total"]))
html = html.replace("/*__UICSS__*/", css("ui.js", "Ui"))
html = html.replace("/*__GAMECSS__*/", css("gameui.js", "GameUI"))
open(os.path.join(PROJ, "index.html"), "w").write(html)
print("built", PROJ, "total", sched["total"])
