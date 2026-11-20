# s12 QA (shots 29-30, g 1695..1868, first_g 1689, 186 frames, 720x1280, 12 samples + OIDN)

take.mkv is stored as take.mkv.partaa/ab (cat them back together).

## Numbers
- qa_auto: PASS (`QA_AUTO.md`), magenta 0.0 %. Its note "no visible change at g 1789" is a metric quirk: the hard cut 29 -> 30 at g 1789 is plainly visible (diff 35).
- rhythm (`film17/rhythm.py --first_g 1689 --cuts 1789`): in-shot median **4.42**, p90 **13.89** (draft was 6.39 / 15.05).

## Actions animated (plan rows 29-30)
- 29: Bertillon raises the record card (arm rises over g 1689-1719, then bobs; proud expression; the card is a prop in his hand). Behind him dupont wears a grey false beard (own cast entry `dupont_fb`) that dissolves out g 1722-1756 to the clean-shaven dupont; the card does not change. Slow push + lateral slide + reframe snap at g 1730 (14 f).
- 30: three groups of gendarme + thief walk toward camera down the aisle (march cycle legs, stop g 1816-1836); Bertillon points (arm pulses); 14 drawers open one after another from g 1792 and 224 cards pop out and hover along the aisle. High crane pull-out with a snap at g 1822 and a counter-move at g 1850.
- Mouths: no quote in these shots; every pose keeps one fixed closed/smile shape, no lip-sync.

## Self-check (6 fps over the take, cut g 1786-1792 inspected)
- Heads above y 880: yes in all frames. Bertillon head centre ~0.5 H in shot 29. Props held: card in hand. Dust halved (dust=0.45); light shafts do not cross any character.
- Shot 30 figures are 60-250 px tall (wide pull-out, intended); the swarm of cards fills the lower aisle by the end.
- Dissolve-in handle: 6 frames each side rendered in 3D.
