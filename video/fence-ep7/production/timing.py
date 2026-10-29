"""Derive shot timing from the recorded voice so picture and sound share one schedule (เอาชีวิตรอด 99 วัน EP.7 คนไร้ประโยชน์).

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
    ("hook", ["n01", ("n02", 0.2), ("n03", 0.2)], 0.3, 0.45, 8.0),     # at the canteen table: ปั้น's hands at her throat, our hand slapping her back, the slap count climbing; "อย่ามัวแต่ตบหลัง"
    ("chapter", ["n04"], 0.3, 0.5, 4.8),                                # the yard at dawn, the board "เหลือ 93 วัน"; ยายจันทร์'s brush by the washroom door
    ("board", ["w01", ("n05", 0.3)], 0.3, 0.6, 7.0),                    # คุณวิน to the line-up: the least useful must go at the week's end; the score card — ปั้น at the bottom
    ("dinner", ["d01", ("d02", 0.25)], 0.4, 0.3, 5.0),                  # ปั้น wolfs her rice to go and wash up; "กินช้าๆ ลูก"
    ("choke", ["n06", ("n07", 0.25)], 0.3, 0.3, 6.0),                   # silent, hands at her throat; can't cough, can't speak, can't breathe
    ("panic", ["d03"], 0.2, 1.4, 3.6),                                  # เจ๊หงส์ slaps, ก้อง grabs a cup, the slap counter climbs; คุณวิน stands and watches
    ("phu", ["p01", ("p02", 2.3)], 0.2, 2.2, 9.5),                       # ภู kneels behind: lean forward, five back blows (counter); not out — abdominal thrusts, out on the third
    ("breathe", ["d04"], 0.8, 0.6, 4.4),                                # she breathes; ครูพิม holds her; "หนูขอโทษ… หนูจะไม่เป็นภาระ"
    ("card", ["n08"], 0.2, 0.6, 7.0),                                   # the steps card: still coughing → keep coughing; not → 5 back blows, 5 abdominal thrusts, alternate
    ("real", ["n09"], 0.2, 0.6, 5.5),                                   # in real life: not out → ambulance; even if out → hospital; babies under 1 → no abdominal thrusts
    ("win", ["w02", ("n10", 0.3), ("n11", 0.4)], 0.3, 0.7, 9.0),        # "มือยังไวเหมือนเดิมนะ ภู" — he has seen it before; the notebook: ปั้น → ภาระ
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("scarf", ["n12", ("n13", 0.3)], 0.5, 0.5, 6.2),                    # midnight, from the dorm window: ภู ties a red scarf under the lamp and walks to the office
    ("office", ["r01", ("w03", 0.4)], 0.4, 0.8, 7.0),                   # outside คุณวิน's lit window: the radio "92… five"; "ผ้าผืนนี้ ฉันเก็บไว้ให้นายตลอด"
    ("drawing", ["n14"], 0.3, 0.6, 4.4),                                # ปั้น's drawing: เจ๊หงส์ behind bars, a fridge with a red cross
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
