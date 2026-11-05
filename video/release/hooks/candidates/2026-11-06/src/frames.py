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

# ---------------- hook 1: box jellyfish — a father's hand tipping a water bottle onto his son's stung shin
h1 = f"""<defs>
<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6c27a"/><stop offset=".45" stop-color="#f7dca8"/><stop offset="1" stop-color="#bfe0e6"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fb6c4"/><stop offset="1" stop-color="#2f7f94"/></linearGradient>
<linearGradient id="sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8cf9c"/><stop offset="1" stop-color="#c8a66a"/></linearGradient>
<radialGradient id="sun"><stop offset="0" stop-color="#fff3c8"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
<linearGradient id="bot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfe8f4" stop-opacity=".75"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".9"/><stop offset="1" stop-color="#9cc8de" stop-opacity=".75"/></linearGradient>
<filter id="b6"><feGaussianBlur stdDeviation="6"/></filter></defs>
<rect width="1080" height="1920" fill="url(#sk)"/><circle cx="820" cy="430" r="260" fill="url(#sun)"/>
<rect y="560" width="1080" height="260" fill="url(#sea)"/><path d="M0,600h1080M0,660h1080M0,720h1080" stroke="#bfe8ee" stroke-width="5" opacity=".5"/>
<path d="M0,800Q540,770 1080,800V1920H0Z" fill="url(#sand)"/>
<path d="M0,790Q260,760 540,790T1080,786" stroke="#fff" stroke-width="10" fill="none" opacity=".7"/>
<!-- far: the vinegar post (empty) and the som-tam auntie's cart -->
<g transform="translate(150,760)" opacity=".85"><rect x="-8" y="-160" width="16" height="160" fill="#8a6a4a"/><rect x="-46" y="-200" width="92" height="56" fill="#f2e6c8" {ln(3)}/><text x="0" y="-164" font-family="F3" font-size="20" text-anchor="middle" fill="#c8241e">น้ำส้มสายชู</text><rect x="-14" y="-140" width="28" height="40" fill="none" stroke="#7a7a7a" stroke-width="3"/></g>
<g transform="translate(880,780)" opacity=".9"><path d="M-80,0V-90H80V0Z" fill="#c8402a" {ln(3)}/><path d="M-100,-90Q0,-150 100,-90Z" fill="#f2c230" {ln(3)}/><circle cx="-50" cy="8" r="16" fill="#3a3a3a"/><circle cx="50" cy="8" r="16" fill="#3a3a3a"/><rect x="-20" y="-130" width="12" height="34" fill="#f2f2e8" {ln(2)}/><rect x="4" y="-128" width="12" height="32" fill="#f2f2e8" {ln(2)}/></g>
<!-- the boy's leg, close: shin across the frame, a translucent box jellyfish tentacles wrapped, welts -->
<path d="M-40,1260Q300,1190 700,1230L760,1330Q380,1310 -40,1380Z" fill="#c98a5e" {ln(6)}/>
<path d="M700,1230Q800,1215 860,1260Q900,1300 860,1340L760,1330Z" fill="#c98a5e" {ln(6)}/>
<path d="M60,1300Q300,1240 660,1270" stroke="#e8b089" stroke-width="10" fill="none" opacity=".6"/>
{''.join(f'<path d="M{120+k*95},1250q30,40 -10,90q-30,30 10,70" stroke="#ff8a8a" stroke-width="10" fill="none" opacity=".55"/>' for k in range(6))}
<g opacity=".8"><ellipse cx="430" cy="1150" rx="78" ry="58" fill="#e8f6ff" stroke="#a8d8f0" stroke-width="4" opacity=".55"/>
{''.join(f'<path d="M{380+k*22},1190q{-20+k*10},60 {10-k*6},130q20,40 -10,90" stroke="#d8f0ff" stroke-width="4" fill="none" opacity=".85"/>' for k in range(5))}</g>
<!-- father's hand and the bottle, mid-pour (the lure) -->
<g transform="translate(640,900) rotate(28)"><rect x="-55" y="-210" width="110" height="300" rx="36" fill="url(#bot)" {ln(5)}/><rect x="-30" y="-262" width="60" height="56" rx="10" fill="#3a8ad0" {ln(4)}/><rect x="-55" y="-120" width="110" height="70" fill="#cfe8f4" opacity=".8"/>
<path d="M-60,-30Q-130,-40 -150,20Q-140,70 -80,60L-40,40Z" fill="#b97c52" {ln(5)}/><path d="M60,-60Q120,-70 128,-10Q120,40 60,30Z" fill="#b97c52" {ln(5)}/></g>
<path d="M560,1010q-20,80 -40,140q-12,50 0,90" stroke="#dff4ff" stroke-width="22" fill="none" opacity=".75" stroke-linecap="round"/>
<path d="M560,1010q-20,80 -40,140q-12,50 0,90" stroke="#ffffff" stroke-width="8" fill="none" opacity=".9" stroke-linecap="round"/>
<!-- the boy's face, wincing, top left -->
<g transform="translate(230,560)"><circle r="120" fill="#c98a5e" {ln(6)}/><path d="M-120,-30Q-110,-140 0,-150Q110,-140 120,-30Q60,-90 0,-80Q-60,-90 -120,-30Z" fill="#1e1612"/><path d="M-60,-10l40,16M60,-10l-40,16" {ln(8)}/><path d="M-40,60q40,-30 80,0" fill="#5a1a1a" {ln(5)}/><path d="M-90,30q-10,30 6,40" stroke="#bfe8ff" stroke-width="10" fill="none"/></g>
"""

