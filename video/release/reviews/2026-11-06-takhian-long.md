> สำเนาใน repo: หลักฐานภาพอยู่ที่ `video/release/reviews/takhian-long-evidence/` (ในรายงานเรียกว่า `evidence/`) · ไม่ได้ใส่โฟลเดอร์ band-10fps และ sheets-1fps

# Review: ต้นตะเคียนกลางนา ฉบับเต็ม (16:9 long), lane C

- **File:** `prod/lane-c` @ `995741b`, `video/takhian-long/LONG-takhian-16x9-share.mp4`
- **Slot:** 9 Nov 2569, 09:30. Due final 8 Nov, 22:00 Bangkok.
- **Reviewer:** โต๊ะตรวจ (independent; I did not make this video).
- **Reviewed:** 6 Nov 2569 (Bangkok). Every finding below comes from the real file, extracted with `git show 995741b:…`.
- **Read-only:** nothing in the repository was committed, pushed or edited.
  - The `git fetch` with the given refspec was rejected (non-fast-forward of the stale tracking ref), but `995741b` was already local and is the remote tip (`git ls-remote`).
- **Evidence folder:** `/tmp/claude-0/-home-user-github-commit-quest-v2/4f94749f-8122-57a4-aa41-e38e84dcb96c/scratchpad/review/takhian-evidence/`. Below, `evidence/` means that folder.

---

## Verdict: **NOT READY**

The file's technical checks all pass: hash, format, loudness, hiss, black/freeze and flashes. It is held back by picture problems that 16:9 exposes, by a chapter list that YouTube will reject, and by the paired gate:

| # | Blocker | Where |
|---|---|---|
| B1 | The cab POV set is still a vertical panel; the field shows at full height on both sides of it | 1:40.07–1:41.55, 1:43.93–1:45.68, 3:29.75–3:33.23 |
| B2 | The ambulance and stretcher are about ⅓ of their correct size next to the people, in the closing image | 3:56.13–4:00.30 |
| B3 | The tree that the caption and voice name is not in frame at all | 2:51.40–2:57.76 |
| B4 | The caption box sits on ลุงเปี๊ยก's mouth and chin at "ไม่หายใจ" | 2:26.11–2:29.72 |
| B5 | Four of the eight reported band fixes still cut off the tree crown or the lightning, including the hook | 0:02.63–0:04.68, 1:41.55–1:53.78 |
| B6 | UPLOAD.md's last chapter is 6.9 s long, so YouTube will not create chapters | description |
| B7 | Paired gate against ทะเลลด: เท่า / **แย่กว่า** / **แย่กว่า** (charter §4 requires เท่าหรือดีกว่า at all 3 points) | peak shot, EP.2 twist |

B1–B6 are mechanical fixes: band and y0 changes, re-staging three cab shots, one asset scale and two text lines. They fit before 8 Nov 22:00.

B7 overlaps B5 for the peak. For the twist, it needs a small plant and a short flashback (see the fixes). Charter §4 makes the gate a review requirement; the coordinator decides whether to require it for a story whose Shorts are already posted.

---

## Blockers (must fix before posting)

### B1: Cab POV shots show set edges (the cab is still a vertical panel)

- **Where:** three shots, 6.7 s in all.
  - `truck` 1:40.07–1:41.55: "ทุกคนมาถึงรถ… ยกเว้นลุงเปี๊ยก".
  - `noo` 1:43.93–1:45.68: "ลุงเปี๊ยก อย่าไป!".
  - `rule3` 3:29.75–3:33.23: "ยังไม่ครบสามสิบ อย่าเพิ่งออกโล่ง!".
- **What is wrong:**
  - The cab interior (windshield, dashboard, ยาย and เดือน from behind) fills only x ≈ 525–1395 of 1920, about 45 % of the width.
  - Left and right of it, the outdoor field and sky (the rainbow in `rule3`) run the full frame height, down past the dashboard to seat level, where the doors and cab floor should be.
  - The windshield rain streaks stop at the cab's edge. It reads as a floating panel pasted on a landscape.
  - Cut points measured from luma steps: 100.067 s and 209.75 s.
