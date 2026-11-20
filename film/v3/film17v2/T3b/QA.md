# T3b QA (g751-856, 106 frames, 720x1280, take.mkv crf14 7 MB)

Setup: T3 69c6528, clear_cast() per frame, ramp + gain 1.05. Changes vs first delivery (TAKE-gate fixes): gasolier raised GAS_DZ 0.6 (T3 ec3f44d), lights x0.8 over g825-835 held to g856. Chair CHAIR_D (-0.4,0) / PRIS_D (-0.15,0) as before.

## Numbers (RGB mean, 90x160 bilinear)
- part mean 118.1, min 103.0 (g804), max 148.6 (g856 handle). g751-850: mean 116.4, max 140.2.
- g751 117.2, g755 118.3, g770 121.8, g800 111.0, g816 105.4, g830 118.0, g845 129.7, g849 138.2.
- g835-849: 122-138, still above 118. Director chose x0.8 plus conform trim 0.85 (brightness is the yellow wall's albedo).
- Black fraction (max RGB < 8): 0 on all 106 frames. qa_auto PASS, no leak slabs.

## Viewed
- Full size: g761 (and g755/g845 test stills earlier at the same settings).
- Phone-size strip (360x640): g751, g755, g816, g845, g849, g856.
- g755/g761: gasolier clear of the green gendarme's face. The lamps now cover part of the SERVICE D'IDENTIFICATION sign (and the end of ARCHIVES at g755); accepted by the director.
- g816: sitter seated, no bar on his face (phone size).
- Not viewed: other frames, only contact.jpg thumbnails. Accepted as before: g775 OTS partial, g781-796 post, g786-791 Bertillon edge, g818-826 pan exits.
- OIDN shimmer on flat walls not measured.
