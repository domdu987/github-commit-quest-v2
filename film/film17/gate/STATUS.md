# Film 17 TAKE gate status
| take | team | status | approved commit | notes |
|---|---|---|---|---|
| s01 | 1 | **PASS** (QA-art R3 SHIP; QA-tech R2 blockers hand + post-whip caliper verified fixed) | render17/team1 d6ecda5 | rhythm 8.96/17.84; minor: brow bar g70-90, coat hem, beard seam |
| s02 | 2 | PASS R3 (QA-tech; 3 should-fix accepted: no hand sprite on blue cuff, edge object, tight push) | c2c810e (USE THIS) | gate/s02/QA_TECH_R3.md |
| s03 | 3 | **PASS** R2 (QA-tech; 5 should-fix accepted: jagged book outline, hand gap early, fg pile edge) | 3fcb09e (USE THIS) | gate/s03/QA_TECH_R2.md |
| s04 | 4 | **PASS** R4 (QA-tech + director look; ear tap reads; should-fix accepted: glove edge clip from g624, gentle taps) | 68d44d5 (USE THIS) | gate/s04/QA_TECH_R4.md |
| s05 | 2 (from 5) | **PASS** R2 (QA-tech + director look; should-fix accepted: edge crop, blown chandelier g685-715, hood cloth) | e553276 (USE THIS) | gate/s05/QA_TECH_R2.md |
| s06 | 5 | **PASS** R2 (QA-tech; should-fix accepted: glove size, weak exit, double-hand g760/772) | 6fe61b4 (USE THIS) | gate/s06/QA_TECH_R2.md |
| s07 | 1 (from 6) | **PASS** R5 (QA-tech + director look; should-fix accepted: faint wall moire, empty table, slab at lower right g1034-51) | f528820 (USE THIS) | gate/s07/QA_TECH_R5.md |
| s08 | 7 | **PASS** R3 (QA-art R2 PASS + QA-tech R3 PASS + director look) | 5866892 (USE THIS) | gate/s08/QA_TECH_R3.md, QA_ART_R2.md |
| s09 | 8 | **PASS** R4 (QA-tech; 3 cosmetic should-fix accepted: edge touches, coat notch) | 084ef5b (USE THIS) | gate/s09/QA_TECH_R4.md |
| s10 | 9 | **PASS** R5 (QA-tech R4 PASS + QA-art R5 PASS; R5 changed only g1406-19 and card post) | 669e44b (USE THIS) | gate/s10/QA_TECH_R4.md, QA_ART_R5.md |
| s11 | 10 | **PASS** R3 (QA-art R2 PASS + QA-tech R3 PASS; should-fix accepted: eye pop g1607 reads as a 'caught' take, chair post, weak fist) | 55446ee (USE THIS) | gate/s11/QA_TECH_R3.md, QA_ART_R2.md |
| s12 | 11 | **PASS** R3 (QA-tech; chins measured all frames, cards 55-72 px) | 3c91397 (USE THIS) | gate/s12/QA_TECH_R3.md |
| s13 | 12 | **PASS** (shot 33 redo after FINAL QA-art; FINAL QA-art R2 SHIP) | 2345bc4 (USE THIS) | FINAL_QA_ART_R2.md |

## FINAL gate (2026-11-20)
| reviewer | result | file |
|---|---|---|
| script checks (qa_auto full cut) | PASS (0 black/frozen/magenta; flagged pops = planned inner cuts) | FINAL_QA_AUTO.md |
| audio | R1 FAIL (caption sync 34/102) -> captions retimed from STT -> R2 PASS: STT 0.995-1.000, -12.2 LUFS, TP -1.5 dBTP, captions 0/102 off (max 0.05 s), SFX >=16 dB under voice | FINAL_AUDIO.md, FINAL_AUDIO_R2.md |
| QA-art | R1 FIX-FIRST (shot 33 hand) -> s13 2345bc4 -> R2 SHIP, overall 8 | FINAL_QA_ART.md, FINAL_QA_ART_R2.md |
| blind viewer | PASS (hook, mocker, mechanism, ending all correct) | FINAL_BLIND.md |
Rhythm full film: in-shot median 6.22 / p90 14.35 (film 2: 5.11 / 18.65; floor 4 / 12). No director overrides.