- **Why it matters:**
  - Set edges inside the 16:9 frame are a named review failure.
  - Two of these shots carry key story beats: ลุงเปี๊ยก going back, and rule 3 in action.
- **Fix:**
  - Build the cab interior to 16:9: A-pillars, side windows or doors and a full-width dashboard.
  - Or scale the cab layer so it covers 1920 px (crop the top and bottom of the windshield).
- **Evidence:**
  - `evidence/B1-cab-set-edges.jpg` (1:40.50, 1:44.60, 3:31.20, 3:32.80).
  - `evidence/band-10fps/sheet-cab.jpg` (99.9–101.6 s at 10 fps).

### B2: Ambulance and stretcher at the wrong scale, in the closing image

- **Where:** `truth`, 3:56.13–4:00.30. Captions: "นางไม่ได้เอาตัวใครไปหรอก… / ฟ้าต่างหาก".
- **What is wrong** (measured on the 3:58.50 frame, 1080p):

  | Object | Measured | Correct size |
  |---|---|---|
  | Van ambulance | ≈ 265 px tall: roof y ≈ 357, wheel contact y ≈ 622 | ≈ 690 px (allowing for its depth) |
  | ยาย, rescuer, เดือน (standing, feet y ≈ 700–710) | ≈ 560, ≈ 625 and ≈ 595 px | — |
  | Stretcher | ≈ 420 px long | Longer than an adult is tall (≈ 600 px) |
  | ลุงเปี๊ยก lying on it | ≈ 370 px long | About adult height (≈ 600 px) |

  - SKILL V12 gives a van ambulance as 2.3–2.7 m, which is 1.4–1.6× a 1.65 m adult.
  - The van's wheels sit only ≈ 80 px higher than the people's feet, about 1.2× their distance, so it should read about 690 px tall. It is about 2.5–3× too small.
  - Lying on the stretcher, ลุงเปี๊ยก is about 0.6× the standing adults.
- **Why it matters:**
  - This is the same class of error that failed another long (a grandmother 4–5× the height of nearby cars and people).
  - The owner has complained about ambulance proportions before (SKILL V12).
  - It is the film's last story image, under the twist line.
  - The posted vertical EP.2 hides it: only the front half of the van shows there. The 16:9 frame shows the whole van beside the group.
- **Fix:**
  - Scale the ambulance about 2.6× with its wheels on the same ground band as the people, or move it well back toward the horizon.
  - Make the stretcher at least as long as an adult is tall, and draw ลุงเปี๊ยก at adult scale.
- **Evidence:** `evidence/B2-ambulance-scale.jpg` (left: the long with measurements; right: the posted Shorts EP.2 at 1:50.80).

### B3: The tree named by the caption and voice is not in frame

- **Where:** `drag` 2:51.40–2:54.97 and `no` 2:54.97–2:57.76, 6.4 s in all.
  - Captions: "ลากลุงไป[ใต้ต้นไม้]ก่อน / ฝนจะได้ไม่โดน" and "[ไม่ได้]ยาย! / ต้นนั้นแหละที่ผ่า!".
- **What is wrong:**
  - No tree appears anywhere in the 1920×1080 frame; only the field and the three characters.
  - Lane C's own snapFit sheet `fit/fit_05.jpg` shows the shrine and trunk above the red band (drag at 172.47 s, y0 = 570; no at 177.06 s, y0 = 546).
  - The miss was visible to the lane but was not among the 8 fixes.
- **Why it matters:**
  - Charter §4, added 6 Nov: anything the caption or voice names must be in frame.
  - This is the "don't move the victim under the lone tree" lesson, and "ต้นนั้น" points at nothing.
- **Fix:** move the band (y0 ≈ 300–350) or re-place the tree in the landscape layout so the shrine and trunk sit at the top right, as in the vertical.
- **Evidence:** `evidence/B3-drag-no-tree-missing.jpg`.

### B4: Caption box covers ลุงเปี๊ยก's face at "ไม่หายใจ"

