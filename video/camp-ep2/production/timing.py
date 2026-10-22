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
    ("open", ["e00", ("e01", 0.5)], 0.3, 0.4, 5.0),
    ("chase", ["e02"], 1.0, 0.8, 4.5),
    ("fall", ["e03"], 1.6, 0.8, 5.0),
    ("voices", ["e04", ("e05", 0.4), ("e06", 0.5), ("e07", 0.3), ("e08", 0.3)], 0.3, 1.6, 8.0),
    ("reunite", [], 0.0, 0.0, 3.2),
    ("map", ["e15"], 1.2, 1.4, 6.0),
    ("herd", ["e09", ("n12", 3.2), ("e10", 0.4)], 0.4, 1.6, 8.0),
    ("bite", ["d06"], 1.0, 0.6, 3.6),
    ("aid", ["n13", "e11", "d07"], 0.2, 0.9, 6.0),
    ("hut", ["e12"], 0.5, 1.4, 3.6),
    ("door", ["e13", ("e14", 0.3)], 1.5, 3.2, 6.0),
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
