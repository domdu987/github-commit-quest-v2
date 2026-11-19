# v3/paper: the film's paper and text artwork (build-order step 3)

Owner: this folder only. No Blender here. Every item is a Python function that returns a complete SVG document,
drawn in D units with the v2 office helpers (`v2/sets/office.py`, imported read-only: `rect`, `line`, `text`,
`greek`, `fit`, palette `PRINT_D`, `INK`, `RED`), and rasterised by headless Chromium (`raster.js`, Playwright)
into `tex/`. Thai comes only from local font files, embedded as `@font-face` in each SVG: Kanit ExtraBold and
Kanit Black (`proj/fonts/th/`), Loma Bold (`/usr/share/fonts/opentype/tlwg/`). Latin uses the set's faces
(DejaVu Serif Bold slab capitals, Liberation Serif masthead, Liberation Mono teletype).

```python
import sys; sys.path.insert(0, PROJ + '/v3/paper'); import paper as P
P.build()                                   # rasterise what changed (sha1 cache in tex/manifest.json); returns {name: png or [frames]}
e = P.REGISTRY['nickname_label']            # {'svg': fn, 'png': path, 'size_D': (w, h), 'px': (W, H) after build, 'kind', 'note', 'transparent'}
svg = e['svg']()                            # the SVG document (sequence items take frame=k)
P.REGISTRY['newspaper_bleed']['frames']     # 12 png paths, f_00 .. f_11
```
CLI: `python3 paper.py all` (build + sheet.jpg + Thai crops), `build [--force]`, `sheet`, `crops`.
`tex/registry.json` repeats the registry (paths, size_D, px, kind, note) for code that does not import Python.

## Using a texture in Blender

