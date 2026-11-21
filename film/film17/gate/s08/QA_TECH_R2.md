# QA_TECH s08 ROUND 2 (shots 20-21, g1039-1201) - VERDICT: FAIL (1 blocking, several should-fix)
Reviewed: all 38 f6 frames (sheets), full-size crops g1039/1064/1094/1130/1134/1139/1144/1149/1159/1169/1179/1184/1189/1194/1199, phone sheet, cut strip 1124-1130. qa_auto PASS (cut 1127 is visibly a hard cut, confirmed by eye). rhythm 4.77/12.49 OK. No blank/black/magenta frames, no visible blur, no dust/beam shafts on characters, no see-through cards. Not measured numerically: Laplacian blur (cv2 not installed), per-frame freeze.

## Round-1 items
1. Inspector front/unobstructed/centred: FIXED (largest, frontmost, g1139-1199). Mouth open "o" and moves g1130-1194; closed at 1199. In window.
2. Gendarme mouths closed: FIXED (smirk/sneer, no open mouths g1130-1199).
3. Shot 21 opening tiny: PARTLY. g1130 inspector head ~79 px; grows to ~146 by 1141 as claimed (head ~150 px at g1139). Faces still small on 1128-1134 but legible after ~1139.
4. Shot 20 cards: PARTLY. Bertillon is mildly slumped (head tilt, half-lidded eyes) but the two cards stay at chest/side height in the same pose in g1039/1064/1094 - no eye-level flip, no clear head-shake read. Claim "cards flipped at eye level" NOT verified.
5. Drawers/candle: drawers - several jammed protruding drawers, book stack, spilled cards on desk (g1069-1109), good. Floating quill/ray removed (OK). Stub candle NOT visible at all (only the cyan lamp); "candle low" unmet.
6. Pull-out shrink: FIXED (he stays large; g1119-1126 head ~150 px).
7. Ring-like prop: STILL PRESENT. A small ring/loop hangs under the right card in every shot 21 frame (g1139-1199, ~y 1020-1040, x 270-300 at 720 width). Reads as stray geometry.
8. Cards vanishing at cut: FIXED (cards in hand g1130+).

## Blocking
B1. Shot 21 (g1130-1199): Bertillon's cards have no hands - both cards hover at chest with no visible fingers/arms, and one carries the ring. Props must be held by hands. In shot 20 only the right card has a hand (left card tucked on chest, acceptable). Fix: show the hand on both cards or drop to one card, delete the ring.

## Should-fix
S1. Inspector eyes/head face the camera, not Bertillon (pupils frontal g1139-1199); "turned toward Bertillon" claim NOT verified. Pupils toward Bertillon (camera-left).
S2. Hands: both of his arms are bent behind/at the head like a stretch (g1139-1149, 1169); no clearly cupped hand beside the mouth, and the "pointing from g1172" is not visible (g1179 arm is out at the side, hand tiny, not aimed at Bertillon). Lean on stress is only a weak torso tilt. Claims partly unverified.
S3. Bertillon's flinch g1130-1138 is not readable (same face/pose as g1139); slump is mild. Add a head drop ~10 deg on 1130.
S4. Right gendarme holds a grey drawer-like box at his belly (g1130-1199) with no clear grip; reads as stray geometry/floating prop.
S5. Shot 20: no candle; cards not flipped/compared with clear change.
S6. Smirk reads as sneer (team-known); no entrance walk (accepted).
Heads: all chins < y 880 (Bertillon ~800 max, inspector ~780). Hold: no >1 s frozen seen by eye.
