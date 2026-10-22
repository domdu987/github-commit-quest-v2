"""Assemble EP.1 scenes 4-16 into the HyperFrames composition.

Reads the hand-built intro (S1-S3) from intro.html, adds character defs from
kdefs.svg, writes ../hf/quest/index.html. Timing comes from TIMES below, which
match the narration schedule used by mix.sh.
"""
import re

ROOT = "/tmp/claude-0/-home-user-github-commit-quest-v2/4f94749f-8122-57a4-aa41-e38e84dcb96c/scratchpad"
intro = open(f"{ROOT}/build/intro.html").read()
kdefs = open(f"{ROOT}/build/kdefs.svg").read()

# scene id -> (start, end)
TIMES = {
    "s4": (19.6, 26.85), "s5": (26.85, 35.2), "s6": (35.2, 41.6), "s7": (41.6, 47.9),
    "s8": (47.9, 52.4), "s9": (52.4, 55.4), "s10": (55.4, 62.85), "s11": (62.85, 76.0),
    "s12": (76.0, 85.4), "s13": (85.4, 92.9), "s14": (92.9, 98.4), "s15": (98.4, 102.6),
    "s16": (102.6, 108.0),
}
TOTAL = 108.0

INK, CREAM, TERRA, NIGHT, WARM = "#2e2a26", "#f4ecd8", "#e07a4f", "#2b4350", "#f2d6a0"

# ---------------- faces (character-local coords) ----------------
FACE = {
    "pe-n": '<path class="l" d="M68,86Q78,83 90,80M110,80Q122,83 132,86"/><ellipse cx="81" cy="105" rx="5" ry="6.5" fill="#2e2a26"/><ellipse cx="123" cy="105" rx="5" ry="6.5" fill="#2e2a26"/><circle cx="79.5" cy="103" r="1.8" fill="#f4ecd8"/><circle cx="121.5" cy="103" r="1.8" fill="#f4ecd8"/>',
    "pe-s": '<path class="l" d="M66,84Q78,76 90,81M110,81Q122,76 134,84"/><circle cx="79" cy="105" r="9" fill="#f4ecd8" class="o3"/><circle cx="121" cy="105" r="9" fill="#f4ecd8" class="o3"/><circle cx="79" cy="105" r="2.4" fill="#2e2a26"/><circle cx="121" cy="105" r="2.4" fill="#2e2a26"/>',
    "pe-r": '<path class="l" d="M68,86Q79,81 90,85M110,85Q121,81 132,86"/><path class="l" style="stroke-width:3.5" d="M70,104Q79,112 88,104M112,104Q121,112 130,104"/>',
    "pe-w": '<path class="l" d="M68,90Q78,86 90,88M110,88Q122,86 132,90"/><path class="l" style="stroke-width:3.5" d="M72,106h16M112,106h16"/>',
    "pm-n": '<path class="l" d="M92,138q4-4 8,0t8,0"/>',
    "pm-s": '<path d="M91,134C91,124 109,124 109,134C109,148 91,148 91,134Z" fill="#2e2a26"/><path d="M95,142Q100,137 105,142Q100,146 95,142Z" fill="#e07a4f"/>',
    "pm-r": '<path d="M90,133Q100,145 110,133Z" fill="#c8664a" class="o3"/>',
    "pm-f": '<path class="l" d="M93,138h14"/>',
    "fe-n": '<path class="l l4" d="M68,88L91,93M109,93L132,88"/><ellipse cx="79" cy="109" rx="7" ry="9" fill="#2e2a26"/><ellipse cx="119" cy="109" rx="7" ry="9" fill="#2e2a26"/><circle cx="76.5" cy="105.5" r="2.6" fill="#f4ecd8"/><circle cx="116.5" cy="105.5" r="2.6" fill="#f4ecd8"/><path class="l l4" d="M69,100Q80,96 91,100M109,100Q120,96 131,100"/>',
    "fe-d": '<path class="l" style="stroke-width:5" d="M67,88L91,94M109,94L133,88"/><ellipse cx="81" cy="110" rx="6.5" ry="7.5" fill="#2e2a26"/><ellipse cx="119" cy="110" rx="6.5" ry="7.5" fill="#2e2a26"/><circle cx="79" cy="107.5" r="2.2" fill="#f4ecd8"/><circle cx="117" cy="107.5" r="2.2" fill="#f4ecd8"/><path class="l l4" d="M69,101L92,103M108,103L131,101"/>',
    "fe-s": '<path class="l" d="M68,92Q78,86 90,83M110,83Q122,86 132,92"/><ellipse cx="80" cy="108" rx="9" ry="10.5" fill="#f4ecd8" class="o3"/><ellipse cx="120" cy="108" rx="9" ry="10.5" fill="#f4ecd8" class="o3"/><circle cx="80" cy="109" r="3.2" fill="#2e2a26"/><circle cx="120" cy="109" r="3.2" fill="#2e2a26"/>',
    "fe-z": '<path class="l l4" d="M68,92L91,94M109,94L132,92"/><path class="l" style="stroke-width:3.5" d="M71,110Q80,116 89,110M111,110Q120,116 129,110"/>',
    "fm-n": '<path class="l" d="M92,135Q101,141 109,133"/>',
    "fm-d": '<path d="M88,132Q100,136 112,131Q110,144 100,145Q90,144 88,132Z" fill="#f4ecd8" class="o3"/><path class="l l2" d="M89,137Q100,140 111,136"/>',
    "fm-s": '<path class="l" d="M88,138q3-5 6,0t6,0t6,0t6,0"/>',
    "fm-o": '<ellipse cx="100" cy="138" rx="8" ry="10" fill="#2e2a26"/>',
    "ce-n": '<circle cx="61" cy="70" r="12" fill="#b9cf98" class="o3"/><circle cx="99" cy="70" r="12" fill="#b9cf98" class="o3"/><ellipse cx="62" cy="68" rx="6" ry="9" fill="#2e2a26"/><ellipse cx="100" cy="68" rx="6" ry="9" fill="#2e2a26"/><circle cx="59" cy="64" r="3" fill="#f4ecd8"/><circle cx="97" cy="64" r="3" fill="#f4ecd8"/>',
    "ce-a": '<circle cx="61" cy="70" r="13" fill="#b9cf98" class="o3"/><circle cx="99" cy="70" r="13" fill="#b9cf98" class="o3"/><ellipse cx="61" cy="70" rx="3" ry="9" fill="#2e2a26"/><ellipse cx="99" cy="70" rx="3" ry="9" fill="#2e2a26"/><circle cx="57" cy="65" r="2.6" fill="#f4ecd8"/><circle cx="95" cy="65" r="2.6" fill="#f4ecd8"/>',
    "ce-z": '<path class="l" style="stroke-width:3.5" d="M50,72q11,8 22,0M88,72q11,8 22,0"/>',
    "cm-n": '<path class="l l2" d="M73,98q3.5,4 7,0q3.5,4 7,0"/>',
    "cm-a": '<path d="M75,97Q80,105 85,97Z" fill="#c8664a" class="o3" style="stroke-width:2"/>',
}

