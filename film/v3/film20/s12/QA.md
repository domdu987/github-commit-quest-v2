# s12 QA: film 20, shot 12 (18,000 pieces of iron) -- SITE site_girders, DAY, stage 1
## Delivered
- take.mkv g 818..910, 93 frames (g 822..906 = shot 12, 4-frame handles each side for the two hard cuts), first_g 818, ~30 MB (not split), 720x1280, 8 spp. s/frame wall ~15.6 (two processes), cpu ~30.
- **qa_stats: `saturation 0.532, brightness 105.1, in-shot motion median 3.94 p90 8.78`**: colour met (sat >= 0.47, luma 85-110); **motion misses**: median 3.94 (just under 4), p90 8.78 (< 12). deliver.py method gives about 4.5 / 8.8. A x1.30 exposure trim in deliver.py lifts the dark raw frames into the luma band.
- qa_auto PASS.
## On screen
Camera at 1.0 m, 7.8 m south of the 3 m high red-lead girder stack, trucking along it at 160 px/s (orbit 6 deg/s, hand-held jitter, small snap x1.12 on "เหล็ก 18,000", g 854-870); two workers (riveter_tongs, riveter_hammer; walk cycle, same pace as the camera) carry a 4.6 m I-girder on their shoulders along the stack 4.4 m from the lens; the derrick's hanging girder (set hook crane_swing, 0 -> 1) swings into frame top-right after g 870; the set bucket is the foreground prop that passes at the bottom (g 870-895).
## Checked
- Heads 74-104 px, centres y 650-725, bottoms < 880; neither carrier is cut by the frame edge (checked probe at 818/850/880/906); feet on the ground with contact decals (ground z 0 verified with ray cast). No mouth animation, no DOF, no text.
- The stack fills the middle band; the lower third is dark gravel ground with the bucket foreground (about 30 %).
## Deviations
- Frame-diff misses the target (above). An earlier take of this shot dipped into a dark neighbouring pile (a black slab through the middle): fixed by starting the truck 3.5 m further left.
- The carried girder is a flat grey-brown beam over their shoulders (runtime box geometry); the lady-style hand-on-shoulder pose is approximated by raised arms. The Eiffel Tower is not in frame (the derrick and stack are the subject; the stage-1 platform appears only in the first tests).
