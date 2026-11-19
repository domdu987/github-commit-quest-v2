# s29 QA: film 16, shot 29 (CHAMBER chamber_table, DAY)
## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps, 45.0 MB: under the 45 MB limit, not split): first_g 1886, 103 frames (g 1886..1988). Shot 29 = g 1895..1979 (63.17-66.01 s); 9 handle frames each side in 3D. Transition in: hard cut.
- 720x1280, 6 spp, 2 threads x 2 processes: **9.6 s/frame wall, 18.73 s CPU**. QA_AUTO.md PASS (its "planned cut has no visible change" note is the handle: the cut is made in the conform).
## Shot
| g | beat |
|---|---|
| 1895-1929 | wide two-shot from the front: the postmaster mocker (left, proud, sash) and the clerk (right) either side of the instrument; camera drifts with slide + arc |
| 1930-1950 | the clerk, bent forward, slides the instrument across the baize toward the mocker (1.0 D, eased, lever follows) |
| 1951-1953 | blink; **1952** pose swap proud -> HORROR (hands to the cheeks, ring eyes, sweat drop, trembling squash) |
| 1952-1965 | **SNAP** (14 f, peak 1.7) swings the camera round to the mocker's face, "ความดูแลของเขา" (65.11 s = g 1956) |
| 1966-1979 | close on the horrified face (head 255 px) with a slow push; instrument beside him |
## Checks
- Mouths: nobody speaks; the horror mouth is a held expression mouth.
- Heads: mocker 70 -> 255 px, centre y 610-630, bottom <= 747 (< 880). The clerk leaves the frame to the right at the end of the swing (not visible as a head).
- Instrument slide: the set's instrument is part of the table mesh; it is cut out at runtime (bmesh) and rebuilt as its own objects. Checked on the contact sheet (g 1913-1961): no ghost copy left on the table; the lever knob moves with it.
- No text, no DOF. Contact decals on.
## Frame-diff (90x160 grey, pairs g 1895..1979)
median **4.0**, p90 **18.68** (targets >= 4 / >= 12). The median is just at the target: the first second is a wide, quiet two-shot; the snap gives the p90.
## Differs from the plan / notes
- The set's instrument (3x scale, 3.5 D tall) hides anyone standing behind the table from a front camera, so the two actors stand at the table's ends beside it and the first half is a wide (heads 65-100 px, below the 110-135 wide size). The horror close-up (255 px) is reached by the snap with an explicit swing pose.
- The instrument slides along the table (clerk to mocker) rather than toward the lens.
- The clerk's hands are not pinned to the instrument: the pushing pose is a pose swap on the slide start.

---
# Revision 2 (after the director's TAKE gate) -- re-rendered, take.mkv (split in two parts)
Frame-diff now median 4.15 / p90 18.89 (minimum pair 3.16: never parked); 103 frames, 9.52 s/frame; heads 82-269 px.
- **Gate 1 (camera parked g 1966-1988): fixed.** After the snap the camera keeps pushing (16 %/s of the framing) and trucks sideways 0.55 D/s until the cut: the smallest in-shot frame-diff pair is 3.16 (it was ~0 for 23 frames).
- **Note 2 (wide opening, slide illegible): partly.** The opening is still a wide two-shot (heads 82-95 px) because the instrument is 3 D tall; the actors now stand at the table ends, the instrument slides 1.1 D toward the mocker over g 1930-1950 (eased) and both are in frame throughout the slide. A closer opening was not possible without losing the clerk.
- The mocker's horror close-up is 255-269 px.
