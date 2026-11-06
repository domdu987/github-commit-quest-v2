# ชุด prompt ทำปกด้วย GPT (ChatGPT image)

วิธีใช้ (3 ขั้น)
1. แนบรูปใน `refs/` ที่ตรงกับตอน 1–2 รูป (เช่น `lt-ep1.jpg`) + `example-finished-cover-lt1.jpg` (ให้ดูว่าปกเสร็จหน้าตาแบบไหน)
2. วาง **MASTER PROMPT** แล้วต่อด้วย **บล็อกของตอนนั้น** (ข้างล่าง) ในข้อความเดียว
3. สั่งขนาด: ปกแนวตั้ง `1024x1536` (TikTok/Shorts) · ปก YouTube `1536x1024`
   - GPT มักสะกดไทยผิดหรือฟอนต์เพี้ยน แนะนำสั่งแบบ **ไม่ใส่ตัวหนังสือ** (แบบ A) แล้วไปใส่เองใน Canva/CapCut ด้วยฟอนต์ **Kanit ExtraBold** ตามสเปกท้ายไฟล์
   - ถ้าอยากให้ GPT ใส่ตัวหนังสือเลย ใช้แบบ B แล้วตรวจคำสะกดทุกครั้ง ถ้าผิดให้พิมพ์ว่า "keep everything, only fix the Thai text to exactly: …"

---

## MASTER PROMPT (วางก่อนเสมอ)

```
Create a YouTube/TikTok thumbnail illustration in the exact art style of the attached reference images (my channel's style). Match it closely:

STYLE
- flat 2D vector cartoon, clean shapes, no outlines, soft cel shading, subtle film grain, slight vignette
- Thai characters with tall slim bodies, long thin arms and legs, small hands, oval/round heads, tiny dot eyes, small round open mouths, simple eyebrows; cute but expressive
- cinematic lighting: strong rim light on the hero, soft volumetric glow, long cast shadows, warm/cool colour contrast
- backgrounds: layered depth (far / mid / near), soft gradient sky, slightly blurred far layer
- small round "coin" badges with a gold bevel may float near the hero (optional)
- NOT 3D, NOT photorealistic, NOT anime, NOT Pixar, no text watermark, no logo

COMPOSITION (thumbnail rules)
- ONE hero character very large in frame: face and upper body fill about 60% of the image, head in the upper-middle area, eyes clearly readable
- an exaggerated reaction on the face (shock / panic / smug)
- one clear story prop or effect next to the hero (see the episode block)
- keep the bottom 30% of the image simple and darker (empty space for the hook text)
- high contrast, saturated, punchy; readable at phone size
```

### แบบ A — ไม่ใส่ตัวหนังสือ (แนะนำ)
```
TEXT: none. Leave the bottom third clean for text that I will add myself.
```

### แบบ B — ให้ GPT ใส่ตัวหนังสือ
```
TEXT (render exactly, Thai language, font like "Kanit ExtraBold"):
- top-left: a small dark pill badge with the series name "<ชื่อซีรีส์>" in <สี> and a small red pill "EP.<เลข>"
- bottom: two lines of huge bold hook text with a thick dark outline and drop shadow
  line 1 (white, smaller): "<บรรทัด 1>"
  line 2 (<สี>, much bigger, tilted -2 degrees): "<บรรทัด 2>"
Spell the Thai text exactly as given. Do not add any other words.
```

---

## บล็อกตามเรื่อง (วางต่อท้าย MASTER PROMPT)

### 1) สกิลจอมโกหก · สีประจำเรื่อง เหลือง #FFD84A · refs: `jk-hero.jpg`, `example-finished-cover-jk1.jpg`
```
HERO: a skinny young Thai office man, neat short black hair with one cowlick, big round glasses, navy-blue suit, white shirt, yellow tie, mouth wide open in shock, eyebrows up.
PROP: he holds a big grey "skill card" with a huge letter "F" on it and a red stamp; a small gold crown badge floats beside his head.
SCENE: warm pink-and-cream glow background, the dark silhouette of a dragon looming behind him, a red gacha machine at the bottom corner.
ACCENT COLOUR for text/badges: bright yellow #FFD84A.
```
- EP.1 ตัวหนังสือ (แบบ B): ซีรีส์ "สกิลจอมโกหก" · EP.1 · บรรทัด 1 "ได้สกิลกากสุด" · บรรทัด 2 "แต่ได้ที่ 1!?"
- EP.2: บรรทัด 1 "มีคนเชื่อแค่คนเดียว" · บรรทัด 2 "ได้มังกร 1%!?" (PROP เปลี่ยนเป็น: เด็กหญิงตัวเล็กยกมือข้างเดียว กับไข่มังกรเรืองแสง)

