# s14 QA: film 20, shot 14 (count: floor one / two / to the top) -- SITE site_rise, DAY, stages 0 -> 1 -> 2 -> 3
## Delivered
- take.mkv g 941..999, 59 frames (g 945..995 = shot 14, 4-frame handles each side, both cuts), first_g 941, 22.7 MB, 720x1280, 8 spp.
- s/frame: wall 18.4 (two processes), cpu 19.2. Frame-diff in-shot: **median 6.37, p90 9.87** (target 4 / 12: median met, p90 misses by 2.1).
- qa_auto PASS.
## On screen
Three eased crane-up snaps (peak 1.7) on "ชั้นหนึ่ง / ชั้นสอง / จนถึงยอด" (g 948 / 967 / 981): g 943-958 (legs-only yard, low) -> first platform appears at the snap middle g 950; g 962-977 -> second platform at g 969; g 977-993 -> finished spire with the lantern at g 985; the camera ends higher each time (preset cameras site_rise_snap1/2/3). Between snaps a 5.5 %/s push + slide. A camera-parented timber post stays at the left edge as foreground.
## Checked
- The tower reads as the Eiffel Tower in every frame (legs -> first platform + arches -> second platform -> spire). Stage jumps are hidden in the snap peaks; no popping scaffolds in the stages. No actors (so no head/mouth rules); no DOF; no text.
## Deviations
- p90 10 < 12. The sky holds the upper third of g 985+ (spire still in frame). The start pose (stage 0, low) is my own: lower and closer than site_rise_snap1.
