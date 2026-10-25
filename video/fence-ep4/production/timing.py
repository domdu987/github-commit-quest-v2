"""Derive shot timing from the recorded voice so picture and sound share one schedule (เอาชีวิตรอด 99 วัน EP.4 รั้วล้ม).

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
    ("hook", ["n01", ("l01", 0.1), ("n02", 0.3)], 0.3, 0.35, 7.0),      # POV through the bars in the rain: a child crying out there; "อย่าเพิ่งออกไป"
    ("chapter", ["n03"], 0.15, 0.4, 3.0),                               # the page: 96 days; no weapon at all
    ("ask", ["d01", ("d02", 0.2), ("n04", 0.15)], 0.1, 0.3, 7.0),        # "เราจะสู้ด้วยอะไร" — the stock-keeper lists what the school has
    ("phuKnife", ["d03", ("n05", 0.3)], 0.2, 0.4, 4.6),                 # "ผมมีมีด"
    ("run", ["n06"], 0.1, 0.4, 3.4),                                    # the runner: three minutes, everything
    ("craft", ["n07", ("n08", 0.25), ("n09", 0.4), ("n10", 0.3)], 0.3, 0.9, 14.0),   # first person: broom + knife + tape = the spear; the steel pipe; +1
    ("loud", ["d04"], 0.15, 0.5, 3.2),                                  # "ด้ามไม่หักแล้ว แต่มันดัง"
    ("rain", ["n11", ("n12", 0.2)], 0.2, 0.4, 5.0),                      # the first rain; they get faster
    ("cry", ["l01", ("d05", 0.1), ("d06", 0.1), ("d07", 0.15), ("d08", 0.2), ("n13", 0.25)], 0.3, 0.3, 14.0),   # the crying; "ผมไปเอง"; "มันร้องเหมือนเดิมทุกครั้ง"; "นั่นไม่ใช่เด็ก"
    ("peek", ["n14", ("n15", 0.2)], 0.2, 0.3, 5.0),                      # the gate a hand's width: the crying stops; they come running in the rain
    ("trap", ["n16"], 0.1, 0.4, 3.4),                                   # the card: a child's cry is a human trap
    ("fenceFall", ["n17", ("n18", 0.15)], 0.2, 0.9, 7.0),                # twenty of them on the wet ground; the section goes down; the lunge
    ("flee", ["d09", ("n19", 0.2)], 0.05, 0.3, 4.4),                     # run for the back door; ก้อง goes down on the rebar
    ("cover", ["d10", ("d11", 0.2)], 0.1, 0.3, 5.0),                     # "ลุงกันให้" — "ยี่สิบวินาทีนะลุง"
    ("count", ["n20", ("n21", 0.3)], 0.2, 0.3, 13.0),                    # 20 → 8: he holds the breach with the spear; he is not running
    ("count2", ["d12"], 0.0, 0.0, 6.1),                                  # 5 → 0: "ปิดซะ ครู" — the bar drops
    ("after", ["n22"], 0.6, 0.6, 4.0),                                  # black; the corridor; five of them
    ("tq", ["n23", ("d13", 0.2), ("n24", 0.25), ("n25", 0.15)], 0.1, 0.4, 12.0),   # the tourniquet
    ("real", ["n26"], 0.1, 0.4, 5.0),                                   # in real life
    ("sig", ["s01"], 0.15, 0.5, 4.2),
    ("radio", ["r01", ("n27", 0.3)], 0.5, 0.4, 7.0),                     # 95… five
    ("ledger", ["d14"], 0.1, 0.4, 3.0),                                 # the spear is ก้อง's now
    ("dawn", ["n28", ("n29", 0.15)], 0.2, 0.4, 6.0),                     # ภู alone at the fallen fence; the small box
    ("walkie", ["w01", ("n30", 0.3)], 0.3, 0.5, 5.0),                    # the second radio
    ("drawing", ["n31"], 0.2, 0.6, 4.6),                                # the drawing: ลุง still standing outside
    ("choice", [], 0.0, 0.0, 3.4),
    ("next", [], 0.0, 0.0, 2.4),
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
