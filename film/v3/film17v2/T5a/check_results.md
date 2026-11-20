# T5a checks (take T5)
- check_take('T5'): hits = [] -> PASS
- check_face('T5'): ok = True -> PASS (inspector max err 5.1 deg, strict-window 1.6 deg)
- key still g1150 (720x1280, 16 spl, OIDN, real cast via stage_cast2): key_g1150.png, mean luma 82.4 (target 90-108)

## Fix round 1 (director fix list): t5a_override.py
- Camera override for g1100-1196, blend to the prepared path over g1196-1210 (g1211 == prepared), lights: ARCHIVE_NIGHT fill_w 110->230, lamp_k 0.75->1.0, gasolier_k 0.4->0.7 (in-process, K.LIGHTS).
- check_take hits [] PASS; check_face ok PASS (inspector 6/3 deg).
- Inspector %H: g1128 27.2, g1135 36.1, g1150 42.4, g1160 44.3, g1190 47.0. Camera speed max 5.9 m/s in 1111-1196.
- Stills: fix_g1150.png (luma 99.4), fix_g1180.png (luma 95.6).
