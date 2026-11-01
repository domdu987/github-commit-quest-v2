"""Derive shot timing from the recorded voice so picture and sound share one schedule (เอาชีวิตรอด 99 วัน EP.5 ปั๊มร้าง).

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
    ("hook", ["n01", ("n02", 0.25)], 0.3, 0.3, 7.0),                                   # trucks at night from the roof; the flash of the swarm on the headlights
    ("count", ["w01", ("ph01", 0.3)], 0.3, 0.5, 7.0),                    # the loudspeaker counts to ten; rule two is for the dead; lights off
    ("dark", ["n03"], 0.3, 0.3, 6.0),                                                  # adapted eyes vs the men in their own beams
    ("arrive", ["n04"], 0.3, 0.6, 5.0),                                  # the horde arrives before ten
    ("lights", ["n05", ("p02", 0.3)], 0.3, 0.4, 7.0),                    # every torch turns to them, they turn to every torch
    ("ladder", ["ph02", ("g02", 0.5), ("p03", 0.4)], 0.4, 0.4, 8.0),                   # the guard up the ladder; "เพราะเรานับได้หก"
    ("trucks", ["n06"], 0.6, 0.6, 6.0),                                  # the swarm on the trucks; the lights die one by one
    ("dawn", ["n07", ("g03", 0.3), ("h01", 0.3)], 0.3, 0.4, 9.0),                      # no trucks, no lights, no sound; the guard's lie
    ("rule6", ["n08"], 0.3, 0.6, 5.0),                                                 # rule six on the wall
    ("later", ["n09", ("r01", 0.3), ("p04", 0.3)], 0.3, 0.4, 9.0),      # twenty days later: the radio counts them as nought
    ("cliff", ["pn01"], 0.4, 0.9, 6.0),                                                # "แล้ววันที่ศูนย์… จะมีใครมามั้ย"; the storm; black
    ("sig", ["s01"], 0.15, 0.4, 4.2),
    ("next", [], 0.0, 0.0, 3.6),                                                       # ตอนที่ 8 card + tease + CTA
    ("end", [], 0.0, 0.0, 0.5),
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
