#!/usr/bin/env python3
"""qa_md.py <take dir> -- writes QA.md of a take from its shot.py, work/qa.json and the per-frame metas."""
import json, os, sys, importlib.util

d = os.path.abspath(sys.argv[1])
sys.argv = [sys.argv[0]]
spec_ = importlib.util.spec_from_file_location("shot", os.path.join(d, "shot.py"))
sh = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(sh)
q = json.load(open(os.path.join(d, "work", "qa.json")))
post = json.load(open(os.path.join(d, "work", "post_log.json")))
r0, r1 = sh.G0 - sh.H_IN, sh.G1 + sh.H_OUT
L = []
L.append("# QA: take %s (shot %s, office, office_day = INTERIOR_DAY)\n" % (sh.TAKE, ", ".join(map(str, sh.SHOTS))))
L.append("- **Frames.** Film frames g %d..%d are the shot; rendered g %d..%d (handles %d in, %d out for the dissolves), %d final frames "
         "`frames/g_%%04d.png`, 720x1280, Cycles 12 samples, 2 threads, one process." % (sh.G0, sh.G1 - 1, r0, r1 - 1, sh.H_IN, sh.H_OUT, r1 - r0))
L.append("- **Source.** `shot.py` (this take) on the shared runner `../s10/otake.py` (set `office3d` + `office_props`, stage actors, "
         "resumable render, streak post as `shots/post.py`). Numbers below: `python3 shot.py qa` -> `work/qa.json`.")
L.append("- **Transition in.** %s\n" % json.dumps(sh.TRANSITION_IN, ensure_ascii=False))
L.append("## What the take does\n")
L.append((sh.__doc__ or "").strip() + "\n")
L.append("## Camera (true 3D camera, corner speed in px per frame)\n")
for m in q["moves"]:
    L.append("- move g %d-%d (film %.2f-%.2f s), peak g %d at %.0f px/frame" % (m["g"][0], m["g"][1], m["film_s"][0], m["film_s"][1], m["peak_g"], m["peak_px"]))
L.append("- static runs (< 0.25 px/frame): %s" % (q["static_runs"] or "none"))
L.append("- constant-speed (linear) runs: %s" % (q["linear_runs"] or "none"))
st = [p["g"] for p in post if p["streaked"]]
L.append("- streaked frames (camera faster than 60 px/frame at the corners): %s; plate under sharp actors: %s; whole frame: %s\n" % (
    st or "none", [p["g"] for p in post if p["streaked"] == "plate"] or "none", [p["g"] for p in post if p["streaked"] == "whole"] or "none"))
L.append("## Heads (720x1280 px, from the projected sprite anchors of every final frame)\n")
L.append("| actor | frames | head width px | head centre y (px) | lowest head bottom y |")
L.append("|---|---|---|---|---|")
for k, v in q["heads"].items():
    L.append("| %s | %d | %.0f-%.0f | %.0f-%.0f (%.2f-%.2f H) | %.0f |" % (k, v["n"], v["w"][0], v["w"][1], v["y"][0], v["y"][1], v["y"][0] / 1280, v["y"][1] / 1280, v["bottom_max"]))
L.append("\nHand cards (names ending in H) are scaled hand cards whose heads lie outside the frame by construction.\n")
L.append("## Pinned props (registration: rendered tip against the projected world target)\n")
for k, v in q["reg_max_px"].items():
    L.append("- %s: max %.2f px" % (k, v))
if not q["reg_max_px"]:
    L.append("- none pinned")
L.append("\n## Popcheck (mean absolute change of consecutive final frames, 180x320)\n")
L.append("- pops (change > 1.8 x both neighbours and > 1 level): %s" % (q["pops"] or "none"))
L.append("- median change %.2f, largest %.2f" % (q["median_diff"], q["max_diff"]))
L.append("- black or magenta cards retried: %s; still wrong: %s\n" % (q["retried"] or "none", q["still_wrong"] or "none"))
L.append("## Colour (`tools/hue_report.py frames/`)\n")
L.append("```\n" + q["hue"].strip() + "\n```\n")
L.append("## Cost\n")
L.append("- CPU seconds per final frame (min / median / max): %s; wall: %s (machine shared with other workers' renders)\n" % (q["cpu_s"], q["wall_s"]))
L.append("## Deviations and notes\n")
for n in getattr(sh, "NOTES", []):
    L.append("- " + n)
open(os.path.join(d, "QA.md"), "w").write("\n".join(L) + "\n")
print("wrote", os.path.join(d, "QA.md"))