### 2) บางระจัน แบต 3% · สีประจำเรื่อง เขียว #9DFF6A · refs: `br-ep1.jpg`, `br-ep2.jpg`
```
HERO: a Thai teenage boy, messy black hair with a blue cloth headband, blue indigo Thai farmer shirt (mo-hom) with light stripes, tied to a wooden post with many loops of rope, holding a smartphone, face panicking.
PROP: a phone screen showing a red battery icon at 3%.
SCENE: old Siamese village camp (year 1766), tall wooden palisade fence of sharpened logs, warm golden afternoon light, dust in the air; a black water buffalo with its tongue out sniffing him; villagers in red loincloths holding spears in the background.
ACCENT COLOUR for text/badges: lime green #9DFF6A.
```
- EP.1 ตัวหนังสือ: ซีรีส์ "บางระจัน แบต 3%" · EP.1 · บรรทัด 1 "มือถือแบต 3%" · บรรทัด 2 "ติดอยู่ ปี 2309!?"
- EP.2: บรรทัด 1 "ทั้งค่ายกราบมือถือ" · บรรทัด 2 "ขอไก่ย่าง ด้วย!?" (SCENE: ชาวบ้านทั้งค่ายก้มกราบมือถือที่เรืองแสงสีฟ้าในมือเขา)

### 3) ช่างเชื่อมสายฟ้า · สีประจำเรื่อง ฟ้า #8AE8FF · refs: `lt-ep1.jpg`, `lt-ep2.jpg`, `example-finished-cover-lt1.jpg`
```
HERO: a Thai welder man in his 30s, black hair standing straight up in electrified spikes, dark leather welding apron over a blue work shirt, thick welding gloves, face shocked with mouth open, small sparks jumping off his hair.
PROP: a giant jagged lightning bolt striking down from a stormy night sky directly onto him; a blinding white-blue electric flash at his feet; a gold lightning-bolt coin badge floats beside him.
SCENE: rooftop of a small iron-works shop at night, dark blue storm clouds, city lights far away, rain-wet reflections, cool blue light with warm orange highlights from the shop sign.
ACCENT COLOUR for text/badges: ice blue #8AE8FF.
```
- EP.1 ตัวหนังสือ: ซีรีส์ "ช่างเชื่อมสายฟ้า" · EP.1 · บรรทัด 1 "ช่างเชื่อมโดนไฟช็อต" · บรรทัด 2 "เป็นเทพ สายฟ้า!?"
- EP.2: บรรทัด 1 "คนทั้งซอยต่อคิว" · บรรทัด 2 "ขอชาร์จ มือถือ!?" (SCENE: หน้าร้าน "เหล็กดัด เจ๊หงส์" ตอนกลางคืน คนต่อคิวยาวยื่นมือถือ ป้ายลอย 100% สีเขียว เขาชี้นิ้วมีไฟสปาร์กเข้ามือถือ)

### 4) คนเดินดิน (เรื่องใหม่ รอคุณอ่านบทก่อน) · สีประจำเรื่อง ส้ม #FFA33C
```
HERO: a skinny Thai teenage boy, short neat black hair, round glasses, grey school uniform shirt, standing on the ground looking UP with a sad-stubborn face, a small dog beside him.
PROP: a gauge/meter floating beside him reading "0%" in red.
SCENE: a city where everyone flies: dozens of people floating in the sky holding bubble tea, bright blue sky with a giant golden glowing ring high above the clouds, a single rusty iron staircase bolted to the side of a 40-storey tower; the boy is the only one on the ground.
ACCENT COLOUR for text/badges: orange #FFA33C.
```
- EP.1 ตัวหนังสือ: ซีรีส์ "คนเดินดิน" · EP.1 · บรรทัด 1 "ทุกคนบินได้" · บรรทัด 2 "ยกเว้นผม 0%!?"

---

## ปกแนวนอน 16:9 (YouTube) เพิ่มท้าย prompt
```
LANDSCAPE VERSION 1536x1024: put the hero large on the LEFT half (face in the left-centre), keep the RIGHT 45% darker and simpler for the hook text. Same scene, same lighting.
```

## สเปกตัวหนังสือ ถ้าใส่เองใน Canva/CapCut (ตามปกที่ทำไว้)
| ส่วน | แนวตั้ง 1080×1920 | แนวนอน 1920×1080 |
|---|---|---|
| ป้ายซีรีส์ (มุมบนซ้าย) | Kanit 800 · 46 px · ตัวหนังสือสีประจำเรื่อง · พื้นดำ #15101C · ขอบ 4 px สีประจำเรื่อง · มุมโค้ง 22 px | 40 px |
| ป้าย EP (ติดกัน) | พื้นแดง #E8322E · ตัวขาว · ขนาดเดียวกัน | เท่ากัน |
| ฮุกบรรทัด 1 | Kanit 800 · 104 px · ขาว · stroke ดำ 18 px · เงาตก 14 px | 84 px · ชิดขวา |
| ฮุกบรรทัด 2 | Kanit 800 · 170 px · สีประจำเรื่อง · stroke ดำ 28 px · เอียง −2° · เรืองแสงสีเดียวกัน | 140 px · ชิดขวา |
| ไล่เงาดำ | จากล่าง 45% ของภาพ ไปโปร่ง | จากขวา 55% ไปโปร่ง |

สีประจำเรื่อง: จอมโกหก #FFD84A · บางระจัน #9DFF6A · ช่างเชื่อม #8AE8FF · คนเดินดิน #FFA33C

## สิ่งที่ต้องไม่มี (ใส่ท้าย prompt ถ้า GPT เผลอทำ)
```
Avoid: 3D render, photorealism, anime eyes, thick black outlines, more than one big character, busy background behind the face, text other than specified, watermark, blurry face.
```
