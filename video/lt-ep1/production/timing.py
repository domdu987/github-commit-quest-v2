"""ช่างเชื่อมสายฟ้า EP.1 (lane A, storytelling). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("w01", ["h1"], 0.05, 0.3, 3.0),                  # hook: welding on the roof in the storm, the bolt comes down on the frag "โดนไฟช็อต"
    ("w02", ["p01_1"], 0.05, 0.3, 3.4),               # not dead: hair up, sparks, the aura, badge เทพเจ้าสายฟ้า
    ("w03", ["p01_2"], 0.05, 0.3, 4.6),               # the shop in the alley: welding at the trestles, เจ๊หงส์ with the calculator, the sign
    ("w04", ["p01_3"], 0.05, 0.35, 6.0),              # the jobs (three tags) · the wage counter 450 ฿/วัน
    ("w05", ["p01_4"], 0.05, 0.3, 3.6),               # the bike: the small dream
    ("w06", ["p02_1"], 0.05, 0.3, 3.4),               # the storm rolls in over the alley
    ("w07", ["p02_2"], 0.05, 0.3, 4.2),               # sent up to the roof: the giant billboard frame, 7 floors
    ("w08", ["p02_3"], 0.05, 0.3, 2.4),               # เจ๊หงส์ shouting up in the rain
    ("w09", ["p02_4"], 0.05, 0.6, 5.8),               # the torch on the steel · the strike · the hand on the exact spot
    ("w10", ["p03_1"], 0.05, 0.3, 5.6),               # the ward, three days later: the hair that stands up
    ("w11", ["p03_2"], 0.05, 0.3, 3.6),               # walking past the beds: every phone 100%
    ("w12", ["p03_3"], 0.05, 0.3, 3.2),               # the nurse takes the pulse: her hair goes up too
    ("w13", ["p03_4"], 0.05, 0.4, 3.2),               # the ECG draws a lightning bolt
    ("w14", ["p04_1"], 0.05, 0.4, 3.4),               # back in the alley: one sneeze, the whole alley goes dark
    ("w15", ["p04_2"], 0.05, 0.3, 3.8),               # the finger points at the gate: sparks from the fingertip
    ("w16", ["p04_3"], 0.05, 0.3, 3.6),               # a day's welding done in three seconds
    ("w17", ["p04_4"], 0.05, 0.4, 7.2),               # เจ๊หงส์ triples the price · the wage stays 450
    ("w18", [], 0, 0, 2.8),                           # next: EP.2
    ("w19", [], 0, 0, 2.2),                           # the channel logo
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
