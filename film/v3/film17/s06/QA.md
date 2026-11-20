# film17 s06 (shots 14-15, narration 24.08-28.25 s) — render team 5

take: g0 725, g1 850, first_g 719, n_frames 138 (6 handle frames each side), transition_in dissolve 11 f. 720x1280, 12 samples + OIDN denoise.
Shot 14 g719-782 records_desk / EVENING_INT; shot 15 g783-856 records_low / EVENING_INT. Hard cut at g783 (frame diff 24.5).

## Numbers
- qa_auto.py take.mkv --first_g 719 --cuts 783: PASS (QA_AUTO.md, phone_sheet.jpg). Its note "planned cut at 783 with no visible change" is wrong: the measured frame diff 782->783 is 24.5 (desk -> low aisle).
- rhythm.py (in-shot, cut excluded): median 5.64, p90 12.23 (targets >= 4 / >= 12).
- Heads: all chins < 880 (max 739); head discs inside the frame (prefect's disc overshoots the right edge by <= 3 px for g764-772, the hand and sash are fully in).

## Actions in the shot_plan rows
- Shot 14: prefect (top hat, sash) at Bertillon's desk, right arm raises to three fingers (g746-756, shape swap hidden in the snap peak), finger bobs on "สามเดือน" (g768); Bertillon writes (nib jitter), worried face after the line, blinks. Camera: slide/push, snap A g746-756 (push + slide left), snap B g770-780 (pull + slide right); green banker's lamp + a pulled drawer/stool fg.
- Shot 15: Bertillon alone under the cabinets (low angle), right hand rises to his pince-nez g802-812 (shape swap at snap 1 peak), small wobble after; snap 1 g802-812 (push in), snap 2 g828-838 (pull out + slide). Dust 0.4, light shafts hidden (director fix), mouths closed (cast17.silent on every pose).
- Not on screen: "the prefect turns away" (he is out of frame in shot 15, which is Bertillon alone per the plan).

## Self-check
Looked at the contact sheet (every 6th frame), 6 full-res frames across both shots and the cut. Bertillon's head was partly cut by the left edge in the first snap: re-framed and g746-782 re-rendered. Known: the prefect's hand is a small ball with three fingers at 1 D = 90 px head; Bertillon's pince-nez hand touches the side of the head, not the glasses bridge.
