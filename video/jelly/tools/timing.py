"""หนวดใส: shot timing from the recorded voice, per segment, so picture and sound share one schedule.
usage: python3 tools/timing.py ep1|ep2|ep3|bridges   → <segment>/schedule.json (Short) + schedule-full.json (long video part)
Each shot: (key, [voice ids | (id, gap) | (id, offset, "start")], pre-roll, post-roll, minimum length). Shots follow the beat tables of
ARC.md v1. Lines marked only="shorts"/"full" in lines.json are dropped from the other cut.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

SEG = sys.argv[1] if len(sys.argv) > 1 else "ep1"
HERE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), SEG)
DUR = json.load(open(os.path.join(HERE, "vo", "durations.json")))
LINES = {ln["id"]: ln for ln in json.load(open(os.path.join(HERE, "lines.json")))}

SHOTS_ALL = {
    "ep1": [
        ("open", ["n01"], 0.05, 0.0, 1.0),            # the open water bottle over the stung shin, father's hand shaking
        ("hook", ["n02"], 0.04, 0.4, 1.6),            # command: push in on the bottle
        ("card", ["n03"], 0.15, 0.4, 2.0),            # sundial on ยาย's porch post
        ("door", ["y01", "d01", "p01"], 0.12, 0.3, 3.0),  # dawn: ยาย at the door with the vinegar basket
        ("rhyme", ["y02", "w01"], 0.12, 0.3, 3.0),    # the three rules as a shadow-puppet legend · HG7 card at rule 2
        ("mock", ["d02", "y03"], 0.12, 0.5, 2.6),     # the photo face-down on the shelf
        ("basket", ["n04"], 0.15, 0.4, 2.6),          # ยาย sets the basket down
        ("map", [], 0.0, 0.0, 2.4),                   # house → beach route
        ("beach", ["w02", "d03", "w03", "d04"], 0.12, 0.3, 3.0),  # loose duck ring · the empty vinegar post (insert)
        ("rock", ["p02", "d05"], 0.1, 0.3, 2.4),
        ("sting", ["p03", "d06"], 0.1, 0.3, 2.4),
        ("crowd", ["x2", "p04", "w04"], 0.1, 0.3, 3.0),
        ("know", ["n05"], 0.15, 0.3, 3.0),            # cut-away skin: stingers fire on fresh water / rubbing
        ("choice", ["d07", "d08", "p05"], 0.1, 0.4, 3.0),  # bottle over the leg → set down · rule 1 ticked
        ("gone", ["d09", "n06", "d10"], 0.1, 0.8, 3.0),    # the empty duck ring among the tentacles
        ("vote", ["n07"], 0.1, 1.6, 3.0),             # Shorts only
        ("endb", ["n08"], 0.2, 0.6, 3.0),             # Shorts only
    ],
    "ep2": [
        ("open", ["n01"], 0.05, 0.0, 1.0),            # ภูมิ pushing up to follow his father
        ("hook", ["n02"], 0.04, 0.4, 1.6),
        ("recap", ["n03"], 0.12, 0.3, 2.6),           # Shorts only
        ("stay", ["p01", "d01"], 0.1, 0.3, 2.4),
        ("know", ["n04"], 0.15, 0.3, 3.0),            # venom moving with movement
        ("leave", ["d02", "x2"], 0.1, 0.3, 2.4),
        ("shore", ["x1", "d03"], 0.1, 0.3, 2.4),
        ("ring", ["n05"], 0.15, 0.4, 2.6),            # flashback: the ring slipping off at dawn
        ("back", ["w01", "d04"], 0.1, 0.3, 2.2),      # น้ำหวาน running from the tower with the bottle
        ("twist", ["w02", "w03"], 0.1, 0.3, 3.0),     # HG7 card at w03
        ("vinegar", ["n06", "w04"], 0.15, 0.3, 3.0),  # 4–6 % bottle + 30 s dial · rule 2
        ("shame", ["d05", "w05"], 0.1, 0.5, 3.0),
        ("hang", ["p06", "x3", "n07"], 0.1, 0.6, 3.0),
        ("vote", ["n08"], 0.1, 1.6, 3.0),             # Shorts only
        ("endb", ["n09"], 0.2, 0.6, 3.0),             # Shorts only
    ],
    "ep3": [
        ("open", ["n01"], 0.05, 0.0, 1.0),            # a towel reaching for the leg
        ("hook", ["n02"], 0.04, 0.4, 1.6),
        ("towel", ["x2", "d01"], 0.1, 0.3, 2.4),
        ("know", ["n03"], 0.15, 0.3, 3.0),
        ("yai", ["y01", "d02", "y02"], 0.1, 0.3, 3.0),  # ยาย runs in with the basket · lifeguard tweezes tentacles (picture only) · rule 3
        ("amb", ["x1"], 0.1, 0.6, 2.2),
        ("hall", ["d03", "y03", "d04"], 0.15, 0.3, 3.0),
        ("secret", ["y04", "y05", "d05"], 0.15, 0.6, 3.0),  # shadow-puppet flashback: the young fisherman, the water bowl
        ("why", ["y06", "y07", "d06"], 0.15, 0.5, 3.0),
        ("wake", ["w01", "p01"], 0.15, 0.4, 3.0),
        ("rules", ["n04"], 0.15, 0.4, 3.0),
        ("dawn", ["d07", "w02", "y08"], 0.15, 0.6, 3.0),
        ("end", [], 0.0, 0.0, 3.0),                   # 1669 card · "ตอนจบ"
    ],
    "bridges": [
        ("A1", ["a01"], 0.4, 0.3, 3.0),               # ยาย's house, the basket by the door, the phone
        ("A2", ["a02"], 0.1, 0.6, 2.4),
        ("B1", ["b01"], 0.2, 0.3, 3.0),               # the lifeguard tower
        ("B2", ["b02"], 0.1, 0.8, 2.4),               # the old photo
    ],
}
SHOTS = SHOTS_ALL[SEG]
GAP = 0.08


def gaps(vid):
    """Pauses inside a recorded line: [(start, length)] in seconds."""
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", os.path.join(HERE, "vo", f"{vid}.wav"),
                                   "-f", "f32le", "-ac", "1", "-ar", "16000", "-"])
    x = np.frombuffer(raw, np.float32)
    n = len(x) // 160
    db = 20 * np.log10(np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(1) + 1e-12) + 1e-9)
    quiet = db < db.max() - 32
    out, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if i > 5 and j < n - 5 and j - i >= 6:
                out.append((i / 100, (j - i) / 100))
            i = j
        else:
            i += 1
    return out


def frag_starts(vid):
    """Start offset of each caption fragment of a line (first is 0)."""
    if "frags" in LINES[vid]:  # set by hand from the loudness envelope (valid for this recording at this tempo)
        return LINES[vid]["frags"]
    frags = LINES[vid].get("cap", LINES[vid]["text"]).split(" / ")
    if len(frags) == 1:
        return [0.0]
    letters = [len(re.sub(r"[\s\[\]{}…!?.,]", "", f)) for f in frags]
    total, dur = sum(letters), DUR[vid]
    cand = gaps(vid)
    starts, used, acc = [0.0], set(), 0
    for k in range(len(frags) - 1):
        acc += letters[k]
        guess = dur * acc / total
        best, score = None, -1e9
        for g in cand:
            if g in used or g[0] + g[1] <= starts[-1] + 0.15:
                continue
            sc = g[1] - abs(g[0] + g[1] / 2 - guess)
            if sc > score:
                best, score = g, sc
        if best is not None and score > -0.35:
            used.add(best)
            starts.append(round(best[0] + best[1] - 0.04, 3))
        else:
            starts.append(round(max(guess, starts[-1] + 0.3), 3))
    return starts


def main(cut, fname):
    t = 0.0
    out = []
    drop = {"shorts": "full", "full": "shorts"}[cut]
    for key, ids, pre, post, mn in SHOTS:
        cur = pre
        vo = []
        kept = [it for it in ids if LINES[it if isinstance(it, str) else it[0]].get("only") != drop]
        if ids and not kept:
            continue  # every line of this shot belongs to the other cut
        ids = kept
        for i, item in enumerate(ids):
            vid, gap, rel = (item, GAP, "end") if isinstance(item, str) else (*item, "end")[:3]
            if i:
                cur = (vo[-1]["t"] if rel == "start" else cur) + gap
            vo.append({"id": vid, "t": round(cur, 3), "dur": DUR[vid], "cap": LINES[vid].get("cap", LINES[vid]["text"]),
                       "frags": frag_starts(vid)})
            cur += DUR[vid]
        dur = max(mn, cur + post)
        out.append({"key": key, "start": round(t, 3), "dur": round(dur, 3), "vo": vo, "voEnd": round(cur, 3)})
        t += dur
    json.dump({"cut": cut, "total": round(t, 3), "shots": out}, open(os.path.join(HERE, fname), "w"), ensure_ascii=False, indent=1)
    for s in out:
        print(f"{s['key']:9s} {s['start']:7.2f} {s['dur']:5.2f}  " + " ".join(f"{v['id']}@{v['t']:.2f}{v['frags'][1:] or ''}" for v in s["vo"]))
    print("TOTAL", cut, round(t, 2))


if __name__ == "__main__":
    if SEG == "bridges":
        main("full", "schedule.json")
    else:
        main("shorts", "schedule.json")       # 9:16 Short
        main("full", "schedule-full.json")    # this episode's part of the 16:9 long video
