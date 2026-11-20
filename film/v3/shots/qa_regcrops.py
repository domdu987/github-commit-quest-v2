#!/usr/bin/env python3
"""qa_regcrops.py -- look at the registration on the rendered frames: 3x crops around the world target of the pinned prop
(the growing end of the track for the pencil, the eraser's target for the eraser), with a cross-hair on the target.

    python3 qa_regcrops.py <raw_dir with meta/> <out.jpg> <g,g,...>
"""
import json, os, sys
from PIL import Image, ImageDraw


def main(argv):
    raw, out = argv[0], argv[1]
    gs = [int(v) for v in argv[2].split(",")]
    R, Z = 48, 3
    S = Image.new("RGB", (len(gs) * (2 * R * Z + 4), 2 * R * Z + 18), (16, 12, 20))
    d = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        m = json.load(open(os.path.join(raw, "meta", "g_%04d.json" % g)))
        x, y = m["reg"]["want"]
        im = Image.open(os.path.join(raw, "f_%04d.png" % (g + 1))).convert("RGB")
        c = im.crop((int(round(x)) - R, int(round(y)) - R, int(round(x)) + R, int(round(y)) + R)).resize((2 * R * Z, 2 * R * Z), Image.LANCZOS)
        x0 = i * (2 * R * Z + 4)
        S.paste(c, (x0, 18))
        cx, cy = x0 + R * Z + (x - round(x)) * Z, 18 + R * Z + (y - round(y)) * Z
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            d.line((cx + dx * 14, cy + dy * 14, cx + dx * 40, cy + dy * 40), fill=(0, 255, 255), width=1)
        d.text((x0 + 3, 2), "g%d  reg %.2f px  %s" % (g, m["reg"]["px"], m["reg"]["who"]), fill=(255, 255, 255))
    S.save(out, quality=93)


if __name__ == "__main__":
    main(sys.argv[1:])
