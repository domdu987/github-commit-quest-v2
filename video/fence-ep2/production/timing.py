"""Derive shot timing from the recorded voice so picture and sound share one schedule (เอาชีวิตรอด 99 วัน EP.2 เครื่องปั่นไฟ).

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
    ("hook", ["n01", ("n02", 0.05), ("n03", 0.1)], 0.3, 0.35, 6.0),     # POV: the starter cord, the red generator in the dark classroom, the fan; the first light
    ("chapter", ["n04"], 0.15, 0.4, 2.8),                               # the page: 98 days
    ("roster", ["n05", ("n05b", 0.05), ("n05c", 0.05)], 0.1, 0.3, 7.0),   # the camp register: everyone's job
    ("map", ["n06", ("d01", 0.15)], 0.1, 0.25, 5.0),                     # the map: the fairground 2 km out; "ไปคนเดียว เร็วกว่า"
    ("gate", ["d02"], 0.15, 0.3, 3.0),                                   # "กลับก่อนมืดนะลุง" the sun HUD at 13:10
    ("fair", ["n07"], 0.15, 0.3, 4.4),                                   # the fairground at noon: the one under the wheel turns (we see it first)
    ("fairRun", [], 0, 0, 2.2),                                          # action: the cart shoved into it, the run
    ("back", ["n08", ("n09", 0.1)], 0.1, 0.3, 4.6),                      # back in time: the fuel can, 5 L = 2 h
    ("inside", ["d03", ("n10", 0.15)], 0.1, 0.25, 4.6),                   # the generator set down inside; ครูพิม hesitates
    ("start", ["n11"], 0.2, 0.3, 3.4),                                   # POV: the cord, the bulb comes on
    ("fan", ["n12"], 0.1, 0.3, 3.4),                                     # everyone under the fan; the clock of light
    ("smoke", ["n13", ("d04", 0.2)], 0.1, 0.25, 5.0),                     # the exhaust: nothing to see; "ครูขา ปั้นปวดหัว"
    ("dizzy", ["n14"], 0.1, 0.25, 3.6),                                  # heads go down
    ("co", ["n15"], 0.1, 0.3, 4.4),                                      # the card: CO kills without warning
    ("collapse", ["n16", ("d05", 0.2)], 0.1, 0.3, 4.4),                   # น้องปั้น goes down; "ดับเครื่องเดี๋ยวนี้"
    ("drag", [], 0, 0, 1.8),                                             # action: the doors, the bodies dragged out
    ("real", ["n17", ("n18", 0.1)], 0.1, 0.35, 5.0),                     # in real life: outside only, 20 ft
    ("wake", ["n19"], 0.2, 0.5, 2.8),                                    # she opens her eyes
    ("yard", ["n20", ("n21", 0.1)], 0.1, 0.3, 5.0),                      # the generator in the middle of the yard; sound carries further than light
    ("horde", ["n22", ("d06", 0.2), ("d07", 0.1)], 0.1, 0.25, 6.4),       # they come to the fence; "ลุงไปดับเอง" / "ยี่สิบวิ"
    ("count", ["n23", ("n24", 0.4)], 0.2, 0.3, 13.0),                    # the countdown 20 → 8: the switch, the sickle breaks
    ("count2", [], 0, 0, 6.1),                                           # 5 → 0: the door
    ("dark", ["n25"], 0.3, 0.3, 3.4),                                    # the light is gone: twenty minutes
    ("hill", ["n26", ("n27", 0.15)], 0.1, 0.4, 5.6),                     # the hill: three blinks; only น้องปั้น sees
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("radio", ["n28", ("r01", 0.25), ("d08", 0.2), ("n29", 0.15)], 0.15, 0.35, 8.0),   # the radio: 97… six; ลุงหมาน switches it off
    ("drawing", ["n30", ("n31", 0.1)], 0.15, 0.5, 5.0),                  # the drawing: the light on the hill, the man at the gate
    ("morning", ["n32", ("n33", 0.15)], 0.1, 0.4, 5.0),                  # morning: the man at the gate
    ("choice", [], 0.0, 0.0, 3.4),
    ("next", [], 0.0, 0.0, 2.4),
]
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
