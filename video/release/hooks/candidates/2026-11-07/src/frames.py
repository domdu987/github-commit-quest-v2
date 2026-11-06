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


# ---------------- hook 1: car into a canal — mother's hand reaching back to her son's buckle, water at the window line
h1 = f"""<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a7a6a"/><stop offset="1" stop-color="#1e3a34"/></linearGradient>
<linearGradient id="in" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a40"/><stop offset="1" stop-color="#1a1a20"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#in)"/>
<!-- side window: water rising outside, bubbles -->
<rect x="80" y="260" width="920" height="560" rx="60" fill="url(#w)" {ln(8)}/>
<path d="M80,520Q300,490 540,520T1000,515V820H80Z" fill="#2a5a50" opacity=".9"/>
{''.join(f'<circle cx="{150+k*110}" cy="{560+(k*53)%220}" r="{8+k%3*5}" fill="none" stroke="#bfe8de" stroke-width="3" opacity=".7"/>' for k in range(8))}
<path d="M80,520Q300,490 540,520T1000,515" stroke="#dff4ee" stroke-width="6" fill="none"/>
<!-- rear seat: the boy in his seat, belt across -->
<rect x="140" y="860" width="800" height="520" rx="50" fill="#4a4048" {ln(6)}/>
<g transform="translate(560,1040)"><circle r="110" fill="#c98a5e" {ln(6)}/><path d="M-110,-20Q-100,-130 0,-140Q100,-130 110,-20Q50,-80 0,-70Q-50,-80 -110,-20Z" fill="#1e1612"/>
<path d="M-50,-5l30,12M50,-5l-30,12" {ln(7)}/><ellipse cy="60" rx="30" ry="22" fill="#5a1a1a" {ln(4)}/><path d="M-80,20q-10,30 6,40M80,20q10,30 -6,40" stroke="#bfe8ff" stroke-width="9" fill="none"/></g>
<path d="M380,940L720,1360" stroke="#2a2a2a" stroke-width="44"/><path d="M380,940L720,1360" stroke="#5a5a5a" stroke-width="30"/>
<rect x="650" y="1280" width="110" height="70" rx="12" fill="#c8c8cc" {ln(5)}/><rect x="676" y="1300" width="58" height="30" rx="6" fill="#d8241e"/>
<!-- mother's arm reaching from the front seat to the buckle (the lure) -->
<path d="M1080,1500Q900,1420 780,1330" stroke="#b97c52" stroke-width="70" stroke-linecap="round" fill="none"/>
<path d="M1080,1500Q900,1420 780,1330" stroke="{INK}" stroke-width="6" fill="none" opacity=".4"/>
<circle cx="770" cy="1320" r="46" fill="#b97c52" {ln(5)}/>
<!-- her own belt still locked, in the foreground -->
<path d="M1000,1560L1080,1760" stroke="#2a2a2a" stroke-width="40"/>
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

# ---------------- hook 3: storm over the rice field, father waving from under the lone tree
h3 = f"""<defs><linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2e3a"/><stop offset=".6" stop-color="#4a5260"/><stop offset="1" stop-color="#6a7a5a"/></linearGradient>
<linearGradient id="rf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a8a3a"/><stop offset="1" stop-color="#3a5a22"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#st)"/>
<!-- clouds -->
{''.join(f'<ellipse cx="{k*170}" cy="{180+(k%3)*40}" rx="190" ry="90" fill="#1e222c" opacity=".9"/>' for k in range(8))}
<!-- the bolt far left -->
<path d="M160,240L120,520L190,520L130,820" stroke="#f4f8ff" stroke-width="12" fill="none" stroke-linejoin="round"/>
<path d="M160,240L120,520L190,520L130,820" stroke="#9ac0ff" stroke-width="30" fill="none" opacity=".35"/>
<!-- rain -->
{''.join(f'<path d="M{(k*53)%1080},{(k*97)%1500}l-18,60" stroke="#c8d2e0" stroke-width="3" opacity=".5"/>' for k in range(70))}
<!-- the field -->
<path d="M0,1040Q540,1000 1080,1040V1920H0Z" fill="url(#rf)"/>
{''.join(f'<path d="M0,{1100+k*90}Q540,{1060+k*90} 1080,{1100+k*90}" stroke="#8aaa4a" stroke-width="4" fill="none" opacity=".5"/>' for k in range(9))}
<!-- the lone tree on the ridge, father under it waving -->
<g transform="translate(720,1060)"><path d="M-20,0V-260M20,0V-260" stroke="#3a2a1a" stroke-width="22"/>
<ellipse cy="-340" rx="230" ry="150" fill="#22381a" {ln(6)}/><ellipse cx="-80" cy="-390" rx="120" ry="80" fill="#2a4a20"/>
<g transform="translate(70,-10)"><circle cy="-120" r="28" fill="#b97c52" {ln(4)}/><path d="M-24,-90h48l10,90h-68z" fill="#3a5a8a" {ln(4)}/><path d="M20,-80L70,-170" stroke="#b97c52" stroke-width="16" stroke-linecap="round"/></g></g>
<!-- foreground: the child's back and muddy feet, mid-step toward the tree (the lure) -->
<g transform="translate(380,1640)"><path d="M-90,-300Q0,-340 90,-300L110,0H-110Z" fill="#c84a3a" {ln(6)}/><circle cy="-360" r="80" fill="#1e1612" {ln(6)}/>
<path d="M-60,0L-90,200M60,0L100,180" stroke="#c98a5e" stroke-width="44" stroke-linecap="round"/></g>
<!-- grandpa crouched far right, small, feet together (the clue) -->
<g transform="translate(960,1260)" opacity=".85"><ellipse cy="10" rx="40" ry="8" fill="#000" opacity=".3"/><path d="M-26,0Q-30,-50 0,-60Q30,-50 26,0Z" fill="#6a6a5a" {ln(3)}/><circle cy="-70" r="16" fill="#b97c52" {ln(3)}/></g>
"""

for i, (body, c1, cmd) in enumerate([(h1, "ถ้าวันหนึ่ง… รถคุณตกน้ำกับลูก", "อย่าปลดเข็มขัดลูกก่อน"),
                                      (h2, "ถ้าวันหนึ่ง… แม่คุณล้มกลางกลิ่นแก๊ส", "อย่าเปิดไฟ"),
                                      (h3, "ถ้าวันหนึ่ง… พ่อเรียกคุณไปใต้ต้นไม้", "อย่าวิ่งไปหาพ่อ")], 1):
    open(os.path.join(OUT, f"hook{i}.html"), "w").write(page(body, c1, cmd, "ฮุก " + str(i)))
print("ok")
