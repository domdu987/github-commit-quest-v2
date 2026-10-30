"""Check the first seconds of an episode against the 3-second hook rules (SKILL.md H1–H6) from its schedule and lines.

Prints the first lines with their times, when the command ("อย่า…" / "ห้าม…") starts, and what fails.
Visual rules (the lure moving in frame 1, two visual changes) still need a look at the snapshots at 0.0 / 1.0 / 2.0 / 3.0 s.

usage: python3 hookcheck.py <episode dir>      (needs schedule.json and lines.json; run python3 timing.py first)
"""
import json
import os
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
    cmd = next((r for r in rows if any(w in lines[r[2]]["text"] for w in ("อย่า", "ห้าม"))), None)
    if not cmd:
        fails.append("H4 no command ('อย่า…' / 'ห้าม…') in the episode")
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
