# s13 QA: film 20, shot 13 (2.5 million rivets) -- SITE site_rivet, DAY, stage 1
## Delivered
- take.mkv g 903..948, 46 frames (g 907..944 = shot 13, 4-frame handles each side, both cuts), first_g 903, 16.0 MB, 720x1280, 8 spp.
- s/frame: wall 22.5 (two processes), cpu 25.9. Frame-diff in-shot (g 907..944): **median 6.82, p90 10.34** (target 4 / 12: median met, p90 misses by 1.7).
- qa_auto PASS (cut notes only: the cuts are at the take edges / handles).
## On screen
Deck of the first platform at 17 m: the thrower (riveter_tongs) holds the tongs with a glowing rivet, flings it g 911-921 (set hook rivet_toss, drawn x3.2 so it reads, about 12 px+), the catcher (riveter_hammer) at the catch mark flinches then cheers with both arms up after the catch (g 923+), the hammerer (riveter_forge) swings the hammer every 9 frames with sparks (spark hook, strength 1.5, hits g 913/922/931/940). Camera: close-medium (5.8 m), push 7 %/s + slide + snap x1.5 on the catch (g 920-933), lifted 1.3 D so the deck rail stays below the faces.
## Checked
- Heads 56-190 px wide, centres y 510-710, bottoms < 880. Feet stand on the real plank surface (ground_z: 0.28 D above the mark z: QA gotcha 4). No mouth animation, no DOF, no text.
- Preset FG hidden (anchored to the preset camera); the deck rail of the camera scaffold stays as natural foreground.
## Deviations
- The bucket is the set's bucket beside the thrower; the catcher stands near it and the rivet flies to his chest, he does not hold the bucket.
- p90 10.34 < 12. The hammerer is partly behind the forge shed.
