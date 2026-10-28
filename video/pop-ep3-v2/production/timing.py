"""เห็ดปอบ EP.3. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("recap", [], 0.0, 0.0, 2.4),                       # EP.2's last image: the ward window, the handprint
    ("hook", ["n01", ("n02", 0.15)], 0.2, 0.9, 4.8),    # flash-forward: the empty bed, the drip swinging — cut
    ("home", ["y01"], 0.1, 0.4, 3.2),                   # ยายคำ at the bedside: let's go home
    ("no", ["m01"], 0.05, 0.3, 2.2),                    # มิ้นท์: the doctor hasn't said so
    ("doc", ["d01"], 0.1, 0.4, 3.0),                    # the doctor: better is not well
    ("know1", ["n03", ("n04", 0.15)], 0.1, 0.8, 7.0),   # diagram: the three stages drawn as they are spoken
    ("know2", ["n05"], 0.1, 0.8, 5.0),                  # diagram: in on the liver
    ("two", ["t01"], 0.1, 0.3, 2.6),                    # ต้น: I had two bowls
    ("scold", ["m02"], 0.05, 0.4, 2.8),                 # มิ้นท์: and who asked for seconds
    ("night2", ["n06"], 0.1, 0.6, 4.4),                 # the second night: the doctor checking
    ("relief", ["d02"], 0.1, 0.4, 3.0),                 # the doctor, relieved
    ("know3", ["n07"], 0.1, 1.2, 5.0),                  # the whole rule, the last line lit
    ("sorry", ["th01"], 0.1, 0.4, 3.0),                 # ลุงทองดี in the doorway with fruit
    ("me", ["m03"], 0.05, 0.4, 2.8),                    # มิ้นท์: I'm the one who's sorry
    ("feet", ["th02"], 0.1, 0.5, 4.0),                  # ลุงทองดี: those prints have longer toes than mine
    ("odd", ["d03"], 0.1, 0.7, 5.8),                    # the doctor: ยาย ate the same — no poison at all
    ("wake", ["n08"], 0.4, 0.6, 3.4),                   # that night: มิ้นท์ wakes
    ("sit", ["n09"], 0.3, 0.8, 4.6),                    # ยาย at the bedside, her back to us
    ("toes", ["n10"], 0.3, 0.9, 5.0),                   # her feet: muddy, the toes too long
    ("hungry", ["y02"], 0.4, 1.6, 6.6),                 # "ยายหิว… ลูก": she turns — green eyes; the hit
    ("last", ["n11", ("n12", 0.3)], 0.8, 1.2, 6.4),     # the village at night, one window lit, eyes in it
    ("rule", ["y03"], 0.4, 1.4, 5.6),                   # the rule in ยาย's voice
    ("end", [], 0.0, 0.0, 3.5),                         # end card: the forest sign — the end
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
