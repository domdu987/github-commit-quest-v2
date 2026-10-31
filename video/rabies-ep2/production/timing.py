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
    ("hook", ["n01"], 0.1, -0.15, 2.5),            # day: ไอ้ดำ wagging by ยาย, her hand bound in herbs; it looks fine
    ("cmd", ["n02"], 0.05, 0.25, 1.6),          # close: ยาย strokes its head — the bite on its ear (the planted mistake, ~0:03)
    ("warn", ["y01"], 0.15, 0.3, 2.6),          # two days earlier, night: ยาย stops the kids at the stair
    ("hide", ["n03"], 0.15, 0.4, 3.0),          # under the house: only its eyes
    ("snap", ["n04"], 0.15, 0.5, 3.0),          # ยาย crawls in with rice; a snap in the dark
    ("herb", ["y02"], 0.15, 0.4, 3.0),          # the kitchen: ยาย pounds herbs onto her hand
    ("home", ["n05"], 0.15, 0.5, 5.0),          # card: the home dog fights a dog from outside · herbs crossed out
    ("khiao", ["k01"], 0.15, 0.4, 2.6),         # villagers with sticks at the fence; ลุงเขียว steps in
    ("pen", ["n06"], 0.15, 0.4, 3.0),           # ไอ้ดำ in a pen under the house, a note "ดูอาการ 10 วัน"
    ("map", ["n07"], 0.1, 0.4, 2.8),            # the village map: the motorbike to the clinic
    ("race", ["n08"], 0.15, 0.5, 4.0),          # card: the race
    ("rule", ["y03"], 0.15, 0.5, 3.0),          # the clinic: ยาย says the rule; the board, rule 2
    ("confess", ["p01"], 0.15, 0.5, 2.8),       # ภูมิ raises his hand
    ("rw", ["n09", "n10"], 0.15, 0.4, 3.2),     # rewind to 0:03
    ("ear", ["n11"], 0.15, 0.5, 3.0),           # the ear, ringed
    ("day6", ["n12"], 0.2, 0.5, 3.4),           # the empty pen, the red collar on the post · then the clinic card
    ("end", ["p02"], 0.2, 0.6, 3.0),            # ภูมิ with the collar, ยาย beside him
    ("final", ["n13"], 0.2, 1.2, 3.6),          # the board, both rules ticked, ตอนจบ
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
