# QA_TECH s05 (take g376-458 = 8 handle + 75 in-shot, 83 frames) - FAIL
Checked: 6 fps frames (g376,377,378,381,386,391,...) + first/last 3, framediff re-measured (in-shot g384-458, 74 pairs): median 3.95, p90 10.64 (min 1.25, max 15.20). Rule median>=4 FAIL (3.95), p90>=12 FAIL. Caption band y880-950 mean max 58.3, bright 0.00 %.
## Issues
1. whole shot - camera: median 3.95 < 4 and p90 10.64 < 12. g455-456 diff < 1.5 (near static at the end). Fix: stronger push/slide so median >= 4 and p90 >= 12.
2. g376-458 - mandatory "sky <= 30 %": the sky gradient takes ~35 % of the frame at g376-391 (y 0-~450) and still ~25-30 % later, with flat cream sun and cloud stickers (brown bars, a sun disc clipped at the left edge x=0 from g376 on). Fix: tilt down further or fill the top with set; drop the sticker clouds/sun.
3. g376-458 - plan beat "townsfolk hand him a general's sash": nobody hands anything. He holds a red sash/vest floating in front of his chest with a smirk; the woman behind the counter only watches; the old man is hidden. The red object has no visible hand contact from a giver and is not "across the counter". Fix: show a townsperson's hand passing the sash over the counter, then Tian Dan takes it; keep both in frame.
4. g446-458 - clipped junk: a large dark brown triangular wedge (awning/roof corner of a foreground prop) enters from the right edge, covers the woman's face from g446 and grows to ~25 % of the frame width at g458. Fix: reroute the camera slide or hide the prop.
5. g376-458 - composition: the bottom ~35 % (y 880-1280) is bare dusk ground; the fg prop (stand + crate at the lower right) is a flat dark navy shape clipped by the right edge. Fix: dense fg (counting board, slips, jars) in the lower third.
6. g376-458 - eye-line: Tian Dan smirks at the lens; he does not look at the sash or the giver.
## Pass items
Tian Dan in front of the counter (mandatory item met); DUSK matches the plan; no oxen (nothing to be plain); heads < 880 (chin max ~y 560); no mouths move; no text; feet have a faint contact shadow; no black/magenta/blur frames; g range 384-458 matches the plan; 8 handle frames g376-383 for the 11-frame dissolve present.
