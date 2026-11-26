export const meta = {
  name: 'dz09-ep1-hook-final-render',
  description: 'Final 720x1280 render of the EP.1 hook, conform and independent review',
  phases: [
    { title: 'Render', detail: 'S01 touch-up, then all 1280 frames at final tier' },
    { title: 'Conform', detail: 'final film with icons, captions, sound' },
    { title: 'Review', detail: 'independent strict review and repair' },
  ],
}
const P = '/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09'
const COMMON = `Project root ${P}. DEAD ZONE 09, Thai zombie series, EP.1 hook film (53.32 s, 24 fps, 1280 frames, 9:16). Read ${P}/v10/film/README.md first (especially the "Draft v3" section: per-shot PCT table, auto PPD, levels, finish.py, known weak points), ${P}/v11/set/API.md, ${P}/v13/icons/API.md, ${P}/v8/cast/API.md. bpy 5.3 Cycles CPU, 4 cores. Never call paid APIs or any network service; no AI image generation. Kill every process you start before returning. Look at your own output frames at full size and report honestly what is still weak; say what you did not check.
USER DECISIONS (latest win): (1) icons are the FLAT v13 status strip, top-left, horizontal, no shadows, no depth. (2) Narration voice is Ohm, mix ${P}/audio/narr_ohm/mix_ohm_v2.wav; narration must stay clearly above effects. (3) Light rain: post levels RAIN=0.2, SPLASH=0.25, HAZE=0.3, TILT=0, DOF=0.25, BLOOM=0.55 are the defaults already; picture must be crisp. (4) Line art of the characters must be crisp in the video: honour the per-shot PCT table (100 % render scale on character shots), no blur on cast, encode CRF 15 tune animation. (5) Characters stay flat, upright, camera-facing 2.5D puppets matching ${P}/uploads/character_sheet.webp.
The draft (${P}/v10/film/draft_v3.mp4, draft_v3_sheet.png, v3_stills_720.png) was checked by the director and approved for final render.`

phase('Render')
const render = await agent(`${COMMON}

YOUR JOB (you own ${P}/v10/film):
A. Bounded touch-up of S01 first (at most about 30 minutes; stop and keep the current version if it does not clearly improve): the hand holding the radio is box geometry and reads as a stack of blocks; make it read as the puppet's gloved hand holding a handheld radio (flat drawn card in the cast's style is fine), and after the push-in (frames 54-80) Kong's face must not sit inside the icon strip box (top-left, y about 8-19 % of height, x up to about 80 % of width): lower the framing a little. Check with final-tier stills (run.py --frames). Change nothing else in the shot scripts unless something is broken.
B. Render the whole film at final tier, 720x1280, into ${P}/v10/film/out/final_720x1280 (move every older frame and stills folder there into a backup folder first so nothing stale is reused). Use 4 workers x 1 thread (python3 run.py --all --tier final --size 720x1280 --threads 1 --worker i/4, per-shot PCT as defined in the shot modules, do not pass --pct), started with nohup in the background with logs in ${P}/v10/film/logs; the runner is resumable, restart a worker that dies. Expect about 20 CPU hours (about 5 h wall): wait with background-safe polling (an until-loop on the frame count, each wait call under 10 minutes) and do not return until all 1280 frames exist. While waiting, spot-check a frame from each shot as it completes (sharp line art, light rain, face colour stable, puppets flat and upright, nothing broken); if a shot is wrong, fix the shot script and re-render only that shot. Do not edit finish.py or cues.py unless broken.
Return: frame count, total CPU hours, wall time, what you changed in S01, per-shot problems found and fixed, anything still wrong.`, { label: 'render:final', phase: 'Render' })

phase('Conform')
const conform = await agent(`${COMMON}

Render report: ${render}

YOUR JOB: conform the final film from ${P}/v10/film/out/final_720x1280 with finish.py exactly as draft v3 was conformed (shot joins, flashes, v13 icon strip composited last, Ohm captions from captions_ohm.ass, title plate, Ohm mix at the same static gain; CRF 15, preset slow, tune animation, yuv420p, AAC 320k, faststart, 24 fps, 53.32 s). Output ${P}/v10/film/DZ09_EP1_hook_916_v1.mp4, ${P}/v10/film/final_sheet.png (3 frames per shot + title, like the draft sheet) and ${P}/v10/film/final_stills.png (8 strongest frames at full 720x1280, 2 rows x 4). Verify: frame count 1280, duration, audio/video sync (narration offset 0.30 s), loudness and true peak, no missing or black frames (scan mean luma per frame), file size. Return files, measurements, problems.`, { label: 'conform', phase: 'Conform' })

phase('Review')
const review = await agent(`${COMMON}

Conform report: ${conform}

YOUR JOB: independent strict review of ${P}/v10/film/DZ09_EP1_hook_916_v1.mp4 as the user will see it on a phone, then repair. You own ${P}/v10/film. Extract a frame every 0.25 s and look at all of them in contact sheets at readable size; measure consecutive-frame differences per shot for flicker or pops, and check cuts. Check: line art crisp, rain light yet wet night; icons flat, readable, correct at each cue, never on a principal's face or a caption; lip sync follows the Ohm voice (compare mouth-open frames with the narration envelope); characters flat, upright, sheet-accurate; continuity between shots (who stands where, cutter, battery LEDs); captions correct Thai and in sync; title hit at 50.72. Fix real defects by re-rendering only the affected frames at final tier and re-conforming to the same file names (keep a copy of the pre-repair film as DZ09_EP1_hook_916_v1_prerepair.mp4). Keep repairs bounded to about 1.5 hours of rendering. Return: defects found, fixes made, an honest prioritised list of what still falls short of a professional result, and what you could not check (you cannot hear audio; say so).`, { label: 'review:final', phase: 'Review' })
return { render, conform, review }