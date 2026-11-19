# v3/acting: poses and cycles for the shot animators (build-order step 5)

Directory: `__PROJ__/v3/acting/`

| File | What |
|---|---|
| `acting.py` | the library: pure functions of time that return v2 puppet pose dicts, the new drawings (mouths, expressions, props, hat keys), narration loudness, note glyphs, flying hat, hand-sprite canvas |
| `proof.py` | `strips` (12-frame strip per function, `strips/<name>.png`), `sheet` (`sheet.jpg`), `continuity` (`continuity.json`, `continuity.txt`), `compare` (`compare.jpg`: strips beside a/t46.5, a/t16.0, b/t05.0, b/t07.0, a/t44.0, b/t44.5) |
| `test3d.py` | two cycles through the 3D stage path (Actor cards, Cycles, stub room): `test3d/frames/`, `test3d/contact.jpg`, `test3d/report.json` |

```python
import sys
sys.path.insert(0, PROJ + "/v3/acting")
import acting                       # imports v3/cast/cast_ext (8 cast members) and registers the new drawings
sys.path.insert(0, PROJ + "/v3/stage"); import actors, sprites     # AFTER acting, or in any order: same puppet module
pose = acting.boss_walk(t)          # t = seconds from the first frame of the action: t = (g - g_start) / 30
```

`puppet.py` and `cast_ext.py` are not edited. `acting` wraps `_face`, `_norm`, `_hat_newsboy`, `_hat_homburg`, `_prop` the way `cast_ext` does and extends `MOUTHS`, `EXPRESSIONS`, `PROP_TYPES`, `PROP_TIP`. Hero and boss output for existing poses is byte-identical with and without it (checked: same sha1 of the SVG).

## 1. Conventions

- Every acting function is pure: `f(t, ...) -> pose dict`. `t` is seconds from the start of THAT action (its first frame is t = 0); event times passed as arguments are on the same local clock. Faces change on whole frames (`fr(t) = round(t * 30)`), bodies are continuous in t (move on ones, eased).
- Facing: `yaw > 0` / `facing = +1` = toward screen-right (unmirrored). Use `Actor.place(flip=True)` or `pose["mirror"]` as usual.
- Extra keys, ignored by the puppet, for the shot's placement:
  - `_lift` (D): raise the card root this far above the floor (walk bob share, run flight, jump, laugh bounce).
  - `_adv` (D): forward travel since t = 0 along the facing direction (walk, run). Key `actor.place(f, start + facing_dir * _adv + up * _lift)` every frame; the planted foot then stays on the floor (measured slide 0.04 D/frame on the walk in 3D, i.e. under 2 px in a medium).
  - `_notes`: live whistle notes `[(age_s, index)]` for `note_glyphs_svg`.
  - `_tip`, `_tip_angle` (hero_redraw), `_seat` (beach_sleep): see the function.
- Expression swaps sit on the closed frame of a 3-frame blink (`blink(f, [swap - 1])`), as in film.py. A listener moves under 0.04 D. Gestures use `go(u)`: in-out with about 4 % anticipation and overshoot, 9 to 10 frames.
- Pinned props in 3D: the functions return the UNPINNED drawing (a prop type and angle). For a registered tip pass `hands={"r": {"tip": world_point, "prop": ..., "angle": ...}}` to `Actor.pose` as in film.py; the solved arm replaces the arm of the pose.

## 2. New drawings (registered on import)

| kind | names | notes |
|---|---|---|
| mouths (`pose["mouth"]`) | `whistle` (small round pucker, ink ring), `laugh_open` (wide D, upper teeth, tongue), `talk_teeth` (open oval with upper teeth), `talk_small` (small o) | drawn under the moustache; any expression |
| expressions (`pose["expr"]`) | `whistling` (eyes shut, brows up, whistle), `guffaw` (squeezed `> <` eyes, laugh_open), `cackle` (happy arcs, laugh_open), `gloat_talk` (laughing eyes, talk_teeth; the talk mouth overrides it), `sleeping` (closed eyes, tiny o mouth; add `fx zzz`), `sad_down` (steep sad brows, frown), `dazed` (small-pupil rings, dash) | discrete drawings like the 20 of the puppet |
| props (`prop_r` / `prop_l`) | `ruler` (wooden yard ruler 0.96 D, ticks, no lettering; tip = far end 0.84), `tape` (narrow paper tape / strip 0.55 D; tip 0.50), `stamp` (rubber stamp, red foot; tip = rubber face 0.21), `stub` (worn red pencil 0.26 D; tip 0.20) | pencil stub at prop scale 1; worn eraser = `{"type": "eraser", "scale": 0.6}` |
| pose keys | `hat_dx`, `hat_dy` (D), `hat_rot` (deg, about the crown), `hat_off` (bool) | hat over the eyes (sleep), brim lifting in a gust, boater pop |

