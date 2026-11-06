"""เรือล่มคืนลอยกระทง: shot timing from the recorded voice, per segment, so picture and sound share one schedule.
usage: python3 tools/timing.py ep1|ep2|ep3|bridges   → <segment>/schedule.json
Each shot: (key, [voice ids | (id, gap) | (id, offset, "start")], pre-roll, post-roll, minimum length). Shots follow the beat tables of
ARC.md (v2). Shots marked shorts-only in lines.json ("only") are still timed here; the cut scripts drop them for the long video.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

SEG = sys.argv[1] if len(sys.argv) > 1 else "ep1"
HERE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), SEG)
DUR = json.load(open(os.path.join(HERE, "vo", "durations.json")))
LINES = {ln["id"]: ln for ln in json.load(open(os.path.join(HERE, "lines.json")))}

SHOTS_ALL = {
    "ep1": [
        ("open", ["n01"], 0.05, 0.0, 1.0),            # low at the waterline: the overloaded boat sliding at the bright pontoon, red stripe under water, knees rising
        ("hook", ["n02"], 0.04, 0.3, 1.6),            # command: push in on the rising knees
        ("card", ["n03"], 0.15, 0.4, 2.0),            # ยาย's thumb rolls the brass counter 0019 → 0000, "แกร๊ก"
        ("est", ["y01"], 0.3, 0.5, 3.4),              # establishing ท่ายายหยิบ: temple across the river, krathong stall, the boat moored
        ("kids", ["k01", "m01", "m06", "y15", "l01"], 0.12, 0.3, 3.0),
        ("whistle", ["k02", "m02"], 0.1, 0.3, 2.4),   # the clue: the orange whistle on ข้าวปั้น's jacket
        ("code", ["y02", "y03", "k03"], 0.12, 0.3, 3.0),
        ("vest", ["y04", "m03", "y05"], 0.12, 0.3, 3.0),
        ("rap", ["y06", "k04", "y07"], 0.12, 0.3, 3.0),  # the rule paddle, rule 1 in red
        ("swim", ["k05", "y08"], 0.1, 0.4, 2.4),
        ("line", ["y09"], 0.12, 0.3, 2.4),            # the red stripe on the hull
        ("coin", ["y10", "n04", "n05"], 0.12, 0.3, 3.0),  # coins in a krathong · the chalkboard section
        ("board", ["y11", "y12", "x01"], 0.12, 0.3, 3.0),
        ("load", ["l02", "l03"], 0.12, 0.3, 2.6),     # ลุง counts on: the stripe sinks a step at each click
        ("maan", ["l04", "h01", "k06", "y14"], 0.12, 0.3, 3.0),  # น้าหมาน on the land-side stairs, three gallons
        ("sign", ["n06", "n07"], 0.15, 0.3, 3.0),     # the "12 คน" sign · the counter 0019 · the map on the chalkboard
        ("fire", ["x03", "m04", "l05"], 0.1, 0.3, 2.6),
        ("sit", ["k07", "l06", "n08", "n09"], 0.1, 0.3, 3.0),
        ("float", ["m05"], 0.15, 0.4, 2.0),
        ("back", ["n10", "y13"], 0.15, 0.3, 3.0),
        ("hit", ["x04", "n11"], 0.1, 1.3, 3.0),       # the wake, the spray, the bump · three whistles (SFX) after n11 · everyone stands
        ("grab", ["m07", "y16"], 0.1, 0.2, 2.0),      # HG1 choice: ข้าวปั้น up on the bench, มะปราง half-rises, ยาย pins her wrist
        ("roll", [], 0.0, 0.0, 2.2),                  # 0.4 s silence, the crack, the boat rolls, the counter drops
        ("evid", ["n12", "k08"], 0.15, 0.5, 3.0),     # the counter 0019 by the tilting "12 คน" sign · ข้าวปั้น's face
        ("choice", ["n13"], 0.1, 1.6, 3.0),           # Shorts only
        ("endb", ["n14"], 0.2, 0.6, 3.0),             # Shorts only
    ],
    "ep2": [
        ("open", ["n01"], 0.05, 0.0, 1.0),
        ("hook", ["n02"], 0.04, 0.3, 1.6),
        ("recap", ["n03"], 0.12, 0.3, 3.0),           # Shorts only
        ("climb", ["x01", "n04"], 0.1, 0.3, 3.0),
        ("rule", ["y01", "r01", "n05", "m01", "k01"], 0.12, 0.3, 3.0),
        ("fail", ["n06"], 0.1, 1.2, 3.0),             # they slide back, the boat rolls, the roof comes down · 0.4 s silence
        ("under", ["n07"], 0.3, 0.6, 3.4),            # under the hull, the propeller
        ("surf", ["l01", "n08", "m02"], 0.12, 0.4, 3.0),
        ("jug", ["m03"], 0.6, 0.6, 2.4),              # twist 1: the gallon lands beside her ("ตุ้บ" in the pre-roll) and floats
        ("stairs", ["x02", "h01", "n09", "n10", "h02"], 0.12, 0.4, 3.0),  # twist 2: น้าหมาน on the stairs, throwing
        ("vest", ["m04", "m05", "n11"], 0.3, 0.8, 3.0),  # the hang: the empty life jacket
        ("choice", ["n12"], 0.1, 2.0, 3.2),           # Shorts only
        ("endb", ["n13"], 0.2, 0.6, 3.0),             # Shorts only
    ],
    "bridges": [
        ("A1", ["a01"], 0.4, 3.0, 4.0),               # ยาย's angle: the hull rising, the counter bouncing
        ("A2", [], 0.0, 0.0, 4.0),                    # through the water surface into the tilting boat (no line)
        ("B1", ["b01"], 0.3, 0.4, 3.0),
        ("B2", ["b02", "b03"], 0.12, 0.3, 3.0),
        ("B3", ["b04", "b05"], 0.12, 0.3, 3.0),
        ("B4", ["b06", ("b07", 0.35)], 0.15, 0.5, 3.0),
    ],
    "ep3": [
        ("open", ["n01"], 0.05, 0.0, 1.0),
        ("hook", ["n02"], 0.04, 0.3, 1.6),
        ("party", ["l01", "n03"], 0.12, 0.4, 3.0),    # she lets go to swim for the party boat · the wake throws her back · she grabs the second gallon
        ("rule", ["y01"], 0.15, 0.6, 2.4),            # rule 3 on the paddle
        ("floatb", ["n04", "n05", "m01"], 0.15, 0.4, 3.4),
        ("rescue", ["x01", "m02", "x02"], 0.12, 0.3, 3.0),
        ("kp", ["n06"], 0.3, 1.2, 3.6),               # ข้าวปั้น by the giant krathong, the whistle in both hands, he won't blow
        ("blow", ["m03"], 0.12, 1.6, 3.0),            # three whistles (SFX) after m03
        ("found", ["x03"], 0.1, 0.5, 2.0),
        ("count", ["y02", "y03"], 0.15, 0.4, 3.4),
        ("maan", ["m04", "h01"], 0.15, 0.5, 3.0),
        ("accuse", ["x04", "l02"], 0.12, 0.6, 3.0),
        ("reveal", ["n07", "k01"], 0.5, 0.5, 3.4),    # 0.5 s silence before, the camera slides down to the orange whistle
        ("hug", ["y04", "l03"], 0.15, 0.5, 3.4),
        ("close", ["k02", "y05"], 0.15, 0.8, 3.4),
        ("end", [], 0.0, 0.0, 3.0),                   # the paddle, three white strikes, "ตอนจบ" · 1669 · 1199 · 191
    ],
}
SHOTS = SHOTS_ALL[SEG]
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


def main(cut, fname):
    t = 0.0
    out = []
    drop = {"shorts": "full", "full": "shorts"}[cut]
    for key, ids, pre, post, mn in SHOTS:
        cur = pre
        vo = []
        kept = [it for it in ids if LINES[it if isinstance(it, str) else it[0]].get("only") != drop]
        if ids and not kept:
            continue  # every line of this shot belongs to the other cut
        ids = kept
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
    json.dump({"cut": cut, "total": round(t, 3), "shots": out}, open(os.path.join(HERE, fname), "w"), ensure_ascii=False, indent=1)
    for s in out:
        print(f"{s['key']:9s} {s['start']:7.2f} {s['dur']:5.2f}  " + " ".join(f"{v['id']}@{v['t']:.2f}{v['frags'][1:] or ''}" for v in s["vo"]))
    print("TOTAL", cut, round(t, 2))


if __name__ == "__main__":
    if SEG == "bridges":
        main("full", "schedule.json")
    else:
        main("shorts", "schedule.json")       # 9:16 Short
        main("full", "schedule-full.json")    # this episode's part of the 16:9 long video
