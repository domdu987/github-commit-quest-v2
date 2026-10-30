"""Side-by-side style-frame sheets for a new story: the latest clip (left) vs the new story (right), labelled, a few pairs per
sheet. The user judges every new story by "is it better than the latest clip", so style frames always go out in pairs (SKILL.md 3).

usage: python3 pairs.py <pairs.json> <out prefix> [pairs per sheet=3]
pairs.json: [{"old": "<png of the latest clip>", "new": "<png of the new story>", "label": "ฉากเปิด", "oldTag": "ตึกโยก EP.1 (ล่าสุด)",
              "newTag": "ทะเลลด (ใหม่)"}, ...]   (frames of the latest clip: snap its stored composition, see SKILL.md 4)
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 432, 768
GAP, PAD, HEAD = 14, 24, 64
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
FONT = os.path.join(REPO, "video", "quake-ep1", "composition", "assets", "fonts", "sriracha.ttf")


def font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def main():
    pairs = json.load(open(sys.argv[1]))
    prefix = sys.argv[2]
    per = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    f_lab, f_tag = font(30), font(24)
    for s in range(0, len(pairs), per):
        chunk = pairs[s:s + per]
        cols = len(chunk)
        sheet_w = PAD * 2 + cols * (2 * W + GAP) + (cols - 1) * PAD * 2
        sheet_h = PAD * 2 + HEAD + H + 40
        im = Image.new("RGB", (sheet_w, sheet_h), "#101014")
        d = ImageDraw.Draw(im)
        for i, p in enumerate(chunk):
            x0 = PAD + i * (2 * W + GAP + PAD * 2)
            d.text((x0, PAD), p["label"], font=f_lab, fill="#ffd34d")
            for j, key in enumerate(("old", "new")):
                fr = Image.open(p[key]).convert("RGB").resize((W, H))
                x = x0 + j * (W + GAP)
                im.paste(fr, (x, PAD + HEAD))
                tag = p.get("oldTag", "คลิปล่าสุด") if key == "old" else p.get("newTag", "เรื่องใหม่")
                d.rectangle([x, PAD + HEAD + H + 6, x + W, PAD + HEAD + H + 38], fill="#2a2a33" if key == "old" else "#0d6e6e")
                d.text((x + 10, PAD + HEAD + H + 8), tag, font=f_tag, fill="#ffffff")
        out = f"{prefix}_{s // per + 1}.jpg"
        im.save(out, quality=86)
        print(out, im.size)


if __name__ == "__main__":
    main()
