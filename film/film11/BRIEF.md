# Film 11: "ไอ้หมอวัว" (cowpox → vaccine; Edward Jenner, Berkeley, Gloucestershire, May 1796)
Repo-relative paths (work in-repo, branch film11/main). Set film/v3/set3d11 (NEW), cast film/v3/cast11 (NEW).
Narration film/film11/audio/narration.wav (62.4 s, Bankky orig 1.15, atempo 1.134), captions film/film11/script/captions.json,
timing film/film11/audio/timing.json, script film/film11/script/script_th.txt, TTS text film/film11/script/tts_bankky_orig.json.
Facts: Jenner vaccinated James Phipps (8) on 14 May 1796 with cowpox from milkmaid Sarah Nelmes (cow "Blossom"); day 7 armpit
discomfort, day 9 mild fever, next day well; 1 July 1796 variolated with smallpox: no disease. Mocker = composite of real critics
(e.g. Dr Benjamin Moseley's "cow-mania"; Gillray's 1802 cartoon of people sprouting cow parts). vaccine < Latin vacca (cow).
Hook line was rephrased for TTS (fal content filter flagged the first wording as a false positive).
Blind test: 7.5 → 8/10 after 3 rewrites (fewer day numbers, milkmaid clue planted in the pivot, "วัคซีนทุกเข็ม" not "ยาทุกเข็ม").
Picture note from the retest: show the mocker's reaction in the ending (he rolls up his sleeve in the vaccination queue).
Locations (planned): A cowshed/dairy barn (key preset), B Jenner's cottage garden + rustic hut + village lane, C village/sickroom.

## Look (client OK on the style board, 2026-11-18)
A = main look (golden morning barn); C (late amber, deeper blue-violet shade) for the crisis/night-ish beats; B approved for exterior.
Full-set fixes vs the board: detailed brown-and-white cows (not blobs), strand hay and layered thatch, dense props and life over the
whole frame INCLUDING the lower third (y 880-1280 is under captions but must not be empty floor), no tie beams cutting the frame,
small near-camera foliage (no giant grass blades), sharp, NO DOF, NO text, shade hue 240-260, magenta <= 10 %.

## Locations and presets (set: film/v3/set3d11/dairy.py)
barn (Blossom's cowshed, Berkeley farm):
  1 barn_wide      eye-level wide, golden morning (hook/pivot milkmaids)
  2 barn_milking   low medium: milkmaid on stool at the cow's flank, pail under the udder (reveal: blistered hands, clear face)
  3 barn_high      high angle, amber (C): pockmarked villagers in the door vs clear-faced milkmaids (reveal crowd)
  4 barn_door      low angle from inside out through the open door to the sunny lane, sun shafts
village (lane, green, Jenner's garden with the rustic thatched hut "Temple of Vaccinia"):
  5 garden_hut     Jenner's hut: boy on a stool, Jenner with lancet (hook, crisis)
  6 lane_wide      village lane, stone cottages, church tower, villagers, town doctor arriving (boss)
  7 lane_high      high angle over the lane/green, crowd laughing (nickname)
  8 garden_queue   ending: long queue from the gate to the hut, sunny
cottage (Phipps family room):
  9 room_day       bed under a window, mother, daylight (count)
 10 room_night     candle, fever night, town doctor at the door pointing (false payoff), C-like amber/blue
 11 room_morning   morning sun, boy jumps out of bed (false payoff turn)
Cast (film/v3/cast11): Jenner, James Phipps (8, + sick/in-bed pose, + "cow horns" gag variant), milkmaid Sarah Nelmes (+ blistered
hand prop) and a 2nd milkmaid, the town doctor/mocker (wig, cane, laugh/point/rolls up sleeve), the boy's mother, 3 villagers with
pockmarked faces, 2 plain villagers, the cow Blossom as a 2D puppet (side view, head turn, tail swish, udder visible).
Props: lancet, small glass jar, notebook, milk pail, candle.

FINAL gate note (film 10 client lesson): the blind viewer gets the narration as heard (timed text from captions.json), not an ASR transcript. QA-tech also checks smoke is not a blob stack and riders are parented to moving things.