Helpers: `note_glyphs_svg(pose["_notes"], mouth_anchor, facing)` (SVG fragment, puppet-local D: rising quavers, 1.1 s life, fade; pass as the sprite `overlay` callable or draw in the overlay pass; the canvas needs +1.0 D above and +0.7 D ahead, see test3d.py), `flying_hat_svg(cast, yaw)` (the hat alone for the flying-boater card), `hand_canvas(cast, pose, side)` (tight feet-relative canvas around elbow, hand and prop: the 512 px/D hand sprites of the inserts), `arm_blend(cast, a, b, u)` (continuous move between two arm specs), `blinks(t, starts)`, `fr(t)`, `go(u)`, `closed_at(t, at)`.

## 3. Narration-driven talk

```python
loud = acting.loudness(21.07, 23.13)            # narration clock (s); frame k = film frame round((21.07 + 0.1) * 30) + k
pose = acting.boss_talk(t, loud, base=lambda s: acting.boss_finger_wag(s, t0=0.9))
```
- `loudness(t0, t1)`: 33 ms RMS per frame / running median of voiced frames (1 s window); 0 = silence (under 4 % of the span's peak).
- `talk_mouth(loud)`: one drawing per frame: silent `flat`, low `talk_a`, mid `talk_teeth`, high `talk_b` (held up to 4 frames), every fourth open change round (`talk_o` / `talk_small`); a drawing holds 3 to 6 frames. Measured on the two quotes: 8.2 and 8.6 changes per second, holds 3 to 5 frames (LOOK_SPEC 5.5.5: 2 to 6 frames, about 7 per s; reference 4.9 to 9.8).
- `boss_talk(t, loud, base, accents, expr)`: eyes and brows held (`talking`, or the base's expr: `gloat_talk`/`wink` from `boss_lean_wink`), no blinks inside the line, mouth from `talk_mouth`, after the line `smirk`. `speaker_motion` adds a new head target at every accent (default every 1.25 s; pass the phrase starts of narration_timing.json): roll alternating 10 to 15 deg, 0.14 to 0.22 D sideways, small vertical, eased over 10 frames, torso at about a third. The base pose's head_roll / head_dx / head_dy / lean are added.

## 4. Function list (all return a pose dict)

Chief (`boss`):

| function | for | inputs |
|---|---|---|
| `boss_talk(t, loud, base=None, accents=None, expr="talking")` | shots 10, 18 quotes | above |
| `boss_walk(t, speed=0.75, facing=1, step=0.68, bob=0.47, sway=0.13, yaw=0.95, arms="behind", pointer=True, expr="smug", blinks_at=(), cast="boss")` | near-profile walk, any cast | one step per 0.68 s; head bob 0.47 D peak to peak (60 % knees, 40 % `_lift`; measured in 3D 0.464 D, period 20 frames); fore-aft sway 0.13 D; feet planted with `_adv`; arms `behind` (+ pointer tucked under the near arm) or `swing` |
| `boss_whistle_stroll(t, notes_at=(0.3, 0.6, 0.9), speed, facing, **walk)` | shot 17 | walk + HELD `whistling` drawing, chin up, `_notes` |
| `boss_laugh_doubled(t, t_in=0, ramp=0.33, lean=25, facing=-1, bounce_hz=4.5, slap_at=(0.5,), pull_strip_at=None)` | shot 12 far | held `guffaw`, bowed 25 deg, shaking, tears + blush, hand on belly, thigh slaps; `pull_strip_at`: draws the paper strip (tape) from the waistcoat |
| `boss_shocked(t, t_shock=0.2, before="smug", yaw=-0.45, drop_pointer_at=None, base=None, cast="boss")` | shot 25 (any cast) | swap on the closed frame at t_shock, 2-frame squash, head pops, open hands flinch up, sweat; pointer gone from drop_pointer_at |
| `boss_finger_wag(t, t0, dur=0.4, yaw, wags=3)` | 'มันไม่ขึ้น' | base for boss_talk |
| `boss_lean_wink(t, t0, wink_at, wink_len=0.15, yaw, horn=False)` | 'ทางด่วนหรอก', 'รถติดเหรอ' | lean 0.12 D + 9 deg, laughing eyes, held wink; `horn=True` squeezes a car horn |
| `boss_mock_search(t, t0, yaw)` | 'ไหนล่ะ' | hand shading the eyes, turning |
| `boss_pointer_whack(t, t_land=0.5, yaw=0.4, raise_len=0.3, target=(1.05,-0.35))` | shot 6 (two calls = the taps of 18) | raise, 3-frame whack, contact squash, rebound |
| `boss_thumb_jerk(t, t0, yaw, expr, cast)` | shots 9, 12 (any cast) | thumb back over the shoulder, held 0.8 s |
| `boss_eraser_bounce(t, yaw, hz=1.6)` | shot 10 opening | eraser tossed in the open palm, smirk |
| `boss_rub_furious(t, t0, stroke=0.33, fill_len=0.8, yaw)` | shot 11c | big strokes, anger_fill rising, steam; pin the eraser |
| `boss_frozen_purple(t, twitch_every=0.4, yaw)` | shot 11 'ลากอีก' | frozen, purple, eye twitch |
| `boss_pant(t, pants_at=(0.1,0.55), yaw, nub=True)` | shot 11d | two pants, worn eraser nub |
| `boss_stamp_thrust(t, stamp_at, tear_at, thrust_at, yaw)` | shot 14 | stamp down, tear, thrust the sheet at the lens, nod |
| `boss_read_tape(t, tear_at=0.4, yaw)` | shot 4 | reads a tape, tears it |

Hero:

| function | for | inputs |
|---|---|---|
| `hero_slumped(t, yaw=0.5, blinks_at=(0.83,), turn_hz=0.8)` | shot 17 | lean 4 deg, head down (pitch 1), `sad_down`, turning the pencil stub, breathing 0.01 D |
| `hero_sad_listener(t, yaw, blinks_at, shut=(1.48, 0.13), sweat_at)` | shot 18 near | frozen sad, eyes down, eyes shut 4 frames, sweat |
| `hero_listener(t, yaw, expr="unimpressed", blinks_at, gaze_shift=(time, before, after))` | shot 10 near, 11c | frozen, blinks, one sideways gaze shift |
| `hero_stunned(t, t_swap=0.1, close_at=0.6, from_expr, yaw)` | shot 25 near | stunned behind a blink, then eyes shut and head lowered 0.1 D |
| `hero_redraw(t, t0, swipe=8, yaw, start, end, ruler=False, stub=False)` | shots 9b, 11b, 11c | pencil tip from `start` to `end` (local) in `swipe` frames (sine), small overshoot; `_tip`, `_tip_angle` for pinning; `ruler=True` puts the ruler in the far hand along the line; `stub=True` for the pencil stub |
| `hero_ruler_rest(t, yaw, blinks_at)` | shot 11d | ruler shouldered like a rifle |
| `hero_study(t, yaw=-0.5, blinks_at)` | shot 4 | chin in hand |

Seniors (`senior_a`, `senior_b`; the laugh and nod work for every cast member):

| function | inputs |
|---|---|
| `senior_nod(t, nods_at, cast, yaw, expr="unimpressed", depth=0.6, blinks_at=())` | nod = pitch 0.6 + 0.05 D dip in 4 frames, back in 6, per time; shot 6: both at 10.80 and 11.00 |
| `senior_laugh(t, cast, yaw, phase=0, hz=3, bounce=0.06, roll=15, thumb_at=None, expr="laughing")` | held laughing drawing, head rolled 15 deg, body bouncing 0.06 D at 3 Hz (`_lift`), shoulders hunching, lean 9 to 13 deg; give the two seniors phase 0 and 0.5; `thumb_at` jerks a thumb back at the map |

Beach (`beach_man`, `beach_woman`):

| function | for | inputs |
|---|---|---|
| `beach_sleep(t, breath=1.3, facing=1, recline=42, z=True)` | shot 8 | near-profile, torso reclined 42 deg, legs out with knees up (foot targets), hands on the belly, boater over the eyes, `sleeping` + Z, chest rise every 1.3 s. Card root = the heels; `_seat` = local hip point the chair seat must carry (put the card in the side plane of the chair) |
| `beach_stretch(t, t0, facing)` | shot 16 | arms up and out, back arched, eyes shut; looks up from t0 + 0.9 |
| `beach_palm_out(t, t0, drops_at, facing, cast)` | shot 16 | flat palm at shoulder height, 1-frame dips per drop |
| `beach_shrug(t, t0, facing, cast, expr, hold=0.5)` | shot 16 | shoulders up, open hands out, head tilt |
| `beach_shade(t, t0, facing=-1, cast, stunned_at=None)` | shot 23 | shading the eyes toward the sea; stunned behind a blink |
| `beach_hold_hat(t, cast, facing, gust_at=None)` | shot 23 | far hand on the back of the brim, gust lifts the brim |
| `beach_shocked(t, t_shock, cast, facing, hat_pop=True, focus=True)` | shot 24 | shocked swap + squash + 3 frames of focus lines; the man's boater lifts 0.45 D and spins over 3 frames, then `hat_off` (hand over to `flying_hat_svg`) |
| `jump_run(t, t_jump, cast, facing, height=0.55, run_speed=3.2, hat_off=None)` | shot 24 | squash 2, leap 2, hang 2 (`_lift` 0.55 D), land 2, then the run (`_adv` from the start of the run) |
| `run_cycle(t, cast, facing, speed=3.2, step=0.34)` | shot 24 | the walk at double rate, lean 14 deg, arms pumping (far arm behind), flight `_lift` |
| `woman_peg_towel(t, peg_at=0.6, facing)` | shot 8 far | both hands up to the line, peg push |
| `woman_hand_out(t, facing)` | shot 16 far | palm held out, blink |

`acting.catalogue()` lists the demo call of each strip (name -> cast, function of t, duration).

## 5. Proof

- Strips: `strips/<name>.png`, 41 functions/variants, 12 evenly spaced frames each, rendered through `sprites.render_sprites` (Chromium) at 96 px/D on one canvas per strip, `_lift` applied, ground line drawn, frame/time and the face drawing labelled. `sheet.jpg` stacks them.
- Reference check (`compare.jpg`): the talk against a/t46.5, shocked against b/t05.0 and a/t16.0, the seniors' laugh against the guards of b/t07.0, the stroll against a/t44.0, the walk against b/t44.5. Fixed after looking: walk knees too deep (bob now 60 % knees, 40 % lift), whistle mouth read as a tongue (now a small dark pucker), arms hidden under the head in reaches (layer and targets), palm and shrug too high, hat hand across the face (far hand on the brim), laugh lean too small (9 to 13 deg + head offset), gestures that started at full speed (back_out -> `go`).
- Continuity (`python3 proof.py continuity`, every frame of every function): anchor travel per frame (head, hands, prop tips, elbows, knees, feet, hip, chest; feet-relative plus `_lift`) and the mean pixel change of consecutive 48 px/D sprites. A pop = an isolated jump (over 0.08 D and 2.2 x both neighbours), a move that starts at full speed (over 0.20 D after a step under a quarter of it), or a pixel spike (2.6 x the median and 1.8 x both neighbours); frames with a drawing swap (expr, mouth, blink, gaze, prop, hand shape, fx, hat_off) on or next to them are excluded. Result: 0 unintended pops in all 41 sequences. Flags inside planned fast actions are listed as intended in `continuity.json` (the whack, the tape tear, the rain drops on the palm, the jump scare, the steam loop; and four reviewed frame by frame: stretch, shade, peg, stamp nod).
- 3D (`test3d.py`, `test3d/contact.jpg`, `report.json`): boss_whistle_stroll (note glyphs as sprite overlay) and beach_man jump_run on Actor cards in the stub room, camera drifting with them, 24 frames at 360x640, 6 samples: 0 clipped sprites, 0 black or magenta cards, head bob 0.464 D at a 20-frame period, planted-foot slide at most 0.04 D per frame on the walk, shadows and feet on the floor, 1.36 s per frame.
