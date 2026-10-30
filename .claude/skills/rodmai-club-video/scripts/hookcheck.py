"""Check the first seconds of an episode against the 3-second hook rules (SKILL.md H) from its schedule and lines.

Checks from the data: the narration starts by 0.5 s (H2), the first words are "ถ้าวันหนึ่ง… คุณ…" (S1), the narrator's command
("อย่า…" / "ห้าม…") starts by ~3 s and sits in a red {…} box (H4), the first shot is short enough to cut inside 3 s (H5, rough).
H1, H3, H5 (the lure moving in frame 1, the wrong detail, two visual changes) need a look at the stills at 0 / 1 / 2 / 3 s.

usage: python3 hookcheck.py <episode dir>      (needs schedule.json and lines.json; run python3 timing.py first)
"""
import json
import os
import re
import sys


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 else "."
    sched = json.load(open(os.path.join(ep, "schedule.json")))
    lines = {l["id"]: l for l in json.load(open(os.path.join(ep, "lines.json")))}
    rows = []
    for sh in sched["shots"]:
        for v in sh.get("vo", []):
            rows.append((sh["start"] + v["t"], sh["start"] + v["t"] + v["dur"], v["id"], v["cap"], sh["key"]))
    rows.sort()
    print("first lines:")
    for a, b, vid, cap, key in rows[:4]:
        print(f"  {a:5.2f}–{b:5.2f}s  [{key}] {vid}: {cap}")
    fails = []
    first = rows[0] if rows else None
    if not first or first[0] > 0.5:
        fails.append(f"H2 narration starts at {first[0]:.2f}s (rule: by 0.5 s)" if first else "H2 no narration")
    if first and not lines[first[2]]["text"].startswith("ถ้าวันหนึ่ง"):
        fails.append("S1 the first words are not 'ถ้าวันหนึ่ง… คุณ…'")
    if first and "คุณ" not in lines[first[2]]["text"]:
        fails.append("S1 the first line does not speak to 'คุณ'")
    # the hook's command is the narrator's ("อย่า…" / "ห้าม…"; not "อย่าง"), not a character shouting "อย่า…" in a scene
    def is_cmd(vid):
        ln = lines[vid]
        narrator = ln["voice"] == "Puck" if "voice" in ln else vid.startswith("n")  # the narrator is always Puck (rule A1), ids n01…
        return narrator and re.search(r"(อย่า(?!ง)|ห้าม)", ln["text"]) is not None
    cmd = next((r for r in rows if is_cmd(r[2])), None)
    if not cmd:
        fails.append("H4 no narrator command ('อย่า…' / 'ห้าม…') in the episode")
    else:
        print(f"command starts at {cmd[0]:.2f}s: {cmd[3]}")
        if cmd[0] > 3.5:
            fails.append(f"H4 the command lands at {cmd[0]:.2f}s (rule: by ~3 s, never after 3.5 s)")
        if "{" not in cmd[3]:
            fails.append("H4 the command is not in a red caption box {…}")
    first_shot = sched["shots"][0]
    if first_shot["dur"] > 3.6:
        fails.append(f"H5 the first shot holds {first_shot['dur']:.1f}s (rule: a cut or a strong move inside the first 3 s)")
    print("PASS" if not fails else "FAIL:\n  " + "\n  ".join(fails))
    print("look at the snapshots at 0.0 / 1.0 / 2.0 / 3.0 s for H1 (the lure moving in frame 1) and H3 (one wrong detail)")


if __name__ == "__main__":
    main()
