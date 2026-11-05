"""บางระจัน แบต 3% EP.3 (lane A, storytelling). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("d01", ["h3"], 0.05, 0.3, 3.6),                  # hook: 1% · the lime ring around the yard · "ชาร์จด้วยอะไร"
    ("d02", ["p08_1"], 0.05, 0.3, 3.2),               # the clip you once saw: a lemon battery
    ("d03", ["p08_2"], 0.05, 0.4, 2.2),               # rule three, broken
    ("d04", ["p08_3"], 0.05, 0.3, 5.6),               # 200 limes, nails, earphone wire, the ring
    ("d05", ["p08_4"], 0.05, 0.4, 2.6),               # the screen flickers… 2%
    ("d06", ["p08_5"], 0.05, 0.3, 2.8),               # the long drums, a temple fair
    ("d07", ["p08_6"], 0.05, 0.3, 2.8),               # except ยายแผ้ว by the empty mortar
    ("d08", ["p08_7"], 0.05, 0.4, 4.4),               # "200 limes for 1%… ไอ้หลานเอ๊ย"
    ("d09", ["p09_1"], 0.08, 0.3, 4.0),               # that night: the patrol reaches the fence
    ("d10", ["p09_2"], 0.05, 0.3, 4.2),               # torches in the fog; the villagers wait in silence
    ("d11", ["p09_3"], 0.05, 0.3, 4.4),               # rule two… อย่าให้ควายเห็น
    ("d12", ["p09_4"], 0.05, 0.3, 2.6),               # torch on, out into the fog
    ("d13", ["p09_5"], 0.05, 0.3, 3.4),               # ไอ้ดำ sees the light and charges
    ("d14", ["p09_6"], 0.05, 0.3, 6.6),               # the enemy's view: a light, then a giant buffalo
    ("d15", ["p09_7"], 0.05, 0.4, 2.0),               # the torches fall back
    ("d16", ["p10_1"], 0.05, 0.5, 3.4),               # the screen dies: 0%
    ("d17", ["p10_2"], 0.05, 0.4, 3.2),               # ไอ้ดำ stops; silence
    ("d18", ["p10_3"], 0.05, 0.3, 3.2),               # the torches creep back
    ("d19", ["p10_4"], 0.05, 0.3, 4.4),               # a long hoarse laugh from the fog
    ("d20", ["p10_5"], 0.05, 0.3, 5.8),               # ยายแผ้ว, torch under the chin, betel-black grin
    ("d21", ["p10_6"], 0.05, 0.3, 2.6),               # the enemy runs
    ("d22", ["p10_7"], 0.05, 0.6, 4.2),               # the scariest sound that night…
    ("d23", [], 0, 0, 2.8),                           # next: the full story on YouTube
    ("d24", [], 0, 0, 2.2),                           # the channel logo
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