def arm(path, sleeve, hands=()):
    s = f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="{path}" fill="none" stroke="{sleeve}" stroke-width="22" stroke-linecap="round"/>'
    for hx, hy in hands:
        s += f'<circle cx="{hx}" cy="{hy}" r="11" fill="#f1cfaa" class="o3"/>'
    return s

ARMS = {
    "p-down": '<use href="#k-phum-arms0"/>',
    "p-cup": arm("M60,188Q50,232 78,262M140,188Q150,232 122,262", "#b9cdd3", [(80, 262), (120, 262)]) +
             '<path d="M74,232h52l-6,40h-40z" fill="#f4ecd8" class="o3"/><path d="M76,244h48" stroke="#e07a4f" stroke-width="7"/><path d="M90,226q6-14 0-24M108,226q6-14 0-24" class="l l2" opacity=".6"/>',
    "p-clip": arm("M60,188Q44,232 52,262M140,188Q160,228 146,250", "#b9cdd3", [(54, 262), (146, 254)]) +
              '<g transform="rotate(12 150 238)"><rect x="128" y="208" width="42" height="56" rx="4" fill="#b98d62" class="o3"/><rect x="133" y="216" width="32" height="44" fill="#f4ecd8"/><path class="l l2" d="M137,226h22M137,238h22M137,250h12"/></g>',
    "p-write": arm("M60,188Q62,240 96,256M140,188Q150,236 118,262", "#b9cdd3", [(98, 256), (118, 262)]) +
               '<rect x="66" y="246" width="70" height="44" rx="3" fill="#f4ecd8" class="o3" transform="rotate(-6 100 268)"/><path class="l l2" d="M76,258h40M76,268h46M76,278h30" transform="rotate(-6 100 268)"/>',
    "p-reach": arm("M60,188Q44,232 46,262M140,188Q186,190 214,170", "#b9cdd3", [(46, 262), (216, 168)]),
    "f-down": '<use href="#k-fon-arms0"/>',
    "f-torch": arm("M62,188Q36,192 22,156M140,188Q170,226 152,262", "#e2b65a", [(18, 148), (150, 266)]) +
               '<rect x="-6" y="114" width="17" height="30" rx="3" transform="rotate(-18 2 129)" fill="#3d3833" class="o3"/><circle cx="-1" cy="120" r="3.5" fill="#fbeecb"/>',
    "f-point": arm("M62,188Q40,236 50,262M140,188Q186,182 222,160", "#e2b65a", [(50, 264), (224, 158)]),
    "f-lap": arm("M62,188Q56,238 90,262M140,188Q146,238 112,262", "#e2b65a", [(92, 262), (110, 262)]),
    "f-slam": arm("M62,188Q40,236 50,262M140,188Q190,160 230,170", "#e2b65a", [(50, 264), (234, 170)]),
}

def char(who, x, y, s=1.0, eyes=None, mouth=None, arms=None, extra="", cid=None, flip=False):
    base = {"p": "#k-phum", "f": "#k-fon", "c": "#k-cat"}[who]
    eyes = eyes or {"p": "pe-n", "f": "fe-n", "c": "ce-n"}[who]
    mouth = mouth or {"p": "pm-n", "f": "fm-n", "c": "cm-n"}[who]
    arms = "" if who == "c" else ARMS[arms or ("p-down" if who == "p" else "f-down")]
    sx = -s if flip else s
    ox = 200 * s if flip else 0
    idattr = f' id="{cid}"' if cid else ""
    return (f'<g{idattr}><g transform="translate({x + ox},{y}) scale({sx},{s})"><g filter="url(#k-rough)">'
            f'<use href="{base}"/>{arms}<g class="eyes">{FACE[eyes]}</g><g class="mouth">{FACE[mouth]}</g>{extra}</g></g></g>')

def shadow(cx, cy, rx):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.13:.0f}" fill="#16232a" opacity=".45"/>'

def cap(sid, lines, top=1640):
    boxes = "".join(f'<div id="{sid}c{i}" class="box">{t}</div>' for i, t in enumerate(lines))
    return f'<div class="cap" style="top:{top}px">{boxes}</div>'

def card(cid, html, left, top, w=None, rot=-2, extra_style=""):
    ws = f"width:{w}px;" if w else ""
    return f'<div id="{cid}" class="hud tape a" style="left:{left}px; top:{top}px; {ws} padding:20px 26px 22px; transform:rotate({rot}deg); {extra_style}">{html}</div>'

def rule(cid, n, title, sub, src, left=90, top=170):
    return card(cid, f'<div style="display:flex;align-items:center;gap:16px"><div class="stk" style="width:92px;height:92px;font-size:46px;outline-offset:-10px">{n}</div>'
                     f'<div><div style="font:700 28px/1 Kanit;letter-spacing:4px">กฎข้อ {n}</div><div style="font:900 60px/1.15 Kanit">{title}</div></div>'
                     f'<div class="srcst">{src}</div></div><div style="font:700 34px/1.3 Kanit;margin-top:8px;color:#5b4f45">{sub}</div>', left, top, w=900, rot=-1.5)

def bubble(bid, text, left, top, tail="left"):
    tl = "40px" if tail == "left" else "auto"
    tr = "auto" if tail == "left" else "40px"
    return (f'<div id="{bid}" class="bub a" style="left:{left}px; top:{top}px">{text}'
            f'<i style="left:{tl}; right:{tr}"></i></div>')

def sfx(xid, text, left, top, rot=-6, size=120, color=TERRA):
    return f'<div id="{xid}" class="a sfx" style="left:{left}px; top:{top}px; font-size:{size}px; color:{color}; transform:rotate({rot}deg)">{text}</div>'

def scene(sid, inner_svg, html="", bg=NIGHT):
    st, en = TIMES[sid]
    return (f'<div id="{sid}" class="clip" data-start="{st}" data-duration="{en - st:.2f}" data-track-index="0" style="background:{bg}">'
            f'<svg id="{sid}v" class="a" width="1080" height="1920" viewBox="0 0 1080 1920">{inner_svg}</svg>{html}</div>')

DARKROOM = f'<rect width="1080" height="1920" fill="#253a44"/><rect width="1080" height="1920" fill="url(#k-ht)" opacity=".18"/>'
FLOOR = '<rect y="1380" width="1080" height="540" fill="#1f3039" class="o"/><path d="M0,1380H1080" stroke="#2e2a26" stroke-width="6"/>'

def window(x, y, w, h):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1c2c34" class="o"/>'
    bx = x + 20
    i = 0
    while bx < x + w - 60:
        bh = 120 + (i * 53) % 170
        s += f'<rect x="{bx}" y="{y + h - bh}" width="{60 + (i * 17) % 40}" height="{bh}" fill="#2b4350" stroke="#2e2a26" stroke-width="3"/>'
        bx += 70 + (i * 23) % 30
        i += 1
    s += f'<circle cx="{x + w - 90}" cy="{y + 90}" r="34" fill="#f4ecd8" class="o3"/>'
    s += f'<path d="M{x + w / 2},{y}V{y + h}M{x},{y + h * 0.45}H{x + w}" stroke="#2e2a26" stroke-width="10"/>'
    return s

