#!/usr/bin/env python3
"""qa_captions.py -- caption geometry on the finished MP4: bounding box of every Thai phrase (difference between the
captioned frame of the MP4 and the same picture frame without captions) and its distance to the nearest head.

    python3 qa_captions.py <proto.mp4> <frames_dir> <raw_dir with meta/> [out.json] [crops.jpg]
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timing


def main(argv):
    mp4, frames, raw = argv[0], argv[1], argv[2]
    T = timing.load()
    tmp = os.path.join(os.path.dirname(HERE), "tmp", "shots", "capq")
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, os.path.join(tmp, "c_%04d.png")], check=True)
    rows, crops = [], []
    for p in T["phrases"]:
        g0 = int(np.ceil(p["t0"] * 30 - 1e-6)); g1 = int(np.ceil(p["t1"] * 30 - 1e-6)) - 1
        g1 = min(g1, T["N"] - 1)
        boxes, margins = [], []
        for g in range(g0, g1 + 1):
            a = np.asarray(Image.open(os.path.join(tmp, "c_%04d.png" % (g + 1))).convert("RGB"), np.int16)
            b = np.asarray(Image.open(os.path.join(frames, "f_%04d.png" % (g + 1))).convert("RGB"), np.int16)
            # caption pixels: white fill or black outline that the picture frame does not have (codec noise never is both
            # that different and that pure)
            d = (np.abs(a - b).max(2) > 90) & ((a.min(2) > 215) | (a.max(2) < 40))
            d[:790] = False; d[1010:] = False
            ys, xs = np.where(d)
            if len(xs) < 50:
                continue
            box = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
            boxes.append(box)
            m = json.load(open(os.path.join(raw, "meta", "g_%04d.json" % g)))
            for who, h in m["heads"].items():
                if h["x"] + h["w"] / 2 > box[0] and h["x"] - h["w"] / 2 < box[2]:      # head above the caption's columns
                    margins.append(box[1] - (h["y"] + h["h"] / 2.0))
        if not boxes:
            rows.append(dict(text=p["text"], frames=[g0, g1], found=False)); continue
        bx = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
        rows.append(dict(text=p["text"], beat=p["beat"], frames=[g0, g1], shown_frames=len(boxes), box=bx, width=bx[2] - bx[0] + 1, height=bx[3] - bx[1] + 1,
                         centre_x=round((bx[0] + bx[2]) / 2.0, 1), centre_y=round((bx[1] + bx[3]) / 2.0, 1),
                         min_gap_to_head_px=(round(min(margins), 1) if margins else None)))
        gm = (g0 + g1) // 2
        crops.append(Image.open(os.path.join(tmp, "c_%04d.png" % (gm + 1))).convert("RGB").crop((60, 820, 660, 980)))
    for r in rows:
        print(r)
    if len(argv) > 3:
        json.dump(rows, open(argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if len(argv) > 4 and crops:
        S = Image.new("RGB", (600 * 2, 160 * ((len(crops) + 1) // 2)), (0, 0, 0))
        for i, c in enumerate(crops):
            S.paste(c, (600 * (i % 2), 160 * (i // 2)))
        S.save(argv[4], quality=93)
    return rows


if __name__ == "__main__":
    main(sys.argv[1:])
