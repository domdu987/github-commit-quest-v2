# QA s19 (render team 5, film 18) round 12 - frames g1427-1514 (+6 handles: take.mkv g1421-1520, 100 frames), jimo_out NIGHT
Frame-diff in-shot (n=87): median **11.49**, p90 **14.38**. qa_auto "blur" g1505+ = whip landing (director: false positive).
- Mouths (round 11 measurement, unchanged camera / herd): worst y 858 at g1485.
- Flame vs face on RENDERED frames, looked at g1436, g1458 and g1484 (phone-size crops): the flame tongues sit to the right of / above the faces with a visible gap (roughly 20-60 px) and none touches a face, horn or blade. I did NOT run an automatic pixel test, and I did not offset individual oxen: my box estimate cannot separate the cases (it reports overlap on every frame whatever the spacing, 8 seeds tried), so I kept the herd as is. g1452-1466 other than g1458 were not individually checked.
- Ground (`J.ground_share`): 0.17 / 0.20 / 0.16 / 0.23 / 0.17 at g1430 / 1450 / 1470 / 1490 / 1500 (g1450 was 0.32; two pots added, two removed where they blocked the oxen).
- Pots now read terracotta: two warm point lights (650 W) near them. One pot still covers the lower right edge of an ox at g1484.