- **Where:** `still`, 2:26.11–2:29.72. Captions: "ไม่ตอบ" / "[ไม่หายใจ]" / "หัวใจอาจหยุดไปแล้ว".
- **What is wrong:**
  - ลุงเปี๊ยก lies face-up at the bottom of the frame, and the caption box sits on his mouth and chin, covering the lower half of his face at 2:26.60 ("ไม่ตอบ") and 2:27.60 ("ไม่หายใจ").
  - In the posted vertical EP.2 (0:19.40 and 0:20.40) the caption sits well below his face.
  - Lane C's band for this shot is y0 = 0 (`fit/fit_04.jpg`), which puts his face exactly in the caption zone.
- **Why it matters:**
  - SKILL V9: "ซับอยู่ในกรอบปลอดภัย ไม่บังหน้า".
  - This is the beat where the viewer must see that he is not breathing: the closed eyes and still mouth.
- **Fix:** lower the band (y0 ≈ 150–250) so his face sits above the caption zone, or raise this shot's caption.
- **Evidence:** `evidence/B4-still-caption-on-face.jpg`.

### B5: Four of the eight reported 16:9 band fixes do not put the tree and lightning fully in frame

What the file shows, against Lane C's own previews (`fit/fixed-cmd.jpg` and `fit/fixed-shots.jpg`, which match the file):

| Shot | Time | Band | In the 16:9 frame |
|---|---|---|---|
| `cmd` (the hook) | 0:02.63–0:04.68 | y0 = 420 | Trunk, ribbons, shrine and the bolt running down the trunk with sparks at the base. **The whole crown and the strike point are above the frame.** |
| `rope` | 1:41.55–1:43.93 | y0 = 400 | Trunk, shrine, buffalo and ลุงเปี๊ยก. **The crown and the two purple sky bolts (1:42.74, the warning as he walks back) are out.** |
| `strike` | 1:45.68–1:51.34 | y0 = 330 | At the strike (1:45.93) the lower crown and the bolt on the trunk are in, **but the crown top and the bolt's entry are cut**. From about 1:48.5 the crown is out (branches only). |
| `taken` | 1:51.34–1:53.78 | y0 = 300 | Trunk, shrine and the three characters. **The crown is out.** |
| `why` | 0:06.95–0:11.06 | y0 = 250 | Whole tree, both people under it. Pass. |
| `sci2` "ฟ้าผ่ายอดไม้" | 0:49.78–0:54.89 | y0 = 230 | Crown, bolt at the top and the side flash to the man. Pass; the crown top touches the edge. |
| `shelter` "รถหลังคาเหล็ก" | 1:09.99–1:17.08 | y0 = 300 | Hut, house (1:13.5) and pickup with the bolt (1:15.5–1:16.5) all fully in. Pass. |
| `again` (climax) | 3:33.23–3:40.00 | y0 = 230 | Crown, bolt and ต้น in. Pass; the crown top touches the edge. |

- **Why it matters:**
  - The brief and charter ask for the tree and lightning fully in frame at these shots.
  - At `cmd`, the first image that answers the command "อย่าวิ่งไปหลบใต้ต้นตะเคียน" shows a trunk, not a lone tall tree struck from the sky. That is the whole idea of the film, inside the first 3 s.
  - At `rope`, the dramatic irony (lightning flickering over the tree as ลุงเปี๊ยก walks to it) is invisible.
  - The lane's own previews show the crown outside the band, so these shots were accepted as fixed without meeting the bar.
- **Fix:** the tree, from crown to base, plus the people is taller than one 1350-px band, so y0 alone cannot fix this. Re-stage the landscape versions:
  - Camera scale about 0.8 on the widened world; or
  - Move the tree down or the people up; or
  - In `cmd` and `strike`, a quick tilt from the struck crown to the base.
  - For `rope`, y0 ≈ 150 keeps ลุงเปี๊ยก and puts the sky bolts in.
  - This also lifts gate 2.
