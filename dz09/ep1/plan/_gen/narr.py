# -*- coding: utf-8 -*-
"""EP.1 narration after the hook title. Pure data + timing model. No bpy, no network."""
import re, json
CPS = 12.58      # measured: mid-sentence captions of the hook (captions_timing.json), Thai chars without spaces/punctuation per second
TAIL = 0.38      # measured: extra length of a sentence-final caption (mean 1.237 s vs 10.75 chars / 12.58)
OVERALL = 11.04  # measured: 553 chars / 50.07 s, pauses included
HOOK_END = 53.32; BITE = 43.795; FPS = 24
A, R = "amber", "red"
NUM = {"50 วินาที":"ห้าสิบวินาที","30 วินาที":"สามสิบวินาที","10 วินาที":"สิบวินาที","2 ครั้ง":"สองครั้ง","ที่ 3":"ที่สาม","4 อย่าง":"สี่อย่าง","60 วินาที":"หกสิบวินาที"}
def spoken(c):
    for k, v in NUM.items(): c = c.replace(k, v)
    return c
def n(t): return len(re.sub(r"[\s\.\!\?…,]", "", t))
# (id, scene, who, captions, emph(caption index, word, colour) or None, gap before (s) or ("at", t), fx cues, trim flag, beat)
S = [
 # ---------------- SCENE 02 (rest): the 60 seconds, in real time ----------------
 ("s17","02","narr",["เหลืออีก","50 วินาที"],(1,"50 วินาที",A),("at",53.62),"hard cut from title to picture; rain + beacons back at full level; low heartbeat pulse starts (one beat per second, under the voice) and runs to s30",0,"countdown opens (pay-off of the hook's last line)"),
 ("s18","02","narr",["ก้องเอาเครื่องตัด","กระแทกมันกระเด็น","ไปชนรถคันข้างๆ"],None,0.10,"metal thud on 'กระแทก'; body hits a car door on 'ชนรถ'",0,"Kong rams the driver off with the tool body"),
 ("s19","02","narr",["สัญญาณกันขโมย","ดังลั่น","มันหันไปหาเสียง","ทันที"],(2,"เสียง",A),0.10,"car alarm (two-tone, panned to the alarm car's side) from the first caption, hazards blink; infected snarl turning away",0,"SETUP: they go for sound and flashing light"),
 ("s20","02","narr",["ก้องพยุงน้อง","ไปหลบหลังรถกู้ภัย"],None,0.15,"two pairs of boots, one dragging; alarm now further off (distance + low-pass)",0,"cover"),
 ("s21","02","kong",["มองหน้าพี่ไว้!","ได้ยินไหม!"],None,0.25,"dry, close; rain on truck metal",0,"dialogue"),
 ("s22","02","narr",["น้องพยักหน้า","แต่เลือด","ไหลไม่หยุด"],(2,"ไหลไม่หยุด",R),0.15,"wet cloth press; junior's breath",0,"wound"),
 ("s23","02","narr",["30 วินาที"],(0,"30 วินาที",A),("at",73.80),"watch tick, close and dry (three ticks before the line)",0,"countdown"),
 ("s24","02","narr",["ลมหายใจน้อง","สั้นลง","ถี่ขึ้น"],(2,"ถี่ขึ้น",R),0.30,"fast shallow breathing, shivering",0,"symptoms"),
 ("s25","02","crew",["พี่...","ผมหนาว..."],(1,"หนาว",R),0.45,"voice low; heartbeat a little faster",0,"dialogue"),
 ("s26","02","kong",["อดทนไว้","เดี๋ยวพี่พาไป","โรงพยาบาล"],(2,"โรงพยาบาล",A),0.30,"",0,"promise no. 2 (SETUP for s49, s75, s86)"),
 ("s27","02","narr",["คืนนี้ ก้องสัญญา","ไปแล้ว 2 ครั้ง"],(1,"2 ครั้ง",A),0.50,"",0,"open loop: the promise count"),
 ("s28","02","narr",["มือที่สั่น","ค่อยๆ","หยุดนิ่ง"],(2,"หยุดนิ่ง",R),0.60,"breathing stops; heartbeat stops with it; only rain",0,"he goes still"),
 ("x1","02","narr",["ก้องแตะชีพจรที่คอ","ไม่มีอะไรเต้นเลย"],(1,"ไม่มีอะไรเต้น",R),0.30,"rain only; glove on wet skin",0,"he checks for a response"),
 ("s29","02","narr",["10 วินาที"],(0,"10 วินาที",A),("at",93.80),"watch tick alone",0,"countdown"),
 ("s30","02","kong",["เฮ้ย!","ได้ยินพี่ไหม!"],None,0.35,"",0,"dialogue"),
 ("s31","02","narr",["แล้วน้อง","ก็ลืมตา"],(1,"ลืมตา",R),("at",100.90),"three watch ticks in silence before the line; sub-bass swell into the next line",0,"PAY-OFF of the 60-second rule: eyes open 57.6 s after the bite"),
 ("s32","02","narr",["แต่ตาคู่นั้น","ไม่ใช่ตาคนแล้ว"],(1,"ไม่ใช่ตาคน",R),0.05,"red flash 1 frame on the cut; infected inhale",0,"pay-off of 'จะไม่ใช่คนอีกต่อไป'"),
 ("s33","02","narr",["มันพุ่งใส่ก้อง","ก้องเอาเครื่องตัดขวาง","ผลักมันสุดแรง"],None,0.10,"snarl; teeth on metal; shove grunt; body against the truck panel",0,"the attack"),
 ("s34","02","narr",["ก้องถอยหลบมุมรถ","มันมองไม่เห็นเขา"],(1,"มองไม่เห็น",A),0.15,"the snarl drops to short searching breaths; Kong's held breath",0,"world rule 7 planted"),
 ("s35","02","narr",["บนหลังคารถ","ไรเดอร์เสื้อเขียว","วิ่งหนีสุดชีวิต","มันกระโจนตามไป"],(3,"กระโจนตาม",R),0.20,"boots on car roofs (hollow bangs), windscreen cracking, a far scream",0,"SETUP: the rider (James) and who chases him"),
 ("s36","02","narr",["ก้องมองไปรอบตัว","ทั้งทางด่วน","มีแต่คนวิ่งหนี","กับพวกที่ไล่กัด"],(3,"ไล่กัด",R),0.25,"crowd screams from several directions, glass breaking left then right, horns",0,"scale"),
 ("s37","02","narr",["นี่ไม่ใช่อุบัติเหตุ","อีกต่อไปแล้ว"],(0,"ไม่ใช่อุบัติเหตุ",R),0.20,"",0,"realisation"),
 ("s38","02","narr",["และไม่ได้เกิด","แค่ที่นี่"],(1,"แค่ที่นี่",R),0.35,"city-wide sirens layered far away, wind; screams reduced to a distant bed",1,"city wide shot"),
 # ---------------- SCENE 03: the last rescue truck ----------------
 ("s39","03","narr",["ไม่ไกลจากรถกู้ภัย","รถเก๋งคันหนึ่ง","พลิกตะแคง"],(2,"พลิกตะแคง",A),0.45,"hazard relay ticking, dripping, a woman's strained effort",0,"new place"),
 ("s40","03","narr",["หมอแพรว","หมอห้องฉุกเฉิน","กำลังดึงชายใส่สูท","ออกจากซากรถ"],(0,"หมอแพรว",A),0.10,"",0,"Praew introduced"),
 ("s41","03","narr",["เขาชื่อคุณทศ","ประตูที่ยุบ","อัดเขาติดเบาะ"],(0,"คุณทศ",A),0.10,"metal creak; Tos's grunts",0,"Tos introduced"),
 ("s42","03","narr",["ไกลออกไป","ฝูงของมัน","กำลังวิ่งมา"],(1,"ฝูงของมัน",R),0.20,"many running feet on wet road, far, growing",0,"deadline"),
 ("s43","03","narr",["ก้องชะงัก","หนีตอนนี้","ยังทัน"],None,0.20,"everything dips for half a second",0,"the choice"),
 ("s44","03","narr",["แต่เขา","วิ่งกลับเข้าไปช่วย"],(1,"กลับเข้าไปช่วย",A),0.20,"boots splashing",0,"Kong's value shown by action"),
 ("s45","03","narr",["ก้องสอดเครื่องถ่าง","เหล็กค่อยๆ","อ้าออก"],None,0.10,"cordless pump whine, metal groaning open",0,"the tool is used"),
 ("s46","03","narr",["คุณทศหลุดออกมา","แต่แบตขีดที่ 3","เริ่มกะพริบ"],(2,"เริ่มกะพริบ",R),0.10,"gauge warning beep x2 (quiet, close)",0,"PAY-OFF of 'แบตเต็ม 3 ขีด' + new open loop"),
 ("s47","03","james",["พี่!","รอผมด้วย!"],None,0.20,"shout from above/behind, roof bangs",0,"dialogue"),
 ("s48","03","narr",["เจมส์","ไรเดอร์ส่งอาหาร","กระโดดลงจากหลังคารถ","และที่ไล่ตามมา","คือน้องของก้อง"],(4,"น้องของก้อง",R),0.10,"landing splash; snarl close behind",0,"PAY-OFF of s35"),
 ("s49","03","narr",["ทุกคนขึ้นรถกู้ภัย","ประตูปิดทัน","แค่เสี้ยววินาที"],None,0.15,"door slam, then a body hitting it",0,"into the truck"),
 ("s50","03","narr",["หน้าที่แนบกระจก","คือคนที่เขาสัญญา","ว่าจะพาไปโรงพยาบาล"],(0,"แนบกระจก",R),0.25,"muffled snarl through glass, nails on glass; cabin is quiet",0,"PAY-OFF of promise no. 2"),
 ("s51","03","narr",["ก้องออกรถ","แทรกไปตามช่องว่าง"],None,0.25,"diesel start, tyres on wet road, mirrors scraping",0,"drive"),
 ("s52","03","narr",["แต่ข้างหน้า","รถบรรทุกขวาง","เต็มถนน"],(1,"ขวาง",R),0.10,"brakes; wipers",0,"obstacle"),
 ("s53","03","narr",["มือเขาไปเอง","ตามความเคยชิน","เปิดไซเรนขอทาง"],(2,"ไซเรน",R),0.15,"switch click, then the siren at full level for 1.2 s (the only moment an effect is allowed to rival the voice: it sits in the gap after the line)",0,"the mistake"),
 ("s54","03","narr",["ทุกตัวบนทางด่วน","หยุดวิ่ง","แล้วหันมา","พร้อมกัน"],(2,"หันมา",R),("gap",1.20),"siren ducks under the voice; all other screams stop",0,"PAY-OFF of the car alarm (s19)"),
 ("s55","03","praew",["ปิดเสียง!","เร็ว!"],None,0.15,"",0,"dialogue"),
 ("s56","03","narr",["ก้องปิดไซเรน","แต่สายไปแล้ว","พวกมันรู้แล้ว","ว่าเขาอยู่ตรงไหน"],(1,"สายไปแล้ว",R),0.10,"siren winds down; silence 0.4 s; then many feet running toward us",0,"consequence"),
 ("s57","03","narr",["เสียง กับแสง","คือสิ่งที่เรียกมัน"],(0,"เสียง กับแสง",A),0.25,"first bodies hit the truck",0,"the rule, learned (used in s66, s91)"),
 ("s58","03","tos",["ขับไปสิ!","จะจอดให้มันกิน","หรือไง!"],None,0.20,"pounding all around",0,"Tos's value shown"),
 ("s59","03","kong",["รถข้างหน้า","ขยับไม่ได้!"],None,0.10,"",0,"dialogue"),
 ("s60","03","james",["พี่! ผมเคยผ่านแถวนี้","มีทางลง","ข้างรถคันนั้น!"],(1,"ทางลง",A),0.15,"",0,"way out"),
 # ---------------- SCENE 04: what must be left ----------------
 ("s61","04","narr",["ฝูงกระแทกรถ","ไม่หยุด","กระจกเริ่มร้าว"],(2,"ร้าว",R),0.25,"body hits in an irregular rhythm, glass crack ticks",0,"pressure"),
 ("s62","04","narr",["ก้องเปิดตู้อุปกรณ์","ของเต็มตู้","แต่แบกไปได้","แค่ 4 อย่าง"],(3,"4 อย่าง",A),0.15,"locker latch, roll-up shutter",0,"the choice of things"),
 ("s63","04","narr",["เครื่องตัด","ชะแลง","วิทยุ","กระเป๋าพยาบาลใบเล็ก"],None,0.15,"one grab sound per item, on the cut",0,"the four things"),
 ("s64","04","narr",["ที่เหลือ","ต้องทิ้งทั้งหมด"],(1,"ทิ้ง",R),0.20,"shutter left open; a monitor beeping once, abandoned",0,"cost"),
 ("s65","04","narr",["ก้องจุดพลุไฟฉุกเฉิน","ขว้างไปอีกฝั่งถนน"],None,0.25,"flare strike and hiss, window crank, the flare skittering on the road",0,"plan built on the rule"),
 ("s66","04","narr",["เกือบทั้งฝูง","วิ่งตามแสงไป"],(1,"ตามแสง",A),0.15,"the pounding moves away to the left",0,"PAY-OFF of s57"),
 ("s67","04","narr",["คุณทศปีนออก","เป็นคนแรก"],(1,"คนแรก",A),0.20,"glass crunch, cloth",0,"character"),
 ("s68","04","narr",["แขนเสื้อเกี่ยวกระจก","ขาดเป็นทาง","เลือดซึมออกมา"],(2,"เลือด",R),0.10,"cloth rip, sharp breath",0,"SETUP: the wound (glass, shown clearly)"),
 ("s69","04","narr",["เขารีบดึงแขนเสื้อ","ลงปิดแผล","ไม่บอกใครสักคำ"],(2,"ไม่บอกใคร",R),0.15,"",0,"SETUP: the secret"),
 ("s70","04","narr",["ทุกคนวิ่งลง","บันไดเหล็ก","ข้างทางด่วน"],None,0.25,"steel treads ringing under four pairs of feet, rain on steel",0,"escape"),
 ("s71","04","narr",["ข้างล่างมืด","และเงียบ"],(0,"มืด",A),0.35,"the expressway noise is now overhead and muffled; drips",0,"world rule 5"),
 ("s72","04","praew",["ของเหลือ","แค่นี้เองเหรอ"],None,0.35,"whispered",0,"dialogue"),
 ("s73","04","kong",["เอาออกมาได้","เท่านี้"],None,0.15,"whispered",0,"dialogue"),
 ("s74","04","praew",["ถ้ามีคนเจ็บหนัก","เราอาจช่วยไม่ได้"],(1,"ช่วยไม่ได้",R),0.20,"whispered",0,"irony: picture is Tos's arm"),
 ("s75","04","narr",["ไม่มีใครเห็น","ว่าคุณทศกอดอก","แน่นกว่าเดิม"],(1,"กอดอก",R),0.25,"",1,"irony stated"),
 ("s76","04","james",["โรงพยาบาลอยู่ข้างหน้า","ผมเคยไปส่งอาหาร"],(0,"โรงพยาบาล",A),0.30,"",0,"goal"),
 ("s77","04","narr",["ก้องมองโทรศัพท์","ยังไม่มีสาย","จากลูก"],(1,"ยังไม่มีสาย",R),0.30,"",0,"open loop: the daughter"),
 # ---------------- SCENE 05: the daughter ----------------
 ("s78","05","narr",["แล้วโทรศัพท์ก็สั่น","จอสว่างวาบ","กลางความมืด"],(1,"สว่างวาบ",R),0.50,"phone buzz on a hard surface x2; everybody's breath stops",0,"PAY-OFF of the missed calls + light = danger"),
 ("s79","05","namnuea",["พ่อ!","พ่ออยู่ไหน!"],None,0.30,"phone-band filter, crowd and engine behind her",0,"dialogue"),
 ("s80","05","namnuea",["เขาพาหนู","ขึ้นรถอพยพ","บอกว่าจะไปท่าเรือ"],(2,"ท่าเรือ",A),0.20,"",0,"the series goal"),
 ("s81","05","namnuea",["ครั้งนี้","พ่ออย่าผิดสัญญานะ"],(1,"อย่าผิดสัญญา",R),0.35,"signal breaking up on the last word",0,"the promise asked for"),
 ("s82","05","narr",["ก้องยังไม่ทันตอบ","สัญญาณก็ขาด"],(1,"สัญญาณก็ขาด",R),0.30,"dead-line tone, one beat, then nothing",0,"cut off"),
 ("s83","05","narr",["สัญญาครั้งที่ 3","เขายังไม่ทัน","ได้พูดออกไป"],(0,"สัญญาครั้งที่ 3",A),0.40,"",0,"PAY-OFF of the promise count (s27)"),
 ("s84","05","narr",["ก้องหันหลัง","จะไปเดี๋ยวนั้น"],None,0.30,"boots turning on gravel",0,"impulse"),
 ("s85","05","praew",["ถ้าคุณไปคนเดียว","ตอนนี้","คุณอาจไปไม่ถึงลูก"],(2,"ไปไม่ถึงลูก",R),0.20,"",0,"the argument"),
 ("s86","05","narr",["ก้องกำโทรศัพท์แน่น","แล้วเดินตามเจมส์","ไปโรงพยาบาล"],None,0.40,"",0,"decision"),
 # ---------------- SCENE 06: the gate that does not open ----------------
 ("s87","06","narr",["โรงพยาบาลริมแม่น้ำ","ไฟยังสว่าง"],(1,"ไฟยังสว่าง",A),0.50,"river wash, a generator hum, no rain noise on roofs for the first time",0,"hope"),
 ("s88","06","narr",["แต่ประตูเหล็ก","ปิดสนิท"],(1,"ปิดสนิท",R),0.20,"hands on steel bars, a chain rattling",0,"but"),
 ("s89","06","guard",["เปิดไม่ได้!","เราไม่รู้ว่า","ใครโดนกัดมาบ้าง!"],(2,"โดนกัด",R),0.25,"voice from inside, behind steel",0,"refusal; SETUP for the wound reveal"),
 ("s90","06","narr",["ก้องยกเครื่องตัดขึ้น","โซ่เส้นนี้","ตัดขาดได้แน่"],None,0.25,"gauge beep (the blinking bar)",0,"temptation; battery loop touched again"),
 ("s91","06","narr",["แต่เสียงตัดเหล็ก","จะเรียกพวกมัน","มาทั้งฝูง"],(2,"ทั้งฝูง",R),0.10,"",0,"the rule applied (pay-off of s57)"),
 ("s92","06","narr",["และคนข้างใน","จะไม่เหลือประตู"],None,0.10,"",1,"Kong's value"),
 ("s93","06","narr",["เขาลดมือลง"],None,0.15,"",0,"decision"),
 ("s94","06","narr",["ข้างๆ กัน","มีตึกสร้างไม่เสร็จ","มืดสนิท"],(2,"มืดสนิท",A),0.30,"tarpaulin flapping, dripping concrete",0,"refuge by rule 5"),
 ("s95","06","narr",["ทุกคน","วิ่งเข้าไปหลบ"],None,0.10,"",1,"move"),
 ("s96","06","narr",["แล้วก้องก็เห็น","เลือดหยดลงพื้น","ทีละหยด","จากแขนเสื้อคุณทศ"],(1,"เลือด",R),0.50,"single drops on concrete, very close, in a quiet room",0,"PAY-OFF of the hidden wound"),
 ("s97","06","praew",["แผลอะไร?"],None,0.35,"",0,"dialogue"),
 ("s98","06","tos",["ไม่มีอะไร!"],None,0.15,"loud; it echoes in the bare concrete",0,"dialogue"),
 ("s99","06","praew",["ขอดูเดี๋ยวนี้!"],None,0.10,"louder; echo",0,"dialogue"),
 ("s100","06","narr",["ก้องรู้ดี","ว่า 60 วินาที","มันสั้นแค่ไหน"],(1,"60 วินาที",A),0.30,"heartbeat pulse of scene 02 returns",0,"PAY-OFF of the 60-second rule"),
 ("s101","06","narr",["แต่เสียงเถียงกัน","ดังเกินไป"],(1,"ดังเกินไป",R),0.25,"the echo of the shouting dies; one far snarl answers",0,"cause"),
 ("s102","06","narr",["ในความมืด","มีเสียงฝีเท้า","วิ่งเข้ามา"],(1,"เสียงฝีเท้า",R),0.15,"running feet on gravel from behind, closing",0,"effect"),
 ("s103","06","narr",["ก้องยกชะแลงขึ้น"],(0,"ชะแลง",A),0.35,"steel bar scrape, heartbeat louder",0,"the last action"),
 ("s104","06","narr",["แต่เขาจะฟาด","ใคร"],(1,"ใคร",R),0.25,"all sound cuts to nothing on 'ใคร'; black; 1.0 s of silence; then one watch tick",0,"CLIFFHANGER"),
]
LABEL = {}
def _ids():
    for i, row in enumerate(S): LABEL[row[0]] = "s%d" % (17 + i)
