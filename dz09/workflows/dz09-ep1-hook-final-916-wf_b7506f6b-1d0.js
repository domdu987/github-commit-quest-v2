export const meta = {
  name: 'dz09-ep1-hook-final-916',
  description: 'Integrate flat icons + Ohm narration + lighter rain, draft v3, then final 720x1280 render, conform and review',
  phases: [
    { title: 'Integrate', detail: 'icons v13, Ohm audio and lip sync, rain levels, shot fixes, draft v3' },
    { title: 'Render', detail: 'all 1280 frames at final tier 720x1280' },
    { title: 'Conform', detail: 'final film with icons, captions, sound' },
    { title: 'Review', detail: 'independent strict review and repair' },
  ],
}
const P = '/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09'
const COMMON = `Project root ${P}. DEAD ZONE 09, Thai zombie series, EP.1 hook film (53.32 s, 24 fps, 1280 frames, 9:16). Read ${P}/v10/film/README.md first (shot scripts, runner, finish, draft v2 and its review notes), ${P}/v11/set/API.md (set + post, section "v12 clarity levels"), ${P}/v13/icons/API.md (the flat icon strip the user approved), ${P}/v8/cast/API.md. bpy 5.3 Cycles CPU, 4 cores. Never call paid APIs or any network service; no AI image generation. Kill every process you start before returning. Look at your own output frames at full size and report honestly what is still weak; say what you did not check.
USER DECISIONS (latest win): (1) icons are the FLAT v13 status strip, top-left, horizontal, no shadows, no depth; the glossy v12 tube gauges and the phone-voice badge are rejected and must not appear. (2) Narration voice is Ohm: audio ${P}/audio/narr_ohm/mix_ohm_v2.wav (final mix, narration starts 0.30 s in), dry narration ${P}/audio/narr_ohm/narr_final.wav, captions ${P}/audio/narr_ohm/captions_timing.json (film time = caption time + 0.30 s; sentence starts are identical to the old narr_v1 timeline, word times inside sentences differ by up to about 0.3 s). (3) Rain must be lighter still, the user said rain still hides the scene: use post levels RAIN=0.2, SPLASH=0.25, HAZE=0.3, TILT=0, DOF=0.25, BLOOM=0.55 as the new defaults (keep the review's per-shot blur fixes for S01 and S09; wet road, puddles and reflections stay). The picture must be crisp. (4) Characters stay flat, upright, camera-facing 2.5D puppets matching ${P}/uploads/character_sheet.webp.`

phase('Integrate')
const integ = await agent(`${COMMON}

YOUR JOB (you own ${P}/v10/film, and may set the new level defaults in ${P}/v11/set/post11.py; do not edit v13/icons except to fix a bug you can prove):
1. Make the lip sync and all narration-driven timing use the Ohm narration: rebuild the mouth envelope in common.py from narr_ohm/narr_final.wav (+0.30 s), captions from narr_ohm/captions_timing.json, and check every cue in cues.py / shots/base.py that is tied to a spoken word against the Ohm captions (picture cues: battery 16.30/16.50/16.70, radio cut 3.243, hang-up 31.75, red eye 41.657, lunge 43.445, scream 43.795, title hit 50.72 stay).
2. Wire v13 icons into finish.py following v13/icons/API.md (overlay after all blur, DZ09 narration source = narr_ohm); remove v12 gauges, old icons and the voice badge; keep the title plate but use the flat v13 biohazard mark handover if the API describes it; use mix_ohm_v2.wav normalised to about -14 LUFS, true peak <= -1 dBTP, without changing the balance.
3. Set the new rain/clarity levels as defaults.
4. Shot fixes (verify each with final-tier stills via run.py --at): S06 Kong's face must be serious and determined, not smirking; S06/S07 bring the young crew member back, standing clearly to the side (not behind Kong); S23 the green delivery box in the foreground covers too much of the lower right: lower or shrink it; S22 and S24 use the scream mouth for the bitten junior; faces must not flicker: remove the glittery wet-speckle patch on faces and limit how far the beacon flash swings face colour (faces keep their sheet skin colour, with at most a mild cool/warm tint); S01: ground the radio (a hand or a dashboard/vest mount, so it does not float) and keep the background legible; S20: make the driver larger in frame (his head at least a third of frame width at the red-eye moment) while keeping the over-the-shoulder; S12: nothing may collide with the icon strip area (top-left, y about 8-19 % of height, x up to about 80 % of width): where a principal's FACE would enter that area, lower the framing a little.
5. Without re-rendering the whole film, conform ${P}/v10/film/draft_v3.mp4 at 720x1280 from the existing draft frames in out/draft_360x640 (re-render at draft tier only the shots you changed in step 4, with the new levels), with the v13 icons, Ohm captions and Ohm mix, plus ${P}/v10/film/draft_v3_sheet.png. This draft is for the user to check timing, icons and voice, so make it as soon as steps 1-3 are done and refresh it after step 4.
6. Render ${P}/v10/film/v3_stills_720.png: final tier 720x1280 stills of S01, S06, S13, S18, S20, S23 with icons and captions (2 rows x 3).
Update README. Return: what changed, files, anything that blocks the final render, CPU s per final frame, weak points.`, { label: 'integrate', phase: 'Integrate' })

