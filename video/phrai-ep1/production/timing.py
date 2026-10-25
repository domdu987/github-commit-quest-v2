"""มือพราย EP.1. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.4, 0.5, 4.4),                 # story opener: title in the night sky, the dive onto the river of krathongs
    ("hook", ["n02"], 0.5, 0.7, 2.6),                 # POV down from the pier: a child's arm reaching for the coins, a pale hand rising
    ("back", ["n03"], 0.2, 0.5, 2.2),                 # chapter card: a krathong, flag "3 ชั่วโมงก่อน", its candle growing back
    ("dusk", ["n04"], 0.1, 0.4, 3.2),                 # wide at dusk: high water, the house on stilts, the temple across
    ("arrive", ["d01"], 0.1, 0.3, 3.0),               # side: แพรว and โต้ง run along the porch, ยาย at the door
    ("coins", ["d02"], 0.05, 0.3, 3.0),               # low angle on โต้ง with his coin jar
    ("warn", ["d03"], 0.1, 0.4, 4.6),                 # ยาย close, the lantern on her face
    ("rule", ["d04"], 0.2, 0.6, 12.2),                # ยาย's three rules (card), the river darkening behind
    ("legend", ["n05", ("n06", 0.3)], 0.3, 0.6, 7.6), # shadow puppets: the drowned become พราย; พราย need a replacement
    ("traits", ["t01", ("t02", 0.15), ("t03", 0.15)], 0.1, 0.6, 9.0),  # the พราย close in shadow puppet: black, green eyes; the lure, the call; pulled under
    ("brag", ["d05"], 0.1, 0.3, 3.2),                 # แพรว, goggles round her neck
    ("cant", ["n07"], 0.1, 0.5, 2.4),                 # over โต้ง's shoulder: he looks down at the black water
    ("crowd", ["n08"], 0.1, 0.3, 2.8),                # 8 p.m.: the pier full of people, krathongs going out
    ("mhem", ["n09"], 0.1, 0.4, 4.0),                 # ตาเหม in his ferry, the lamp on the bow
    ("kids", ["n10"], 0.1, 0.3, 2.8),                 # kids at the edge fishing coins out of the krathongs with sticks
    ("know", ["n11"], 0.1, 0.6, 4.6),                 # knowledge: don't pick up floating things, don't bend over the water
    ("under", ["n12"], 0.2, 0.7, 4.4),                # the camera sinks through the surface: the drowned under the krathongs
    ("gone", ["n13"], 0.1, 0.4, 2.6),                 # 9 p.m.: แพรว turning round in the crowd
    ("whisper", ["r01"], 0.3, 0.4, 3.9),              # the far end of the pier: โต้ง alone, a krathong drifting to him
    ("five", ["d06"], 0.1, 0.3, 3.0),                 # โต้ง's POV: a five-baht coin shining in the krathong
    ("bend", ["n14"], 0.1, 0.9, 2.2),                 # side on: he bends — a pale hand takes his wrist — splash
    ("scream", ["d07"], 0.1, 0.5, 1.2),               # แพรว turns, runs
    ("stop", ["d08"], 0.1, 0.5, 1.8),                 # แพรว about to dive; ยาย grabs her arm
    ("hug", ["n15"], 0.2, 0.5, 3.4),                  # under the water: a drowning child clutching whoever comes in
    ("how", ["n16"], 0.1, 0.6, 5.4),                  # knowledge: shout, throw, reach
    ("shout", ["d09"], 0.1, 0.4, 3.2),                # low angle: แพรว shouting, heads turn
    ("throw", ["n17"], 0.1, 0.5, 6.0),                # the gallon, a little water in it, thrown straight to โต้ง
    ("reach", ["n18"], 0.1, 0.6, 5.0),                # ตาเหม's bamboo pole; แพรว crouched low, pulling
    ("leg", ["d10"], 0.2, 0.6, 3.4),                  # โต้ง soaked on the planks, coughing
    ("sig", ["s01"], 0.15, 0.5, 4.6),                 # channel signature
    ("marks", ["n19"], 0.1, 0.5, 3.4),                # ankle close-up: five finger marks
    ("shadow", ["n20"], 0.1, 0.6, 4.4),               # the water: everyone's reflection — except ตาเหม's
    ("night", ["n21"], 0.2, 0.4, 3.8),                # 2 a.m. inside: wet footprints up from the river steps to the net
    ("call", ["r02"], 0.3, 0.5, 4.4),                 # โต้ง walking down the steps to the water, a krathong waiting
    ("choice", [], 0.0, 0.0, 3.4),                    # wake ยาย / follow him yourself
    ("next", [], 0.0, 0.0, 2.6),                      # end card: the pier sign
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
