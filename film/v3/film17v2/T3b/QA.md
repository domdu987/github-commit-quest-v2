# T3b QA (g751-856, 106 frames, 720x1280, take.mkv crf14 7 MB)

Setup: T3 69c6528 setup, clear_cast() before each stage_cast2, ramp + gain 1.05 applied. Only change vs T3: CHAIR_D (-0.4,0), PRIS_D (-0.15,0) (post / head-rest bar fix).

## Numbers (RGB mean, 90x160 bilinear)
- part mean 118.8, min 102.6 (g804), max 153.7 (g856, handle). g751-850: mean 116.9, max 145.2.
- g751 116.6, g770 119.3, g800 111.1, g830 121.0. Above the 95-110 target; director trims at conform.
- Black fraction (max RGB < 8): 0 on all 106 frames. No leak slabs.
- qa_auto PASS, 0 cuts detected, magenta 0 %.

## Viewed at full size
g793, g775, g816, g822 (full size); g751, g850 (phone-size strip 360x640 only, with g775/793/816/822 also there).
- g816: head-rest bar not over the face; armrest rail in front of his chest; reads seated.
- g822: post at the sitter's left, face clear.
- g793: face about 70 % visible, partly behind the purple post at right edge (accepted per brief).
- g775: sitter partly cut by the left edge, an accepted OTS partial.
- g818-826: accepted pan exits at the left edge.
- Not viewed: other frames, only contact.jpg thumbnails.

Residual: OIDN shimmer on flat walls not measured.
