# ไม้จิ้มฟ้า (The Sky-Poker), Brescia 1769: final release

- `sky_poker_v3.mp4`: 65.6 s, 720x1280, 30 fps. Thai narration (voice Bankky via fal.ai ElevenLabs v3, expressive, priest lines in character voice), Thai captions (Kanit Black), Suno music "Curious Little Creatures" at -31 dB RMS, 142 sound effects, voice at -14.4 dB RMS (measured from the reference clips).
- `cover_a.jpg`: vertical cover (frame g 1323, the bolt hitting the spire).

Rebuild: takes come from branches render/team1..5 (film/v3/film2/sNN/take.mkv) plus s01 frames; `conform_full.py <takes_root> <out>` joins them with dissolves, then
`NARR=narration_v3.wav NARR_DB=-17.8 FRAMES=<out>_frames MUSIC=music_suno.wav MUSIC_DB=-31 python3 conform.py 1968 <out> takes/s*/cues.json`.
