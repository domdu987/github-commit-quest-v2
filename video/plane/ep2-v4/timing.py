"""รอดคนเดียว EP.2 v4 (S17 card rhythm). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01"], 0.05, 0.04, 1.0),      # B0 คิว on the rocks by the tail at dusk, the smoke across the bay (same angle as EP.1's last frame)
    ("cmd", ["n02"], 0.03, 0.20, 0.9),       # his foot steps down a rock → red
    ("why", ["n03"], 0.10, 0.15, 3.0),       # B1 up and away from him: a dot on grey rock | from a plane window
    ("wreck", ["n04"], 0.08, 0.15, 3.0),     # the tail reads as a plane from the sky | the wet chart: the route crosses the island (S12)
    ("smoke", ["n05"], 0.06, 0.30, 1.4),     # his face turned back to the smoke → red
    ("night", ["n06"], 0.12, 0.10, 2.4),     # B2 waves, spray | inside the tail, curled up
    ("shelter", ["n07"], 0.08, 0.12, 2.0),   # wind outside, still inside
    ("vest", ["n08"], 0.08, 0.15, 3.0),      # plant 1: he zips the jacket over the orange vest | plant 2: the phone light out of the door
    ("glow", ["n09"], 0.08, 0.25, 1.6),      # 4 a.m.: the smoke is a light now, blinking → red
    ("q1", ["q01"], 0.06, 0.12, 1.6),        # B3 คิว jumps up: the village!
    ("lure", ["n10"], 0.08, 0.12, 3.0),      # his feet leave the wreck | the phone light finds the cliff edge, the black surf
    ("dont", ["n11"], 0.05, 0.25, 1.3),      # the command again at the edge → stones drop down the cliff
    ("q2", ["q02"], 0.08, 0.20, 1.6),        # he backs into the wreck: I'll wait here
    ("morning", ["n12"], 0.12, 0.08, 1.6),   # B4 orange sky, the helicopter's shadow on the water
    ("q3", ["q03"], 0.04, 0.10, 1.6),        # he runs out waving, face big
    ("pass", ["n13"], 0.08, 0.15, 2.4),      # from the helicopter: the grey wreck melts into the rocks
    ("under", ["n14"], 0.08, 0.30, 1.6),     # close: the orange edge under his zip → red
    ("rule", ["n15"], 0.10, 0.20, 4.0),      # B5 the safety card on the antenna (≥ half the screen) | vest on the wing | panel | blanket
    ("back", ["n16"], 0.08, 0.25, 1.6),      # the helicopter turns back, a flash → red
    ("found", ["r01"], 0.06, 0.12, 2.0),     # B6 the cockpit: found him
    ("saved", ["n17"], 0.08, 0.15, 1.6),     # คิว crying-smiling, rotor wind
    ("empty", ["r02"], 0.08, 0.20, 2.0),     # the front section across the bay: a dead fire, nobody → red
    ("hush", [], 0.0, 0.0, 0.5),             # twist: silence, bass out, darker
    ("twist", ["n18"], 0.12, 0.15, 4.0),     # B7 the smoke from the first shot | the signal fire by the front section | the phone light seen from there
    ("walk", ["n19"], 0.08, 0.15, 1.8),      # torches in a line down the cliff in the dark
    ("lost", ["n20"], 0.10, 0.60, 1.8),      # the empty front section, ash in the wind → red
    ("end", [], 0.05, 0.10, 2.8),            # the safety card, both rules ticked
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
