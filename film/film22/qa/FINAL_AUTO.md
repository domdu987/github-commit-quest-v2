# Film 22 final automatic checks (film-13 workflow: free scripts only; client decision 2026-11-21)
release22/circuit_v1.mp4: 63.0 s, 720x1280, 30 fps, 41.0 MB (crf 21)
- Takes: 15/15 PASSED (film22/qa/sNN/PASSED): ground_check22 PASS on all 15; qa_jitter per take, BIGZOOM/fast-travel flags explained there.
- s03: frames g196-222 (shaft flooded red) bridged by a dissolve g195->g223 in conform22.
- Audio: integrated -12.5 LUFS, peak -1.1 dBFS. Music: the client's Suno "The Curious Commuter" at -31 dB under the voice, faded to 63.0 s. SFX: 41 cues from the reused library (fal was locked when the library was built).
- Intelligibility (local faster-whisper small, Thai): final mix 0.878 vs clean narration 0.881 (the mix costs nothing).
- qa_jitter on the final film: median 0.36 px; seconds over 2 px: 3 s (2.5, s02 rise), 11 s (2.7, s04 travel), 49 s (2.9, s12 ride), 60 s (5.1, s15 dive through the window) - all planned eased camera travel, no shake effect used.
- COLOUR_SPEC (hue_report, 1 fps, whole film, after grade22): red 35.8, orange 24.3, blue 22.8, violet 5.2, magenta 1.5 %; sat 0.41; val 0.52; dark 0.13. All in band except violet (+0.2 over 5 %).
- qa_stats2: 2 detected cuts (travel joins make the film read as continuous camera moves), sat 0.386, luma 103.8.
