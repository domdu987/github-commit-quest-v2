# T3 key still g800 (real cast, 720x1280, 16 samples + OIDN, 95.5 s)
- check_take('T3') hits: [] -> PASS
- check_face('T3'): ok=True -> PASS
- luma mean (PIL 'L') of this still: 86.8 (target 95-110) -> LOW by ~8; fix by lights only if approved
- Issue seen: a translucent diagonal light wedge runs from the lower-left table across Bertillon's torso/coat (shaft on a cast card, violates client rule). Need director call on fix (hide light_shaft in T3 / TAKE_OVER).
- Not seen: back-view slab (Bertillon is mirrored front/3-4 view here; no OTS in T3).

## v2 (director-approved fix): g_0800_key_v2.png
- TAKE_OVER['T3']['measure'] = beam_k 0 (shaft hidden), shade_mul 1.5, fill_w 360, win_w 420, win_lamp 200, lamp_k 1.5, gain 1.12. Lights only; no haze, no saturation change.
- Wedge across Bertillon: gone (viewed). Luma mean 98.7 (target 95-110). 96.7 s/frame.