def door(x, y, num, w=230, h=500, lit=False, open_=False, did=None):
    idattr = f' id="{did}"' if did else ""
    s = f'<rect x="{x - 14}" y="{y - 14}" width="{w + 28}" height="{h + 14}" fill="#1c2c34" class="o"/>'
    if lit:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f2d6a0"/>'
    s += f'<g{idattr}><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#3c5763" class="o"/><circle cx="{x + w - 34}" cy="{y + h / 2 + 20}" r="11" fill="#c9b98f" class="o3"/></g>'
    s += f'<rect x="{x + w / 2 - 50}" y="{y - 64}" width="100" height="40" rx="4" fill="#e6d9bd" class="o3"/><text x="{x + w / 2}" y="{y - 33}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="28" fill="#2e2a26">{num}</text>'
    return s

scenes, js = [], []
J = js.append

def capjs(sid, times):
    for i, (t0, t1) in enumerate(times):
        J(f'capIn("#{sid}c{i}", {t0}, {t1 if t1 else "null"});')

# ---------------- S4: Phum in room 2714 ----------------
st = TIMES["s4"][0]
s4 = DARKROOM + window(560, 220, 440, 620) + FLOOR
s4 += '<g id="s4mw"><rect x="80" y="760" width="300" height="190" rx="12" fill="#9fb3b8" class="o"/><rect x="104" y="790" width="190" height="130" fill="#1c2c34" class="o3"/><circle cx="330" cy="820" r="12" fill="#2e2a26"/><circle cx="330" cy="870" r="12" fill="#2e2a26"/><rect x="60" y="950" width="400" height="430" fill="#3c5763" class="o"/></g>'
s4 += shadow(560, 1700, 230) + char("p", 390, 1010, 1.6, "pe-s", "pm-s", "p-cup", cid="s4p")
s4 += shadow(900, 1690, 110) + char("c", 780, 1440, 1.45, "ce-a", "cm-a", cid="s4c")
h4 = card("s4n", '<div style="display:flex;gap:16px;align-items:center"><div style="width:64px;height:64px;border-radius:14px;background:#e07a4f;border:4px solid #2e2a26;display:grid;place-items:center;font:900 40px/1 Kanit;color:#2e2a26">!</div><div><div style="font:700 28px/1.2 Kanit;color:#b0553a">แจ้งเตือนฉุกเฉิน · ตอนนี้</div><div style="font:900 40px/1.2 Kanit">ไฟดับทั่วกรุงเทพฯ ยังไม่มีกำหนดกลับมา</div></div></div>', 60, 110, w=960, rot=-1)
h4 += sfx("s4x", "ปิ๊บ!", 150, 640, -10, 100, WARM)
h4 += cap("s4", ["ภูมิ · <span class=\"k\">ห้อง 2714</span>", "วางแผนทุกอย่าง <span class=\"k\">ยกเว้นคืนนี้</span>"])
scenes.append(scene("s4", s4, h4))
J(f'tl.fromTo("#s4v", {{scale:1.08, transformOrigin:"540px 1100px"}}, {{scale:1, duration:7.2, ease:"power1.out"}}, {st});')
J(f'tl.fromTo("#s4mw", {{x:-30}}, {{x:0, duration:0.4, ease:"back.out(2)"}}, {st});')
J(f'tl.fromTo("#s4x", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.25, ease:"back.out(3)"}}, {st + 0.1});')
J(f'tl.to("#s4x", {{opacity:0, duration:0.3}}, {st + 1.6});')
J(f'tl.fromTo("#s4n", {{y:-260}}, {{y:0, duration:0.45, ease:"back.out(1.6)"}}, {st + 0.9});')
J(f'tl.fromTo("#s4p", {{y:"+=0"}}, {{y:"-=10", duration:0.6, repeat:9, yoyo:true, ease:"sine.inOut"}}, {st});')
J(f'tl.fromTo("#s4c", {{rotation:0}}, {{rotation:-4, transformOrigin:"50% 100%", duration:0.4, repeat:13, yoyo:true, ease:"sine.inOut"}}, {st});')
capjs("s4", [(st + 0.2, st + 3.6), (st + 3.7, None)])

# ---------------- S5: corridor, Fon appears ----------------
st = TIMES["s5"][0]
s5 = '<rect width="1080" height="1920" fill="#2b4350"/><path d="M0,0L330,520H750L1080,0Z" fill="#22363f" class="o"/><path d="M0,1920L330,1150H750L1080,1920Z" fill="#1f3039" class="o"/>'
s5 += '<rect x="330" y="520" width="420" height="630" fill="#182830" class="o"/><rect x="455" y="610" width="170" height="70" rx="8" fill="#5a9573" class="o3"/><text x="540" y="658" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="36" fill="#f4ecd8">EXIT →</text>'
s5 += '<ellipse cx="540" cy="650" rx="190" ry="110" fill="#5a9573" opacity=".18"/>'
s5 += door(40, 760, "2714", w=220, h=720) + f'<g id="s5door">{door(820, 760, "2715", w=220, h=720, lit=True, did="s5d")}</g>'
s5 += '<path id="s5beam" d="M760,1010L330,880L330,1240Z" fill="#f2d6a0" opacity=".35"/>'
s5 += shadow(300, 1790, 200) + char("p", 140, 1150, 1.45, "pe-s", "pm-s", "p-down", cid="s5p")
s5 += shadow(800, 1790, 200) + char("f", 640, 1150, 1.45, "fe-d", "fm-n", "f-torch", cid="s5f", flip=True)
h5 = sfx("s5x", "แกร๊ก", 700, 420, 8, 110, WARM)
h5 += bubble("s5b", "“ห้องคุณ… <span class=\"k\">น้ำยังไหลไหม?</span>”", 380, 860, tail="right")
h5 += cap("s5", ["ฝน · <span class=\"k\">ห้อง 2715</span>", "เพื่อนบ้านที่<span class=\"k\">ไม่เคยทัก</span>กัน"])
scenes.append(scene("s5", s5, h5))
J(f'tl.fromTo("#s5d", {{scaleX:1}}, {{scaleX:0.25, transformOrigin:"100% 50%", duration:0.5, ease:"power2.out"}}, {st + 0.4});')
J(f'tl.fromTo("#s5x", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.2, ease:"back.out(3)"}}, {st + 0.4});')
J(f'tl.to("#s5x", {{opacity:0, duration:0.3}}, {st + 1.8});')
J(f'tl.fromTo("#s5f", {{x:220, opacity:0}}, {{x:0, opacity:1, duration:0.6, ease:"power2.out"}}, {st + 0.8});')
J(f'tl.fromTo("#s5beam", {{opacity:0}}, {{opacity:.35, duration:0.3}}, {st + 1.3});')
J(f'tl.fromTo("#s5beam", {{skewY:0}}, {{skewY:2, transformOrigin:"760px 1010px", duration:0.8, repeat:7, yoyo:true, ease:"sine.inOut"}}, {st + 1.6});')
J(f'tl.fromTo("#s5b", {{scale:0, opacity:0, transformOrigin:"80% 100%"}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(2.5)"}}, {st + 6.1});')
capjs("s5", [(st + 0.2, st + 2.9), (st + 3.0, st + 6.0)])

