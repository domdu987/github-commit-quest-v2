# QA s01 (plan shot 1, hook), round 2 after QA-art FIX-FIRST — g 0..62 + out-handle 63..68
- qa_auto: PASS (69 frames). QA_AUTO.md, phone_sheet.jpg, contact.jpg.
- Fixes: lift 0.40 -> 0.95 (flash-forward) so a full-width dark gap with glowing cribbing and jacks sits under the ground floor; old stair hidden (cannot reach the door); camera crane DOWN (1.9 -> 0.55 D) + tilt up, so the facade rises against the static foreground crib pier; people moved to the flanks / foreground (nobody covers the foundation line); mud ~20 %; dust motes 0.2-0.5 D, brighter, 70 of them along the foundation edge.
- Limit: the set's lift is 3.6 D max, i.e. ~15 px/D at the framing that fits the whole hotel, so the facade climb is ~50-60 px against the pier (crane + lift), not 100.
- Heads: chin (head centre + radius) max 873 px; mouths none; no DOF/text.

## Round 3 (QA-tech + client notes)
- Three workers now act at the jacks in the gap (worker_turn_bar A/B alternating every 6 frames, bars hidden in 3D); old stair hidden; puddle/scum hidden (no smeared reflection); crates + barrels in the foreground so the bottom of the frame is sharp detail; dust is 11 thin falling streams of tan grains (no round white blobs).
- Nothing stands on the hotel (nobody on the stair/portico/windows), so no parenting needed.
- Chin line: all heads < 880 except the smallest worker (wc) by up to 4 px at g 40-68 (head-centre + radius estimate).
- Cut convention left as delivered (round(t*30)), the conform handles the +3 offset via handles.

## Round 4 (QA r2 blocking items)
- Lift now starts at h 0.62 (dark void with lit cribbing visible from frame 0) and climbs to 1.00; dust grains are dark brown thin streaks (<= 3 px wide), no white/round blobs; spare-jack props on the left crib pile (the lamp-like object) and the puddles hidden; workers at the jacks turn bars (A/B cycle).
