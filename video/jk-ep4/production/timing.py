"""สกิลจอมโกหก EP.4 (lane A, storytelling). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("d01", ["j4h"], 0.05, 0.35, 2.6),                        # hook: the bucket lifting, horns underneath
    ("d02", ["p18_1"], 0.08, 0.25, 3.4),                      # morning: you dozing against a crate, the bucket rises by itself
    ("d03", ["p18_2", "p18_3"], 0.05, 0.4, 3.9),              # horns pushing it up · two of them
    ("d04", ["p19_1", "p19_2"], 0.05, 0.4, 5.2),              # rule three, under the lens again: พูดเล่น… ก็นับ
    ("d05", ["p19_3", "p19_4"], 0.05, 0.3, 6.0),              # the whole town believed the joke; the horns grow
    ("d06", ["p20_1", "p20_2"], 0.05, 0.3, 2.9),              # royal guards close in: "จับราชาปีศาจ!"
    ("d07", ["p20_3", "p20_4"], 0.05, 0.35, 5.1),             # ถั่วงอก spreads his arms in front of you, shaking
    ("d08", ["p21_1", "p21_2", "p21_3"], 0.05, 0.25, 6.4),    # you take the bucket off in front of everyone
    ("d09", ["p21_4", "p21_5"], 0.05, 0.3, 4.4),              # "ข้านี่แหละ… ราชาปีศาจ!" · ears like two lanterns
    ("d10", ["p21_6", "p21_7"], 0.05, 0.35, 2.9),             # the town as one: "หูแดง! โม้!"
    ("d11", ["p22_1", "p22_2"], 0.05, 0.3, 4.4),              # the count drops to zero, the horns shrink away
    ("d12", ["p22_3"], 0.05, 0.4, 5.4),                       # the dragon still out cold in town: proof
    ("d13", ["p23_1"], 0.05, 0.6, 3.3),                       # for the first time, red ears saved your life
    ("d14", ["p24_1", "p24_2"], 0.08, 0.3, 5.4),              # night under the board: the kid's question
    ("d15", ["p24_3", "p24_4", "p24_5"], 0.05, 0.3, 2.9),     # you smile: "จริงสิ" · the ears flash
    ("d16", ["p24_6", "p24_7"], 0.05, 1.0, 4.6),              # ติ๊ง 1% · another gecko lands on your head
    ("d17", [], 0, 0, 3.0),                                   # end of part one
    ("d18", [], 0, 0, 2.4),                                   # the channel logo
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
