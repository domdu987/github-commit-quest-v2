# T6a2 QA (take T6, g1453-1535, 83 frames)

Setup: T6a's `render_t6a.run()` unchanged (same offsets, lights, 16 samples + OIDN, 720x1280), run for g1453-1535 only.
Added only the director's stale-actor leak fix (remove c2_/back_hair_/back_coat_ objects + `actors.clear_registry()` before each `stage_cast2`). An earlier run without it was discarded (19 frames).

## Identity check vs T6a
g1515 rendered in a fresh process vs `T6a/key2/g_1515.png`: same size, mean abs diff 0.066/255, max 3, 0 % of pixels differ by > 8 (noise only).

## Numbers
- Luma (RGB-mean, 90x160 bilinear): part mean 104.7, min 98.4, max 134.3 (after the beam-off re-render). Target 95-112 (P1 excluded); max is in the P1 card frames.
- qa_auto: PASS (0.0 % magenta). rhythm.py: 83 frames, 0 cuts detected, in-shot median 19.27, p90 34.05.
- Only the first 30 frames were luma-checked while rendering; I did not run a separate shimmer check on flat walls beyond viewing the frames below.

## Frames viewed (each at full 720x1280 and at phone size 360x640)
- g1453: high wide view of the archive hall. Blue balcony railing on the left, sign "GRAND ARCHIVES", carpet runner down the middle. Bertillon's group is tiny in the distance at the left. Cart with boxes in the foreground, sitting on the floor. No black slabs.
- g1475: camera lower and closer. The group (Bertillon, gendarmes, Dupont) stands by the wall drawer with a small table in front of them. The foreground table has a lamp, books and cards. Floor tiles clean. Phone size reads fine.
- g1495: mid shot. Bertillon holds a card up in his raised hand. The open drawer is to the left of him, Dupont is behind him wearing a green cap, and the gendarmes stand in the back. Feet are on the floor, and the table in front has props on it.
- g1515 (key): Bertillon fills the left, card held up. Dupont has sweat drops and a worried mouth. A gendarme with a moustache is on the right. The stool and floor are clean. His coat hem is a flat dark shape but the front reads as coat. No black slab.
- g1525: close-up, Bertillon's head is cut by the left frame edge. The card in his hand shows a bottle and two portraits. Dupont is on the right with sweat drops. Slight blur on the card edge, expected from the move.
- g1535: P1 card close-up. The MARTIN card fills about 76 % of the frame width: two orange-haired portraits, fingerprint, hand, table of strokes. Bertillon's sleeve is at the left edge, and a paper corner at top left. The open drawer is below the card. Card text is readable at phone size.

## Not verified
- Mouth/quote windows were not inspected frame by frame (no dialogue window in this range per takes.md).
- Contact sheet (contact.jpg) shows every 6th frame.

## Beam-off revision (director request)
- Beam switch: `TAKE_OVER['T6']['archive']['beam_k'] = 0.0` (same as T6a's beam0.py), set in render_t6a2.py.
- Beam-off vs original beam-on mean abs diff: g1460 3.97, g1470 3.22, g1475 3.08, g1480 2.86, g1485 2.10, g1490 0.92, g1530 0.00.
- Re-rendered g1453-1492 (40 frames) beam-off; g1493-1535 are the original frames (diff < 1 by g1492). Seam new/old at g1491-1492: diff 0.78 / 0.64.
- The 6-frame view above was of the beam-on version. After the re-render I only re-viewed g1453, g1471, g1491 at phone size: the pale cone over the vault is gone in all three. The luma stats and the contact sheet are updated. qa_auto re-run: PASS.
