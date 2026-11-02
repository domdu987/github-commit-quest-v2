"""รูพญานาค EP.3 รูยังกว้างได้ ไหว้ไกลร้อยเมตร (ตอนจบ). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.05, 0.0, 1.0),             # hook: the hole at dawn, its lip crumbling outward, the red rope sagging into it
    ("hook", ["n02"], 0.04, 0.4, 1.6),             # command at ~3 s: ยาย's silhouette inside the rice barn doorway, the ring of cracks at the barn post
    ("barn", ["m01", ("y01", 0.1)], 0.12, 0.25, 2.2),  # the kids at the rope shouting; inside, ยาย tugging the jammed door
    ("pry", ["n03", ("s01", 0.1)], 0.12, 0.3, 2.2),    # พ่อใหญ่สิน wedges the old drill rod and levers the door; ยาย tumbles out into his arms
    ("rule", ["y02"], 0.1, 0.15, 2.0),             # rules card for 1.9 s only (palm-leaf line 3 sooting in, the "ส." mark), then cut to everyone running down the bund
    ("far", ["n04"], 0.1, 0.25, 2.2),              # wide from high: the family running away from the barn; distance marks on the bund
    ("count", ["t01", ("m02", 0.1)], 0.08, 0.3, 2.2),  # joke: ต้นข้าว counting giant steps, มุก dragging him on
    ("grow1", ["n05"], 0.12, 0.25, 2.2),           # cutaway / top-down: the old hole's rim breaking away, wider (G3)
    ("grow2", ["n06"], 0.12, 0.25, 2.2),           # a second ring of cracks opening in the field nearby (B1)
    ("myth", ["g01"], 0.08, 0.25, 2.2),            # ผู้ใหญ่ทอง on the megaphone under a blue sky: "dry season, no sinkholes"
    ("know1", ["n07"], 0.12, 0.25, 2.2),           # cutaway: rain soaking the topsoil after the drought, the layer swelling dark (G4 U2)
    ("know2", ["n08"], 0.12, 0.3, 2.2),            # cutaway: the cave roof bending under the weight
    ("rain", ["n09"], 0.15, 0.3, 2.2),             # night: the first rain of the year arrives over the paddies
    ("sink", ["n10"], 0.15, 0.8, 2.2),             # the rice barn settles slowly into a new hole, upright, everyone safe at the rope 100 m away
    ("loss", ["y03", ("t02", 0.2)], 0.15, 0.35, 2.2),  # ยาย's face, rain; ต้นข้าว takes her hand
    ("leaf", ["y04"], 0.15, 0.35, 2.2),            # ยาย hands the palm-leaf bundle to พ่อใหญ่สิน
    ("hand", ["n11", ("s02", 0.15)], 0.12, 0.3, 2.2),  # twist: close on the inscribed leaf and his hand, the same strokes
    ("ess", ["m03"], 0.08, 0.3, 2.2),              # insert: the "ส." at the tip of leaf 3; มุก's finger
    ("num", ["t03"], 0.08, 0.3, 2.2),              # ต้นข้าว holds his scrap of lucky numbers against the last notch on the well post
    ("low", ["n12"], 0.12, 0.3, 2.2),              # the notch column, the lowest cut glinting
    ("warn", ["t04"], 0.08, 0.45, 2.2),            # ต้นข้าว, quiet
    ("week", ["n13"], 0.15, 0.3, 2.2),             # a week later: the red rope ring with signs, wide
    ("shrine", ["n14"], 0.15, 0.3, 2.2),           # the naga shrine rebuilt far back; villagers wai from there; ยาย and มุก wai together
    ("sell", ["g02"], 0.08, 0.3, 2.2),             # joke: ผู้ใหญ่ทอง with a "ขาย" sign on the pump
    ("close", ["n15", ("n16", 0.3)], 0.3, 0.8, 3.6),   # closing: the whole family wai-ing from the rope, the hole far behind at sunset
    ("end", [], 0, 0, 2.4),                        # end card: the headman's sign with the note "ตอนจบ"
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