# ---------------- hook 2: the waterfall turns red-brown while mum kneels packing the picnic
h2 = f"""<defs>
<linearGradient id="sk2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a7a7e"/><stop offset="1" stop-color="#a8b8a4"/></linearGradient>
<linearGradient id="fall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a4a26"/><stop offset=".55" stop-color="#b8784a"/><stop offset="1" stop-color="#e8f2f2"/></linearGradient>
<linearGradient id="pool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a5a32"/><stop offset=".5" stop-color="#6a9a8a"/><stop offset="1" stop-color="#3a6a62"/></linearGradient>
<filter id="b8"><feGaussianBlur stdDeviation="8"/></filter></defs>
<rect width="1080" height="1920" fill="url(#sk2)"/>
<path d="M0,0H1080V900Q900,840 780,880V300Q680,260 540,300Q400,250 300,320V900Q160,860 0,920Z" fill="#2e4a34"/>
{''.join(f'<circle cx="{(k*137)%1080}" cy="{60+(k*73)%520}" r="{70+(k*31)%60}" fill="#{["22402a","35583a","2a4a30"][k%3]}"/>' for k in range(26))}
<path d="M300,320Q420,280 540,300Q660,270 780,300L760,960H320Z" fill="#5a5048"/>
<path d="M400,300Q540,280 680,300L700,960H380Z" fill="url(#fall)"/>
{''.join(f'<path d="M{410+k*28},{320+(k%3)*30}V{940}" stroke="#{["c89060","f2e2c8","a86a3e"][k%3]}" stroke-width="{6+(k%2)*4}" opacity=".7"/>' for k in range(10))}
<ellipse cx="540" cy="960" rx="300" ry="50" fill="#f2e8dc" opacity=".8" filter="url(#b8)"/>
<path d="M0,940Q300,900 540,960Q800,920 1080,960V1400H0Z" fill="url(#pool)"/>
<path d="M120,1010q200,-30 420,10M600,1040q200,-20 400,10" stroke="#e8d8c8" stroke-width="6" fill="none" opacity=".5"/>
{''.join(f'<path d="M{200+k*170},{990+(k%2)*40}l40,-6l20,14l-30,10z" fill="#5a3a1e" opacity=".8"/>' for k in range(5))}
<path d="M0,1300Q300,1240 620,1290Q860,1260 1080,1300V1920H0Z" fill="#7a6a58"/>
<path d="M0,1300Q300,1240 620,1290Q860,1260 1080,1300" stroke="{INK}" stroke-width="6" fill="none"/>
<!-- picnic: striped mat half folded, cool box, slippers (the lure: packing) -->
<path d="M180,1420L700,1380L760,1520L220,1570Z" fill="#d8302a" {ln(5)}/>{''.join(f'<path d="M{200+k*80},{1418-k*3}L{240+k*80},{1566-k*4}" stroke="#f2f2e8" stroke-width="18"/>' for k in range(7))}
<path d="M560,1390L700,1380L760,1520L620,1530Z" fill="#a8201a" {ln(5)}/>
<g transform="translate(860,1440)"><rect x="-90" y="-80" width="180" height="120" rx="14" fill="#2a6ad0" {ln(5)}/><rect x="-90" y="-100" width="180" height="34" rx="10" fill="#f2f2f2" {ln(4)}/></g>
<g transform="translate(330,1610) rotate(-12)"><ellipse rx="40" ry="16" fill="#f2c230" {ln(3)}/></g><g transform="translate(400,1620) rotate(8)"><ellipse rx="40" ry="16" fill="#f2c230" {ln(3)}/></g>
<!-- mum kneeling, back to the falls, folding the mat -->
<g transform="translate(560,1360)"><path d="M-70,0Q-80,-150 0,-170Q80,-150 70,0Z" fill="#3a9a6a" {ln(5)}/><circle cy="-220" r="56" fill="#c98a5e" {ln(5)}/><path d="M-56,-230Q-50,-290 0,-290Q56,-290 58,-226Q30,-260 0,-256Q-30,-262 -56,-230Z" fill="#1e1612"/>
<path d="M-60,-120L-170,40M60,-120L120,40" stroke="#c98a5e" stroke-width="26" stroke-linecap="round"/><path d="M-60,0L-90,80H90L60,0Z" fill="#2a3a5a" {ln(4)}/></g>
<!-- grandpa's radio on the high rock (the clue), top right -->
<g transform="translate(900,700)"><path d="M-120,40L-80,-40H90L130,40Z" fill="#6a6058" {ln(4)}/><rect x="-36" y="-80" width="72" height="44" rx="8" fill="#c8402a" {ln(3)}/><path d="M24,-80l26,-50" stroke="{INK}" stroke-width="4"/><path d="M-80,-120q20,-14 40,0M-90,-140q30,-22 60,0" stroke="#ffe08a" stroke-width="4" fill="none"/></g>
"""

