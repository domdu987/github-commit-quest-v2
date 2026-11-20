# QA.md: film 17 v2, T2b (T2, g494-657, 164 frames), render17v2/T2b

Render: `render_T2b.py` (720x1280, 16 samples + OIDN, 2 threads, `stage_cast2` on every frame, motion blur off). Real cast17 cards only.
T2a's T2 light overrides (measure `shade_mul` 1.2, plus its corridor values) are applied, so g494 continues T2a's g493 (director's instruction).
The extra smoothstep lift g497-510 that the director allowed is wired in but set to 1.0, because the overrides alone already met the luma target.
The cast is cleared before every `stage_cast2` (c2_*, back_hair_*, back_coat_*, `actors.clear_registry()`): no leak.

## Numbers (qa_stats2 / v2_gate.stats metric: 90x160 bilinear, RGB mean)
- Luma part mean **112.0**, min 99.0, max 117.8 (takes.md target 95-110). First 30 frames: 108.1 (104.2-110.2). It runs hotter later: 110 of the 164 frames are above 110 (first at g517), and from about g560 it sits at 114-118, so the part is about 2 above the target. Left as is (director: report only, trimmed at conform).
- Saturation 0.604, vivid 75.4 %.
- `qa_auto.py` PASS (magenta 0.0 %). Its note, "planned cuts with no visible change", is expected: there is no visible cut inside this part. The film cut at g651 falls inside it, and g652-657 are the handle frames, the same shot continuing.
- `rhythm.py`: median 3.45, p90 13.77 (target >= 4 / >= 12). The median is below 4 because this is a slow push-in on a talking figure. Not changed.
- Lip-sync only on g493-651 (`talk` True for the inspector). Every other mouth is closed (cast17 story poses). The gendarmes use standing poses instead of the laughing ones because the laugh ends at g493.
- File: take.mkv 8.8 MB (no split needed).

## Frames I actually looked at
Full size (720x1280): g510, g523 (side by side), g630, g657, plus the g560 key still earlier. Phone size (360x640 tiles on contact.jpg): g494, 520, 560, 600, 630, 651, 652, 657. Mouth crops at full-res: g600, 615, 630, 645, 651, 652, 657.

| g | what I see |
|---|---|
| 494 | Low camera looking up at a saturated blue ceiling with honey beams and a gasolier. Two gendarmes at the left on books, the tripod and the seated prisoner at the right. The inspector is small and front-on with an open mouth. Floor contact is visible. |
| 510 (full) | The inspector points at the wall chart, open mouth below the moustache. The tripod is partial foreground on the right and does not cover his face. Prisoner at the left on a stool. Blue ceiling not grey. |
| 523 (full) | Same stance, bigger in frame, tripod clearer; the seated prisoner has the calipers on his head at the right edge. Mouth open. |
| 560 | Close medium. Inspector front-on, mouth open; the tripod hood is at the left edge and the OTS figure's hat edge is at the right. Neither touches his face. |
| 600 | Larger, mouth open (round shape). Face clear. Feet on the floor, shadow under him. |
| 630 (full) | Inspector centre, arm out, round open mouth under the moustache, readable at phone size. The tripod hood covers the left edge only. Cap, feet and shadow are fine. The window is bright and the sky out there is blue and yellow, not washed out. |
| 651 | Open mouth, last lip-sync frame. |
| 652, 657 (657 full) | Mouth shape is the closed `flat` shape: a thin horizontal line under the moustache. Same pose, camera still holding. 657 reads closed at full size. |

## Not done / limits
- I did not look at all 164 frames as a clip, so I have no clip-level verdict on OIDN shimmer. The 8 phone tiles and the 4 full-size frames showed no visible noise on the flat walls or ceiling.
- No thin or edge-on card seen in the frames I viewed. The OTS figure at the right edge (g560-600) is only partly in frame.
- The final stretch is brighter than the target (see above). Nothing was changed.
