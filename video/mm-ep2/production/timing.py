"""ผีแม่ม่าย EP.2 ปั๊มให้ฟื้น. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01"], 0.3, 0.3, 2.9),            # 3 a.m. again: Fon shaking Keng, his arm flops; green eyes at the foot of the mattress
    ("hook2", ["n02"], 0.1, 0.4, 1.8),           # mom at the door with the flashlight, the dark road beyond
    ("mom", ["c01"], 0.1, 0.2, 2.6),             # mom, crying: the ghost doctor
    ("fon", ["f01"], 0.1, 0.3, 2.4),             # Fon, close: "ผีหรือไม่ผี… ต้องปั๊มก่อน!"
    ("rule", ["b01"], 0.3, 1.2, 4.2),            # memory: Bua at the sala (sepia), then rule card 2 over the dark room
    ("check", ["n03"], 0.2, 0.4, 2.6),           # Fon's cheek to his mouth, eyes on his chest: nothing
    ("call", ["f02"], 0.1, 0.2, 2.2),            # Fon on the phone, speaker on
    ("know1", ["n04"], 0.3, 0.6, 5.8),           # the phone: 1669, the checklist ticks (AED, address, condition, call-back)
    ("eta", ["o01"], 0.1, 0.4, 3.3),             # the dispatcher; the ambulance chip starts counting down from 12:00
    ("window", ["f03"], 0.1, 0.1, 2.4),          # Fon at the open shutters, shouting to the next house
    ("piak", ["p01"], 0.1, 0.2, 2.8),            # Piak wakes on his bamboo platform beside สมศรี
    ("fon2", ["f04"], 0.05, 0.2, 1.4),           # Fon: the box with the heart!
    ("map", ["n05"], 0.3, 0.9, 4.4),             # the village map: Piak's motorbike to the sala (the AED pin) and back
    ("floor", ["n06"], 0.2, 0.5, 2.8),           # Fon and mom pull him off the mattress onto the planks
    ("hands", ["n07"], 0.3, 0.6, 4.6),           # insert from above: the lower half of the breastbone, heel of the hand, fingers locked
    ("pump", ["n08"], 0.2, 0.6, 5.0),            # Fon pumping: the depth gauge and the beat
    ("mouth", ["c02", ("f05", 0.1)], 0.1, 0.3, 3.2),
    ("tug", [], 0, 0, 2.6),                      # the bulb flickers; black fingers take his ankle from the dark and pull
    ("nogive", ["f06"], 0.1, 0.6, 1.6),          # Fon hauls him back: "ไม่ให้!"
    ("keep", ["n09"], 0.2, 0.4, 2.8),            # pumping on in the flicker; the chip counts down
    ("aed", ["p02", ("f07", 0.1)], 0.1, 0.3, 4.6),  # Piak bursts in with the AED case
    ("on", ["a01"], 0.1, 0.3, 4.0),              # the AED close: lid up, power, it talks
    ("pads", ["n10"], 0.3, 0.6, 4.8),            # insert from above: the two pads
    ("analyze", ["a02", ("p03", 0.1)], 0.1, 0.3, 4.4),  # hands up; ลุงเปี๊ยก's painted nails in the air
    ("shock", ["a03"], 0.1, 1.6, 4.6),           # the button; the jolt; the widow shrieks and comes apart
    ("resume", ["n11"], 0.2, 0.4, 2.8),          # straight back to the chest
    ("route", [], 0, 0, 3.4),                    # the map: the ambulance from the house to the provincial hospital
    ("arrive", [], 0, 0, 2.0),                   # the ER entrance: the ambulance pulls in, lights
    ("er", ["d01"], 0.2, 0.4, 3.0),              # the doctor to the family
    ("wake", ["k01", ("f08", 0.1)], 0.1, 0.4, 6.6),  # Keng awake on the monitor; Fon laughs and cries
    ("ask", ["d02"], 0.2, 0.4, 3.6),             # the doctor to mom
    ("silent", ["n12"], 0.3, 0.9, 2.6),          # mom looks away; behind her, in the black window, the green eyes
    ("choice", [], 0, 0, 3.3),                   # บอกหมอ / ปิดไว้ — dragged to ปิดไว้
    ("next", [], 0, 0, 2.4),                     # the tag: ตอนจบ · ตรวจใจก่อนสาย
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
