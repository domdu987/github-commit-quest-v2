# Film 12: "ไอ้ร่มเดินได้" (Jonas Hanway's umbrella, London 1750s)
True core: from the early 1750s Jonas Hanway carried an umbrella in London for about 30 years; hackney coachmen jeered and threw rubbish because umbrellas threatened their rainy-day fares; umbrellas were for a time called "Hanways". The head coachman is a composite mocker (series convention).
Formula: hook (hated for an umbrella) / pivot / mocker bet (pink lace umbrella of his wife) / nickname / count (yr1 veg, yr2 eggs, yr3 mud splash) / false payoff (10 yrs, still alone) / reveal (rain = coachmen's richest day; umbrella = walk home free) / aha (men follow one by one; "Hanway") / ending (coachman under his wife's pink lace umbrella on an empty coach).
Blind test: v1 7/10 -> 3 rewrites -> retest hook 8/10, all beats read; 2 word fixes applied.
Narration: Bankky, speed 1.15, original setting, atempo 1.134, 59.0 s, per-sentence STT >= 0.97 (s07 0.83 only because STT writes "Hanway" in Latin letters; audibly correct).
Set: NEW set v3/set3d12 (rainy Georgian street + coach rank). Cast: v3/cast12.

## Suno (music)
Styles: playful baroque chamber comedy, pizzicato strings, harpsichord, sneaky bassoon, light tuba bounce, sly 3/4 waltz feel, rainy-street mischief, warm and whimsical, slow build to a cheeky finish, 100 bpm, instrumental underscore
Exclude styles: vocals, choir, heavy drums, EDM, trap, rock guitar, epic orchestral, sad piano, lo-fi
Settings: Instrumental ON, Weirdness 35 %, Style influence 70 %, length over 60 s.

## Sound / conform (prepared 2026-11-18)
SFX library film12/audio/sfx (14 files, fal ElevenLabs sound-effects v2, ~58 s generated, est. US$0.10-0.15), cues in film12/audio/sfx_cues.json.
Conform: `python3 film/conform12.py --name film12_v1 <take folders>` -> film/release12/<name>.mp4 + report (LUFS target -12, TP <= -1). Test on 4 passed takes: 1785 frames, -12.2 LUFS, -1.4 dBTP, Thai captions OK. Music: waiting for the client's Suno track (film12/audio/music_suno.wav).
