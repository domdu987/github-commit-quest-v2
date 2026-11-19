# FINAL gate - QA-art (Opus), film 13 "ไอ้แม่แรง" - release13/raeng.mp4
Input: release13/raeng.mp4 (720x1280, 30 fps, 1995 frames, 66.5 s, captions burned in) + release13/qa_auto/QA_AUTO.md.
Reference look: release9/rice_v1.mp4 (approved film-9 look; no release10 mp4 exists).
Sheets (scratch, /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/final13/):
- full2fps_00..11.jpg - full res, 2 fps (every 15th frame, 12 per sheet)
- phone_0..2.jpg - 360x640, 1 frame / 0.5 s, cyan line = y 880
- hook.jpg (g 0-150, every 5), reveal.jpg (g 1290-1650, every 10), ending.jpg (g 1670-1994, every 8)
- cmp_*.jpg - full-res checks (blur flags, heads vs caption band, s25 ceiling, purse, fall), ref_release9.jpg

## VERDICT: FIX-FIRST (one blocking item, cheap: one shot of s26)

## Blocking fixes
1. **s26 shot 28 (wide "ตึกลอยสูง / ขึ้นเกือบสองเมตร"), g 1800-1826 (60.0-60.9 s): a head crosses the caption band.**
   The red-vest, bowler-hat townsman walks in near camera at the right edge. Face centre about y 855 at g 1800 and about y 905
   at g 1815-1822, chin about y 940, until he leaves the frame at about g 1827. That breaks the hard rule (heads fully above y 880),
   and the s26 take gate missed it. He does not cover the caption text, but the rule has no exceptions and a director override is not allowed.
   Fix: re-render only shot 28 (g 1775-1870) with this card placed farther back on the plank walk, or walking at a smaller
   scale, or removed. Keep everything else in the shot. Re-run qa_auto on the head check, then re-conform.

No other blocking items.

## qa_auto "suspected blur" (104 frames): FALSE POSITIVES
Checked at full size:
- g 152-161 (tea_close, end of s02 plus gap-fill handle frames 159-161): cups, saucer rims, window bars and the town are crisp. The
  Laplacian drop comes from big smooth areas (lilac table and saucer, sky). It is not blur and not DOF.
- g 594 (cut into s10) and g 639-642 (suite_window): candles, armchair piping, the rich man's face lines and the rug edges are all
  crisp. The low score comes from the large, smooth, dark parquet floor and the wall. It is not blur.
- No depth-of-field anywhere in the film. Sharpness meets the client rule.
- Exception (texture, not DOF): in the cellar shots s22 (g 1416-1466) and **s25 (g 1602-1679)**, the floor beam above is a stretched,
  smeared wood-grain slab. In s25 it covers the top ~30 % of the frame. On the phone sheet it reads like a motion-smeared band.
  The s25 take gate accepted it as non-blocking. I keep it non-blocking but list it as the first polish item below.

## qa_auto "pops outside planned cuts"
All flagged g are planned cuts: take starts 63/162/367/594/726/912/975/1110/1300/1416/1467/1537/1602/1680, or intra-take shot
changes listed in the plan: 108 (shot 3), 303 (6), 447/513 (8, 9), 650 (11), 780/843 (12 second framing, 13), 1173/1255 (18, 19),
1743/1775/1871/1909 (27-30). There are no real pops.

