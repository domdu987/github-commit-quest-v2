#!/usr/bin/env python3
"""longplan_check.py — check a 16:9 long's plan against CINEMA BIBLE §7 ("the long is a film, not Shorts glued together").

Usage:  python3 longplan_check.py --plan video/<story>-long/production/longplan.json [--rendered-total 283.4]

longplan.json (absolute times in the long, seconds):
{
  "title": "หนวดใส ฉบับเต็ม",
  "total": 300.0,
  "segments": [                      # in order, covering 0 → total
    {"id": "cold",  "kind": "cold_open", "start": 0,   "end": 18,  "long_only": true},
    {"id": "title", "kind": "title",     "start": 18,  "end": 21},
    {"id": "ep1",   "kind": "episode",   "start": 21,  "end": 110, "from": "EP.1"},
    {"id": "secret","kind": "secret",    "start": ..., "end": ..., "long_only": true},
    {"id": "lesson","kind": "lesson",    ...},
    {"id": "epi",   "kind": "epilogue",  "start": ..., "end": ..., "long_only": true},
    {"id": "card",  "kind": "end_card",  ...}
  ],                                 # other kinds: bridge, threat, credits
  "acts": [{"n": 1, "start": 0, "end": 75}, {"n": 2, ...}, {"n": 3, ...}],
  "chapters": [{"t": 0, "title": "..."}, ...],
  "hook_t": 20.9,                    # where the Shorts EP.1 hook command lands in the long
  "silences": [{"start": 150.0, "end": 154.0}],          # long silences only (3–5 s)
  "theme": [{"t": 3, "label": "open"}, {"t": 160, "label": "choice"}, {"t": 280, "label": "epilogue", "key": "+2"}],
  "choices": [{"t": 120.5}, {"t": 170.2}],               # painful choices
  "biggest_threat": {"t": 200.0, "long_only": true},     # the largest danger, never shown in the Shorts
  "extreme_wide": [{"t": 25, "act": 1}, {"t": 140, "act": 2}, {"t": 260, "act": 3}],
  "credits_ambience": 5.0,           # seconds of held ambience over the credits before silence
  "end_card": {"next": "เรื่องต่อไป: <ชื่อ> ทุกวัน 09:30", "subscribe": true, "prev_long_link": true}
}
Long-only share counts only kinds cold_open, bridge, secret, epilogue and threat; a long_only flag on a title,
episode, lesson, end card or credits segment is reported (WARN) and not counted.
The end card's next-story name may stay a placeholder ("…") while planning (WARN); with --rendered-total
(the check of the finished file) a placeholder is a FAIL.
Exit code 1 on any FAIL.
"""
import argparse
import json
import re
import sys


