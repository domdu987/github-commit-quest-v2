"""Derive shot timing from the recorded voice so picture and sound share one schedule.

Each shot lists its voice lines in order, as "id", ("id", gap) where gap is the time from the end of
the previous line (negative = overlap), or ("id", offset, "start") to start offset seconds after the
previous line started. A shot lasts pre + lines + post, but never less than `min`.
Every line's caption is split on " / " into fragments; each fragment's start is found from the pauses
in the recorded line (falling back to its share of the characters), so captions and camera cuts land
on the beat of the voice. Writes schedule.json (used by the composition and by mix.py).
"""
import json
import os
import re
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = json.load(open(os.path.join(HERE, "vo", "durations.json")))
LINES = {ln["id"]: ln for ln in json.load(open(os.path.join(HERE, "lines.json")))}

# key, [voice ids], pre-roll, post-roll, minimum length
SHOTS = [
    ("hook", ["n01", ("n02", 0.45)], 0.5, 0.5, 5.6),
    ("rewind", ["n03"], 0.25, 0.35, 1.9),
    ("canopy", ["n04"], 0.15, 0.25, 2.4),
    ("vlog", ["d01"], 0.15, 0.25, 4.0),
    ("leg", ["d02"], 0.15, 0.25, 2.1),
    ("guide", ["d03"], 0.2, 0.25, 2.9),
    ("rule", ["d04"], 0.15, 0.45, 7.0),
    ("legend", ["n05", "n06", "n07"], 0.15, 0.35, 6.2),
    ("laugh", ["d05"], 0.1, 0.15, 2.2),
    ("stream", ["n08", "d06", ("d07", 0.2)], 0.15, 0.35, 5.8),
    ("xsec", ["n09", "n10"], 0.15, 0.35, 4.8),
    ("signs", ["n11"], 0.15, 0.35, 3.7),
    ("climb", ["n12"], 0.15, 0.35, 2.4),
    ("night", ["n13"], 0.3, 0.25, 3.1),
    ("cry", ["k01"], 0.5, 0.15, 4.4),
    ("listen", ["d08", "d09"], 0.15, 0.25, 3.3),
    ("phonecam", ["d10"], 0.15, 0.9, 3.1),
    ("sleep", ["n14"], 0.25, 0.4, 2.6),
    ("feet", [], 0.0, 0.0, 2.4),
    ("twoam", ["n15", "d11", "d12"], 0.25, 0.15, 3.8),
    ("leech", ["n16"], 0.15, 0.25, 1.8),
    ("howto", ["n17", "n18", "n19"], 0.15, 0.35, 6.4),
    ("bleed", ["n20"], 0.15, 0.35, 2.6),
    ("relief", ["d13"], 0.1, 0.15, 2.3),
    ("print", ["n21"], 0.15, 0.25, 2.3),
    ("ring", ["n22"], 0.15, 0.35, 2.7),
    ("hammock", ["n23"], 0.15, 0.4, 2.7),
    ("close", ["k02"], 0.8, 0.35, 1.9),
    ("choice", [], 0.0, 0.0, 3.4),
]
GAP = 0.14


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
            sc = g[1] - 0.5 * abs(g[0] + g[1] / 2 - guess)
            if sc > score:
                best, score = g, sc
        if best is not None and score > -0.35:
            used.add(best)
            starts.append(round(best[0] + best[1] - 0.04, 3))
        else:
            starts.append(round(max(guess, starts[-1] + 0.3), 3))
    return starts


def main():
    t = 0.0
    out = []
    for key, ids, pre, post, mn in SHOTS:
        cur = pre
        vo = []
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
    json.dump({"total": round(t, 3), "shots": out}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)
    for s in out:
        print(f"{s['key']:9s} {s['start']:7.2f} {s['dur']:5.2f}  " + " ".join(f"{v['id']}@{v['t']:.2f}{v['frags'][1:] or ''}" for v in s["vo"]))
    print("TOTAL", round(t, 2))


if __name__ == "__main__":
    main()
