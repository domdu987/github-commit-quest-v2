# Film 17: "ไอ้ช่างวัดหู" (Alphonse Bertillon's anthropometry, Paris 1882-1883)
Branch film17/main. Set film/v3/set3d17 (NEW), cast film/v3/cast17 (NEW). Facts and sources: FACTS.md. Music text: SUNO.md.
Same style, pipeline and client rules as films 9-16 (skill reference-style-shorts + production-lessons incl. §10 film-2 camera rhythm; QA_TEAM.md stricter QA).
Narration audio/narration.wav (Bankky RwilAvCC3o05RLuACpAn, speed 1.15 original setting, atempo 1.134); per-sentence STT 0.987-1.000.
Script script/script_th.txt, TTS text script/tts_bankky_orig.json, captions script/captions.json, timing audio/timing.json.
Blind test (Sonnet): v1 7/10 (hook 6, ending 7) -> 3 rewrites (shorter pivot, list cut to หัว นิ้ว เท้า แขน หู + drawers by size, mug-shot lecture cut before the punchline) -> retest 8/10 (hook 7, mechanism 8, ending 8) -> 2 word fixes. Hook "หนีบ" removed (fal content checker flagged it).
Locations (draft): A Paris police records office ("Préfecture" attic): towering card cabinets, gas lamps, ledgers, desks / B measuring room at the Dépôt: measuring chair with head rest, calipers, wall height scale, camera on tripod, queue of prisoners on a bench / C the card-drawer wall reveal (narrowing: big drawer -> box -> one card) / D ending: the chief inspector seated in the measuring chair, calipers on his ear, policemen laughing.
Cast (draft): Bertillon (thin clerk, black frock coat, pince-nez, neat beard), chief inspector (stout, big moustache, kepi/uniform), prefect (top hat, sash), "Dupont/Martin" (scruffy thief, cap), 2-3 gendarmes, prisoners.
Shot planning: also read the style bible on branch claude/new-session-73ou27 commit 38b5918, film/skill/reference-style-shorts/references/bible/camera.md + scene-tricks.md (framing change every 1.3-1.4 s, drift/snap numbers); client overrides in that SKILL.md section win.

## Client decision 2026-11-19 (typed in this chat)
"เรื่อง 17 ไม่ต้องรอผม OK ให้ QA-art อนุมัติแทนแล้วเรนเดอร์ได้เลย และเพลงไม่ต้องรอผม ให้ทำเองด้วย fal.ai (elevenlabs/music/v2.5 แบบ instrumental) ให้ทีมตรวจเลือก"
-> SET gate approval = QA-art (Opus) PASS; send sheets to client as FYI only. Music: fal-ai/elevenlabs/music v2.5 instrumental, QA picks. FINAL gate + sending the finished film + WAIT queue row unchanged.

## v2 remake decision (client, in this chat, 2026-11-20)
"ทำเรื่อง 17 ใหม่" and "ทำใหม่ ตามกฎ G H I ทั้งหมด ใช้ป้ายตัวหนังสือได้ ไม่ต้องรอผม OK ฉาก ให้ QA-art อนุมัติแล้วเรนเดอร์เลย"
-> remake to QA_TEAM §G/§H/§I, text signs allowed, QA-art approves the v2 set on the client's behalf, render without waiting. Plan: film/film17/v2/PLAN_V2.md.
