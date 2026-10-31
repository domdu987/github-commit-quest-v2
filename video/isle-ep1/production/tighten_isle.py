import re, json, subprocess
W="/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8").write(s)
def rep1(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:90]); return s.replace(old, new)
L={l["id"] for l in json.load(open(f"{W}/isle1/lines.json"))}
assert "p03" in L, "already tightened"
# ---- lines: drop the photo joke; faster deliveries on the long lines
p=f"{W}/isle1/mklines.py"; s=rd(p)
i=s.index('ln("p03"'); j=s.index("\n", i); s=s[:i]+s[j+1:]
def tempo(s, lid, old, new):
    m=re.search(r'^ln\("%s",.*$' % lid, s, re.M); line=m.group(0)
    if "tempo_override" in line: n=line.replace(f"tempo_override={old}", f"tempo_override={new}"); assert n!=line, lid
    else:
        k=line.rfind(")", 0, line.find("#") if "#" in line else len(line)); n=line[:k]+f", tempo_override={new}"+line[k:]
    return s.replace(line, n)
s=tempo(s,"n01",None,1.4); s=tempo(s,"t09",1.2,1.3); s=tempo(s,"i01",1.38,1.42); s=tempo(s,"y05",1.32,1.38); s=tempo(s,"n10",1.4,1.46); s=tempo(s,"t12",1.28,1.34)
# n11 keeps its override on the continuation line
s=rep1(s, "จนกู้ชีพมาถึง\", tempo_override=1.42)", "จนกู้ชีพมาถึง\", tempo_override=1.5)")
wr(p, s)
# ---- timing
p=f"{W}/isle1/timing.py"; s=rd(p)
for old,new in [
 ('("yai", ["y01", ("y02", 0.25), ("t01", 0.3), ("y04", 0.3)], 0.4, 0.4, 9.0)','("yai", ["y01", ("y02", 0.2), ("t01", 0.25), ("y04", 0.25)], 0.3, 0.3, 8.0)'),
 ('("boat", ["t02", ("u01", 0.2), ("u02", 0.2)], 0.6, 0.4, 8.0)','("boat", ["t02", ("u01", 0.15), ("u02", 0.15)], 0.5, 0.35, 8.0)'),
 ('("stranded", ["n04", ("p02", 0.25), ("t03", 0.25)], 0.5, 0.3, 8.0)','("stranded", ["n04", ("p02", 0.2), ("t03", 0.2)], 0.4, 0.25, 7.5)'),
 ('("survive", ["t04"], 2.8, 0.4, 5.8)','("survive", ["t04"], 2.5, 0.3, 5.3)'),
 ('("fish", ["t05", ("t06", 0.3), ("p03", 0.3), ("p04", 0.35), ("t07", 0.3)], 0.6, 0.4, 11.0)','("fish", ["t05", ("t06", 0.3), ("p04", 0.4), ("t07", 0.3)], 0.6, 0.35, 9.0)'),
 ('("grill", ["n06", ("t08", 0.4), ("p05", 0.3)], 0.5, 0.5, 8.0)','("grill", ["n06", ("t08", 0.3), ("p05", 0.25)], 0.5, 0.4, 7.5)'),
 ('("wait", ["n07", ("t09", 0.4), ("p06", 0.25), ("t10", 0.6), ("n08", 0.25)], 0.3, 0.3, 12.0)','("wait", ["t09", ("p06", 0.2), ("t10", 0.45), ("n08", 0.2)], 1.6, 0.25, 10.0)'),
 ('("still", ["p07", ("i01", 0.3), ("n09", 0.25), ("p08", 0.3), ("p11", 0.6)], 0.4, 1.9, 14.0)','("still", ["p07", ("i01", 0.2), ("n09", 0.2), ("p08", 0.25), ("p11", 0.5)], 0.3, 1.85, 14.0)'),
 ('("rule", ["y05", ("p09", 0.6), ("n10", 0.5)], 0.8, 0.8, 11.0)','("rule", ["y05", ("p09", 0.5), ("n10", 0.4)], 0.6, 0.7, 11.0)'),
 ('("night", ["i02"], 0.5, 4.3, 8.2)','("night", ["i02"], 0.5, 3.7, 7.6)'),
 ('("dawn", ["t11", ("u03", 1.3), ("p10", 0.45)], 1.0, 1.8, 10.0)','("dawn", ["t11", ("u03", 1.1), ("p10", 0.4)], 0.9, 1.5, 9.0)'),
 ('("line", ["t12"], 0.7, 1.0, 10.0)','("line", ["t12"], 0.5, 1.0, 9.0)')]:
    s=rep1(s, old, new)
