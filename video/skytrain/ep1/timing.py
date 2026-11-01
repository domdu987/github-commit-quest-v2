"""ซอมบี้รถไฟฟ้า EP.1 กดกระดิ่ง. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01"], 0.10, -0.32, 2.6),          # 0-0.8 s close: zombie palms slam the gangway glass, the city high outside; then the car in alarm
    ("cmd", ["n02"], 0.06, 0.22, 1.5),           # a hand closes on the red emergency lever
    ("before", ["n03"], 0.20, 0.15, 3.4),        # ten minutes before: the train glides along the viaduct at dusk → inside, calm
    ("live", ["t01"], 0.10, 0.20, 2.2),          # นัท live on the selfie stick; the car screen above the door behind him
    ("rhyme", ["c01", ("t02", 0.15), ("c02", 0.15)], 0.15, 0.30, 4.0),   # ลุงเชิด on the bench muttering; นัท jokes; ลุง answers
    ("lcd", [], 0.0, 0.0, 1.1),                  # insert: the car screen (สวนหลวงเก่า greyed: งดให้บริการ · เดินรถอัตโนมัติ)
    ("scream", ["n04"], 0.12, 0.15, 2.8),        # the end car: a passenger lunges; people run toward the middle car
    ("shut", ["m01"], 0.04, 0.25, 1.5),          # นัท slams the gangway door shut
    ("glass", ["n05"], 0.15, 0.25, 3.4),         # close: faces and palms on the glass, the first crack
    ("suit", ["s01"], 0.08, 0.20, 1.7),          # the man in the suit grabs the lever
    ("lever", ["n06"], 0.15, 0.25, 3.0),         # close on the lever box: "ใช้เมื่อจอดที่สถานีเท่านั้น"
    ("drop", ["n07"], 0.15, 0.25, 3.2),          # outside: the drop from the viaduct to the street; the electrified rail
    ("rule", ["c03"], 0.12, 0.50, 2.8),          # ลุงเชิด grabs his arm; the rule card
    ("bell", ["n08"], 0.15, 0.15, 3.0),          # เมย์ presses the yellow bell
    ("occ", ["o01"], 0.10, 0.25, 3.8),           # the control centre answers through the grille; the screen's dot moves on
    ("bend", ["n10"], 0.12, 0.15, 2.3),          # the hinge bends, a gap, a hand through
    ("push", ["m02"], 0.08, 0.70, 2.6),          # everyone's back against the door; the dot nears the station
    ("arrive", [], 0.0, 0.0, 1.5),               # outside: the train slows into a dark station (silence before the doors)
    ("out", ["m03"], 0.55, 0.35, 2.6),           # the doors open, everyone pours out; เมย์ on her knees: รอดแล้ว
    ("quiet", ["n11"], 0.15, 0.25, 2.4),         # the platform: half the lights off, nobody
    ("sign", ["n12"], 0.12, 0.25, 2.8),          # the sign: สวนหลวงเก่า + the งดให้บริการ tape
    ("turn", ["n13"], 0.12, 0.95, 3.2),          # the staff at the far end turns: milky eyes
    ("next", [], 0.0, 0.0, 3.2),                 # next-episode card
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
