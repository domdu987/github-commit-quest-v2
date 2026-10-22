"""Derive shot timing from the recorded voice so picture and sound share one schedule.

Each shot lists its voice lines in order, as "id", ("id", gap) where gap is the time from the end of
the previous line (negative = overlap), or ("id", offset, "start") to start offset seconds after the
previous line started. A shot lasts pre + lines + post, but never less than `min`.
Writes schedule.json (used by the composition and by mix.py).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = json.load(open(os.path.join(HERE, "vo", "durations.json")))

# key, [voice ids], pre-roll, post-roll, minimum length
SHOTS = [
    ("open", ["d00", ("n00", 1.4, "start")], 0.3, 1.6, 6.0),
    ("arrive", ["n01", "n02"], 0.3, 1.3, 5.0),
    ("ranger", ["d01"], 0.4, 0.5, 4.0),
    ("van", ["n03", "d16", "d02"], 0.3, 1.0, 4.0),
    ("fire", ["n04"], 0.4, 1.6, 4.6),
    ("call", ["d03"], 0.1, 0.2, 4.0),
    ("callpov", ["d04"], 0.4, 0.4, 2.8),
    ("choice", ["d05", "n06"], 2.5, 0.6, 5.0),
    ("lost", ["n07"], 0.7, 0.8, 4.4),
    ("stop", ["n08"], 0.2, 1.0, 4.5),
    ("whistle", ["n09", ("n10", 2.4)], 1.4, 0.6, 6.0),
    ("hush", [], 0.0, 0.0, 4.2),
    ("reveal", ["d12"], 2.4, 0.6, 5.0),
    ("twoshot", ["d13", "d14"], 0.2, 0.4, 4.0),
    ("eyes", ["n16"], 0.3, 1.6, 4.2),
    ("final", ["d15"], 0.3, 2.9, 6.0),
]
GAP = 0.2


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
            vo.append({"id": vid, "t": round(cur, 3), "dur": DUR[vid]})
            cur += DUR[vid]
        dur = max(mn, cur + post)
        out.append({"key": key, "start": round(t, 3), "dur": round(dur, 3), "vo": vo, "voEnd": round(cur, 3)})
        t += dur
    json.dump({"total": round(t, 3), "shots": out}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)
    for s in out:
        print(f"{s['key']:10s} {s['start']:7.2f} {s['dur']:5.2f}  " + " ".join(f"{v['id']}@{v['t']:.2f}" for v in s["vo"]))
    print("TOTAL", round(t, 2))


if __name__ == "__main__":
    main()