_ids()
def relabel(txt): return re.sub(r"\b(s\d+|x\d+)\b", lambda m: LABEL.get(m.group(1), m.group(1)), txt)
def build():
    out = []; t = HOOK_END
    for (sid, sc, who, caps, em, gap, fx, trim, beat) in S:
        if isinstance(gap, tuple) and gap[0] == "at":
            assert gap[1] >= t - 1e-6, (sid, gap[1], t)
            pause = gap[1] - t; t0 = gap[1]
        else:
            g = gap[1] if isinstance(gap, tuple) else gap
            pause = g; t0 = t + g
        cl = []; tc = t0
        for i, c in enumerate(caps):
            d = max(0.42, n(spoken(c)) / CPS) + (TAIL if i == len(caps) - 1 else 0.0)
            e = dict(text=c, t0=round(tc, 3), t1=round(tc + d, 3))
            if em and em[0] == i:
                assert em[1] in c, (sid, em)
                e["emph"] = em[1]; e["colour"] = em[2]
            cl.append(e); tc += d
        tts = " ".join(spoken(c) for c in caps)
        out.append(dict(id=LABEL[sid], label=sid, scene=sc, speaker=who, tts=tts, text=" ".join(caps), start=round(t0, 3), dur=round(tc - t0, 3), end=round(tc, 3),
                        voiced=round(tc - t0 - TAIL, 3), pause_before=round(pause, 3), chars=n(tts), chars_billed=len(tts), captions=cl, fx=relabel(fx), optional_trim=bool(trim), beat=relabel(beat)))
        t = tc
    return out
if __name__ == "__main__":
    o = build()
    for s in o:
        print(s["id"], s["scene"], "%7.2f %5.2f" % (s["start"], s["dur"]), "p%.2f" % s["pause_before"], s["text"])
    print("end", o[-1]["end"], "chars", sum(s["chars"] for s in o), "billed", sum(s["chars_billed"] for s in o), "caps", sum(len(s["captions"]) for s in o))
    sc = {}
    for s in o: sc.setdefault(s["scene"], [s["start"], 0])[1] = s["end"]
    print(sc)
