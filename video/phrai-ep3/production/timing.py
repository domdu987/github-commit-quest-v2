"""มือพราย EP.3. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("recap", [], 0.0, 0.0, 2.0),                     # EP.2's last image: แพรว's head above the river, the pale face rising behind her
    ("hook", ["n01", ("n02", 0.15)], 0.3, 0.6, 6.0),  # top-down: thrashing far out, the bank a line of lights — stamped out · EP.3
    ("swim", ["n03"], 0.1, 0.4, 4.2),                 # top-down close, tracking: freestyle flat out toward the lights
    ("tired", ["n04"], 0.1, 0.4, 5.0),                # water level: her head dipping, water in her mouth
    ("call", ["r01"], 0.3, 0.4, 4.6),                 # under the river looking up: her legs kicking; the drowned woman rising
    ("grab", ["n05"], 0.1, 0.5, 3.6),                 # under: the pale hand closes on her ankle and pulls
    ("sink", ["n06"], 0.1, 0.3, 2.4),                 # water level: her face going under
    ("memory", ["d01"], 0.2, 0.5, 5.2),               # flash back to EP.1: ยาย on the porch, the rule card, line 3 lit
    ("mouth", ["n07"], 0.1, 0.5, 5.6),                # water level: she stops fighting, mouth up, breathing
    ("float", ["n08"], 0.1, 0.5, 5.6),                # top-down: on her back, arms out, hands sculling
    ("then", ["n09"], 0.1, 0.8, 7.0),                 # top-down wide: the ladder far off, a gallon; RLSS source
    ("moon", ["n10"], 0.1, 0.5, 5.6),                 # POV: the full moon, the river lapping over the lens
    ("loose", ["n11"], 0.1, 0.5, 3.2),                # under: the hand lets go and sinks into the dark
    ("gallon", ["n12"], 0.1, 0.5, 4.4),               # top-down: the gallon drifts in; she holds on
    ("help", ["d02"], 0.1, 0.4, 3.2),                 # water level: on the gallon, shouting
    ("oar", ["n13"], 0.1, 0.4, 2.9),                  # the ferry's lamp out of the dark, the oar held out
    ("hold", ["d03"], 0.1, 0.4, 3.2),                 # ตาเหม close, the lamp under his face
    ("land", ["n14"], 0.1, 0.5, 3.8),                 # the hospital landing; she climbs out; the ferry at the steps
    ("dawn", ["n15"], 0.1, 0.5, 4.2),                 # the ward at sunrise: ยาย comes in, โต้ง asleep
    ("tell", ["d04"], 0.1, 0.3, 2.8),                 # แพรว close
    ("dead", ["d05"], 0.1, 0.6, 4.8),                 # ยาย close: the truth
    ("legend", ["n16"], 0.1, 0.6, 6.8),               # shadow puppets: the young ferryman dives in bare-handed
    ("every", ["n17"], 0.1, 0.5, 5.2),                # sunrise on the river: ตาเหม in his ferry, no reflection, fading
    ("know", ["n18"], 0.1, 0.8, 6.2),                 # the pier at dawn: shout, throw, reach + source
    ("wake", ["n19"], 0.1, 0.3, 3.4),                 # the ward: โต้ง's eyes open
    ("whisper", ["d06"], 0.1, 0.6, 8.0),              # โต้ง close, whispering to his sister
    ("marks", ["n20"], 0.1, 0.6, 3.6),                # แพรว's ankle: five finger marks
    ("last", ["r02"], 0.3, 0.7, 5.8),                 # the river at sunrise: a krathong, a pale hand under it; cut to black
    ("end", [], 0.0, 0.0, 2.8),                       # end card: the pier sign, ตอนจบ
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