class Report:
    def __init__(self):
        self.fails = self.warns = 0

    def ok(self, m):
        print(f"ok    {m}")

    def warn(self, m):
        self.warns += 1
        print(f"WARN  {m}")

    def fail(self, m):
        self.fails += 1
        print(f"FAIL  {m}")

    def check(self, cond, m, warn_only=False):
        (self.ok if cond else (self.warn if warn_only else self.fail))(m)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--rendered-total", type=float, help="length of the rendered long, to compare with the plan")
    a = ap.parse_args()
    P = json.load(open(a.plan, encoding="utf-8"))
    R = Report()
    total = float(P["total"])
    segs = sorted(P.get("segments", []), key=lambda s: s["start"])
    print(f"== {P.get('title', a.plan)} · {total:.1f} s · {len(segs)} segments")

    # ---- segments cover the film without gaps ----
    t = 0.0
    for s in segs:
        if abs(s["start"] - t) > 0.05:
            R.fail(f"ช่วง {s['id']} เริ่ม {s['start']:.2f} แต่ช่วงก่อนจบ {t:.2f} (มีช่องว่างหรือซ้อน)")
        t = s["end"]
    R.check(abs(t - total) <= 0.05, f"ช่วงทั้งหมดจบที่ {t:.2f} (total {total:.2f})")
    if a.rendered_total:
        R.check(abs(a.rendered_total - total) <= 0.1, f"ความยาวไฟล์จริง {a.rendered_total:.2f} ตรงกับแผน {total:.2f}")

    def kind(k):
        return [s for s in segs if s.get("kind") == k]

    # ---- long-only scenes ≥ 25 % ----
    # Only scenes made for the film count: cold open, bridges, the secret, the epilogue and a film-only threat scene.
    # The title, end card and credits are not scenes, and EP.3 / lesson stay episode material (the momentum valve
    # may still cut EP.3 into a Short), so they never count even when flagged long_only.
    counted_kinds = {"cold_open", "bridge", "secret", "epilogue", "threat"}
    lo = [s for s in segs if s.get("long_only") and s.get("kind") in counted_kinds]
    skipped = [s for s in segs if s.get("long_only") and s.get("kind") not in counted_kinds]
    if skipped:
        R.warn("long_only ที่ไม่นับ (ไตเติล การ์ด เครดิต ตอน บทเรียน ไม่ใช่ฉากที่ทำเพื่อหนัง): "
               + ", ".join(f"{s['id']} ({s.get('kind')})" for s in skipped) + " · แก้ในแผนให้เป็น false")
    lo_len = sum(s["end"] - s["start"] for s in lo)
    R.check(lo_len >= 0.25 * total - 1e-6,
            f"ฉากเฉพาะฉบับยาวรวม {lo_len:.1f} วิ = {100 * lo_len / total:.1f}% (ต้อง ≥ 25%) · {', '.join(s['id'] for s in lo) or '-'}")
    R.check(len(lo) >= 3, f"ฉากเฉพาะฉบับยาว {len(lo)} ฉาก (ต้อง ≥ 3)")

    cold = kind("cold_open")
    if not cold:
        R.fail("ไม่มี cold open (ฉากอดีตที่เป็นที่มาของกฎ 15–20 วิ ก่อนไตเติล)")
    else:
        c = cold[0]
        d = c["end"] - c["start"]
        R.check(c["start"] <= 0.05, f"cold open เริ่มที่ {c['start']:.2f} (ต้องเริ่มคลิป)")
        R.check(15 - 1e-6 <= d <= 20 + 1e-6, f"cold open ยาว {d:.1f} วิ (15–20)")
        R.check(bool(c.get("long_only")), "cold open เป็นฉากเฉพาะฉบับยาว")
        ttl = kind("title")
        if ttl:
            R.check(ttl[0]["start"] >= c["end"] - 0.05, f"ไตเติลขึ้นหลัง cold open ({ttl[0]['start']:.2f})")
        else:
            R.warn("ไม่มีช่วง title ในแผน (ไตเติลต้องขึ้นหลัง cold open)")

    sec = kind("secret")
    R.check(bool(sec) and all(s.get("long_only") for s in sec),
            "มีฉาก \"ความลับของคน\" เต็มความยาว และเป็นฉากเฉพาะฉบับยาว" if sec else "ไม่มีฉาก \"ความลับของคน\" (secret)")

    epi = kind("epilogue")
    if not epi:
        R.fail("ไม่มีบทส่งท้าย 20–30 วิ หลังบทเรียน")
    else:
        e = epi[-1]
        d = e["end"] - e["start"]
        R.check(20 - 1e-6 <= d <= 30 + 1e-6, f"บทส่งท้ายยาว {d:.1f} วิ (20–30)")
        les = kind("lesson")
        if les:
            R.check(e["start"] >= les[-1]["start"], f"บทส่งท้ายมาหลังบทเรียน ({e['start']:.1f} ≥ {les[-1]['start']:.1f})")
        else:
            R.warn("ไม่มีช่วง lesson ในแผน จึงตรวจลำดับบทเรียน → ส่งท้ายไม่ได้")

    # ---- the Shorts EP.1 hook inside the first 30 s ----
    h = P.get("hook_t")
    R.check(h is not None and h <= 30.0, f"ฮุกเดียวกับ Shorts EP.1 ขึ้นที่ {h} วิ (ต้องอยู่ใน 30 วิแรก)")

    # ---- three acts 25 / 50 / 25 and chapters ----
    acts = sorted(P.get("acts", []), key=lambda x: x["start"])
    if len(acts) != 3:
        R.fail(f"มี {len(acts)} องก์ (ต้อง 3)")
    else:
        for x, (lo_p, hi_p) in zip(acts, [(18, 32), (40, 60), (18, 32)]):
            p = 100 * (x["end"] - x["start"]) / total
            R.check(lo_p <= p <= hi_p, f"องก์ {x['n']} ยาว {p:.0f}% (เป้า {(lo_p + hi_p) // 2}% · รับ {lo_p}–{hi_p}%)", warn_only=True)
    ch = sorted(P.get("chapters", []), key=lambda c: c["t"])
    R.check(len(ch) >= 3 and ch and ch[0]["t"] == 0, f"chapters {len(ch)} ข้อ เริ่มที่ 0:00 (YouTube ต้อง ≥ 3 ข้อ)")
    gaps = [b["t"] - a_["t"] for a_, b in zip(ch, ch[1:])]
    R.check(all(g >= 10 for g in gaps), "chapters ห่างกันอย่างน้อย 10 วิทุกข้อ")
    for x in acts:
        R.check(any(abs(c["t"] - x["start"]) <= 5 for c in ch), f"มี chapter ที่ต้นองก์ {x['n']} ({x['start']:.0f} วิ)")

    # ---- film pacing: one long silence mid-film, 2–3 painful choices, biggest threat long-only ----
    a2 = acts[1] if len(acts) == 3 else {"start": total * 0.25, "end": total * 0.75}
    sil = [s for s in P.get("silences", []) if 3 - 1e-6 <= s["end"] - s["start"] <= 5 + 1e-6]
    R.check(any(a2["start"] <= s["start"] <= a2["end"] for s in sil), f"มีความเงียบยาว 3–5 วิช่วงกลางเรื่อง ({len(sil)} จุดที่ยาว 3–5 วิ)")
    chs = [c for c in P.get("choices", []) if a2["start"] <= c["t"] <= a2["end"]]
    R.check(2 <= len(chs) <= 3, f"ทางเลือกที่เจ็บในองก์ 2: {len(chs)} จุด (2–3)")
    bt = P.get("biggest_threat")
    R.check(bool(bt) and bt.get("long_only"), "ภัยลูกใหญ่สุดอยู่ในฉบับยาวเท่านั้น (Shorts EP.2 จบค้างก่อนถึง)")

    # ---- 16:9 framing: one extreme wide per act ----
    ew = P.get("extreme_wide", [])
    for n in (1, 2, 3):
        R.check(any(e.get("act") == n for e in ew), f"มีช็อตกว้างมากในองก์ {n}")

    # ---- film sound: theme × 3 (open / choice / epilogue with key change), credits ambience ----
    th = {x.get("label"): x for x in P.get("theme", [])}
    R.check(all(k in th for k in ("open", "choice", "epilogue")), f"ธีมหลักกลับมา 3 ครั้ง (open / choice / epilogue): {sorted(th)}")
    R.check(bool(th.get("epilogue", {}).get("key")), "ธีมตอนส่งท้ายเปลี่ยนคีย์ (key)")
    R.check(float(P.get("credits_ambience", 0)) >= 5 - 1e-6, f"บรรยากาศค้างใต้เครดิต {P.get('credits_ambience', 0)} วิ (≥ 5)")

    # ---- end card ----
    ec = P.get("end_card", {})
    nxt = ec.get("next", "")
    R.check("ทุกวัน 09:30" in nxt and "เรื่องต่อไป" in nxt,
            f"การ์ดท้าย \"เรื่องต่อไป: … ทุกวัน 09:30\": {nxt or '-'}")
    m = re.search(r"เรื่องต่อไป\s*:?\s*(.*?)\s*ทุกวัน", nxt)
    name = m.group(1).strip() if m else ""
    if re.sub(r"[….<>\s]", "", name) in ("", "ชื่อ"):
        # a placeholder is fine while planning; the rendered long must carry the real name
        (R.fail if a.rendered_total else R.warn)(
            f"การ์ดท้ายยังไม่มีชื่อเรื่องต่อไป ({nxt or '-'}) · ต้องใส่ชื่อจริงก่อนเรนเดอร์")
    else:
        R.ok(f"การ์ดท้ายบอกชื่อเรื่องต่อไป: {name}")
    R.check(bool(ec.get("subscribe")), "การ์ดท้ายมีปุ่มติดตาม")
    R.check(bool(ec.get("prev_long_link")), "การ์ดท้ายลิงก์ไปคลิปยาวเรื่องก่อนหน้า")

    print(f"== สรุป: FAIL {R.fails} · WARN {R.warns}")
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
