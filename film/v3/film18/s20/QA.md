# QA s20 (render team 5, film 18) round 7 - frames g1515-1595 (+6 handles: take.mkv g1509-1601, 93 frames), jimo_out NIGHT
Frame-diff in-shot (n=80): median **4.03**, p90 **6.70**. qa_auto PASS.
- Lead ox in pure profile at about 40 % of frame height, running screen-left, `face='rage'` (all charging oxen use it); head at x 0.25-0.35, its flame trailing at x 0.8-0.95 (still near the right edge on some frames).
- Tripod brazier on the ox's back: raycast at g1589 hit `halos`, `wood`, `posts` (road tripods at x 9.5). Their flames, halo quads and mesh faces in the field are removed at runtime.
- Camera pitched down (look z 0.1), eased push, no wobble; sky about 30 %.
- NOT fixed: bare ground still about 45 % of the frame: the lane next to the low camera. The set's v2 dressing and `R2.dress` put (almost) nothing there and my own soft dark bush sprites did not render; no Qi silhouettes were added in the lower third.
