# Film 24 version C (turtle_C): relight + hero ship + big explosions (client 2026-11-27)
Client: "ค. แล้วทำให้เรือเต่าเป็นจุดเด่นหน่อย ทำเรื่องเต่าอลังการ ฉากยิงปืนให้ระเบิดแบบอลังการ ใกล้ๆ ร่างภาพมา"
Spec: film/LIGHT_SPEC.md (overrides COLOUR_SPEC for this film). The narration, captions, timing, SFX bed and overlays are UNCHANGED (65.0 s, 1950 frames).
Client checklist still applies: nothing floats, no shake, nothing parented to camera, no sliding, no clones, contact shadows, hard cuts.
Tone: comic and bloodless. Fire and fireballs ARE allowed now (client), but no people are hurt on screen. Sailors jump into the sea comically, or the hull bursts with nobody visible.

## Light per location (LIGHT_SPEC)
- Yard (shots 1, 2, 4, 8a, 8b): late-afternoon/sunset low sun, 8-12 deg, behind or 3/4 behind the subjects.
  - Long mast and rigging shadows and gobo patterns rake across the quay.
  - Lantern and brazier pools on the wharf.
  - Haze with god rays through the rigging and the sheds.
- Sea (all others): golden-hour sun, 6-10 deg, low over the far mountains, mostly back or 3/4 back.
  - Water glitter path.
  - Pastel peach-to-lavender sky.
  - Haze layers.
  - Cannon flashes and fires give warm practical light.
- Colour: saturation 0.28-0.35, warm amber 35-45 % against cool blue/lavender 30-45 %. No flat cyan water: shadowed water goes deep blue-lavender, sunlit water goes amber.
- Cards: add a warm rim (the puppet `rim` key) on the sun side when backlit, with contact shadows as before.

## Shot changes (everything else keeps the shot_plan.md framing and animation, relit)
| shot | t (s) | g | change |
|---|---|---|---|
| 4 | 9.60-14.37 | 288-431 | **HERO 1.** Low-angle slow push-in on the finished turtle ship on the slipway, BACKLIT by the low sun through haze. God rays through the rigging and masts, a rim light on the spike rows and the dragon head (thin smoke curling), long shadows toward camera. Yi small at the foot of the ship, silhouetted with a rim. |
| 13a | 47.10-50.90 | 1413-1527 | aerial U: keep the accepted s13 move (top-down U), relit golden hour. Overlay ✗ marks start later (see overlays). |
| 13b | 50.90-52.00 | 1527-1560 | **CLOSE CANNON FIRE.** Low and close along the turtle ship's gun-port side: ports open, 3-4 muzzle flashes in sequence with smoke rings and a warm flash light on the hull, recoil puff. Camera fixed in the world with a slow slide. |
| 13c | 52.00-53.57 | 1560-1607 | **CLOSE HIT.** A Japanese atakebune takes hits: fireball, flying planks and splinters, water columns, a shockwave ring on the water, the sail and rigging catching fire with embers. Two ashigaru cards leap off the far rail into the sea in a comic arc and splash (no injury). Camera close and low. |
| 14 | 53.57-58.90 | 1607-1767 | **HERO 2.** Slow orbit past the dragon head (smoking) on the moving turtle ship. Background: burning, listing Japanese fleet with smoke columns, embers in the air, and a sun disc behind the smoke giving god rays. Foam wake and oars in rhythm. The top third must stay readable for the tally (1718-1767). |

## Overlays
- The ✗ marks now pop on the hit ships in 13c (the close hit: one big ✗ on the burning ship at about g 1575) and on the visible burning ships in shot 14.
- The aerial 13a has no ✗ marks.
- The tally is unchanged (g 1718-1767, top third).

## Order
1. Kit (film/v3/kit/ + README), relit set3d24 (`J.set_look('C')`, env JOSEON_LOOK=C), the new hero and explosion set-ups and hooks.
2. board_C.jpg: 8-10 look frames at low samples, with real cast24 cards where people are seen. Producer go-ahead before any full render.
3. Re-render all takes in look C (3 teams), conform24 VERSION=C, then release film/release24/turtle_C.mp4.

## UPDATE 2026-11-27 (client on board_C): build-up sequence + new timing
The client asked for a step-by-step "what's on the ship" build-up. The "count" beat is rewritten (Bankky, original settings, STT 1.0), with a 1.2 s hero-pose pause after it:
"แต่อีซุนชิน ยังสร้างต่อ ทีละชั้น ตัวเรือ ไม้สนหนาๆ พายเรียง สองข้าง ปืนใหญ่ เรียงรอบลำ หลังคา กระดองเต่า เหล็กแหลม เต็มหลัง แล้วปิดท้ายด้วย หัวมังกร พ่นควัน"
- The film is now **70.1 s, N = 2104 frames**. Everything up to g 733 is unchanged. Shots 8a/8b (old g 734-918) are REPLACED by the build-up (g 734-1072). Every later shot, caption, SFX cue and overlay shifts by **+154 frames (+5.13 s)**: old g X ≥ 919 becomes X+154.
- Old narration, timing and captions are kept in audio/bk0_v1/ (used by turtle_A / turtle_B).

### Build-up (location `build_dock`, J.set_build(stage,k), slow low orbit build_cam(u), one take s08C, g 734-1072)
| stage | g | narration cue | action | callout label (conform overlay, Kanit) |
|---|---|---|---|---|
| 0 intro | 734-780 | แต่อีซุนชิน ยังสร้างต่อ | Empty dry dock at dusk, keel blocks, lanterns, god rays; camera starts orbit | — |
| 1 hull | 781-829 | ทีละชั้น ตัวเรือ ไม้สนหนาๆ | Keel + ribs slam in, then planks layer on in sweeping waves (thud hits) | ตัวเรือไม้สนหนา |
| 2 oars | 830-861 | พายเรียง สองข้าง | Oars slide out in rhythm, both sides | พาย ข้างละ 8-10 |
| 3 guns | 862-897 | ปืนใหญ่ เรียงรอบลำ | Cannons slide out port by port, muzzle glints, counter ticks to 11 | ช่องปืน ราวข้างละ 11 · ชอนจา จีจา ฮยอนจา |
| 4 roof | 898-931 | หลังคา กระดองเต่า | Hex shell plates drop and lock | หลังคาคลุมทั้งลำ |
| 5 spikes | 932-970 | เหล็กแหลม เต็มหลัง | Spikes pop up row by row, sparkles | เหล็กแหลม กันปีนขึ้นเรือ |
| 6 dragon | 971-1037 | แล้วปิดท้ายด้วย หัวมังกร พ่นควัน | Dragon head bolts on at ~1006, eyes glint, smoke at ~1023 | หัวมังกร พ่นควันบังตา |
| 7 hero | 1038-1072 | (1.2 s pause, music hit) | Complete ship, sun behind, rim on spikes; camera settles slowly (never static > 6 frames) | ไอ้เรือเต่า (title-style) |
- SFX: one punchy hit per stage start (wood slam, oar clack, cannon clunk, plate clank, metal shing, dragon roar/hiss), on top of the yard bed.
- Labels: top 25 % and one side band free; set exports build_anchor(stage) screen points for leader lines. Labels pop on at stage start and stay until the next stage.

### New g for the version C shots (old + 154 where after 918)
13a 1567-1680 · 13b 1681-1713 · 13c 1714-1760 · 14 1761-1920 (tally 1872-1920) · 15 1921-2103.
