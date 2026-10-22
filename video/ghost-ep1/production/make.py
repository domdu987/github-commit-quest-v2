"""Assemble the HyperFrames project for the episode from the template, libraries and schedule."""
import json
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "hf", "lib")
PROJ = os.path.join(HERE, "..", "hf", "ghost")

os.makedirs(os.path.join(PROJ, "assets"), exist_ok=True)
for f in ("package.json", "hyperframes.json", "meta.json"):
    src = os.path.join(HERE, "..", "hf", "rig", f)
    if not os.path.exists(os.path.join(PROJ, f)):
        shutil.copy(src, PROJ)
if not os.path.exists(os.path.join(PROJ, "assets", "fonts")):
    shutil.copytree(os.path.join(HERE, "..", "hf", "rig", "assets", "fonts"), os.path.join(PROJ, "assets", "fonts"))
for f in ("rig.js", "sets.js", "ui.js", "engine.js"):
    shutil.copy(os.path.join(LIB, f), os.path.join(PROJ, "assets", f))

sched = json.load(open(os.path.join(HERE, "schedule.json")))
ui_css = subprocess.check_output(["node", "-e", f"global.window={{}};require('{os.path.join(LIB, 'ui.js')}');process.stdout.write(window.Ui.CSS)"]).decode()
html = open(os.path.join(HERE, "ep.tmpl.html")).read()
html = html.replace("/*__SCHEDULE__*/", json.dumps(sched, ensure_ascii=False))
html = html.replace("/*__TOTAL__*/", str(sched["total"]))
html = html.replace("/*__UICSS__*/", ui_css)
open(os.path.join(PROJ, "index.html"), "w").write(html)
print("built", PROJ, "total", sched["total"])
