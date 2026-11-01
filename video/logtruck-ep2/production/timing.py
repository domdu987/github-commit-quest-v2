"""ท่อนซุงลงเขา EP.2 ต่อรุม อย่าลงน้ำ. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01"], 0.15, 0.1, 2.8),        # 0–0.8 the stack pours off the back, logs tumble at the lens; เจ๋ง stamps on the brake
    ("cmd", ["n02"], 0.05, 0.45, 1.9),        # profile: logs across the road between the truck and our car; title board EP.2
    ("stop", ["h01"], 0.05, 0.3, 1.8),        # the two-shot: หนิง screams, both thrown forward
    ("short", ["n03"], 0.1, 0.3, 3.4),        # POV stopped: one log rolls at us and stops a metre short; the gap coin
    ("rail", ["n04"], 0.1, 0.35, 4.4),        # the logs fetch up on the rail; the mirror: the grille rushes in and stops, air brakes
    ("help", ["j01"], 0.05, 0.2, 2.2),        # เจ๋ง reaches for the door
    ("no", ["h02"], 0.05, 0.3, 2.0),          # หนิง grabs his arm
    ("k4", ["n05"], 0.1, 0.3, 4.6),           # profile: stopped on the shoulder, the log across the lane, traffic still coming; coin don't lift
    ("call", ["n06"], 0.1, 0.4, 6.0),         # the two-shot: หนิง on the phone; coins 1586 / 1193 / 1669
    ("foot", ["n07"], 0.1, 0.4, 3.2),         # the gas station at the foot of the hill, late sun
    ("selfie", ["h03"], 0.1, 0.3, 2.6),       # หนิง raises her phone for a selfie, เจ๋ง stretching
    ("what", ["j02"], 0.6, 0.3, 2.8),         # the hiss first; headlights sweep over them
    ("reveal", ["n08"], 0.1, 0.4, 4.6),       # the tanker rolls in beside the pumps — the first full look
    ("orange", ["n09"], 0.1, 0.35, 3.0),      # close: the orange plate, the red diamond; coin
    ("k6", ["n10"], 0.1, 0.4, 5.6),           # หนิง lowers the phone; smoke from the tanker's wheels drifts toward the pumps; coins
    ("ask", ["n11"], 0.1, 1.2, 4.4),          # the smoke at the pump, the hiss → black
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
