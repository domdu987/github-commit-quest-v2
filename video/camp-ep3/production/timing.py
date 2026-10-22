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
    ("open", ["f00"], 0.3, 2.3, 5.0),
    ("chai", ["f01"], 1.0, 0.6, 3.5),
    ("inside", ["d08"], 0.6, 0.7, 4.0),
    ("map", ["f03"], 1.0, 1.4, 6.0),
    ("signal", ["f04", ("d09", 2.3)], 0.3, 0.6, 6.0),
    ("who", ["d10", "f05"], 0.3, 1.0, 5.0),
    ("aspirin", ["f06", "f07", "f08"], 0.3, 1.0, 6.0),
    ("siege", ["f09", ("f10", 0.4)], 1.7, 3.2, 6.0),
    ("sneak", ["g01", ("g02", 0.5), ("g03", 0.8)], 0.3, 1.7, 8.0),
    ("window", ["d11", ("f11", 0.4)], 0.6, 1.0, 6.0),
    ("dawn", ["f12", ("n15", 1.4)], 2.4, 1.2, 6.0),
    ("after", ["f14"], 0.4, 1.4, 4.0),
    ("call", ["f15", ("f16", 0.5)], 1.4, 0.6, 4.5),
    ("phone", ["f17"], 0.6, 3.4, 6.0),
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
