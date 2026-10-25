"""Assemble the HyperFrames project for the episode from the template, libraries and schedule."""
import json
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "hf", "lib")
PROJ = os.path.join(HERE, "..", "hf", "krasue3k")

os.makedirs(os.path.join(PROJ, "assets"), exist_ok=True)
for f in ("package.json", "hyperframes.json", "meta.json"):
    if not os.path.exists(os.path.join(PROJ, f)):
        shutil.copy(os.path.join(HERE, "..", "hf", "rig", f), PROJ)
if not os.path.exists(os.path.join(PROJ, "assets", "fonts")):
    shutil.copytree(os.path.join(HERE, "..", "hf", "rig", "assets", "fonts"), os.path.join(PROJ, "assets", "fonts"))
for f in ("rig.js", "sets.js", "camp.js", "koi.js", "zom.js", "hands.js", "mok.js", "pov.js", "phrai.js", "ui.js", "gameui.js", "mokui.js", "phraiui.js", "krasue.js", "fx.js", "engine.js", "opener.js", "openers.js"):
    shutil.copy(os.path.join(LIB, f), os.path.join(PROJ, "assets", f))


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
