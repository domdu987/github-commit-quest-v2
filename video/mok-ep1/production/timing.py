"""Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.4, 0.6, 4.4),                # story opener: title + EP.1 in the night sky, eyes in the clouds, dive onto the mountain road
    ("hook", ["n02"], 0.7, 0.6, 2.4),                # driver's POV in the fog, hand going for the high beams; a villager waving in the fog
    ("chapter", ["n03"], 0.15, 0.5, 2.6),           # green road sign "บ้านหมอก 3 กม." with the episode plate, headlights sweep across
    ("road", ["n04"], 0.1, 0.35, 3.0),              # wide: the mountain road in Loei, one pair of lights climbing
    ("mint", ["d01"], 0.1, 0.3, 2.4),               # the village petrol station, มิ้นท์ impatient by the car
    ("saeng", ["d02"], 0.15, 0.35, 2.4),            # ยายแสง at the pump looks up
    ("rule", ["d03"], 0.1, 0.4, 7.0),               # her rule (card)
    ("gps", ["d04"], 0.1, 0.3, 2.6),                # เจ laughs; insert: the license plate as they pull away
    ("mirror", ["n05"], 0.1, 0.5, 4.0),             # the convex mirror: someone in a blanket behind the car
    ("three", ["n06"], 0.15, 0.35, 2.8),            # 3 a.m., the car in thickening fog
    ("high", ["d05"], 0.1, 0.2, 2.2),               # her hand on the stalk
    ("glare", ["n07"], 0.05, 0.4, 3.0),             # white wall of glare; a face right in front
    ("swerve", [], 0, 0, 1.6),                      # action: the swerve
    ("low", ["n08"], 0.1, 0.4, 4.4),                # low beams, the road lines (steps card)
    ("wave", ["n09"], 0.1, 0.35, 2.8),              # someone waving at the roadside
    ("stop", ["d06", ("d07", 0.05)], 0.1, 0.4, 3.4),# inside: "stop for him" / "don't stop!"
    ("pass", [], 0, 0, 1.6),                        # action: they pass him; his head turns with them
    ("white", ["n10"], 0.1, 0.3, 2.6),              # nothing but white
    ("haz", ["n11"], 0.1, 0.3, 3.0),                # hazard button; pull onto the shoulder
    ("off", ["n12"], 0.1, 0.3, 5.2),                # lights off but hazards, handbrake, foot off the brake (steps card)
    ("why", ["n13"], 0.1, 0.4, 3.8),                # top-down: the car behind follows the brake lights
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("behind", ["n14"], 0.15, 0.35, 3.2),           # through the rear window: headlights come up and stop
    ("nobody", ["n15"], 0.1, 0.5, 2.2),             # outside: the car behind, nobody gets out
    ("plate", ["n16"], 0.1, 0.5, 3.6),              # its plate = their plate
    ("knock", ["g01"], 0.2, 0.4, 3.6),              # the man from the roadside at หวาน's window
    ("choice", [], 0.0, 0.0, 3.4),
    ("next", [], 0.0, 0.0, 2.3),                    # end card: the petrol receipt
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
