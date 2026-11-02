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
    ("hook", ["n01"], 0.03, 0.02, 1.0),      # B0 คิว points at the smoke behind the far karst (EP.1's last frame)
    ("cmd", ["n02"], 0.03, 0.2, 0.9),       # his face → red
    ("why", ["n03"], 0.06, 0.075, 3.0),       # B1 up and away: a dot on grey rock (aerial)
    ("wreck", ["n04"], 0.048, 0.075, 2.4),     # the tail from the sky, ring | the wet chart
    ("bottle", ["n05"], 0.048, 0.06, 1.8),    # half a bottle of water in his hand (the clock)
    ("sun", ["n06"], 0.06, 0.3, 1.4),       # sun on the rocks, heat shimmer → red
    ("empty1", ["n07"], 0.06, 0.05, 1.6),    # B2 the last drop, the empty bottle
    ("thirst", ["n08"], 0.036, 0.05, 1.8),    # cracked lips | he kneels at the water's edge, cupping seawater
    ("nosea", ["n09"], 0.04, 0.2, 1.0),     # his hands stop at his mouth → red
    ("salt", ["n10"], 0.048, 0.06, 2.4),      # the water runs out of his fingers; salt crust on the rock
    ("look", ["n11"], 0.036, 0.05, 1.6),      # he looks up: green coconuts
    ("coco", ["n12"], 0.048, 0.06, 3.0),      # he knocks one down, opens it on a metal edge, drinks | a brown one beside
    ("onetree", ["n13"], 0.06, 0.3, 1.6),   # wide: the only palm on the island → red
    ("rain", ["n14"], 0.072, 0.05, 3.0),      # B3 night rain: the plastic sheet from the wreck catching water
    ("vest", ["n15"], 0.048, 0.075, 3.0),      # plant: orange vest under the jacket | the phone light out of the tail
    ("glow", ["n16"], 0.08, 0.2, 1.6),      # 4 a.m.: the fire across the bay | his face lit orange → red
    ("q1", ["q01"], 0.036, 0.06, 1.6),        # คิว jumps up: the village!
    ("lure", ["n17"], 0.048, 0.06, 2.4),      # the cliff side-on, he walks toward the light
    ("dont", ["n18"], 0.05, 0.25, 1.3),      # he brakes at the edge, stones fall
    ("q2", ["q02"], 0.048, 0.1, 1.6),        # back in the tail: I'll wait here
    ("tide", ["n19"], 0.072, 0.05, 3.4),      # B4 low tide: limpets on the rocks | a bush with bright red fruit, his hand reaching
    ("nofruit", ["n20"], 0.04, 0.2, 1.2),   # his hand stops → red
    ("shell", ["n21"], 0.048, 0.05, 1.8),     # he prises limpets off a rock the sea covers at high tide
    ("cook", ["n22"], 0.036, 0.05, 1.4),      # shells on the embers
    ("fire", ["n23"], 0.036, 0.05, 2.0),      # the lighter from a passenger's bag, the fire catches
    ("rotor", ["n24"], 0.04, 0.3, 1.4),     # he looks up → red
    ("q3", ["q03"], 0.024, 0.05, 1.6),        # B5 he runs out waving, the helicopter high
    ("pass", ["n25"], 0.048, 0.075, 4.0),      # it flies past | his face | grey wreck, thin smoke
    ("under", ["n26"], 0.08, 0.3, 1.6),     # close: the orange edge under his zip → red
    ("bright", ["n27"], 0.06, 0.05, 1.4),    # B6 the safety card | the vest spread on the wreck
    ("flash", ["n28"], 0.036, 0.05, 1.4),     # the metal panel tilted, a flash
    ("leaves", ["n29"], 0.036, 0.075, 2.6),    # green leaves on the fire, white smoke against black rock
    ("back", ["n30"], 0.08, 0.12, 1.6),      # the helicopter turns back → red
    ("found", ["r01"], 0.03, 0.03, 2.0),     # the rescuer: found him
    ("saved", ["n31"], 0.03, 0.03, 2.4),     # คิว crying-smiling, rotor wind
    ("empty", ["r02"], 0.06, 0.1, 2.0),     # the front section: nobody → red
    ("hush", [], 0.0, 0.0, 0.5),             # twist: silence, darker
    ("twist", ["n32"], 0.04, 0.04, 4.0),     # B7 the smoke | the signal fire by the front section | the phone light seen from there
    ("walk", ["n33"], 0.03, 0.03, 1.8),      # torches leaving into the jungle at night
    ("lost", ["n34"], 0.08, 0.1, 1.8),      # footprints into the dark jungle, the rescuer kneeling → red
    ("end", [], 0.05, 0.05, 3.0),            # the safety card: three rules ticked
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
