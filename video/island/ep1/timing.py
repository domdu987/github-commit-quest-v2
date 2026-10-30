"""ติดเกาะ EP.1 กระหายแค่ไหน อย่าหมายน้ำเค็ม (วิธีเล่าแบบ A คุณคือคนติดเกาะ). Derive shot timing from the recorded voice so picture and sound share one schedule.

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
    ("open", ["n01"], 0.15, 0.12, 2.6),          # opener (hook rule: the command lands by ~3 s): a girl's hand scoops clear seawater toward cracked lips; the title scratched in wet sand
    ("hook", ["n02"], 0.1, 0.6, 2.2),            # push in: the water runs out between the fingers; {อย่าดื่มน้ำทะเล}
    ("you", ["n03", ("n04", 0.15)], 0.2, 0.5, 4.2),    # the format: "ครั้งนี้ คุณคือคนติดเกาะ ทุกทางแยก คุณเลือก" — the coconut cards flash
    ("map", ["n05"], 0.3, 0.9, 4.4),             # map: Bangkok → the pier (van) → เกาะหลังเต่า (boat); the snack-bag pin
    ("pier", ["p01", ("j01", 0.12)], 0.2, 0.4, 5.0),   # the pier: ภูมิ's three snack bags; ลุงเจี๊ยบ tosses one bottle
    ("rule", ["w01", ("w02", 0.3)], 0.3, 0.5, 5.2),    # ตาเวียง at his hut: rule 1 on the paddle (rule card), then "น้ำจืด… อยู่บนต้น"
    ("laugh", ["x01", ("p02", 0.1), ("n06", 0.2)], 0.2, 0.4, 6.0),  # "ตาบ้ามาอีกแล้ว", ภูมิ sings the rule back, "คุณหัวเราะ เหมือนทุกคน"
    ("legend", ["n07", ("n08", 0.15), ("f01", 0.2)], 0.3, 0.4, 7.8),  # the shadow screen: the fires on เกาะผี, the swimmer who never came back; ฟ้า "นิทานหลอกเด็ก"
    ("storm", ["n09"], 0.3, 0.6, 4.4),           # the 3D map: the squall builds in the west as the boat leaves the pier
    ("squall", [], 0, 0, 3.0),                   # on the boat: rain, waves, the engine dies, ลุง yanks the cord
    ("wreck", ["j02"], 0.2, 0.5, 3.4),           # "เครื่องดับ! เกาะเรือไว้!!" the hull hits the rocks
    ("wash", ["f02"], 0.2, 0.6, 3.2),            # from the beach: the boat and ลุง drift off into the rain, the red cap floats
    ("day1", ["n10", ("p03", 0.25)], 0.3, 0.4, 5.4),   # "วันที่ 1": the two on the empty beach, the foam box: "น้ำส้มสายชู? จิ้มขนมเหรอ"
    ("heat", ["n11"], 0.3, 0.5, 3.0),            # insert: the bottle is empty; the sun; "บ่ายสอง"
    ("fork1", ["n12", ("n13", 0.9)], 0.2, 0.5, 6.2),   # the fork card: A ดื่ม (ผสมน้ำจืด) / B ไม่ดื่ม — countdown — "คนส่วนใหญ่ เลือกดื่ม"
    ("give", ["f06"], 0.3, 0.5, 3.0),             # the wrong path, played like a film: ฟ้า hands the last fresh water to her brother
    ("drink", ["f03", ("p04", 0.15)], 0.2, 0.5, 5.2),  # "พี่ดื่มน้ำทะเลก็ได้ ในคลิปบอกว่าผสมน้ำจืดนิดเดียว" — she tips a few drops in and drinks; ภูมิ "พี่…"
    ("know1", ["n14", ("n15", 0.15)], 0.3, 0.4, 6.0),  # the body diorama: the kidneys can only make urine less salty than the sea; more water out than in
    ("know2", ["n16", ("n17", 0.2)], 0.2, 0.5, 5.6),   # mixing in fresh water only spends it on the salt; the gauge drops; "ยิ่งดื่ม ยิ่งกระหาย"
    ("worse", ["f04"], 0.3, 0.6, 3.4),           # ฟ้า dizzy under the palm, lips cracked, the symptom slats; she folds
    ("dark", ["n18"], 0.4, 0.8, 3.2),            # the screen drains to black: "ทางนี้… คุณไม่ถึงเช้า"
    ("rewind", ["n19", ("w03", 0.2)], 0.2, 0.4, 5.0),  # ◀◀ the sea runs backward; the paddle glows: rule card 1, ตาเวียง's voice echoes
    ("pourout", [], 0, 0, 2.0),                  # the right path: she pours the cup out on the sand
    ("tree", ["p05"], 0.2, 0.5, 3.2),            # ภูมิ looks up the coconut palm: "น้ำจืด… อยู่บนต้น!"
    ("stake", ["p06", ("n20", 0.2)], 0.3, 0.5, 5.4),   # insert: the sharpened stake in the sand, the husk torn, water runs: "ใครปักไม้ไว้?" / "น้ำมะพร้าวอ่อน ดับกระหายได้"
    ("sip", ["f05"], 0.3, 0.5, 3.0),             # ฟ้า drinks from the coconut: "…คลิปไม่เคยบอก"
    ("rain", ["n21", ("n22", 0.3)], 0.3, 0.5, 5.2),    # dusk rain on the poncho, ภูมิ's open mouth: "ฝนมา ดื่มให้มากที่สุด" / "คุณรอด คืนแรก"
    ("night", ["p07"], 0.6, 0.6, 4.2),           # the first night: a tap from the rocks, one light far out on the water: "พี่… ไฟมันเรียกเรา"
    ("close", ["n23", ("n24", 0.25)], 0.3, 0.7, 3.8),  # wide: the light on the black sea: "ไฟบนทะเลคืนนั้น… / ไม่ใช่เรือมารับ"
    ("fork2", ["n25", ("n26", 0.2)], 0.3, 0.6, 6.4),   # the hanging fork: ว่ายออกไปหาไฟ / รอจนเช้า — the countdown runs out, no answer: comment → black
    ("end", [], 0, 0, 2.4),                      # the end card: the bottle with the note "ตอนที่ 2 · พิษไหม้" drifts onto the beach
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
