# s20 QA: film 4, shot 20 (DAWN ending: the master on the timber pile, push to the pillar still swinging), pagoda set v2, render worker 4

Delivered: `take.mkv` = `frames/g_1829.png .. g_1967.png` (139 frames, 720x1280, 12 samples, 2 threads; meta.json first_g 1829, n_frames 139).
g 1836..1967 = shot 20 (61.21 s to the end, N = 1968); g 1829..1835 = 7-frame in-handle for the dissolve from shot 19, rendered in 3D.
No out-handle (the film ends). Also `meta.json`, `cues.json`, `contact.jpg`, `compare.jpg` (vs ref a t0125 / t0127 / t0129), `work/hue.txt`.
Mean 15.0 s wall / 29.6 s CPU per frame. Re-rendered once: in the first pass the camera came in behind the east stone lantern, which
blurred across the frame from g 1912 to g 1958 and hid the pillar (old outputs in `work/old_v1`, not delivered).

## Timing
| g | what | ref a |
|---|---|---|
| 1829-1880 | from the south tip of the rubble: the master (cast4, stunned, mouth closed) stands on the fallen tower's timbers, right third, looking toward the pagoda; the pagoda fills the left; slow push past him ("ช่างใหญ่ยืน" g 1853, he leaves frame right at ~g 1851) | t0125 |
| 1880-1926 | the push swings onto the runner axis and drops toward the open base ("มองเสากลาง" g 1889); the near stone lantern passes through the lower frame g ~1904-1914 (parallax layer, the base stays visible above it) | t0127 |
| 1926-1967 | eased slow hold on the open base: the golden pillar foot centred, still swinging gently (set_pillar_swing 1.6 -> 1.1 deg, 0.42 Hz; storeys still); focus pulled from the master to the pillar over g 1872-1902 | t0129 |
Framing changes: the push has eased phases at 1829 / 1880 / 1926; never static (slowest speed in the final hold ~0.3 px/frame at the edges).

## State
DAWN, cutaway off, collapse 1 with dust off and settle 0 (the settled-dust bank read as a pink blob in the foreground), sway 0, pillar swing keyed per frame.
DOF: focus empty animated master -> pillar, f 5. head_flip True (DAWN sun from the east-south-east: screen-right in this view).
Master head (on screen g 1829-1850): centre x 463 -> 711, y 0.41-0.45 H, width 118-149 px; head bottom well above 880.

## Colour (`work/hue.txt`)
red 47.4, orange 15.4, blue 13.0, violet 12.1, magenta 11.5; sat 0.36, val 0.60, dark 0.03. Warm dawn on the red pagoda: red above the band,
magenta 1.5 over (pink-gold DAWN key on red lacquer and the pink snow-lit ground; the set's DAWN stills sit at the same values). Shade on the
ground reads blue-violet.

## Differs from the plan / reference
- The ref's closing image is a wide graphic cross-section; the plan asks the push to the pillar, done as planned.
- The master leaves frame early (~0.5 s into the shot) as he is passed; the pillar's swing is small on screen (~0.4 D at the foot).
