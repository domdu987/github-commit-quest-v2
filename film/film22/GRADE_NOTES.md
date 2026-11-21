# Film 22 grade vs the client COLOUR_SPEC (conform grade only, no re-render: client decision 2026-11-21)
`grade22.py` runs on the conformed frames:
1. A spec pre-grade (`film22/spec_grade.py`) for each shot whose hue shares are out of band (blue > 30 %, violet > 5 %, magenta > 10 %). It moves blue/violet chroma toward grey (x0.6), remaps violet to blue and magenta to crimson, and adds lamp warmth.
2. The v1.1 grade (`grade_v11.py`, copied from film 21 / the skill), with per-shot stage-1 values solved toward V 0.54 and S 0.43.

Test on the accepted lodgings takes (hue_report, caption band included):

| shot | red | orange | blue | violet | magenta | sat | val | dark | before the grade |
|---|---|---|---|---|---|---|---|---|---|
| s01 | 39.9 | 21.6 | 21.6 | 4.2 | 1.2 | 0.36 | 0.52 | 0.19 | blue 43 %, red 14 %, sat 0.56 |
| s04 | 20.0 | 16.2 | 54.8 | 6.9 | 1.6 | 0.37 | 0.46 | 0.26 | blue 77 %, red 1 %, sat 0.63 |
| s05 | 37.1 | 25.8 | 25.5 | 3.4 | 1.2 | 0.39 | 0.53 | 0.22 | blue 48 %, red 7 %, sat 0.59 |

## Shots that stay outside the band (spec §3: "night ... may fall outside these bands, the reason must be written")
- **s04, blue 55 %:** the frame is filled by Beck's circuit diagrams. These are navy blueprint sheets, a story object ("ช่างเขียนแบบวงจรไฟฟ้า"), and the night window sits behind him.
- **Dark 0.19-0.26:** night interior; the room is lit by one desk lamp.

The final film's per-shot values are written to grade22.json next to the conformed frames, and the full-film hue rows are added below at release.
