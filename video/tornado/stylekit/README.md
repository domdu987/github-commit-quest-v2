# ทอร์นาโด: style frames kit

## Current: big tornado, no ghosts (`tw/`)
Owner, 4 Nov 2569: "ไม่ต้องเอาผีนะ เอาแบบภัยพิบัติใหญ่ ธอนาโดไม่ใช่พายุงัวช้าง ทำมารูปมา"

Six frames, each 3 s, in `../frames/`:
1. **t1 · ทอร์นาโดมาแต่ไกล.** A wedge-cone tornado under its supercell (stacked plates, clear slot, power flashes) comes across the plains toward the town. Cars have stopped on the highway and people are filming it (the mistake) while ยายบัว yells.
2. **t2 · ถล่มหมู่บ้าน.** Roofs tear off toward the funnel, a pole snaps, and big debris (a car, sheets, planks) flies. ฝน and ปู run.
3. **t3 · หลบห้องน้ำกลางบ้าน.** The windowless inner room. They kneel and cover their heads while dust falls, the door bulges and the bulb swings.
4. **t4 · ห้ามหลบใต้สะพาน.** A grey what-if. Drivers crawl up the embankment under the highway overpass, and the wind and debris rush through the gap.
5. **t5 · หมอบในคูน้ำ.** No building in reach, so ปู lies flat in the roadside ditch with his arms over his head as the tornado passes. The tree and the pickup are far off.
6. **t6 · หลังพายุผ่าน.** A gold after-storm light. The village is flattened and a pole is down; the tornado ropes out in the distance.

New pieces in `src/ngw.js`:
- `Ngw.monster` / `Ngw.monsterLife`
- `Ngw.ruin` (level 1: roof torn; level 2: walls broken)
- `Ngw.debris`, `Ngw.overpass`, `Ngw.streaks`
- `Ngw.pole` / `Ngw.wires`, `Ngw.road`, `Ngw.sign`
- `Ngw.funnel` gained the `tone: "dark"` option.

### v3 additions (owner: "คิดว่าดีเท่าทะเลลดยัง"), using the ทะเลลด grammar
Ten frames in story order: a0, b0, t1, c0, t2, t3, t4, d0, t5, t6. The new ones:
- **a0 · ชีวิตปกติ.** A bright afternoon at ยายบัว's roadside stall: ฝน is live and ปู has his camera. A thunderstorm is building far off.
- **b0 · เสียงครืน.** The warning sign. A loud, continuous roar (Ready.gov: "a loud roar like a freight train"; SPC: "doesn't fade in a few seconds like thunder"). ปู: "เสียงรถไฟ? แถวนี้ไม่มีรางนะ".
- **c0 · กฎของยายบัว.** `TideUI.rule` with three rhyming rules and new coin icons:
  - "ได้ยินครืน อย่ายืนดู"
  - "ห้องใน ไม่ใกล้หน้าต่าง"
  - "หนีไม่ทันตึก หมอบลึกที่ต่ำ"
- **d0 · จะหลบที่ไหน?** `TideUI.choice`: "มุดใต้สะพานทางหลวง" / "หมอบราบในคูน้ำ". The countdown digit is removed (no HUD numbers).

### v4 the epic storm (owner: "ทำพายุให้อลังการกว่านี้")
`Ngw.epic` / `Ngw.epicLife` replace `Ngw.monster` in every storm frame. It returns `{ sky, mid }`, and `Sets.ngwScape` takes it as `o.epic`.

What it draws (`o.sun` sets the side the low sun is on):
- **Sky:** a low sun glowing behind the storm's flank, rain and hail shafts lit gold at their feet, and a lumpy storm body.
- **Mothership:** striated tiers corkscrewing up, each with a gold rim and a dark gap, plus the inflow band, the wall cloud and a cloud-to-ground bolt.
- **Funnel:** horizontal shading so the silhouette stays whole, curved front-face spiral bands, a lit rim on the sun side, a dust sheath, and a collar that hides the join with the cloud.
- **Base:** sub-vortices, a debris fountain with a plume, debris with motion streaks, ground inflow dust and power flashes.

The frames are in `../frames/` as `01`–`10`, each in a vertical and a landscape version.

## v1 นาคเล่นน้ำ (rejected: it had a legend and a small spout) — `sf/`, frames in `../frames/v1-นาคเล่นน้ำ-ไม่ใช้/`

The five style frames in `../frames/` were built from this kit. Each one comes in two versions:
- vertical 1080×1920 (IG/Facebook)
- landscape 1920×1080 (YouTube, via `video/longform/landscape.js`)

## Frames (`sf/body.part`, 3 s each)
1. **f1 · นาคเล่นน้ำกลางบึง.** The waterspout over the lake.
   - ตาเทียน kneels and wais the naga shrine.
   - ฝน livestreams it (live hearts come off her phone) and ปู films it with his camera.
   - The bank crowd holds phones up.
2. **f2 · งวงข้ามนาเข้าหมู่บ้าน.** The landspout has come off the lake and crosses the paddies toward the temple, the houses and the school. ปู is alone in the field, filming it (the EP.1 cliffhanger).
3. **f3 · ห้องน้ำกุฏิ.** The windowless inner room. ยายบัว, ฝน and ตาเทียน are down on their knees with a forearm over the face and a hand over the head (`kCover`). The bulb swings, the door rattles and the storm flashes through the vent.
4. **f4 · ตำนาน.** On the shadow-puppet screen, the naga rises out of the lake as a twisting column into the cloud, its eyes lit. The villagers wai it from the bank.
5. **f5 · ปูหมอบในคูน้ำ.** ปู lies flat in the ditch with his arms over his head (`prone`) while the landspout tears past. A lone tree and a parked pickup stand far off.

## Pieces (`src/ngw.js`)
- `Ngw.funnel` / `Ngw.funnelLife`: the funnel.
  - Kinds: `water` (grey-white rope, spray mound and rings, lotus leaves lifted) or `land` (dusty rope, debris cloud, straw, leaves and roof-sheet bits in orbit).
  - A lowered wall cloud sits over the top.
  - In motion, the bands spin, the rope sways about its top, the base breathes, and the debris orbits. `dx` moves the funnel across the frame.
- `Sets.ngwScape`: the `Sets.tkScape` storm world plus these options:
  - `lake` (lake + bank)
  - `spouts`, `shrine`, `naga` (naga statue), `crowd`
  - `farLake`, `village` (`Ngw.wat` temple, `Ngw.school`, `Tk.house`)
  - `ditch`, `far`, `props`
- `Sets.ngwKuti` + `Ngw.kutiLife`: the kuti bathroom.
- `Sets.ngwLegend`: the puppet legend, built on `Sets.legend3`.
- Cast:
  - `fon`/`fonPhone`: yellow raincoat, ponytail
  - `pu`/`puCam`: bucket hat, striped tee, camera
  - `yaiBua`: lotus blouse, green sarong
  - `taTian`: khaki shirt, white moustache, red-check ผ้าขาวม้า over the shoulder

## Build
```bash
bash video/tornado/stylekit/build/build.sh <hf dir with lib/> ngw1 vertical tw    # vertical
bash video/tornado/stylekit/build/build.sh <hf dir with lib/> ngwL landscape tw   # 16:9
```
- `sf/common.part` is the takhian common part with one change: its storm hook (rain, wind, wet actors, hands) also accepts `ngwScape`.
- Snapshots:
  - vertical: `snapV.cjs`
  - landscape: `snapL.cjs`, one browser at a time
