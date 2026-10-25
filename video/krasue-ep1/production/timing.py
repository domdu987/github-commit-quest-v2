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
    ("open", ["a01"], 0.4, 0.4, 4.6),                 # story opener: a green light writes the title; the power stutters on over the flood
    ("hook", ["a02"], 0.2, 0.6, 2.4),                 # low at the water: เต้ย wading toward a light, a broken line spitting — cut
    ("back", ["n03"], 0.2, 0.5, 1.6),                 # chapter card: the meter running backwards — 6 hours earlier
    ("dusk", ["a03"], 0.1, 0.3, 2.4),                 # wide at dusk: the village on stilts
    ("live", ["d01"], 0.1, 0.2, 4.2),                 # ฝน close, going live
    ("toey", ["a04"], 0.05, 0.3, 2.8),                # เต้ย on the steps, his flip-flop floating off
    ("boat", ["a05"], 0.1, 0.3, 2.8),                 # ลุงเปี๊ยก paddles up: "ไอ้หนู!"
    ("rule", ["a06"], 0.1, 0.5, 6.0),                 # his two rules (card)
    ("legend", ["n06"], 0.1, 0.2, 2.8),               # the one-baht comic: its cover
    ("traits", ["t01", ("a07", 0.1), ("a08", 0.1)], 0.1, 0.3, 8.0),  # the panels: by day / the head floats off / it calls names
    ("skeptic", ["d04"], 0.05, 0.3, 3.6),             # ฝน laughs it off
    ("chaem", ["n07", ("a09", 0.15)], 0.1, 0.3, 6.6), # ป้าแช่ม brings curry
    ("cold", ["a10"], 0.1, 0.5, 2.2),                 # her hand on ฝน's wrist: ice cold
    ("nine", ["a11", ("a12", 0.1)], 0.1, 0.3, 3.2),   # 9 p.m.: เต้ย shouts, the water at the outlets
    ("know", ["a13", ("a14", 0.1), ("a15", 0.1)], 0.1, 0.4, 7.6),  # the house in cross-section: cut the main; never touch it wet
    ("cut", ["a22"], 0.1, 0.6, 4.0),                  # ฝน dries her hands, the lever down — dark
    ("dark", ["a16"], 0.1, 0.3, 3.4),                 # the village dark; one light over the field
    ("cam", ["a17"], 0.1, 0.4, 3.0),                  # her phone in the dark: "can't see a thing" — but there is something by the light
    ("sleep", ["a18"], 0.1, 0.3, 2.0),                # everyone asleep
    ("bomb", ["a19"], 0.1, 0.4, 3.4),                 # down the pole: a line snapped, its end under the water
    ("two", ["a20"], 0.1, 0.6, 1.4),                  # 2 a.m.
    ("call", ["r01"], 0.3, 0.3, 4.8),                 # the light at the window, calling เต้ย
    ("answer", ["d06"], 0.1, 0.3, 2.0),               # เต้ย at the door, green on his face
    ("wade", ["a21"], 0.1, 0.3, 3.2),                 # he walks down into the flood after it
    ("shout", ["d07"], 0.05, 0.3, 1.8),               # ฝน at the door
    ("know2", ["a23", ("a24", 0.1)], 0.1, 0.4, 5.4),  # a line in the water: the water can be live; always assume it is
    ("know3", ["a25"], 0.1, 0.5, 4.0),                # stay ten metres back, call 1129
    ("sig", ["s01"], 0.15, 0.4, 4.4),                 # channel signature
    ("clue", ["a26", ("a27", 0.15)], 0.2, 0.5, 5.4),  # ป้าแช่ม's window left open; the light came out of it
    ("whisper", ["r02"], 0.2, 0.3, 4.2),              # by the line, in the dark: only her eyes — "อีกนิดเดียว… ลูก…"
    ("choice", [], 0.0, 0.0, 3.2),                    # shout at him / wade in after him
    ("next", [], 0.0, 0.0, 2.4),                      # end card: the sign on the pole
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