## Scores (1-10)
| category | score | note |
|---|---|---|
| Set density / ornament | 8 | Hotel facade, plank walks, cribbing and jacks, and the street of awnings and lamps match film 9. The suite and the s15 count field are thinner. |
| Lighting & colour | 7 | Warm key light, lit windows, warm lamp pools under the hotel, blue-violet shade. The interiors run flat lilac/purple. s10 is dusk with candles, then s11 is bright day in the same beat. |
| Composition / framing | 7 | Good wides and mediums, and the camera keeps moving. s10 is half empty floor with the rich man small. s25 is 30 % smeared ceiling. In the s12 first framing the rich man is about 40 px at the top while he speaks Q1. |
| Character acting | 7 | Smug, laugh and mock read. The whistle reads. The fall and the sulk in the mud are clear and comic. Shot 27 "no ground under foot" is soft: he stands on the slab edge, does not step into air, and barely looks down. |
| Key moments (hook / reveal / ending) | 7 | Hook: the hotel on cribbing over lamp-lit voids and calm tea guests. The rise is subtle, but the image is strange. Reveal: whistle, bars together, even lift at every corner, all inside the lit world. Ending: the raised portico, the short old stair, the fall into mud and the purse to Pullman are all clear. |
| Overall match to references / client taste | 8 | Same flat-puppet-in-lit-3D look as release 9. No text signs, no 2D panels. Clouds are the approved half-disc style. |

## Continuity across cuts
- **Lift state:** OK.
  - Hook (s01): lifted, with cribbing and lamps under (flash-forward).
  - Pivot and setup (s04/s07), boss (s10-s12), nickname and count (s13/s14): the hotel sits at grade.
  - Jack and cribbing props already stand by the front stair in s04 rain (g 315-345) and s07 (g 525-590). This is preparation; acceptable.
  - False (s17/s19): interior only.
  - Reveal: s23 lifted on cribbing, s24 high on cribbing.
  - Ending (s26): full lift. The old stair stops about 2 m below the portico, and the gap reads.
- **Light:** DAY → RAIN (s04) → DAY. Three mismatches:
  - s07 shot 7 (g 367-446) has a much lower, golden sunset sun, and the sky is sprinkled with dozens of tiny cloud chips that read as confetti.
  - s10 (g 594-650) is dusk purple with candles lit, but s11/s12 straight after are bright day.
  - The ending's "MORNING" is the same warm DAY preset as s23/s24, which is fine.
  The s10 → s11 jump is the most visible. None is blocking.
- **Costume:** consistent.
  - Rich man: green check coat, top hat, grey side hair, cane at the ending.
  - Pullman: bowler, black coat, mustard waistcoat, teal tie, in s01, s07, s12, s13, s16, s20 and s26.
  - The guest couple matches in s02 and s19. The lady wears a red dress and cream bonnet; the gentleman a bowler and brown coat.
  - The gentleman guest is close to Pullman's silhouette (bowler and moustache). The blind viewer may confuse them. Not blocking.
- **Moving things:** the rich man's raised purse is held in his stick arm from g ~1917 until Pullman takes it, so no prop floats.
  The workers stay attached to their bars in s21/s22.
- **Splashes:** the client asked for no round-blob splashes, dust or halos. Two shots checked:
  - Fall (g 1898-1910): a spiky brown crown with flecks. Not a blob. OK.
  - s05 (g 285): a large translucent white crown-shaped splash in front of the cart. It is not round, but it reads like a plastic bowl. Polish only.

## Caption legibility (judged on the phone sheet)
- Kanit Black, white with a heavy black outline, one phrase at a time, centred at about y 900. Legible in every frame: on the bright mud,
  the rain grey, the orange cellar and the patterned rugs.
- Thai renders correctly. No tofu or black blobs.
- Heads sit above the band everywhere except blocking item 1. The s13 crowd and s16 workers come close (about y 780-820) but stay above it.

## Non-blocking polish (only if a re-render happens anyway)
1. s25 (g 1602-1679), and s22 to a lesser degree: tilt the camera down or retexture the floor beam above, so the stretched grain stops
   taking 30 % of the aha shot. Also show more of the "thousands of jacks" field.
2. s10 (g 594-650): match s11's daylight. Turn the candles off, give the window a day sky, and frame tighter so the empty parquet goes.
3. s07 shot 7 (g 367-446): cut the cloud chips to a few large clouds, as in s01/s23. Raise the sun to the DAY preset.
4. s26 shot 27 (g 1743-1774): put the front foot over the edge, in the air, and tilt the head down, so "ใต้เท้าไม่มีพื้น" is literal.
5. s05 (g 280-295): make the white crown splash smaller and muddier, or drop it.
