"""เต็นท์ผีอำ EP.1. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", [], 0.0, 0.0, 4.0),                        # opener: coals in the dark, smoke writes the title, eyes in the smoke
    ("hook", ["n01", ("n02", 0.2)], 0.2, 0.6, 5.0),    # flash-forward: a tent glowing orange in the rain, a shadow on its wall
    ("arrive", ["n03"], 0.2, 0.5, 3.6),                 # dusk: the campsite on the ridge, the sign
    ("vlog", ["p01"], 0.1, 0.4, 3.4),                   # ภูมิ vlogging (his phone's view)
    ("pork", ["o01"], 0.1, 0.4, 3.4),                   # โอ๊ต and the หมูกระทะ stove
    ("booze", ["j01"], 0.1, 0.4, 3.0),                  # น้าแจ๋ว and the bottle
    ("cold", ["b01"], 0.1, 0.5, 2.8),                   # ใบเตย shivering
    ("plot", ["k01"], 0.1, 0.5, 4.0),                   # ลุงแก้ว at the plot-nine post
    ("why", ["o02"], 0.05, 0.2, 1.6),                   # โอ๊ต: why
    ("am", ["k02"], 0.3, 0.6, 2.8),                     # ลุงแก้ว close, torch from below: เดี๋ยวผีอำ
    ("legend1", ["n04"], 0.2, 0.3, 4.0),                # shadow play: the tent at plot nine
    ("legend2", ["n05"], 0.1, 0.6, 3.8),                # shadow play: something squatting on a sleeper
    ("joke", ["o03"], 0.1, 0.5, 3.2),                   # โอ๊ต laughs it off; ลุงแก้ว doesn't
    ("rule", ["k03"], 0.3, 0.7, 4.4),                   # the rule, line one
    ("rain", ["n06"], 0.3, 0.3, 3.8),                   # nine o'clock: rain, the tent shaking
    ("bring", ["o04"], 0.1, 0.4, 3.0),                  # inside: โอ๊ต brings the stove in
    ("know1", ["n07"], 0.1, 0.6, 4.0),                  # diagram: burning charcoal gives off CO
    ("know2", ["n08"], 0.1, 0.6, 3.4),                  # diagram: can't see it, can't smell it
    ("know3", ["n09"], 0.1, 0.6, 3.6),                  # diagram: a closed tent fills fast
    ("know4", ["n10"], 0.1, 0.7, 3.6),                  # diagram: a flap open is not enough
    ("order", ["p02"], 0.1, 0.4, 3.0),                  # ภูมิ: the stove goes outside after
    ("more", ["o05"], 0.05, 0.4, 2.4),                  # close on the pan: one more piece
    ("cheers", ["j02"], 0.1, 0.5, 2.8),                 # น้าแจ๋ว: cheers
    ("out", ["n11"], 0.2, 0.5, 3.8),                    # outside in the rain: ภูมิ sets the stove down, zips the door
    ("two", ["n12"], 0.4, 0.5, 3.4),                    # two a.m.: ภูมิ wakes, hot
    ("back", ["n13"], 0.2, 0.7, 3.9),                   # the stove is back, glowing at his feet
    ("chest", ["n14"], 0.3, 0.5, 4.0),                  # POV: he can't move; a weight on his chest
    ("ghost", ["g01"], 0.4, 1.1, 6.0),                  # eyes only, hold, the hit (koi-style)
    ("choice", [], 0.0, 0.0, 4.4),                      # the choice
    ("next", [], 0.0, 0.0, 3.0),                        # end card: the campsite sign — part two
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
