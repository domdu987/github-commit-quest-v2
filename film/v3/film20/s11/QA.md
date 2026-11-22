# T11 / s11 v2 (client rejection of rivet_v1: floating, shake, too close)
Changes: re-rendered the whole take, same g0/g1/first_g, handles 8/8 and transitions unchanged (meta.json).
- Ghost glass overlay on the left (camera-parented timber post `fg_post_s11`) removed.
- Camera rebuilt: no snaps, no shake, no hand-held noise. Slow eased Catmull-Rom drifts, lens pulled back 25-50 % wider (ground, base, crane read),
  fence part cranes up 1.8 m. Two short eased flights (g797-813, g887-901) join the set locations; one smooth crane-up g945-1003.
- Stage 1 pops in at g805 behind flight 1 (was 830). Speed lines / punch-in shake removed.
- Cards bounce 0.015 D (was 0.10: they left the ground); ground_check PASS (GROUND.md). Cards keep their contact shadows.
- qa_auto PASS (QA_AUTO.md; sharpen post extended to g797-1003). qa_stats: sat 0.542, luma 102.3.
- Frame-diff median 2.15 / p90 17.9 (below the old 4.0 target: intended, calm camera).

qa_jitter (take.mkv): no second above 2.0 px; overall median jitter 0.32 px.

## v2b (director's float-hunter item, g813-873)
The carried beam was drawn behind both workers' heads at cap height. It is now carried at hip/hand height (z 0.74 D) and IN FRONT of both cards (y -0.22 D toward the camera), so it reads as held in their hands and covers no face. Re-rendered g805-880 only; the rest of the take is untouched (same camera, same frames). qa_auto PASS, qa_jitter overall median 0.32 px, no second above 2.0 px, frame-diff median 2.17 / p90 17.85.
