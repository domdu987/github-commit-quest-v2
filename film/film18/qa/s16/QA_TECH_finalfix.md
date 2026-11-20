# QA-tech FINAL-fix s16: FAIL

Checked: take.mkv (120 frames, g1195-1314, in-shot g1205-1308), all frames extracted. 6 fps montage, a 3-frame step montage g1250-1308 with y 860/880/950 guide lines, 1:1 crops of the caption band, and 3x zoom crops of the girl at g1268, 1275, 1285, 1290, 1295, 1298, 1300, 1304, 1306 and 1308.

## Blocker: the girl's face is not above y 860 at g1250-1308
- She is now smaller and further back, standing between the diggers, behind a basket, with the basket rim hiding her lower face. That part is as intended.
- But the visible part of her face (the brow and eyes, white with black buns above) reaches the line and then sinks into the caption band as the camera moves:
  - g1250-1260: buns at y about 830-840, face hidden behind the basket top (about y 855). OK.
  - g1268: eyes at y about 860.
  - g1275-1285: eyes at y about 860-870.
  - g1290-1295: eyes at y about 870-875, face top 850.
  - g1298-1308: eyes at y about 880-895, with her forehead at about y 865-880 and buns at 840-850.
- So from about g1268 to g1308 (about 40 frames) the visible face is on or below y 860, and about g1295-1308 the eyes sit inside the caption band (880-950). The head limit of "above y 860 on every frame from g1250 to g1308" is not met. The same problem as last time (face under the caption), only smaller, with her chin hidden.
- Fix: keep her buns and eyes at y <= 840 through g1308. Move her up the wall, or deeper, or lock her to a screen position, or remove her after about g1265. The camera tilt is carrying her down the frame, so any fix must keep the girl's world position moving up as the camera settles.

## Other checks (PASS)
- Holes, glow and camera look unchanged vs the passed round-4 take. The first breach opens at about g1228-1230, then more open one after another, each warm-lit, five to six by the end. The same dolly and truck. The same night palette, moon-blue sky and orange wall glow. Frame-diff matches the round-4 take (8.52 / 9.53 then, 8.24 / 9.55 now).
- Other faces: the elder and the other townsfolk are at y <= 840 on all frames g1250-1308 (skin mask, no skin rows at y 880-950 except the girl). The elder's beard tip reaches about y 880 at g1300-1308, as in the passed take. That is a beard, not a face. The other diggers' faces are at y 650-830.
- Frame-diff (area 90x160, in-shot, n=103): median 8.24, p90 9.55, min 4.89, max 11.20. This matches the claim (8.23 / 9.56) and is within 9-12, fine for the take gate. Single steps of 10.8 at g1212 and 11.2 at g1251 are the lighting step in the dissolve and a hole-opening, not pulses.

Notes (non-blocking):
- Pale needle streaks on the ground and a flat white-yellow quad on the ground at about g1295-1308 are still there (noted in the round-4 report).
- Dark navy outlined rocks and baskets in the foreground read as chunky but lit, not as grey slabs.
