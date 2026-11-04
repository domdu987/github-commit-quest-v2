"""เสียงรถไฟ EP.1 (ทอร์นาโด). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.15, 0.12, 2.5),        # the title painted on the highway in the first frame; ฝน's live on the giant tornado (the lure)
    ("hook", ["n02"], 0.08, 0.5, 2.0),         # cut: ฝน raising her phone, the tornado behind her — red box "อย่ายกมือถือขึ้นถ่าย" + sting
    ("norail", ["n03"], 0.2, 0.4, 2.6),        # wide: open paddies, the highway, no railway anywhere — "ครืน…"
    ("clock", ["n04"], 0.2, 0.4, 1.8),         # the stall clock spins back an hour
    ("stall", ["n05"], 0.3, 0.4, 3.2),         # bright afternoon: ยายบัว's grill stall by the highway, the village, the temple
    ("live", ["f01", ("f02", 0.1)], 0.2, 0.3, 4.4),   # ฝน live, selling grilled chicken (live screen, comments, hearts)
    ("pu", ["p01", ("b01", 0.15)], 0.2, 0.4, 4.6),    # ปู with his little camera boasting; ยายบัว laughs at him
    ("cloud", ["n06"], 0.3, 0.5, 3.6),         # wide: behind the happy stall, a storm tower growing on the horizon (we see it first)
    ("tian", ["t01", ("t02", 0.15)], 0.2, 0.4, 5.0),  # ตาเทียน pulls up in his pickup; "open the windows" (planted)
    ("tale", ["b02", ("b03", 0.12)], 0.3, 0.5, 6.0),  # ยายบัว's old saying, close, the light dimming behind her
    ("eyes", ["f03"], 0.1, 0.3, 2.2),          # ฝน rolls her eyes: นิทาน
    ("ride", ["p02"], 0.1, 0.3, 2.6),          # ปู begs a ride in ตาเทียน's pickup (planted)
    ("dark", ["n07"], 0.3, 0.4, 3.0),          # 15:00 on the stall clock; the sky dark as night
    ("roar", ["n08", ("p03", 0.3)], 0.3, 0.4, 4.4),   # the roar comes: "ครืน…" — ปู: "เสียงรถไฟ? แถวนี้ไม่มีรางนะ"
    ("know1", ["n09"], 0.2, 0.4, 3.6),         # ฝน's phone: thunder spikes and fades; this sound is one long band that never stops
    ("touch", ["n10"], 0.2, 0.5, 3.4),         # the giant funnel touches down at the edge of the paddies
    ("lure", ["f04", ("n11", 0.15)], 0.1, 0.4, 5.0),  # ฝน's live: comments "ถ่ายต่อ" / "หนีเร็ว"
    ("rule", ["b04"], 0.1, 0.4, 3.2),          # ยายบัว shouts; the zinc rule sign: rule 1
    ("know2", ["n12", ("n13", 0.15)], 0.2, 0.4, 6.2),  # the roar = go now; some have no funnel to see (dust whirling under the cloud)
    ("pickup", ["t03"], 0.1, 0.3, 3.2),        # ตาเทียน: "ขึ้นรถ!" — behind him ปู climbs into the pickup bed (we see it; ฝน doesn't)
    ("run", ["f05", ("n14", 0.2)], 0.1, 0.4, 4.4),    # ฝน and ยาย run; the grill left smoking
    ("hit", ["n15"], 0.5, 0.6, 3.6),           # silence, then the first roof tears off and flies into the funnel
    ("house", ["f06", ("b05", 0.1)], 0.2, 0.4, 4.4),  # inside: ฝน at the window — ยาย: "อย่า! เข้าห้องน้ำ!"
    ("count", ["n16", ("b06", 0.15)], 0.2, 0.4, 5.2),  # the inner bathroom: ยาย counts heads
    ("where", ["f07"], 0.1, 0.3, 2.0),         # ฝน: "ปูอยู่ไหน!"
    ("gone", ["n17"], 0.2, 0.5, 3.0),          # cut: the pickup on the highway, ปู in the back, the tornado behind
    ("truck", ["t04", ("p04", 0.2)], 0.1, 0.5, 5.2),  # ตาเทียน drives at the overpass; ปู: "ใต้สะพานปลอดภัยจริงๆ ใช่ไหม"
    ("choice", ["n18"], 0.2, 0.5, 4.8),        # the choice: มุดใต้สะพาน / หมอบในคูน้ำ, pulled toward the bridge → black
    ("end", ["n19"], 0.45, 0.7, 3.0),          # the end card (owner 4 Nov: shorts carry EP.1 only): a highway sign "ปูจะรอดไหม? · ดูเรื่องเต็มได้ที่ช่อง YouTube" + plate "กดติดตาม"
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
