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
    ("hook", ["n01"], 0.05, -0.15, 2.4),          # night on the island: the tail on the rocks in the wind, lights across the bay; คิว in the door
    ("cmd", ["n02"], 0.15, 0.35, 1.5),           # he steps down toward the lights → red
    ("night", ["n03"], 0.2, 0.2, 3.6),           # inside the tail: hunched against the cold, the orange vest under his jacket (the planted mistake ~0:04)
    ("roof", ["n04"], 0.2, 0.3, 3.0),            # outside: the wind and spray beat on the tail; his light inside
    ("lights", ["n05"], 0.2, 0.3, 3.2),          # 4 a.m.: lights blink across the bay
    ("village", ["q01"], 0.1, 0.3, 2.6),         # he jumps up
    ("spot", ["n06"], 0.2, 0.3, 3.4),            # card: one person from the air (✗)
    ("wreck", ["n07"], 0.2, 0.3, 3.4),           # card: the wreck from the air (✓)
    ("route", ["n08"], 0.2, 0.4, 4.0),           # card: they search the flight path first
    ("wait", ["q02"], 0.1, 0.4, 2.4),            # he sits back down by the wreck
    ("heli", ["n09"], 0.2, 0.2, 2.6),            # dawn: rotor sound, a helicopter over the sea
    ("wave", ["q03"], 0.1, 0.3, 2.2),            # he waves and shouts
    ("pass", ["n10"], 0.2, 0.3, 3.6),            # it flies on: the grey wreck lost on the grey rocks
    ("rw", ["n11"], 0.2, 0.6, 4.0),              # rewind to 0:04
    ("vest", ["n12"], 0.2, 0.3, 2.6),            # he opens the jacket: the orange vest
    ("lay", ["n13"], 0.2, 0.4, 4.0),             # the vest on the tailplane, the cowl panel propped to the sun
    ("stand", ["n14"], 0.2, 0.3, 2.6),           # wide: the tail stands out
    ("glint", [], 0, 0, 2.2),                    # the helicopter turns back, the panel flashes
    ("found", ["r01"], 0.1, 0.4, 3.2),           # "found!" — hovering over him: relief
    ("empty", ["r02"], 0.1, 0.5, 3.0),           # the turn: the front section across the bay at dawn — empty, a dropped torch, footprints
    ("truth", ["n15", ("n16", 0.3)], 0.2, 0.4, 5.6),   # flashback, 4 a.m.: the torches were survivors, and they saw HIS phone light
    ("walkoff", ["n18"], 0.2, 0.5, 3.6),         # flashback: the torches leave the wreck and wind off along the shore into the dark
    ("end", ["n17", ("n19", 0.4)], 0.2, 1.2, 5.0),   # the helicopter lifts him away; the safety card ticks both rules
    ("fin", [], 0, 0, 4.0),                      # end card: ตอนจบ
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
