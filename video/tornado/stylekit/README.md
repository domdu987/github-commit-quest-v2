# นาคเล่นน้ำ: style frames kit (owner 4 Nov 2569: "ทำภาพมาก่อน")

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
bash video/tornado/stylekit/build/build.sh <hf dir with lib/> ngw1             # vertical
bash video/tornado/stylekit/build/build.sh <hf dir with lib/> ngwL landscape   # 16:9
```
- `sf/common.part` is the takhian common part with one change: its storm hook (rain, wind, wet actors, hands) also accepts `ngwScape`.
- Snapshots:
  - vertical: `snapV.cjs`
  - landscape: `snapL.cjs`, one browser at a time