# ---------------- hook 3: rip current — the dark calm gap between the breakers, a swimmer pulled out
h3 = f"""<defs>
<linearGradient id="sk3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ab8e0"/><stop offset="1" stop-color="#d8eef6"/></linearGradient>
<linearGradient id="sea3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a7a9a"/><stop offset="1" stop-color="#5ab8c8"/></linearGradient>
<linearGradient id="rip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a4a62"/><stop offset="1" stop-color="#2a6a7e"/></linearGradient>
<filter id="b5"><feGaussianBlur stdDeviation="5"/></filter></defs>
<rect width="1080" height="1920" fill="url(#sk3)"/>
<rect y="380" width="1080" height="1200" fill="url(#sea3)"/>
<!-- breakers left and right, a calm dark channel in the middle running out to sea -->
{''.join(f'<path d="M0,{560+k*150}Q140,{530+k*150} 330,{560+k*150}" stroke="#ffffff" stroke-width="{22+k*6}" fill="none" opacity=".85" stroke-linecap="round"/><path d="M750,{560+k*150}Q940,{530+k*150} 1080,{560+k*150}" stroke="#ffffff" stroke-width="{22+k*6}" fill="none" opacity=".85" stroke-linecap="round"/>' for k in range(6))}
<path d="M360,1560Q400,1000 470,420H620Q690,1000 730,1560Z" fill="url(#rip)" opacity=".9"/>
{''.join(f'<path d="M{430+k*40},{1500-k*60}q10,-60 0,-120" stroke="#e8f2f2" stroke-width="5" fill="none" opacity=".45"/>' for k in range(6))}
<path d="M545,1380V560" stroke="#ffffff" stroke-width="10" stroke-dasharray="40 30" opacity=".35"/><path d="M520,600l25,-50l25,50" fill="none" stroke="#ffffff" stroke-width="10" opacity=".45"/>
<path d="M0,1560Q540,1500 1080,1560V1920H0Z" fill="#e8d6a8"/><path d="M0,1560Q540,1500 1080,1560" stroke="#ffffff" stroke-width="16" fill="none"/>
<!-- the swimmer in the channel, arm up, head low -->
<g transform="translate(560,900)"><ellipse rx="70" ry="22" fill="#ffffff" opacity=".6"/><circle cy="-30" r="34" fill="#c98a5e" {ln(4)}/><path d="M-34,-40Q-30,-74 0,-74Q32,-74 34,-40Q10,-56 -34,-40Z" fill="#1e1612"/><path d="M20,-20L80,-140" stroke="#c98a5e" stroke-width="20" stroke-linecap="round"/><path d="M-6,-24q8,6 16,0" stroke="{INK}" stroke-width="4" fill="none"/></g>
<!-- the little sister's yellow duck float on the sand (the clue), parents' umbrella -->
<g transform="translate(220,1700)"><ellipse rx="80" ry="34" fill="#f2c230" {ln(4)}/><ellipse rx="34" ry="14" fill="#e8d6a8"/><circle cx="60" cy="-30" r="22" fill="#f2c230" {ln(3)}/><path d="M78,-30l20,4l-20,6z" fill="#f07a1a"/></g>
<g transform="translate(860,1660)"><path d="M0,0V-260" stroke="#6a5a4a" stroke-width="10"/><path d="M-180,-240Q0,-330 180,-240Z" fill="#d8302a" {ln(4)}/><path d="M-90,-262Q0,-320 90,-262" stroke="#f2f2e8" stroke-width="14" fill="none"/></g>
<!-- the red flag on the lifeguard pole -->
<g transform="translate(120,1380)"><path d="M0,200V-120" stroke="#6a5a4a" stroke-width="10"/><path d="M0,-120l110,30l-110,40z" fill="#d8241e" {ln(3)}/></g>
"""

for i, (body, c1, cmd) in enumerate([(h1, "ถ้าวันหนึ่ง… น้องคุณโดนแมงกะพรุนที่ทะเล", "อย่าเอาน้ำเปล่าราด"),
                                      (h2, "ถ้าวันหนึ่ง… น้ำตกตรงหน้าคุณเปลี่ยนเป็นสีขุ่นแดง", "อย่ารอเก็บของ"),
                                      (h3, "ถ้าวันหนึ่ง… คลื่นดึงคุณออกจากฝั่ง", "อย่าว่ายสวนเข้าฝั่ง")], 1):
    open(os.path.join(OUT, f"hook{i}.html"), "w").write(page(body, c1, cmd, "ฮุก " + str(i)))
print("ok")