phase('Render')
const render = await agent(`${COMMON}

Integration report: ${integ}

YOUR JOB: render the whole film at final tier, 720x1280, into ${P}/v10/film/out/final_720x1280 (move any older frames there into a backup folder first so nothing stale is reused). Use 4 workers x 1 thread (python3 run.py --all --tier final --size 720x1280 --threads 1 --worker i/4), started with nohup in the background with logs in ${P}/v10/film/logs; the runner is resumable, so if a worker dies restart it. Expect about 13 CPU hours (3.5-4 h wall): wait with long background-safe polling (an until-loop on the frame count, checked every few minutes, each wait call under 10 minutes), and do not return until all 1280 frames exist. While waiting, spot-check a frame from each shot as it completes (sharpness, rain level light, no flicker artefacts on faces, puppets flat and upright, nothing broken); if a shot is wrong, fix the shot script (you own ${P}/v10/film) and re-render only that shot. Do not edit finish.py or cues.py unless broken. Return: frame count, total CPU hours, wall time, per-shot problems found and fixed, anything still wrong.`, { label: 'render:final', phase: 'Render' })

phase('Conform')
const conform = await agent(`${COMMON}

Render report: ${render}

YOUR JOB: conform the final film from ${P}/v10/film/out/final_720x1280 with finish.py: shot joins, flashes, v13 icon strip, Ohm captions (Kanit Black, as in the draft), title plate, Ohm mix. Output ${P}/v10/film/DZ09_EP1_hook_916_v1.mp4 (H.264 high, yuv420p, CRF about 16, 24 fps, AAC 192k, faststart, 53.32 s), ${P}/v10/film/final_sheet.png (3 frames per shot + title, like the draft sheet) and ${P}/v10/film/final_stills.png (8 strongest frames at full 720x1280, 2 rows x 4). Verify: frame count 1280, duration, audio/video sync (narration offset 0.30 s), loudness about -14 LUFS, captions never overlapped by icons, no missing or black frames (scan mean luma per frame), no v12 gauges. Return files, measurements, problems.`, { label: 'conform', phase: 'Conform' })

phase('Review')
const review = await agent(`${COMMON}

Conform report: ${conform}

YOUR JOB: independent strict review of ${P}/v10/film/DZ09_EP1_hook_916_v1.mp4 as the user will see it on a phone, then repair. You own ${P}/v10/film. Extract a frame every 0.25 s and look at all of them in contact sheets at readable size; also check consecutive-frame differences per shot for flicker or pops (measure), and difference spikes at cuts. Check: picture crisp and rain light (not veiled) yet wet night; icons flat, readable, correct at each cue, never on a face or caption; lip sync follows the Ohm voice (compare mouth-open frames with the narration envelope); characters flat, upright, sheet-accurate costume colours; continuity between shots (who stands where, door open/closed, cutter in hands, battery LEDs); captions correct Thai and in sync; title hit at 50.72. Fix real defects by re-rendering only the affected frames at final tier and re-conforming to the same file names. Return: defects found, fixes made, and an honest prioritised list of what still falls short of a professional result, plus what you could not check (you cannot hear audio; say so).`, { label: 'review:final', phase: 'Review' })
return { integ, render, conform, review }