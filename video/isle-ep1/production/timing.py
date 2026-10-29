"""Derive shot timing from the recorded voice so picture and sound share one schedule (ติดเกาะร้าง EP.1 ปลาลูกโป่ง).

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
    ("hook", ["n01", ("n02", 0.12)], 0.25, 0.35, 6.5),                      # frame one: the balloon fish in his hands; cut to the sand, looking up, unable to blink
    ("yai", ["y01", ("y02", 0.25), ("t01", 0.3), ("y04", 0.3)], 0.4, 0.4, 9.0),               # the porch: the rule, the joke, the last line
    ("boat", ["t02", ("u01", 0.2), ("u02", 0.2)], 0.6, 0.4, 8.0),             # the longtail: ลุงนวล's method; "มารับก่อนมืด"
    ("stranded", ["n04", ("p02", 0.25), ("t03", 0.25)], 0.5, 0.3, 8.0),        # the squall; no signal; โต้ง's dream come true
    ("survive", ["t04"], 2.8, 0.4, 5.8),                                       # fire, water, shelter — all right; "เหลือข้อเดียว… อาหาร"
    ("fish", ["t05", ("t06", 0.3), ("p03", 0.3), ("p04", 0.35), ("t07", 0.3)], 0.6, 0.4, 11.0),   # the pool: it swims to him; the balloon; the photo; ยาย's rule vs ลุงนวล's method
    ("grill", ["n06", ("t08", 0.4), ("p05", 0.3)], 0.5, 0.5, 8.0),             # over the fire: the viewer is told first; the first bite; "ไม่กิน… อ้วน"
    ("wait", ["n07", ("t09", 0.4), ("p06", 0.25), ("t10", 0.6), ("n08", 0.25)], 0.3, 0.3, 12.0),   # twenty minutes of nothing; the numb lip; the stick he can't hold
    ("still", ["p07", ("i01", 0.3), ("n09", 0.25), ("p08", 0.3), ("p11", 0.6)], 0.4, 1.9, 14.0),   # eyes open, nothing moves; inside his head; she hears nothing, says it; the blanket (post 2.0)
    ("cloth", ["i03"], 0.8, 0.6, 3.4),                                         # from under the blanket: "พี่… อย่าคลุม… ผมยังอยู่"
    ("rule", ["y05", ("p09", 0.6), ("n10", 0.5)], 0.8, 0.8, 11.0),   # ยาย's words in memory; she uncovers him; the breath stops; no antidote — breathe for him
    ("card", ["n11"], 0.25, 0.45, 7.0),                                        # the safety card: gutting doesn't help, 1669, 2 breaths 30 compressions
    ("night", ["i02"], 0.5, 4.3, 8.2),                                         # the night: breaths counted, breaths given; the moon crosses (the counter tells it)
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("dawn", ["t11", ("u03", 1.3), ("p10", 0.45)], 1.0, 1.8, 10.0),             # his finger moves; the boat; ลุงนวล sees; "ลุงบอกว่ากินได้"; the stick by the fire
    ("line", ["t12"], 0.7, 1.0, 10.0),                                         # on the boat home: "เขาตัวเย็นมาก"
    ("choice", [], 0.0, 0.0, 3.6),
]


def pauses(wav):
    """Return the start times of speech chunks separated by silences of 0.14 s or more."""
    x = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", wav, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]), np.float32)
    hop = 160
    n = len(x) // hop
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    db = 20 * np.log10(rms + 1e-9)
    thr = max(db.max() - 34, -48)
    loud = db > thr
    starts, i = [], 0
    while i < n:
        if loud[i]:
            j = i
            while j < n and (loud[j] or (j + 14 < n and loud[j:j + 14].any())):
                j += 1
            starts.append(i / 100)
            i = j
        else:
            i += 1
    return starts


def frags(lid, dur):
    cap = LINES[lid].get("cap", LINES[lid]["text"])
    parts = cap.split(" / ")
    if len(parts) == 1:
        return [0.0]
    if "frags" in LINES[lid]:
        return LINES[lid]["frags"][:len(parts)]
    starts = pauses(os.path.join(HERE, "vo", f"{lid}.wav"))
    chars = [len(re.sub(r"[\[\]{}…]", "", p)) for p in parts]
    total = sum(chars)
    est = [0.0]
    for c in chars[:-1]:
        est.append(est[-1] + dur * c / total)
    out = [0.0]
    for k in range(1, len(parts)):
        cands = [s for s in starts if abs(s - est[k]) < 0.6 and s > out[-1] + 0.25]
        out.append(min(cands, key=lambda s: abs(s - est[k])) if cands else est[k])
    return [round(v, 3) for v in out]


def main():
    sched, t = [], 0.0
    for key, lines, pre, post, mn in SHOTS:
        vo, cur = [], pre
        for n, item in enumerate(lines):
            if isinstance(item, tuple):
                lid = item[0]
                if len(item) == 3 and item[2] == "start":
                    cur = vo[-1]["t"] + item[1]
                else:
                    cur = cur + item[1]
            else:
                lid = item
            d = DUR[lid]
            vo.append({"id": lid, "t": round(cur, 3), "dur": d, "cap": LINES[lid].get("cap", LINES[lid]["text"]), "frags": frags(lid, d)})
            cur += d
        dur = max(mn, cur + post)
        sched.append({"key": key, "start": round(t, 3), "dur": round(dur, 3), "vo": vo, "voEnd": round(cur, 3)})
        t += dur
    json.dump({"shots": sched, "total": round(t, 3)}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)
    for s in sched:
        print(f"{s['key']:10s} {s['start']:6.2f} {s['dur']:5.2f} ", " ".join(f"{v['id']}@{v['t']:.2f}{v['frags'][1:] if len(v['frags']) > 1 else ''}" for v in s["vo"]))
    print("TOTAL", round(t, 2))


if __name__ == "__main__":
    main()