# ---------------- S6: building cutaway ----------------
st = TIMES["s6"][0]
s6 = f'<rect width="1080" height="1920" fill="#e6d9bd"/><rect width="1080" height="1920" fill="url(#k-htc)" opacity=".0"/>'
s6 += '<rect x="290" y="300" width="500" height="1240" fill="#f4ecd8" class="o"/>'
for f in range(10):
    y = 420 + f * 108
    s6 += f'<path d="M290,{y}H790" stroke="#2e2a26" stroke-width="3" opacity=".5"/><rect x="330" y="{y + 30}" width="60" height="50" fill="#c9d6d9" class="o3"/><rect x="690" y="{y + 30}" width="60" height="50" fill="#c9d6d9" class="o3"/>'
s6 += '<g id="s6roof"><rect x="420" y="190" width="240" height="130" rx="10" fill="#9fb3b8" class="o"/><rect id="s6lvl" x="432" y="236" width="216" height="72" fill="#8fb0b8"/><text x="540" y="180" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#2e2a26">ถังดาดฟ้า</text></g>'
s6 += '<rect x="400" y="1560" width="280" height="150" rx="10" fill="#9fb3b8" class="o"/><rect x="412" y="1600" width="256" height="98" fill="#8fb0b8"/><text x="540" y="1770" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#2e2a26">ถังชั้นล่าง</text>'
s6 += '<path d="M680,1620H860V250H660" fill="none" stroke="#2e2a26" stroke-width="30" stroke-linejoin="round"/><path id="s6pipe" d="M680,1620H860V250H660" fill="none" stroke="#8fb0b8" stroke-width="18" stroke-linejoin="round" stroke-dasharray="40 30"/>'
s6 += '<g id="s6pump"><circle cx="860" cy="1440" r="70" fill="#e07a4f" class="o"/><text x="860" y="1456" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#2e2a26">ปั๊ม</text></g>'
s6 += '<g id="s6off" opacity="0"><path d="M800,1380l120,120M920,1380l-120,120" stroke="#b0553a" stroke-width="18" stroke-linecap="round"/><rect x="930" y="1500" width="120" height="60" rx="6" fill="#b0553a" class="o3"/><text x="990" y="1543" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="36" fill="#f4ecd8">OFF</text></g>'
s6 += '<g id="s6arr">' + "".join(f'<path d="M230,{460 + i * 220}v110m-26,-30 26,30 26,-30" fill="none" stroke="#5a7f8a" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>' for i in range(5)) + '</g>'
h6 = cap("s6", ["ไฟดับ = <span class=\"k\">ปั๊มหยุด</span>", "เหลือแค่น้ำใน<span class=\"k\">ถังดาดฟ้า</span>"], top=40)
scenes.append(scene("s6", s6, h6, bg="#e6d9bd"))
J(f'tl.fromTo("#s6pipe", {{strokeDashoffset:0}}, {{strokeDashoffset:-280, duration:1.6, ease:"none"}}, {st});')
J(f'tl.fromTo("#s6off", {{opacity:0, scale:2, transformOrigin:"860px 1440px"}}, {{opacity:1, scale:1, duration:0.2, ease:"power4.in"}}, {st + 1.6});')
J(f'tl.fromTo("#s6pump", {{x:0}}, {{x:6, duration:0.05, repeat:5, yoyo:true}}, {st + 1.8});')
J(f'tl.to("#s6pipe", {{stroke:"#c9b98f", duration:0.3}}, {st + 1.8});')
J(f'tl.fromTo("#s6arr", {{y:-20, opacity:0}}, {{y:20, opacity:1, duration:1, repeat:3, yoyo:true, ease:"sine.inOut"}}, {st + 3.0});')
J(f'tl.fromTo("#s6lvl", {{scaleY:1}}, {{scaleY:0.45, transformOrigin:"50% 100%", duration:3.2, ease:"none"}}, {st + 3.0});')
capjs("s6", [(st + 0.2, st + 2.9), (st + 3.0, None)])

# ---------------- S7: rule 1 - fill water now ----------------
st = TIMES["s7"][0]
s7 = '<rect width="1080" height="1920" fill="#3c5763"/><rect width="1080" height="1920" fill="url(#k-ht)" opacity=".15"/>'
s7 += '<path d="M120,1200H960V1540Q960,1640 860,1640H220Q120,1640 120,1540Z" fill="#f4ecd8" class="o"/><path d="M160,1240H920V1520Q920,1590 850,1590H230Q160,1590 160,1520Z" fill="#c9d6d9" class="o3"/>'
s7 += '<rect id="s7w" x="164" y="1300" width="752" height="286" fill="#8fb0b8" opacity=".9"/>'
s7 += '<rect x="780" y="1060" width="70" height="140" fill="#9fb3b8" class="o"/><path d="M700,1080H850" stroke="#2e2a26" stroke-width="34" stroke-linecap="round"/><path d="M700,1080H850" stroke="#b9cdd3" stroke-width="24" stroke-linecap="round"/>'
s7 += '<path id="s7s" d="M712,1100V1300" stroke="#cfe2e6" stroke-width="22" stroke-linecap="round" stroke-dasharray="30 18"/>'
s7 += shadow(130, 1530, 140) + char("f", -20, 1000, 1.2, "fe-d", "fm-d", "f-point", cid="s7f")
h7 = rule("s7r", 1, "รองน้ำทันที", "≈ 3.8 ลิตร / คน / วัน (ดื่ม + ใช้)", "FEMA")
h7 += sfx("s7x", "ซ่าาา", 760, 900, -4, 96, WARM)
h7 += cap("s7", ["<span class=\"k\">รองน้ำ</span> ก่อนทั้งตึกเปิดก๊อก", "≈ <span class=\"k\">3.8 ลิตร</span> / คน / วัน"])
scenes.append(scene("s7", s7, h7))
J(f'tl.fromTo("#s7r", {{y:-400, rotation:-8}}, {{y:0, rotation:-1.5, duration:0.45, ease:"back.out(1.5)"}}, {st + 0.1});')
J(f'tl.fromTo("#s7w", {{scaleY:0.15}}, {{scaleY:1, transformOrigin:"50% 100%", duration:6, ease:"power1.out"}}, {st + 0.3});')
J(f'tl.fromTo("#s7s", {{strokeDashoffset:0}}, {{strokeDashoffset:-240, duration:1, repeat:5, ease:"none"}}, {st + 0.3});')
J(f'tl.fromTo("#s7x", {{scale:0}}, {{scale:1, duration:0.25, ease:"back.out(3)"}}, {st + 0.5});')
capjs("s7", [(st + 0.3, st + 3.1), (st + 3.2, None)])