Map the PNG 1:1 onto a quad of `size_D` (texture y runs down; (0, 0) is the item's top-left corner). Transparent
items carry alpha (ragged torn edge, round signs, the hand-cut label): use the alpha as the material's alpha
(Principled alpha or a mix with a transparent BSDF). Colours are the neutral-light colours of the surface; the
office light model lights them as it lights the set's own textures (`v3/set3d/textures.py`). The ink outline
(`INK #2a1712`, about 6 px) is drawn into each texture as on the set's calendar and sign. Cycles does not
mip-map: in a far view use a copy scaled down to about 1.5 x the screen size (stage API trap 8).

## Items

| name | size_D (w x h) | px | kind | shots and use |
|---|---|---|---|---|
| `forecast_sheet` | 1.08 x 1.40 | 1580 x 2048 | static, alpha | 14: the hi-res quad after the tear. English header U.S. WEATHER BUREAU, typewriter OFFICIAL FORECAST / SEPT. 20, 1938, typed THAI ฝนตก and ลมกระโชก (Loma Bold, ink-roughened), red round Thai stamp ทางการ on the header block, torn bottom edge |
| `forecast_sheet_teletype` | 1.08 x 1.40 | 1580 x 2048 | static, alpha | 14: the same sheet still in the machine (no stamp, straight bottom); also the chief's paper |
| `forecast_sheet_base` | 1.08 x 1.40 | 1580 x 2048 | static, alpha | sheet without the two words and the stamp |
| `forecast_word_1`, `forecast_word_2`, `forecast_stamp` | 1.08 x 1.40 | 1580 x 2048 | overlay, alpha | the word ฝนตก (pops 30.85), ลมกระโชก (31.30) and the stamp (29.82) alone, in the same frame as the sheet: stack over `forecast_sheet_base` to pop or bloom them |
| `forecast_sheet_en` | 1.08 x 1.40 | 1580 x 2048 | static, alpha | English variant (RAIN, / GUSTY WINDS, stamp OFFICIAL) - see Language below |
| `nickname_label` | 1.15 x 0.34 | 2400 x 710 | static, alpha | 13, 17, 18, 19-22, 25: hand-cut cream strip, THAI ทางด่วนพายุ in red-brown brush (Kanit ExtraBold, one `<text>` per grapheme cluster, jitter +-4.5 deg / +-0.007 D / 95-106 %, displacement + speckle + dry-brush streaks), red brush underline, doodled road with an up arrow at the right end. Pin: `P.LB_PIN` = (0.50, 0.045) D from the top-left, clear of the lettering |
| `calendar_pad_20` | 0.66 x 0.90 | 1173 x 1600 | static, alpha | 4: the whole tear-off pad, SEPTEMBER (red band) / 20 / TUESDAY / 1938 (20 Sept. 1938 was a Tuesday, checked). Same size and layout as the set texture `calendar` (anchor `calendar_rect`): swap it in |
| `calendar_pad_21` | 0.66 x 0.90 | 1173 x 1600 | static, alpha | 17, 18, 25 and the kitchen wall: leaf 21 WEDNESDAY on top. It is also what lies under leaf 20 |
| `calendar_leaf_20`, `calendar_leaf_21` | 0.62 x 0.86 | 1153 x 1600 | static | the top leaf alone, for the flutter quad; it sits at offset (0.02, 0.02) D inside the pad (`P.LEAF`) |
| `newspaper` | 1.50 x 1.95 | 2000 x 2600 | static | 15, 26: front page. Masthead 'Long Island Daily' (mixed-case old-style serif, as A t32.0), WEDNESDAY, SEPTEMBER 21, 1938, double rules, greeked two-line headline and four columns, engraved lighthouse in a ruled box. Weather box lower right (`P.WB` = x 0.56, y 1.00, w 0.88, h 0.84 D): header THAI พยากรณ์อากาศวันนี้ with a rain-cloud vignette, big ฝนตก (Loma Bold, the sheet's face, size 0.25 D), smaller ลมกระโชก |
| `newspaper_en` | 1.50 x 1.95 | 2000 x 2600 | static | English weather box: TODAY'S FORECAST / RAIN, / GUSTY WINDS |
| `newspaper_bleed` | 1.50 x 1.95 | 2000 x 2600 | sequence of 12 | 26: from 64.95 the drop sits on ฝนตก as a bead (f_00-f_04, soaking in), a wet ring spreads (radius 0.04 to 0.17 D, eased) and the word's ink runs blue-brown into it; one frame per film frame, then hold f_11. Big-word centre `P.WB_W1` |
| `speed_sign` | 0.26 x 0.26 | 1600 | static, alpha | 20: red ring, '100' (Kanit Black, navy), THAI กม./ชม. under it |
| `speed_sign_back` | 0.26 x 0.26 | 1600 | static, alpha | its painted back with the bracket; the spin pin goes through the centre |
| `stamp_impression` | 0.34 x 0.34 | 1500 | static, alpha | the round ทางการ stamp alone (same drawing as on the sheet) |
| `stamp_face` | 0.34 x 0.34 | 1500 | static, alpha | the rubber face of the stamp prop: mirrored design on red-brown rubber |
| `tick_stamp` | 0.20 x 0.20 | 1500 | static, alpha | 7: tick-mark stamp on the chalk curve (12.95), no words |
| `no_right_turn`, `no_left_turn` | 0.22 x 0.22 | 1500 | static, alpha | 19: the two pictograms that pop on the east (46.45) and west (46.85) walls, no words |
| `compass` | 0.30 x 0.30 | 1500 | static, alpha | 19: compass rose, north point red, Latin N (ping 45.15) |
| `spinner_disc`, `spinner_disc_ghost` | 0.16 x 0.16 | 1500 | static, alpha | the storm spinner disc (red, cream spiral, pin hole at the centre) and its grey ghost (21) |
| `paper_tape` | 0.12 x 0.80 | 240 x 1600 | static, alpha | 4: the teletype tape the chief reads and tears |
| `desk_typed_sheet` | 0.50 x 0.65 | 1231 x 1600 | static, alpha | 12: the greeked typed sheet on the foreground desk |
| `beach_sign` | 2.20 x 0.95 | 2400 x 1036 | static | 8, 16, 23: the fence sign reworded, LONG ISLAND large, BATHING BEACH · SUFFOLK COUNTY 1938 small (same size as `beach_tex` 'sign': swap it in) |

Every item is drawn by one function with parameters: `forecast_svg(lang, words, stamp, torn, paper, only)`,
`label_svg(seed)`, `calendar_svg(day, part)`, `newspaper_svg(lang, bleed)`, `speed_sign_svg(side)`,
`stamp_svg(face, lang)`, `tick_stamp_svg()`, `no_turn_svg(direction)`, `compass_svg()`, `spinner_svg(ghost)`,
`tape_svg()`, `typed_sheet_svg()`, `beach_sign_svg()`; each takes `long_px` (pixels on the long side).

## Style (LOOK_SPEC 3.4, environment_materials 1.7 and 3.7)

Paper `#fff5df` with a faint fibre grain (two noise layers at 7-20 percent), printed ink `#836d4e`, darker ink
`#574430` for the large typed words and small lettering, red `#b61d32`, navy `#081148`, cream `#f3d9a8` on red.
One or two large lines per item; everything else greeked (dash bars, letter blocks in the newspaper headline);
thin ruled frames; slab capitals with 0.6-2 px letter spacing; the masthead in mixed-case serif; teletype lines in a
typewriter face. Ink is roughened by an SVG filter (fractal-noise displacement, speckle voids, dry-brush streaks on
the label and the stamp); the paper edges are hand-cut (small wobble) or torn (the forecast sheet, the tape).

## Language

The plan (shot_plan.md shots 14, 15, 26 and its TEXT POLICY) makes the forecast words, the stamp, the newspaper weather
box, the label and the km/h unit THAI; signs, map print, calendar, masthead and dateline stay English. The registry's
default items follow the plan. The worker brief also names the English forecast words "RAIN, GUSTY WINDS"; those
are delivered as `forecast_sheet_en` and `newspaper_en` (same layout, so either pair can be used as long as shots 14,
15 and 26 use the same language).

## Checks done

- Thai shaping at full size (`python3 paper.py crops` -> `tmp/crop_thai_*.png`): the tone mark of ด่ and the vowel
  under ยุ in the label, ณ์ and the stacked ี้ of นี้ in the newspaper header, กม./ชม. on the sign and ทางการ in the
  stamp all sit on their base letters (each cluster is shaped by Chromium inside one `<text>`; marks have zero
  advance in Kanit and Loma, used for the per-cluster layout).
- Sizes: the large typed words on the sheet have an x-height of 0.14 D (ฝนตก) and 0.135 D (ลมกระโชก, compressed
  to 0.94 D wide): 90 px or more when the 1.08 D sheet fills the 720 px frame (shot 14 asks for 80 px). Newspaper
  ฝนตก x-height 0.13 D.
- Dates: 20 and 21 September 1938 = Tuesday and Wednesday (Python datetime).
- `sheet.jpg`: every item next to the reference text props a/t32.0, a/t40.0, a/t27.5 and the crop sheet
  ref/crops/env/A_text_props.jpg.
