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
    ("open", ["n01"], 0.4, 0.5, 4.4),                 # story opener: title in the night sky, the dive onto the dorm (fire on the 7th floor)
    ("wake", ["n02", ("d01", 0.15)], 1.3, 0.2, 4.8),  # POV: eyes open on the ceiling (smoke alarm, smoke), the knocking; look to the door
    ("stop", ["n03"], 0.1, 0.5, 1.5),                 # your fist stops an inch from the doorknob
    ("phone", ["n04"], 0.15, 0.3, 3.4),               # the phone in your hand: 02:03, battery 8%
    ("timer", ["n05"], 0.1, 0.4, 3.6),                # the two-minute countdown starts
    ("gap", ["n06"], 0.1, 0.35, 4.6),                 # floor level: smoke under the door, orange light, feet moving outside
    ("bang", ["d02"], 0.1, 0.3, 3.2),                 # the door shakes, the knob rattles
    ("sign", ["n07"], 0.1, 0.3, 6.2),                 # the back of the door: an old fire notice with red handwriting
    ("rule", ["r01"], 0.2, 0.5, 9.4),                 # the handwritten rule (card)
    ("dao", ["n08"], 0.1, 0.5, 5.6),                  # the signature: ดาว 714 · 2539
    ("touch", ["n09"], 0.1, 0.3, 3.0),                # your fist touches the knob, then the door: hot
    ("hot", ["n10"], 0.1, 0.4, 5.0),                  # card: hot, or smoke round the door → keep it shut, another way out
    ("noexit", ["n11"], 0.1, 0.4, 2.8),               # whip pan to the window: seven floors down
    ("smoke", ["n12"], 0.1, 0.3, 3.0),                # the smoke under the ceiling thickens
    ("crawl", ["n13"], 0.1, 0.4, 4.2),                # down on the floor, crawling; a burnt hand hangs from แพร's bed
    ("seal", ["n14"], 0.1, 0.4, 4.8),                 # your hands push a cloth into the gap under the door
    ("call", ["n15", ("d03", 0.25)], 0.1, 0.4, 7.4),  # the phone: 199, the fire service answers
    ("window", ["n16"], 0.1, 0.8, 4.8),               # the window: wave the torch, the truck far below; in the glass the blanket sits up
    ("sig", ["s01"], 0.15, 0.5, 4.8),                 # channel signature
    ("reveal", ["n17"], 0.1, 0.3, 4.0),               # the peephole: แพร in the smoky corridor, alive
    ("prae", ["d04"], 0.1, 0.3, 4.0),                 # แพร shouting through the door
    ("turn", [], 0.0, 0.0, 1.6),                      # the torch swings to the bed
    ("ghost", ["g01"], 0.6, 0.4, 6.0),                # the blanket falls: ดาว sits up
    ("choice", [], 0.0, 0.0, 3.6),                    # open the door / stay with her
    ("next", [], 0.0, 0.0, 2.6),                      # end card: the key tag 714
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
