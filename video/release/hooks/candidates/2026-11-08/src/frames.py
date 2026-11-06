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


# ---------------- hook 1: riverbank, a child just pulled out, grandma lifting him over her shoulder (the folk "drain the water" move)
h1 = f"""<defs><linearGradient id="s1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2d8a0"/><stop offset="1" stop-color="#c8d8c0"/></linearGradient>
<linearGradient id="r1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a9a8a"/><stop offset="1" stop-color="#4a6a5a"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#s1)"/><rect y="520" width="1080" height="380" fill="url(#r1)"/>
{''.join(f'<path d="M{k*120},{600+(k%3)*80}q40,-14 80,0" stroke="#cfe4da" stroke-width="5" fill="none" opacity=".6"/>' for k in range(9))}
<path d="M0,880Q540,840 1080,880V1920H0Z" fill="#b89a6a"/><path d="M0,880Q540,840 1080,880" stroke="#8a6a3a" stroke-width="8" fill="none"/>
<!-- grandma, back to us, hoisting the limp boy over her shoulder -->
<g transform="translate(560,1360)"><path d="M-150,-330Q0,-380 150,-330L190,240H-190Z" fill="#7a4a8a" {ln(7)}/><circle cy="-400" r="86" fill="#d8d0c4" {ln(6)}/>
<path d="M-60,-470q60,-40 120,0" stroke="#e8e4dc" stroke-width="30" fill="none"/>
<g transform="translate(-40,-420) rotate(-70)"><path d="M0,0h300v90h-300z" fill="#3a8ad0" {ln(6)}/><circle cx="340" cy="45" r="60" fill="#c98a5e" {ln(5)}/><path d="M330,15q12,10 0,20M352,15q12,10 0,20" stroke="{INK}" stroke-width="4" fill="none"/>
<path d="M60,90l-40,160M200,90l-10,170" stroke="#c98a5e" stroke-width="30" stroke-linecap="round"/></g></g>
<!-- water dripping from the boy -->
{''.join(f'<path d="M{380+k*30},{900+k*40}v30" stroke="#9ad0f0" stroke-width="6" stroke-linecap="round"/>' for k in range(5))}
<!-- the parent's hands reaching in from the right (the choice), a phone on the sand showing 1669 -->
<path d="M1100,1400Q900,1380 780,1300" stroke="#b97c52" stroke-width="56" stroke-linecap="round" fill="none"/>
<g transform="translate(200,1700) rotate(-12)"><rect x="-60" y="-110" width="120" height="220" rx="18" fill="#1e1e22" {ln(4)}/><rect x="-48" y="-92" width="96" height="170" rx="8" fill="#2a8a4a"/><text x="0" y="0" font-family="F3" font-size="34" text-anchor="middle" fill="#fff">1669</text></g>
"""

# ---------------- hook 2: a pond, the little brother waving and sinking, the older sister on the bank rolling her eyes (the 4th "prank")
h2 = f"""<defs><linearGradient id="s2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ac8e0"/><stop offset="1" stop-color="#d8ecd0"/></linearGradient>
<linearGradient id="p2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a8a6a"/><stop offset="1" stop-color="#2a4a3a"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#s2)"/>
<ellipse cx="540" cy="900" rx="620" ry="300" fill="url(#p2)" {ln(6)}/>
<!-- the boy in the water, one hand up, head tipping back, mouth at the waterline -->
<g transform="translate(620,860)"><ellipse rx="90" ry="20" fill="#cfe8d8" opacity=".6"/><circle cy="-20" r="46" fill="#c98a5e" {ln(5)}/><path d="M-46,-30Q-40,-74 0,-76Q40,-74 46,-30Q20,-56 -46,-30Z" fill="#1e1612"/>
<path d="M30,-10L90,-170" stroke="#c98a5e" stroke-width="22" stroke-linecap="round"/><ellipse cx="0" cy="8" rx="14" ry="6" fill="#5a1a1a"/></g>
{''.join(f'<circle cx="{580+k*24}" cy="{820-k*30}" r="{6+k*2}" fill="none" stroke="#e8f4ee" stroke-width="3"/>' for k in range(4))}
<!-- tally marks scratched on the jetty post: three prank days -->
<g transform="translate(180,1180)"><rect x="-26" y="-260" width="52" height="320" fill="#8a6a4a" {ln(4)}/><path d="M-12,-200v60M0,-200v60M12,-200v60" stroke="#f2e6c8" stroke-width="6"/></g>
<!-- the sister on the bank, arms crossed, back to the camera, phone in hand (the lure: ignore him) -->
<path d="M0,1240Q540,1200 1080,1240V1920H0Z" fill="#8aa85a"/>
<g transform="translate(560,1700)"><path d="M-120,-300Q0,-340 120,-300L140,60H-140Z" fill="#e85a7a" {ln(6)}/><circle cy="-370" r="84" fill="#1e1612" {ln(6)}/>
<path d="M-120,-220Q0,-180 120,-220" stroke="#c98a5e" stroke-width="40" stroke-linecap="round" fill="none"/></g>
"""