# ---------------- S8: containers montage + toilet note ----------------
st = TIMES["s8"][0]
s8 = '<rect width="1080" height="1920" fill="#e6d9bd"/>' + '<rect y="1300" width="1080" height="620" fill="#cdbd98" class="o"/>'
cont = ''
for i, (x, w, h, col) in enumerate([(70, 120, 260, "#cfe2e6"), (220, 150, 200, "#9fb3b8"), (400, 200, 300, "#e07a4f"), (630, 130, 240, "#cfe2e6"), (790, 210, 180, "#8ea3a9")]):
    cont += f'<g class="s8c"><rect x="{x}" y="{1300 - h}" width="{w}" height="{h}" rx="14" fill="{col}" class="o"/><rect x="{x + 10}" y="{1300 - h * 0.7}" width="{w - 20}" height="{h * 0.62}" fill="#8fb0b8" opacity=".75"/></g>'
s8 += cont + shadow(960, 1450, 90) + char("c", 860, 1260, 1.1, "ce-n", "cm-n", cid="s8c")
s8 += shadow(240, 1880, 170) + char("p", 100, 1330, 1.25, "pe-n", "pm-n", "p-clip", cid="s8p")
h8 = card("s8m", '<div style="font:700 30px/1 Kanit;letter-spacing:3px">คลังน้ำ · ห้อง 2714</div><div style="font:900 64px/1.2 Kanit;margin-top:8px">2 คน × 3 วัน × 3.8 ล.</div><div style="font:900 84px/1.1 Kanit;color:#b0553a">≈ 23 ลิตร</div>', 140, 260, w=800, rot=-2)
h8 += card("s8t", '<div style="font:900 56px/1.2 Kanit">น้ำในอ่าง = <span style="color:#b0553a">ราดชักโครก</span></div><div style="font:700 36px/1.3 Kanit">ไม่ใช่ไว้ดื่ม · กดเต็ม 1 ครั้ง ≈ 6 ลิตร</div>', 120, 300, w=840, rot=2)
h8 += cap("s8", ["สองคน สามวัน ≈ <span class=\"k\">23 ลิตร</span>", "น้ำในอ่างไว้<span class=\"k\">ราดชักโครก</span>"], top=1700)
scenes.append(scene("s8", s8, h8, bg="#e6d9bd"))
J(f'tl.fromTo(".s8c", {{y:500}}, {{y:0, duration:0.35, stagger:0.12, ease:"back.out(1.6)"}}, {st});')
J(f'tl.fromTo("#s8m", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(2)"}}, {st + 0.4});')
J(f'tl.to("#s8m", {{x:-1100, duration:0.3, ease:"power2.in"}}, {st + 2.2});')
J(f'tl.fromTo("#s8t", {{x:1100}}, {{x:0, duration:0.35, ease:"back.out(1.4)"}}, {st + 2.3});')
capjs("s8", [(st + 0.3, st + 2.2), (st + 2.3, None)])

# ---------------- S9: tap stops ----------------
st = TIMES["s9"][0]
s9 = '<use href="#bathbase"/>'
h9 = card("s9k", '<div style="font:700 30px/1 Kanit;letter-spacing:3px">ไฟดับมาแล้ว</div><div style="font:900 84px/1.1 Orbitron, Kanit">00:49</div>', 640, 160, w=360, rot=3)
h9 += sfx("s9x", "โครก… โครก…", 380, 840, 6, 92, WARM)
h9 += cap("s9", ["20:31 น. · ก๊อกน้ำ… <span class=\"k\">หยุดไหล</span>"])
_intro = open(f"{ROOT}/build/intro.html").read()
_bath = re.search(r'<svg id="bath"[^>]*>(.*?)</svg>', _intro, re.S).group(1)
for _i in sorted(set(re.findall(r'id="([a-zA-Z0-9-]+)"', _bath)), key=len, reverse=True):
    _bath = re.sub(r'id="%s"' % _i, 'id="s9%s"' % _i, _bath)
    _bath = re.sub(r'url\(#%s\)' % _i, 'url(#s9%s)' % _i, _bath)
scenes.append(scene("s9", _bath, h9))
J(f'tl.fromTo("#s9k", {{y:-300}}, {{y:0, duration:0.4, ease:"back.out(1.6)"}}, {st + 0.2});')
J(f'tl.fromTo("#s9x", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.2, ease:"back.out(3)", repeat:1, yoyo:true, repeatDelay:0.8}}, {st + 0.5});')
J(f'tl.fromTo("#s9dropg", {{y:0, opacity:1}}, {{y:470, duration:0.35, ease:"power2.in"}}, {st + 2.2});')
J(f'tl.set("#s9dropg", {{opacity:0}}, {st + 2.56});')
capjs("s9", [(st + 0.3, None)])

# ---------------- S10: fridge rule 2 ----------------
st = TIMES["s10"][0]
s10 = DARKROOM + FLOOR
s10 += '<g id="s10fr"><rect x="560" y="420" width="400" height="1000" rx="24" fill="#d8dfda" class="o"/><path d="M560,820H960" stroke="#2e2a26" stroke-width="6"/><rect x="600" y="560" width="22" height="150" rx="8" fill="#9fb3b8" class="o3"/><rect x="600" y="880" width="22" height="200" rx="8" fill="#9fb3b8" class="o3"/>'
s10 += '<g id="s10x" opacity="0"><path d="M620,500L900,760M900,500L620,760" stroke="#e07a4f" stroke-width="44" stroke-linecap="round" opacity=".85"/><path d="M620,900L900,1300M900,900L620,1300" stroke="#e07a4f" stroke-width="44" stroke-linecap="round" opacity=".85"/></g></g>'
s10 += shadow(340, 1760, 200) + char("p", 160, 1000, 1.5, "pe-s", "pm-s", "p-reach", cid="s10p")
h10 = rule("s10r", 2, "อย่าเปิดตู้เย็น", "ปิดสนิท ≈ 4 ชม. · ช่องฟรีซเต็ม ≈ 48 ชม.", "USDA")
h10 += card("s10k", '<div style="font:700 28px/1 Kanit;letter-spacing:3px">ความเย็นเหลือ</div><div id="s10t" style="font:900 72px/1.1 Orbitron, Kanit">04:00:00</div>', 590, 1180, w=440, rot=2)
h10 += sfx("s10x2", "ปัง!", 620, 640, -12, 150)
h10 += cap("s10", ["กฎข้อ 2 · <span class=\"k\">อย่าเปิดตู้เย็น</span>", "ปิดสนิท ของสดอยู่ได้ ≈ <span class=\"k\">4 ชม.</span>"], top=1700)
scenes.append(scene("s10", s10, h10))
J(f'tl.fromTo("#s10r", {{y:-400}}, {{y:0, duration:0.45, ease:"back.out(1.5)"}}, {st + 0.1});')
J(f'tl.fromTo("#s10p", {{x:-60}}, {{x:30, duration:1.4, ease:"sine.inOut"}}, {st + 0.4});')
J(f'tl.fromTo("#s10x2", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.18, ease:"back.out(3)"}}, {st + 1.9});')
J(f'tl.to("#s10x2", {{opacity:0, duration:0.3}}, {st + 3.0});')
J(f'tl.fromTo("#s10fr", {{x:0}}, {{x:10, duration:0.04, repeat:5, yoyo:true}}, {st + 1.9});')
J(f'tl.fromTo("#s10x", {{opacity:0}}, {{opacity:1, duration:0.2}}, {st + 2.0});')
J(f'tl.to("#s10p", {{x:-80, duration:0.3, ease:"power2.out"}}, {st + 1.95});')
J(f'tl.fromTo("#s10k", {{y:300, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:"back.out(1.6)"}}, {st + 3.4});')
J('(function(){ const el=document.getElementById("s10t"); const vals=["04:00:00","03:59:59","03:59:58","03:59:57","03:59:56"]; ' +
  f'vals.forEach((v,i)=> tl.call(()=>{{ el.textContent=v; }}, null, {st + 3.8} + i)); }})();')
