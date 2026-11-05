"""Style-frame sheet: rows of ทะเลลด (vertical) | เดิม (the delivered film) | ใหม่ (the rework), phone-friendly.
usage: python3 sheet3.py <out.jpg>"""
import sys
from PIL import Image, ImageDraw, ImageFont

S = "/tmp/claude-0/-home-user-github-commit-quest-v2/4f94749f-8122-57a4-aa41-e38e84dcb96c/scratchpad"
F = S + "/rw/hf/rig/assets/fonts/"
fb = lambda n: ImageFont.truetype(F + "f2.ttf", n)
fx = lambda n: ImageFont.truetype(F + "f3.ttf", n)
out = sys.argv[1]
ROWS = [
    ("1. ร้านไก่ย่างยายบัว", "ร้านไก่ย่างจริง: ไก่ไม้หนีบนอนบนตะแกรงเตาถ่าน ยายถือพัดพัดเตา ใต้หลังคามีเงา คนมีเงาบนพื้น", "td1_19", "t11.00", "t11.00"),
    ("2. ความสูง: ปูกับยาย", "ทุกฉากใช้สเกลเดียวกัน: เด็ก 9 ขวบสูงแค่อกผู้ใหญ่ (แบบทะเลลด)", "td1_91", "t20.50", "t22.50"),
    ("3. ใต้สะพาน (ภาพกว้าง)", "สะพานจริง: คาน เสา สูงราว 3 คน · เชิงลาดเป็นคันดินลาด ~35° · คนปีนขึ้นไปหลบใต้คาน (แบบที่เกิดจริง)", "td2_1", "t133.00", "t131.50"),
    ("4. ใต้สะพาน (ภาพใกล้)", "ตัดเข้าใกล้ตอนตาเทียนพูด: ตัวละครใหญ่ขึ้นเกือบเท่าตัว เห็นคานอยู่เหนือหัว", "td2_10", "t134.50", "t134.50"),
    ("5. ฉากลาก", "ปูตัวเล็กกว่าตาเทียนตามจริง · มือจับกันจริง · กล้องเข้าใกล้ขึ้น", "td2_4", "t146.30", "t146.30"),
    ("6. ฉากกอด", "เดิมปูดูสูงกว่ายาย → ยายยืนก้มกอด แขนโอบหลังหลาน หน้าปูซบอกยาย", "td2_7", "t197.00", "t197.00"),
]
VH = 384; VW = VH * 9 // 16; WW = VH * 16 // 9; G = 16; LH = 92
W = VW + 2 * WW + 4 * G
H = 120 + len(ROWS) * (LH + VH + G + 10) + 20
img = Image.new("RGB", (W, H), "#14110e"); d = ImageDraw.Draw(img)
d.text((G, 22), "เสียงรถไฟ · ภาพตัวอย่างฉบับแก้ รอบ 2 (ยังไม่เรนเดอร์ทั้งเรื่อง)", font=fx(44), fill="#ffe2a0")
d.text((G, 78), "ทะเลลด  |  เดิม (ที่ส่งไป)  |  ใหม่", font=fb(28), fill="#c8c0b4")
y = 128
for title, note, td, old, new in ROWS:
    d.text((G, y), title, font=fx(36), fill="#f6efe2")
    d.text((G, y + 46), note, font=fb(24), fill="#9fd88a")
    yy = y + LH
    ims = [(f"{S}/cmp/{td}.png", VW, "ทะเลลด", "#9ec8ff"), (f"{S}/sf/old/{old}.png", WW, "เดิม", "#c8c0b4"), (f"{S}/sf/new/{new}.png", WW, "ใหม่", "#ffd27a")]
    x = G
    for path, w, tag, col in ims:
        im = Image.open(path).convert("RGB").resize((w, VH), Image.LANCZOS); img.paste(im, (x, yy))
        tw = d.textbbox((0, 0), tag, font=fx(30)); bw = tw[2] - tw[0] + 28
        d.rounded_rectangle((x + 10, yy + 10, x + 10 + bw, yy + 56), 10, fill="#000000")
        d.text((x + 24, yy + 12), tag, font=fx(30), fill=col)
        x += w + G
    y = yy + VH + G + 10
img.save(out, quality=86)
print(out, img.size)
