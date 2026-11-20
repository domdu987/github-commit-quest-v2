# QA-tech sE1 (team7 2bcd73a)

**Verdict: FAIL** (1 blocking issue: the opening beat is not readable). Everything else passes. g790-885, 96 frames, 720x1280.

Method: frames every 5th (f6), full-size ffmpeg extracts of g790-794, 833-843, 848, a gray frame-diff on all 96 frames, and a crop-diff on the Scots.

## Beat by beat
| Beat (plan row E1) | g | Result |
|---|---|---|
| Laughing soldiers on the bank point across | 790-797 | FAIL. The soldiers are 4 small figures in the top third (heads about 6 % of frame height). The bottom 60 % is empty yellow ground and grass. The camera leaves them by about g797. Only g793-796 are non-handle frames, and the first 3 are dissolve-covered. The laugh drawing and bounce read, but pointing across is not readable. |
| One mimes hoeing | 790-797 | FAIL. Not discernible at phone size, and no time to see it. |
| Camera rises, flies over river and up the hill | 797-834 | PASS. Clear eased flight over river, loop meadow, bridge and Abbey Craig. Parallax and the sun shafts read well. Diffs 16-31 (blur flag is the planned swoop). |
| SNAP punch-in on 27.80 (g837), 6 frames of speed lines, 2-frame shake | 835-843 | PASS. The jump is at g834-836 (diff 49 at g835). Speed lines are on g837-842. Shake is visible. Lands about g843. The snap peaks about on the narration word. |
| Scots line, Wallace unbothered, eyebrow | 843-885 | PASS, weak. Five Scots in blue, with Wallace in the middle (long hair, beard, grey mail, green kilt) and identifiable. Eyes are half-lidded and calm. The eyebrow raise from g848 is only a small lopsided shift and does not read at phone size. |

## Checks
- **Final-hold motion:** the last 50 frames (g836-885) have median diff 8.1. The only low frames are g844-846 (<2.2) and g882-885 (<2.9), about 3-4 frames each. No near-static hold over 1 s. Scots crop-diff 6-18, so the Scots are always moving. PASS.
- **Spear pole:** the pole runs through the right third from g841 on. At g841-846 it overlaps the edge of the right-most Scot's face (x 560-600) and his shoulder. After about g860 it clears the face. Non-blocking, see issue 2.
- **Character size:** Wallace head about 12 % of frame height, readable by hair and beard. PASS. The Scots are small at the end, and the faces carry little detail.
- **Head position:** Scots heads at y about 560-660, above y 880. Bank soldiers' heads about y 290-350. PASS. No face over 35 %. No one floats, with contact shadows and rocks under the Scots. Nobody is cut by the frame edge, but the right-most Scot is partly hidden by the pole.
- **Colour story:** English crimson and gold only, Scots saltire blue tunics, saltire flags visible on the hill. The loop meadow g810-830 is a strong orange-yellow set colour, but no neon, no red or lime tiles. PASS (the grade is normalised at the conform).
- **Mouths:** the English laugh drawing is open throughout, with no lip-sync. The Scots' mouths are closed. PASS.
- **Always acting:** the English bounce, and the Scots sway, blink and shift. PASS.
- **D6 handles g790-792:** the dissolve is continuous. g790-792 are the same bank framing, backing out (diff 7.5-8.1), and g793 is the P_BANK pose with no pop (diff 15 at the start of the rise). Soldiers' positions match g793. PASS. Nothing in D (a previous segment) was available to compare, so the continuity of the shared pose is by meta.json only.
- **Bloodless:** PASS.

## Issues
1. **BLOCKING, g790-797. The opening beat (laughing soldiers pointing across, one hoeing) is invisible.**
   - Soldiers are about 6 % of frame height at the top of the frame, hold for only about 4 frames after the dissolve, and the lower 60 % of the frame is empty ground.
   - Fix: re-stage the bank crew bigger, so they fill the middle third at about 12-15 % head height and sit lower in the frame. Add 1-2 more soldiers if possible.
   - Hold P_BANK about 10-12 frames (about g793-805), a slow drift only. Start the rise about g803 and keep the flight and the snap landing at g837 by shortening the early flight, or shift the flight a little.
   - Make the pointing arm and the hoe pantomime large and distinct. Add a few props to the foreground ground (crates, tent rope, barrels) so there is no empty plane.
2. Non-blocking, g841-860. The spear pole overlaps the right-most Scot's face and shoulder. Move the foreground pole 0.3-0.5 m to the right or left (out of the face) or fade it out at g841-860.
3. Non-blocking, g848-885. Wallace's eyebrow raise is subtle. Exaggerate the brow (higher, tilted) and add a 2-3 frame hold so it reads at phone size.
4. Non-blocking, g843-885. The final slide is slow at the ends (diff under 3 at g844-846 and g882-885) and fine overall. An easing change would add a small push: 6-10 % over the hold.
5. Non-blocking, g810-830. The loop meadow is intensely yellow-orange. Normalisation at the conform should pull it back. Re-check at the conform stage.
