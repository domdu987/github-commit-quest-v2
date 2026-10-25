"""มือพราย EP.2. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("recap", [], 0.0, 0.0, 2.0),                     # EP.1's last image: โต้ง at the foot of the river steps, the krathong waiting
    ("hook", ["n01", ("n02", 0.15)], 0.3, 0.6, 6.0),  # top-down: โต้ง on the planks, not breathing; ยาย's arms come to lift him — stamped out · EP.2
    ("follow", ["n03"], 0.1, 0.4, 3.0),               # wide: แพรว comes down the steps with her phone torch
    ("lure", ["r01"], 0.3, 0.4, 3.4),                 # under the water looking up: his legs coming down, pale hands waiting
    ("sleep", ["n04"], 0.1, 0.4, 3.6),                # side: โต้ง wading deeper, eyes shut
    ("stop", ["d01"], 0.05, 0.3, 1.8),                # แพรว close, shouting
    ("almost", ["n05"], 0.1, 0.4, 3.6),               # she runs for the edge to dive — and stops
    ("srt", ["n06"], 0.1, 0.5, 4.4),                  # shout, throw the gallon, reach the pole
    ("help", ["d02"], 0.1, 0.3, 2.8),                 # low: shouting up at the house
    ("out", ["n07"], 0.1, 0.5, 4.0),                  # she drags him onto the planks; he doesn't move
    ("yai", ["d03"], 0.1, 0.3, 3.6),                  # ยาย runs in to lift him over her shoulder
    ("no", ["d04"], 0.05, 0.3, 1.6),                  # แพรว catches ยาย's arms
    ("dont", ["n08"], 0.1, 0.6, 5.6),                 # knowledge: no shoulder carry
    ("call", ["n09"], 0.1, 0.5, 4.2),                 # 1669; laid flat on hard, level ground
    ("check", ["n10"], 0.1, 0.5, 3.6),                # top-down: shake the shoulders, call his name
    ("air", ["n11"], 0.1, 0.5, 4.2),                  # top-down: forehead, chin, two breaths
    ("cpr", ["n12"], 0.1, 0.8, 5.4),                  # top-down: 30 compressions, 2 breaths
    ("breathe", ["n13"], 0.1, 0.5, 3.0),              # top-down: water coughed up, lips pink again
    ("recover", ["n14"], 0.1, 0.6, 5.6),              # side: on his side, a blanket, nothing to eat or drink
    ("flood", ["n15"], 0.1, 0.5, 3.2),                # the road under water, the ambulance stuck far off
    ("ferry", ["d05"], 0.1, 0.4, 3.8),                # low: ตาเหม in his ferry at the steps, hand out
    ("mid", ["n16"], 0.1, 0.5, 5.0),                  # wide: the ferry gliding mid-river, the oar held up dry
    ("hands", ["n17"], 0.2, 0.6, 4.2),                # under the hull: a dozen pale hands pushing it along
    ("look", ["d06"], 0.1, 0.5, 2.8),                 # ตาเหม close, the lamp under his face
    ("fall", ["n18"], 0.1, 0.6, 3.2),                 # the boat jolts; แพรว goes over the side
    ("swim", ["r02"], 0.3, 0.4, 3.6),                 # in the water: แพรว's head above the surface, a pale face rising behind
    ("choice", [], 0.0, 0.0, 3.4),                    # swim for it / float on your back
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
