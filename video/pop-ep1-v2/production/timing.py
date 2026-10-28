"""เห็ดปอบ EP.1. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", [], 0.0, 0.0, 4.0),                        # story opener: steam off a pot writes the title; a black hand lifts the lid; green eyes in the steam
    ("hook", ["n01", ("n02", 0.15)], 0.2, 0.6, 4.6),    # flash-forward: a hand reaching for a white mushroom by the termite mound — cut
    ("clock", ["n03"], 0.2, 0.6, 2.0),                  # the kitchen clock running backwards
    ("arrive", ["n04"], 0.2, 0.4, 2.6),                 # wide: the village at the first rains
    ("net", ["m01"], 0.1, 0.3, 2.6),                    # มิ้นท์ close, phone up in the rain
    ("expert", ["t01"], 0.1, 0.4, 3.6),                 # ต้น bragging
    ("rule", ["y02"], 0.1, 0.6, 3.4),                   # ยายคำ at the foot of the stairs, the rule card, row one
    ("thong", ["n05"], 0.1, 0.4, 3.0),                  # ลุงทองดี at his fence by the forest, barefoot, staring
    ("rumor", ["t02"], 0.1, 0.4, 3.0),                  # ต้น whispering to มิ้นท์
    ("legend", ["n06", ("n07", 0.15), ("n08", 0.15)], 0.2, 0.5, 7.0),  # the shadow-puppet screen, panel by panel
    ("scoff", ["m02"], 0.1, 0.3, 2.8),                  # มิ้นท์ rolls her eyes
    ("forest", ["n09"], 0.1, 0.4, 3.2),                 # wide: ป่าโคก, the two of them walking in
    ("found", ["t03"], 0.05, 0.3, 2.6),                 # ต้น points: white mushrooms by the mound
    ("selfie", ["m03"], 0.05, 0.5, 2.6),                # มิ้นท์ stops him for a photo — flash
    ("pick", [], 0.0, 0.0, 1.6),                        # close: his hand pulls one up, the cup at its foot
    ("know1", ["n12", ("n13", 0.15)], 0.1, 0.5, 6.0),   # diagram: the two white mushrooms side by side; an eye, crossed out
    ("dusk", ["n14"], 0.1, 0.4, 3.6),                   # dusk: ลุงทองดี crouched by the mound, alone
    ("warn", ["th01"], 0.2, 0.5, 3.0),                  # ลุงทองดี close, pointing at the basket
    ("run", ["m04"], 0.05, 0.4, 2.4),                   # the two of them run
    ("cook", ["n15"], 0.1, 0.4, 2.6),                   # night: the kitchen under the house, the pot on the fire
    ("rice", ["y03"], 0.1, 0.4, 3.6),                   # ยายคำ shows the rice: still white
    ("know3", ["n16", ("n17", 0.15)], 0.1, 0.5, 4.4),   # diagram: the folk tests crossed out
    ("know4", ["n18"], 0.1, 0.5, 4.4),                  # diagram: boiling does not help
    ("eat", ["t04", ("m05", 0.2)], 0.1, 0.4, 5.0),      # ต้น on his second bowl; มิ้นท์ with a cup of noodles
    ("fine", ["n19", ("n20", 0.2)], 0.1, 0.5, 6.0),     # the village at night, everyone asleep
    ("two", ["n21"], 0.2, 0.5, 2.0),                    # 2 a.m.
    ("sound", ["m06"], 0.1, 0.6, 2.6),                  # มิ้นท์ under the mosquito net: chewing below
    ("peek", [], 0.0, 0.0, 4.2),                        # through the floor gaps: by the pot, a shape — only its eyes (koi-style hit)
    ("clue", ["n22", ("n23", 0.15)], 0.3, 0.6, 6.6),    # torchlight: bare footprints, long toes, toward ลุงทองดี's house
    ("pain", ["t05"], 0.2, 0.6, 3.4),                   # ต้น curled up, holding his stomach
    ("choice", [], 0.0, 0.0, 3.4),                      # hospital now / wait for morning
    ("next", [], 0.0, 0.0, 2.6),                        # end card: the forest sign — ตอนที่ 2
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
