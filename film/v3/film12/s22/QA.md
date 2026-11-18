# QA s22 (film 12, ending: shots 22-23), g 1573-1784 (212 frames; in-handle 1573-1578; no out-handle, end of film) -- re-render after director gate
Render: RAIN, 720x1280, OIDN; shot 22 at 24 samples (~48 s/frame), shot 23 at 20 samples (~27 s/frame), 2 threads.
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg), magenta 0.0 %. The auto detector misses the cut at g 1656 (similar palette); checked by eye: clear cut, and now a different
  angle/height/lens (shot 22 low and far, lens 32; shot 23 closer, 24 mm, from higher), so it is no longer a jump-zoom.
- Gate fixes: (1) shot 23: the coachman's own fist grips the pole (sprite prop kept, sprite canopy clipped away above the hat, the 3D pink umbrella continues from the pole,
  pole foot computed from the card anchors every frame). (2) shot 23: whole canopy incl. right tips inside the frame through g 1784 (about 30 px margin), lamp post
  fully inside, head y 559->557 (0.43 H). (3) shot 23: the empty cab (windows, no passengers) shows at left; box lanterns hidden (no black boxes); camera raised so the horse
  is only in the bottom ~20 % right. (4) shot 22: custom camera low on the left kerb, lens 32, push (-3.6,-3,2.5)->(-3.2,2.5,2.5): a row of 3-4 coaches, set_rank_busy(0)
  (dark lanterns, hanging horse heads side-on and inside the frame), cobble foreground cut to about a third, coachmen a/b/c glum.
- Heads px y: shot 22 box_a 467->407, box_b 569->561, box_c 611->615 (all < 880; box_a ~0.32-0.36 H at the end of the push, wide shot, exempt); shot 23 box_a ~0.43 H.
- Mouths still, no text, no floating feet (cards stand on the box plank), rain continuous, gentle breathing sway on the cards.
- Not fixed / known: tiny pink frill fragments of the sprite canopy remain just above the hat in shot 23; horse faceting; canopy reads salmon-pink (not retinted, to keep
  magenta share low); shot 22 fine puddle grain reduced (24 samples) but not zero; no contact-shadow rework under the boots (set card shadows as in the approved set).
- Framing change: shot 22 one 2.6 s push, shot 23 one 4.3 s push; no extra in-shot cut (plan).