capjs("s10", [(st + 0.3, st + 3.6), (st + 3.7, None)])

# ---------------- S11: stranger with gas can ----------------
st = TIMES["s11"][0]
s11 = '<rect width="1080" height="1920" fill="#22363f"/><path d="M0,0L330,520H750L1080,0Z" fill="#1c2c34" class="o"/><path d="M0,1920L330,1150H750L1080,1920Z" fill="#1a2930" class="o"/>'
s11 += '<rect x="330" y="520" width="420" height="630" fill="#121f25" class="o"/>'
s11 += '<g id="s11m"><path id="s11beam" d="M560,700L1080,560V900Z" fill="#f2d6a0" opacity=".3"/>'
s11 += '<path d="M480,1150V900Q480,860 500,840H600Q620,860 620,900V1150Z" fill="#0f1a1f" class="o3"/><circle cx="550" cy="790" r="52" fill="#0f1a1f" class="o3"/><circle cx="572" cy="772" r="12" fill="#f2d6a0"/>'
s11 += '<g transform="translate(610,960)"><rect width="80" height="110" rx="10" fill="#b0553a" class="o3"/><rect x="18" y="-24" width="40" height="28" rx="6" fill="#b0553a" class="o3"/></g></g>'
s11 += char("p", -40, 1200, 1.35, "pe-s", "pm-f", "p-down", cid="s11p") + char("f", 230, 1220, 1.3, "fe-s", "fm-s", "f-down", cid="s11f")
h11 = card("s11k", '<div style="font:900 64px/1 Kanit">22:40 น.</div>', 700, 150, rot=3)
h11 += bubble("s11b", "“ถอดปลั๊กไว้… ตอนไฟกลับมา <span class=\"k\">ไฟจะกระชาก</span>”", 120, 330, tail="right")
h11 += cap("s11", ["ชายแปลกหน้า <span class=\"k\">หิ้วแกลลอนน้ำมัน</span>", "เดินขึ้นมาถึง<span class=\"k\">ชั้น 27</span>"], top=1700)
scenes.append(scene("s11", s11, h11, bg="#22363f"))
J(f'tl.fromTo("#s11k", {{y:-300}}, {{y:0, duration:0.4, ease:"back.out(1.6)"}}, {st + 0.2});')
J(f'tl.fromTo("#s11m", {{x:520, opacity:0}}, {{x:0, opacity:1, duration:2.2, ease:"power1.out"}}, {st + 0.6});')
J(f'tl.to("#s11m", {{x:-60, scale:0.92, transformOrigin:"550px 1150px", duration:4, ease:"none"}}, {st + 2.8});')
J(f'tl.fromTo("#s11beam", {{rotation:-4}}, {{rotation:4, transformOrigin:"560px 700px", duration:1.2, repeat:9, yoyo:true, ease:"sine.inOut"}}, {st});')
J(f'tl.fromTo("#s11b", {{scale:0, opacity:0, transformOrigin:"80% 100%"}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(2.5)"}}, {st + 7.1});')
J(f'tl.to("#s11m", {{opacity:0, duration:1.2}}, {st + 11.4});')
capjs("s11", [(st + 0.3, st + 3.5), (st + 3.6, st + 7.0)])

# ---------------- S12: rule 3 - CO ----------------
st = TIMES["s12"][0]
s12 = '<rect width="1080" height="1920" fill="#e6d9bd"/>'
s12 += '<g id="s12g"><rect x="140" y="880" width="360" height="260" rx="20" fill="#e07a4f" class="o"/><rect x="170" y="910" width="300" height="130" rx="10" fill="#2e2a26"/><circle cx="240" cy="1090" r="26" fill="#f4ecd8" class="o3"/><rect x="330" y="1070" width="120" height="40" rx="8" fill="#f4ecd8" class="o3"/><text x="320" y="860" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#2e2a26">เครื่องปั่นไฟ</text></g>'
s12 += '<g id="s12b"><path d="M600,960H940L900,1120H640Z" fill="#9fb3b8" class="o"/><path d="M620,960H920" stroke="#2e2a26" stroke-width="8"/>' + "".join(f'<circle cx="{660 + i * 50}" cy="945" r="18" fill="#3a3533" class="o3"/>' for i in range(6)) + '<text x="770" y="860" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#2e2a26">เตาถ่าน</text></g>'
s12 += '<g id="s12no" opacity="0"><circle cx="320" cy="1010" r="230" fill="none" stroke="#b0553a" stroke-width="26"/><path d="M160,850L480,1170" stroke="#b0553a" stroke-width="26"/><circle cx="770" cy="1010" r="230" fill="none" stroke="#b0553a" stroke-width="26"/><path d="M610,850L930,1170" stroke="#b0553a" stroke-width="26"/></g>'
s12 += '<g id="s12co" opacity="0">' + "".join(f'<circle cx="{200 + (i * 137) % 700}" cy="{1350 + (i * 61) % 180}" r="{40 + (i * 13) % 40}" fill="#c9c3b6" opacity=".55"/>' for i in range(14)) + '<text x="540" y="1450" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="110" fill="#5b4f45" opacity=".85">CO</text></g>'
h12 = rule("s12r", 3, "ห้ามปั่นไฟในห้อง", "รวมถึงเตาถ่าน · เปิดหน้าต่างก็ไม่พอ", "CDC")
h12 += cap("s12", ["กฎข้อ 3 · <span class=\"k\">ห้ามปั่นไฟในห้อง</span>", "CO <span class=\"k\">ไม่มีสี ไม่มีกลิ่น</span>"], top=1660)
scenes.append(scene("s12", s12, h12, bg="#e6d9bd"))
J(f'tl.fromTo("#s12r", {{y:-400}}, {{y:0, duration:0.45, ease:"back.out(1.5)"}}, {st + 0.1});')
J(f'tl.fromTo(["#s12g","#s12b"], {{scale:0.3, opacity:0, transformOrigin:"50% 50%"}}, {{scale:1, opacity:1, duration:0.35, stagger:0.15, ease:"back.out(2)"}}, {st + 0.6});')
J(f'tl.fromTo("#s12no", {{opacity:0, scale:1.6, transformOrigin:"540px 1010px"}}, {{opacity:1, scale:1, duration:0.22, ease:"power4.in"}}, {st + 2.6});')
J(f'tl.fromTo("#s12co", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:1.5, ease:"sine.out"}}, {st + 4.6});')
J(f'tl.to("#s12co", {{y:-30, duration:3, ease:"sine.inOut"}}, {st + 6.1});')
capjs("s12", [(st + 0.3, st + 4.5), (st + 4.6, None)])

