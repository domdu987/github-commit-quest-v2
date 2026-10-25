"""แสงกระสือ EP.3. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01", ("n02", 0.15)], 0.3, 0.7, 5.4),    # flash-forward: morning, a hand pushing the main switch up — stamped out · EP.3
    ("latch", ["n03"], 0.1, 0.4, 2.8),                  # close: ฝน's hand on the door bolt, green between the planks
    ("open", ["r01"], 0.3, 0.5, 4.8),                   # the door from inside, the green under it
    ("rule1", ["n04", ("d01", 0.2)], 0.1, 0.6, 5.0),    # the rule card, row one: แสงลอยผ่าน อย่าขาน
    ("silent", ["n05"], 0.1, 0.5, 3.6),                 # ฝน close, her hand over her mouth
    ("why", ["r02"], 0.3, 0.5, 5.4),                    # the door: knocking, the green brighter
    ("rise", ["n06"], 0.1, 0.5, 4.4),                   # the light lifts from under the door to the window
    ("face", ["n07"], 0.2, 0.8, 4.6),                   # the window close: a face against the glass — a bun
    ("dawn", ["n08"], 0.1, 0.6, 5.0),                   # dawn over the flood, a rooster; the light floats back to the house next door
    ("morning", ["n09"], 0.1, 0.4, 4.2),                # morning inside: the water gone, mud, the tide line on the walls
    ("reach", ["n10"], 0.1, 0.3, 3.4),                  # ฝน on the stairs reaching for the lever
    ("stop", ["d02"], 0.05, 0.4, 3.0),                  # ลุงเปี๊ยก at the door: อย่า!
    ("know1", ["n11"], 0.1, 0.6, 5.0),                  # knowledge: don't turn the power back on until an electrician checks
    ("know2", ["n12"], 0.1, 0.6, 5.6),                  # knowledge: anything that was under water must be dry and checked first
    ("know3", ["n13"], 0.1, 0.6, 5.0),                  # knowledge: sparks or a burning smell — switch off at once
    ("outlet", ["n14"], 0.1, 0.5, 5.0),                 # the outlet behind the fridge, burnt black; the tester
    ("here", ["d03"], 0.1, 0.4, 3.6),                   # ลุงเปี๊ยก close: this is where it leaked
    ("who", ["n15"], 0.1, 0.7, 4.6),                    # the switch close up: a long black hair caught on the lever
    ("pot", ["n16"], 0.1, 0.4, 3.6),                    # ฝน walking along the porch with the pot
    ("mat", ["n17"], 0.1, 0.5, 5.0),                    # top-down: ป้าแช่ม asleep on the mat, the blanket to her chin
    ("rag", ["n18"], 0.1, 0.6, 4.0),                    # by the pillow: a rag smeared green
    ("wake", ["n19", ("d04", 0.2)], 0.1, 0.5, 6.4),     # her face: eyes open, a smile
    ("glint", ["n20"], 0.1, 0.8, 3.8),                  # her eyes flash green
    ("night", ["n21"], 0.2, 0.5, 5.4),                  # that night: the water up again, a green light over the field
    ("call", ["r03"], 0.3, 0.6, 6.6),                   # the light close: the face, calling
    ("last", ["n22"], 0.3, 1.0, 5.6),                   # black; one green light; the rule
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