wr(p, s)
# ---- shots: fish becomes two framings (no photo), wait loses the narration, night shorter
p=f"{W}/isle1/shots.part"; s=rd(p)
a=s.index('      // ---------- 6. the fish'); b=s.index('      // ---------- 7. the grill'); blk=s[a:b]
A=blk[blk.index('        set: "pool"'):blk.index('      }, {\n        set: "beach", setOpts: { id: "fs2"')]
C=blk[blk.index('        set: "beach", setOpts: { id: "fs3"'):]
C=C.replace('VA("fish", vo("fish", 3) - 0.15, 4)', 'VA("fish", vo("fish", 2) - 0.15, 3)')
C=rep1(C, 'bubbles: [bubAt(bub("fish", 3, 700, 520, 760, { br: true, end: vo("fish", 4) - 0.05 }), vo("fish", 3) - 0.15, D("fish")), bubAt(bub("fish", 4, 460, 520, 420, { br: true }), vo("fish", 3) - 0.15, D("fish"))],',
            'bubbles: [bubAt(bub("fish", 2, 700, 520, 760, { br: true, end: vo("fish", 3) - 0.05 }), vo("fish", 2) - 0.15, D("fish")), bubAt(bub("fish", 3, 460, 520, 420, { br: true }), vo("fish", 2) - 0.15, D("fish"))],')
C=rep1(C, 'Fx.heart(tl, t0, D("fish") - (vo("fish", 3) - 0.15), 0.7, 0.4);', 'Fx.heart(tl, t0, D("fish") - (vo("fish", 2) - 0.15), 0.7, 0.4);')
assert 'vo("fish", 4)' not in C and '"fish", 3) - 0.15' not in C
new='      // ---------- 6. the fish: it swims to him; the balloon; ยาย\'s rule against ลุงนวล\'s method (the photo joke cut for pace) ----------\n      split("fish", vo("fish", 2) - 0.15, {\n'+A+'      }, {\n'+C
s=s[:a]+new+s[b:]
# wait
a=s.index('      // ---------- 8. the wait'); b=s.index('      // ---------- 9. still'); blk=s[a:b]
w=blk
w=rep1(w, 'captions: caps("wait", [0, 4]),', 'captions: caps("wait", [3]),')
w=rep1(w, 'ui: [{ type: "counter", t: vo("wait", 0) - 0.1, end: vo("wait", 1) + 1.2, label: "ผ่านไปแล้ว", icon: "clock", unit: "นาที", keys: [{ t: vo("wait", 0), v: 0 }, { t: vo("wait", 0) + 1.9, v: 20 }], right: true, top: 150 }],',
            'ui: [{ type: "counter", t: 0.1, end: vo("wait", 0) + 1.2, label: "ผ่านไปแล้ว", icon: "clock", unit: "นาที", keys: [{ t: 0.15, v: 0 }, { t: 1.35, v: 20 }], right: true, top: 150 }],')
w=rep1(w, 'bubbles: [bub("wait", 1, 440, 520, 440, { br: true }), bub("wait", 2, 780, 540, 780), bub("wait", 3, 450, 560, 450)],', 'bubbles: [bub("wait", 0, 440, 520, 440, { br: true }), bub("wait", 1, 780, 540, 780), bub("wait", 2, 450, 560, 450)],')
for k in (1,2,3,4): w=w.replace(f'vo("wait", {k})', f'vo("wait", {k-1})')
assert 'vo("wait", 4)' not in w
s=s[:a]+w+s[b:]
# night: squeezed to 7.6 s
s=rep1(s, 'keys: [{ t: 0.2, v: 14 }, { t: 1.3, v: 9 }, { t: 2.0, v: 0 }, { t: 3.3, v: 0 }, { t: 3.7, v: 6 }, { t: 5.8, v: 6 }, { t: 6.5, v: 0 }, { t: 7.6, v: 5 }], alarm: 2.0,', 'keys: [{ t: 0.2, v: 14 }, { t: 1.2, v: 9 }, { t: 1.9, v: 0 }, { t: 3.0, v: 0 }, { t: 3.4, v: 6 }, { t: 5.3, v: 6 }, { t: 6.0, v: 0 }, { t: 7.0, v: 5 }], alarm: 1.9,')
s=rep1(s, '{ t: 2.1, mode: "breathe", eyes: "closed", mouth: "o", opts: { period: 1.5, n: 2, t0: 0 } }, { t: 3.9, mode: "compress", eyes: "worry", mouth: "grit", opts: { period: 0.5, n: 6, t0: 0 } }, { t: 5.8, mode: "kneelWatch", eyes: "worry", mouth: "flat" }, { t: 6.7, mode: "breathe"', '{ t: 2.0, mode: "breathe", eyes: "closed", mouth: "o", opts: { period: 1.5, n: 2, t0: 0 } }, { t: 3.6, mode: "compress", eyes: "worry", mouth: "grit", opts: { period: 0.5, n: 6, t0: 0 } }, { t: 5.3, mode: "kneelWatch", eyes: "worry", mouth: "flat" }, { t: 6.1, mode: "breathe"')
s=rep1(s, 'red(tl, t0 + 2.0, 0.4, 0.8); red(tl, t0 + 6.5, 0.35, 0.8);', 'red(tl, t0 + 1.9, 0.4, 0.8); red(tl, t0 + 6.0, 0.35, 0.8);')
s=rep1(s, '{ t: 2.0, glide: 1.2, ...fr(380, 1560, 1.9, 540, 1000), drift: { s: 0.02 } }, { t: 5.8, ...fr(520, 1380, 1.0, 540, 940)', '{ t: 2.0, glide: 1.2, ...fr(380, 1560, 1.9, 540, 1000), drift: { s: 0.02 } }, { t: 5.3, ...fr(520, 1380, 1.0, 540, 940)')
# fish#1: she quotes the rule, not smiling at a photo
s=rep1(s, 'PW(760, 1680, 0.82, [{ t: 0, mode: "point", eyes: "squint", mouth: "flat" }', 'PW(760, 1680, 0.82, [{ t: 0, mode: "point", eyes: "squint", mouth: "flat" }')
wr(p, s)
# ---- mix cues
p=f"{W}/isle1/mix.py"; s=rd(p)
s=rep1(s, 'FSH = vo_t("fish", 2) - 0.15; FS3 = vo_t("fish", 3) - 0.15', 'FSH = vo_t("fish", 2) - 0.15')
s=rep1(s, '("fish", FSH + vo_t("fish", 2) - FSH + 0.9, "shutter", 0.45), ("fish", FS3 + 0.1, "whoosh", 0.3), ("fish", vo_t("fish", 4), "sting", 0.4), *beats("fish", vo_t("fish", 3), D["fish"] - vo_t("fish", 3), 0.7, 0.4),',
            '("fish", FSH + 0.1, "whoosh", 0.3), ("fish", vo_t("fish", 3), "sting", 0.4), *beats("fish", vo_t("fish", 2), D["fish"] - vo_t("fish", 2), 0.7, 0.4),')