- **Evidence:**
  - `evidence/B5-hook-crown-and-rope-lightning.jpg`.
  - `evidence/band-10fps/top-edge-strips.jpg`: the top 240 px of 9 frames.
  - `evidence/band-10fps/sheet-cmd.jpg`, `sheet-rope.jpg`, `sheet-strike.jpg`, `sheet-again.jpg`.
  - `evidence/C5-band-pass-why-sci2-shelter-again.jpg` (the 4 that pass).

### B6: Chapter list breaks YouTube's 10-second rule, so no chapters will appear

- **Where:** UPLOAD.md, description, last line "4:01 กฎ 3 ข้อของยายหอม".
- **What is wrong:**
  - The film is 247.87 s long, so the last chapter runs 4:01 → 4:07.87 = **6.9 s**.
  - YouTube needs every chapter to be at least 10 s, or it creates no chapters at all.
  - UPLOAD.md's note "ทุกช่วงยาวเกิน 10 วิ" is wrong for this line. All other chapters run 13–49 s.
- **Fix:**
  - Delete the 4:01 line, or fold it into the 3:47 chapter ("ความจริงของต้นตะเคียน · กฎ 3 ข้อ").
  - Also change "3:34 ฟ้าผ่าซ้ำที่เดิม" to **3:33**: the strike flashes at 3:33.48, so 3:34 lands half a second after it.

### B7: Paired gate against ทะเลลด fails at 2 of 3 points

See the paired gate section below: (1) เท่า, (2) **แย่กว่า**, (3) **แย่กว่า**. Charter §4 requires "เท่าหรือดีกว่า" at all three points.

**Cheapest path to "เท่า":**

- **Peak:**
  - Fix B5 for `again` and `strike` so the crown and the bolt's origin are in frame.
  - Add a closer second angle of the crown being hit, and hold the burning trunk about 0.5–1 s.
  - Add a short build before the strike: hair rising, a sizzle.
- **Twist:**
  - Plant the photo: put a small framed photo in the shrine in EP.1 (`buff` 0:22.7–0:28 and `sci1` 0:44.6–0:49.8), and make the `photo` shot's interior match the red-gold spirit house.
  - Replace the static ยาย close-up in `grand` (3:52.3–3:56.1) with a 3–4 s sepia flashback: the photo comes alive, the young grandfather shelters under the tree, and the strike.

---

## Minor notes (would improve, not blocking)

Evidence: `evidence/M-minor-notes.jpg`.

**Framing**

1. **`hut` 1:01.49–1:03.64:** the top edge cuts the เถียงนา roof (eaves visible, ridge out) while the caption says "มีหลังคา!". The whole hut is shown from 1:05.4.
2. **`joke` 0:40.82–0:44.56:** the top edge cuts ลุงเปี๊ยก's raised hands at 0:43.6.
3. **`speak` 2:33.71–2:37.24:** the phone on speaker, named in "เปิดลำโพงวางไว้ข้างตัว", is cut at the top, so "1669" is unreadable from about 2:35. ลุงเปี๊ยก's face is cut at the nose. (1669 reads clearly in `phone`, 2:30–2:33.7.)
4. **`fear` 2:11.67–2:14.09:** ลุงเปี๊ยก's head touches the left edge, and the corner badge "ต้นตะเคียนกลางนา" overlaps his chin.
5. **`sci1` 0:44.56–0:49.78:** "ต้นไม้สูงต้นเดียว… คือที่ที่ฟ้าชอบผ่าลง" plays while the crown top touches the top edge, so the tree's height does not read.
6. **`tired` 3:03.35–3:05.03 and `e2_joke` 3:09.70–3:13.03:** the caption box touches ลุงเปี๊ยก's chin, though it does not cover his eyes or mouth.
7. **`leg1`/`leg2` 0:28.00–0:40.82:** the shadow-puppet screen is a vertical panel, about 42 % of the width, centred in a dark room for 12.8 s, so it reads as pillar-boxed vertical video. A wider screen would use the 16:9 frame.
8. **`e2_buff` 3:18.17–3:20.03:** the buffalo ("ควาย!") is a dark lump behind the trunk, its head hidden.

**Continuity**

