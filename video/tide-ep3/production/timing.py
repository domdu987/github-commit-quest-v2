"""ทะเลลด EP.3 หนีไม่ทัน ขึ้นชั้นสูง (ตอนจบ). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01"], 0.15, -0.3, 2.6),            # back to the second wave, ยาย's side: people run past the shop to the pickups on the beach road
    ("cars", ["n02"], 0.3, 0.5, 1.9),              # the jam: bumper to bumper, hazards blinking (the command at ~2.9 s)
    ("jam", ["x01", ("n03", 0.2)], 0.1, 0.5, 5.5),  # a man in a pickup leans on the horn; the narrator: 2547, cars jammed and crashed
    ("yai", ["y01"], 0.2, 0.4, 2.6),               # ยาย turns from the road to the hotel beside her shop
    ("stair", ["y02"], 0.3, 0.6, 3.6),             # she climbs the hotel's outside stair, saying her own rule 3; the board
    ("know", ["n04", ("n05", 0.15), ("n06", 0.15), ("n07", 0.15)], 0.2, 0.6, 12.0),  # the graphic: where to go when the hill is too far
    ("hours", ["n08", ("n09", 0.2)], 0.3, 0.5, 6.0),   # the present, hours later: the hill, the drained village, the stain on the hotel
    ("roof", ["t01", ("j01", 0.3)], 0.6, 0.6, 4.5),    # จูน's phone zooms on the hotel roof: ยาย waving the wet photo
    ("hug", ["t02", ("y03", 0.25)], 0.3, 0.7, 5.0),    # on the wet sand: the kids run to ยาย; the joke
    ("ask", ["j02"], 0.3, 0.5, 3.0),               # ตาจุ่น comes; ยาย looks away; จูน asks
    ("photo", ["c01"], 0.3, 0.4, 3.4),             # insert: the old photo of the two young fishermen (EP.1's wall)
    ("clip", ["c02"], 0.2, 0.5, 3.6),              # insert: the clipping, a fisherman carrying a young woman out of the water
    ("mom", ["j03"], 0.3, 0.7, 3.0),               # close on จูน: it was her mother
    ("why", ["y04", ("c03", 0.3)], 0.3, 0.6, 4.5),     # ยาย and ตาจุ่น
    ("hands", ["n10"], 0.3, 0.8, 3.8),             # she takes his hand, the first time in 22 years
    ("board", ["t03"], 0.3, 0.7, 3.5),             # ยาย's rule board washed up; on its back, carved: จุ่น
    ("moken", ["n11"], 0.3, 0.7, 6.0),             # the shadow screen: the Moken listened to the sea
    ("wed", ["n12"], 0.3, 0.6, 3.6),               # the next Wednesday, 08:00: the tower's test, the whole village stops to listen
    ("duck", ["t04"], 0.3, 0.5, 3.2),              # ตังค์ gives the duck ring to ตาจุ่น
    ("final", ["c04"], 0.3, 1.0, 5.5),             # ตาจุ่น looks at the sea: the last line
    ("end", [], 0, 0, 3.0),                        # the end card: ตอนจบ
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