# ---------------- hook 3: longtail boat to an island, the child tugging at the orange vest buckle, mother's fingers on it
h3 = f"""<defs><linearGradient id="s3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd890"/><stop offset="1" stop-color="#9ad8e8"/></linearGradient>
<linearGradient id="w3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a9ab8"/><stop offset="1" stop-color="#1a5a7a"/></linearGradient></defs>
<rect width="1080" height="1920" fill="url(#s3)"/><circle cx="860" cy="300" r="110" fill="#fff4c8"/>
<rect y="620" width="1080" height="1300" fill="url(#w3)"/>
<path d="M700,620q80,-120 200,-90q90,20 140,90z" fill="#3a6a3a"/>
{''.join(f'<path d="M{k*110},{700+(k%4)*70}q40,-16 80,0" stroke="#bfeaf2" stroke-width="5" fill="none" opacity=".7"/>' for k in range(10))}
<!-- the boat hull, close -->
<path d="M-40,1300Q540,1260 1120,1300L1040,1600Q540,1640 40,1600Z" fill="#a8743a" {ln(8)}/><path d="M-40,1300Q540,1260 1120,1300" stroke="#e8c88a" stroke-width="10" fill="none"/>
<!-- the child in an orange vest, sweaty, pulling at the buckle -->
<g transform="translate(480,1180)"><path d="M-150,-200Q0,-240 150,-200L170,160H-170Z" fill="#f07a1a" {ln(7)}/><path d="M-150,-60h300M-150,40h300" stroke="#f2f2f2" stroke-width="16"/>
<circle cy="-290" r="96" fill="#c98a5e" {ln(6)}/><path d="M-96,-310Q-86,-400 0,-404Q86,-400 96,-310Q40,-350 0,-344Q-40,-350 -96,-310Z" fill="#1e1612"/>
<path d="M-40,-300l24,6M40,-300l-24,6" {ln(6)}/><path d="M-30,-240q30,-16 60,0" fill="none" {ln(5)}/><path d="M80,-330q10,20 0,34" stroke="#bfe8ff" stroke-width="8" fill="none"/>
<rect x="-30" y="-20" width="60" height="44" rx="8" fill="#2a2a2a" {ln(4)}/></g>
<!-- mother's fingers on the buckle (the lure: unclip it) -->
<path d="M1100,1240Q800,1210 520,1170" stroke="#b97c52" stroke-width="54" stroke-linecap="round" fill="none"/><circle cx="510" cy="1168" r="34" fill="#b97c52" {ln(4)}/>
<!-- grandma in the stern, oddly bulky under her shirt (the clue: two vests) -->
<g transform="translate(900,1250)" opacity=".9"><path d="M-70,-140Q0,-170 70,-140L80,60H-80Z" fill="#6a8a5a" {ln(4)}/><path d="M-60,-60h120" stroke="#f07a1a" stroke-width="10" opacity=".8"/><circle cy="-190" r="46" fill="#d8d0c4" {ln(4)}/></g>
"""

for i, (body, c1, cmd) in enumerate([(h1, "ถ้าวันหนึ่ง… ลูกคุณเพิ่งถูกช่วยขึ้นจากน้ำ", "อย่าอุ้มพาดบ่า"),
                                      (h2, "ถ้าวันหนึ่ง… น้องคุณแกล้งจมน้ำอีกแล้ว", "อย่าคิดว่าน้องแกล้ง"),
                                      (h3, "ถ้าวันหนึ่ง… ลูกขอถอดชูชีพบนเรือ", "อย่ายอมให้ถอด")], 1):
    open(os.path.join(OUT, f"hook{i}.html"), "w").write(page(body, c1, cmd, "ฮุก " + str(i)))
print("ok")
