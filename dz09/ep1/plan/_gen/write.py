# -*- coding: utf-8 -*-
import json, os, shots, narr
from collections import Counter, OrderedDict
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, S = shots.build()
tc = lambda t: "%d:%05.2f" % (t // 60, t % 60)
SCN = {"02": "SCENE 02 (rest) คนที่กลับมา", "03": "SCENE 03 รถกู้ภัยคันสุดท้าย", "04": "SCENE 04 สิ่งที่ต้องทิ้ง", "05": "SCENE 05 ลูกสาว", "06": "SCENE 06 ประตูที่ไม่เปิด"}
WHO = {"narr": "narration", "kong": "ก้อง (line)", "crew": "น้องในทีม (line)", "james": "เจมส์ (line)", "praew": "หมอแพรว (line)", "tos": "คุณทศ (line)", "namnuea": "น้ำเหนือ (line, on the phone)", "guard": "รปภ. โรงพยาบาล (line)"}
for s in N:
    s["shots"] = [x["id"] for x in S if any(n["id"] == s["id"] for n in x["narration"])]
end = S[-1]["t1"]; last_word = N[-1]["end"]
chars = sum(s["chars"] for s in N); billed = sum(s["chars_billed"] for s in N)
ncap = sum(len(s["captions"]) for s in N); nem = sum(1 for s in N for c in s["captions"] if "emph" in c)
trim = [s for s in N if s["optional_trim"]]; trim_s = sum(s["dur"] + s["pause_before"] for s in trim)
voiced = sum(s["dur"] for s in N)
emph_table = [[c["text"], c["emph"], c["colour"]] for s in N for c in s["captions"] if "emph" in c]
meta = OrderedDict(
    title="DEAD ZONE 09 EP.1, narration after the hook title", voice="Ohm (one narrator: third person + the short lines)",
    hook=dict(occupies=[0.0, narr.HOOK_END], bite_at=narr.BITE, script="audio/narr_ohm/script.json (s01-s16)"),
    rate=dict(source="audio/narr_ohm/captions_timing.json", overall_chars_per_s=narr.OVERALL, mid_caption_chars_per_s=narr.CPS, sentence_tail_s=narr.TAIL,
              char_definition="Thai characters incl. vowel and tone marks, numbers spelled out, without spaces and punctuation",
              model="caption = max(0.42, chars / 12.58) s; the last caption of a sentence + 0.38 s; then the pause written per sentence"),
    episode=dict(first_new_word=N[0]["start"], last_word_ends=round(last_word, 2), picture_ends=round(end, 2), running_time=tc(end), frames_total=S[-1]["f1"], frames_new=S[-1]["f1"] - S[0]["f0"]),
    count=dict(sentences=len(N), captions=ncap, emphasised_captions=nem, chars_spoken=chars, chars_with_spaces_and_punctuation=billed,
               hook_chars_spoken=573, hook_chars_with_spaces=609, optional_trim_sentences=[s["id"] for s in trim], optional_trim_seconds=round(trim_s, 2)),
    emph_for_finish_py=emph_table, sentences=N)
json.dump(meta, open(os.path.join(OUT, "narration_ep1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---- narration md
m = []
m.append("# DEAD ZONE 09 / เขตปิดตาย 09, EP.1: narration after the hook title\n")
m.append("One voice (Ohm) tells the story in the third person and also speaks the short lines, as in the hook (`audio/narr_ohm/script.json`, s01-s16). Ids continue at s17. Lower-case `s` = sentence, upper-case `S` = shot (the hook's convention). Machine copy: `narration_ep1.json`. Generator: `_gen/narr.py` (text + timing model), `_gen/write.py`.\n")
m.append("## Numbers\n")
m.append("| | |\n|---|---|")
m.append("| Hook | 0:00.00 - 0:53.32 (bite at 0:43.80, title 0:50.72) |")
m.append("| New narration | %s - %s, %d sentences, %d captions (%d with a coloured key word) |" % (tc(N[0]["start"]), tc(last_word), len(N), ncap, nem))
m.append("| Episode running time | **%s** (%.2f s, %d frames at 24 fps; new picture %d frames). Last word ends %s, then black and the end card |" % (tc(end), end, S[-1]["f1"], S[-1]["f1"] - S[0]["f0"], tc(last_word)))
m.append("| Characters to record | **%d** spoken Thai characters (numbers spelled out, no spaces or punctuation); **%d** counting spaces and punctuation, which is how a text-to-speech service bills. The hook was 573 / 609 |" % (chars, billed))
m.append("| Speaking rate measured from the hook | 553 caption characters in 50.07 s = 11.04 per second with pauses; 12.58 per second inside a sentence; the last caption of a sentence runs 0.38 s longer |")
m.append("| Voice time / silence | %.1f s of sentences in %.1f s of new picture; the rest is picture and effect beats |" % (voiced, end - narr.HOOK_END))
m.append("| Estimate error | The hook's sentences ran from 6.8 to 18.1 characters per second, so single lines can be 30 %% off. Timings here are intended starts; the cut follows the real recording, as the hook did |")
m.append("")
m.append("## Length: 5:35 against the 6:00-6:40 target\n")
m.append("The screenplay gives the rest of SCENE 02 and SCENES 03-06 5:47 (0:53 to 6:40). This script takes 4:41 for them. What went and why:\n")
m.append("- **SCENE 03, the first drive.** The screenplay has the truck drive along the gaps before the lorry. Here it is two shots (S83-S84). A truck driving through a jam is the most expensive thing to animate honestly and tells nothing new.")
m.append("- **SCENE 04, the walk.** The talk on the way down is three whispered lines at the stair foot. No walking-and-talking filler.")
m.append("- **SCENE 05.** The call is three lines from her and none from Kong: he is cut off before he can promise. Praew's argument is one line. The screenplay's 65 s becomes 29 s.")
m.append("- **SCENE 06.** The refusal at the gate is one line; the flight to the building site is two shots.")
m.append("- **Not cut:** the 60 seconds of SCENE 02 run in real time (the junior's eyes open 57.6 s after the bite on the episode clock), so that scene keeps its full length.")
m.append("- Rendering is the other reason: every 10 s of picture costs about 3.5 CPU hours at these settings.")
m.append("- %d sentences are marked *trim*: they can go without breaking a set-up (%.1f s together)." % (len(trim), trim_s))
m.append("")
m.append("## Retention structure\n")
m.append("| Loop | Opened | Kept alive | Paid off |\n|---|---|---|---|")
m.append("| 60 seconds | hook s16 | s17 / s23 / s30 countdown, four watch inserts | s32-s33 (eyes open at 57.6 s); s101 at the end |")
m.append("| Sound and light call them | s19 car alarm | s35 (out of sight = lost) | s54-s55 siren; s58 rule said aloud; s66-s67 flare; s79 phone light; s92 the cutter not used; s102 the shouting |")
m.append("| The battery | hook s04 | | s47 third bar blinks; s91 at the chain |")
m.append("| Kong's promises | hook s06-s10 | s26-s27 promise two | s51 the junior at the glass; s82-s84 promise three never spoken |")
m.append("| The daughter's call | hook s05-s10 | s78 no call yet | s79-s83 the call; the pier is the series goal |")
m.append("| The rider | s36 | | s48-s49 |")
m.append("| Tos's wound | s69-s70 | s75-s76, s90 | s97-s100; left open by s105 |")
m.append("| What was left behind | s63-s65 | s73-s75 | later episodes |")
m.append("")
m.append("## Script\n")
m.append("Caption split is marked with `/`. **Bold** = the coloured word (amber = fact, red = threat). Start and length are on the episode clock.\n")
cur = None
for s in N:
    if s["scene"] != cur:
        cur = s["scene"]; ss = [x for x in N if x["scene"] == cur]
        m.append("\n### %s (%s - %s)\n" % (SCN[cur], tc(ss[0]["start"]), tc(ss[-1]["end"])))
        m.append("| id | start | s | who | captions | colour | chars | effect cue | shots | note |\n|---|---|---|---|---|---|---|---|---|---|")
    caps = " / ".join((c["text"].replace(c["emph"], "**" + c["emph"] + "**") if "emph" in c else c["text"]) for c in s["captions"])
    col = next((c["colour"] for c in s["captions"] if "emph" in c), "")
    m.append("| %s | %s | %.2f | %s | %s | %s | %d | %s | %s | %s%s |" % (s["id"], tc(s["start"]), s["dur"], WHO[s["speaker"]], caps, col, s["chars"], s["fx"], " ".join(s["shots"]), s["beat"], " *(trim)*" if s["optional_trim"] else ""))
m.append("\n## Text for the recording (one line per sentence, numbers spelled out)\n")
m.append("```")
for s in N: m.append("%s\t%s" % (s["id"], s["tts"]))
m.append("```")
m.append("\n## Lines for `finish.EMPH` (caption, word, colour)\n")
m.append("```")
for a, b, c in emph_table: m.append('("%s", "%s", %s_ASS),' % (a, b, c.upper()))
m.append("```")
m.append("\n`finish.emph` matches on the whole caption text. No new caption repeats another with a different colour; `เฮ้ย!` (s31) is already red in the hook table.")
m.append("\n## Mix notes\n")
m.append("- Narration stays clearly above effects, as in the hook mix. One exception by design: the siren after s54 plays at full level for 1.2 s in a gap with no words, then ducks under s55.")
m.append("- The heartbeat pulse (s17-s28, back at s101) is a low effect under the voice, not music.")
m.append("- Whispered lines (s73-s77) are performed quietly by the narrator, not lowered in the mix.")
m.append("- No status icons anywhere. The watch, the phone screens, the gauge LEDs and the map are props shown full frame.")
open(os.path.join(OUT, "narration_ep1.md"), "w", encoding="utf-8").write("\n".join(m) + "\n")
# ---- shots
cf = Counter(); cn = Counter(); setf = Counter(); scf = Counter()
for x in S: cf[x["cls"]] += x["frames"]; cn[x["cls"]] += 1; setf[x["set"]] += x["frames"]; scf[x["scene"]] += x["frames"]
A_close = sum(x["frames"] for x in S if x["cls"] == "A" and any(k in x["size"] for k in ("CU", "INSERT", "OTS")))
COST = {"A": 65, "B": 40, "C2": 35, "C1": 0}
cpu = {k: cf[k] * COST[k] for k in cf}; cpu_h = sum(cpu.values()) / 3600.0
SETS = OrderedDict([
 ("X1", "v11 expressway, the hook's rescue zone as built (wreck, rescue truck, work lamp, jam, skyline). Existing."),
 ("X1s", "X1 plus the overturned sedan 40 D behind the truck, placed where no hook camera (S03-S05, S24) sees it. Dressing of the existing set."),
 ("X2", "The same expressway model 150 D further on: jack-knifed lorry across the lanes, service-stair gate at the left barrier, a taxi against the truck's left side. Dressing of the existing set + two new props."),
 ("X2c", "X2 at the truck: exterior shots that need the cab door, windscreen and the people inside (cab shell from CAB)."),
 ("CAB", "NEW: rescue truck crew cab interior (two front seats, rear bench, console with the siren switch, windows) and the equipment wall with roll shutter and dressed shelves."),
 ("UND", "NEW: service stair on a pier and the street under the expressway (piers, puddles, rain curtains at the deck edges)."),
 ("BUS", "NEW, one shot: a bus window panel with wet glass and moving lights. Fallback: replace S130 with a phone screen (C1)."),
 ("RIV", "NEW: riverside block, hospital side: steel gate, forecourt, lit facade, river."),
 ("SITE", "NEW: riverside block, building-site side: hoarding with a bent panel, bare concrete hall with columns. Same file as RIV."),
 ("2D", "Drawn full frame in SVG, composited in finish.py. No Blender.")])
js = OrderedDict(episode=dict(fps=24, size="720x1280", hook_frames=[0, 1280], new_frames=[S[0]["f0"], S[-1]["f1"]], running_time=tc(end)),
     classes=dict(A="character close / medium, final tier at 100 % scale", B="wide / environment / prop insert with no head over 0.10 of the frame width, final tier at 75 %",
                  C1="drawn 2D full frame, no Cycles render", C2="re-uses a hook shot's staging code (S08 jaws, S09 gauge macro, S24 crane), final tier 75 %, 4 spp"),
     totals=dict(shots=len(S), frames_by_class=dict(cf), shots_by_class=dict(cn), frames_by_set=dict(setf), frames_by_scene=dict(scf), mean_shot_s=round((end - narr.HOOK_END) / len(S), 2),
                 cpu_s_per_frame=COST, cpu_hours=round(cpu_h, 1), wall_hours_4_cores=round(cpu_h / 4, 1)),
     sets=SETS, shots=S)
json.dump(js, open(os.path.join(OUT, "shots_ep1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
m = []
m.append("# DEAD ZONE 09 EP.1: shot list after the hook (S25-S%d)\n" % (24 + len(S)))
m.append("Continues `v10/film` (S01-S24, frames 0-1279). Times are the episode clock; frames are film frames `g` (0-based, end exclusive), so `run.py --frames f0:f1` renders a shot. Every cut sits on a caption start of `narration_ep1.json` unless the cut-on column says it is a picture beat. Machine copy: `shots_ep1.json`. Generator: `_gen/shots.py`.\n")
m.append("## Totals\n")
m.append("| | shots | frames | seconds | CPU s / frame | CPU h |\n|---|---|---|---|---|---|")
for k, lab in (("A", "A: character close / medium, 100 %"), ("B", "B: wide / environment / prop insert, 75 %"), ("C2", "C2: re-used hook staging (jaws, gauge, crane), 75 %"), ("C1", "C1: drawn 2D, no render")):
    m.append("| %s | %d | %d | %.1f | %d | %.1f |" % (lab, cn[k], cf[k], cf[k] / 24.0, COST[k], cpu[k] / 3600.0))
m.append("| **all** | **%d** | **%d** | **%.1f** | | **%.1f** (about %.0f h on 4 cores with 4 workers x 1 thread) |" % (len(S), sum(cf.values()), sum(cf.values()) / 24.0, cpu_h, cpu_h / 4))
m.append("")
m.append("- Mean shot %.2f s (the hook: 2.22 s). S105 is one shot of four setups on four words." % ((end - narr.HOOK_END) / len(S)))
m.append("- Of the A frames, %d are close-ups, inserts or over-shoulders and %d are mediums. Rendering the mediums at 75 %% would save about %.0f CPU h; the standing decision is 100 %% for character shots, so the table does not assume it." % (A_close, cf["A"] - A_close, (cf["A"] - A_close) * 25 / 3600.0))
m.append("- The cost figures are the README's: 65 CPU s per frame at 100 %, 40 at 75 %; 35 for the 4 spp macros (S09 measured 31.5). New sets are not measured yet: the cab interior and the dark sets should be cheaper than the expressway, the 40-extra wides (S58, S68, S89) dearer.")
m.append("- B and C are %.0f %% of the frames. A stays high because the story after the title is four people talking and hiding; calling those shots B would break the crisp-line rule." % (100.0 * (cf["B"] + cf["C1"] + cf["C2"]) / sum(cf.values())))
m.append("")
m.append("## Sets\n")
m.append("| code | what | frames |\n|---|---|---|")
for k, v in SETS.items(): m.append("| %s | %s | %d |" % (k, v, setf[k]))
m.append("")
m.append("## Screen direction (holds for the whole episode)\n")
m.append("- **Safety is screen right, the threat comes from screen left.** The direction of travel on the expressway, the lorry, the stair, the hospital and the building site are all to the right. The crash zone, the horde and the last runners are to the left.")
m.append("- Profile and tracking shots of the road and the truck are taken from the median side, so the left barrier and the stair gate are in the background.")
m.append("- Three moves go right to left on purpose: the driver thrown at the alarm car (S27-S30), Kong running back to the sedan (S70), and the flare, which is thrown toward the camera side (S108-S109).")
m.append("- Dialogue pairs keep one line each: Kong right / junior left in SCENE 02; in the cab the camera stays ahead of the windscreen or on the driver's side; Praew left / Kong right under the expressway; at the gate outside = left, inside = right.")
m.append("- S164-S165: Kong faces the lens with Tos on his right and the gap on his left, so the last eye movement reads as a choice between two screen sides.")
m.append("")
m.append("## Rules every shot keeps\n")
m.append("- Puppets stay upright and camera-facing. Nobody lies on the ground: the junior sits against the wheel, the knock-down of the screenplay is a stagger against the truck, Tos in the tipped car is a card rolled 80 degrees seen through the windscreen frame.")
m.append("- Drawings on twos, camera and lip sync on ones; walks and runs use `gait8` with planted feet; every still pose has breath, blink, rain, beacon or prop motion, and no shot is a held frame with a camera move.")
m.append("- Levels: RAIN 0.2, SPLASH 0.25, HAZE 0.3, TILT 0, DOF 0.25, BLOOM 0.55. Under the expressway and in the building site RAIN is 0 on the actors' plane (rain only at the deck edges and outside the hoarding).")
m.append("- No status icons. Captions as in the hook.")
m.append("- Resumable: one folder per shot, a frame that exists is skipped; render order by scene, A shots of a scene last so that B and C can be cut and judged first.")
m.append("")
cur = None
for x in S:
    if x["scene"] != cur:
        cur = x["scene"]; xs = [y for y in S if y["scene"] == cur]
        m.append("\n## %s: %s - %s, %d shots, %d frames\n" % (SCN[cur], tc(xs[0]["t0"]), tc(xs[-1]["t1"]), len(xs), sum(y["frames"] for y in xs)))
        m.append("| shot | time | frames | class | set | size | cast and action | camera | lens | reads in 0.5 s | sound | narration | cut on |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    nar = "; ".join("%s: %s" % (n["id"], " / ".join(n["captions"])) for n in x["narration"]) or "(none)"
    m.append("| %s | %s - %s | %d-%d (%d) | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (x["id"], tc(x["t0"]), tc(x["t1"]), x["f0"], x["f1"], x["frames"], x["cls"], x["set"], x["size"], x["action"], x["camera"], x["lens"], x["reads"], x["sound"] or "-", nar, x["cut_on"]))
open(os.path.join(OUT, "shots_ep1.md"), "w", encoding="utf-8").write("\n".join(m) + "\n")
print(tc(end), end, chars, billed, dict(cf), dict(cn), round(cpu_h, 1), trim_s, A_close, dict(setf), dict(scf))
print([ (x["id"], x["cut_on"][:14]) for x in S if x["id"] in ("S58","S68","S70","S83","S84","S89","S90","S105","S109","S110","S111","S112","S130","S168","S169","S27","S30","S47","S53","S81","S120","S127","S144","S157","S165","S166")])
