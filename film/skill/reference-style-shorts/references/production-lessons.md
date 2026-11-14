# Production lessons, films 2-9 (Thai client, Ricks-Clips-style shorts)

Everything here came from the client's own reactions while making nine films. Treat the "client taste" rules as hard rules for this
client, and as strong defaults for new clients until they say otherwise.

## 1. Story formula — measured on 8 hit shorts (9-33M views)
Analysis lives in the repo at film/analysis/ (per-clip breakdowns, transcripts, 1 fps sheets, DIRECTOR_REVIEW.md).
Common to ALL 8: 45-65 s, ~220 words (~210 wpm, no pauses); first sentence <=3-5 s states a strange act or contradiction with NO reason;
one "You see," pivot; reason withheld until 65-85 % of the runtime; countable escalation (15 min -> 20 min -> door breaks); reveal =
ONE visual mechanism; last line = twist or ironic payoff, then a hard cut on the last word (no outro, no CTA); one narrator who voices
the characters in quotes; flat 2D puppets in a lit 3D world; camera never static (new framing every 1.5-2.3 s); 1-3 word captions.
7 of 8: a mocker who doubts or laughs at the hero (and usually gets comeuppance), text on props carries plot.
What the top-viewed titles share: concrete visual object + counter-intuitive claim ("Why perfect railroads don't work"); low performers
were explainers ("How painkillers work") or hypotheticals.
Our working template (scored by a blind Sonnet tester before recording):
hook (strange act) / pivot "คืออย่างนี้นะ" + era / mocker quote (+ promise he will regret, e.g. "ถ้าเอ็งทำได้ ข้าจะซื้อหมด") /
nickname "ไอ้..." / countable escalation / false payoff (hero seems to lose) / crisis / one-image reveal / aha / ending = the mocker's
own words come back at him. Length 58-70 s is fine; the client explicitly said longer is OK.
Always run a blind tester (Sonnet) on the script, apply its 3 rewrites, re-test once.

## 2. Client taste (hard rules)
- SHARP picture. No depth-of-field blur at all (the client rejected it; the references are sharp too — verify at full res, never claim
  "the reference blurs").
- Prefers the ORIGINAL look of films 6/7: wide and medium framings that show a beautiful dense set, calm but always-moving camera.
  A remake with extreme close-ups, many text signs and a flat blue 2D infographic reveal was REJECTED ("วิดีโอเดิมดีกว่า").
- Reveals must be shown inside the lit 3D world (a torn loaf with droplets in the bakery light; mortar macro between real bricks), never
  as a flat 2D diagram. Thai text rendered into the picture broke into black blobs once — avoid in-picture Thai text unless verified.
- Captions: Kanit Black ~88 px, one phrase at a time, centred at y 900 of 1280 (the one-word small style was rejected).
- Voice: ElevenLabs v3 voice "Bankky" (RwilAvCC3o05RLuACpAn) via fal.ai, speed 1.15, default stability, English bracket tags
  ([mysterious, playful], [deep, mocking character voice], [laughs]), assembled with atempo ~1.134. The client tried Gemini (Fenrir,
  Charon) and an expressive Bankky (stability 0) and went back to this original setting.
- Music: the client makes it in Suno. Give him Styles + Exclude styles text, Instrumental on, Weirdness ~35 %, Style influence ~65-75 %,
  length > film. Mix music at -31 dB RMS under voice at -14.4 dB.
- Never cut scenes silently. When shortening, list what disappears and ask; prefer faster cutting over dropping scenes.
- ASK BEFORE RENDERING: show the set contact sheet and get an explicit OK before launching render teams. Do not start on your own.
- Comic falls only, no injury; birds/animals stay visibly where the story says (bird inside the cage).

## 3. Production system that worked
- Script -> narration (per sentence, STT-verified ≥0.97 per line, rerecord failures) -> captions.json/timing.json -> shot plan with
  sentence-anchored times -> set + cast builders (Opus subagents, in parallel) -> contact sheet -> CLIENT OK -> worked-example take s01
  (Opus subagent) -> 5-7 render teams (cloud sessions via create_session, branch renderN/teamK, clone_depth 1) -> conform_full ->
  conformN.py (captions + SFX + mix) -> QA -> release.
- Worker briefs: film/WORKER.md + film/WORKERn.md per film (set API, cast API, worked example + gotchas, client rules, take contract:
  meta.json g0/g1/first_g/n_frames/transition_in dict, 6 handle frames, take.mkv split with `split -b 40M` above 45 MB).
- Teams sometimes stall (background launcher deadlocks, idle sessions): schedule a check with send_later, look at status_detail,
  nudge with send_message. Normalise transition_in strings to dicts before conform.
- Re-cutting existing footage to a new narration is cheap and keeps the look (edit6e.py / edit7e.py style EDL: per sentence a list of
  source frame ranges, proportionally trimmed; last segment keeps its end).
- Lip-sync check after a re-cut: compute which source frame is on screen when the new quote starts vs where the old quote began;
  shift the source range if the offset > 0.3 s.
- SFX: generate a per-film library with fal ElevenLabs sound-effects v2, place cues by sentence time, and duck SFX overlapping speech
  (-6 dB short, -3 dB beds, extra -4 dB on laughs/gasps/crowds).
- Disk is small (~10 GB free): delete decoded frames (takes*/frames, deliver/*_frames) of finished films; keep take.mkv.

## 4. Picture-QA team (film/QA_TEAM.md)
QA-tech (Sonnet): strict checklist per take/sheet (blur, heads above y 880, clipping, floating feet, black/frozen frames, pops, Thai text,
continuity, mouths only on quotes, plan coverage) -> PASS/FAIL with frame numbers.
QA-art (Opus): scores density, light/colour, composition, acting, key-moment clarity vs references and the client taste -> SHIP/FIX-FIRST.
Gates: SET (before any render, then show the client) -> TAKE (each delivered take) -> FINAL (before sending).
Automated final checks: frozen/black frame scan; per-sentence STT on the final mix vs clean narration (mix must not be worse by >5 %).

## 5. Session hygiene
Finished render teams can be archived (read-only, transcripts kept, unarchive possible; all work is on their git branches and the
releases on the main branch in film/release*). Never touch sessions you did not create.
