"""ตึกโยก EP.1 หมอบ ป้อง เกาะ. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.6, 0.5, 4.8),            # title opener: the tower sways against the sky, the rooftop pool slops over; ตึกโยก · EP.1
    ("hook", ["n02"], 0.15, 0.8, 2.6),           # POV down the corridor of floor 27: it tilts, the sign swings, the lift at the end
    ("back", ["n03"], 0.5, 0.5, 3.0),            # tape rewind → the rider app in your hand: room 2714, มิว, ETA 02:00 counting down, 13:18
    ("lobby", ["s01"], 0.3, 0.5, 4.0),           # the lobby: ลุงสมศักดิ์ points from his desk; the right lift has a paper sign
    ("lift", [], 0, 0, 2.4),                     # POV in the lift: you press 27, the display runs up; the ETA keeps falling
    ("door", ["m01"], 0.6, 0.3, 3.2),            # 2714 opens: มิว blows the whistle; the room behind her (table, window wall, fridge)
    ("bag", ["m02"], 0.15, 0.3, 3.2),            # she peeks into the delivery bag
    ("whistle", ["m03"], 0.2, 0.4, 3.4),         # insert: the orange whistle; by the door the red emergency bag with a torch
    ("ripple", ["n04"], 0.4, 0.8, 2.8),          # 13:20: rings in the glass of water, the lamp starts to swing
    ("tower", [], 0, 0, 2.4),                    # outside: the tower sways, the pool spills down its side, birds burst off
    ("panic", ["m04"], 0.1, 0.5, 2.6),           # มิว grabs your hand, pulling toward the lift
    ("choice1", [], 0, 0, 3.2),                  # the choice: วิ่งไปลิฟต์ / หมอบใต้โต๊ะ, 3-2-1 — it picks the lift
    ("wrong", [], 0, 0, 2.2),                    # you run in, the doors close, 27 → 26 → 25
    ("stuck", ["n05"], 0.7, 0.7, 3.6),           # the power dies: dark, a jolt, the red emergency light, the display goes blank
    ("rewind", [], 0, 0, 1.6),                   # tape rewind back to the choice: ✓ หมอบใต้โต๊ะ
    ("drop", ["n06"], 0.4, 0.4, 3.0),            # you pull มิว under the table
    ("cover", ["n07"], 0.2, 0.6, 3.8),           # under the table: หมอบ / ป้อง / เกาะ marked on the two of you; the lamp hits the tabletop
    ("slide", ["m05", ("n08", 0.15)], 0.2, 0.5, 4.6),  # the table slides; you shuffle with it, still holding the leg
    ("glass", [], 0, 0, 2.2),                    # the window wall cracks and bursts inward; the power cuts
    ("danger", ["n09"], 0.3, 0.6, 3.8),          # mom's plan of the room: red zones (glass, lamp, shelf, tank), the table green
    ("run", ["m06"], 0.1, 0.4, 2.6),             # มิว tries to crawl out; your hand holds her arm
    ("fall", ["n10"], 0.3, 0.6, 3.8),            # the corridor: ceiling panels crash where a ghost-you is running
    ("rule", ["m07"], 0.3, 1.2, 5.0),            # the fridge note → the rule card (rule 1 lit)
    ("stop", ["m08"], 0.7, 0.3, 3.0),            # the shaking stops; dust settles; the fire alarm starts
    ("after", ["n11"], 0.2, 0.6, 3.8),           # the seismogram: the main shock, then aftershocks — หลบซ้ำ
    ("real", ["n12", ("n13", 0.15), ("n14", 0.15)], 0.3, 0.6, 8.0),  # the map: Myanmar → Bangkok, 28 มี.ค. 2568 13:20 ขนาด 8.2; towers sway > 20 s
    ("mom", ["m09"], 0.3, 0.6, 2.8),             # มิว calls แม่: no answer
    ("dark", [], 0, 0, 2.0),                     # you open the door: the corridor is pitch black; the emergency light dies
    ("candle", ["m10", ("n15", 0.3)], 0.3, 0.6, 5.0),  # มิว takes a candle and matches from the shrine cabinet; behind her the gas canister hisses
    ("choice2", [], 0, 0, 3.4),                  # your call: จุดเทียน / ใช้ไฟฉาย — the match strikes → black
    ("end", [], 0, 0, 2.6),                      # the end card: the orange whistle with its tag "ตอนที่ 2 · ลงบันได"
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
