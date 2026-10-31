"""ต่อหัวเสือ EP.1 ต่อรุม อย่าลงน้ำ. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01"], 0.1, -0.1, 2.5),        # the yard, the title plank on the shrine fence; แทน running for the pond, the swarm behind her
    ("cmd", ["n02"], 0.05, 0.4, 1.7),         # แทน at the pond's edge; behind her ตา's door stands open (0:03, the planted mistake)
    ("why", ["n03"], 0.1, 0.2, 4.4),         # card: the pond in section — they wait above the water; you have to come up to breathe
    ("back", ["n04"], 0.1, 0.3, 3.6),         # ten minutes earlier: the calm yard, ใบข้าว and แทน, name tags
    ("palm", ["b01"], 0.1, 0.3, 2.8),         # ใบข้าว aims his slingshot at the pods
    ("reveal", ["n05"], 0.1, 0.15, 4.6),       # tilt from the shrine up to the nest — nobody looks up
    ("legend", ["n06"], 0.1, 0.2, 5.4),       # the shadow screen: the เจ้าที่ and his soldiers
    ("sing", ["n07"], 0.2, 0.3, 4.2),         # ป้านวล: long sleeves, boots, the sun blazing
    ("crazy", ["b02"], 0.1, 0.3, 1.8),        # ใบข้าว leans to แทน
    ("first", ["n08"], 0.1, 0.6, 3.6),        # the first hornet circles แทน's face — she swats it
    ("still", ["n09"], 0.15, 0.4, 3.6),       # card: one → stand still ✓ / swat → stung ✗
    ("wake", ["n10"], 0.15, 0.7, 2.6),        # the nest's hole: the soldiers pour out
    ("toey", ["k01"], 0.05, 0.3, 1.8),        # แทน: "สระ! โดดน้ำ!"
    ("rule", ["g01"], 0.1, 1.0, 3.8),         # ตา's voice from somewhere → the rule board (rule 1)
    ("know", ["n11"], 0.1, 0.2, 5.0),        # card: open ground ✗ / indoors ✓
    ("grab", ["n12"], 0.1, 0.3, 2.8),         # ป้านวล throws his towel over แทน and hauls her off the bank (the scars on his hand)
    ("shed", ["w01"], 0.05, 0.9, 2.4),        # the shed door slams; hornets thud on the screen
    ("rw", ["n13", "n14"], 0.15, 0.4, 6.2),    # ↺ 0:03: the open door behind her
    ("where", ["b03"], 0.1, 0.4, 2.2),        # ใบข้าว made it into ตา's house: the empty room
    ("shrine", ["n15"], 0.1, 0.3, 2.8),       # ยาย at the shrine all along, hunched, the swarm above
    ("fine", ["g02"], 0.1, 0.9, 2.4),         # "ยายไม่เป็นไรหรอก" — her arm dotted with stings
    ("next", [], 0, 0, 3.8),                  # next: ตอนที่ 2 (ตอนจบ) ยายบอกว่าไม่เป็นไร
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