# ---------------- S13: night on sofa ----------------
st = TIMES["s13"][0]
s13 = DARKROOM + window(80, 180, 420, 560) + FLOOR
s13 += '<radialGradient id="s13g" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#f2d6a0" stop-opacity=".45"/><stop offset="1" stop-color="#f2d6a0" stop-opacity="0"/></radialGradient><ellipse cx="560" cy="1260" rx="520" ry="420" fill="url(#s13g)"/>'
s13 += '<path d="M440,1180H1040V1480H440Z" fill="#7a5a48" class="o"/><path d="M440,1100H1040V1220H440Z" fill="#8a6a56" class="o"/>'
s13 += char("f", 620, 860, 1.25, "fe-z", "fm-n", "f-lap", cid="s13f")
s13 += char("c", 700, 1140, 0.95, "ce-z", "cm-n", cid="s13c")
s13 += '<text id="s13z" x="900" y="1150" font-family="Kanit" font-weight="900" font-size="60" fill="#f4ecd8" opacity="0">z z</text>'
s13 += shadow(260, 1600, 170) + char("p", 100, 1030, 1.3, "pe-w", "pm-f", "p-write", cid="s13p")
h13 = card("s13k", '<div style="display:flex;align-items:center;gap:16px"><svg width="110" height="56" viewBox="0 0 96 48"><rect x="3" y="3" width="80" height="42" rx="8" fill="#f4ecd8" class="o3"/><rect x="84" y="15" width="9" height="18" rx="3" fill="#2e2a26"/><rect id="s13bat" x="10" y="10" width="14" height="28" rx="4" fill="#b0553a"/></svg><div style="font:900 70px/1 Kanit">19%</div></div>', 600, 140, rot=3)
h13 += card("s13n", '<div style="font:700 30px/1 Kanit;letter-spacing:3px">จดลงกระดาษ</div><div style="font:900 50px/1.3 Kanit">1669 เจ็บป่วย<br>199 ไฟไหม้<br>1784 ปภ.</div>', 70, 760, w=420, rot=-3)
h13 += cap("s13", ["จดเบอร์ฉุกเฉิน<span class=\"k\">ลงกระดาษ</span>", "ส้มโอ… <span class=\"k\">หลับ</span>บนตักคนแปลกหน้า"], top=1640)
scenes.append(scene("s13", s13, h13))
J(f'tl.fromTo("#s13k", {{y:-300}}, {{y:0, duration:0.4, ease:"back.out(1.6)"}}, {st + 0.2});')
J(f'tl.fromTo("#s13n", {{x:-500, rotation:-12}}, {{x:0, rotation:-3, duration:0.45, ease:"back.out(1.5)"}}, {st + 1.6});')
J(f'tl.to("#s13n", {{x:-560, duration:0.3, ease:"power2.in"}}, {st + 3.9});')
J(f'tl.fromTo("#s13z", {{opacity:0, y:0}}, {{opacity:1, y:-60, duration:1.5, repeat:2, ease:"sine.out"}}, {st + 3.4});')
J(f'tl.fromTo("#s13c", {{scaleY:1}}, {{scaleY:0.97, transformOrigin:"50% 100%", duration:1, repeat:7, yoyo:true, ease:"sine.inOut"}}, {st});')
capjs("s13", [(st + 0.3, st + 3.8), (st + 3.9, None)])

# ---------------- S14: everything dark except 2719 ----------------
st = TIMES["s14"][0]
s14 = '<rect width="1080" height="1920" fill="#1f3039"/><path d="M0,0L380,600H700L1080,0Z" fill="#192830" class="o"/><path d="M0,1920L380,1100H700L1080,1920Z" fill="#16232a" class="o"/>'
s14 += '<rect x="380" y="600" width="320" height="500" fill="#121c21" class="o"/>'
s14 += '<rect x="450" y="720" width="180" height="380" fill="#22363f" class="o3"/><rect id="s14glow" x="450" y="1090" width="180" height="14" fill="#f2d6a0"/><path id="s14spill" d="M450,1104H630L760,1300H320Z" fill="#f2d6a0" opacity=".35"/>'
s14 += '<rect x="500" y="660" width="80" height="38" rx="4" fill="#e6d9bd" class="o3"/><text x="540" y="689" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#2e2a26">2719</text>'
s14 += char("c", 470, 1360, 0.9, "ce-a", "cm-n", cid="s14c")
h14 = card("s14m", '<div style="font:700 28px/1 Kanit;letter-spacing:3px">แผนผังชั้น 27</div><svg width="520" height="150" viewBox="0 0 520 150" style="display:block;margin-top:10px"><rect x="2" y="54" width="516" height="42" fill="#cdbd98" class="o3"/>'
               + "".join(f'<rect x="{10 + i * 100}" y="4" width="84" height="46" fill="{"#e07a4f" if i in (1,) else "#3c4a50"}" class="o3"/><rect x="{10 + i * 100}" y="100" width="84" height="46" fill="{"#f2d6a0" if i == 4 else ("#e07a4f" if i == 1 else "#3c4a50")}" class="o3"/>' for i in range(5))
               + '<text x="152" y="34" font-family="Kanit" font-weight="900" font-size="20" text-anchor="middle" fill="#2e2a26">เรา</text><text x="152" y="130" font-family="Kanit" font-weight="900" font-size="20" text-anchor="middle" fill="#2e2a26">เรา</text><text x="452" y="130" font-family="Kanit" font-weight="900" font-size="22" text-anchor="middle" fill="#2e2a26">2719</text></svg>', 260, 140, rot=-2)
h14 += sfx("s14x", "หึ่งงง…", 640, 980, 6, 84, WARM)
h14 += cap("s14", ["02:13 น. · ทั้งตึก<span class=\"k\">มืดสนิท</span>", "ยกเว้น<span class=\"k\">ห้อง 2719</span>"], top=1660)
scenes.append(scene("s14", s14, h14, bg="#1f3039"))
J(f'tl.fromTo("#s14v", {{scale:1}}, {{scale:1.18, transformOrigin:"540px 1000px", duration:5.5, ease:"power1.in"}}, {st});')
J(f'tl.fromTo("#s14c", {{y:120, scale:1.2, transformOrigin:"50% 100%"}}, {{y:0, scale:0.9, duration:4.5, ease:"none"}}, {st + 0.4});')
J(f'tl.fromTo(["#s14glow","#s14spill"], {{opacity:.5}}, {{opacity:1, duration:0.18, repeat:25, yoyo:true, ease:"none"}}, {st});')
J(f'tl.fromTo("#s14m", {{y:-300}}, {{y:0, duration:0.4, ease:"back.out(1.6)"}}, {st + 2.6});')
J(f'tl.fromTo("#s14x", {{opacity:0}}, {{opacity:1, duration:0.4}}, {st + 1.2});')
capjs("s14", [(st + 0.2, st + 2.5), (st + 2.6, None)])

