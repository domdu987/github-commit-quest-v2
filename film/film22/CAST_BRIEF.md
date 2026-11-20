# Film 22 cast brief (builder: Sonnet) -> film/v3/cast22/
Film: "ไอ้ช่างวงจร", Harry Beck's Underground diagram, London 1931-33. Read film/film22/WORLD.md, film/film22/script/script_th.txt, film/QA_TEAM.md §G and §I, film/v3/cast10/API.md (the newest cast module on this branch) and film/v2/puppet/API.md. Look at film/ref_shorts/R3_sheet.jpg and R5_sheet.jpg for how the reference characters act (clear poses, props in hand, big readable expressions).

PROJ = /home/user/github-commit-quest-v2/film. Build `film/v3/cast22/cast22.py` the way cast10 extends cast9: import cast10 (which chains the earlier casts and v2/puppet), add new CAST entries, pose keys and props through wrappers, and never edit an earlier module. Also write `API.md`, `test_cast22.py` (prints ALL OK; earlier casts' poses must stay byte-identical, as cast10's test checks) and `sheet.jpg` (every member in every STORY22 pose, labelled, on a mid-grey and on a dark-blue background so the rim/ink reads on both).

## Cast (head D = 1, the usual proportions; 1930s London)
| key | look |
|---|---|
| `beck` | Harry Beck, the hero: slim, about 3.1 D; neat dark side-parted hair, **round wire glasses**, clean-shaven, white shirt with **rolled sleeves** and black sleeve garters, a dark grey **waistcoat**, a **red tie** (signature colour), grey trousers, a pencil behind the ear. Quiet, earnest; mostly calm or focused, small proud smile at the end. |
| `official` | the invented publicity official (the mocker): **stout**, about 3.4 D; balding with a comb-over, a big ginger **handlebar moustache**, ruddy cheeks, a navy **pinstripe three-piece suit** with a gold **watch chain**, a yellow **bow tie**, a carnation. Pompous. Expressions: smug, big laugh (face goes red), sneer, shock (jaw drop, eyes wide, sweat drops), sulky defeat. |
| `clerk_a`, `clerk_b`, `clerk_c` | publicity-office clerks: a thin young man with slicked hair and a green eyeshade, a woman typist with a 1930s bob and a cardigan, a chubby older man with a bald head and spectacles; all laugh at Beck. |
| `pass_man` | passenger: grey overcoat, **bowler hat**, umbrella or briefcase, a newspaper. |
| `pass_woman` | passenger: a **cloche hat**, a red or teal coat, a handbag. |
| `pass_child` | a child in a school cap and shorts with knee socks. |
| `old_gent` | an elderly gentleman with a white beard, a monocle or magnifying glass, squinting. |
| `porter` | Underground staff: navy uniform with a peaked cap and a red-blue badge, handing out maps, wheeling crates. |

Crowd: a helper `crowd_member(i, pose)` that re-colours/re-hats the passengers (8+ variants) so crowds never look cloned.

## Props (drawn on the cards, held in the hands with the anchors)
ruler, fountain pen, 45° set square, T-square, rolled drawing (white paper, coloured lines peeking at the end), a big diagram sheet (flat card, can be waved), a red rubber stamp, a **small folded pocket map** (cover: the red-blue roundel and "UNDERGROUND"; open: a bright little diagram in red/blue/green/yellow), knife and fork, a napkin tucked in the collar, a letter marked NOTICE, a newspaper, a briefcase, an umbrella, a teacup.

## STORY22 poses (name -> what it must read as; add more if useful). Talking poses must accept `mouth=talk_mouth(...)`.
- beck: `beck_rule_line` (ruler on the board, pen drawing, leaning in), `beck_set_square` (45° square held up), `beck_hold_circuit` (holds a circuit sheet beside him, looks at it), `beck_thumb_push` (pushes a point on the board with his thumb), `beck_carry_roll` + walk cycle with the roll under his arm, `beck_present_roll` (lays the roll on a desk, hopeful), `beck_sag` (shoulders down, walking away), `beck_knock`, `beck_read_notice` (reads the NOTICE letter, sighs), `beck_proud` (small smile, arms folded).
- official: `off_sit_glance` (at his desk, glancing at the sheet), `off_stamp` (stamp raised high), `off_laugh_back` (rocking back, laughing, red face; talking), `off_wave_sheet` (waves the diagram, talking), `off_eat_mime` (holds the sheet to his open mouth as if biting, talking), `off_toss_drawer` (flicks the sheet into a drawer), `off_smug_rub` (rubbing hands, smug, talking), `off_peek` (peeks from behind a pillar or newspaper), `off_jaw_drop` (shock), `off_buried_eat` (napkin, knife and fork, a map on the fork, puffed cheeks, sweat, mouth closed).
- clerks: `clerk_type`, `clerk_laugh_point`, `clerk_laugh_belly`, `clerk_sit`.
- passengers: `pass_walk` cycle, `pass_squint` (nose close to a wall map), `pass_unfold_map`, `pass_read_map`, `pass_tap_map` (finger on the map), `pass_point`, `pass_smile_board` (confident step toward the train), `pass_bump` (bumped, hat askew).
- porter: `porter_hand_map`, `porter_push_crate`.

## Rules
- Flat unlit 2D puppets; ink, rim (set the rim on the side away from the key) and expression drawings as the earlier casts do; only quoted speakers move mouths.
- Clothes in saturated period colours (no grey mush): the official's navy + yellow + gold, Beck's red tie, passengers in reds, teals, mustard, bottle green.
- Head width, proportions and ink weight consistent with cast10 so the stage system and set scale work unchanged.
- Do not commit; the director commits. Report the API summary and the sheet path.
