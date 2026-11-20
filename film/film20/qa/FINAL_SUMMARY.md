# Film 20 ไอ้ช่างหมุด — FINAL gate summary (QA_TEAM §D + §F)

Release: `film/release20/rivet_v1.mp4` on film20/main (68.2 s, 720x1280 @30, h264/aac, 80.8 MB, not split). Caption: `film/release20/caption.txt`. Queue row: WAIT (client posts himself).
Final file = rc6: all 15 takes passed at the TAKE gate; s24 = round 10 (team2 8238f20); captions re-timed to the spoken phrases.

## The four reviewers
| # | Reviewer | Verdict | Key numbers | Report |
|---|---|---|---|---|
| 1 | Script/tech checks (sonnet) | PASS (BIGZOOM 2 flag resolved, see overrides) | qa_auto: 0 frozen, 0 black, 0 dropped; 5/5 planned hard cuts (g80, 1093, 1431, 1912, 1968), all dissolves clean. sat 0.565, vivid 57.4 %, luma 95.4, motion median 7.95 / p90 24.25 | FINAL_1_tech.md |
| 2 | Audio + captions (sonnet) | PASS (after the caption re-time, rc3) | STT final vs clean narration 1.000 in all 10 sentences (≥0.93); -12.6 LUFS; true peak -1.2 dBTP; SFX ≥8 dB under the voice; caption sync 0/96 over ±0.15 s (was 38/96; worst now 0.05 s); caption text == script | FINAL_2_audio.md |
| 3 | QA-art (opus) | PASS with notes | §G.4 "as vivid, wide and grounded as film 2?" YES; §I.7 "same channel as the ref shorts?" YES (vs R3/R5); all beats read in order | FINAL_3_art.md |
| 4 | Blind viewer (sonnet) | PASS | 4/4 correct: hook (hates the tower, eats on it daily), mocker = Maupassant + his vow, mechanism (antenna → army needs it → 70-year extension), ending (keeps the vow by sitting inside it) | FINAL_4_blind.md |

## Film-2 camera numbers (side by side, FINAL_1_tech.md)
| | film 2 | film 20 |
|---|---|---|
| motion median / p90 | 4.75 / 16.9 | 7.95 / 24.25 |
| moving-frame share | 78 % | 96.8 % |
| near-still frames | 10.2 % | 1.0 % |
| hard cuts | ~28 | 5 (§I: travel takes, target 4-10) |
| close-ups | n/a | 3 (§I.6 cap) |
Side-by-side vividness sheet: scratchpad final/side_by_side_film2.jpg (QA-art: YES).

## §H BIGZOOMs and angle types
- BIGZOOM 1: 5.93-10.60 s (T03, g178-317): Eiffel <5 % → ~36 % in ~3.1 s, lands on "วิศวกรไอเฟล".
- BIGZOOM 2: 57.75-61.77 s (s24, g1732-1852): Maupassant <5 % (~g1743) → ≥35 % (~g1838) in ~3.1 s, 40 % at the landing; through the clear restaurant window onto his first bite on "กินข้าวบนหอ".
- Angle types (8): high/bird's-eye, low hero, over-the-shoulder, through a foreground frame, crane up/down, side slide, whip tilt, crash pull-out.

## Overrides (§E: each with a second, independent opus reviewer)
1. s24 round 10: QA-tech "narrow FAIL" on a speed step at g1834/1835. Independent opus ruling: the zoom eases out smoothly and keeps a slow creep, a normal landing, not a defect; §H met (FINAL_1_tech.md, last section).
2. s24→s25 join: QA-tech asked for a frame match; independent opus ruling: the plain 9-frame dissolve (outside view → inside reverse angle, same head position) reads naturally (TAKE5.md).
3. s21 and s27 "suspected blur" flags from qa_auto: false positives (flat cartoon areas), judged by QA-tech and QA-art.

## Conform-side fixes
- True-peak guard (oversampled limiter, -0.6 → -1.2 dBTP).
- Sill seam paint-out under the chair (s27; s24 no longer has it).
- Captions re-timed to the spoken phrases (retime_captions.py).

## Open non-blocking notes
- Eiffel is only 1-3 px until ~6.3 s (a warm glow marks his spot).
- Petition close-up crops heads at the top (15.8-17.8 s); the vow pose holds ~4 s (19.8-23.8 s).
- "Must be demolished" is carried by narration only; "20 years pass" is shown by the change to dusk only (40.8-43.2 s).
- Tower legs look bleached at 51.2 s; the 1889 fair set is reused for the 1909/10 extension beat (55.8-57.2 s).
- BIGZOOM 2 starts on the restaurant front (a ~8x zoom), not a whole-city wide.
- Restaurant lighting differs between the window shot and the inside shots (59.8-65.8 s).
- Process note: QA-art, the blind viewer and audio judged rc2/rc3. Only s24 changed afterwards (re-checked by QA-tech, QA-art r8 and the independent opus ruling). The audio is identical.
