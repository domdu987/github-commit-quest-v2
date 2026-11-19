# s01 QA: film 16, shot 1 (the hook) -- LINE line_close, DAY

**This is the worked example for every film-16 render team.** Copy `c16.py` into your take folder and read its GOTCHAS first. Then use `shot.py` and `deliver.py` as templates.

## Delivered
- `frames/g_0000.png .. g_0074.png`: 75 frames, 720x1280, 7 spp (TG.FINAL_SAMPLES line), 2 threads, OIDN FAST. No captions, no audio.
- `take.mkv`: libx264rgb crf 6, 30 fps, first_g 0, 75 frames, 16.3 MB.
- Frame ranges:
  - g 0..68 = shot 1 (plan 0.00-2.31 s).
  - g 69..74 = 6-frame out-handle, rendered in 3D. The camera move and his idle continue into it.
  - There are no handle frames before g 0 (the film opens here).
- `meta.json`:
  - g0 0, g1 69 (exclusive: the hard cut to shot 2 falls at g 69), first_g 0, n_frames 75;
  - transition_in {"type":"cut","frames":0}; also transition_out, events, the camera and s/frame.
  - WORKER16.md asks for 9 handle frames a side. The director's brief for this take said 6 after and none before, and that is what is rendered.
- `cues.json`: 10 cues (film seconds). The main sound is the **glass clink at g 47** (cap). Others:
  - the sun-glint "ting" at g 24;
  - the snap whoosh at g 22-35;
  - the wire swish and tick at g 55-64.
- `contact.jpg`: 16 frames, cyan line = y 880.
- `QA_AUTO.md` (PASS) and `phone_sheet.jpg`.
- `framediff.json`: per-pair frame-diff numbers.
- Scripts:
  - `c16.py`: the film-16 helper.
  - `shot.py`: `probe`, `camreport`, `stills` and `final` (draft and final share one loop).
  - `deliver.py`: final delivery, or `deliver.py draft` to review a draft.
- `.gitignore`: keeps `raw/ frames/ work/` out of git.

## Shot (what the viewer sees)
| g | beat | caption (event g = round((t+0.10)*30)) |
|---|---|---|
| 0-21 | Morse on the leaning ladder (rung 12) holds a big inverted green bottle up over the bare top of pole 1. The coil is on his other arm and the wire runs pole 0 -> coil -> pole 2. The camera is already moving. | "ชายคนนี้เอา" -0.01 |
| 22-35 | SNAP push x2.8 + 0.8 D sideways pan (13 f, peak 1.6). Sun glint on the held bottle at g 24-31. | "คอขวดเบียร์" 0.71 = g 24 |
| 34-47 | He lowers the bottle mouth-down onto the pole top (body dips). **g 47 contact**: the set's peg1 wood + glass + star switch on, the hand-held copy switches off, and a star flare runs g 47-56. | "ไปคว่ำไว้บน" 1.57 = g 50 |
| 51-53 | Blink. The pose swaps cap -> drape on the closed frame (g 52). | |
| 52-64 | His raised hand takes the wire at the coil and flicks it up over the glass. The wire overshoots 0.42 D and settles. | |
| 65 | The set's spans 0+1 and the wrap ring (peg1_wiremat) switch on; the per-frame slack wire switches off. | |
| 66-74 | Pleased smile (behind the blink at g 65), idle sway. Hard cut at g 69; the handle continues. | |

Pole 1 changes state on the beat: bare, then bottle at g 47, then wired at g 65. All visibility keys are CONSTANT and keyed on every frame.

## Checked (all 75 frames at full size, scrubbed at 6 fps, plus g 45-50, 50-54 and 63-67 frame by frame)

### Heads and staging
- Heads are 93 -> 281 px wide; head centre y 457-583; the lowest head bottom is y 639. No head reaches the caption band (y 880).
- Below y 880 there is only the coat, the ladder rails, the pole, the trees and the wheat.
- **Contact:** he stands on the rung mark. The contact decal is off (ladder). The proxy shadow falls on the pole and rails.

