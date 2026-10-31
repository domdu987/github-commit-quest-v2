"""รั้วสุดท้าย EP.1. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("hook", ["n01"], 0.15, -0.3, 2.6),          # the bulging can on the desk under ปั้น's opener, the title in chalk behind
    ("dont", ["n02"], 0.2, 0.2, 1.8),            # insert: the lid swells; ครูพิม's hand pulls the opener away
    ("tox", ["n03"], 0.15, 0.25, 3.4),           # from the classroom window down to the gate at dusk: the padlock hangs OPEN (planted, ~0:05)
    ("die", ["n04"], 0.1, 0.3, 2.2),             # card: a taste on a spoon → the skull
    ("day", ["n05"], 0.15, 0.2, 2.4),            # day 100: the school from the road, the horde in the paddies
    ("five", ["n06"], 0.1, 0.3, 3.4),            # the yard: the five, name tags
    ("rule", ["k01"], 0.1, 0.4, 2.8),            # ครูพิม at the gate + the camp's rule slate (rule 1)
    ("rice", ["n07"], 0.1, 0.3, 4.0),            # เจ๊หงส์'s ledger: rice 3 days → ก้อง slips out of the gate
    ("map", ["n08"], 0.1, 0.3, 3.2),             # map school → market, then the market: one crate of cans
    ("run", [], 0, 0, 2.6),                      # dusk road: ก้อง running with the crate, the horde behind
    ("gate", ["n09"], 0.1, 0.3, 2.8),            # the gate: he slips in, ครูพิม slams it, the horde hits the bars
    ("free", ["k02"], 0.1, 0.3, 2.4),            # the classroom: ก้อง shows the crate
    ("bulge", ["n10"], 0.1, 0.3, 2.2),           # insert: one can's lid is domed (we see it first)
    ("signs", ["n11"], 0.15, 0.3, 4.2),          # card: bulging · leaking · foam → throw it out
    ("taste", ["n12"], 0.1, 0.3, 2.2),           # ปั้น's drawing: the can with a skull — she knew
    ("sympt", ["n13"], 0.15, 0.4, 5.6),          # card: blurred vision · drooping eyelids · hard to swallow → hospital now
    ("rw", ["n14"], 0.2, 0.5, 4.0),              # rewind to 0:05: the window shot
    ("lock", ["n15"], 0.1, 0.4, 2.4),            # insert: the open padlock swinging on the chain
    ("radio", ["n16", "r01"], 0.2, 0.5, 3.6),    # night: the radio wakes by itself, "หก"
    ("count", ["n17"], 0.1, 0.3, 2.6),           # the classroom at night: five asleep, five chalk marks
    ("draw", ["k03"], 0.1, 0.6, 2.8),            # ปั้น's drawing of six people (one on the water tower) → bare prints in the mud by the gate
    ("next", [], 0, 0, 4.2),                     # next-episode card on the ledger + channel
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
