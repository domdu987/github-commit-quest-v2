"""แสงกระสือ EP.1. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.4, 0.6, 5.0),                 # story opener: a green light writes the title, turns into a face; the power stutters on over the flood
    ("hook", ["n02"], 0.4, 0.9, 3.2),                 # low at the water: เต้ย wading toward a pole, a broken line spitting in the water — cut
    ("back", ["n03"], 0.3, 0.7, 2.2),                 # chapter card: the meter, its disc and numbers running backwards — 6 hours earlier
    ("dusk", ["n04"], 0.1, 0.4, 3.6),                 # wide at dusk: the village on stilts, the water up to the floors
    ("live", ["d01"], 0.1, 0.3, 4.4),                 # ฝน close, going live on her phone
    ("toey", ["d02"], 0.05, 0.4, 2.4),                # low angle on เต้ย: me too!
    ("boat", ["n05"], 0.1, 0.4, 4.2),                 # ลุงเปี๊ยก paddles up to the porch
    ("rule", ["d03"], 0.2, 0.7, 10.0),                # ลุงเปี๊ยก's rules (card)
    ("legend", ["n06"], 0.2, 0.4, 3.0),               # the old one-baht comic: its cover
    ("traits", ["t01", ("t02", 0.15), ("t03", 0.15)], 0.1, 0.5, 10.0),  # the comic's panels: by day / the head pulls free / floats to the lights, calls a name
    ("skeptic", ["d04"], 0.1, 0.4, 3.8),              # ฝน laughs it off; ลุงเปี๊ยก in his boat behind
    ("chaem", ["n07", ("d05", 0.2)], 0.1, 0.4, 7.4),  # ป้าแช่ม brings curry; close on her
    ("cold", ["n08"], 0.1, 0.5, 4.6),                 # her cold hand on ฝน's wrist / she leaves, a green glint
    ("nine", ["n09"], 0.1, 0.4, 3.8),                 # 9 p.m. inside: the clock, the water creeping to the outlets
    ("know1", ["n10"], 0.1, 0.6, 5.2),                # knowledge: water near the outlets → cut the main
    ("know2", ["n11"], 0.1, 0.6, 5.8),                # knowledge: never touch anything electric wet or standing in water
    ("know3", ["n12"], 0.1, 0.6, 4.8),                # knowledge: if the panel is under water, don't wade to it; call the electrician
    ("cut", ["n13"], 0.1, 0.8, 5.0),                  # ฝน dries her hands, stands on the stairs, pulls the lever — dark
    ("dark", ["n14"], 0.2, 0.5, 4.4),                 # the village dark; one green light left over the field
    ("bomb", ["n15"], 0.1, 0.6, 4.6),                 # down the pole: a line snapped, its end under the water, spitting
    ("call", ["r01"], 0.3, 0.5, 5.2),                 # the light floats close: a face, green eyes, the guts glowing
    ("answer", ["d06"], 0.1, 0.4, 2.4),               # เต้ย at the door, green light on his face
    ("wade", ["n16"], 0.1, 0.4, 3.6),                 # he walks down the steps into the flood after it
    ("shout", ["d07"], 0.05, 0.4, 2.2),               # ฝน at the door
    ("know4", ["n17"], 0.1, 0.6, 6.8),                # knowledge: a line in the water can charge it; always assume it is live
    ("know5", ["n18"], 0.1, 0.7, 7.0),                # knowledge: don't wade in, 10 m away, call 1129
    ("sig", ["s01"], 0.15, 0.5, 4.6),                 # channel signature
    ("near", ["n19"], 0.1, 0.5, 4.3),                 # เต้ย standing in the water a few steps from the line
    ("whisper", ["r02"], 0.3, 0.6, 4.8),              # the กระสือ over the water by the line: closer…
    ("choice", [], 0.0, 0.0, 3.4),                    # shout at him / wade in after him
    ("next", [], 0.0, 0.0, 2.6),                      # end card: the sign on the pole
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