9. **`photo` 3:46.55–3:50.26:** "รูปในศาล" is never set up. The shrine holds only two dolls at 0:25.6, 0:46.5 and 3:42.2 (`evidence/G3-shrine-no-photo-setup.jpg`), and the photo's dark wooden wall does not match the red-gold spirit house. This is part of the B7 fix.
10. **`rule3` cab POV 3:31.2:** the hanging timer reads 12:40, while the watch insert 3 s earlier counts 12:04–12:07. The shot comes from EP.2 unchanged.

**Packaging**

11. **No end card.** The film ends on a walking wide shot; the last caption is at about 4:05.9. The ทะเลลด long ends on its own "ทะเลลด / ตอนจบ" card. A 1–2 s end title would close it.
12. **Thumbnail `thumb.jpg`:** the title "ต้นตะเคียนกลางนา" covers ลุงเปี๊ยก's head, and the tree crown is cut. Not part of this check list.

---

## Check table

| # | Check | Result | Evidence (from the real file) |
|---|---|---|---|
| 1 | sha256 and size | **PASS** | 94,633,065 B; sha256 `e0364d7481868e512f13fdda216e3169b0b2498cb8a81e1213765c1ba94b95fb`. Both match the report. `day-2026-11-09.json` still has `commit`/`video_sha256` = null (`in_production`). |
| 2 | Format, rate, frames, A/V | **PASS** | 1920×1080 h264 High yuv420p · r_frame_rate 60/1 (avg 60/1) · nb_frames 14872 (a full decode also counted 14872) · video 247.866667 s vs audio 247.866000 s (Δ 0.0007 s) · AAC LC 48 kHz stereo 192 kb/s |
| 3 | Hook "อย่า…" within 3 s | **PASS** | See the hook detail below the table |
| 4 | Picture: 1 fps sheets, black/freeze, defects | **FAIL** | See the picture detail below the table. Fails on B1, B2 and B4. |
| 5 | 16:9 band check | **FAIL** | 4 of the 8 fixed shots pass (why, sci2, shelter, again); cmd, rope, strike and taken do not (B5). Extra misses: the tree in drag/no (B3), the caption on the face in still (B4), plus minor notes 1–5. |
| 6 | Sound | **PASS** | See the sound detail below the table |
| 7 | Flashes (V1b) | **PASS** | See the flash detail below the table |
| 8 | UPLOAD.md | **FAIL** | See the UPLOAD.md detail below the table. Fails on the last chapter (B6). |
| 9 | Paired gate vs ทะเลลด | **FAIL** | (1) เท่า · (2) แย่กว่า · (3) แย่กว่า. See below. |

**Check 3, hook:**
- `hookcheck.py` was run on the long's own `full/schedule.json`, with `lines.json` built from its captions (the long's folder has no `lines.json`): **PASS**.
  - Narration starts at 0.15 s: "ถ้าวันหนึ่ง… / คุณติด[พายุ]กลางทุ่งนา".
  - The command `{อย่าวิ่งไปหลบใต้ต้นตะเคียน}` starts at 2.63 s in a red box, and is visible in the 2.70 s and 2.90 s frames.
  - First shot 2.63 s.
- The voice-band RMS rises from −39 to −9 dB at 2.62–2.70 s.
- Whisper (faster-whisper medium) on 2.55–4.75 s heard "อย่าวิ่งไปหลบใต้ต้นตะเขียน". The posted Shorts reads "…ตะเขียด", so this is an ASR limit; "อย่าวิ่ง" is clear.

**Check 4, picture:**
- 248 frames (t = k + 0.5 s), each 480×270, on 21 sheets (`evidence/sheets-1fps/`). I looked at all of them, then at full 1080p frames for every suspect.
- blackdetect (d ≥ 0.3 s, pix_th 0.06): **none**. freezedetect (n 0.001, d ≥ 3 s): **none** (`evidence/logs/black-freeze-detect.log`).
- No garbled or broken frames.
- Bridge joins at 1:58.13 and 2:11.67 are consistent (`evidence/C4-bridge-joins.jpg`): เดือน kneels by ลุงเปี๊ยก on both sides of the first join, and the scorched trunk is on the card.
- No clicks at the joins.

