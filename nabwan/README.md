# นับวัน reel source

Source for the นับวัน story reels. Quality rules live in `../CLAUDE.md`; read them first.

To work, copy this folder to a scratch directory, set up a Python venv (numpy, soundfile, faster-whisper), and
regenerate media. Narration (`storyN/vo/*.wav`), music (`storyN/music/*`) and renders are not in git: the voice
request bodies (`req_*.json`) and placement scripts (`placeN.py`) are here, so takes can be regenerated.

| path | what |
|---|---|
| `demo/engine.js`, `demo/fx.js`, `demo/render.js` | frame engine (layers, springs, captions), deterministic Playwright renderer |
| `story2/puppet2.js` | chibi character rig (pose / reach / blink) |
| `pro/pro.js` | lighting and camera: rim + shade, cast shadows, AO, light pools / shafts, bokeh, shot lists, depth of field |
| `story8/props8.js` | room props (night window, fairy lights, plants, shelves, posters, cork board, clock, cat, fan, lucky cat…) |
| `story11/rain11.js` | rain kit: streaks, splashes, puddles, drips, lens drops, umbrella, rain-shadow mask, wet patch, wet-ground reflections |
| `storyN/` | one reel: `charsN.js`, `setsN.js`, `iconsN.js`, `scenes.js`, `vo.js`, `index.html`, `audio.py` |
| `cover/` | cover frame grabber + cover template + shooter |
| `brand/brand.js` | end-card brand chip |
| `scripts/` | transcription, contact-sheet grid, analysis helpers |
| `deliver/แคปชั่น-ทุกคลิป.txt` | every post caption |

Stories: 2 = 75 วันของพ่อ · 3 = 1,095 ข้อความของแม่ · 4 = 47 ครั้งที่ลบข้อความ · 5 = 127 ใบสมัคร ·
6 = 4,380 วันที่รอ · 7 = 11 ปีที่เพื่อนไม่เคยลืม · 8 = 312 ชามที่ไม่มีผักชี · 9 = 39 บาทที่แม่ไม่กล้ากด ·
10 = 52 ปีกับกระทงสองใบ · 11 = 12 ฤดูฝน ที่ไหล่ของพ่อเปียก.

Render: `cd demo && PAGE=../storyN/index.html node render.js video ../storyN/out/video.mp4 30 [t0 tEnd]`
(`tEnd` is an end time). Stills: `node render.js stills <dir> t1 t2 …`. Mix: `python storyN/audio.py storyN/segments.json storyN/music/<file> storyN/out/mix`.
