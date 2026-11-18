# QA s21 (shot 21, barn_milking / A, g 1232..1301, take g 1226..1307)
Own check at 6 fps (contact.jpg, every 5th frame), full-size stills during the build and first / last frames (hard cuts in and out; handles are the same push in 3D):
- Heads: all chins above y 880 (max chin y 640, the cow's head at g 1226); Sarah's head 106 -> 170 px.
- Milking: Blossom (mirrored, faces screen-left) and Sarah (sarah_milk, mirrored) are placed from the cow's anchors: Sarah's feet sit on `milker_feet` (moved 1.25 D along the view ray so she stands in front of the set's pail), hands antiphase +-0.06 at the teats height; the 3D pail of the set is under the udder; the set's own stool is left of her.
- Blossom: chews every frame (chew = g / 12), ear flick every 66 frames, tail swish; set hooks (hens, lanterns, motes) alive.
- Sarah's face clear and smooth, smiling; no sore card in this shot (James is not in it).
- Mouths: nobody speaks (smile mouth).
- Camera: slow push-in from the preset barn_milking camera, looking a little lower (look z 0.95 -> 0.75) so the group sits at 0.40-0.45 H and less roof shows.
- Deviation: the second milkmaid is not in this shot (plan names Sarah only); the cow faces screen-left as the set's stand-point note says, so the puppet pair is mirrored.
- Note: the lower 40 % of the first frames is straw floor with hens / pails (the set's near dressing), the group stays in the upper half.
- Colour (own measure, tools/hue_report + dairy_hue.shade_hue, every 10th frame): shade hue 241.2-243.6 (band 240-260); magenta share max 10.5 % (g 1252 10.5, g 1262 10.2: 0.2-0.5 points above the 10 % limit on a stretch of about 15 frames, all other frames <= 9.5 %). Per-shot light override in shot.py: DAIRY_P lift (0.007, 0.020, 0.042) instead of the preset (0.007, 0.020, 0.036): the preset view measured shade hue 236-239 (below 240) on this camera.