**Check 6, sound:**
- ebur128 (peak=true): **−14.3 LUFS** integrated, true peak **−2.7 dBFS**, LRA 2.6 LU (`evidence/logs/ebur128-summary.txt`).
- `hisscheck.py` on the share (no `--vo`): flatness 0.37, pause HF median −83.8 dBFS → **PASS** (`evidence/logs/hisscheck.txt`).
- musiccheck: **not run (no stems in repo at 995741b; only `full/vo/x01–x03.wav` and `mix.py`); lane reported PASS** (−34.2 / −28.7 / 19.5 LU / 4 %).

**Check 7, flashes:**
- Per-frame mean luma on all 14872 frames found **10** short full-frame flashes, identical to the lane's list: 2.73, 26.00, 49.98, 70.50, 88.68, 105.93, 118.75, 171.82, 213.48 and 224.70 s.
- Gaps between flashes run 11.2–53.1 s, so the worst 10 s window holds **1**, and the worst 1 s window holds 1 rising edge (the limit is 3 per second).
- The brightest frame is 144.5/255 (213.48 s); no frame is above 150, so there is no white-out.
- Other luma steps are cuts or lighting changes inside a shot:
  - 204.40: cut to the watch insert.
  - 221.75 and 224.10: the bright scars close-up, then the dark storm insert.
  - 232.27: the grand close-up.
  - 100.57: a +10 glare on the cab windshield, local rather than full-frame.
- Evidence: `evidence/C7-flash-luma-timeline.png` and `evidence/logs/flash-analysis.txt`.

**Check 8, UPLOAD.md:**
- Title "ติดพายุกลางทุ่งนา… อย่าวิ่งไปหลบใต้ต้นตะเคียน | ต้นตะเคียนกลางนา ฉบับเต็ม" follows the format, is 73 characters and has no hashtags ✓.
- Chapters start at 0:00 ✓. **The last chapter is 6.9 s** ✗ (B6).
- Spot-checks against the picture:
  - 0:28 → `leg1` at 28.00 ✓.
  - 2:25 → `call` at 144.27, "ลุง!" then "ไม่ตอบ" ✓.
  - 3:14 → `clear` at 193.03, rainbow and ambulance ✓.
  - Extra: 3:34 → lands 0.5 s after the strike at 213.48 (use 3:33).
- The pinned comment has sources: NWS Lightning Safety, Myths, Tips and Outdoors, and Ramathibodi for CPR ✓.

---

## Paired gate (ทะเลลด ฉบับเต็ม `f22ec60` vs ต้นตะเคียน ฉบับเต็ม `995741b`)

### 1. First 3 s: **เท่า**

Evidence: `evidence/gate1-first3s.jpg`.

**ทะเลลด:**
- 0–1 s: the engraved title "ทะเลลด EP.1" under water.
- Between 1 and 2 s: the water drains to sand and fish appear (the lure).
- About 3.0 s: red box "อย่าลงไปเก็บ" over a close fish.
- Quiet, clean and curiosity-led. The subject (the bay drawing back) is fully readable.

**ต้นตะเคียน:**
- Frame 1 is a living scene: 4 characters and a dog on the dike, with the shrine, ribbons and the in-world title sign behind them in a storm.
- Cut at 2.63 s; a lightning strike flashes at 2.73 s and the characters flinch.
- The red command lands at **2.63 s**, about 0.4 s earlier than ทะเลลด's.

**Why equal:**
- Better pace and action than ทะเลลด, but weaker subject clarity: the command is about a lone tall tree, and the frame shows only the trunk, with the crown and strike point cut (B5).
- The dark, busy frame is also harder to read on a phone than ทะเลลด's two-colour image.
- With the `cmd` crown in frame this would be **ดีกว่า**.

### 2. Peak shot: **แย่กว่า**

Evidence: `evidence/gate2-peak.jpg`.

**ทะเลลด, 2:53–2:55:**
- The second wave rises from a line to a wall over about 2.3 s, behind and over the palm crowns.
- It spans the full width; the wall was widened for 16:9.
- Red "ใหญ่กว่าเดิม".
- The threat dominates the frame for seconds. It is the thumbnail image.

