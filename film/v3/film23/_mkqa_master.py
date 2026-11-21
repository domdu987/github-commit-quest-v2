#!/usr/bin/env python3
"""mkqa.py: QA.md = header + notes.md (hand-written) + the measured numbers (QA_NUMBERS.json, GROUND.md, QA_AUTO.md, QA_JITTER.txt)."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
q = json.load(open(H + "/QA_NUMBERS.json")); m = json.load(open(H + "/meta.json"))
notes = open(H + "/notes.md").read() if os.path.exists(H + "/notes.md") else ""
g = open(H + "/GROUND.md").read().splitlines()
gl = [l for l in g if l.startswith("- checked objects")]
ja = open(H + "/QA_JITTER.txt").read().strip()
auto = open(H + "/QA_AUTO.md").read().splitlines()[0]
o = ["# %s QA: film 23, shot S%02d (%s, %s)" % (m["take"], m["shots"][0], m["location"], m["light"]), "",
     notes, "",
     "## Frame budget",
     "g0 %d, g1 (planned) %d, g1_render %d (planned x 1.25 tail), first_g %d (in-handle %d), n_frames %d, transition_in %s %d f. 720x1280, 12 samples, 30 fps; take.mkv libx264rgb crf 6 (%s MB%s)." % (
         m["g0"], m["g1"], m["g1_render"], m["first_g"], m["handle_in"], m["n_frames"], m["transition_in"]["type"], m["transition_in"]["frames"], q["take_mb"], ", split in 40 MB parts: `cat take.mkv.part* > take.mkv`" if m.get("split") else ""),
     "Render cost: %.1f s wall / frame (2 threads, two renders at once), %.1f CPU s / frame." % (q["s_per_frame_wall_mean"], q["cpu_s_per_frame_mean"]), "",
     "## Automatic QA (all run on take.mkv)",
     "- `ground_check --every 10`: %s -> GROUND.md" % (gl[0][2:] if gl else ""), "  " + [l for l in g if "result:" in l][0].strip() if any("result:" in l for l in g) else "",
     "- `qa_auto.py take.mkv --first_g %d`: %s (QA_AUTO.md, phone_sheet.jpg)" % (m["first_g"], auto.replace("# ", "")),
     "- `qa_jitter.py take.mkv` (every second must be <= 2.0 px; it prints a line only for a second above 2): `%s`" % ja.replace("\n", " | "),
     "- frame diff on 90x160 grey, in-shot frames: median %.2f, p90 %.2f (rule: >= 4 / >= 12), min %.2f" % (q["fdiff_median"], q["fdiff_p90"], q["fdiff_min"]),
     "- shade hue (ghost_hue.shade_hue, rule 240-260): " + ", ".join("%s g%d = %.1f (shaded share %.2f)" % (k, v["g"], v["hue"], v["shaded_frac"]) for k, v in q["shade_hue"].items()),
     "- heads (screen px, 720x1280, head centre; a head is out of the caption band while centre y + w/2 < 880):"]
for k, v in q["heads"].items():
    o.append("  - %s: centre y %d .. %d, x %d .. %d, head width <= %d px  (bottom of the head <= %d)" % (k, v["ymin"], v["ymax"], v["xmin"], v["xmax"], v["wmax"], v["ymax"] + v["wmax"] / 2))
o += ["", "Contact sheet: `contact.jpg` (16 frames, cyan line = y 880); phone sheet: `phone_sheet.jpg`. Scripts: `shot.py` (probe / stills / final / ground), `c23.py`, `deliver.py`, `mkqa.py`."]
open(H + "/QA.md", "w").write("\n".join(o) + "\n")
print("\n".join(o))
