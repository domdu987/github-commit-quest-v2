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
    ("van", ["n03", "d02"], 0.3, 0.8, 4.0),
    ("fire", ["n04", "n05"], 0.4, 1.1, 5.0),
    ("call", ["d03", ("d04", -0.3)], 0.1, 0.3, 4.0),
    ("choice", ["d05"], 2.5, 2.0, 5.0),
    ("lost", ["n07"], 0.7, 0.5, 4.0),
    ("stop", ["n08"], 0.2, 1.0, 4.5),
    ("whistle", ["n09", ("n10", 1.9)], 1.4, 0.7, 6.0),
    ("hide", ["n11", ("n12", 0.3)], 0.8, 1.0, 7.0),
    ("snake", ["d06"], 1.0, 0.6, 3.6),
    ("firstaid", ["n13", "d07"], 0.2, 1.0, 6.0),
    ("radio", ["d08", "n15"], 0.3, 0.6, 5.0),
    ("message", ["d09"], 2.2, 0.4, 5.0),
    ("who", ["d10"], 0.2, 0.4, 3.6),
    ("window", ["d11"], 0.8, 1.3, 6.0),
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
