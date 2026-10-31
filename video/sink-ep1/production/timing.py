"""นาทีก่อนจม EP.1 อย่าเพิ่งโทรหาใคร. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01"], 0.15, -0.3, 2.6),          # the canal road at 1 a.m.: the car's headlights along the dark water, no rail
    ("lock", ["n02"], 0.3, 0.3, 1.9),            # insert: ต้น presses the window lock (the planted mistake, LED on at ~0:04)
    ("float", ["n03"], 0.2, 0.3, 3.4),           # the car floating nose-down in the canal; the countdown starts
    ("all", ["n04"], 0.1, 0.4, 2.6),             # under the water: the headlights' beams in the murk, bubbles
    ("drive", ["n05"], 0.2, 0.2, 4.0),           # 1 a.m., the drive home: the road through the windscreen
    ("swerve", ["n06"], 0.1, 0.8, 2.4),          # an unlit motorbike in the headlights → the swerve
    ("plunge", [], 0, 0, 1.6),                   # outside: the car goes off the bank into the canal, the splash
    ("inrush", [], 0, 0, 2.0),                   # inside: the jolt, water spurting in at the door seals, the countdown appears
    ("belt", ["n07"], 0.2, 0.3, 2.8),            # in the cabin: water at the floor; step 1
    ("door", ["n08"], 0.2, 0.3, 3.2),            # the door: the water outside presses it shut
    ("window", ["n09"], 0.2, 0.3, 3.4),          # his window goes down
    ("kid", ["n10"], 0.2, 0.3, 2.8),             # he turns to ขิม
    ("phone", ["n11"], 0.2, 0.4, 3.0),           # the phone on the seat, the water rising round it; call 1669 once ashore
    ("rw", ["n12"], 0.2, 0.6, 4.2),              # rewind to 0:04: the lock pressed
    ("kim", ["k01"], 0.1, 0.4, 2.2),             # her window: she presses, nothing; the water outside at the glass
    ("led", ["n13"], 0.2, 0.3, 2.4),             # the lock's orange light still on
    ("panel", ["n14"], 0.2, 0.3, 3.0),           # he presses her window on his own panel: nothing (some cars lock every window but the driver's)
    ("flicker", ["n15"], 0.2, 0.9, 2.8),         # the dash lights flicker; the countdown at single digits
    ("next", [], 0, 0, 4.2),                     # next-episode card + channel
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
