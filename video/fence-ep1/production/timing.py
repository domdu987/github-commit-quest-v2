"""Derive shot timing from the recorded voice so picture and sound share one schedule (วันที่ 100 EP.1 กระป๋องบวม).

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
    ("hook", ["n01", ("n02", 0.05), ("n03", 0.1)], 0.3, 0.35, 6.0),     # POV: the bulging can in our hands at dusk, a small hand reaching for it
    ("chapter", ["n04"], 0.15, 0.4, 2.6),                                # the blackboard: "วันที่ 100" in chalk
    ("yard", ["n05"], 0.1, 0.22, 4.0),                                    # the school yard, five of them, the head count
    ("rules", ["d01"], 0.15, 0.3, 5.0),                                 # ครูพิม at the board, the three rules
    ("noon", ["n07"], 0.1, 0.22, 3.4),                                    # the road at noon: a slow one in the shimmer
    ("dusk", ["n08"], 0.1, 0.22, 2.4),                                    # same road, sun down: it runs
    ("ledger", ["n09", ("d02", 0.15)], 0.1, 0.25, 4.0),                  # เจ๊หงส์'s ledger, the rice sack, 3 days
    ("gate", ["n10", ("d03", 0.1)], 0.1, 0.22, 5.6),       # ก้อง leaves by the gate, the sun HUD
    ("market", ["n11", ("n12", 0.1)], 0.1, 0.22, 4.4),                    # the market: the last cans; the vendor standing in the gap (seen first by us)
    ("clatter", ["n13"], 0.25, 0.3, 2.6),                                # a can drops, the sound ring on the map, it turns
    ("lunge", [], 0, 0, 1.5),                                            # action: it comes over the stall
    ("shelf", [], 0, 0, 1.4),                                            # action: ก้อง backs into the shelf, cans everywhere
    ("run", [], 0, 0, 1.6),                                              # action: POV out of the market into the open, the sun on the horizon
    ("road", ["n14", ("n15", 0.05), ("d05", 0.05)], 0.1, 0.2, 4.0),                     # the dusk road: ก้อง running, not alone
        ("bolt", [], 0, 0, 1.3),                                             # action: ครูพิม pulls the bolt (breaking her own rule)
    ("snag", [], 0, 0, 1.8),                                             # action: the backpack strap through the bars, a hand grabs it
    ("cut", [], 0, 0, 1.4),                                              # action: ลุงหมาน's sickle cuts the strap, the bag goes outside
    ("slam", ["d06"], 0.05, 0.4, 2.2),                                   # "ปิด! ปิดเลย!" the gate slams, arms through the bars
    ("cans", ["n16", ("n17", 0.1)], 0.15, 0.22, 4.4),                     # the desk: four cans, one swollen; the count 12 → 4
    ("reach", ["d07", ("n18", 0.1)], 0.1, 0.25, 3.2),                    # น้องปั้น's hand (we see it first)
    ("stop", ["d08"], 0.05, 0.35, 1.6),                                  # "อย่า!"
    ("signs", ["n19"], 0.1, 0.22, 4.4),                                   # knowledge: the signs on the can
    ("toxin", ["n20", ("n21", 0.1)], 0.1, 0.22, 4.6),                     # the toxin: can't see, smell, taste; one bite
    ("real", ["n23"], 0.1, 0.35, 3.4),                                   # in real life: throw the whole can away
    ("three", ["n29"], 0.1, 0.4, 3.6),                                   # three cans left, and they know where we are (the fence at night)
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("radio", ["n24", ("r01", 0.25), ("n25", 0.3)], 0.15, 0.4, 7.0),     # the radio wakes: "หก"
    ("drawing", ["n26"], 0.15, 0.6, 3.2),                                # น้องปั้น's drawing: count them
    ("tank", ["n27", ("n28", 0.1)], 0.1, 0.4, 4.6),                      # morning: the gauge one notch down
    ("choice", [], 0.0, 0.0, 3.4),
    ("next", [], 0.0, 0.0, 2.4),                                         # end card: the ledger page
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
