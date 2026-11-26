# -*- coding: utf-8 -*-
"""EP.1 edit pass (script editor / line producer) on top of the screenwriter's draft in ../_gen.
Reads ../_gen/narr.py and ../_gen/shots.py as data (not modified), applies the edit tables below, re-times with the same
timing model, and returns (sentences, shots). Keys in the tables are the DRAFT ids (s17..s105, S25..S167); output ids are
renumbered and every row keeps its draft_id. No bpy, no network."""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "_gen"))
import narr as D          # draft narration data + timing constants
import shots as DS        # draft shot data
A, R = "amber", "red"
FPS = 24
NUM = dict(D.NUM); NUM.update({"ที่ 2": "ที่สอง", "3 ขีด": "สามขีด"})
def spoken(c):
    for k, v in NUM.items(): c = c.replace(k, v)
    return c
n = D.n
DEL = None
# ---------------------------------------------------------------- narration edits (key = draft id)
# value: DEL, or dict with any of caps, emph (list of (caption index, word, colour)), gap (seconds or ("at", t)), fx, beat, why
NE = {
 "s19": dict(caps=["สัญญาณกันขโมย", "ดังลั่น", "มันทิ้งเหยื่อ", "หันไปหาเสียง"], emph=[(3, "เสียง", A)],
             why="'ทันที' was filler; 'มันทิ้งเหยื่อ' states the strange thing the viewer must notice (it leaves a victim for a noise), which is the question the siren answers"),
 "s27": dict(caps=["สัญญาครั้งที่ 2", "ของคืนนี้"], emph=[(0, "สัญญาครั้งที่ 2", A)],
             why="shorter; the count is kept as a motif but no longer does arithmetic in the middle of the countdown"),
 "s29": dict(caps=["ก้องจับชีพจร", "ไม่เต้นแล้ว"], emph=[(1, "ไม่เต้นแล้ว", R)],
             why="'ไม่มีอะไรเต้นเลย' is not how a rescuer says it; the neck is where the wound is, so the place is left to the picture"),
 "s37": dict(caps=["ทั้งทางด่วน", "มีแต่คนวิ่งหนี", "กับพวกที่ไล่กัด"], emph=[(2, "ไล่กัด", R)], gap=1.25,
             why="'ก้องมองไปรอบตัว' described the picture; the look is now a silent shot before the line"),
 "s39": DEL,  # city-wide line + second crane: the hook already ends on this crane 75 s earlier; the hospital and the evacuation bus say 'everywhere' later
 "s40": dict(caps=["ไม่ไกลกัน", "รถเก๋งคันหนึ่ง", "พลิกตะแคง"], emph=[(2, "พลิกตะแคง", A)], why="shorter"),
 "s41": dict(caps=["หมอแพรว", "หมอห้องฉุกเฉิน", "กำลังดึงคุณทศ", "ออกจากซากรถ"], emph=[(0, "หมอแพรว", A), (2, "คุณทศ", A)],
             why="names Tos here, so the filler sentence 'เขาชื่อคุณทศ' can go; the suit is in the picture"),
 "s42": dict(caps=["แต่ประตูที่ยุบ", "อัดเขาติดเบาะ"], emph=[(1, "ติดเบาะ", R)], why="but-therefore instead of an introduction"),
 "s46": dict(caps=["ก้องเอาเครื่องตัดง้างประตู", "คุณทศหลุดออกมา"], emph=[],
             fx="cordless pump whine, metal groaning open; Tos's breath as he comes free",
             beat="the tool is used; Tos is out (two draft sentences in one)", why="the mechanics of the rescue are not the drama; the choice before it is"),
 "s47": DEL,  # merged into s46; the blinking third bar contradicts the bible ('3 ขีดใน EP.1') and is paid off instead at the chain (s91)
 "s49": dict(caps=["เจมส์", "ไรเดอร์ส่งอาหาร", "กระโดดลงจากหลังคารถ", "แต่ที่ตามหลังมา", "คือน้องของก้อง"], emph=[(0, "เจมส์", A), (4, "น้องของก้อง", R)],
             why="'แต่' turns the line; James's name gets a colour as the other two principals' names do"),
 "s57": dict(caps=["ก้องปิดไซเรน", "แต่สายไปแล้ว", "ทั้งฝูงรู้แล้ว", "ว่าเขาอยู่ตรงไหน"], emph=[(1, "สายไปแล้ว", R)], why="'ทั้งฝูง' is the screenplay's word and is stronger than 'พวกมัน'"),
 "s68": dict(caps=["คุณทศเบียดออกไป", "เป็นคนแรก"], emph=[(1, "คนแรก", A)], why="the door opens a hand-span against a taxi: he squeezes, he does not climb"),
 "s76": DEL,  # 'ไม่มีใครเห็น ว่าคุณทศกอดอก แน่นกว่าเดิม' said what the insert S120 shows
 "s83": dict(caps=["ก้องยังไม่ทันรับปาก", "สัญญาณก็ขาด"], emph=[(1, "สัญญาณก็ขาด", R)],
             beat="cut off before he can promise: PAY-OFF of the promise motif (s27)", why="carries the meaning of the cut sentence s84 in two words ('รับปาก')"),
 "s84": DEL,  # 'สัญญาครั้งที่ 3 เขายังไม่ทัน ได้พูดออกไป': bookkeeping; s83 now says it
 "s85": dict(caps=["ก้องหันหลัง", "จะไปหาลูกเดี๋ยวนั้น"], emph=[], why="says where he is going"),
 "s87": dict(caps=["ก้องกำโทรศัพท์แน่น", "แล้วเดินตามเจมส์ไป"], emph=[], why="the next sentence starts with 'โรงพยาบาล'; saying it twice in a row was a stumble"),
 "s90": dict(caps=["เปิดไม่ได้!", "ใครโดนกัดมาบ้าง", "ก็ไม่รู้!"], emph=[(1, "โดนกัด", R)], why="spoken word order; the line is invented (the screenplay gives the guard none) and stays short"),
 "s91": dict(caps=["ก้องยกเครื่องตัดขึ้น", "แบตยังเต็ม 3 ขีด", "ตัดโซ่ขาดแน่"], emph=[(1, "3 ขีด", A)],
             fx="the cutter's motor clicks ready (no warning beep: the gauge is steady)",
             beat="PAY-OFF of the hook's 'แบตเต็ม 3 ขีด': he has the power and still cannot use it", why="keeps the bible's three bars and pays the hook's set-up here"),
 "s93": dict(caps=["และคนข้างใน", "จะไม่เหลือประตูกั้น"], emph=[(1, "ไม่เหลือประตู", R)], trim=0,
             why="no longer optional: without it Kong spares the chain only to save himself, and his value (other lives count) is not on screen"),
 "s95": dict(gap=0.30),
 "s96": DEL,  # 'ทุกคน วิ่งเข้าไปหลบ': the picture
 "s97": dict(caps=["แล้วก้องก็เห็น", "เลือดหยดลงพื้น", "จากแขนเสื้อคุณทศ"], emph=[(1, "เลือด", R)], gap=0.95, why="'ทีละหยด' is in the picture and the sound"),
 "s101": dict(caps=["ก้องจำได้ดี", "น้องของเขา", "ใช้เวลาแค่ 60 วินาที"], emph=[(2, "60 วินาที", A)],
              beat="PAY-OFF of the 60-second rule, stated as what Kong has seen, not as a clock running on Tos",
              why="the draft ('ก้องรู้ดี ว่า 60 วินาที มันสั้นแค่ไหน') implied a 60-second clock on Tos, who has been with them for minutes; a bite would have turned him long ago. This wording is only what Kong knows and keeps the number"),
}
# new sentences: (after draft id, key, scene, who, caps, emph, gap, fx, beat, why)
NI = [
 ("s29", "n1", "02", "narr", ["ก้องคิดว่า", "เขาเสียน้องไปแล้ว"], [(1, "เสียน้องไปแล้ว", R)], 0.30, "rain only; Kong's breath going out of him",
  "REVERSAL SET-UP: Kong believes the worst is over; the audience has been told what comes next",
  "new: the shortened s29 left 3 s of dead air before '10 วินาที'; this line uses it to put Kong one step behind the audience, which is the hook's own device ('ก้องยังไม่รู้เลยว่า')"),
]
# new shots: (after draft id, key, scene, ref, cls, set, size, action, camera, lens, reads, sound, why)
SI = [
 ("S42", "N1", "02", "n1.0", "A", "X1", "CU", "Kong's face alone: the hand comes away from the jaw (glove edge leaving frame left), `alarmed` falls to `guilty`, his eyes shut for four frames; rain runs off the fringe.",
  "locked", "66 mm", "a man who thinks his friend has died", "rain only", "carries the new sentence; replaces what would have been a 4.5 s hold on S42"),
]
# ---------------------------------------------------------------- shot edits (key = draft id)
# value: DEL, or dict with any of ref, cls, set, size, action, camera, lens, reads, sound, why
WATCH = "Analogue face, nothing to read but one red second hand; a drop of the junior's blood sits on the 12 mark, where the hand stood at the bite. "
SE = {
 "S26": dict(action="Kong's wrist: black glove cuff, orange sleeve edge, a square rescue watch strapped over the cuff. " + WATCH + "The hand is at the 2 (10 s gone, 50 to go round to the blood) and sweeps on; rain drops land and run on the glass; the wrist jolts with the shove.",
             reads="a second hand leaving a blood spot", why="a count the eye can read in one second without digits: the hand has to come back round to the blood"),
 "S36": dict(action="Watch, frontal. " + WATCH + "The hand passes the 6, straight down: half way. A rain drop cuts through a new smear on the glass.", reads="the hand at the bottom, half way round"),
 "S35": dict(cls="B"), "S41": dict(cls="B"), "S138": dict(cls="B"), "S149": dict(cls="B"), "S160": dict(cls="B"),
 "S43": dict(ref="s30.0-0.90", action="Watch, extreme close on the hand tip climbing past the 10: 50, 51, 52; the blood spot at 12 is in the top of the frame, two marks ahead. The drop on the glass trembles at each tick.", reads="the hand climbing toward the blood spot"),
 "S46": dict(action="Watch, tighter still: the hand tip ticks 55, 56, 57 and touches the edge of the blood spot.", reads="the hand reaching the blood"),
 "S47": dict(cls="A", set="X1", camera="locked, 780 ppd; 3 % push; 1-frame pop on the open", lens="100 mm",
             action="ECU of the junior's eyes on the rendered puppet (not a separate 2D drawing), closed, wet lashes, rain and one beacon sweep on grey skin. On 'ลืมตา' (57.6 s after the bite) the lids snap open on one frame: white eyes, tiny red pupils that contract.",
             why="the pay-off of the whole hook must sit in the same light and rain as the shots round it; 39 frames at 100 % cost 0.7 CPU h"),
 "S42": dict(action="Kong's two gloved fingers under the junior's jaw on the unhurt side, the junior's head tipped against the wheel, eyes shut (`blink` 2); Kong's face in the top of the frame searching his. On 'ไม่เต้นแล้ว' Kong's eyes widen."),
 "S54": dict(action="Low from the road: a rider in a green jacket and white helmet runs left to right over the roofs of the jam, two lanes behind the truck; in the foreground the junior's head snaps up toward the noise of his boots."),
 "S55": dict(action="James on the roofs, run cycle with every footfall planted on a roof panel, one long step across a gap between cars; terrified face over his shoulder. No delivery box: it lies on the deck where the hook left it."),
 "S56": dict(action="The junior springs onto a bonnet, then a roof (crouch, lunge, crouch on twos) and goes after the rider, left to right. The rider drops out of sight behind the bus; the junior stops on a roof, head hunting (rule 7). The space behind the truck is empty."),
 "S57": dict(ref="s37.0-1.05", action="Kong steps out from the corner; head turns left to right across the frame (`alarmed`), red then blue on his wet face. No words."),
 "S58": dict(ref="s37.0", action="Big wide down the expressway: about twenty figures (the ten extras roles and back-lit repeats) running between the cars, left to right, seen from the waist up over the bonnets so no foot contact is drawn; doors open, an umbrella rolling; two faster figures vault bonnets side-on. Beacons, hazards, sodium, the skyline.",
             why="capped crowd: the audit could not measure 40 figures (memory and CPU), and a run toward the lens needs a cycle that does not exist"),
 "S59": dict(ref="s37.2", action="Between two taxis: an infected woman in office clothes slams a running man against a car door and bites at his shoulder (both upright); behind them another goes over a bonnet on hands and feet. All heads under a tenth of the frame."),
 "S61": DEL,
 "S63": dict(ref="s40.2", action="The sedan on its left side, roof toward us (the underside is never seen and is not built): hazards ticking on the upper flank, steam, glass crumbs, a briefcase in a puddle. Praew braced at the empty windscreen frame hauling on a navy sleeve.",
             reads="an overturned car, a doctor pulling at it"),
 "S66": dict(action="Tos's face, sideways in frame: `angry`-afraid, glasses askew; the buckled door's edge lies across the bottom of the frame pressing him into the seat, and he shoves at it with his free hand; it does not give."),
 "S67": DEL,  # door insert: needs a flexing buckled panel for 60 frames; S66 now carries it
 "S68": dict(action="Long lens back down the lanes (screen left): infected running toward us between the cars, back-lit by headlights and hazards, seen from the waist up over the bonnets (twelve distinct figures, the rest silhouettes); two vault bonnets side-on in the middle distance; phases offset so no two are in step."),
 "S71": DEL,  # the cut from Kong running (S70) straight to the jaws is faster and reuses the hook's macro
 "S72": dict(ref="s46.0", action="The hook's S08 jaw staging on new metal: the tips go into the gap between the buckled door frame and the seat and open; the frame bends away in three pushes (pump recoil each time)."),
 "S73": dict(ref="s46.1"),
 "S74": DEL,  # gauge macro with the blinking bar
 "S76": dict(action="James mid-run in profile, looking back over his shoulder with `scared`; white helmet, green jacket, no box."),
 "S78": dict(action="On the bus roof behind him: the junior, infected, drops into a crouch, drawn back by the shout (orange long sleeves, the crest of hair, the torn neck, grey-green skin, red pupils). Kong's head and shoulder are a dark shape at the right edge, turned to him."),
 "S79": dict(action="All four run left to right to the truck: James first, Praew with Tos's arm, Kong last and looking back; far behind, heads and shoulders of the horde above the car roofs, closing."),
 "S83": dict(cls="B", set="CAB", size="POV side", action="From the rear bench through the side window as the cab moves off: the junior's palms slide off the wet glass, he runs three steps beside the truck and falls behind; wrecks and the barrier slide past (the camera and cab shell travel along the shoulder; the truck's exterior and wheels are not seen).",
             camera="locked to the cab; road shake", lens="28 mm", reads="the friend falling behind outside the window", sound="diesel, tyres on water, a mirror scrape",
             why="no exterior of a moving truck: nothing in the set moves today, and turning wheels plus lights that follow the body were a day of work for one 2.6 s shot"),
 "S85": dict(action="Low, behind the rescue truck, which has just stopped (nose dips and settles over 6 f, brake lights flaring on the wet road): ahead in its headlights a six-wheel box truck slewed across all three lanes, cab against the left barrier. Beside the cab, at the barrier, a small steel gate under one dim lamp.",
             camera="locked, low", size="W low", reads="a wall of lorry across the road"),
 "S92": dict(cls="B", why="it is the S87 console setup, not a hook macro"),
 "S94": dict(action="From the truck's roof looking back and left: the horde comes through four gaps between cars, converging on us, seen from the waist up over the bonnets; two cross a roof side-on."),
 "S104": dict(action="Across the shelves: the big orange trauma bag, a defibrillator case, an oxygen cylinder, rope, a folded stretcher, helmets, an extinguisher, a battery charger with its slot empty (one code-drawn shelf-wall texture with shallow relief); standing proud of it as real props, the cutter case, the crowbar in its clips, a small red pouch and a box of road flares."),
 "S105": dict(action="Four cuts on the four words, one glove each: (a) the cutter lifted by its D-handle, three LEDs steady; (b) the crowbar pulled from its clips; (c) the chest radio's volume knob turned down to zero, LED still on; (d) the small red first-aid pouch taken and pushed into Praew's blue gloves."),
 "S109": dict(action="Road level, side-on to their run: the horde peels off the truck and crosses the frame after the skittering red light, long shadows sweeping between their legs (sprint cycle, planted, at most twelve figures); three stay hammering at the truck's rear."),
 "S114": dict(action="The service stair, side-on from the next pier: the deck edge and the top two flights bolted to the pier, rain falling past. Four small figures go through the gate and down, left to right, planted on the treads, and out of the bottom of the frame; above them red flare glow and running silhouettes on the deck.",
              camera="crane down with them 1.0 D", why="one flight module, instanced; the full six-flight tower is never in one frame"),
 "S115": DEL,  # boots insert at 100 %: it would put the one new gait (stairs) under the closest lens for 39 frames
 "S121": DEL,
 "S130": dict(set="UND", size="OTS", action="Past Kong's ear and the glowing edge of the phone: Praew and James have stopped and watch him, hearing the small voice; Tos stands apart at the pier, arms crossed. Nobody moves but for breath and the drips.",
              camera="locked; 2 % creep", lens="50 mm", reads="the others listening to a voice in a phone", sound="her voice, phone band, an engine and a megaphone behind it",
              why="the bus-window shot of Namnuea needs its own set and her full puppet for 3 s; the screenplay keeps her a voice in EP.1 (see PRODUCTION_PLAN, decision 6)"),
 "S134": DEL,
 "S140": dict(action="The riverside hospital: a six-storey block with lit windows and a plain lit cross drawn for this film, the river and its reflections to the right, a sodium-lit forecourt full of small seated silhouettes; in the foreground a tall steel sliding gate. Four figures arrive from the left."),
 "S145": dict(action="The hook's jaw macro with the gauge in the same frame: steel tips round a chain link, three green LEDs steady.", reads="jaws on a chain, three green lights", sound="motor click, ready"),
 "S148": dict(action="Through the bars, wide: the guard has stepped back; behind him the seated silhouettes on the forecourt lift their heads to the cutter, one pulls a smaller shape close. Extras roles in silhouette against the lit entrance, heads under a tenth of the frame.",
              why="no new nurse, child, old man and drip stand for one 2.6 s shot"),
 "S150": dict(action="The next lot along the river: a bare concrete frame against the sky, a few scaffold tubes in silhouette, no light in it; a corrugated site hoarding with one panel bent open."),
 "S151": dict(ref="s95.2", action="On 'มืดสนิท': the four slip through the gap in the hoarding one at a time, left to right; Kong last, looking back."),
 "S154": dict(ref="s97.2"),
 "S159": dict(size="FLASH", action="Seven frames of S47 again (the junior's eyes snapping open), tinted red, then eighteen of Kong's eye from S158's setup held under it at 30 %: a memory, cut on the word.", camera="reuse of rendered frames", reads="the red eyes opening",
              why="reuses rendered frames; nothing new is drawn"),
}
def _remap(txt, m):
    return re.sub(r"\b([sS]\d+)\b", lambda g: m.get(g.group(1), g.group(1)), txt)
