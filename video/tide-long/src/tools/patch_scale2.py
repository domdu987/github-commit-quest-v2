"""Long version, review round 2 (6 Nov): what B1 left and three EP.3 notes. Run after patch_scale.py. Exact, asserted replacements
in tidelong/ep3/body.part; a replacement already present is skipped.

  B1′ the people running to their cars in "hook" (and the same set in "brB") were drawn at walker scale 0.72–0.78: 67–78 px against
      sedans of 93–96 px and ยาย (on her deck, further back) at ~100 px. At the cars' ~65 px/m an adult is ~107 px, so the walkers are
      scaled ×1.6 (s0 0.75 → 1.20 …): ~1.1× the sedans, as tall as ยาย or more (×1.45 measured level with the roofs). (The helper reads s0 only.)
  N3  ยาย stood on her deck in "hook" and "yai" but vanished from it in "cars" and "jam" between them, with the deck in frame:
      she is there now too, still hugging the photo.
  N1  in "wed" the caption "วันพุธถัดมา…" covered จูน's face for ~0.4 s as the camera tilted down past it: จูน stands 120 further
      right (x 930 → 1050), out of the caption's column. (N4, the tilt holding on the tower a little longer, is in land3.part.)"""
import os

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
p = os.path.join(W, "ep3", "body.part")
done = []


def sub(old, new):
    s = open(p).read()
    if new in s:
        return done.append("already")
    assert s.count(old) == 1, (old[:90], s.count(old))
    open(p, "w").write(s.replace(old, new)); done.append("ok")


# B1′ walkers ×1.45
sub('{ x0: 1200, y0: 1700, x1: 900, y1: 1650, s0: 0.75, s1: 0.72, step: 0.12, flip: true, at: 0.6 }, { x0: 40, y0: 1695, x1: 330, y1: 1648, s0: 0.75, s1: 0.72, step: 0.13, at: 1.2 },',
    '{ x0: 1200, y0: 1700, x1: 900, y1: 1650, s0: 1.20, s1: 1.15, step: 0.12, flip: true, at: 0.6 }, { x0: 40, y0: 1695, x1: 330, y1: 1648, s0: 1.20, s1: 1.15, step: 0.13, at: 1.2 }, // long: ×1.6 (review r2 B1′)')
sub('{ x0: 1180, y0: 1700, x1: 760, y1: 1640, s0: 0.75, s1: 0.72, step: 0.12, flip: true }, { x0: 1260, y0: 1720, x1: 520, y1: 1640, s0: 0.78, s1: 0.72, step: 0.12, flip: true, at: 0.3 },',
    '{ x0: 1180, y0: 1700, x1: 760, y1: 1640, s0: 1.20, s1: 1.15, step: 0.12, flip: true }, { x0: 1260, y0: 1720, x1: 520, y1: 1640, s0: 1.25, s1: 1.15, step: 0.12, flip: true, at: 0.3 }, // long: ×1.6 (review r2 B1′)')
sub('{ x0: 60, y0: 1690, x1: 420, y1: 1640, s0: 0.74, s1: 0.72, step: 0.13 }, { x0: -40, y0: 1700, x1: 250, y1: 1644, s0: 0.76, s1: 0.72, step: 0.12, at: 0.5 },',
    '{ x0: 60, y0: 1690, x1: 420, y1: 1640, s0: 1.18, s1: 1.15, step: 0.13 }, { x0: -40, y0: 1700, x1: 250, y1: 1644, s0: 1.22, s1: 1.15, step: 0.12, at: 0.5 },')
# N3 ยาย on her deck in cars and jam
YAIA = '\n        actors: [A("yaiTideHug", YAI.x, YAI.y, YAI.s, [{ t: 0, mode: "hugPhoto", eyes: "worry", mouth: "frown" }], { flip: true })], // long: ยาย stays on her deck (review r2 N3)'
for cam in ('cam: { keys: [{ t: 0, ...fr(560, 1560, 2.1, 540, 980) }, { t: D("cars"), glide: D("cars"), ...fr(540, 1565, 2.25, 540, 980) }] },',
            'cam: { keys: [{ t: 0, ...fr(760, 1590, 1.7, 540, 1060) }, { t: D("jam"), glide: D("jam"), ...fr(700, 1590, 1.8, 540, 1060) }] },'):
    sub(cam, cam + YAIA)
# N1 จูน out of the caption's column in wed
sub('A("june", 930, 1820, 0.6, [{ t: 0, mode: "idle", eyes: "normal", mouth: "flat" }], { flip: true }),',
    'A("june", 1050, 1820, 0.6, [{ t: 0, mode: "idle", eyes: "normal", mouth: "flat" }], { flip: true }), // long: was x 930, under the caption during the tilt (review r2 N1)')
print("patch_scale2:", " ".join(done))
