# -*- coding: utf-8 -*-
"""Writes the edited narration_ep1.{json,md}, shots_ep1.{json,md} and numbers.json (for PRODUCTION_PLAN.md). No bpy, no network."""
import json, os, re, edit
from collections import Counter, OrderedDict
D = edit.D
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, S, smap, xmap = edit.build()
i = lambda d: smap[d]          # draft sentence id -> edited id
x = lambda d: xmap[d]          # draft shot id -> edited id
tc = lambda t: "%d:%05.2f" % (t // 60, t % 60)
SCN = {"02": "SCENE 02 (rest) คนที่กลับมา", "03": "SCENE 03 รถกู้ภัยคันสุดท้าย", "04": "SCENE 04 สิ่งที่ต้องทิ้ง", "05": "SCENE 05 ลูกสาว", "06": "SCENE 06 ประตูที่ไม่เปิด"}
WHO = {"narr": "narration", "kong": "ก้อง (line)", "crew": "น้องในทีม (line)", "james": "เจมส์ (line)", "praew": "หมอแพรว (line)", "tos": "คุณทศ (line)", "namnuea": "น้ำเหนือ (line, on the phone)", "guard": "รปภ. โรงพยาบาล (line)"}
# measured 2026-11-26 07:32 from v10/film/out/final_720x1280/log_*.jsonl (530 frames of the hook final): 100 % 68.2 CPU s (200 frames), 75 % 36.6 (330 frames)
COST = OrderedDict([("A", 68.2), ("B", 36.6), ("C2", 32.0), ("C1", 2.0)])
WALL = 1.08 / 4      # wall h per CPU h: 4 workers, 8 % over CPU on the shared cores (72.4/68.2, 39.9/36.6)
ALLOW = 1.35         # audit: 20 % re-renders + 15 % crowds and new sets
DRAFT = 10.3         # CPU s per frame at 360x640 (README, draft v3)
# ---------------------------------------------------------------- asset register
SETS = OrderedDict([
 ("X1",  dict(what="v11 expressway, the hook's rescue zone as built (wreck, rescue truck, work lamp, jam, skyline). Dressing for SCENE 02: one hatchback's lamps on an alarm rhythm, a window-glass burst.", status="exists + dressing", days=0.25)),
 ("X1s", dict(what="X1 plus the overturned sedan 40 D behind the truck, out of the hook cameras' view (to be checked against S03-S05, S24). `V.car` sedan rolled onto its side, shot from the roof and windscreen side only: no underside is built.", status="dressing", days=0.4)),
 ("X2",  dict(what="The same deck 150 D further on: a `truck6` box truck slewed across the three lanes (bevel pass, hazards), the stair gate and one lamp at the left barrier, a taxi with a smashed window against the rescue truck's left side, the rescue truck placed here with its lights on its root.", status="dressing", days=0.5)),
 ("X2c", dict(what="The rescue truck's exterior as a hero: an opening crew door (`split_door`), see-through glass onto the cab shell, a light bar that can go dark, the body rocking on its root. It never drives in an exterior shot.", status="new (from `V.rescue_truck`)", days=0.75)),
 ("CAB", dict(what="Rescue truck crew cab interior: two front seats, rear bench, console with the siren switch, streaked windows, roof raised so seated puppets keep full size; the equipment wall behind the bench (roll shutter, one code-drawn shelf texture, four real props). The shell and camera travel along the shoulder in two shots.", status="new", days=1.25)),
 ("UND", dict(what="Service stair (barrier gap, gate, one flight-and-landing module instanced on a pier) and the street under the expressway reduced to what the dark shows: wet ground, puddles, rain curtains at the deck edges, one far sodium lamp, parked-car silhouettes. Piers and slab underside exist.", status="new", days=2.0)),
 ("RIV", dict(what="Riverside hospital seen through its gate: lit facade (tower window textures), wall, sliding gate of bars with chain, booth light, plain lit cross, river plane with object index 1, a street stub with one lamp. People inside are silhouettes of the extras.", status="new", days=1.25)),
 ("SITE", dict(what="Building site: corrugated hoarding with a bent panel, a bare concrete hall (floor, six columns, slab, puddles), the frame outside as a silhouette. Same file as RIV.", status="new", days=1.0)),
 ("2D",  dict(what="Drawn full frame in SVG and composited in the conform: the watch (four states), phone screens (map, lock, incoming, call, lost), black, end card.", status="new drawings", days=0.5)),
])
CAST = OrderedDict([
 ("kong_wet", dict(what="exists; add the wristwatch, the crowbar on the pack and in two hands", days=0.25)),
 ("driver", dict(what="exists", days=0)),
 ("extras", dict(what="exists (10 roles); the green rider is taken out of the set", days=0)),
 ("crew_bitten / crew_dying / crew_infected", dict(what="new variants of `crew_wet`: wound on the side the hook's final S21-S24 show, three grey steps, the driver's eyes and jaws", days=0.5)),
 ("infected(extras)", dict(what="new transform (skin, eyes, torn cloth, claw hands) on the ten roles, plus a silhouette mode; at most twelve distinct figures in a frame", days=0.5)),
 ("james_wet", dict(what="new, from `crew` proportions and the rider outfit; helmet, no delivery box in EP.1", days=0.5)),
 ("praew_wet", dict(what="new: bun, coat layer, stethoscope, blue gloves; to be measured on the sheet first", days=1.0)),
 ("tos_wet / tos_torn", dict(what="new, from `driver` proportions; glasses, navy jacket; the tear and cut tied to the anatomical left forearm", days=0.75)),
 ("guard", dict(what="new minor: cap, pale blue shirt, torch", days=0.25)),
])
CYCLES = OrderedDict([
 ("survivor run", dict(what="about 2.4 m/s, planted, for Kong, Praew, Tos, James", days=0.4)),
 ("infected sprint", dict(what="about 3.4 m/s, side-on, forward lean, phase offsets", days=0.3)),
 ("roof run and jump down", dict(what="James and the junior; planted on roof points from `F.top`", days=0.4)),
 ("support walk", dict(what="Kong walking the junior (two figures locked at the shoulder)", days=0.2)),
 ("stairs down", dict(what="walk with one tread of drop per step; wide shot only", days=0.25)),
 ("slam loop", dict(what="three drawings on twos, hands on steel or glass", days=0.15)),
 ("crowd waist-up run", dict(what="bob and arm swing for figures whose feet are hidden by cars", days=0.1)),
 ("sleeve snag and clamp", dict(what="Tos, left arm", days=0.2)),
])
# every shot's assets: cast by name in the action text, props and cycles by hand (draft shot ids)
TAG = [(r"\bKong\b", "kong_wet"), (r"\b[Jj]unior\b", "crew variants"), (r"\bPraew\b", "praew_wet"), (r"\bTos\b", "tos"), (r"\bJames\b|\brider\b", "james_wet"), (r"\bguard\b", "guard"),
       (r"\bhorde\b|\b([Aa]n|[Tt]hree|two|dozen|running|every running) infected\b|infected (woman|running|figure)", "infected(extras)"), (r"\bextras\b|silhouettes|fleeing|people keep", "extras")]
MAN = OrderedDict([
 ("driver", "S25 S27 S28 S29 S30 S40"), ("tos", "S111"), ("infected(extras)", "S162 S147"),
 ("watch card", "S26 S36 S43 S46"), ("phone screens", "S123 S125 S128 S131 S133"), ("alarm lamps", "S28 S29 S30 S40"), ("gauze stain", "S34 S35"),
 ("hook macro S08/S09", "S72 S145"), ("flare prop + light", "S107 S108 S109 S114"), ("crowbar", "S105 S113 S118 S119 S160 S164 S165"),
 ("survivor run", "S28 S70 S76 S77 S79"), ("infected sprint", "S59 S83 S109 S162"), ("roof run and jump down", "S54 S55 S56 S75 S77 S78 S94"), ("support walk", "S31"),
 ("stairs down", "S114"), ("slam loop", "S80 S81 S96 S98 S101 S102 S109"), ("crowd waist-up run", "S58 S68 S79 S89 S94"), ("sleeve snag and clamp", "S110 S111 S112"),
])
NOT = {"infected(extras)": "S69 S25"}
NEWTAG = {"crew variants", "praew_wet", "tos", "james_wet", "guard", "infected(extras)", "watch card", "phone screens", "alarm lamps", "gauze stain", "flare prop + light", "crowbar"} | set(CYCLES)
for s in S:
    assert s["set"] in SETS, s["set"]
    tags = [t for (rx, t) in TAG if re.search(rx, s["action"]) and s["draft_id"] not in NOT.get(t, "").split()] if s["set"] != "2D" else []
    for t, ids in MAN.items():
        if s["draft_id"] in ids.split() and t not in tags: tags.append(t)
    s["assets"] = [s["set"]] + tags
for t, ids in MAN.items():
    for d in ids.split(): assert d in xmap and "(cut)" not in xmap[d], (t, d)
for c in CYCLES: assert c in MAN, c
# ---------------------------------------------------------------- totals
cf = Counter(); cn = Counter(); setf = Counter(); setn = Counter(); scf = OrderedDict();
for s in S:
    cf[s["cls"]] += s["frames"]; cn[s["cls"]] += 1; setf[s["set"]] += s["frames"]; setn[s["set"]] += 1
    scf.setdefault(s["scene"], Counter())[s["cls"]] += s["frames"]
cpu = lambda c: sum(c[k] * COST[k] for k in c) / 3600.0
end = S[-1]["t1"]; last_word = N[-1]["end"]
chars = sum(s["chars"] for s in N); billed = sum(s["chars_billed"] for s in N)
ncap = sum(len(s["captions"]) for s in N); nem = sum(1 for s in N for c in s["captions"] if "emph" in c)
voiced = sum(s["dur"] for s in N)
emph_table = [[c["text"], c["emph"], c["colour"]] for s in N for c in s["captions"] if "emph" in c]
HOOK_EMPH = {"คนเจ็บไม่ตอบสนอง", "เฮ้ย!", "ก็เงียบไป", "ฝนถล่มกรุงเทพฯ", "รถชนกันเป็นแพ", "ก้อง", "เจ้าหน้าที่กู้ภัย", "เครื่องตัดไร้สาย", "แบตเต็ม 3 ขีด", "4 สาย", "น้ำเหนือ", "วันนี้พ่อสัญญา", "ทุกครั้งเลย...", "แล้วก็วางสาย", "ไม่ขยับเลยสักนิด", "เงยหน้าขึ้น", "มันพุ่ง", "เข้ากัดทันที", "อีก 60 วินาที", "จะไม่ใช่คน"}
allcaps = [c["text"] for s in N for c in s["captions"]]
clash = sorted(set(c for c in allcaps if c in HOOK_EMPH))
scene_rows = []
for sc, c in scf.items():
    xs = [y for y in S if y["scene"] == sc]; fr = sum(c.values()); h = cpu(c)
    scene_rows.append(OrderedDict(scene=sc, t0=xs[0]["t0"], t1=xs[-1]["t1"], seconds=round(xs[-1]["t1"] - xs[0]["t0"], 2), shots=len(xs), frames=fr, A=c["A"], B=c["B"], C2=c["C2"], C1=c["C1"],
                                  cpu_h=round(h, 1), wall_h=round(h * WALL, 1), wall_h_allow=round(h * WALL * ALLOW, 1), cpu_h_allow=round(h * ALLOW, 1),
                                  draft_cpu_h=round((fr - c["C1"]) * DRAFT / 3600.0, 1), draft_wall_h=round((fr - c["C1"]) * DRAFT / 3600.0 * WALL, 1),
                                  chars=sum(s["chars"] for s in N if s["scene"] == sc), chars_billed=sum(s["chars_billed"] for s in N if s["scene"] == sc), sentences=sum(1 for s in N if s["scene"] == sc),
                                  first_shot=xs[0]["id"], last_shot=xs[-1]["id"], f0=xs[0]["f0"], f1=xs[-1]["f1"], sets=sorted(set(y["set"] for y in xs))))
tot_cpu = cpu(cf)
A_med = sum(s["frames"] for s in S if s["cls"] == "A" and not any(k in s["size"] for k in ("CU", "INSERT", "OTS")))
numbers = OrderedDict(running_time=tc(end), seconds=round(end, 2), frames_total=S[-1]["f1"], frames_new=S[-1]["f1"] - S[0]["f0"], shots=len(S), mean_shot_s=round((end - D.HOOK_END) / len(S), 2),
    frames_by_class=dict(cf), shots_by_class=dict(cn), cost_cpu_s_per_frame=COST, cpu_h_by_class={k: round(cf[k] * COST[k] / 3600.0, 1) for k in COST},
    cpu_h=round(tot_cpu, 1), wall_h=round(tot_cpu * WALL, 1), cpu_h_allow=round(tot_cpu * ALLOW, 1), wall_h_allow=round(tot_cpu * WALL * ALLOW, 1),
    draft_pass_cpu_h=round((sum(cf.values()) - cf["C1"]) * DRAFT / 3600.0, 1), draft_pass_wall_h=round((sum(cf.values()) - cf["C1"]) * DRAFT / 3600.0 * WALL, 1),
    A_medium_frames=A_med, A_medium_saving_cpu_h=round(A_med * (COST["A"] - COST["B"]) / 3600.0, 1),
    sentences=len(N), captions=ncap, emph=nem, chars_spoken=chars, chars_billed=billed, last_word=round(last_word, 2), voiced_s=round(voiced, 1),
    scenes=scene_rows, frames_by_set=dict(setf), shots_by_set=dict(setn),
    set_days=sum(v["days"] for v in SETS.values()), cast_days=sum(v["days"] for v in CAST.values()), cycle_days=sum(v["days"] for v in CYCLES.values()),
    cut_sentences=[d for d in edit.NE if edit.NE[d] is None], cut_shots=[d for d in edit.SE if edit.SE[d] is None], hook_caption_clash=clash)
json.dump(numbers, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "numbers.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------------------------------------------------------- narration json
meta = OrderedDict(
    title="DEAD ZONE 09 EP.1, narration after the hook title (EDITED; the screenwriter's draft is narration_ep1_draft.json)", voice="Ohm (one narrator: third person + the short lines)",
    hook=dict(occupies=[0.0, D.HOOK_END], bite_at=D.BITE, script="audio/narr_ohm/script.json (s01-s16)"),
    rate=dict(source="audio/narr_ohm/captions_timing.json", overall_chars_per_s=D.OVERALL, mid_caption_chars_per_s=D.CPS, sentence_tail_s=D.TAIL,
              char_definition="Thai characters incl. vowel and tone marks, numbers spelled out, without spaces and punctuation",
              model="caption = max(0.42, chars / 12.58) s; the last caption of a sentence + 0.38 s; then the pause written per sentence"),
    episode=dict(first_new_word=N[0]["start"], last_word_ends=round(last_word, 2), picture_ends=round(end, 2), running_time=tc(end), frames_total=S[-1]["f1"], frames_new=S[-1]["f1"] - S[0]["f0"]),
    count=dict(sentences=len(N), captions=ncap, emphasised_captions=nem, chars_spoken=chars, chars_with_spaces_and_punctuation=billed, hook_chars_spoken=573, hook_chars_with_spaces=609,
               draft_sentences=89, draft_chars_spoken=2685, draft_chars_with_spaces_and_punctuation=2856, draft_running_time="5:34.62"),
    id_map_draft_to_edited=smap, emph_for_finish_py=emph_table, sentences=N)
json.dump(meta, open(os.path.join(OUT, "narration_ep1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------------------------------------------------------- narration md
m = []
m.append("# DEAD ZONE 09 / เขตปิดตาย 09, EP.1: narration after the hook title (edited)\n")
m.append("One voice (Ohm) tells the story in the third person and also speaks the short lines, as in the hook (`audio/narr_ohm/script.json`, s01-s16). Ids continue at s17. Lower-case `s` = sentence, upper-case `S` = shot. This is the script editor's version: the screenwriter's draft is kept as `narration_ep1_draft.md` / `.json`, ids were renumbered after the cuts, and every row carries its draft id. Machine copy: `narration_ep1.json`. Generator: `_gen_v2/edit.py` (the edit tables, on top of `_gen/narr.py`) and `_gen_v2/write2.py`.\n")
m.append("## Numbers\n")
m.append("| | edited | draft |\n|---|---|---|")
m.append("| Hook | 0:00.00 - 0:53.32 (bite at 0:43.80, title 0:50.72) | same |")
m.append("| New narration | %s - %s, %d sentences, %d captions (%d with a coloured key word) | 89 sentences, 227 captions (61) |" % (tc(N[0]["start"]), tc(last_word), len(N), ncap, nem))
m.append("| Episode running time | **%s** (%d frames at 24 fps; new picture %d frames) | 5:34.62 (8,031; 6,751) |" % (tc(end), S[-1]["f1"], S[-1]["f1"] - S[0]["f0"]))
m.append("| Characters to record | **%d** spoken Thai characters (numbers spelled out, no spaces or punctuation); **%d** counting spaces and punctuation, which is how a text-to-speech service bills | 2,685 / 2,856 |" % (chars, billed))
m.append("| Voice time | %.1f s of sentences in %.1f s of new picture | 236.9 s in 281.3 s |" % (voiced, end - D.HOOK_END))
m.append("| Speaking rate (measured from the hook) | 11.04 characters per second with pauses; 12.58 inside a sentence; a sentence-final caption runs 0.38 s longer | same model |")
m.append("| Estimate error | The hook's sentences ran from 6.8 to 18.1 characters per second, so single lines can be 30 % off. Times are intended starts; the cut follows the real recording, as the hook did | |")
m.append("")
m.append("## What the edit changed and why\n")
m.append("Checks asked for, and their result:\n")
m.append("- **The hook's promise is paid on screen.** The hook's last words are 'อีก 60 วินาที เพื่อนของเขา จะไม่ใช่คน อีกต่อไป' (bite at 0:43.80). The first words after the title are 'เหลืออีก 50 วินาที' at 0:53.62, 9.8 s after the bite. '30 วินาที' falls at 1:13.80 (30.0 s after) and '10 วินาที' at 1:33.80 (50.0 s after). The eyes open on 'ลืมตา' at about 1:41.5, 57.7 s after the bite: inside the rule's 60 seconds, in real time, with no cut that skips time. The count is visible four times as Kong's watch (%s, %s, %s, %s). The watch was redesigned: no digits, one red second hand that has to come back round to a drop of blood on the 12 mark. A viewer reads it without reading." % (x("S26"), x("S36"), x("S43"), x("S46")))
m.append("- **First 10 seconds after the title (0:53.3 - 1:03.3).** Three things land: the countdown restated (%s), the fight (%s), and a question (%s: it drops a victim to go to a noise; why?). That question is answered by the siren at %s and used by the heroes at %s. No line in this stretch describes scenery." % (i("s17"), i("s18"), i("s19"), i("s55"), i("s67")))
m.append("- **Dialogue against the screenplay.** All 20 screenplay lines used are word for word: %s. One line is invented, the guard's (%s), because the screenplay only says he refuses. Kong says nothing in the phone call (%s-%s), which is what the screenplay has. In the hook's manner no line is attributed in words: each plays on a close shot of its speaker, or on Kong listening to the phone." % (", ".join(i(k) for k in ("s21", "s25", "s26", "s31", "s48", "s56", "s59", "s60", "s61", "s73", "s74", "s75", "s77", "s80", "s81", "s82", "s86", "s98", "s99", "s100")), i("s90"), i("s80"), i("s82")))
m.append("- **The cliffhanger.** The last words are 'ก้องยกชะแลงขึ้น / แต่เขาจะฟาด ใคร', then black on 'ใคร' (%s-%s). Nothing follows but the end card." % (i("s104"), i("s105")))
m.append("")
m.append("Lines fixed because they contradicted the screenplay, the world rules or the hook:\n")
m.append("- **Battery.** The draft made the third bar blink (draft s47, and the gauge at the chain). The bible says three bars in EP.1 and the hook says 'แบตเต็ม 3 ขีด'. The bar is steady again; the hook's set-up is paid at the gate instead (%s: 'แบตยังเต็ม 3 ขีด ตัดโซ่ขาดแน่', and he still cannot use it)." % i("s91"))
m.append("- **The 60 seconds at the end.** Draft s101 ('ก้องรู้ดี ว่า 60 วินาที มันสั้นแค่ไหน') put a 60-second clock on Tos. Tos has been with the group for minutes; by rule 1 a bite would have turned him long before. %s now says only what Kong has seen ('น้องของเขา ใช้เวลาแค่ 60 วินาที'). The audience, who watched the glass cut him, knows more than Kong: that is the cliffhanger's irony, and the rule is not bent." % i("s101"))
m.append("- **The crowbar.** The screenplay has Kong push the driver off with a crowbar in SCENE 02, then take a crowbar from the truck in SCENE 04. He cannot do both. He shoves with the cutter that is already in his hands (%s), and the crowbar stays a SCENE 04 choice that pays off in the last shot." % i("s18"))
m.append("- **The roof chase.** In the draft the junior chases James over the roofs for 45 s without catching him, against rule 2. Now he loses James behind the bus (rule 7, %s) and is brought back by James's own shout (rule 3, %s). No line changed; the shot list carries it." % (x("S56"), x("S78")))
m.append("")
m.append("Cut or tightened for pace (every row below says which):\n")
m.append("| draft id | draft text | now | reason |\n|---|---|---|---|")
dj = json.load(open(os.path.join(OUT, "narration_ep1_draft.json"), encoding="utf-8"))
dtext = {s["id"]: s["text"] for s in dj["sentences"]}
for s in dj["sentences"]:
    d = s["id"]
    if d in edit.NE and edit.NE[d] is None:
        why = {"s39": "the hook already ends on this crane 75 s earlier; the shut hospital and the evacuation bus say 'everywhere' later", "s47": "merged into the sentence before it; the blinking bar contradicted the bible",
               "s76": "said what the insert of his arm shows", "s84": "bookkeeping; the sentence before it now says it with 'รับปาก'", "s96": "the picture shows it"}[d]
        m.append("| %s | %s | *cut* | %s |" % (d, dtext[d], why))
    elif d in edit.NE and "why" in edit.NE[d]:
        new = next(q for q in N if q["draft_id"] == d)
        m.append("| %s | %s | %s: %s | %s |" % (d, dtext[d], new["id"], new["text"], edit.NE[d]["why"]))
for q in N:
    if q["edit"].startswith("new"): m.append("| (new) | | %s: %s | %s |" % (q["id"], q["text"], q["edit"][5:]))
m.append("")
m.append("The episode is now %s, 16 s shorter than the draft and 1:21 under the screenplay's 06:40. Nothing was added to fill the time: see PRODUCTION_PLAN.md, decision 2.\n" % tc(end))
m.append("## Retention structure\n")
m.append("| Loop | Opened | Kept alive | Paid off |\n|---|---|---|---|")
m.append("| 60 seconds | hook s16 | %s / %s / %s countdown, four watch inserts; %s (Kong thinks it is over) | %s-%s (eyes open); %s at the end |" % (i("s17"), i("s23"), i("s30"), i("n1"), i("s32"), i("s33"), i("s101")))
m.append("| Sound and light call them | %s car alarm | %s (out of sight = lost) | %s-%s siren; %s rule said aloud; %s-%s flare; %s phone light; %s the cutter not used; %s the shouting |" % (i("s19"), i("s35"), i("s54"), i("s55"), i("s58"), i("s66"), i("s67"), i("s79"), i("s92"), i("s102")))
m.append("| The battery | hook s04 | | %s at the chain: full, and useless |" % i("s91"))
m.append("| Kong's promises | hook s06-s10 | %s-%s promise two | %s the junior at the glass; %s-%s the third is asked for and never given |" % (i("s26"), i("s27"), i("s51"), i("s82"), i("s83")))
m.append("| The daughter's call | hook s05-s10 | %s no call yet | %s-%s the call; the pier is the series goal |" % (i("s78"), i("s79"), i("s83")))
m.append("| The rider | %s | | %s-%s |" % (i("s36"), i("s48"), i("s49")))
m.append("| Tos's wound | %s-%s | %s (picture: his arm), %s | %s-%s; left open by %s |" % (i("s69"), i("s70"), i("s75"), i("s90"), i("s97"), i("s100"), i("s105")))
m.append("| What was left behind | %s-%s | %s-%s | later episodes |" % (i("s63"), i("s65"), i("s73"), i("s75")))
m.append("")
m.append("Every scene clip ends on an open question, so each delivered clip holds on its own: 02 'นี่ไม่ใช่อุบัติเหตุ อีกต่อไปแล้ว'; 03 James's way out, unseen; 04 'ยังไม่มีสาย จากลูก'; 05 he follows the others, away from her; 06 'ใคร'.\n")
m.append("## Script\n")
m.append("Caption split is marked with `/`. **Bold** = the coloured word (amber = fact, red = threat). Start and length are on the episode clock.\n")
cur = None
for s in N:
    if s["scene"] != cur:
        cur = s["scene"]; ss = [q for q in N if q["scene"] == cur]
        m.append("\n### %s (%s - %s)\n" % (SCN[cur], tc(ss[0]["start"]), tc(ss[-1]["end"])))
        m.append("| id | draft | start | s | who | captions | chars | effect cue | shots | note |\n|---|---|---|---|---|---|---|---|---|---|")
    caps = " / ".join((c["text"].replace(c["emph"], "**" + c["emph"] + "**") + (" (%s)" % c["colour"]) if "emph" in c else c["text"]) for c in s["captions"])
    mark = "" if s["edit"] == "kept" else (" *(retimed)*" if s["edit"] == "retimed" else (" *(new)*" if s["edit"].startswith("new") else " *(edited)*"))
    m.append("| %s | %s | %s | %.2f | %s | %s | %d | %s | %s | %s%s |" % (s["id"], s["draft_id"], tc(s["start"]), s["dur"], WHO[s["speaker"]], caps, s["chars"], s["fx"] or "-", " ".join(s["shots"]), s["beat"], mark))
m.append("\n## Text for the recording (one line per sentence, numbers spelled out)\n")
m.append("Record all five scenes in one session, after the user has approved this text. Each scene is its own file set (`audio/ep1/scNN/`).\n")
m.append("```")
cur = None
for s in N:
    if s["scene"] != cur: cur = s["scene"]; m.append("# scene %s" % cur)
    m.append("%s\t%s" % (s["id"], s["tts"]))
m.append("```")
m.append("\n## Lines for the caption emphasis table (caption, word, colour)\n")
m.append("```")
for a, b, c in emph_table: m.append('("%s", "%s", %s_ASS),' % (a, b, c.upper()))
m.append("```")
m.append("\nThe conform matches on the whole caption text. No new caption carries two different colours. New captions that are also in the hook's table and so take the hook's colour: %s." % (", ".join("`%s`" % c for c in clash) or "none"))
m.append("\n## Mix notes\n")
m.append("- Narration stays clearly above effects, as in the hook mix. One exception by design: the siren after %s plays at full level for 1.2 s in a gap with no words, then ducks under %s." % (i("s54"), i("s55")))
m.append("- The heartbeat pulse (%s-%s, back at %s) is a low effect under the voice, not music." % (i("s17"), i("s28"), i("s101")))
m.append("- Whispered lines (%s-%s) are performed quietly by the narrator, not lowered in the mix." % (i("s73"), i("s77")))
m.append("- No status icons anywhere. The watch, the phone screens, the gauge LEDs and the map are props shown full frame.")
open(os.path.join(OUT, "narration_ep1.md"), "w", encoding="utf-8").write("\n".join(m) + "\n")
# ---------------------------------------------------------------- shots json
js = OrderedDict(episode=dict(fps=24, size="720x1280", hook_frames=[0, 1280], new_frames=[S[0]["f0"], S[-1]["f1"]], running_time=tc(end)),
     note="EDITED by the script editor / line producer; the screenwriter's draft is shots_ep1_draft.json. Shot ids were renumbered; draft_id is on every shot.",
     classes=dict(A="any shot in which a named character's face is read, and the two wound inserts; final tier at 100 % scale", B="wides, crowds, driving, environment, prop and hand inserts with no face; final tier at 75 %",
                  C1="drawn 2D full frame or reuse of rendered frames; no Cycles render", C2="re-uses the hook's jaw / gauge macro staging (S08, S09); final tier 75 %, 4 spp"),
     totals=dict(shots=len(S), frames_by_class=dict(cf), shots_by_class=dict(cn), frames_by_set=dict(setf), frames_by_scene={r["scene"]: r["frames"] for r in scene_rows}, mean_shot_s=numbers["mean_shot_s"],
                 cpu_s_per_frame=COST, cpu_hours=numbers["cpu_h"], wall_hours_4_cores=numbers["wall_h"], cpu_hours_with_35pct_allowance=numbers["cpu_h_allow"], wall_hours_with_35pct_allowance=numbers["wall_h_allow"]),
     scenes=scene_rows, sets=SETS, cast=CAST, cycles=CYCLES, id_map_draft_to_edited=xmap, shots=S)
json.dump(js, open(os.path.join(OUT, "shots_ep1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------------------------------------------------------- shots md
m = []
m.append("# DEAD ZONE 09 EP.1: shot list after the hook (S25-S%d), reconciled with the assets audit\n" % (24 + len(S)))
m.append("Continues `v10/film` (S01-S24, frames 0-1279). Times are the episode clock; frames are film frames (0-based, end exclusive). Every cut sits on a caption start of `narration_ep1.json` unless the cut-on column says it is a picture beat. This is the line producer's version: the screenwriter's draft is `shots_ep1_draft.md` / `.json`; shots were renumbered after the cuts and every row carries its draft id. Machine copy: `shots_ep1.json`. Generator: `_gen_v2/edit.py`, `_gen_v2/write2.py`.\n")
m.append("Frame numbers move when the narration is recorded (single lines can be 30 % off the estimate). Shot ids, classes and assets do not.\n")
m.append("## Totals\n")
m.append("| class | shots | frames | seconds | CPU s / frame | CPU h |\n|---|---|---|---|---|---|")
LAB = (("A", "A: a named character's face is read (and the two wound inserts), 100 %"), ("B", "B: wide, crowd, driving, environment, prop or hand insert, 75 %"), ("C2", "C2: the hook's jaw / gauge macro re-staged, 75 %, 4 spp"), ("C1", "C1: drawn 2D or reused frames, no render"))
for k, lab in LAB: m.append("| %s | %d | %d | %.1f | %.1f | %.1f |" % (lab, cn[k], cf[k], cf[k] / 24.0, COST[k], cf[k] * COST[k] / 3600.0))
m.append("| **all** | **%d** | **%d** | **%.1f** | | **%.1f** |" % (len(S), sum(cf.values()), sum(cf.values()) / 24.0, tot_cpu))
m.append("")
m.append("- Final render: **%.1f CPU h = %.1f wall h** on 4 cores; with the audit's 35 %% allowance (re-renders, crowds, new sets) **%.1f CPU h = %.1f wall h**." % (tot_cpu, tot_cpu * WALL, tot_cpu * ALLOW, tot_cpu * WALL * ALLOW))
m.append("- Costs per frame are measured on the hook final as it ran (530 frames in `v10/film/out/final_720x1280/log_*.jsonl` at 07:32): 68.2 CPU s at 100 %, 36.6 at 75 %. C2 is the README's 31.5 for S09, rounded up. C1 is an allowance for compositing. Wall time is CPU time x 1.08 / 4. None of the new sets has been measured.")
m.append("- %d shots, mean %.2f s (the hook: 2.22 s). The draft list was 143 shots, 6,751 frames and 95.5 CPU h at the README's older 65 / 40 figures, which is 97.2 CPU h at today's measured ones." % (len(S), numbers["mean_shot_s"]))
m.append("- %d of the A frames are mediums. Rendering those at 75 %% would save %.1f CPU h; the standing decision is 100 %% for character shots, so it is not assumed (PRODUCTION_PLAN.md, decision 3)." % (A_med, numbers["A_medium_saving_cpu_h"]))
m.append("")
m.append("| scene | time | shots | frames | A | B | C2 | C1 | CPU h | wall h | wall h with allowance |\n|---|---|---|---|---|---|---|---|---|---|---|")
for r in scene_rows: m.append("| %s | %s - %s | %d | %d | %d | %d | %d | %d | %.1f | %.1f | %.1f |" % (r["scene"], tc(r["t0"]), tc(r["t1"]), r["shots"], r["frames"], r["A"], r["B"], r["C2"], r["C1"], r["cpu_h"], r["wall_h"], r["wall_h_allow"]))
m.append("")
m.append("## What the reconciliation changed\n")
m.append("Shots dropped or redesigned because their asset cost was out of proportion to their screen time (shot ids in this table are the draft's):\n")
m.append("| draft shot | was | now | asset saved |\n|---|---|---|---|")
RECON = [
 ("S61", "second crane over the city (62 f)", "cut with its sentence", "far smoke plumes and extra beacons across the skyline"),
 ("S63", "overturned sedan with a wheel still turning", "sedan seen from the roof and windscreen side only", "an underside (floor pan, exhaust, axles) for a body that has none: about half the audit's 0.75 day"),
 ("S67", "insert of the buckled door flexing (60 f)", "cut; the door edge is in the bottom of Tos's close-up", "a deforming door panel"),
 ("S71, S74", "spreader set to the door (34 f); gauge macro with a blinking bar (64 f)", "cut; S70 cuts straight to the jaw macro", "a blinking-gauge state; one staging"),
 ("S83", "exterior tracking shot of the truck driving off (62 f)", "the same beat from inside, through the side window", "a driving hero truck: turning wheels, body motion, every light following the root (most of the audit's 1.0 day)"),
 ("S85", "high wide of a jack-knifed ten-wheel lorry as the truck brakes into frame", "low wide from behind the stopped truck; the lorry is the set's own `truck6` slewed across the lanes", "a new articulated lorry; a second driving shot"),
 ("S58, S68, S94, S109", "crowds of 20 to 40 running at the lens", "at most twelve distinct figures plus silhouettes; runs toward the lens are waist-up over the bonnets; full-figure runs are side-on", "6-10 new crowd designs and a depth-axis run cycle; keeps the unmeasured crowd inside what one worker's memory is known to hold"),
 ("S104", "nine pieces of rescue gear on shelves", "one drawn shelf-wall texture plus four real props", "seven modelled props"),
 ("S114, S115", "six-flight stair tower; boots insert at 100 % (39 f)", "top two flights side-on in a wide; insert cut", "the full tower (1.5 days became 1.0 with the gate); the one new gait is never under a close lens"),
 ("S121", "Tos alone at a pier (87 f at 100 %)", "cut with its sentence", "1.6 CPU h"),
 ("S130", "Namnuea at a bus window (84 f)", "the others listening to the phone, on the existing dark set", "a bus-window set, her full puppet and a dry variant for one shot"),
 ("S134", "Kong lowers the phone (91 f at 100 %)", "cut with its sentence; the lost-call screen with his reflection carries the beat", "1.7 CPU h"),
 ("S148", "nurse with a child, old man, woman with a drip stand", "the extras as seated silhouettes behind the guard", "three designs, two props"),
 ("S150", "eight-floor frame with scaffolding and torn netting", "the frame as a silhouette, a few scaffold tubes", "netting alpha (the audit's +10-15 % on those shots) and half a day of scaffolding"),
 ("UND as a whole", "a street with shophouse fronts, parked vehicles, lamps, cables, trees (audit: 2.5 days)", "what an almost black frame shows: ground, puddles, rain curtains, one lamp, silhouettes", "about 1.5 days"),
]
for a, b, c, d in RECON: m.append("| %s | %s | %s | %s |" % (a, b, c, d))
m.append("")
m.append("Shots that changed class:\n")
m.append("- %s (the eyes opening) from a separate 2D drawing to class A: the hook's pay-off has to sit in the same rain and light as the shots round it." % x("S47"))
m.append("- %s, %s, %s, %s, %s (gauze, hand, fist on the phone, jaws off the chain, fist on the crowbar) from A to B: hand and prop inserts with no face, the class the draft already gave the gloves on the bars and the finger on the switch." % (x("S35"), x("S41"), x("S138"), x("S149"), x("S160")))
m.append("- %s (palm on the siren switch) from C2 to B: it is the console setup, not a hook macro." % x("S92"))
m.append("- %s (the memory flash) reuses rendered frames of %s." % (x("S159"), x("S47")))
m.append("- New: %s, Kong's face on the new sentence %s." % (x("N1"), i("n1")))
m.append("")
m.append("## Asset register: every set, character and cycle the shots call for\n")
m.append("| set | what | status | builder-days | shots | frames |\n|---|---|---|---|---|---|")
for k, v in SETS.items(): m.append("| %s | %s | %s | %.2f | %d | %d |" % (k, v["what"], v["status"], v["days"], setn[k], setf[k]))
m.append("| **sets** | | | **%.2f** (the audit's list: 11-12) | | |" % numbers["set_days"])
m.append("")
m.append("| cast | what | builder-days |\n|---|---|---|")
for k, v in CAST.items(): m.append("| `%s` | %s | %.2f |" % (k, v["what"], v["days"]))
m.append("| **cast** | Namnuea stays a voice and a phone avatar, as in the hook | **%.2f** |" % numbers["cast_days"])
m.append("")
m.append("| cycle | what | builder-days |\n|---|---|---|")
for k, v in CYCLES.items(): m.append("| %s | %s | %.2f |" % (k, v["what"], v["days"]))
m.append("| **cycles** | each passes the sole-drift check of `walk8.py measure` before a shot uses it. Not needed any more: run toward the lens, lying figure, fall, backward drag, drive and brace | **%.2f** |" % numbers["cycle_days"])
m.append("")
m.append("The last column of every shot row lists its set and the cast, props and cycles it needs. Tags in **bold** do not exist yet and are in the tables above.\n")
m.append("## Screen direction (holds for the whole episode)\n")
m.append("- **Safety is screen right, the threat comes from screen left.** The direction of travel on the expressway, the lorry, the stair, the hospital and the building site are all to the right. The crash zone, the horde and the last runners are to the left.")
m.append("- Profile and tracking shots of the road and the truck are taken from the median side, so the left barrier and the stair gate are in the background.")
m.append("- Three moves go right to left on purpose: the driver thrown at the alarm car (%s-%s), Kong running back to the sedan (%s), and the flare (%s-%s)." % (x("S27"), x("S30"), x("S70"), x("S108"), x("S109")))
m.append("- Dialogue pairs keep one line each: Kong right / junior left in SCENE 02; in the cab the camera stays ahead of the windscreen or on the driver's side; Praew left / Kong right under the expressway; at the gate outside = left, inside = right.")
m.append("- %s-%s: Kong faces the lens with Tos on his right and the gap on his left, so the last eye movement reads as a choice between two screen sides." % (x("S164"), x("S165")))
m.append("")
m.append("## Rules every shot keeps\n")
m.append("- Puppets stay upright and camera-facing. Nobody lies on the ground: the junior sits against the wheel, the knock-down of the screenplay is a stagger against the truck, Tos in the tipped car is a card rolled 80 degrees seen through the windscreen frame.")
m.append("- Every spoken line plays on a close shot of its speaker with lip sync (or on Kong listening, for the phone), because one voice speaks for everyone.")
m.append("- Drawings on twos, camera and lip sync on ones; walks and runs use `gait8` with planted feet; every still pose has breath, blink, rain, beacon or prop motion, and no shot is a held frame with a camera move.")
m.append("- A figure whose feet are in frame never runs toward or away from the lens.")
m.append("- Levels: RAIN 0.2, SPLASH 0.25, HAZE 0.3, TILT 0, DOF 0.25, BLOOM 0.55. Under the expressway and in the building site RAIN is 0 on the actors' plane.")
m.append("- No status icons. Captions as in the hook.")
m.append("- Resumable: one folder per shot, a frame that exists and verifies is skipped; within a scene B and C shots render first, A shots last.")
m.append("")
cur = None
for s in S:
    if s["scene"] != cur:
        cur = s["scene"]; xs = [y for y in S if y["scene"] == cur]
        m.append("\n## %s: %s - %s, %d shots, %d frames\n" % (SCN[cur], tc(xs[0]["t0"]), tc(xs[-1]["t1"]), len(xs), sum(y["frames"] for y in xs)))
        m.append("| shot | draft | time | frames | class | set | size | cast and action | camera | lens | reads in 0.5 s | sound | narration | cut on | assets |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    nar = "; ".join("%s: %s" % (q["id"], " / ".join(q["captions"])) for q in s["narration"]) or "(none)"
    ast = ", ".join(("**%s**" % a) if (a in NEWTAG or (a in SETS and SETS[a]["status"] != "exists + dressing")) else a for a in s["assets"])
    mark = "" if s["edit"] == "kept" else " *(%s)*" % ("new" if s["edit"].startswith("new") else "edited")
    m.append("| %s | %s%s | %s - %s | %d-%d (%d) | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (s["id"], s["draft_id"], mark, tc(s["t0"]), tc(s["t1"]), s["f0"], s["f1"], s["frames"], s["cls"], s["set"], s["size"], s["action"], s["camera"], s["lens"], s["reads"], s["sound"] or "-", nar, s["cut_on"], ast))
open(os.path.join(OUT, "shots_ep1.md"), "w", encoding="utf-8").write("\n".join(m) + "\n")
print(json.dumps({k: v for k, v in numbers.items() if k != "scenes"}, ensure_ascii=False))
for r in scene_rows: print(json.dumps(r, ensure_ascii=False))
print("maps", i("s105"), x("S167"), x("S47"), x("S111"), x("S154"), x("S53"), x("S81"), x("S90"), x("S107"), x("S109"), x("S127"), x("S143"), x("S164"), x("S165"), x("S70"), x("N1"))