def build():
    # ---------- narration
    rows = []
    for (lab, sc, who, caps, em, gap, fx, trim, beat) in D.S:
        did = D.LABEL[lab]
        e = NE.get(did, {})
        if did in NE and e is DEL: continue
        r = dict(draft_id=did, scene=sc, who=who, caps=list(e.get("caps", caps)), emph=e.get("emph", [em] if em else []), gap=e.get("gap", gap),
                 fx=e.get("fx", D.relabel(fx)), trim=e.get("trim", trim), beat=e.get("beat", D.relabel(beat)),
                 edit=("edited: " + e["why"]) if "why" in e else ("retimed" if e else "kept"))
        rows.append(r)
        for (aft, key, sc2, who2, caps2, em2, gap2, fx2, beat2, why2) in NI:
            if aft == did: rows.append(dict(draft_id=key, scene=sc2, who=who2, caps=caps2, emph=em2, gap=gap2, fx=fx2, trim=0, beat=beat2, edit="new: " + why2))
    smap = {r["draft_id"]: "s%d" % (17 + i) for i, r in enumerate(rows)}
    for did in NE:
        if NE[did] is DEL: smap[did] = did + "(cut)"
    out = []; t = D.HOOK_END
    for i, r in enumerate(rows):
        gap = r["gap"]
        if isinstance(gap, tuple) and gap[0] == "at":
            assert gap[1] >= t - 1e-6, (r["draft_id"], gap[1], t)
            pause = gap[1] - t; t0 = gap[1]
        else:
            g = gap[1] if isinstance(gap, tuple) else gap
            pause = g; t0 = t + g
        cl = []; tc = t0
        for j, c in enumerate(r["caps"]):
            d = max(0.42, n(spoken(c)) / D.CPS) + (D.TAIL if j == len(r["caps"]) - 1 else 0.0)
            e = dict(text=c, t0=round(tc, 3), t1=round(tc + d, 3))
            for em in r["emph"]:
                if em[0] == j:
                    assert em[1] in c, (r["draft_id"], em)
                    e["emph"] = em[1]; e["colour"] = em[2]
            cl.append(e); tc += d
        tts = " ".join(spoken(c) for c in r["caps"])
        out.append(dict(id="s%d" % (17 + i), draft_id=r["draft_id"], scene=r["scene"], speaker=r["who"], tts=tts, text=" ".join(r["caps"]), start=round(t0, 3), dur=round(tc - t0, 3),
                        end=round(tc, 3), voiced=round(tc - t0 - D.TAIL, 3), pause_before=round(pause, 3), chars=n(tts), chars_billed=len(tts), captions=cl,
                        fx=r["fx"], optional_trim=bool(r["trim"]), beat=r["beat"], edit=r["edit"]))
        t = tc
    by = {s["draft_id"]: s for s in out}
    # ---------- shots
    base = []; scene = None; k = 0
    for h in DS.H:
        if isinstance(h, str): scene = h; continue
        did = "S%d" % (25 + k); k += 1
        e = SE.get(did, {})
        if did in SE and e is DEL: continue
        f = dict(draft_id=did, scene=scene, ref=h[0], cls=h[1], set=h[2], size=h[3], action=h[4], camera=h[5], lens=h[6], reads=h[7], sound=h[8])
        why = e.get("why"); f.update({a: b for a, b in e.items() if a != "why"})
        f["edit"] = ("edited: " + why) if why else ("edited" if e else "kept")
        base.append(f)
        for (aft, key, sc2, ref2, cls2, set2, size2, act2, cam2, lens2, reads2, snd2, why2) in SI:
            if aft == did: base.append(dict(draft_id=key, scene=sc2, ref=ref2, cls=cls2, set=set2, size=size2, action=act2, camera=cam2, lens=lens2, reads=reads2, sound=snd2, edit="new: " + why2))
    xmap = {f["draft_id"]: "S%d" % (25 + i) for i, f in enumerate(base)}
    for did in SE:
        if SE[did] is DEL: xmap[did] = did + "(cut)"
    def tref(r):
        if r[0] == "@": return float(r[1:]), None
        m = re.match(r"([sn]\d+)\.(\d+)([+-][\d.]+)?$", r); s = by[m.group(1)]; c = s["captions"][int(m.group(2))]
        off = float(m.group(3) or 0)
        return c["t0"] + off, (c["text"] if off == 0 else None)
    for f in base: f["t"], f["word"] = tref(f["ref"])
    for a, b in zip(base, base[1:]): assert b["t"] > a["t"], (a["draft_id"], b["draft_id"], a["t"], b["t"])
    end = base[-1]["t"] + DS.END_PAD
    allmap = dict(smap); allmap.update(xmap)
    S = []
    for i, f in enumerate(base):
        t0 = f["t"]; t1 = base[i + 1]["t"] if i + 1 < len(base) else end
        f0 = int(round(t0 * FPS)); f1 = int(round(t1 * FPS))
        assert f1 - f0 >= 8, (f["draft_id"], t0, t1)
        cov = []
        for s in out:
            caps = [c["text"] for c in s["captions"] if c["t0"] < t1 - 0.02 and c["t1"] > t0 + 0.02 and (min(c["t1"], t1) - max(c["t0"], t0)) > 0.25 * (c["t1"] - c["t0"])]
            if caps: cov.append(dict(id=s["id"], captions=caps))
        S.append(dict(id="S%d" % (25 + i), draft_id=f["draft_id"], scene=f["scene"], t0=round(t0, 3), t1=round(t1, 3), f0=f0, f1=f1, frames=f1 - f0, cls=f["cls"], set=f["set"], size=f["size"],
                      action=_remap(f["action"], xmap), camera=f["camera"], lens=f["lens"], reads=f["reads"], sound=f["sound"], narration=cov, cut_on=f["word"] or "(picture beat, no word)", edit=f["edit"]))
    for s in out:
        s["fx"] = _remap(s["fx"], allmap); s["beat"] = _remap(s["beat"], allmap)
        s["shots"] = [x["id"] for x in S if any(q["id"] == s["id"] for q in x["narration"])]
    return out, S, smap, xmap
if __name__ == "__main__":
    N, S, smap, xmap = build()
    from collections import Counter
    for s in N: print(s["id"], s["draft_id"], s["scene"], "%7.2f %5.2f p%.2f" % (s["start"], s["dur"], s["pause_before"]), s["text"], "|", " ".join(s["shots"]))
    cf = Counter(); cn = Counter()
    for x in S: cf[x["cls"]] += x["frames"]; cn[x["cls"]] += 1
    print(len(N), "sentences", len(S), "shots", S[-1]["t1"], S[-1]["f1"], dict(cf), dict(cn))
    print("chars", sum(s["chars"] for s in N), "billed", sum(s["chars_billed"] for s in N))
    for x in S:
        if x["frames"] > 90 or x["frames"] < 18: print("len", x["id"], x["draft_id"], x["cls"], x["frames"], x["cut_on"])
        if not x["narration"]: print("no words", x["id"], x["draft_id"], x["frames"])
    seen = {}
    for s in N:
        for c in s["captions"]:
            k = c["text"]; v = (c.get("emph"), c.get("colour"))
            if k in seen and seen[k] != v: print("EMPH CLASH", k, seen[k], v)
            seen[k] = v
