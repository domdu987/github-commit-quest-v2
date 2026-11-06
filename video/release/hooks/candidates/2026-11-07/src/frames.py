import os
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "/tmp/claude-0/-home-user-github-commit-quest-v2/dadc119d-850b-549d-82c6-f1e8a1f13306/scratchpad/mw/hf/rig/assets/fonts/f3.ttf"
INK = "#1e1a16"

def page(body, cap1, cmd, badge):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:F3;src:url('file://{FONT}')}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000}}
.cap{{position:absolute;left:0;right:0;top:1430px;text-align:center;font-family:F3;color:#fff}}
.l1{{display:inline-block;font-size:44px;white-space:nowrap;background:rgba(10,12,16,.82);border:3px solid rgba(255,255,255,.25);border-radius:22px;padding:14px 34px}}
.l2{{display:inline-block;margin-top:22px;font-size:80px;background:#d8241e;border-radius:22px;padding:12px 40px;box-shadow:0 8px 0 #7a0e0a}}
.badge{{position:absolute;left:40px;bottom:160px;font-family:F3;font-size:30px;color:#fff;background:rgba(0,0,0,.45);padding:6px 16px;border-radius:12px}}
.tag{{position:absolute;right:30px;top:30px;font-family:F3;font-size:28px;color:#ffd84a;background:rgba(0,0,0,.5);padding:6px 14px;border-radius:10px}}
</style></head><body>
<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{body}</svg>
<div class="cap"><div class="l1">{cap1}</div><br><div class="l2">{cmd}</div></div>
<div class="badge">{badge}</div><div class="tag">ร่างเฟรม 0 · ไม่ใช่ภาพจาก engine</div>
</body></html>"""

def ln(w=4): return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


# ---------------- hook 1 (v2, 6 Nov): DAYTIME flash flood on a road — brown water at the windscreen, toddler in a rear-facing car seat,
# the mother at the wheel twisting back to the car-seat buckle while her own belt is still locked (different from นาทีก่อนจม: night canal)
h1 = f"""<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bcd2dc"/><stop offset="1" stop-color="#e8e2c8"/></linearGradient>
<linearGradient id="mud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8804a"/><stop offset="1" stop-color="#6a4a26"/></linearGradient>
<linearGradient id="cab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a5a62"/><stop offset="1" stop-color="#2e2e34"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#cab)"/>
<!-- windscreen: daylight, a flooded road, brown current, a road sign half under water -->
<path d="M90,180H990L940,700H140Z" fill="url(#sky)" {ln(8)}/>
<path d="M140,520Q540,470 940,520L940,700H140Z" fill="url(#mud)"/>
{''.join(f'<path d="M{160+k*70},{540+(k%3)*40}q30,-14 60,0" stroke="#e8d2a8" stroke-width="5" fill="none" opacity=".8"/>' for k in range(11))}
<g transform="translate(760,470)"><path d="M0,80V-40" stroke="#6a6a6a" stroke-width="10"/><rect x="-50" y="-110" width="100" height="70" rx="8" fill="#f2c230" {ln(4)}/><path d="M-30,-60l60,-30" stroke="{INK}" stroke-width="8"/></g>
<path d="M140,520Q540,470 940,520" stroke="#f2e6c8" stroke-width="6" fill="none"/>
<!-- dashboard + steering wheel (driver = mother, right-hand drive) -->
<path d="M60,700H1020V860H60Z" fill="#26262c" {ln(6)}/>
<circle cx="780" cy="820" r="150" fill="none" stroke="#1a1a1e" stroke-width="34"/><circle cx="780" cy="820" r="40" fill="#1a1a1e"/>
<!-- rear-facing toddler car seat (between the front seats, seen from the driver) -->
<g transform="translate(400,1220)"><path d="M-200,-260Q-210,120 -120,200H140Q220,120 210,-260Q0,-330 -200,-260Z" fill="#d8302a" {ln(7)}/>
<path d="M-150,-200Q0,-250 150,-200V120H-150Z" fill="#f2a0a0" opacity=".35"/>
<circle cy="-100" r="92" fill="#c98a5e" {ln(6)}/><path d="M-92,-120Q-80,-200 0,-206Q80,-200 92,-120Q40,-160 0,-150Q-40,-160 -92,-120Z" fill="#2a1e16"/>
<path d="M-40,-110l26,10M40,-110l-26,10" {ln(6)}/><ellipse cy="-50" rx="26" ry="18" fill="#5a1a1a" {ln(4)}/><path d="M-66,-80q-8,24 4,32" stroke="#bfe8ff" stroke-width="8" fill="none"/>
<path d="M-90,-10L0,60L90,-10" stroke="#2a2a2a" stroke-width="26" fill="none"/><rect x="-30" y="40" width="60" height="50" rx="10" fill="#c8c8cc" {ln(4)}/><rect x="-16" y="54" width="32" height="22" rx="4" fill="#d8241e"/></g>
<!-- water already on the cabin floor -->
<path d="M0,1560Q540,1520 1080,1560V1920H0Z" fill="#8a6a3a" opacity=".85"/>
<!-- the mother's arm twisting back to the car-seat buckle (the lure) · her own belt locked across her shoulder, foreground right -->
<path d="M1100,1200Q760,1250 430,1290" stroke="#b97c52" stroke-width="70" stroke-linecap="round" fill="none"/><circle cx="420" cy="1290" r="44" fill="#b97c52" {ln(5)}/>
<path d="M880,1000L1080,1500" stroke="#2a2a2a" stroke-width="48"/><rect x="1000" y="1360" width="80" height="60" rx="8" fill="#c8c8cc" {ln(4)}/>
"""

# ---------------- hook 2: dark kitchen, gas smell, mother on the floor, a child's hand on the light switch
h2 = f"""<defs><radialGradient id="dk" cx=".5" cy=".55" r=".7"><stop offset="0" stop-color="#2a3038"/><stop offset="1" stop-color="#0a0c10"/></radialGradient>
<linearGradient id="dr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f2d28a" stop-opacity=".0"/><stop offset="1" stop-color="#f2d28a" stop-opacity=".35"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#dk)"/>
<!-- door light from the hall -->
<path d="M0,300L420,520V1400L0,1700Z" fill="url(#dr)"/>
<!-- stove + LPG tank, a faint green-grey haze (gas) -->
<rect x="560" y="560" width="440" height="300" rx="16" fill="#3a3e44" {ln(5)}/><circle cx="680" cy="620" r="40" fill="#22262a" {ln(4)}/><circle cx="880" cy="620" r="40" fill="#22262a" {ln(4)}/>
<rect x="600" y="880" width="150" height="260" rx="60" fill="#5a6a8a" {ln(5)}/><rect x="640" y="850" width="70" height="40" rx="8" fill="#9aa2aa" {ln(4)}/>
{''.join(f'<path d="M{620+k*60},{860-k*18}q40,-60 0,-120q-40,-60 10,-120" stroke="#9ab8a0" stroke-width="10" fill="none" opacity=".25"/>' for k in range(6))}
<!-- the woman on the floor, apron (silhouette — face hidden) -->
<path d="M380,1330Q520,1270 760,1300Q860,1320 900,1370Q760,1400 520,1400Q420,1395 380,1330Z" fill="#2e2a2c" {ln(5)}/>
<path d="M560,1290L700,1300L690,1390L560,1395Z" fill="#c84a4a" opacity=".85"/>
<circle cx="350" cy="1340" r="52" fill="#3a3230" {ln(5)}/><path d="M300,1320q40,-40 100,-10" stroke="#1e1612" stroke-width="30" fill="none"/>
<!-- light switch on the wall by the door, a child's finger almost on it (the lure) -->
<rect x="150" y="760" width="110" height="170" rx="14" fill="#e8e2d6" {ln(5)}/><rect x="185" y="800" width="40" height="70" rx="8" fill="#cfc8bc" {ln(4)}/>
<path d="M-20,900Q90,860 160,840" stroke="#c98a5e" stroke-width="54" stroke-linecap="round"/><circle cx="178" cy="836" r="24" fill="#c98a5e" {ln(4)}/>
<circle cx="205" cy="835" r="70" fill="none" stroke="#ffd84a" stroke-width="4" stroke-dasharray="12 10" opacity=".7"/>
"""

# ---------------- hook 3 (v2, 6 Nov · replaces lightning): flooded house — father under the brown water by the gate, daughter on the stairs,
# one foot already in the water (the lure: going in after him)
h3 = f"""<defs><linearGradient id="fw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a7a48"/><stop offset="1" stop-color="#5a4224"/></linearGradient>
<linearGradient id="wl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8cdb4"/><stop offset="1" stop-color="#b8aa8a"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#wl)"/>
<!-- the open doorway to the street: gate, a floating plastic chair, rain-grey daylight -->
<rect x="420" y="240" width="560" height="760" fill="#c8d4d8" {ln(8)}/>
<path d="M440,620H960" stroke="#5a5a5a" stroke-width="10"/>{''.join(f'<path d="M{460+k*50},620V880" stroke="#5a5a5a" stroke-width="8"/>' for k in range(10))}
<!-- the water: inside and outside, one level -->
<path d="M0,860Q540,830 1080,860V1920H0Z" fill="url(#fw)"/>
{''.join(f'<path d="M{40+k*90},{900+(k%4)*60}q30,-12 60,0" stroke="#d8c09a" stroke-width="5" fill="none" opacity=".7"/>' for k in range(12))}
<g transform="translate(860,880) rotate(-12)"><path d="M-50,0h100v-20h-100z" fill="#2a8ad0" {ln(4)}/><path d="M-40,-20v-60h80v60" fill="none" stroke="#2a8ad0" stroke-width="12"/></g>
<!-- the father: only a hand and the top of his head above the water near the gate -->
<g transform="translate(640,900)"><ellipse rx="120" ry="20" fill="#e8d6b0" opacity=".5"/><path d="M-40,0Q0,-46 40,0" fill="#2a1e16" {ln(4)}/>
<path d="M90,10L130,-130" stroke="#b97c52" stroke-width="26" stroke-linecap="round"/><circle cx="134" cy="-140" r="20" fill="#b97c52" {ln(4)}/></g>
<!-- the stairs down into the water, the daughter halfway, one foot in -->
{''.join(f'<path d="M{0+k*40},{1880-k*110}h300v110h-300z" fill="#9a8a72" {ln(4)}/>' for k in range(8))}
<g transform="translate(300,1300)"><path d="M-70,-260Q0,-290 70,-260L90,40H-90Z" fill="#3a6ac8" {ln(6)}/><circle cy="-320" r="66" fill="#1e1612" {ln(6)}/>
<path d="M-40,40L-60,240M40,40L90,330" stroke="#c98a5e" stroke-width="38" stroke-linecap="round"/>
<path d="M60,-200L250,-330" stroke="#c98a5e" stroke-width="30" stroke-linecap="round"/></g>
<!-- the clue: empty gallons tied with a rope on the stair rail (ยาย's habit) -->
<g transform="translate(140,1080)">{''.join(f'<rect x="{k*70}" y="0" width="56" height="80" rx="12" fill="#e8eef0" {ln(3)}/>' for k in range(3))}<path d="M-20,0Q100,-40 220,0" stroke="#c8a040" stroke-width="6" fill="none"/></g>
"""

for i, (body, c1, cmd) in enumerate([(h1, "ถ้าวันหนึ่ง… น้ำพัดรถคุณกับลูก", "อย่าปลดเข็มขัดลูกก่อน"),
                                      (h2, "ถ้าวันหนึ่ง… แม่คุณล้มกลางกลิ่นแก๊ส", "อย่าเปิดไฟ"),
                                      (h3, "ถ้าวันหนึ่ง… พ่อคุณจมน้ำหน้าบ้าน", "อย่าลงไปช่วยพ่อ")], 1):
    open(os.path.join(OUT, f"hook{i}.html"), "w").write(page(body, c1, cmd, "ฮุก " + str(i)))
print("ok")