### Hands, props and eye-lines
- **Hand pins:**
  - The raised hand is pinned to the bottle neck at g 0-51 (error 0).
  - It is pinned to the wire at g 52-58 (error 0).
  - At g 59-66 the flick goes beyond his reach (error 0.18-0.72 D). This is intended: the wire leaves his hand.
- **Props:** the bottle (a 3D copy of the set's own bottle) stays in the fist until contact. The coil stays on the other arm throughout, and the wire runs into it.
- **Eye-lines:**
  - g 0-51: gaze up at the bottle (determined);
  - g 52-64: up at the glass;
  - g 66 on: happy, eyes closed.

### Rules and plan
- **Mouths:** no quote in this shot. Expression mouths only, no lip-sync.
- **No DOF:** dof is off at build and before every render. **No text** anywhere.
- **Plan coverage:**
  - low angle, already moving on frame 0;
  - push + slide;
  - one eased snap on "คอขวดเบียร์";
  - the cap with a glint;
  - the wire draped over the glass;
  - ladder rails in the frame.
- **Continuity into shot 2 (line_wide DAY):**
  - the bottle stays on pole 1 and the wire is on the glass;
  - Morse ends at the ladder top, smiling;
  - shot 2 starts with him at the ladder foot (a cut, allowed).

### Automatic checks
- `qa_auto.py take.mkv --first_g 0 --cuts 69`: **PASS**. No black, blank, magenta or frozen frames; magenta 0.0 %.
- Its only note: "planned cut g 69 has no visible change". This is expected, because g 69-74 is the handle and the real cut happens in the conform.
- Sprite 'clipped' warnings: 0. Retried frames: 0.

### Colour
- `hue_report` on g 0-68 (every 3rd frame): blue 63.9 %, orange 19.1 %, magenta 0.7 %, sat 0.50, val 0.71.
- Shade is blue-violet from the set's DAY ambient. Warm sun is on the pole, the ladder and the wheat.
- `hue_report` prints "OUT: red, orange, blue, sat, val, dark" against its default reference (an older film). This is the client-approved set look, not a grade fault.

## Frame-diff (production-lessons §10)
**Method** (`deliver.py framediff`, also `c16.framediff`):
- every frame is converted to grey = mean of R, G and B, then resized to 90x160 (bilinear);
- the score is the mean absolute difference to the previous frame, in 0-255 levels;
- in-shot pairs only: g 1..68 (no handle).

| | median | p90 | min | max |
|---|---|---|---|---|
| **final s01** | **6.38** | **12.40** | 4.7 | 16.5 |
| target | >= 4 | >= 12 | | |
| film 2 (reference) | 5.3 | 19.1 | | |

The 360x640 draft gave 6.39 / 12.35, within 0.05 of the final, so **tune on drafts**.

Where the high pairs come from:
- the snap, g 27-33 (11.4-16.5);
- the cap -> drape pose swap, g 52 (15.7);
- the wire flick, g 57 (12.1).

Without the pose-swap pair the p90 would be about 12.1. Treat p90 here as just passing, not as comfortable.

How the camera got there (draft numbers):

| camera | median | p90 |
|---|---|---|
| push 8 %/s + slide 45 px/s + snap x1.35/16 f | 2.32 | 4.26 |
| + arc 9 deg/s, slide 55, snap x1.5 | 4.11 | 7.53 |
| snap x2.2/13 f with 1.3 D pan | 5.41 | 12.06 (but the frame cut his head) |
| final: slide 60, arc 14, snap x2.8/13 f, peak 1.6, shift (-0.8, +0.15) D | 6.39 | 12.35 |

- The **median** comes from the drift.
- The **p90** comes only from a **fast snap that pans**. A pure zoom over a smooth sky barely registers.

## Seconds per frame
**6.99 s wall / 13.4 s CPU** mean at final: 720x1280, 7 spp, 2 threads, two processes at once on 4 cores.
- The whole take took about 4.5 min wall.
- Build takes about 22 s per process.
- The draft (360x640, 6 spp) runs at about 2 s wall per frame.

## Gotchas for render teams (details in c16.py)
1. **Key every hook on every rendered frame.** Use TG hooks with `frame=`, and `C.key_vis()` for single set objects. `Take()` has already called `TG.clear_keys()`.
2. **World points must be functions.** `K.W()` depends on the rotation that `TG.build` sets (LINE = -90 deg). s01's first probe computed them at import and missed by 20 D.
3. **Pole 1 is the hero pole.** Each peg is split by material: `peg1_wood / _glass / _wiremat / _glintm` (`C.peg_parts(1)`). Wire spans are `STATE['spans_bottle'][i]`.
4. **The set's bottle is 3.3x oversize (2.27 D); the cast16 `bottle` prop is 0.8 D.** s01 drops `prop_r` from morse_cap_peg. Instead it lowers a copy of the set's own glass mesh (`LN.ins_bottle`, same material) with the fist pinned to its neck. It then switches to the set's bottle on the contact frame, so nothing pops.
   - Shot 23 (the callback) should reuse this exactly.
   - Shot 22 (bottle held to the sun at the wagon) can use the card prop, because no set bottle replaces it there.
5. **Reach on the ladder.** A hand gets only ~0.5-0.9 D above his head centre, and the bottle top is out of reach. Plan gestures around that, for example the flick.
6. **Slack or moving wire.** Build one small mesh per frame (`build_wire`) and show each on its own frame only. Use the same rods and sag as the set's spans, so the swap to the set's spans does not jump.
   - The wire from pole 0 passes near any camera close to the pole line and renders as a thick black bar. s01 keeps the camera about 5 D off the line, on the road side.
7. **Cards on steep cameras:**
   - keep pitch below about 40 deg (card max_slant 50);
   - low close cameras give upper_k ~1.2, so pass a taller canvas than CANVAS16 (s01 uses (-2.25, -4.75, 2.25, 0.125)) or the hair is clipped flat;
   - watch the logs for "sprite clipped".
8. **Mirror vs. the pole side.** Morse's STORY16 hook poses face screen-right. In this camera the pole is screen-left, so the pose uses `mirror=True`. Hands keys stay "r"/"l" of the UNMIRRORED figure.
9. **Camera.**
   - Run `python3 shot.py camreport` (CamPath.report) before rendering. It shows px/frame per frame, and the longest run below 0.25 px/frame must be <= 6 (s01: 0).
   - `decay < 1` keeps a hard-cut shot moving on its first and last frames.
   - Hand-made orbits: `arc_deg_s` is the cheapest source of parallax when the foreground is thin.
10. **Pose swaps** go on the closed frame of a 3-frame blink (`blink(g, [s])`, swap at s + 1). The drawn arms still jump; that is accepted, but it shows up as a frame-diff spike.
11. **Draft vs. final output.** `shot.py final ... 0.5 6` writes drafts to `work/draft` and never mixes them into `raw/`. Run two processes on interleaved frame lists (`0:74:2` and `1:74:2`). The loop resumes and skips frames already rendered at the same scale and samples.

## Differs from the plan / notes
- **Light:** DAY, as the shot_plan row says. L02 is the approved DAY tile; its AFTER_RAIN twin, L01, is for shot 23.
- **Ladder rails:** they appear in the lower right of the frame, at about 4-7 D from the lens, not 1-2 D. With the subject 10 D up and the card limit on pitch, no camera can bring the rails within 1-2 D of the lens and still see Morse. After the snap the near rail and rung ends sit in the lower right corner.
- **Snap size:** the snap is x2.8, at the top of the bible's x1.3-x3 range. It was needed for the p90 target. The framing ends as a close (head 281 px), with the bottle and the wire kept in frame.
- **Transmissive glass noise.** The held bottle copy (transmissive glass at the set's 7 spp) is slightly grainier than the set's own bottle. Judge it on take.mkv; the samples were not raised (cost).
