#!/usr/bin/env python3
"""shotlist_check.py — check an episode plan against the CINEMA BIBLE (owner 6 Nov 2569, video/release/CINEMA-BIBLE.md).

usage:
  python3 shotlist_check.py --schedule schedule.json --shotlist shotlist.json [--soundplan soundplan.json] [--cues sfx_cues.json]

  schedule.json   the episode schedule (shots with key/start/dur, vo lines with id/t/dur/cap); commands are captions with "{อย่า"
  shotlist.json   {"total": s, "cuts": [{"n","key","t","dur","emotion","size","angle","move","lead_sound","fg","light",
                   "face_w","hold","threat_first","note", optional "deg","silhouette","command","command_t","expect"}]}  · one entry per cut, absolute times
                  commands = captions that start with "{อย่า" + the first line inside a cut marked "command": true
                  + "command_t": <seconds> on a cut = the exact time of the word "อย่า" inside a longer line
                  - "command": false on a cut = its red-box line is a mid-story rule, not a real command (no full silence needed)
  soundplan.json  {"drone_start": t, "silences": [[t0, t1], ...], "sting": t, "bpm": [[t, bpm], ...], "ambience": [...]}
  sfx_cues.json   the mix's cue list {"sfx": [{"t", "type", "gain"}]} (type "sting" is counted)

Prints ok / WARN / FAIL lines and exits 1 when anything FAILs. A WARN needs a reason in that cut's "note".
"""
import argparse
import json
import sys

EMOTIONS = {"hook", "safe", "uneasy", "fear", "choice", "twist", "lesson"}
SIZES = {"ECU", "CU", "MCU", "MS", "WS", "EWS"}
MOVES = {"cut", "hold", "pushIn", "pullOut", "whip", "dutch", "shake"}
# seconds per cut by emotion (CINEMA BIBLE §1 and §4)
RANGE = {"hook": (0.8, 1.2), "safe": (2.0, 3.0), "uneasy": (4.0, 6.0), "fear": (0.5, 1.5), "choice": (1.8, 2.6),
         "twist": (3.0, 4.0), "lesson": (0.0, 2.0)}
TOL = 0.05
FACE_MIN = 270  # px at 1080 wide = 1/4 of the frame


class Report:
    def __init__(self):
        self.fails, self.warns = 0, 0

    def ok(self, msg):
        print(f"ok    {msg}")

    def warn(self, msg):
        self.warns += 1
        print(f"WARN  {msg}")

    def fail(self, msg):
        self.fails += 1
        print(f"FAIL  {msg}")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def commands(sched, forced=()):
    """(absolute start, end, caption, shot key) of every command line, plus every voice line's span.
    A command is a caption that starts with the red box "{อย่า…" (rhyme lines that only contain one are not),
    or the first voice line inside a cut marked "command": true in the shot list."""
    cmds, lines = [], []
    for sh in sched.get("shots", []):
        for v in sh.get("vo", []):
            a = sh["start"] + v["t"]
            b = a + v.get("dur", 0)
            cap = v.get("cap", "")
            lines.append((a, b, v.get("id", "")))
            if cap.strip().startswith("{อย่า") or any(f0 - 1e-6 <= a < f1 for f0, f1 in forced):
                cmds.append((a, b, cap, sh["key"]))
    seen, out = set(), []
    for c in sorted(cmds):
        win = next(((f0, f1) for f0, f1 in forced if f0 - 1e-6 <= c[0] < f1), None)
        if win and win in seen:
            continue  # one command per marked cut
        if win:
            seen.add(win)
        out.append(c)
    return out, sorted(lines)


