# QA-tech sA1 v2 (team1 9cc4f6f)

**Verdict: PASS** (no blocking issue; 4 non-blocking notes).

Inputs: take.mkv (84 frames, g0-83, 720x1280), QA.md, meta.json, contact.jpg, phone_sheet.jpg, f6/ (every 5th g). Full-size frames g0, g20, g40, g60, g80 viewed; 2x crops of the crest (g60) and the bridge (g20). Team figures taken from QA.md (qa_auto PASS, rhythm median 9.63, p90 12.01). Colour judged as content only (colour policy).

## Old list, item by item
| old item | status |
|---|---|
| 1 Scots not findable (blocking) | FIXED. Three blue saltire banners and a blue/gold line sit on the open slope, clear of the pines. Banners read at full size from g30-40 and are clear at g60-80. At g0 only a 2 px white X shows (the crag is under 5 % of the frame, as the plan wants). |
| 2 Two-by-two knights not readable (blocking) | MOSTLY FIXED. Crimson/white caparisoned pairs fill the deck and the causeways with a gold pennon each. At g20 the crop shows a clear double red-white column; at g40 full size it is a red-white double line along the bridge. At g0 on the phone sheet it is still a thin brown-red line (non-blocking, note 1). |
| 3 Flat yellow light-shaft slabs | FIXED. No slabs on the crag in any viewed frame. |
| 4 Velocity into the D6 | OK. Pre-roll key at g-40 and the g159 key keep the move going through g81-83. A2 must match the g81-83 handle velocity. |
| 5 Slow first second | FIXED. Cruise speed from g0. p90 12.01 against the old 8.15. |
| Palette (old art fix 1) | FIXED. The neon pink crag is gone: it is now a grey-green crag with a dark pine crown. The fields are green and straw-gold with some brown strips. The river is teal. No neon fields. The loop meadow is a large ochre-yellow flat; that is set colour (see note 3). |

## Beat table
| g | what is on screen | read at phone size |
|---|---|---|
| 0-15 | Extreme wide from the south. Loop, bridge, camp and the crag in one frame, with the mountain ridge above. Everything is under 5 % of frame height. | Strong map read. The bridge is a thin line. The crag is small and dark. |
| 15-35 | The camera drops towards the bridge. The pair column becomes a red-white double dotted line. | The "two by two" idea reads from about g25-30. |
| 35-55 | The bridge runs diagonally across the frame, with a teal river and the camp tents with red-white parasols. The crag grows, with three saltires. | Best beat. Knights and Scots are both findable. |
| 55-70 | The bridge leaves the frame. The crag with its saltire line is centre. | The Scots line reads (blue banners, blue/gold figures). |
| 70-80 | The camera flies over the river towards the crag, with the pines on top and the slope in the lower half. | Reads as the arrival at P_A. |
| 81-83 | The handles continue the move. | OK. |

## Checks
- **BIGZOOM:** one continuous, eased move through set detail (river, bridge, parasols, pines). Start under 5 %. A1 ends at the fixed P_A, not yet medium; that is correct for the half (A2 carries it to 35-60 %). Figures at g80 are about 1-2 % of the height. No pop (rhythm median 9.63, p90 12.01).
- **Heads above y 880:** not applicable (no cast cards). At g80 the figures are around y 580-740.
- **Floating:** nothing floats. Trees, tents and pines are grounded with shadows. The knights ride on the deck. No figures are cut by the frame edge (the bridge leaves at the left/bottom, which is scenery).
- **Faces over 35 %:** none.
- **Colour story:** English crimson/white/gold (caparisons, parasols). Scots saltire blue/white. No blue on the English. The Scots line also carries orange/gold blocks (see note 2).
- **Characters acting:** the riders walk north at 1.3 m/s. The Scots stand still. Both are too small for acting at this distance; the hook needs only presence.
- **Camera clearance:** the camera is clear of the ground and the pines at P_A (g80 pose 95 m high, over the river). No clipping.
- **Bloodless:** yes.
- **D6 handle:** continues the same direction and speed. OK.

## Issues
1. **g0-25, non-blocking.** The bridge column is a thin brown line on the phone sheet at g0-15; the pairs only read from about g25. Fix, if there is time: widen the pair scale from 1.4x to about 1.8x, or start the camera about 15 % lower. Not required: the narration "ทีละสองคน" falls later than g0, and by g30-45 the column reads clearly.
2. **g40-80, non-blocking.** The Scots are small blue and gold blocks scattered on the slope; they read as a banner-and-block crowd more than as soldiers. The gold/orange blocks are close to the English gold. Fix: make the Scots all blue/white, with the tartan/gold limited to banners. The saltires carry the read, so this is optional.
3. **g0-30, non-blocking.** A large ochre-yellow meadow dominates the loop, with a yellow cast over the lower frame. It is set colour and the conform pulls yellows back, so it is not a fail. If the set can be changed, make the meadow green-straw.
4. **g0-80, non-blocking.** The pine crown hides the crest top where the Scots stand at g60-80, so the line is read from the saltires only. Fix: thin the pines on the crest on the camera side. A2 sees the same crag, so tell team 5 to match it.
5. **Join note (info).** A2 (team 5) starts at P_A (40, 10, 95 -> 150, 140, 20, 22 mm) at g80, and must keep the velocity of the g81-83 handles, not a fresh ease-in.
