# QA sD1 (film 21, plan v3): g 542-642, CUT in, whip right out
- World camp_table (K.build_world), lantern, KING'S TREASURY sign on the chest, light shafts, 32 samples, 720x1280. Cressingham (one card, contact shadow, gold rim via K.with_rim) behind the table.
- Camera: one continuous arc round the table (az -112 to -48 deg, radius 2.6 to 1.9 m), a director-noted extra push-in of 0.5 m during the laugh (from g 606), whip right in the last 6 frames (g 636-642, horizontal motion blur).
- Acting: counts coins (coin hand bobbing, lean and head sway, blinks) -> looks up across the river (g 603-611) -> bursts out laughing at narration 20.29 (g 612): fixed laugh drawing, bounce, tears, NO lip-sync (no speak() call in this segment). Head about 160 px tall at the end (director note: >= 120-140), scale pan stays off his face.
- Colour (qa_stats2): saturation 0.627, vivid 71.8 %, luma 107.6. The raw grade for camp_table came out at luma 120.7, so a uniform gamma 1.19 x 1.05 post-correction was applied to all 101 frames (sat 0.563 -> 0.627). Same factor on every frame, no flicker.
- Rhythm (film21/rhythm.py): median in-shot diff 6.94, p90 16.88 (needs >= 4 / >= 12). Still frames 0 %.
- qa_auto: ONE FAIL, "suspected blur" on g 637-642: this is the planned whip pan (intentional motion blur, 6 frames, plan D1 -> D2 whip). The "pops" at g 637-641 are the same frames. Nothing else flagged; magenta 0 %.
- Not covered: the lower part of the frame in the first 40 frames is table underside and grass (planks), accepted as foreground layer.
