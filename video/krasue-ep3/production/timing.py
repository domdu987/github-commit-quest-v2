"""แสงกระสือ EP.3 (สูตรเสียงกอย re-cut). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("recap", [], 0.0, 0.0, 2.0),                       # EP.2's last image: the door, green light seeping under it
    ("hook", ["n01", ("n02", 0.15)], 0.3, 0.7, 5.4),    # flash-forward: morning, a hand pushing the main switch up — cut
    ("latch", ["n03"], 0.1, 0.4, 2.6),                  # close: ฝน's hand on the door bolt, green between the planks
    ("open", ["r01"], 0.3, 0.4, 4.4),                   # the door from inside, the green under it
    ("toey", ["c01"], 0.1, 0.3, 3.6),                   # เต้ย on the stairs looking up: the voice comes from above
    ("shush", ["c02"], 0.05, 0.4, 3.4),                 # ฝน, a finger to her lips: the first rule
    ("why", ["r02"], 0.2, 0.4, 4.8),                    # the door: knocking, the green brighter
    ("face", ["n07"], 0.2, 0.8, 4.6),                   # the window close: only eyes — a bun; the koi-style hit
    ("dawn", ["n08"], 0.1, 0.5, 4.6),                   # dawn over the flood; the light floats back to the house next door
    ("morning", ["c03", ("c04", 0.25)], 0.1, 0.3, 6.8), # morning, mud everywhere: เต้ย teases about the views; ฝน goes to turn the power on
    ("reach", [], 0.0, 0.0, 1.4),                       # her hand on the lever
    ("stop", ["d02"], 0.05, 0.4, 2.8),                  # ลุงเปี๊ยก at the door: อย่า!
    ("know1", ["n11"], 0.1, 0.5, 4.6),                  # diagram: an electrician checks before the power goes back on
    ("joke", ["c05", ("c06", 0.2)], 0.1, 0.4, 5.0),     # เต้ย: you're an electrician; ลุงเปี๊ยก: that's why — move!
    ("know2", ["n12"], 0.1, 0.5, 5.4),                  # diagram: appliances that were under water — dry, then checked
    ("know3", ["n13"], 0.1, 0.5, 5.8),                  # diagram: sparks or a burning smell — the main switch down at once
    ("outlet", ["d03"], 0.5, 0.4, 4.4),                 # the outlet behind the fridge, burnt black, the tester: ลุงเปี๊ยก: this is where it leaked
    ("who", ["c07", ("c08", 0.25)], 0.1, 0.6, 7.0),     # ฝน asks who pushed it up; the lever close: green slime on it
    ("pot", ["n16", ("c09", 0.2)], 0.1, 0.4, 5.6),      # the porch: ฝน with the pot, เต้ย behind her refusing the curry
    ("mat", ["c10"], 0.1, 0.4, 3.2),                    # top-down: ป้าแช่ม asleep on the mat, the blanket to her chin
    ("rag", ["n18"], 0.1, 0.5, 4.2),                    # by the pillow: a rag smeared green
    ("wake", ["d04"], 0.6, 0.4, 4.8),                   # her eyes open, a smile
    ("glint", ["n20"], 0.1, 0.8, 3.8),                  # her eyes flash green
    ("night", ["c11"], 0.2, 0.6, 3.0),                  # that night: the water up again, a green light over the field
    ("call", ["r03"], 0.3, 1.5, 6.6),                   # the light close: the face, calling — koi-style hit
    ("last", ["n22"], 0.3, 1.0, 5.4),                   # black; one green light; the rule
    ("end", [], 0.0, 0.0, 3.0),                         # end card: the sign on the pole — ตอนจบ
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
