# Film 18 v3: client fixes after watching oxclerk_v2 (2026-11-22)

What the client said: "รั้ว ไห ลอยตามกล้อง ซ้ายๆ ไปมา คนขาไม่เดิน" ("the fences and jars float along with the camera, swaying left and right, and people's legs don't walk"). His screenshots are at 0:20 (foreground fence and spears), 0:22 (the general) and 0:36 (the foreground jar next to the general). See QA_TEAM.md §M on claude/new-session-73ou27.

## Root cause 1: foreground props stuck to the camera
The set's foreground props (lantern, wheel, spear_rack, jar, pick_baskets, reeds, counter, torch) were parented to the camera. Any prop a take parented to the camera has the same problem.

**Set fix, already on film18/main:**
- `J.attach_fg` now builds the prop FIXED IN THE WORLD at the set's shot-start pose. It parallaxes naturally as the camera moves.
- New helper `J.unparent_from_camera(cam)`: call it after your camera is posed at the take's FIRST frame. It moves every camera child to the world at its current pose.

**What every re-rendered take must do:**
1. Pull `film/v3/set3d18` from film18/main.
2. Search your shot.py and helpers for `parent = cam`, `.parent = camera`, child-of constraints, or anything that copies the camera transform. Remove each one, or call `J.unparent_from_camera(cam)` at the first frame.
3. If your camera path differs from the set's default, check that the world-fixed foreground prop still sits 1.5-3 D in front of the lens at the first frame. If it doesn't, move it in the world (`J.STATE['fg_objs']`).
4. Check: on the 6 fps strip, foreground props must move AGAINST the camera direction (parallax). They must never hold a fixed screen position while the background moves.

## Root cause 2: characters slide without walking
**The rule:** anyone who changes position on the ground must step: legs swing, at least 2 steps per metre, feet planted on each step. Use the cast walk/run gait drawings. Otherwise they stay planted.
- Idle sway is allowed only with the feet locked.
- No card may translate on the ground while showing a standing or idle drawing.

**Check:** on the 6 fps strip, every figure that moves more than 0.3 D shows alternating leg drawings.

## Root cause 3: the characters themselves (the client added "และดูตัวละคร" ("and look at the characters") with a screenshot of s05 at about 0:13; film18/qa/client_v2_characters_s05.png)
In that frame:
- **Clones:** the SAME card appears twice: two identical basket girls and two identical bearded old men, one big and one small. On a phone this reads as copy-paste.
- **Sliding:** the carriers slide with standing legs.
- **Frozen faces:** everyone wears the same fixed smile, whatever is happening.

Rules for every re-rendered take:
1. **No identical twins in one frame.** Vary each extra with a different cast member (old_man, woman, child, townsfolk variants), a different colour of robe or hat, a different pose, or a mirror plus a different prop. At most one instance of each card design per frame, except distant crowd silhouettes.
2. **Everyone acts** with a prop and an action that fits the beat. In s05: carriers walk with STEPPING legs, the elder hands the sash to Tian Dan, and a townsperson points or cheers. Faces react to the beat (surprise, laughter, worry), not one smile for everyone.
3. **Legs step** whenever a figure travels (see root cause 2).
4. **Scope:** this applies to all crowd and extra shots: s05, s06, s07 (yard), s12 (wall folk), s16 (diggers), s17, s23 (pot beaters), and the camp crowds s09, s10, s11, s13 and s24.

## Other leftovers (producer's 1 fps check)
| Time | Shot | Problem | Fix |
|---|---|---|---|
| 0:10-0:12 | s04 | Brown and white discs hover over the field: the siege tents, as in s03 | Remove them, as in s03 v2 |
| 0:31 | s11 → s12 | Ghost double exposure of giant soldier faces over the wall | Director: changed to a HARD CUT at conform (`film18/qa/transitions.json`); no re-render |
| 1:03-1:04 | s25 | Aerial flags float with no poles | Add poles that stand on the ground, or remove the flags |

## Teams (2 maximum), each auditing ALL its shots and re-rendering ONLY the affected ones
- **Team 4 (yan_camp):** s08, s09, s10, s11, s13, s14, s15, s21, s22, s24. Known: s08 spear rack (0:20-0:22), s14 jar (0:36). Plan for s15 jars and s11 too.
- **Team 5 (jimo_in, jimo_out, vista):** s01, s03, s04, s05, s06, s07, s12, s16, s17, s18, s19, s20, s23, s25, s26. Known: s04 discs, s25 flags, s05 counter, s12 wheel, s16 baskets, s17 reeds, s23 torch, and walking in s06 (Tian Dan walks house to house) and s26 (the general runs).

## Per take, in QA.md
- ground_check: exit 0.
- qa_jitter: no second above 2 px, except planned whips.
- A §M statement: "no camera-parented objects (list checked)", and "moving figures step / are planted".

Base each shot on its CURRENT PASSED take; see `film18/qa/<shot>/PASSED` for the take hash. Keep the camera moves smooth, as in v2. Encode at crf 20 or higher. The audio stays exactly as it is.
