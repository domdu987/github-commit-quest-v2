"""Derive shot timing from the recorded voice so picture and sound share one schedule (เอาชีวิตรอด 99 วัน EP.6 นิคม).

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
    ("hook", ["n01", ("n02", 0.2), ("n03", 0.2)], 0.3, 0.4, 7.5),     # first person in the washroom, a bottle in each hand over the bucket; "อย่าผสม"
    ("chapter", ["n04"], 0.3, 0.45, 4.8),                                # the board over the road at dawn, the six walking up; the camera glides to the lit fence
    ("gate", ["g01", ("n07", 0.25)], 0.3, 0.45, 5.2),                     # "เปิดประตู… ภูกลับมาแล้ว" — the gate slides, the whole estate stares at ภู
    ("win", ["w01", ("d01", 0.6)], 0.3, 0.45, 6.5),                      # คุณวิน: "ยินดีต้อนรับกลับบ้าน" (skill card เจ้านาย in the gap); ปั้น: the red tie from her drawing
    ("offer", ["w02", ("w03", 0.25)], 0.2, 0.5, 7.0),                   # rooms, three meals, power, tap water — for one thing: everyone must be useful
    ("register", ["w04", ("d02", 0.2)], 0.6, 1.3, 6.0),                 # the roster fills (no narration); "แล้วเด็กคนนี้ทำอะไรได้" — ปั้น gets "รอดู"
    ("knows", ["w05", ("d03", 0.25), ("n10", 0.25)], 0.2, 0.75, 8.0),      # he already knows the school; rule 3 on the card — "มีใครบางคน… บอกทางไปแล้ว"
    ("workshop", ["n11", ("d04", 2.6)], 0.2, 1.4, 7.5),   # the workshop: upgrade, first person (the card runs in the gap); "เราอยู่ที่นี่เถอะ" — "ขอครูคิดก่อน"
    ("calm", ["n14", ("n15", 0.3)], 0.4, 0.5, 5.0),                    # orderly, quiet, too quiet; one old woman in the whole estate
    ("yai", ["d06", ("y01", 0.2)], 0.2, 0.45, 6.0),                     # ยายจันทร์ scrubbing; "ยายยังทำไหว… ต้องให้เขาเห็น"
    ("mix", ["y02", ("n16", 0.2), ("n17", 0.2)], 0.2, 0.5, 8.5),      # two bottles into one bucket; bleach + the acid in toilet cleaner = chlorine gas
    ("sink", ["n18", ("n19", 0.2)], 0.2, 0.5, 6.0),                    # heavier than air, it pools on the floor — where ยาย kneels
    ("signs", ["n20", ("n21", 0.2)], 0.2, 0.55, 7.5),                  # coughing, stinging eyes, breathing hard; more → chest pain; enough → death
    ("out", ["d07", ("d08", 0.25)], 0.1, 0.6, 7.0),                     # "ออกไปข้างนอก!" — ภู: doors and windows open, don't go back in until the gas has gone
    ("real", ["n22"], 0.15, 0.55, 5.0),                                 # in real life: never mix cleaners; trouble breathing → ambulance
    ("watch", ["n24", ("n25", 0.3)], 0.3, 0.6, 6.4),                    # ยาย lives but can't work today; at the first-floor window someone writes it down
    ("dinner", ["d10"], 0.9, 0.6, 4.4),                                 # the canteen: คุณวิน presiding — "ที่นี่ไม่มีเด็กเลย นอกจากปั้น"
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("radio", ["r01", ("n27", 0.3)], 0.5, 0.55, 7.5),                   # 93… five; and in คุณวิน's room another radio is on
    ("night", ["n28", ("n29", 0.3)], 0.4, 0.9, 7.6),                    # midnight: the gate opens; ยายจันทร์ walked out; the gate closes (1 → 0)
    ("drawing", ["n30", ("n31", 0.2)], 0.2, 0.5, 5.2),                  # ปั้น's drawing: ยาย outside the fence among the black shapes
    ("choice", [], 0.0, 0.0, 3.4),
    ("next", [], 0.0, 0.0, 2.6),
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
