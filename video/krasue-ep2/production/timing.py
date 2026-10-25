"""แสงกระสือ EP.2. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("recap", [], 0.0, 0.0, 2.0),                       # EP.1's last image: เต้ย in the water by the broken line, the กระสือ beyond
    ("hook", ["n01", ("n02", 0.15)], 0.3, 0.7, 5.6),    # flash-forward: the kitchen lit, เต้ย stuck to the fridge, a hand reaching — stamped out · EP.2
    ("step", ["n03"], 0.1, 0.4, 3.0),                   # low at the water: ฝน's feet going in
    ("stop", ["d01"], 0.05, 0.4, 2.4),                  # ลุงเปี๊ยก in his boat, torch up, shouting
    ("off", ["n04"], 0.1, 0.6, 5.0),                    # wide: the line spitting… then dead; the lamp by the temple goes out
    ("pull", ["d02"], 0.1, 0.4, 3.4),                   # he paddles in and hauls เต้ย into the boat
    ("dazed", ["d03"], 0.2, 0.5, 4.2),                  # เต้ย close in the boat, eyes far away
    ("one", ["n05"], 0.1, 0.4, 4.0),                    # 1 a.m.: the village lights come back — but one house stays dark
    ("down", ["n06"], 0.1, 0.4, 3.8),                   # the main switch close up, still down
    ("phone", ["n07"], 0.1, 0.3, 2.4),                  # upstairs: ฝน's face in the phone light
    ("replay", ["n08"], 0.1, 0.7, 6.0),                 # the live replay: the light following เต้ย… a face in it
    ("two", ["n09"], 0.2, 0.4, 3.8),                    # 2 a.m.: downstairs, the lights flicker on by themselves
    ("lever", ["n10"], 0.1, 0.5, 3.0),                  # the switch close up: the lever going up on its own, green light beside it
    ("call", ["r01"], 0.3, 0.5, 5.6),                   # the กระสือ by the switch, calling up the stairs
    ("walk", ["n11"], 0.1, 1.0, 4.6),                   # เต้ย down the stairs, into the water, his hand on the fridge — the shock
    ("scream", ["d04"], 0.05, 0.4, 2.4),                # ฝน at the top of the stairs
    ("rush", ["n12"], 0.1, 0.3, 3.0),                   # she runs down, reaching for his hand
    ("rule", ["d05"], 0.1, 0.5, 2.8),                   # the rule card flashes: ใครโดนดูด อย่าจับ
    ("know1", ["n13"], 0.1, 0.6, 5.0),                  # knowledge: don't touch someone still in contact
    ("know2", ["n14"], 0.1, 0.6, 3.4),                  # knowledge: cut the power first
    ("guard", ["n15"], 0.1, 0.6, 4.0),                  # at the switch: a head floating beside it
    ("broom", ["n16"], 0.1, 0.8, 6.6),                  # ฝน on the dry step with the broom; the handle knocks the lever down
    ("know3", ["n17"], 0.1, 0.6, 6.4),                  # knowledge: something that doesn't conduct, standing on something dry
    ("dark", ["n18"], 0.1, 0.5, 5.0),                   # lights out: the กระสือ shrieks and is gone; เต้ย drops into the water
    ("drag", ["n19"], 0.1, 0.5, 3.8),                   # she drags him up the stairs; he isn't breathing
    ("know4", ["n20"], 0.1, 0.6, 5.6),                  # knowledge: 1669, CPR right away (top-down on the boards)
    ("breathe", ["n21"], 0.1, 0.6, 4.4),                # she keeps pressing… his eyes open
    ("sig", ["s01"], 0.15, 0.5, 4.6),                   # channel signature
    ("knock", ["n22"], 0.2, 0.6, 3.6),                  # 3 a.m.: knocking at the door downstairs
    ("voice", ["r02"], 0.2, 0.4, 4.4),                  # the door from the stairs: ป้าแช่ม's voice
    ("answer", ["d06"], 0.1, 0.4, 2.2),                 # ฝน answers
    ("under", ["n23"], 0.1, 0.6, 5.0),                  # under the door: green light seeping in across the water
    ("inside", ["r03"], 0.2, 0.5, 5.6),                 # the door close up, the green getting brighter
    ("choice", [], 0.0, 0.0, 3.4),                      # open the door / keep quiet
    ("next", [], 0.0, 0.0, 2.6),                        # end card: the sign on the pole — ตอนที่ 3 (ตอนจบ)
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
