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
