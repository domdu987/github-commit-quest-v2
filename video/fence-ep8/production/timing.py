"""Derive shot timing from the recorded voice so picture and sound share one schedule (เอาชีวิตรอด 99 วัน EP.8 ยาตู้เย็น).

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
    ("hook", ["n01", ("n02", 0.2), ("n03", 0.25)], 0.4, 0.5, 8.5),      # inside the dead medicine fridge: เจ๊หงส์'s hand on the insulin vial, thermometer creeping up, "ไฟดับมาแล้ว" 1 → 26 h
    ("chapter", ["n04"], 0.3, 0.5, 5.0),                                # the yard after the storm, cracked solar panels; the board "เหลือ 92 วัน"
    ("dark", ["n05", ("w01", 0.3)], 0.3, 0.5, 6.5),                     # the canteen: the red-cross fridge dark; คุณวิน keeps the power for his own room
    ("hong", ["n06", ("h01", 0.3)], 0.3, 0.7, 7.5),                     # เจ๊หงส์ takes out her insulin, feels the warm vial, pushes the box away; ปั้น watches
    ("skip", ["n07", ("n08", 0.3)], 0.4, 0.5, 5.5),                     # the dorm at dusk: she skipped it; by night she can't get up; ปั้น hugs the box
    ("kong", ["k01", ("p01", 0.15)], 0.3, 0.9, 4.8),                    # ก้อง at the barred window, คุณวิน's lit window; "ก้อง… อย่า!" — he's gone
    ("steal", ["n09"], 0.6, 1.6, 4.8),                                  # the office: ก้อง opens the small fridge, cold light on his face; a torch behind the door glass
    ("label", ["pn01", ("ph01", 0.3), ("ph02", 0.25)], 0.3, 0.6, 10.0), # ปั้น holds the box out to ภู; the label card "28 วัน"; เจ๊หงส์ opens her eyes
    ("card", ["n10", ("n11", 0.35)], 0.2, 0.6, 12.0),                   # the card: a day without power → replace, unless the label says; insulin 28 days; a life-saving drug — don't stop
    ("real", ["n13"], 0.2, 0.5, 4.4),                     # in real life: shade, coolest place, never frozen; check sugar more often; doctor or pharmacist
    ("alarm", ["n14"], 0.3, 1.4, 6.0),                                  # the torch on ก้อง, the box drops, guards; the estate bell
    ("run", ["w02", ("p02", 0.5)], 0.6, 2.4, 4.8),                      # across the yard under the searchlights; ภู shoves a guard, ก้อง breaks free
    ("gate", ["h02", ("p03", 0.9)], 0.8, 1.2, 5.5),                     # the sliding gate from outside: เจ๊หงส์ pushes ปั้น through; it slams with her inside
    ("outside", ["pn02"], 0.8, 0.6, 4.2),                               # the dark field; ปั้น holds the insulin box
    ("walkie", ["w03", ("w04", 0.4), ("n15", 0.5)], 0.6, 0.6, 12.0),    # ภู's bag crackles: คุณวิน "ขอบใจนะ ที่บอกทางไปโรงเรียนให้ฉัน ตั้งแต่วันแรก"; rule three
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("count", ["r01"], 0.4, 0.8, 6.0),                                  # the radio: "เก้าสิบเอ็ดวัน… สี่"
    ("drawing", ["n16"], 0.3, 0.6, 4.4),                                # ปั้น's drawing: everyone wading through a flooded field (EP.9)
    ("choice", [], 0.0, 0.0, 3.4),
    ("next", [], 0.0, 0.0, 2.6),
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
