"""รูพญานาค EP.2 น้ำบ่อขุ่นแดง แจ้งแล้วถอย. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.1, 0.0, 1.0),             # hook: ยาย's well at night, the bucket comes up brown mud; cracks ring the house post
    ("hook", ["n02"], 0.06, 0.4, 1.6),             # command at ~3 s: the ring of cracks creeps under the house stilts, a post tilts
    ("out", ["m01", ("y01", 0.1)], 0.15, 0.2, 2.2),  # night, the kids pull ยาย down the house steps; she strains back toward the rice barn
    ("rice", ["t01"], 0.08, 0.2, 1.8),             # ต้นข้าว grabs ยาย's other hand (joke beat)
    ("rule", ["y02"], 0.1, 0.15, 2.0),             # rules card for 1.9 s only (palm-leaf line 2 sooting in), then cut to the kids running to the headman with the muddy bucket while ยาย finishes the line
    ("tell", ["n04"], 0.1, 0.25, 2.2),             # straight on: the kids running to the headman's house with the muddy bucket
    ("nope", ["g01"], 0.08, 0.25, 2.2),            # ผู้ใหญ่ทอง on the loudspeaker tower / megaphone, waving incense (plan fails)
    ("call", ["m02", ("n05", 0.15)], 0.1, 0.3, 2.2),  # มุก dials 1784 on her one-bar phone; coin icon "call"
    ("water", ["g02"], 0.08, 0.2, 2.2),            # villagers line up at the rim with bowls of holy water
    ("stop", ["t02"], 0.06, 0.25, 2.2),            # ต้นข้าว jumps in front, arms out
    ("why", ["n06"], 0.15, 0.3, 2.2),              # cutaway: water poured in washes soil into the cave, the rim widens (U3 G2)
    ("wai", ["t03", ("m03", 0.1)], 0.1, 0.3, 2.2),  # joke: ต้นข้าว catches มุก doing a quick wai
    ("pump", [], 0, 0, 1.0),                       # night: the far pump thumps again (sound only); heads turn
    ("found", ["t04"], 0.08, 0.25, 2.2),           # they follow the sound: the big pump by ผู้ใหญ่ทอง's dry-season field
    ("hose", [], 0, 0, 1.2),                       # the blue hose gushing onto the dry-season paddies all night (picture only)
    ("know1", ["n09"], 0.15, 0.3, 2.2),            # cutaway: pump draws down the water table (G1 p20)
    ("know2", ["n10"], 0.12, 0.3, 2.2),           # cutaway: the cave roof loses its support and drops (G1)
    ("mural", ["n11"], 0.15, 0.3, 2.2),            # the ฮูปแต้ม naga dissolves into the cutaway: the "hungry naga" is the water that's gone
    ("valve", ["n12"], 0.15, 0.3, 2.2),            # twist: an old hand with an iron drill rod shuts the valve; the pump dies — พ่อใหญ่สิน
    ("sin1", ["s01"], 0.12, 0.3, 2.2),             # พ่อใหญ่สิน, close, lit by a lamp
    ("sin2", ["s02"], 0.12, 0.3, 2.2),             # memory sketch on the mural style: a buffalo at a hole 30 years ago
    ("sin3", ["s03"], 0.12, 0.3, 2.2),            # insert: the notches on the well post, falling night by night
    ("ton", ["t05"], 0.08, 0.3, 2.2),              # ต้นข้าว, eyes wide
    ("cordon", ["n13"], 0.15, 0.3, 2.2),           # dawn: officials with red rope round the hole (G1 · B5)
    ("sneak", ["n14"], 0.15, 0.3, 2.2),            # wide: everyone at the rope, a small figure (ยาย) slipping back toward the barn
    ("rumble", ["n15"], 0.12, 0.3, 2.2),           # low rumble; a clod drops; ground ripples (G1)
    ("ring", ["m04"], 0.08, 0.3, 2.2),             # the ring of cracks reaches the barn post; มุก points
    ("close", ["n16", ("n17", 0.25)], 0.25, 0.3, 2.2),  # cutaway under ยาย's house: the cave with no water left
    ("choice", ["n18"], 0.2, 0.3, 2.2),            # choice card pulled toward "ตามยายเข้าไป" → black
    ("end", [], 0, 0, 2.0),                        # end card: the headman's sign "ตอนที่ 3 · ไหว้ไกลร้อยเมตร (ตอนจบ)"
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