# ---------------- S15: the door opens ----------------
st = TIMES["s15"][0]
s15 = '<rect width="1080" height="1920" fill="#16232a"/><rect x="290" y="300" width="500" height="1200" fill="#f2d6a0"/>'
s15 += '<path id="s15beam" d="M290,1500H790L1080,1920H0Z" fill="#f2d6a0" opacity=".5"/>'
s15 += '<rect id="s15d" x="290" y="300" width="500" height="1200" fill="#22363f" class="o"/><rect x="250" y="270" width="580" height="30" fill="#121c21" class="o3"/>'
s15 += char("c", 470, 1440, 1.05, "ce-a", "cm-a", cid="s15c")
s15 += '<g opacity=".95">' + char("p", -60, 1150, 1.5, "pe-s", "pm-s", "p-down") + char("f", 740, 1150, 1.5, "fe-s", "fm-o", "f-down", flip=True) + '</g>'
h15 = sfx("s15x", "เอี๊ยดดด…", 330, 160, -4, 110, WARM)
h15 += cap("s15", ["ทำไม<span class=\"k\">ไฟยังติด</span>?"], top=1700)
scenes.append(scene("s15", s15, h15, bg="#16232a"))
J(f'tl.fromTo("#s15d", {{scaleX:1}}, {{scaleX:0.18, transformOrigin:"0% 50%", duration:2.6, ease:"power2.inOut"}}, {st + 0.3});')
J(f'tl.fromTo("#s15beam", {{opacity:0}}, {{opacity:.5, duration:2}}, {st + 0.6});')
J(f'tl.fromTo("#s15x", {{opacity:0}}, {{opacity:1, duration:0.4}}, {st + 0.3});')
J(f'tl.fromTo("#s15v", {{scale:1}}, {{scale:1.08, transformOrigin:"540px 900px", duration:4.2, ease:"none"}}, {st});')
capjs("s15", [(st + 2.2, None)])

# ---------------- S16: end card ----------------
st = TIMES["s16"][0]
h16 = ('<div id="s16a" class="a" style="left:0;right:0;top:330px;text-align:center"><span class="stamp" style="font-size:54px;display:inline-block;transform:rotate(-4deg)">ตอนต่อไป</span></div>'
       '<div id="s16b" class="a ttl" style="left:0;right:0;top:470px;text-align:center;font-size:150px">ตอนที่ <b>2</b></div>'
       '<div id="s16c" class="a" style="left:60px;right:60px;top:690px;text-align:center;font:900 76px/1.25 Kanit">ห้องที่<span class="k">ไฟไม่เคยดับ</span></div>'
       '<div id="s16d" class="hud a" style="left:110px;width:860px;top:900px;padding:26px 30px 30px;text-align:center;transform:rotate(-1deg)">'
       '<div style="font:700 32px/1 Kanit;letter-spacing:3px">คอมเมนต์บอกหน่อย</div><div style="font:900 56px/1.3 Kanit;margin-top:10px">ถ้าเป็นคุณ… จะเคาะประตู 2719 ไหม?</div>'
       '<div style="display:flex;gap:24px;justify-content:center;margin-top:18px"><div class="stk" style="width:auto;height:auto;border-radius:16px;padding:10px 26px;font-size:46px">A เคาะ</div><div class="stk" style="width:auto;height:auto;border-radius:16px;padding:10px 26px;font-size:46px;background:#9fb3b8">B ไม่เคาะ</div></div></div>'
       '<div id="s16e" class="a" style="left:0;right:0;top:1290px;text-align:center;font:900 60px/1.2 Kanit">กดติดตาม <span style="color:#b0553a">ก่อนไฟจะดับอีกครั้ง</span></div>')
scenes.append(f'<div id="s16" class="clip" data-start="{st}" data-duration="{TIMES["s16"][1] - st:.2f}" data-track-index="0" style="background:radial-gradient(circle, #d4c4a2 1.6px, transparent 2.3px) 0 0/12px 12px #e6d9bd">{h16}</div>')
J(f'tl.fromTo("#s16a", {{opacity:0, scale:2}}, {{opacity:1, scale:1, duration:0.2, ease:"power4.in"}}, {st + 0.1});')
J(f'tl.fromTo("#s16b", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {st + 0.3});')
J(f'tl.fromTo("#s16c", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35, ease:"back.out(2)"}}, {st + 0.6});')
J(f'tl.fromTo("#s16d", {{scale:0.6, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(1.8)"}}, {st + 1.1});')
J(f'tl.fromTo("#s16e", {{opacity:0}}, {{opacity:1, duration:0.4}}, {st + 1.6});')
J(f'tl.fromTo("#s16e", {{scale:1}}, {{scale:1.06, duration:0.5, repeat:5, yoyo:true, ease:"sine.inOut"}}, {st + 2.0});')

# ---------------- assemble ----------------
html = intro
html = html.replace('data-duration="19.6" data-width', f'data-duration="{TOTAL}" data-width')
html = re.sub(r'\s*<audio[^>]*></audio>', '', html)
extra_css = """
      .l { fill: none; stroke: #2e2a26; stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; }
      .l2 { stroke-width: 2.2; } .l4 { stroke-width: 4.5; } .cr { stroke: #f4ecd8; }
      .srcst { margin-left: auto; color: #b0553a; border: 4px solid #b0553a; border-radius: 6px; padding: 2px 12px 4px; font: 900 30px/1.2 Kanit; transform: rotate(-8deg); }
      .bub { background: #f4ecd8; border: 5px solid #2e2a26; border-radius: 28px; padding: 22px 30px 26px; font: 900 52px/1.25 Kanit; box-shadow: 7px 7px 0 rgba(46,42,38,.8); max-width: 820px; }
      .bub i { position: absolute; bottom: -38px; width: 50px; height: 40px; background: #f4ecd8; border: 5px solid #2e2a26; border-top: 0; clip-path: polygon(0 0, 100% 0, 30% 100%); }
    </style>"""
html = html.replace("    </style>", extra_css, 1)
defs = f'<svg width="0" height="0" class="a" style="position:absolute"><defs>{kdefs}</defs></svg>'
html = html.replace('<svg id="grain"', defs + "\n" + "\n".join(scenes) + '\n      <svg id="grain"', 1)
html = html.replace("for (let i = 0; i * 0.083 < 19.6; i++)", f"for (let i = 0; i * 0.083 < {TOTAL}; i++)")
capdef = "\n      // ---- scenes 4-16 ----\n      " + "\n      ".join(js) + "\n\n      // ---- film grain"
html = html.replace("\n      // ---- film grain", capdef, 1)
open(f"{ROOT}/hf/quest/index.html", "w").write(html)
print("ok", len(html))
