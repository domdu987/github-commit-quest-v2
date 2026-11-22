# Film 18 v2: client fixes (2026-11-22). The client: "มุมกล้องของลอย" / "มุมกล้องมันสั่น" -> "แก้ได้เลย"

Re-render ONLY these shots. Narration, music, captions and every other take stay exactly as in v1.
Tools (pull branch claude/new-session-73ou27, or film18/main where they are copied):
- film/v3/tools/ground_check.py: run on EVERY re-rendered take, after your shot script builds the scene. Example: `python3 -c "exec(open('shot.py').read()); import sys; sys.argv=['x','--every','5','--out','GROUND.md']; exec(open('PROJ/v3/tools/ground_check.py').read()); run_cli()"`, or the blender -b form in its header. It must exit 0.
  - Thrown or flying props (pots, helmets, cups in the air) and flags on poles: tag obj["airborne"]=True, or use airborne_frames.
  - Give every card a contact shadow (add_contact_shadow).
- film/qa_jitter.py take.mkv: every second must print NO "shake" line, i.e. median jitter <= 2 px. The only exception is ONE planned shake of 0.6 s or less at an ox impact. Mark it in QA.md.

Camera rules for every re-rendered shot:
- NO sway, NO handheld noise, NO per-frame random offsets. Use one smooth eased (smoothstep) dolly and/or truck. A held punch-in is allowed only if it is eased over 6 frames or more.
- Character bounce (laughing or cheering) at most 0.02 D, at 2 Hz or slower. Fast crowds jitter the frame-diff, so keep crowd motion gentle.
- Keep frame-diff median >= 4 (eased dolly plus parallax). p90 is now only a note.
- Set scene.cycles.transparent_max_bounces = 64.

Start each shot from the script of its PASSED take, the commit listed below: `git checkout <commit> -- film/v3/film18/<shot>`. Push the new take to your own render branch, in the same folder.

| shot | v1 time | fix | base (team, commit) |
|---|---|---|---|
| s03 | 5.2-9.9 | flat discs and flags hover over the field (0:06). Ground or remove them; poles must stand on the ground | team2 f0aa6b46f |
| s05 | 12.8-15.3 | camera shake 0:13-0:15. Smooth the move | team1 ddea3b2a2 |
| s06 | 15.3-17.7 | camera shake 0:15-0:17. Smooth the move | team1 c9258d107 |
| s11 | 28.4-31.5 | soldiers behind the pots have no feet or ground (0:29). Plant them, add contact shadows | team3 6a77db2ff |
| s13 | 33.4-35.7 | shake 0:33-0:35 (worst, 7 px) | team4 647aae125 |
| s14 | 35.7-37.9 | shake 0:35-0:37 | team4 4191aac81 |
| s15 | 37.9-40.2 | shake 0:37-0:39 | team4 d7f8c8b3c |
| s19 | 47.6-50.5 | shake 0:48-0:50 (keep the planned whip at the end) | team5 9897eb4a |
| s20 | 50.5-53.2 | ox shadow detached from the ox, bundles hanging in the air (0:51.5). Shadow under the hooves, bundles tied to the tail | team5 9897eb4a |
| s21 | 53.2-56.1 | black silhouettes stand on nothing (0:54), plus shake. Put them on the ground with contact shadows | team3 8ccfd7ff8 |
| s22 | 56.1-58.0 | shake 0:56-0:57 | team4 c31713cbd |
| s23 | 58.0-60.2 | shake 0:57-0:60 | team5 688a39e3 |
| s24 | 60.2-62.7 | shake 0:60-0:62. One <= 0.6 s impact shake allowed | team4 945fa615c |

Teams: team 4 = s11 s13 s14 s15 s21 s22 s24 (yan_camp). team 5 = s03 s05 s06 s19 s20 s23 (vista, jimo_in, jimo_out).
QA.md for each take must contain: the ground_check result (exit code and summary), the qa_jitter output, and frame-diff. The director grades at conform with COLOUR_SPEC v1.1.