def cut_at(cuts, t):
    for c in cuts:
        if c["t"] - 1e-6 <= t < c["t"] + c["dur"]:
            return c
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--schedule", required=True)
    ap.add_argument("--shotlist", required=True)
    ap.add_argument("--soundplan")
    ap.add_argument("--cues")
    a = ap.parse_args()
    R = Report()
    sched = load(a.schedule)
    sl = load(a.shotlist)
    total = float(sched.get("total") or sl.get("total") or 0)
    cuts = sorted(sl.get("cuts", []), key=lambda c: c["t"])
    sp = load(a.soundplan) if a.soundplan else None
    cues = load(a.cues) if a.cues else None
    print(f"== {a.shotlist}: {len(cuts)} cuts · {total:.2f} s")

    # ---- the plan covers the episode, one emotion per cut ----
    if not cuts:
        R.fail("ไม่มีคัตใน shot list")
        return 1
    if abs(cuts[0]["t"]) > TOL:
        R.fail(f"คัตแรกเริ่มที่ {cuts[0]['t']:.2f} วิ ไม่ใช่ 0")
    for p, q in zip(cuts, cuts[1:]):
        gap = q["t"] - (p["t"] + p["dur"])
        if abs(gap) > TOL:
            R.fail(f"คัต {p['n']}→{q['n']}: {'ช่องว่าง' if gap > 0 else 'ซ้อนกัน'} {abs(gap):.2f} วิ ที่ {p['t'] + p['dur']:.2f}")
    end = cuts[-1]["t"] + cuts[-1]["dur"]
    if total and abs(end - total) > 0.1:
        R.fail(f"คัตสุดท้ายจบที่ {end:.2f} วิ แต่ตอนยาว {total:.2f} วิ")
    bad = [c for c in cuts if c.get("emotion") not in EMOTIONS]
    if bad:
        R.fail("ช็อตไม่มีอารมณ์ (ตัดทิ้งหรือใส่อารมณ์): " + ", ".join(f"{c['n']}@{c['t']:.1f}" for c in bad))
    else:
        R.ok("ทุกคัตมีอารมณ์ 1 อย่าง")
    for c in cuts:
        if c.get("size") not in SIZES:
            R.warn(f"คัต {c['n']}: ขนาดช็อต '{c.get('size')}' ไม่อยู่ใน {sorted(SIZES)}")
        if c.get("move") not in MOVES:
            R.warn(f"คัต {c['n']}: การเคลื่อน '{c.get('move')}' ไม่อยู่ใน {sorted(MOVES)}")

    # ---- number of cuts ----
    if 60 <= total <= 120:
        lo, hi = 18, 30
    else:
        lo, hi = round(total * 0.15), round(total * 0.25)
    (R.ok if lo <= len(cuts) <= hi else R.fail)(f"จำนวนคัต {len(cuts)} (เกณฑ์ {lo}–{hi} สำหรับ {total:.0f} วิ)")

    # ---- the hook: 3 cuts in 3 s, cut, no move ----
    hook = [c for c in cuts if c["t"] < 3.0 - 1e-6]
    if len(hook) < 3:
        R.fail(f"ฮุก 0–3 วิมี {len(hook)} คัต (ต้อง 3 คัต ช็อตละ 0.8–1.2 วิ)")
    else:
        R.ok(f"ฮุก 0–3 วิมี {len(hook)} คัต")
    for c in hook:
        if c.get("move") not in ("cut", "hold"):
            R.fail(f"คัต {c['n']} ในฮุก: การเคลื่อน '{c.get('move')}' ฮุกต้องตัดทันที ไม่เคลื่อน")

    # ---- length by emotion ----
    for c in cuts:
        emo = c.get("emotion")
        if emo not in RANGE:
            continue
        lo_, hi_ = RANGE[emo]
        if c.get("hold"):
            continue
        if emo == "hook" and hook and c is hook[-1]:
            hi_ = max(hi_, 3.4 - c["t"])  # the last hook cut may run on into the command
        if not (lo_ - TOL <= c["dur"] <= hi_ + TOL):
            msg = f"คัต {c['n']} ({emo}) ยาว {c['dur']:.2f} วิ เกณฑ์ {lo_}–{hi_} วิ"
            R.warn(msg + (f" · เหตุผล: {c['note']}" if c.get("note") else " · ไม่มีเหตุผลใน note"))
    for c in cuts:
        if c.get("emotion") == "choice" and c.get("move") != "hold":
            R.fail(f"คัต {c['n']} (ทางเลือกที่เจ็บ) ต้องนิ่งสนิท move = hold (ตอนนี้ {c.get('move')})")
        if c.get("emotion") == "twist" and c.get("move") != "pullOut":
            R.warn(f"คัต {c['n']} (หักมุม) ควรเป็น pull-out ช้า (ตอนนี้ {c.get('move')})")
        if c.get("move") == "dutch":
            if c.get("emotion") != "fear":
                R.warn(f"คัต {c['n']}: dutch angle ใช้เฉพาะจุดที่โลกพัง (fear) · ตอนนี้ {c.get('emotion')}")
            deg = c.get("deg", 10)
            if not 8 <= abs(deg) <= 12:
                R.warn(f"คัต {c['n']}: dutch {deg}° (เกณฑ์ 8–12°)")
        if c.get("move") == "whip" and c.get("emotion") != "fear":
            R.warn(f"คัต {c['n']}: whip-pan ใช้ในช่วงภัย · ตอนนี้ {c.get('emotion')}")

    # ---- one overlong 'uneasy' hold per episode ----
    holds = [c for c in cuts if c.get("hold")]
    if len(holds) != 1:
        R.warn(f"ช็อตค้างนานเกินคาด (hold: true) มี {len(holds)} คัต · ต้องมี 1 คัตต่อตอน")
    for c in holds:
        # "expect" = how long the viewer expects this kind of shot to stay (e.g. 3.0 for an insert); default = the middle of its range
        lo_, hi_ = RANGE.get(c.get("emotion"), (2.0, 3.0))
        exp = float(c.get("expect") or (lo_ + hi_) / 2)
        if c.get("emotion") != "uneasy":
            R.warn(f"คัต {c['n']} hold: ช็อตที่ค้างนานเกินคาดควรเป็นช่วงผิดปกติ (uneasy) · ตอนนี้ {c.get('emotion')}")
        if c["dur"] < 1.5 * exp - TOL:
            R.warn(f"คัต {c['n']} hold ยาว {c['dur']:.2f} วิ ต้อง ≥ 1.5 × ที่คนดูคาด ({exp:.1f} วิ) = {1.5 * exp:.2f} วิ")
        else:
            R.ok(f"ช็อตค้างนานเกินคาด: คัต {c['n']} {c['dur']:.1f} วิ (คาด {exp:.1f} วิ)")

    # ---- commands: pause 0.3 s, silence 1 s, still shot ----
    cmds, lines = commands(sched, [(c["t"], c["t"] + c["dur"]) for c in cuts if c.get("command") and not c.get("command_t")])
    # "command": false on a cut = its red-box "{อย่า…}" line is a mid-story rule, not a real command (hook/choice):
    # the red box stays, a short dip is enough, no full 1 s silence / pause / slow-down is required
    exempt = [(c["t"], c["t"] + c["dur"]) for c in cuts if c.get("command") is False]
    if exempt:
        keep = [x for x in cmds if not any(f0 - 1e-6 <= x[0] < f1 for f0, f1 in exempt)]
        for x in cmds:
            if x not in keep:
                R.ok(f"กล่องแดง {x[2]} ที่ {x[0]:.2f} วิ อยู่ในคัตที่ตั้ง \"command\": false (กฎกลางเรื่อง ไม่ใช่คำสั่งจริง ใช้ dip สั้นๆ ได้)")
        cmds = keep
    # a cut can name the exact time of the word "อย่า" (e.g. from Whisper word times) when it sits inside a longer line
    for c in cuts:
        if c.get("command_t") is not None:
            ct = float(c["command_t"])
            cmds = [x for x in cmds if abs(x[0] - ct) > 0.05] + [(ct, ct + 1.0, f"(คัต {c['n']} command_t)", c.get("key", ""))]
    cmds.sort()
    if not cmds:
        R.warn("ไม่เจอคำสั่ง '{อย่า…}' ใน schedule")
    silences = (sp or {}).get("silences", [])
    for (ca, cb, cap, key) in cmds:
        prev = [l for l in lines if l[1] <= ca + 1e-6 and l[0] < ca - 1e-6]
        gap = ca - max((l[1] for l in prev), default=-9)
        if prev:
            (R.ok if gap >= 0.3 - 0.02 else R.fail)(f"คำสั่ง {cap} ที่ {ca:.2f} วิ: เว้นก่อน 'อย่า' {gap:.2f} วิ (ต้อง ≥ 0.3)")
        if ca < 3.6:
            if ca > 3.5:
                R.fail(f"คำสั่งในฮุกขึ้นที่ {ca:.2f} วิ (เกิน 3.5)")
            elif ca > 3.0:
                R.warn(f"คำสั่งในฮุกขึ้นที่ {ca:.2f} วิ (เป้า ≤ 3.0)")
            else:
                R.ok(f"คำสั่งในฮุกขึ้นที่ {ca:.2f} วิ")
        if sp is not None:
            need = 1.0
            covered = any(s0 <= ca - need + TOL and s1 >= ca - TOL for s0, s1 in silences)
            (R.ok if covered else R.fail)(f"เงียบ ≥ {need:.1f} วิก่อน 'อย่า' ที่ {ca:.2f} วิ (ชั้นเพลง บรรยากาศ SFX เหลือแค่ลมหายใจ)")
        c = cut_at(cuts, ca)
        if c and ca >= 3.0 and c.get("emotion") != "choice":
            R.warn(f"คำสั่ง {cap} ที่ {ca:.2f} วิ อยู่ในคัต {c['n']} ({c.get('emotion')}) · ช็อตทางเลือกที่เจ็บควรเป็น choice นิ่ง 2 วิ")
    if sp is None:
        R.warn("ไม่มี soundplan.json จึงตรวจช่วงเงียบ drone และ sting ไม่ได้")

    # ---- sting: once per episode ----
    stings = [x for x in (cues or {}).get("sfx", []) if x.get("type") == "sting" and x.get("gain", 1) > 0]
    if cues is not None:
        (R.ok if len(stings) == 1 else R.fail)(f"sting ใน cue ของมิกซ์ {len(stings)} ครั้ง (ต้อง 1 ครั้งต่อตอน ตอนภัยเผยตัวจริง)")
    if sp is not None:
        st = sp.get("sting")
        if st is None:
            R.fail("soundplan ไม่มีจุด sting")
        else:
            if stings and all(abs(x["t"] - st) > 0.3 for x in stings):
                at = ", ".join("%.2f" % x["t"] for x in stings)
                R.warn(f"sting ในแผนเสียง {st:.2f} วิ ไม่ตรงกับ cue ({at})")
            pre = any(abs(s1 - st) <= 0.15 and 0.5 - TOL <= s1 - s0 <= 1.0 + TOL for s0, s1 in silences)
            (R.ok if pre else R.warn)(f"ตัดเงียบสนิท 0.5–1 วิ ก่อน sting ที่ {st:.2f} วิ")
        ds = sp.get("drone_start")
        first_uneasy = next((c["t"] for c in cuts if c.get("emotion") == "uneasy"), None)
        if ds is None:
            R.warn("soundplan ไม่มีจุดเริ่ม drone")
        elif first_uneasy is not None and abs(ds - first_uneasy) > 3:
            R.warn(f"drone เริ่ม {ds:.1f} วิ แต่ช่วงผิดปกติเริ่ม {first_uneasy:.1f} วิ")
        else:
            R.ok(f"drone เริ่ม {ds:.1f} วิ")
        bpm = sp.get("bpm") or []
        if not bpm:
            R.warn("soundplan ไม่มี bpm ของจังหวะหัวใจ (90→130)")
        elif not (80 <= bpm[0][1] <= 100 and 120 <= bpm[-1][1] <= 140):
            R.warn(f"bpm {bpm[0][1]}→{bpm[-1][1]} (เกณฑ์ 90→130)")
        else:
            R.ok(f"จังหวะหัวใจ {bpm[0][1]}→{bpm[-1][1]} bpm")

    # ---- sound before picture, faces, foreground, light, silhouette ----
    firsts = [c for c in cuts if c.get("threat_first")]
    if not firsts:
        R.warn("ไม่มีคัตที่เห็นภัยครั้งแรก (threat_first) จึงตรวจเสียงมาก่อนภาพไม่ได้")
    for c in firsts:
        ls = c.get("lead_sound") or 0
        if ls <= 0:
            R.fail(f"คัต {c['n']} เห็นภัยครั้งแรก แต่ไม่มีเสียงมาก่อนภาพ (ต้อง 1–2 วิ)")
        elif not 1.0 - TOL <= ls <= 2.0 + TOL:
            R.warn(f"คัต {c['n']}: เสียงมาก่อนภาพ {ls:.1f} วิ (เกณฑ์ 1–2 วิ)")
        else:
            R.ok(f"คัต {c['n']}: เสียงภัยมาก่อนภาพ {ls:.1f} วิ")
        if not c.get("silhouette") and "silhouette" not in (c.get("note") or "") and "เงา" not in (c.get("note") or ""):
            R.warn(f"คัต {c['n']} เห็นภัยครั้งแรก: ควรเป็น backlight/silhouette (ใส่ silhouette หรือเขียนเหตุผลใน note)")
    for c in cuts:
        emo = c.get("emotion")
        if emo in ("choice", "twist") or (emo == "fear" and c.get("size") in ("ECU", "CU")):
            fw = c.get("face_w") or 0
            if fw and fw < FACE_MIN:
                R.fail(f"คัต {c['n']} ({emo}): หน้ากว้าง {fw} px ต่ำกว่า {FACE_MIN} (1/4 ของเฟรม)")
            elif not fw and "ไม่มีหน้า" not in (c.get("note") or ""):  # a cut of a bottle, an empty ring or a choice board says so in its note
                R.warn(f"คัต {c['n']} ({emo}): ยังไม่ได้วัดความกว้างหน้า (face_w)")
        if emo != "lesson" and not c.get("fg"):
            R.warn(f"คัต {c['n']}: ไม่มี foreground ขวางมุมเฟรม")
        if emo in ("fear", "choice") and not c.get("light"):
            R.warn(f"คัต {c['n']} ({emo}): ไม่ได้ระบุแหล่งแสงในเรื่อง")

    print(f"== สรุป: FAIL {R.fails} · WARN {R.warns}")
    return 1 if R.fails else 0


if __name__ == "__main__":
    sys.exit(main())