s=rep1(s, '*[("wait", vo_t("wait", 0) + 0.1 + k * 0.19, "tick", 0.35) for k in range(10)], ("wait", vo_t("wait", 0) + 2.0, "ding", 0.3),', '*[("wait", 0.15 + k * 0.12, "tick", 0.35) for k in range(10)], ("wait", 1.4, "ding", 0.3),')
s=rep1(s, '("wait", vo_t("wait", 1) - 0.2, "sting", 0.35), ("wait", vo_t("wait", 3) + 0.6, "thud", 0.6), ("wait", vo_t("wait", 3) + 0.62, "rustle", 0.3),', '("wait", vo_t("wait", 0) - 0.2, "sting", 0.35), ("wait", vo_t("wait", 2) + 0.6, "thud", 0.6), ("wait", vo_t("wait", 2) + 0.62, "rustle", 0.3),')
s=rep1(s, '("wait", vo_t("wait", 4), "riser", 0.5), ("wait", frag("wait", 4, 4), "sting", 0.9), ("wait", frag("wait", 4, 4), "boom", 0.5),', '("wait", vo_t("wait", 3), "riser", 0.5), ("wait", frag("wait", 3, 4), "sting", 0.9), ("wait", frag("wait", 3, 4), "boom", 0.5),')
s=rep1(s, '*beats("wait", 0.0, vo_t("wait", 1), 0.9, 0.3), *beats("wait", vo_t("wait", 1), D["wait"] - vo_t("wait", 1), 0.55, 0.7),', '*beats("wait", 0.0, vo_t("wait", 0), 0.9, 0.3), *beats("wait", vo_t("wait", 0), D["wait"] - vo_t("wait", 0), 0.55, 0.7),')
s=rep1(s, 'dip(T("wait", vo_t("wait", 3) - 0.2), T("wait", -0.05), 0.25)', 'dip(T("wait", vo_t("wait", 2) - 0.2), T("wait", -0.05), 0.25)')
s=rep1(s, '("night", 2.0, "sting", 0.7), ("night", 2.0, "boom", 0.4), ("night", 2.2, "breath", 0.9), ("night", 3.6, "breath", 0.9), *[("night", 4.0 + k * 0.5, "thud", 0.5) for k in range(5)],', '("night", 1.9, "sting", 0.7), ("night", 1.9, "boom", 0.4), ("night", 2.1, "breath", 0.9), ("night", 3.3, "breath", 0.9), *[("night", 3.7 + k * 0.45, "thud", 0.5) for k in range(5)],')
s=rep1(s, '("night", 6.5, "sting", 0.6), ("night", 6.8, "breath", 0.9), ("night", 7.7, "gasp", 0.5),', '("night", 6.0, "sting", 0.6), ("night", 6.3, "breath", 0.9), ("night", 7.1, "gasp", 0.5),')
assert 'vo_t("wait", 4)' not in s and 'FS3' not in s and 'vo_t("fish", 4)' not in s
wr(p, s); print("tightened")
