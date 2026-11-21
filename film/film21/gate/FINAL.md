# Film 21 "ไอ้ชาวนาบนเนิน" — FINAL gate (film-13 QA §D, producer's hard-defects-only rule)
Release: film/release21/farmers_v1.mp4 — 61.6 s, 720x1280, 30 fps, h264 + aac, 47 MB. Hard cut on the last "ตูม".
Takes: 17 segments (film/film21/fetch_takes.sh TABLE), conform with the client's COLOUR_SPEC v1.1 grade (film/grade21.py).
Music: the client's own Suno track "The Sneaky Jig", mixed at -31 dB under the narration (ducked).

| Check | Result |
|---|---|
| 1. Script checks (qa_auto, every frame) | PASS: 1848 frames, no black/blank/magenta/frozen; the cuts land on the planned frames (verified frame diffs at g80, 642, 1044, 1640; the tool's "no change" note is a false flag); soft frames = the planned fast dive (g103-116) and whip (g637-641) |
| qa_jitter | median 0.51 px; no second over 4.0 px (the flagged seconds are smooth dives and pushes; ruled not shake at the TAKE gates) |
| 2. Audio | integrated -12.3 LUFS (band -14 to -11), true peak -1.4 dBFS (limit -1); per-sentence STT on the final mix 0.962-1.000 (all 11 >= 0.93); captions from captions.json (narration timing +0.10 s, Kanit Black 88, y 900) |
| Colour (COLOUR_SPEC v1.1) | brightness 0.53, saturation 0.44 (in band); red 15 %, dark 0.22 out of band: daylight exterior battle (see film/film21/GRADE_NOTES.md) |
| 3. QA-art (opus) | SHIP, no hard defects; scores: set 8, light/colour 7, composition 7, acting 8, hook 7, mocker 9, false payoff 8, reveal 7, ending 8, overall 8 (gate/FINAL_QA_ART.md) |
| 4. Blind viewer (sonnet) | all four answered correctly: hook (they watch and do nothing), mocker (the treasurer mocks the "farmers on the hill"), mechanism (bridge chokepoint, attack at half across, half the army trapped), ending ("fast and cheap" -> swimming back) |

Open notes (not blocking, logged): the hook dive at 3.4-4.0 s is fast and dark; the bridgehead block is small on a phone at 44-48 s; the horn at 38-41 s is small in frame; the shore shot holds near-still about 2.5 s at 57-59.5 s; a cropped dark banner edge at 35-37.6 s; flat puppet cards have no rim light; taste notes on F (pointing, Scots behind helmets in the close-up), E1 (snap size, Wallace's brow), H1 (caption-band heads at 1306-1310).
Overrides: sE2 and sJ1 by an independent Opus reviewer (§E); sF accepted under the producer's hard-defects-only rule (14:26).
