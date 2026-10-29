"""ทะเลลด EP.1 ทะเลถอย อย่าคอยดู. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.4, 0.3, 4.6),            # opener: the sea pulls back off "ทะเลลด EP.1" pressed into wet sand; fish flop
    ("hook", ["n02"], 0.1, 0.6, 2.2),            # close: a flopping fish on the sand, a child's hand reaching for it
    ("clock", ["n03"], 0.3, 0.4, 2.4),           # ร้านยาย's wall clock spins back two hours
    ("map", ["n04"], 0.3, 1.0, 4.4),             # map: Bangkok → Phang Nga, the car on the route, zoom to บ้านแหลมหอย
    ("arrive", ["j01"], 0.2, 0.3, 3.0),          # the village beach: จูน goes live on her selfie stick
    ("tang", ["t01"], 0.1, 0.3, 2.6),            # ตังค์ in his duck ring runs to the water's edge
    ("acct", ["j02", ("y01", 0.1)], 0.2, 0.4, 4.2),   # in the shop: จูน sets up "ยายพร❤️"; ยาย squints at the phone
    ("photo", ["y02"], 0.2, 0.5, 3.4),           # insert: ยาย wipes the old photo; the newspaper clipping beside it
    ("test", ["n05"], 0.3, 1.2, 4.6),    # 08:00 Wednesday: the tower's test tone; only ตาจุ่น stops to listen
    ("rumor", ["t02"], 0.2, 0.6, 4.2),   # the kids watch ตาจุ่น from the shop; he turns and looks back
    ("rule", ["y03", ("j03", 0.15)], 0.2, 0.5, 4.4),    # ยาย taps the driftwood board: rule 1; จูน rolls her eyes
    ("legend", ["n07", ("n08", 0.12), ("n09", 0.15)], 0.3, 0.5, 8.6),  # shadow screen: ละบูน, the seven-layer wave, elders lead children uphill
    ("quake", ["n10"], 0.3, 0.3, 4.2),           # the 3D map: a quake under the sea, rings spreading toward the coast
    ("cup", ["n11"], 0.2, 0.4, 2.6),             # a glass of water on ยาย's table barely trembles
    ("recede", ["n12"], 0.2, 0.4, 3.0),          # the sea draws back; boats tilt onto the mud
    ("fish", ["t04", ("j05", 0.08)], 0.1, 0.3, 4.0),    # ตังค์ runs out with his bucket; จูน's live; comments roll in
    ("walk", ["n13"], 0.2, 0.4, 3.0),            # wide: people walk out onto the seabed, picking up fish, taking photos
    ("know1", ["n14", ("n15", 0.15)], 0.2, 0.4, 5.0),   # cross-section: the trough reaches the shore first, the water draws back
    ("know2", ["n16", ("n17", 0.15)], 0.2, 0.4, 5.4),   # cross-section: the jet coin, the car coin, the runner who can't keep up
    ("know3", ["n18", ("n19", 0.12)], 0.2, 0.5, 4.6),  # back on the beach: time-left bar shrinking; ตาจุ่น lifts the conch
    ("conch", ["c01", ("x01", 0.15)], 0.2, 0.3, 3.8),   # ตาจุ่น blows the conch and shouts; a tourist laughs
    ("run", ["j06", ("t05", 0.08)], 0.1, 0.5, 3.8),     # จูน grabs ตังค์; the duck ring drops; rule card 1 lights up
    ("hill", [], 0, 0, 2.0),                     # the evacuation steps up the hill, the sign, the tower's beacon
    ("wave1", ["x02", ("n20", 0.2)], 0.3, 0.5, 5.4),   # from the hill: the first wave is a fast-rising surge round the shop; people laugh and walk back down
    ("again", ["t06"], 0.3, 0.5, 3.4),           # ตังค์ stares: the sea draws back again, farther than before
    ("yai", ["j07"], 0.2, 0.4, 2.6),             # จูน looks round: ยาย is not on the hill
    ("clue", [], 0, 0, 2.2),                     # below: the shop door open, one of ยาย's slippers on the steps
    ("close", ["n21", ("n22", 0.25)], 0.3, 0.7, 3.8),   # wide: the bay drawn back, a white line on the horizon
    ("choice", [], 0, 0, 3.2),                   # the choice: วิ่งลงไปตามยาย / ตะโกนเรียกจากบนเขา, pulled toward the first → black
    ("end", [], 0, 0, 2.4),                      # the end card: the evacuation sign with a note "ตอนที่ 2 · คลื่นแรกไป"
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
