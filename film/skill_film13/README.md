# The skill exactly as it was when films 1-13 (up to ไอ้แม่แรง) were made

The client decided on 2026-11-21: "กลับไปใช้สกิลที่ทำคลิป 1 ถึง ไอ้แม่แรง".
- `reference-style-shorts/` is film/skill at commit a456d12 (2026-11-18), the last skill change before film 13 was released (074b429, 2026-11-19).
- `QA_TEAM_film13.md` is QA_TEAM.md as it was at film 13. The later sections §G to §L are NOT part of this workflow.

Directors follow THIS folder, not film/skill/ (that one was upgraded to v3 after film 13).
Keep the client's standing decisions made later:
- Music is made on fal.ai (elevenlabs/music/v2.5).
- QA-art approves the look.
- Text signs are allowed.
- Queue rows stay WAIT.
- Keep at most 3 render teams.
- Run the free automatic scripts (qa_auto, ground check, qa_jitter) on every take.
