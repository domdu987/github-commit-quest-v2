# Shot plan, film 18 (ไอ้เสมียนวัว — Tian Dan's fire oxen at Jimo, 279 BC)
Narration: film/film18/audio/narration.wav (70.10 s), laid at +0.10 s. Shot boundary at narration time t = frame round(t*30); event at x = round((x+0.1)*30). Film end = 70.40 s, N = 2112.
Captions: film/film18/script/captions.json (phrase times). Sentence starts:
hook 0.00 · pivot 5.20 · count 15.30 · boss 19.90 · nickname 28.44 · false 31.45 · turn 40.15 · attack 43.63 · reveal 50.51 · aha 60.25 · ending 65.27 · end 70.10

## Camera grammar (client rule, film-2 rhythm; production-lessons §10)
- EVERY shot has a clear eased push or pull of 6-10 % of the framing per second plus a lateral slide of about 40 px/s. No near-static hold longer than 1 s. Median in-shot frame-diff ≥ 4, p90 ≥ 12 (measured at the FINAL gate next to film 2's 5.3 / 19.1).
- Quick push-ins on punch lines (quotes, nickname, "ยอมแล้ว!"), one whip on the charge, one snap on the reveal.
- Foreground prop 1-2 D from the lens in most shots (lantern, spear rack, wine jar, cart wheel, reed bundles, tent rope).
- Dissolve 11 f between places or times (13-15 f for night falls); HARD CUT on quotes and beats (marked CUT).
- Wide and medium framings that show the dense lit set; no extreme close-ups; inserts only on warm material objects in 3D. Sharp, no DOF, no text anywhere.
- Heads above y 880. Mouths move ONLY on the general's two quotes (22.45-27.95, 36.99-39.95). Laughing characters bounce 0.06 D at ~3 Hz.
- Battle is comic and bloodless: oxen charge, tents collapse, soldiers scatter and fall on their bottoms, pots fly; nobody is hurt, no weapons strike anyone.

## Sets (NEW set v3/set3d18, module jimo.py; locations and light presets)
- **jimo_in** — inside Jimo: the inner face of the rammed-earth wall, a lantern-lit lane and a yard with ox pens, stalls of a market, houses with tiled roofs, the wall walk with torches. Lights: DUSK, NIGHT. States: holes 0..N in the wall base (set_holes), oxen count/dress state.
- **jimo_out** — the outer face of the wall and gate tower, moat and bridge, the road toward the camp (board_1). Lights: DUSK, NIGHT.
- **yan_camp** — the Yan camp in front of Jimo: tent rows, fires, the general's table with wine jars, chariot, drums, pennants, palisade (board_2). Lights: DUSK, NIGHT. States: set_party (cheering soldiers, raised cups), set_rout (tents collapsed, pots and cups flying, fodder scattered).
- **vista** — a high view over the Qi plain at dusk: many small walled towns with black Yan pennants, two towns still lit warm (Jimo nearest, Ju far). 3D, no map, no labels.

## Cast (v3/cast18, flat 2D puppets)
- **tiandan** (hero): thin market clerk, plain ochre robe, black scholar's cap, bamboo tally slips at his belt; calm, almost never speaks.
- **general** (mocker, invented): stout Yan general, dark lacquered armour with red cords, plumed helmet, big moustache, bronze wine cup; laughs with belly bounce.
- **yan_soldier_a/b/c**: Yan soldiers (black and red), spears; laughing, cheering, fleeing variants.
- **townsfolk**: old man, woman, child, each with a bronze vessel and stick (beating it); one envoy in plain robe bowing.
- **ox_plain** and **ox_dragon** (2D puppet, side and 3/4): red silk coat with gold five-colour dragon pattern, short blades on the horns, reed bundle on the tail with states off / lit (flame card + emitter light); gallop cycle; a herd instancer for wide shots (10-60 visible, plus silhouettes).
- **qi_soldiers**: dark silhouettes running behind the oxen (5,000 picked men; no faces needed).

## Shot table
| # | t0-t1 (s) | frames | set / light | camera | action | trans in |
|---|---|---|---|---|---|---|
| 1 | 0.00-5.20 | 0-156 | jimo_in / NIGHT | **BIGZOOM A** (client §H): one continuous eased crane-down + push, 0-3.6 s from EXTREME WIDE high over the moonlit wall top and tiled roofs (whole ox yard + pens + lanterns + dozens of dragon-dressed oxen; Tian Dan < 5 % of frame height but findable at the lit ox) down over the roofs to MEDIUM on Tian Dan (body 35-60 % of frame height), then 3.6-5.2 s slow push 6 %/s + slight orbit | Tian Dan tugs the dragon silk over an ox, then ties short blades to its horns ("ผูกมีด" 3.13 = g97, he is at medium by then); the herd of dressed oxen fills the yard behind. (Replaces old s01 + s02.) | — |
| 3 | 5.20-9.89 | 156-297 | vista / DUSK | establishing high, push 6 %/s, slide left | "คืออย่างนี้นะ": the Qi plain at dusk; black Yan pennants rise one by one over small walled towns (pop on 7.32-9.89), dozens of them. | dissolve 15 |
| 4 | 9.89-12.81 | 297-384 | vista / DUSK | high, push-in toward the near lit town | Two towns stay warm-lit with no Yan flag; push to the nearer, Jimo, on "จี๋โม่" 11.91. | — (same take, snap) |
| 5 | 12.81-15.30 | 384-459 | jimo_in / DUSK | eye, push-in 8 %/s; fg market stall scale | Market lane: Tian Dan at a clerk's stall with tally slips and an abacus-free counting board; townsfolk hand him a general's sash (made general). | dissolve 11 |
| 6 | 15.30-17.69 | 459-531 | jimo_in / DUSK | eye, slide left 40 px/s along the lane | He walks house to house; townsfolk lead oxen out of gates; "สิบตัว" 17.23: ten oxen in the yard. | CUT |
| 7 | 17.69-19.90 | 531-597 | jimo_in / DUSK | high (4 D), pull-out x1.6 snap on "พันกว่าตัว" | "ร้อยตัว" a yard full; snap pull-out to the whole quarter packed with oxen (instancer ~200 visible + silhouettes). | — |
| 8 | 19.90-22.45 | 597-674 | yan_camp / DUSK | eye, push-in 8 %/s; fg spear rack | The general on the camp rampart looks at Jimo through the dusk, sees oxen tails behind the wall gate, bursts out laughing (bounce). | dissolve 13 |
| 9 | 22.45-24.56 | 674-737 | yan_camp / DUSK | eye medium, push-in 9 %/s | QUOTE 1a lip-sync "จะเอาวัวมาสู้ทัพข้างั้นเหรอ!" arms wide; soldiers behind laugh. | CUT |
| 10 | 24.56-28.44 | 737-853 | yan_camp / DUSK | medium-close push-in 10 %/s then slight slide | QUOTE 1b lip-sync "ถ้าวัวพวกนั้น… ข้าจะยอมให้วัวไล่ข้ากลับบ้านเลย!" thumb at his chest, chin up. | — |
| 11 | 28.44-31.45 | 853-944 | yan_camp / DUSK | wide eye, pull-out 7 %/s; fg wine jars | Soldiers around a fire mock-moo, make horns with fingers, laughing; push-in on "ไอ้เสมียนวัว" 30.64. | CUT |
| 12 | 31.45-33.41 | 944-1003 | jimo_out / DUSK | eye low, slide right; fg cart wheel | The gate opens a crack; a bowing envoy walks out over the bridge with a white flag-like plain banner; old folk and women stand on the walls (no soldiers). | dissolve 11 |
| 13 | 33.41-35.67 | 1003-1071 | yan_camp / NIGHT party | wide high, pull-out 6 %/s | Camp party: soldiers cheer, raise cups, dance; a sentry drops his spear and joins in; torches by the palisade left alone. | dissolve 13 (night falls) |
| 14 | 35.67-37.85 | 1071-1136 | yan_camp / NIGHT | eye medium, push-in 9 %/s; fg wine jar | General raises his cup, laughs (bounce); QUOTE 2a lip-sync "ไอ้เสมียนวัวยอมแล้ว!" from 36.99. | CUT |
| 15 | 37.85-40.15 | 1136-1205 | yan_camp / NIGHT | medium-close push-in 10 %/s | QUOTE 2b "พรุ่งนี้กินเนื้อวัวกัน!" he mimes carving, licks lips; cup tilts. | — |
| 16 | 40.15-43.63 | 1205-1309 | jimo_in / NIGHT | low inside the wall base, slide left along the wall; fg pick and baskets | Silent townsfolk dig through the rammed earth; holes open one after another (set_holes 0→12) on "รูหลายสิบรู". | dissolve 15 |
| 17 | 43.63-46.27 | 1309-1388 | jimo_in / NIGHT | eye medium, push-in 8 %/s; fg reed bundles | Reed bundles soaked from a jar are tied to the oxen's tails, lined up nose-first at the holes. | CUT |
| 18 | 46.27-47.56 | 1388-1427 | jimo_in / NIGHT | eye, quick push-in | Tian Dan raises a torch: "จุดไฟ" 47.13 → tails light in a ripple (flame cards + lights). | CUT |
| 19 | 47.56-50.51 | 1427-1515 | jimo_out / NIGHT | low wide at the wall, WHIP pan to follow | Oxen burst out of the holes in the wall (dust puffs), glowing tails, gallop across the moat bridge and field toward the camp; dark Qi soldiers behind. | CUT (whip out at end) |
| 20 | 50.51-53.20 | 1515-1596 | jimo_out / NIGHT | low tracking beside the herd, push 7 %/s | Reveal A: fire behind, the oxen run forward only (they never turn back toward the flame); herd charges, tails streaming sparks. | whip in |
| 21 | 53.20-56.08 | 1596-1683 | yan_camp / NIGHT | eye from the Yan side (POV-ish), SNAP push x1.5 on "สัตว์ประหลาด" | Reveal B: out of the dark comes a wall of glowing red dragon monsters with flashing blades; soldiers' jaws drop, cups fall. | CUT |
| 22 | 56.08-58.04 | 1683-1742 | yan_camp / NIGHT | medium push-in 9 %/s | Close-medium on one ox in full flare: dragon silk, blades glinting ("วาววับ"), flame tail; terrified soldier freezes. | — |
| 23 | 58.04-60.22 | 1742-1807 | jimo_out / NIGHT | high over the wall top, pull-out; fg torch | On the wall: old men, women, kids beat bronze pots and basins, mouths wide (no lip-sync, shout drawings), sound rings. | dissolve 9 |
| 24 | 60.22-62.74 | 1807-1882 | yan_camp / NIGHT rout | wide high, slide 50 px/s + push | Rout (comic): tents fold down, soldiers flee in all directions, pots and helmets fly, a chariot rolls away empty; nobody hurt. | CUT |
| 25 | 62.74-65.27 | 1882-1958 | vista / DAWN | establishing high, push 6 %/s | Qi banners return over the towns of the plain one by one (70+), warm dawn. | dissolve 15 |
| 26 | 65.27-70.40 | 1958-2112 | jimo_out road / DAWN | **BIGZOOM B** (client §H): one continuous eased crane-down + push, 65.3-68.9 s from EXTREME WIDE high above Jimo's wall (wall + gate + moat + road + fields + smoking far camp; the general < 5 % of frame height, a tiny figure on the road with oxen behind) down in front of him to a low MEDIUM (35-60 % of frame height), then keep tracking backward ahead of him with the push-in on "วิ่งหนีวัว" | The general runs down the road toward home, helmet askew, cup still in hand, a few dragon oxen trotting after him with smoking tails; HARD CUT on "ตลอดทาง". | dissolve 11 |

Counts: 26 shots, mean 2.70 s; 9 dissolves, 12 hard cuts, 1 whip, 2 snaps; framing changes inside 4 shots (4, 7, 11, 21) for an average change about every 2.3 s.
Lip-sync shots: 9, 10, 14, 15 (general only). Key shots for QA-art at the TAKE gate: 1-2 (hook), 7 (count payoff), 13-15 (false payoff), 19-22 (reveal), 26 (ending).

## Sound cues (SFX library to generate, fal sound-effects v2)
ox moo, ox herd gallop, crowd laugh (men), belly laugh, cups clink, party cheer, pickaxe on earth, earth crumble, torch whoosh/ignite, fire crackle, bronze pot clangs, war panic shouts (comic), tent collapse thud, distant night insects, dawn birds.


## Client §H (2026-11-20): BIGZOOMs and angle types
- BIGZOOM A: s01 0.00-3.6 s (extreme wide -> medium Tian Dan), jimo_in NIGHT. BIGZOOM B: s26 65.3-68.9 s (extreme wide -> medium general), jimo_out DAWN.
- Angle types used: high/bird's-eye (s01 start, s03, s04, s07, s13, s24, s25), low hero (s16, s19, s26 end), side tracking (s06, s20), through a foreground frame (s08 spear rack, s11 wine jars, s17 reed bundles), crane down (s01, s26), over-the-shoulder (s09 camera behind the table past the general).
- s02 is merged into s01 (25 takes).
