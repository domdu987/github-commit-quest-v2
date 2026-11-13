# s17 QA: film 5, shot 17 (the ending), mine set (pithead DUSK)

Delivered: `take.mkv` = frames g 1806..1967 (162 frames, 720x1280, 12 samples, 2 threads, no captions, no audio); first_g 1806,
in-handle g 1806..1813 (17a camera keeps moving, for a 12-f dissolve from s16), no out-handle (the film ends on g 1967, hold).
Also `meta.json`, `cues.json` (7 cues), `contact.jpg` (16 frames), `compare.jpg` (finals beside ref a t0121 / t0125 / t0127), `shot.py`, `deliver.py`, `qa.py`.

## Client rules
- **No DOF / no blur**: `M.setup_dof(scene, None, None, cam=...)` at build and before every render; the oxygen_insert DOF default is never applied. No motion blur.
- **Bird visibly inside the cage**: the cage stands on the bench (nobody holds it), drawn as the cast's 2D `canary_in_cage` (bars over the bird), so the bird
  is behind the bars in every frame, lying on the cage floor, then on its perch.
- **Gentle bird**: `fallen` with eyes softly closed (never X) and a slow breath, eyes open g 1879-1891, hop to the perch g 1894-1899, one note g 1899-1934,
  awake to the end.

## Timing (captions.json, narration at +0.10 s)
| sub-shot | g | what |
|---|---|---|
| 17a | 1806-1871 (in-handle 1806-1813) | medium: alfie kneeling at the first-aid bench, the brass OXYGEN box, its rubber tube to the small mask in his fist at the cage bars ("บนปากเหมือง เขาให้นกดมออกซิเจน"); slow push |
| 17b | 1872-1967 (cut) | closer on the cage, mask and alfie: eyes open ("นกน้อยลืมตา" 1879), alfie's worried face turns happy (closed smile, 1889), hop up, one note ("แล้วร้องออกมาอีกหนึ่งโน้ต" 1899-1934); slow push to g 1950, hold to the end |

## Staging and numbers (`work/qa.txt`)
```
sub-shot 17a (g 1806..1871, 66 frames)
  alfie   head w   218..  249 px, centre x  548.. 563, centre y  575.. 583 (0.45..0.46 H); head bottom below 880: none
  bird    head w    41..   47 px, centre x  362.. 372, centre y  709.. 719 (0.55..0.56 H); head bottom below 880: none
  fist vs mask back on screen: median 12.3 px, max 13.3 px
  render: wall 11.86 s, cpu 21.91 s per frame (mean)
  retried frames: []
sub-shot 17b (g 1872..1967, 96 frames)
  alfie   head w   366..  437 px, centre x  530.. 561, centre y  554.. 568 (0.43..0.44 H); head bottom below 880: none
  bird    head w    74..   94 px, centre x  173.. 229, centre y  680.. 798 (0.53..0.62 H); head bottom below 880: none
  fist vs mask back on screen: median 24.9 px, max 27.1 px
  render: wall 11.32 s, cpu 22.29 s per frame (mean)
  retried frames: []
```
popcheck: pops (g -> g+1, change): [(1871, 1872, 50.6), (1889, 1890, 2.8)]
near-still transitions (< 0.35 levels): [1806, 1807, 1808, 1869, 1870, 1872, 1873, 1874, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966]
magenta / black frames: []


Pops: the cut 1871/1872, and 1889/1890 (2.8 levels: alfie's worried -> happy expression switch, a deliberate beat). Still frames 1948-1966 = the requested hold.
Mouths: alfie never talks (worried frown, then a closed smile).

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s17 17a (g 1806-1871)                          36.2   34.9    0.2    2.1    1.0    7.8    7.0   10.9  0.32 0.57 0.03   OUT: blue,violet,magenta,sat,dark
s17 17b (g 1872-1967)                          25.3   44.1    0.4    0.7    0.1   14.2    7.0    8.1  0.37 0.55 0.09   OUT: red,orange,violet,sat
s17 all                                        29.5   40.5    0.3    1.2    0.5   11.8    7.0    9.2  0.35 0.56 0.07   OUT: red,orange,blue,violet,sat,dark
```
Dusk exterior: red/orange dominant like s01 4a; shade blue-violet, magenta 8-11 (the orange-pink dusk sky and warm bench, as the set's DUSK finals).

## Seconds per frame
~11.5 s wall / ~22 s CPU mean (2 threads, denoise FAST).

## Differences from the plan / known issues
- Plan "slow push, hold" kept, split into 17a / 17b (one cut at 1872) for the 1.0-1.5 s framing rule; 17b pushes to g 1950 then holds.
- The set's oxygen box stays on the bench; its lying tube and mask are cut from the `oxygen_box` mesh at runtime (x > 11.79, z < 1.25) and replaced by
  my keyed rubber tube (bevelled bezier from the outlet valve) and a small rubber mask in alfie's right fist (fist vs mask back 12-27 px).
  Alfie uses `alfie_revive`'s kneel without the cast's 2D oxygen box (would be a second box).
- Hut / engine window emission x0.55 at runtime (the set's blown yellow window blocks; still bright warm panels).
- Alfie's reaching arm crosses his chest (he faces screen-left toward the cage); kneeling leg pose as in the cast.
