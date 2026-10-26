"""Derive shot timing from the recorded voice so picture and sound share one schedule (เอาชีวิตรอด 99 วัน EP.5 ปั๊มร้าง).

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
    ("hook", ["n01", ("n02", 0.3), ("n03", 0.3)], 0.3, 0.4, 7.0),        # first person on the white-hot highway, the last bottle; "อย่ารอให้หิวน้ำ"
    ("chapter", ["n04"], 0.15, 0.4, 3.2),                               # the board: 95 days; the school is not safe any more
    ("pack", ["d01", ("d02", 0.25)], 0.2, 0.35, 6.0),                   # ลุงหมาน's pickup, three litres, six bottles, five people
    ("wave", ["n05", ("d03", 0.3), ("d04", 0.25)], 0.3, 1.0, 7.5),      # seen from the fallen fence: ปั้น waves from the truck bed; "ลุงหมานค่ะ" — the gap is empty, the hat
    ("highway", ["n06", ("n07", 0.25)], 0.3, 0.4, 6.5),                 # top-down between the dead cars; at noon they are slow
    ("empty", ["n08", ("d05", 0.3)], 0.4, 0.4, 5.5),                    # the fuel needle at E, the engine coughs out on the bridge; four kilometres
    ("walk", ["n09", ("n10", 0.2), ("d06", 0.2)], 0.2, 0.3, 9.0),       # 39 degrees; ก้อง carries the most and will not drink
    ("rule", ["n11", ("n12", 0.2)], 0.15, 0.5, 5.5),                    # NIOSH: thirst is already heat exhaustion; a cup every 15–20 minutes
    ("confuse", ["d07", ("n13", 0.25)], 0.3, 0.6, 6.0),                 # "ทำไมถนนมันเอียง" — he goes down on the road
    ("signs", ["d08", ("n14", 0.25), ("n15", 0.2)], 0.2, 0.5, 9.0),     # hot, dry, confused: heat stroke; 41 degrees in 10–15 minutes
    ("shade", ["d09"], 0.2, 0.6, 3.6),                                  # drag him into the shade, off with the outer shirt
    ("nodrink", ["d10", ("d11", 0.1), ("n16", 0.25)], 0.1, 0.4, 6.5),   # ปั้น runs with the bottle; "เขาไม่รู้สึกตัว" — nothing by mouth
    ("craft", ["d12", ("d13", 0.15), ("n17", 0.3), ("n18", 0.2), ("n19", 0.3)], 0.2, 0.8, 15.0),   # "น้ำเหลือสองขวด" — "ใช้ไปเลย"; the cooling cloths, first person
    ("lunge", ["n20", ("n21", 1.2)], 0.2, 0.6, 6.0),                    # not only us under the bridge: the lunge; ครูพิม uses ก้อง's spear
    ("wake", ["n22", ("d14", 0.3)], 0.3, 0.5, 5.0),                     # twenty minutes: his eyes open; "ค่อยๆ จิบ"
    ("real", ["n23", ("n24", 0.2)], 0.15, 0.5, 6.5),                    # in real life: an ambulance at once; stay, shade, cool fast
    ("station", ["n25", ("n26", 0.25), ("n27", 0.2)], 0.3, 0.4, 8.0),   # dusk: the station; the fridge still full; the door locked from inside
    ("roof", ["d15"], 0.1, 0.5, 3.0),                                   # "มีคนอยู่บนหลังคา"
    ("gun", ["g01", ("d16", 0.3), ("g02", 0.25)], 0.2, 0.6, 8.0),       # the rifle on the canopy; "ขอแค่น้ำ" — "ไม่มีอะไรฟรี"
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("radio", ["r01", ("n28", 0.3), ("g03", 0.3)], 0.5, 0.4, 10.0),     # 94… five; the guard hears it too
    ("name", ["g04", ("n29", 0.35)], 0.4, 0.6, 6.0),                    # the torch on ภู's face: "คุณวินคิดว่าแกตายไปแล้ว"
    ("drawing", ["n30", ("n31", 0.2)], 0.2, 0.6, 6.0),                  # the drawing: the lit factory, ภู shaking hands with a man in a tie
    ("choice", [], 0.0, 0.0, 3.4),
    ("next", [], 0.0, 0.0, 2.4),
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
