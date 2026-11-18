# Film 12 style board: a Georgian London street in the rain

Files (all in `film/v3/set3d12/`): `street.py` (the set), `street_tex.py` (numpy/PIL artwork, cached in `tex_street/`), `street_hue.py`, `make_board.py`,
`styleboard/sb1_street_wide.png`, `sb2_coach_low.png`, `sb3_street_high.png` (720x1280), `board.jpg` (2160x1280), `hue.txt`.
Helpers are imported (never copied) from film 2 / 5 / 6 / 8 / 9 / 10 (`tower`, `mine`, `wall`, `wall_tex`, `harbour_tex`, `spec/grade_compositor`); no other folder was edited.

## Run
```
pip install bpy==5.3.0 numpy pillow                 # Python 3.13, Cycles CPU, 4 cores
cd film/v3/set3d12
python3 street.py styleboard                        # the three board stills -> styleboard/ (14 samples, 720x1280)
python3 street.py styleboard street_wide            # one still   (presets: street_wide | coach_low | street_high)
python3 street.py stills [preset]                   # 360x640, 6 samples drafts -> street_work/stills/
python3 street.py final [preset]                    # 720x1280 -> street_work/final/
SAMPLES=6 python3 street.py final                   # override the sample count
python3 street_hue.py && python3 make_board.py      # hue.txt and board.jpg
```
API: `import street as S; A = S.build('street_wide'); cam = S.make_camera(S.CAMS['street_wide']); S.stage_placeholders(A, 'street_wide'); S._shot_extras(A, cam, 'street_wide'); S.render(path)`
(`S.render_preset(preset, out, quality)` does all of it). Rain streaks, drips and lamp halos are camera-dependent geometry made in `_shot_extras` after the camera exists.

## Look
World: 1 unit = 1 head (adults 3), z up, street along +y, houses at x = +-9.8, roadway +-5.9, kerb/pavement to +-6.3, cornices z 19.35, roofs/chimneys above.
One hard warm key (sun az 205, elev 60, from -x: lights the right row, the road right of x~3 and the coach rank), blue-violet shade (tint hue ~250), warm practicals
(sash windows with per-pane amber glow maps, bow shop windows with goods, oil lamps with halo cards + real point lights, coach lanterns). Setts and pavement are glossy
(Fresnel-weighted GGX, bounce 1) so windows and lamps reflect; layered puddles (shallow sheet + deep pool, see-through water film) carry ripple-ring decals; gutters carry flowing-water texture.
Rain: ~1000 crisp pointed ribbons at constant ~2 px width, camera-only; eave drips; mist only in the far distance (compositor mist pass, no blur); no depth of field.
Props: 10 brick facades (6 houses, 4 shops), pictorial signs (boot, teapot, pretzel, no letters) on iron brackets, awnings, area railings, lead pipes, chimneys with pots,
slate roofs, oil lamp posts, barrow of vegetables, barrels, crates, 3 hackney coaches with horses (rank on the right kerb), a closed far-end terrace,
placeholder actor cards (Hanway under a dark umbrella, a coachman on the box, a passer-by), umbrella domes in sb3 incl. a pink lace one on a coach.

## Numbers (final, 14 samples, 720x1280, 4 threads, OIDN denoise)
| still | wall | CPU | shade hue | magenta |
|---|---|---|---|---|
| sb1_street_wide | 9.6 s | 37 s | 253.7 | 9.2 % |
| sb2_coach_low | 11.1 s | 43 s | 244.9 | 9.1 % |
| sb3_street_high | 7.0 s | 27 s | 255.9 | 9.9 % |
(full rows in `styleboard/hue.txt`; the reference rows of `tools/hue_report.py` point at a missing folder, so `street_hue.py` prints only our rows.)
Magenta came from brick in warm-bounce shade and from mauve mist/clouds: bounce light cut to 0.07, mist and clouds moved to peach / blue-grey.

## Weak spots
1. Horse and coach are chunky low-poly shapes (stilt legs, log-like body); fine for a style board, they need a proper horse if it is seen close.
2. The wet road in sb1/sb2 reads as one milky mirror lake; puddles (fan-triangulated blobs) show noise and pale sky reflections in the bottom third, and cobbles lose their stones there.
3. Facades are a repeated 10-texture set with flat painted windows (relief only from sills/lintels); sky is soft-edged mauve toon clouds; placeholder cards have stick legs, and the rain is slightly heavy.
