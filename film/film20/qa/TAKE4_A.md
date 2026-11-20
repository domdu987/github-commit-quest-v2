# TAKE gate round 4, QA-tech A, film 20: s03 s11 s15 s23
Method: all frames extracted (g = first_g + index), qa_auto.py (--first_g, no cuts inside any take) + qa_stats2.py, viewed at 6 fps (s15/s23 at 10 fps) plus handles and beat frames, full-size crops of s11 rivet/toss. Takes not edited. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeqa4/
| take | sat | vivid % | luma | motion med / p90 | auto | handles | verdict |
|---|---|---|---|---|---|---|---|
| s03 | 0.535 | 56.5 | 98.9 | 4.85 / 12.97 | PASS | 8+226+8 ok | FAIL |
| s11 | 0.565 | 66.3 | 99.7 | 4.72 / 15.45 | PASS (soft g836-838, 917 = flights) | 8+243+8 ok | PASS (notes) |
| s15 | 0.586 | 49.5 | 86.8 | 7.12 / 11.33 (own 7.7 / 13.3; within 10 % = NOTE) | PASS | 8+97+4 ok | PASS |
| s23 | 0.544 | 47.2 | 97.6 | 6.43 / 12.25 | PASS | 8+76+8 ok | PASS |
No black/magenta/frozen/pop frames, no text/tofu, no mouth motion tied to quotes, heads < 880 in all four.

## s03 FAIL (BIGZOOM 1 + crane). Round-3 list:
- R3-1 (start not an extreme wide of Paris; no Seine; 50-55 % empty sand; zoom too short): PARTLY FIXED. The 5 % -> 35 % descent is now continuous ~g190-g285 (~3.2 s) with Eiffel < 5 % until ~g200 and a medium (~45 % of frame height) at g285-g310: duration OK. NOT FIXED: g170-g200 (1 s+) is still ~60-65 % bare orange dirt with dozens of tiny black scatter specks, grid of white blocks as "Paris", no Seine, no sky band to speak of, no whole-town view; Eiffel/table is not findable (only a yellow lamp dot beside a leg). g200-g235 the dirt + brick pier + long shadow is ~45 % of the frame.
- R3-2 (pale brick wall slab 40-45 % behind Eiffel; black/blue plan table in the bottom 25-30 %): NOT FIXED. g240-g315 the pale brick pier wall still fills ~30-40 % of the frame at left and behind him; g230-g265 the plan table is still a saturated blue/dark slab in the lower right (~20 % of the frame, reads as a keyboard/grille, not cream plans). g275-g285 the tall lamp pole and its big yellow globe cross the frame beside his head (not through the face, but a bright blob and bar at the top).
- R3-3 (leg bowed, timber look): NOTE, not fixed. g330-g370 the leg is a banana curve and g362-g380 an underside timber slab fills the top ~35 % of the frame; the flat platform deck reads as a slab.
- OK: Eiffel not cut at the landing, pointing up proudly g285-g312; riveters visible on the platforms g375-g410; crane up reads; no cut inside; handles correct; stats pass.
- Fix list: (1) start higher and further, pitch up so a sky + skyline + Seine band takes the top 25 % and the yard is dressed (girder stacks, carts, forge smoke) instead of bare dirt; keep the legs and the table in frame; (2) move the pier wall out of the Eiffel line, cream plans on a light wood table, nothing blue/black in the bottom 30 %; (3) move the lamp pole off his head line.

## s11 PASS (notes). Round-3 list:
- R3-1 giant rivet reads as an orange mushroom: PARTLY FIXED. Now a grey-mauve iron dome + fat shank held sideways in his fist (g805-g820); at phone size it reads as a big bolt/mallet. NOTE: colour is mauve-grey, not iron/red-lead; punch-in speed lines read.
- R3-2 black unlit box g820-821: FIXED (no black slab in g817-g825).
- R3-3 ground/sand 40-50 % g823-841 with no character: FIXED to ~25-30 % (sky + leg/crane dominate g825-g845). NOTE: g745-g805 sand ~30 % and g850-g905 floor ~28-33 % (carriers' dark ground + timber); g835-g840 is an empty sky/yard flight without Eiffel or a character (~0.3 s).
- R3-4 rivet toss/catch only a small spark: PARTLY FIXED. g925-g933 an orange-hot block arcs from the thrower into the grey bucket held by the catcher (visible at 360x640), catcher cheers g935-g945 with the bucket overhead (open shouting mouth, not a quote: NOTE). Tongs are not readable (NOTE).
- R3-5 p90 15.45 from three sweeps: NOTE, frames sharp; auto flags g836-838 and g917 only.
- Beats on screen: fence laugh + point (g745-g800), punch-in "ไอ้ช่างหมุด" g802-g815, girder stack with two carriers (g848-g905), toss/catch (g917-g945), three stage jumps g948/g969/g985 (platform 1, platform 2, finished tower), end on the whole tower g985-g1003 (sat/vivid pass). No cut inside (qa_stats2 shot count 6 = fast flights, auto finds no pop). Streak: all different camera angles.

## s15 PASS. Round-3 notes: official face ~33-35 % for < 1 s (g1009-g1030, hat included ~36 %: punctuation-length), Eiffel head ~35 % g1078-g1093 (0.5 s). Permit held by visible hands; EXPOSITION UNIVERSELLE 1889 banner readable to ~g1075; tricolours in the crowd are vertical blue-white-red; sweat + worried swap g1066-g1069; luma 86.8 (floor 85, close); p90 11.33 within 10 % of 12 (NOTE). Foreground gent back card bottom-left ~15 % never over a face. Mouths closed. Fist holding the paper is a dark ball (NOTE).

## s23 PASS. Round-2 list:
- 1 bowler a flat black dish at chest height: FIXED. g1706-g1738 the bowler is held overhead on a raised arm, bare head, proud closed-eye smile; it still reads as a flat dark disc (NOTE: arm barely visible, brim crosses behind the official's top hat g1714-g1738, no face covered).
- 2 official walks out of frame: FIXED. He stays in frame the whole take (steps back, right edge < 720), document hand-over g1664-g1684 visible, doc moves to Eiffel's other hand.
- 3 Eiffel cut at thighs / tower leaves frame: FIXED enough. He is shown to the thighs at the end (head ~20-25 %), banner + lattice stay behind him; nothing half-cut by a frame edge.
- 4 p90 11.45: FIXED (12.25).
- Flags vertical tricolours, crowd bobbing, no black bars/lamp-post, ground < 25 %, handles ok.
