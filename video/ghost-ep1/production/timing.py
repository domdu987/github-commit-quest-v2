"""Derive shot timing from the recorded voice so picture and sound share one schedule.

Each shot lists its voice lines in order; a shot lasts pre + lines (+ gaps) + post, but never less
than `min`. Writes schedule.json (used by the composition and by mix.py).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = json.load(open(os.path.join(HERE, "vo", "durations.json")))

# key, [voice ids], pre-roll, post-roll, minimum length
SHOTS = [
    ("open", ["n00"], 1.25, 0.55, 4.0),
    ("flash", ["n01"], 0.25, 0.55, 3.2),
    ("arrive", ["n02"], 0.3, 0.6, 3.6),
    ("storm", ["n03"], 0.3, 0.6, 3.8),
    ("mistake1", ["d04", "n04"], 0.3, 1.0, 4.2),
    ("exhaust", ["n05"], 0.25, 0.8, 3.4),
    ("cat", ["n06"], 0.25, 0.4, 3.6),
    ("knock", ["n07"], 1.0, 0.9, 3.8),
    ("headache", ["n08"], 0.2, 0.5, 3.2),
    ("mistake2", ["n09"], 0.2, 0.7, 3.6),
    ("losttime", ["n10"], 0.6, 0.4, 3.6),
    ("ghost", ["n11"], 0.25, 1.1, 3.6),
    ("wake", ["n12"], 0.2, 0.5, 3.2),
    ("symptoms", ["n13"], 0.2, 0.4, 3.4),
    ("catfirst", ["n14"], 0.2, 0.4, 3.2),
    ("xray", ["n15"], 0.2, 0.5, 3.6),
    ("escape", ["n16"], 0.15, 0.5, 3.6),
    ("block", ["d17"], 0.6, 1.2, 3.0),
    ("call", ["n18"], 0.2, 0.5, 3.6),
    ("rescue", ["n19"], 0.2, 0.5, 3.6),
    ("morning", ["n20"], 0.3, 0.6, 3.6),
    ("thinks", ["n21"], 0.2, 0.5, 3.4),
    ("who", ["d22"], 0.3, 1.2, 3.2),
    ("stillhere", ["n23"], 0.3, 1.6, 3.8),
    ("end", ["n24"], 0.4, 1.8, 5.0),
]
GAP = 0.2


def main():
    t = 0.0
    out = []
    for key, ids, pre, post, mn in SHOTS:
        cur = pre
        vo = []
        for i, vid in enumerate(ids):
            if i:
                cur += GAP
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