**ต้นตะเคียน, `again` 3:33.23–3:40 (the climax):**
- The idea is good: a strike from a clear, rainbow sky right after the storm "ended".
- But the shot is weaker:
  - The tree occupies only the upper-middle third of a wide shot, and its crown top touches the frame edge.
  - The bolt is a thin line that stays bright for about 0.13 s (the flash at 3:33.48).
  - Most of the shot is ต้น sitting in the field under a knowledge caption ("16–24 กิโลเมตร").
- The EP.1 strike on ลุงเปี๊ยก (1:45.93), the other candidate and the thumbnail source, has its crown and bolt entry cut (B5).

**Why worse:** less scale, less hold time and less spectacle than ทะเลลด's wave. The concept is not the problem; staging and framing are (see B5/B7 fixes).

### 3. EP.2 twist: **แย่กว่า**

Evidence: `evidence/gate3-twist.jpg` and `evidence/G3-shrine-no-photo-setup.jpg`.

**ทะเลลด, 3:04–3:13:**
- After the shop is smashed ("ร้านยาย! ไม่นะ!"), "ยายพร❤️: ยายอยู่ชั้น 5 โรงแรม" pops into จูน's live.
- Then VO "ยายพิมพ์เป็นแล้ว!… ยายอยู่ชั้นห้า… ที่โรงแรม!" and a push-in on the hotel.
- It is planted in EP.1 (จูน made ยาย an account and taught her the heart) and pays off ยาย's rule "หนีไม่ทัน ขึ้นชั้นสูง".
- Despair turns to relief, delivered with an in-world device, then dread again (wave 3, the live stream dies).

**ต้นตะเคียน, 3:13–4:00:**
- Calm and a rainbow after the storm. ต้น runs off for the buffalo, ยาย checks the watch (12 min), and the tree is struck again (3:33.48). ต้น is knocked down but alive ("ผม… ยังอยู่ครับ", 3:40).
- Then old burn scars on the trunk, the shrine photo "ตาของหนู", "สามสิบปีก่อน เขาหลบฝนใต้ต้นนี้", and "นางไม่ได้เอาตัวใครไปหรอก… ฟ้าต่างหาก".
- Strong idea: the legend becomes lightning, and ยายหอม has a personal stake.

**Why worse:**
- **Not planted:** the shrine shows only two dolls, never a photo, before 3:46, and the photo's room does not match the shrine.
- **Told, not shown:** a still sepia photo (5.7 s) and a 3.9 s static close-up of ยาย under narration.
- **Short scare:** ต้น's danger resolves in about 6.5 s (strike 3:33.48, "ผม… ยังอยู่ครับ" 3:40.00).
- **Rule as a warning, not a payoff:** ต้น survives by luck after breaking rule 3. ยาย in ทะเลลด survives *because* she followed the rule.

**Fix (B7):** plant the photo in EP.1's shrine shots and replace the static `grand` close-up with a 3–4 s flashback. That would likely reach **เท่า**.

---

## Method notes

- **Tools:** ffprobe/ffmpeg 6.1.1; the skill's `hisscheck.py` and `hookcheck.py`; my own scripts for 1 fps and 10 fps sheets, top-edge strips, luma per frame and annotated evidence (in `…/scratchpad/review/tools/`); faster-whisper medium for the voice.
- **Reference:** ทะเลลด ฉบับเต็ม from `f22ec60:video/tide-long/LONG-tide-16x9-share.mp4` (5:28.75, 19725 frames).
- **Vertical comparisons:** the posted Shorts HQs (`video/release/hq/takhian-ep1-HQ-m2.mp4`, `takhian-ep2-HQ-m2.mp4`) and Lane C's own snapFit sheets (`fit/`), which show this build's full vertical frame with the 16:9 band.
- **Not run:** edgecheck needs the HTML build, which is not in the repo; captions were checked by eye on all 248 frames, and none are cut by the frame edge. musiccheck needs stems (see check 6).
