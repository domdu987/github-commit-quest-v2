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
    ("recap", [], 0.0, 0.0, 2.2),                     # EP.1's last image: ดาว sitting up on แพร's bed, your hand on the knob
    ("hook", ["n01"], 0.25, 0.5, 4.8),                # the fire-escape plan: you are here, 714 · title EP.2
    ("knob", ["n02", ("g01", 0.25)], 0.1, 0.4, 5.6),  # wide, from behind ดาว on the bed: you at the door, hand on the knob; she whispers
    ("cool", ["n03"], 0.1, 0.4, 4.6),                 # low at the gap: water running in (the hoses), up to your fist on the cooled knob
    ("slow", ["n04", ("n05", 0.2)], 0.1, 0.5, 7.0),   # side on: the door eases open on the dark; ready to shut it
    ("prae", ["d01"], 0.1, 0.4, 3.4),                 # through the gap: แพร's face in the smoke
    ("dark", ["n06"], 0.1, 0.4, 3.6),                 # wide down the corridor: you step out into the black with the torch
    ("close", ["n09", ("g02", 0.5)], 0.1, 0.6, 6.4),  # side on in the corridor: you pull 714's door shut; knocking and her voice inside
    ("blind", ["n07"], 0.1, 0.4, 6.0),                # your eyes: the smoke rolls down, the torch beam dies in it (fire is dark)
    ("low", ["n08"], 0.1, 0.4, 4.6),                  # floor level, side on: you drop and crawl toward the exit sign
    ("hand", ["d02"], 0.1, 0.4, 3.4),                 # close: a hand finds yours in the dark ("แพร")
    ("alarm", ["n10"], 0.1, 0.5, 5.0),                # the red fire-alarm station: you pull it; bells, strobes
    ("doors", ["n11"], 0.3, 0.9, 6.0),                # jump: every door down the corridor swings open; eyes in every room
    ("sig", ["s01"], 0.15, 0.5, 4.8),                 # channel signature
    ("cold", ["n12"], 0.2, 0.8, 4.4),                 # the torch finds the hand you are holding: black, cracked, glowing
    ("far", ["d03"], 0.1, 0.6, 3.6),                  # far down the corridor: แพร at the stairwell door, her own torch
    ("lift", ["n13", ("g03", 0.4)], 0.3, 0.9, 6.4),   # ding: the lift opens, bright and clear; ดาว stands inside
    ("choice", [], 0.0, 0.0, 3.6),                    # take the lift / take the stairs
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
