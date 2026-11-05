"""สกิลจอมโกหก EP.3 (lane A, storytelling). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("c01", ["j3h"], 0.05, 0.35, 2.6),                        # hook: you in the bucket, the % climbing over your head
    ("c02", ["p13_1"], 0.05, 0.25, 5.2),                      # 12… 31… 47…
    ("c03", ["p13_2"], 0.05, 0.2, 3.8),                       # through the window: the thing out cold by the road
    ("c04", ["p13_3", "p13_4"], 0.05, 0.4, 7.0),              # gecko → monitor lizard → crocodile → a baby dragon the size of a cart
    ("c05", ["p14_1", "p14_2"], 0.05, 0.3, 2.6),              # Ken slams the table: "โม้ทั้งเพ!"
    ("c06", ["p14_3", "p14_4"], 0.05, 0.35, 4.8),             # you growl from the bucket: "ข้านี่แหละ ราชาปีศาจ"
    ("c07", ["p14_5"], 0.05, 0.3, 3.0),                       # Ken falls off his chair, the tavern laughs
    ("c08", ["p14_6"], 0.05, 0.5, 3.8),                       # faint grey numbers drift up from their heads (the set-up)
    ("c09", ["p15_1", "p15_2"], 0.05, 0.3, 4.1),              # 99 — one short
    ("c10", ["p15_3", "p15_4"], 0.05, 0.25, 6.5),             # all eyes on the counter: มะปราง wiping a tear
    ("c11", ["p15_5"], 0.05, 0.4, 2.0),                       # "เชื่อก็ได้… เรื่องมันสนุก"
    ("c12", ["p16_1", "p16_2", "p16_3"], 0.05, 0.3, 3.4),     # ติ๊ง 100% · บึ้ม · the glass shakes
    ("c13", ["p16_4"], 0.05, 0.6, 5.4),                       # a real dragon the size of a building, out cold in the square
    ("c14", ["p17_1", "p17_2"], 0.05, 0.4, 4.9),              # that night the board spins: rank one
    ("c15", ["p17_3"], 0.05, 0.8, 3.6),                       # the worst skill… the most broken skill in the world
    ("c16", [], 0, 0, 3.0),                                   # next episode
    ("c17", [], 0, 0, 2.4),                                   # the channel logo
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
