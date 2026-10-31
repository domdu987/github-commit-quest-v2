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
    ("hook", ["n01", ("n02", 0.2), ("n03", 0.25)], 0.3, 0.2, 7.0),      # inside the dead medicine fridge: her hand on the vial, the thermometer, "ไฟดับมาแล้ว 26 ชม."
    ("dark", ["n04", ("n05", 0.3)], 0.3, 0.3, 7.0),                     # the canteen: the board "เหลือ 92 วัน"; the storm broke the panels; the red-cross fridge dark all night
    ("hong", ["n06", ("h01", 0.3)], 0.3, 0.5, 6.8),                     # เจ๊หงส์ feels the warm vial, pushes the box away; ปั้น watches
    ("skip", ["n07", ("n08", 0.3)], 0.3, 0.3, 4.8),                     # the dorm at dusk: she skipped it; by night she can't get up
    ("kong", ["k01", ("p01", 0.15)], 0.3, 0.7, 4.4),                    # ก้อง at the barred window; "ก้อง… อย่า!" — he's gone
    ("steal", ["n09"], 0.6, 0.8, 3.6),                                  # the office: the bar fridge, cold light; a torch behind the door glass
    ("label", ["pn01", ("ph01", 0.3), ("ph02", 0.25)], 0.3, 0.3, 8.0),  # the label: 28 days; "ยังใช้ได้… อย่าหยุดยา"; เจ๊หงส์ opens her eyes
    ("card", ["n10", ("n11", 0.3)], 0.2, 0.3, 10.0),                    # the four rules
    ("alarm", ["n14"], 0.3, 0.7, 4.6),                                  # the torch on ก้อง, the box drops, the bell
    ("run", ["w02", ("p02", 0.5)], 0.6, 1.5, 3.8),                      # across the yard under the searchlights
    ("gate", ["h02", ("p03", 0.9)], 0.8, 0.8, 4.6),                     # the gate slams with เจ๊หงส์ inside
    ("walkie", ["pn02", ("w03", 0.4), ("w04", 0.3), ("n15", 0.35)], 0.3, 0.3, 12.0),   # the field: "ยาของเจ๊อยู่กับหนู"; the walkie: "ขอบใจที่บอกทาง… ตั้งแต่วันแรก"
    ("confess", ["ph03", ("ph04", 0.4), ("p04", 0.35)], 0.3, 1.2, 9.0), # ภู: the voice is คุณวิน counting; "ผมจะไปพาเจ๊กลับมาเอง" — he walks back; "ภู…!"
    ("dawn", ["n17", ("pn03", 1.1), ("n18", 0.5)], 0.4, 1.3, 7.5),      # the gate opens at dawn; เจ๊หงส์ walks out alone; ภู behind the bars; it closes
    ("radio", ["r01", ("p05", 0.9)], 0.4, 0.6, 8.0),                    # "เก้าสิบเอ็ดวัน… สี่" — ครูพิม turns it off: "ไม่ต้องให้ใครนับเราอีก"
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("choice", [], 0.0, 0.0, 3.4),
    ("end", [], 0.0, 0.0, 2.8),
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
