"""รูพญานาค EP.1 ดินแยกเป็นวง อย่าหลงเข้าใกล้. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.12, 0.1, 2.5),            # hook A: night, the village kneels at the torn rim with incense and phones; bike light rakes across
    ("hook", ["n02"], 0.05, 0.5, 2.1),            # close: ต้นข้าว's sneaker at the lip, a crack running under it, a clod drops
    ("crowd", ["n03"], 0.2, 0.3, 3.0),            # wide-ish: the lucky-number board 9-2-7, the stall, people asking; "why not?" left open
    ("lotto", ["n04"], 0.1, 0.5, 2.6),            # opening card: the board's drums roll back, chalk writes "สามวันก่อน"
    ("map", ["n05"], 0.3, 0.9, 4.4),              # map: Bangkok → Loei by the Mekong, the bus on the route, zoom to บ้านโนนนาค
    ("arrive", ["m01", ("y01", 0.12)], 0.2, 0.3, 4.4),  # ยาย's yard: มุก holds her phone up for signal; ยาย with a sickle and a rice sheaf
    ("ton", ["t01"], 0.1, 0.3, 3.0),              # ต้นข้าว runs through the cut field with his phone, past the straw stacks
    ("door", ["m02"], 0.2, 0.5, 2.8),             # insert: ยาย's door won't shut; the fence post leans (a real sign, G1)
    ("night", ["n06"], 0.3, 0.4, 3.4),            # night yard: a far pump thumps; nobody looks up
    ("notch", ["n07"], 0.2, 0.5, 3.6),            # insert: พ่อใหญ่สิน cuts a notch on the well post, below the others
    ("rumor", ["t02"], 0.2, 0.4, 3.0),            # the kids at the window watch พ่อใหญ่สิน; he looks back
    ("rule", ["y02", ("m03", 0.15)], 0.2, 0.5, 4.8),    # rules card: ยาย's palm-leaf, line 1 sooted; มุก rolls her eyes
    ("morning", ["n08"], 0.2, 0.4, 3.4),          # morning: the headman's field has a huge hole; people running
    ("sell", ["g01"], 0.1, 0.3, 3.0),             # ผู้ใหญ่ทอง at his stall plants the sign and sells incense
    ("legend", ["n09", ("n10", 0.15)], 0.3, 0.5, 7.4),  # the ฮูปแต้ม wall: the naga coiled under the earth, the ground splitting in a ring
    ("know0", ["n11", ("n12", 0.12)], 0.2, 0.4, 5.2),   # cutaway block: under the field is limestone; water dissolves a cave
    ("cave", ["n13"], 0.2, 0.6, 3.6),             # the cave runs on under ยาย's house (the viewer knows first)
    ("pray", ["n14"], 0.2, 0.3, 3.0),             # night: the rim full of incense and phones
    ("ask", ["t03"], 0.1, 0.3, 2.6),              # ต้นข้าว kneels and wai's at the hole, grinning
    ("lean", ["m04"], 0.1, 0.3, 3.0),             # side view: ต้นข้าว bends over the lip, phone out over the dark; มุก shouts
    ("crack", ["m05"], 0.1, 0.4, 3.4),            # the cracks ring the headman's feet; มุก points; people step back
    ("collapse", [], 0, 0, 2.4),                  # 0.4 s silence, then the rim drops where he stood (he had stepped back; no one falls)
    ("know1", ["n15"], 0.2, 0.4, 4.0),            # top-down: the ring of cracks round the hole, rings spreading (G1)
    ("know2", ["n16"], 0.2, 0.5, 4.4),            # everyone backing away; the coin icons: ring · sound · go
    ("thong2", ["g02"], 0.1, 0.4, 2.6),           # ผู้ใหญ่ทอง laughs it off with a dusty face
    ("home", ["n17"], 0.3, 0.6, 4.8),             # the twist: back home, ยาย's well water is mud; cracks ring the house posts
    ("fear", ["t04"], 0.2, 0.5, 3.0),             # ต้นข้าว, close, whispering
    ("close", ["n18", ("n19", 0.25)], 0.3, 0.6, 3.6),  # wide: the house in the dark, a low rumble, a ring of cracks glinting in the moon
    ("choice", ["n20"], 0.2, 0.6, 4.6),           # the choice: นอนต่อจนเช้า / พายายออกไปตอนนี้, pulled toward the first → black
    ("end", [], 0, 0, 2.4),                       # end card: the headman's sign with a note "ตอนที่ 2 · น้ำบ่อขุ่นแดง"
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
