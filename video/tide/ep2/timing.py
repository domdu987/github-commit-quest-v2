"""ทะเลลด EP.2 คลื่นแรกไป อย่าไว้ใจ. Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.15, 0.12, 2.6),            # EP.1's last frame on the hill (the bay drawn back, the white line); จูน dashes for the steps down
    ("grab", ["n02"], 0.05, 0.5, 1.8),             # insert: ตาจุ่น's old hand clamps จูน's wrist on "อย่า" (sting); her sandal skids
    ("pull", ["j01"], 0.12, 0.4, 2.6),             # two-shot on the steps: จูน yanks against the grip
    ("face", ["c01"], 0.3, 0.5, 2.8),              # close on ตาจุ่น: "ครั้งนี้… ตาไม่ปล่อย" (the rumour turned round)
    ("rule", ["c02"], 0.3, 0.6, 3.6),              # two-shot + ยาย's board: rule 1 ticked, rule 2 painted on
    ("how", ["j02"], 0.2, 0.4, 2.8),               # close on จูน: "ตารู้ได้ไง… นั่นกฎของยาย" (the EP.3 clue)
    ("below", ["n03"], 0.3, 0.5, 3.8),             # from the hill: people back on the wet beach collecting things; the line thickens (the audience sees it)
    ("series", ["n04", ("n05", 0.15)], 0.2, 0.4, 5.4),   # graphic: a train of crests, the gaps between them
    ("heights", ["n06", ("n07", 0.12), ("n08", 0.12), ("n09", 0.12)], 0.2, 0.6, 9.0),   # graphic: 2–3 m → 6–7 m → over 10 m vs the hotel
    ("stay", ["n10"], 0.2, 0.4, 3.2),              # back on the hill: ตาจุ่น still holding จูน, ตังค์ beside them; source chip ปภ.
    ("siren", ["a01"], 0.1, 0.4, 3.4),             # the tower for real: beacon, horns, the announcement chip
    ("turn", ["x01"], 0.1, 0.4, 3.4),              # the people below turn and run back up the steps toward the camera
    ("shop", ["y01"], 0.2, 0.4, 2.8),              # down at the shop: ยาย hugging the old photo, the sea far out behind
    ("hotel", ["y02"], 0.2, 0.5, 2.8),             # ยาย looks up at the 5-storey hotel next door → cut before she moves
    ("wall", ["n11"], 0.2, 0.4, 4.2),              # the second wave: a turbulent wall of water over the beach, a runner ahead of it
    ("smash", ["j03"], 0.4, 0.9, 5.0),             # from the hill: the village floods, ยาย's shop goes under
    ("duck", [], 0, 0, 3.0),                       # the duck ring floats past the hotel in the floodwater
    ("hush", [], 0, 0, 2.4),                       # silence: the kids frozen on the hill
    ("live", ["t01", ("j04", 0.2)], 1.35, 0.6, 5.0),   # จูน's live still on: "ยายพร❤️: ยายอยู่ชั้น 5 โรงแรม" pops up (the twist)
    ("raft", ["n12"], 0.2, 0.5, 3.4),              # a tourist clings to an ice cooler in the floodwater (UNESCO-IOC · USGS)
    ("notyet", ["c03"], 0.3, 0.6, 2.4),            # ตาจุ่น looks back at the sea: "ยังไม่จบ…"
    ("wave3", [], 0, 0, 4.4),                      # the next wave, bigger: the water climbs the hotel to the 3rd floor
    ("comment", [], 0, 0, 3.2),                    # the live: "ยายพร❤️: น้ำถึงชั้นสามแล้ว", then the typing stops
    ("tang", ["t02"], 0.3, 0.6, 2.6),              # close on ตังค์: "ยาย… ไม่พิมพ์แล้ว…"
    ("close", ["n13", ("n14", 0.25)], 0.3, 0.7, 3.8),   # the phone: the live freezes and ends
    ("choice", [], 0, 0, 3.2),                     # the choice, pulled toward going down to the hotel → black
    ("end", [], 0, 0, 2.4),                        # the end card: ตอนที่ 3 · หนีไม่ทัน (ตอนจบ)
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
