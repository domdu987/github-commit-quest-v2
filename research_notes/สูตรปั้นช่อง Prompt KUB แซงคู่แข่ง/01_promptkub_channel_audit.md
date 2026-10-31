# Prompt KUB (@promptkub / พร้อมท์ครับ) — Channel Audit, snapshot 2026-10-31

Legend used throughout: **[FH]** = first-hand from the platform page itself (date given); **[OWNER]** = claimed by the channel owner on ygnos.com sales pages (Instagram Graph API screenshots/figures as quoted there); **[3P]** = third-party tracker/blog; **[DERIVED]** = computed by the researcher from the cited numbers (method stated). Thai Buddhist year 2569 = 2026 CE.

## Q0. How was the channel measured, and which numbers are first-hand vs. claimed?

### Takeaway
Instagram (the main channel) cannot be read directly (login wall / HTTP 429), but Instagram's public embed pages return the account header (posts, followers), per-reel likes, comment counts and captions, so a small set of first-hand IG numbers exists; YouTube and TikTok were measured first-hand via rendered pages and the public RSS feed; every tracker (Social Blade, ViewStats, NoxInfluencer) was blocked or empty, so all view totals and the growth curve for Instagram are owner-claimed (ygnos.com) unless marked otherwise.

### Cited Findings
- Instagram profile embed (rendered 2026-10-31) header: "promptkub · PromptKUB · 241K followers • 148 posts" [FH] — [instagram.com/promptkub/embed/](https://www.instagram.com/promptkub/embed/); the reel embeds fetched the same day show "148 posts · 242K followers" [FH] — [reel Den1l8AO-a1 embed](https://www.instagram.com/reel/Den1l8AO-a1/embed/captioned/).
- Direct Instagram profile fetch returns only the login page ("Create an account or log in to Instagram"), both as plain HTTP and in a headless browser [FH, 2026-10-31] — [instagram.com/promptkub](https://www.instagram.com/promptkub/).
- YouTube About page rendered 2026-10-31: "Promptkub", @Promptkub, channel ID UCnpJKj1chdaFWdFQj5BX5EQ, "33.8K subscribers", "47 videos", "1,414,039 views", "Joined Aug 13, 2025", country "Thailand", description "Contact for business inquiry: business@ygnos.com | Line ID: @promptkub" [FH] — [youtube.com/@promptkub/about](https://www.youtube.com/@promptkub/about).
- YouTube public RSS feed (fetched 2026-10-31) lists the 15 most recent uploads with exact timestamps, view counts, like counts and descriptions [FH] — [feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- Social Blade returned HTTP 403 for all three profile pages (YouTube handle, Instagram user, TikTok user), so no tracker history is available — [socialblade.com/youtube/handle/promptkub](https://socialblade.com/youtube/handle/promptkub), [socialblade.com/instagram/user/promptkub](https://socialblade.com/instagram/user/promptkub), [socialblade.com/tiktok/user/promptkub](https://socialblade.com/tiktok/user/promptkub).
- ViewStats page for @promptkub rendered with empty "Subscribers"/"Total Views" fields ("@undefined/channelytics") [3P, 2026-10-31] — [viewstats.com/@promptkub](https://www.viewstats.com/@promptkub); NoxInfluencer shows only "--"/0 placeholders behind "Please upgrade your plan" [3P] — [noxinfluencer.com](https://www.noxinfluencer.com/youtube/channel/UCnpJKj1chdaFWdFQj5BX5EQ).
- The ygnos.com course/brand pages state their numbers come from "Instagram Graph API ของบัญชี @promptkub ดึงเมื่อ 18 ต.ค. 2569" and "ดึงจาก Meta Graph API วันที่ 25 ต.ค. 2569" [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop), [ygnos.com/brand](https://ygnos.com/brand).
- Correction to the brief: the ygnos homepage's 1.5M figure is for ONE clip, not combined views: "1.5M วิว จากคลิปเดียวบน IG" and "คลิปแอนิเมชันที่คนดู 1.5M วิว ทำด้วย AI ทั้งเรื่อง", with "สถิติจาก IG @promptkub ณ 15 ต.ค. 2569" [OWNER] — [ygnos.com](https://ygnos.com/).

### Inferences
- Owner-claimed Instagram figures are internally consistent with the first-hand embed header (104 posts/198,931 followers on 25 Oct → 148 posts/241–242K followers on 31 Oct), so they are plausible, but they remain unaudited.
- Instagram post dates below are derived by decoding each reel shortcode into its media ID and reading the embedded millisecond timestamp (Instagram ID scheme: timestamp = (id >> 23) + 1314220021721 ms). The decoded dates (13–18 Oct 2026) fall exactly inside the owner's stated 10–17 Oct viral window, which corroborates the method.

### Gaps
- No tracker (Social Blade etc.) history exists for any platform; subscriber/follower curves before 2026-10-31 are owner-claimed only.
- Instagram per-reel view counts are not exposed by the embed; only likes and comment counts are first-hand.
- After ~30 watch-page requests YouTube began serving an "unusual traffic" interstitial, so upload dates for the pre-pivot tutorials and all caption/transcript extraction were not obtainable.
- Web search budget for this session was exhausted before Instagram-indexed reel URLs could be searched for further shortcodes.

## Q1. Which platforms does Prompt KUB post on, with what handles and size?

### Takeaway
The channel is effectively a one-platform Instagram Reels account (@promptkub, ~241–242K followers, 148 posts on 2026-10-31) with a secondary YouTube channel (@Promptkub, 33.8K subscribers, 47 videos, 1.41M views) used mainly for 8–60-minute long-form versions; the TikTok handle @promptkub is a private personal account with zero videos, a Facebook page facebook.com/Promptkub exists but is behind a login wall, and no Lemon8 or X presence was found.

### Cited Findings
- **Instagram** — URL [instagram.com/promptkub](https://www.instagram.com/promptkub/); display name "PromptKUB"; "241K followers • 148 posts" [FH 2026-10-31] — [profile embed](https://www.instagram.com/promptkub/embed/). Reel embeds the same day show "148 posts · 242K followers" and label audio as "Original audio" [FH] — [reel embed](https://www.instagram.com/reel/DecTQRbOcXU/embed/captioned/).
- Instagram is the only content platform the owner's site names: "ตอนหลักทุกตอนดูฟรีบน IG @promptkub เสมอ"; the site links only IG and LINE (@promptkub) — no YouTube/TikTok/Facebook links appear anywhere on ygnos.com (grep of all pages found 23 links to instagram.com/promptkub/ and 4 reel links, none to other platforms) [OWNER] — [ygnos.com](https://ygnos.com/).
- Instagram total views: "74.7M วิว จาก 104 โพสต์", "198,931 ผู้ติดตาม Instagram", "1,173,795 บัญชีที่มีส่วนร่วมในรอบ 28 วัน", "ตัวอย่างคลิปที่เกิน 1 ล้านวิว (29 คลิป)", all dated "25 ต.ค. 2569" [OWNER] — [ygnos.com/brand](https://ygnos.com/brand).
- Instagram per-clip performance: "REACH 437,069 บัญชีที่เห็นต่อคลิป (ค่ากลาง 83 คลิป 10–22 ต.ค.)", "ENGAGE 8.7% การมีส่วนร่วมต่อการเข้าถึง", "WATCH 33.0 วิ เวลาดูเฉลี่ยต่อคลิป (ค่ากลาง)" [OWNER] — [ygnos.com/brand](https://ygnos.com/brand).
- Instagram clip length: "คลิปเล่าเรื่องเอาตัวรอด 60–70 วินาที" (vertical Reels) [OWNER] — [ygnos.com/brand](https://ygnos.com/brand); the one commissioned brand clip is "แอนิเมชัน 72 วินาที · ซับไทย + อังกฤษ" [OWNER] — [ygnos.com/work/peaceful-day](https://ygnos.com/work/peaceful-day).
- **YouTube** — [youtube.com/@promptkub](https://www.youtube.com/@promptkub): 33.8K subscribers, 47 videos (33 in the Videos tab + 14 in the Shorts tab, counted from the fully scrolled grids), 1,414,039 total views, joined Aug 13, 2025, country Thailand [FH 2026-10-31] — [about](https://www.youtube.com/@promptkub/about), [videos](https://www.youtube.com/@promptkub/videos), [shorts](https://www.youtube.com/@promptkub/shorts). Channel RSS "published" timestamp: 2025-08-13T18:50:53+00:00 [FH] — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- YouTube format: the storytelling uploads are horizontal long-form "4K" videos of 8:01–59:05 (series episodes 8–11 min; standalone features 20:53, 26:26, 48:17, 58:24, 59:05); only 2 storytelling Shorts exist (ถ้าคุณเป็นกิ้งกือ 11K, ลุงเฉลย เพชรคือตลอดไป 6.5K) [FH] — [videos grid](https://www.youtube.com/@promptkub/videos).
- **TikTok** — [tiktok.com/@promptkub](https://www.tiktok.com/@promptkub) exists but is "privateAccount: true", nickname "Prompong Wijitpanya", account created 2018-06-12, 23 followers, 753 following, 1 like, 0 videos, language th [FH 2026-10-31, from the page's server-rendered `__UNIVERSAL_DATA_FOR_REHYDRATION__`] — [tiktok.com/@promptkub](https://www.tiktok.com/@promptkub). The channel therefore has no TikTok distribution.
- **Facebook** — a page titled "Prompt Kub" exists at [facebook.com/Promptkub](https://www.facebook.com/Promptkub) (surfaced by web search); fetching it returns only Facebook's login wall, so size/activity are unknown [FH 2026-10-31].
- **LINE** — official account @promptkub ("LINE ID: @promptkub", "ติดต่อด่วน") used for sales/support, not content [OWNER] — [ygnos.com/brand](https://ygnos.com/brand).
- **Lemon8 / X** — web searches for "promptkub"/"Prompt KUB" with lemon8/twitter returned no matching account; only unrelated "PUNKub" Lemon8 profile and crypto pages — [search result page](https://www.lemon8-app.com/pun_kub?region=th) (not related).
- Business contact on YouTube About and ygnos: business@ygnos.com; seller "บริษัท วีเพย์ โพรฟิต จำกัด" (V Pay Profit Co., Ltd.), juristic no. 0225562000413 [OWNER] — [ygnos.com/brand](https://ygnos.com/brand). Company registry snippets: registered 13 March 2019 (2562), registered capital ฿1,000,000, status active, Chanthaburi province, business type software retail [3P] — [dataforthai.com](https://www.dataforthai.com/company/0225562000413/), [creden.co](https://data.creden.co/company/general/0225562000413).

### Inferences
- The TikTok display name "Prompong Wijitpanya" is the only personal name attached to the handle anywhere; it is a private account and may or may not be the channel operator (the site never names a person), so treat it as unverified.
- Views per platform: Instagram ≈74.7M (25 Oct, claimed) vs YouTube 1.41M (31 Oct, first-hand) → Instagram carries >98% of the channel's audience; YouTube is a repurposing/long-form outlet started 3 weeks after the IG launch.

### Gaps
- Instagram follower count at finer granularity (e.g., exact number on 31 Oct) is only available rounded (241K/242K).
- Facebook page size, age and content unknown (login wall).
- Whether the Facebook page or an older YouTube persona predates the 2026 pivot is unknown.

## Q2. Growth timeline: start, spike, and whether growth has stalled

### Takeaway
The storytelling channel is about five weeks old: first Instagram post ≈23 Sep 2026, 8 followers on 1 Oct, under 100 on 10 Oct, ~25,000 on 17 Oct, 26,192 on 18 Oct, 59.4K on 20 Oct, 198,931 on 25 Oct and ~241–242K on 31 Oct; the spike was triggered by the Thai adaptation of Stickocalypse's "The Last Farm" posted ~14 Oct (1.5M views within ~2 days), and growth has slowed sharply in the last week (≈7K followers/day vs ≈28K/day during 20–25 Oct) but not stalled.

### Cited Findings
- "+25 วัน หลังโพสต์แรก — 18 ต.ค. 2569" (i.e., first post ≈ 23 Sep 2026), "26,192 ผู้ติดตาม", "43 โพสต์", "10,051,027 วิวรวม ของคลิปที่โพสต์ถึงวันนี้" [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop).
- Follower timeline quoted verbatim: "ผู้ติดตาม: 1 ต.ค. 8 คน, 10 ต.ค. ยังไม่ถึงร้อยคน (สถิติรายวันของ Instagram), 17 ต.ค. ราว 25,000 คน (เจ้าของเพจบันทึก), 18 ต.ค. 26,192" and headline "จาก 0 สู่ 25,000 ผู้ติดตาม — @promptkub · 10 → 17 ต.ค. 2569" [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop).
- 18 Oct milestones: "3 คลิปที่ทะลุล้านวิว", "19 คลิปที่ทะลุแสนวิว", top clips "ถ้า Zombie ระบาดหนัก จะเกิดอะไรขึ้น 1.54M", "ก่อนลงดอย ขอแวะขายชาเย็นแปป 1.38M", "เมื่อน้ำท่วมคอนโด ต้องทำไง 646K" [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop).
- 20 Oct (IG Story alt text): "1M+ CLUB: 7 คลิปของ @promptkub ที่ทะลุล้านวิว ทำด้วย AI ทั้งหมด วิวรวมทั้งเพจ 22.6M ผู้ติดตาม 59.4K สถิติจาก Instagram ณ 20 ต.ค. 2569" [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop).
- 25 Oct: 198,931 followers, 74.7M views / 104 posts, 29 clips >1M, top clips "ชาเย็นก่อนลงดอย 3.42M", "ถ้าซอมบี้ระบาดหนัก 2.68M", "ค้างภู EP.1 2.15M" [OWNER] — [ygnos.com/brand](https://ygnos.com/brand).
- 31 Oct: 241K followers • 148 posts [FH] — [profile embed](https://www.instagram.com/promptkub/embed/).
- The viral Zombie reel (shortcode DecTQRbOcXU) decodes to 2026-10-13 17:03 UTC = 14 Oct 00:03 Bangkok [DERIVED from shortcode]; the homepage reported it at "1.5M วิว" with "สถิติ ณ 15 ต.ค. 2569" [OWNER] — [ygnos.com](https://ygnos.com/).
- YouTube: the first storytelling upload is "วันธรรมดาที่ตลาดน้ำ แต่ดันเกิดโรคระบาดขึ้น!" dated Oct 16, 2026 (61,143 views, 967 likes, 34 comments on 31 Oct) [FH] — [watch?v=pKIzIBLCB2c](https://www.youtube.com/watch?v=pKIzIBLCB2c); everything older on the channel (Aug 2025–early Oct 2026) is AI-tool tutorials and demo clips with 362–4.5K views each [FH] — [videos grid](https://www.youtube.com/@promptkub/videos).
- Pre-pivot YouTube content examples: "Nano banana - Ai ตัวใหม่ที่จะมาล้าง Qwen, Wan2.2, Flux??" (11:49, 1.1K views, ~1 yr), "สอนใช้ Chat GPT เวอร์ชั่นคนขายของ" (1:26, 362 views), "PROMPTKUB – Dark Magic Book | Animation (Short)" (1:01, 741 views, ~1 yr), shorts such as "(ผลงาน Ai) 2020 Mercedes-AMG GT" 1.7K and "คลิปผลงานสร้าง Ai โดย promptkub (Warrix V-Shirt)" 1.7K [FH] — [videos](https://www.youtube.com/@promptkub/videos), [shorts](https://www.youtube.com/@promptkub/shorts).

### Inferences
- Follower velocity [DERIVED from the cited points]: 10→17 Oct ≈ +3.6K/day; 18→20 Oct ≈ +16.6K/day; 20→25 Oct ≈ +27.9K/day (peak); 25→31 Oct ≈ +7K/day — a ~75% deceleration in the most recent week while posting volume stayed at 7+ posts/day, suggesting the explore/reels distribution boost is fading.
- Views per post [DERIVED]: 234K avg on 18 Oct (10.05M/43) → 718K avg on 25 Oct (74.7M/104); the median reach of 437K for 10–22 Oct implies a long-tailed distribution dominated by the 29 million-view clips.
- YouTube subscribers (33.8K) almost certainly accrued after 16 Oct 2026: the 27 pre-pivot uploads total ≈34K views combined, while the 20 storytelling-era uploads total ≈1.44M, i.e., ~97% of lifetime channel views in 13 days [DERIVED from grid counts; the About total of 1,414,039 lags the per-video sum].
- Chronology: YouTube storytelling started 2 days after the IG Zombie clip went viral (14→16 Oct), consistent with YouTube being an opportunistic second outlet rather than the launch platform.

### Gaps
- No day-by-day follower series exists outside the owner's chart (the interactive chart's data was not extractable); the 17 Oct "ราว 25,000" is explicitly the owner's own note, not API data.
- No independent confirmation of the 74.7M / 198,931 figures.
- Whether follower growth has continued to decelerate after 31 Oct cannot be known yet.

## Q3. Clip-by-clip: top/bottom clips, posting cadence, times and recurring themes

### Takeaway
Only four Instagram reels are individually identifiable (all four are million-view clips, posted 14–18 Oct 2026, with 61K–317K likes and 24–191 comments), while all 47 YouTube videos are tabulated below; on both platforms the clear winners are second-person Thai-localised survival scenarios (zombies in Bangkok, floods, mountain camping, the New Year drive home) and standalone feature-length "จบในตอน" stories, while later episodes of a series decay to a quarter of episode 1, and pre-pivot AI tutorials sit at the bottom with a few hundred views.

### Cited Findings
**Instagram reels (first-hand likes/comments/captions from embeds on 2026-10-31; views owner-claimed; post time derived from shortcode, Bangkok time)**

| Reel (first caption line) | URL | Posted [DERIVED] | Views [OWNER] | Likes [FH] | Comments [FH] | Caption & hashtags [FH] |
|---|---|---|---|---|---|---|
| ถ้า Zombie ระบาดหนัก จะเกิดอะไรขึ้น? (= สวนสุดท้าย EP.1, Thai adaptation of "The Last Farm") | [reel/DecTQRbOcXU](https://www.instagram.com/reel/DecTQRbOcXU/) | 2026-10-14 00:03 | 1.5M (15 Oct) → 1.54M (18 Oct) → 2.68M (25 Oct) | 252,606 | 101 | "ตัวอย่างงาน Ai! — ถ้า Zombie ระบาดหนัก จะเกิดอะไรขึ้น? 🎬 ดัดแปลงเป็นเวอร์ชันไทยจาก THE LAST FARM ต้นฉบับโดย @stickocalypse_shorts ภาพทุกช็อตให้ AI เขียนโค้ดวาดขึ้นใหม่ · เสียงบรรยายโดย AI · ขอบคุณต้นฉบับครับ 🙏" — no hashtags |
| เมื่อน้ำท่วมคอนโด ต้องทำไง? | [reel/Dee1cvfOWeM](https://www.instagram.com/reel/Dee1cvfOWeM/) | 2026-10-14 23:40 | 646K (18 Oct) | 61,642 | 24 | "เมื่อน้ำท่วมคอนโด ต้องทำไง?" — no hashtags |
| ค้างภู EP.1 | [reel/DemD5eruki2](https://www.instagram.com/reel/DemD5eruki2/) | 2026-10-17 19:01 | 2.15M (25 Oct) | 161,747 | 97 | "ตัวอย่างงาน AI โดย Prompt KUB \| ตอน ค้างภู "EP. 1"" #ค้างภู #ซอมบี้ #เดินป่า #กางเต็นท์ #เอาตัวรอด #animation #AIanimation #PromptKUB |
| ก่อนลงดอย ขอแวะขายชาเย็นแปป | [reel/Den1l8AO-a1](https://www.instagram.com/reel/Den1l8AO-a1/) | 2026-10-18 11:35 | 1.38M (18 Oct) → 3.42M (25 Oct) | 316,599 | 191 | "ก่อนลงดอย ขอแวะขายชาเย็นแปป \| ตัวอย่างงาน AI โดย Prompt KUB ตอน "อย่าแข่งกันถูก แข่งกันคุ้ม"" #PromptKUB #ธุรกิจ #ค้าขาย #ชาเย็น #การตลาด #จิตวิทยาการตลาด #ขายของ #AIAnimation |

Sources for the table: embeds [Den1l8AO-a1](https://www.instagram.com/reel/Den1l8AO-a1/embed/captioned/), [DecTQRbOcXU](https://www.instagram.com/reel/DecTQRbOcXU/embed/captioned/), [DemD5eruki2](https://www.instagram.com/reel/DemD5eruki2/embed/captioned/), [Dee1cvfOWeM](https://www.instagram.com/reel/Dee1cvfOWeM/embed/captioned/); views from [ygnos.com/workshop](https://ygnos.com/workshop) (18 Oct) and [ygnos.com/brand](https://ygnos.com/brand) (25 Oct).

- Other Instagram titles known only by name/alt text (no shortcode): "สวนสุดท้าย ตอนที่ 1 ชาวสวนกับสุนัข", "สวนสุดท้าย ตอนที่ 3", "ถ้าน้ำท่วมใหญ่ ตอนคุณอยู่คอนโด" [OWNER] — [ygnos.com](https://ygnos.com/); commissioned clip "Peaceful Day × Prompt KUB" (72 s, Paid partnership, cold-plunge spa Sukhumvit 62) [OWNER] — [ygnos.com/work/peaceful-day](https://ygnos.com/work/peaceful-day).
- Instagram cadence [OWNER counts]: 43 posts by 18 Oct (25 days after first post), 83 clips in 10–22 Oct, 104 posts by 25 Oct — [workshop](https://ygnos.com/workshop), [brand](https://ygnos.com/brand); 148 posts by 31 Oct [FH] — [embed](https://www.instagram.com/promptkub/embed/).

**YouTube — all 47 uploads (first-hand, 2026-10-31; exact timestamps UTC from RSS/watch pages, otherwise YouTube's relative age)**

Long-form (Videos tab, newest first):
1. รถไฟฟ้าขบวนสุดท้าย 4K (เรื่องเต็ม 1 ชั่วโมง จบในตอน) — 58:24 — 2026-10-28 12:13Z — 108,270 views, 1,556 likes, 88 comments — [ZMdUd9jv7RI](https://www.youtube.com/watch?v=ZMdUd9jv7RI)
2. 30 วัน ห้ามเปิดไฟ ตอนที่ 6 4K — 9:03 — 2026-10-28 10:03Z — 25,552 views, 332 likes — [ILLi5Q4bI9U](https://www.youtube.com/watch?v=ILLi5Q4bI9U)
3. 30 วัน ห้ามเปิดไฟ ตอนที่ 5 4K — 8:53 — 2026-10-28 10:03Z — 26,309 views, 296 likes — [v6F2OEDdkr8](https://www.youtube.com/watch?v=v6F2OEDdkr8)
4. บ้านที่ไม่เคยได้กลับ 4K (50 นาที เต็มเรื่อง ตอนเดียวจบ) — 48:17 — 2026-10-27 15:07Z — 182,737 views, 2,617 likes, 72 comments — [ltvzLD1C7kA](https://www.youtube.com/watch?v=ltvzLD1C7kA)
5. 450 กิโลถึงบ้าน ตอนที่ 5 4K (ส่งท้าย) — 8:44 — 2026-10-26 12:24Z — 35,040 views, 423 likes — [HglAM4vtEE0](https://www.youtube.com/watch?v=HglAM4vtEE0)
6. 30 วัน ห้ามเปิดไฟ ตอนที่ 4 4K — 8:34 — 2026-10-25 17:41Z — 43,892 views, 533 likes — [1RuKPwp0sIY](https://www.youtube.com/watch?v=1RuKPwp0sIY)
7. ถ้าคืนนี้อยากนอนหลับ อย่าดู!! | กฏกะดึก ห้อง 7 0 4 — 26:26 — 2026-10-25 14:01Z — 96,526 views, 1,388 likes — [o1vUyec_BeU](https://www.youtube.com/watch?v=o1vUyec_BeU)
8. จุดพักรถตีสาม 4K (แรงบันดาลใจ "หมอกในร้านสะดวกซื้อ") | (เรื่องยาว จบในตอน) — 20:53 — 2026-10-23 23:42Z — 111,741 views, 1,856 likes — [3A8hMsQvBoI](https://www.youtube.com/watch?v=3A8hMsQvBoI)
9. 30 วัน ห้ามเปิดไฟ ตอนที่ 3 4K — 8:47 — 2026-10-23 16:24Z — 53,515 views, 631 likes — [mwTycuauJ5I](https://www.youtube.com/watch?v=mwTycuauJ5I)
10. 450 กิโลถึงบ้าน ตอนพิเศษ 4K — 9:02 — 2026-10-22 14:11Z — 62,207 views, 732 likes — [NcJfrVhufHg](https://www.youtube.com/watch?v=NcJfrVhufHg)
11. 30 วัน ห้ามเปิดไฟ ตอนที่ 2 4K — 9:19 — 2026-10-21 16:49Z — 72,827 views, 777 likes — [odS31BEotV8](https://www.youtube.com/watch?v=odS31BEotV8)
12. เรือด่วนเที่ยวสุดท้าย 4K (จบในตอนเดียว เปิดฟังได้ยาวๆ) — 59:05 — 2026-10-21 10:46Z — 145,645 views, 2,282 likes, 111 comments — [vuvhqWAY0FE](https://www.youtube.com/watch?v=vuvhqWAY0FE)
13. 30 วัน ห้ามเปิดไฟ ตอนที่ 1 4K — 10:40 — 2026-10-20 17:19Z — 118,384 views, 1,342 likes — [ujv6SdDMJtY](https://www.youtube.com/watch?v=ujv6SdDMJtY)
14. 450 กิโลถึงบ้าน ตอนที่ 3 ตอนจบ 4K — 8:24 — 2026-10-20 16:44Z — 63,082 views, 908 likes — [PQwfhWXWSDI](https://www.youtube.com/watch?v=PQwfhWXWSDI)
15. 450 กิโลถึงบ้าน ตอนที่ 2 4K — 8:01 — "10 days ago" (~20 Oct) — 67K views — [Jmztm1F8S8Y](https://www.youtube.com/watch?v=Jmztm1F8S8Y)
16. 450 กิโลถึงบ้าน ตอนที่ 1 4K — 8:56 — Oct 19, 2026 — 137,573 views, 1,643 likes, 35 comments — [5HndptcZwkM](https://www.youtube.com/watch?v=5HndptcZwkM)
17. วันธรรมดาที่ตลาดน้ำ แต่ดันเกิดโรคระบาดขึ้น! — 11:55 — Oct 16, 2026 — 61,143 views, 967 likes, 34 comments — [pKIzIBLCB2c](https://www.youtube.com/watch?v=pKIzIBLCB2c)
18. เมื่อซอมบี้บุกเมือง แต่คุณติดอยู่บน BTS — 2:19 — "2 weeks ago" — 12K views — [xq9CD1vqIoA](https://www.youtube.com/watch?v=xq9CD1vqIoA)
19. เฟดเสียง + มาร์คจุด ใน Premiere Pro เวอร์ชันใหม่ (2025 / 2026) | ฉบับง่าย — 3:00 — 2 weeks — 1.1K — [kLyggn0C0c4](https://www.youtube.com/watch?v=kLyggn0C0c4)
20. PhotoCraft ผู้มาแทน PhotoShop?!?! (สอนโหลด ติดตั้ง และใช้งานได้จริง โคตรฟรี โคตรดี!) — 2:14 — 2 weeks — 1.2K — [MeWCcGQur1o](https://www.youtube.com/watch?v=MeWCcGQur1o)
21. ตัวอย่างคลิปสอนใช้ Ai ในการสร้างคลิป (ฉบับไว) — 5:40 — 4 weeks — 829 — [SEu9YWYxiJo](https://www.youtube.com/watch?v=SEu9YWYxiJo)
22. สอน ทำเกมเล่นกับลูก ด้วย Claude (Ai) | ทำตามได้ ง่ายมากๆ — 4:11 — 1 month — 428 — [wY9k9aaORTY](https://www.youtube.com/watch?v=wY9k9aaORTY)
23. วิธีทำคลิป Ai แบบง่ายๆ — 4:35 — 1 month — 832 — [yrt8Nhg_iSE](https://www.youtube.com/watch?v=yrt8Nhg_iSE)
24. ตัวอย่างคลิป Ai (100%) — 1:01 — 1 month — 442 — [UuZ-0n4DFzA](https://www.youtube.com/watch?v=UuZ-0n4DFzA)
25. สอนใช้ Premiere Pro (2025 & 2026) | ฉบับง่าย — 7:50 — 1 month — 504 — [O1nul96rML0](https://www.youtube.com/watch?v=O1nul96rML0)
26. Ai ตอนนี้ แค่กด 1 ปุ่ม ได้ทั้ง Storyboard, ภาพ, คลิป, ต่อฉาก, เปลี่ยนฉาก เปลี่ยนทุกอย่าง — 4:04 — 10 months — 371 — [jD3L3bvO6Bs](https://www.youtube.com/watch?v=jD3L3bvO6Bs)
27. สอนวิธีใช้ Ai ทำคลิปคุณภาพ ระดับ Production House — 5:23 — 1 year — 378 — [ArN9qS5HGCo](https://www.youtube.com/watch?v=ArN9qS5HGCo)
28. สอนใช้ Chat GPT เวอร์ชั่นคนขายของ | ใน 1 นาที (ดูจบ คุณทำงานง่ายขึ้น 99%) — 1:26 — 1 year — 362 — [-MY-OP4jYIY](https://www.youtube.com/watch?v=-MY-OP4jYIY)
29. สอนทำภาพเท่ๆ ด้วย Nano Banana (Google Ai เปลี่ยนภาพ) — Gemini 2.5 Flash — 14:05 — 1 year — 4.5K — [ce-DiWRURAA](https://www.youtube.com/watch?v=ce-DiWRURAA)
30. สอนเปลี่ยนตัวละครใน วีดีโอ แบบเท่ๆ ใน 7 ขั้นตอน ด้วย (Nano Banana + Veo3) | Ai showcase — 9:40 — 1 year — 910 — [FlfrSEHEgSc](https://www.youtube.com/watch?v=FlfrSEHEgSc)
31. Nano Banana ai ใช้ prompt แบบไหนได้บ้าง | ตัวอย่างงานจริง — 5:57 — 1 year — 1.2K — [EjcW6MHvKQ8](https://www.youtube.com/watch?v=EjcW6MHvKQ8)
32. Nano banana - Ai ตัวใหม่ที่จะมาล้าง Qwen, Wan2.2, Flux?? — 11:49 — 1 year — 1.1K — [Zcto1kZV6Xk](https://www.youtube.com/watch?v=Zcto1kZV6Xk)
33. PROMPTKUB – Dark Magic Book | Animation (Short) — 1:01 — 1 year — 741 — [I85rB3Q651E](https://www.youtube.com/watch?v=I85rB3Q651E)

Shorts tab (14): ถ้าคุณเป็นกิ้งกือ ตอนหลงทาง 11,165 views, 317 likes, 5 comments, Oct 26, 2026 — [r7TSsOfztQg](https://www.youtube.com/shorts/r7TSsOfztQg); ลุงเฉลย เพชรคือตลอดไป 4K 6.5K — [aWKjhvzYKHk](https://www.youtube.com/shorts/aWKjhvzYKHk); ผมลองให้ Ai ทำคลิปแบบนี้ให้ 3K; ผลงาน Ai 100% (ทั้งตัดต่อ ทั้งคิดคอนเซป ทั้งทำเป็นคลิป Reel) 1.1K; Ai ไปไกลกว่าที่คุณคิด 2.1K; BADLAND Predator #aivideo 1.2K; ผลงาน Ai สร้างโดย Promptkub 807; Video สร้างจาก Ai 496; AUTODEW Studio 2.2K; ผลงานสร้างจาก Ai 100% - ยกเว้นข้อความ 373; (ผลงาน Ai) 2020 Mercedes-AMG GT 1.7K; ผลงานจาก #aivideo - Ai 100% ยกเว้น Subtitle 1.9K; ขวดไวน์ราคาแพง #aiภาพ #สอนสร้างai #chatgpt #midjourney #geminiflash #smartphone #nano #movie 2.4K; คลิปผลงานสร้าง Ai โดย promptkub (Warrix V-Shirt) 1.7K [FH] — [shorts grid](https://www.youtube.com/@promptkub/shorts). Sources for long-form rows 1–14: [RSS feed](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ); rows 15–33 and relative ages: [videos grid](https://www.youtube.com/@promptkub/videos).

- **YouTube top 5 by views (31 Oct):** (1) บ้านที่ไม่เคยได้กลับ 182,737 (48:17, 27 Oct, ghost/fog horror, standalone); (2) เรือด่วนเที่ยวสุดท้าย 145,645 (59:05, 21 Oct, zombies/Chao Phraya express boat, standalone); (3) 450 กิโลถึงบ้าน ตอนที่ 1 137,573 (8:56, 19 Oct, zombies/New Year drive to Khon Kaen, series opener); (4) 30 วัน ห้ามเปิดไฟ ตอนที่ 1 118,384 (10:40, 20 Oct, zombies/condo blackout, series opener); (5) จุดพักรถตีสาม 111,741 (20:53, 24 Oct, fog horror at a mountain convenience store, standalone) [FH] — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- **YouTube bottom 5 (all pre-pivot tutorials/demos):** สอนใช้ Chat GPT เวอร์ชั่นคนขายของ 362; Ai ตอนนี้ แค่กด 1 ปุ่ม 371; ผลงานสร้างจาก Ai 100% - ยกเว้นข้อความ (short) 373; สอนวิธีใช้ Ai ทำคลิปคุณภาพ ระดับ Production House 378; สอน ทำเกมเล่นกับลูก ด้วย Claude 428 [FH] — [videos grid](https://www.youtube.com/@promptkub/videos). Weakest storytelling-era items: ลุงเฉลย เพชรคือตลอดไป (short) 6.5K, ถ้าคุณเป็นกิ้งกือ (short) 11.2K, เมื่อซอมบี้บุกเมือง แต่คุณติดอยู่บน BTS (2:19) 12K.
- Series decay on YouTube [FH]: 450 กิโลถึงบ้าน EP1 137.6K → EP2 67K → EP3 63K → ตอนพิเศษ 62K → EP5 35K; 30 วัน ห้ามเปิดไฟ EP1 118K → EP2 72.8K → EP3 53.5K → EP4 43.9K → EP5 26.3K → EP6 25.6K (EP5–6 are 3 days old) — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- YouTube cadence and timing [FH]: 15 uploads between 2026-10-19 and 2026-10-28 (10 days) with multi-upload days on 20 Oct (3), 21 Oct (2), 23 Oct (2), 25 Oct (2), 26 Oct (2), 28 Oct (3); upload times 10:03–23:42 UTC = 17:03–06:42 Bangkok, i.e., mostly early evening to past midnight Thai time — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- Stickocalypse comparator (first-hand, 31 Oct): Part 1 "THE LAST FARM" Short 6M views; Part 2 "The Barn Wasn't Empty" 379K; Part 4 "The City Went Silent" 241K; Part 5 131K; Part 6 79K; Part 8 "They Split the Herd" 15K — [youtube.com/@Stickocalypse_Shorts/shorts](https://www.youtube.com/@Stickocalypse_Shorts/shorts).

### Inferences
- Instagram posting cadence [DERIVED from owner counts + first-hand 148]: ≈1.7 posts/day for 23 Sep–18 Oct (43 posts/25 days), then ≈8.7/day for 18–25 Oct (61 posts/7 days) and ≈7.3/day for 25–31 Oct (44 posts/6 days); "83 clips in 10–22 Oct" vs "43 posts by 18 Oct" implies ~10 posts/day during 19–22 Oct. Overall ≈3.9 posts/day since launch.
- Instagram posting times for the four dated reels: 00:03, 23:40, 19:01 and 11:35 Bangkok — consistent with YouTube's evening/late-night pattern, but n=4.
- Like-to-view ratios on Instagram [DERIVED, likes 31 Oct vs views 25 Oct so slightly overstated]: ชาเย็น 9.3%, Zombie 9.4%, ค้างภู 7.5%, น้ำท่วมคอนโด 9.5% (vs 18 Oct views) — an unusually high like rate; comments are very low (24–191 per million-view reel), i.e., a passive-watch audience. YouTube like rates are ~1.1–1.6% on long-form.
- What differentiates winners: (a) a second-person "ถ้าคุณ…" premise anchored in a recognisable Thai place (BTS, Chao Phraya, condo, Isan highway, Doi); (b) openers (EP.1) and standalone "จบในตอน" features beat continuations; (c) the single non-horror hit (ชาเย็น, a business/psychology parable) is the best clip of all, suggesting the narration + HUD format travels beyond zombies; (d) weakest storytelling items are gimmick/POV shorts (กิ้งกือ, ลุงเฉลย) and very short cuts (BTS 2:19).
- The identical 10:03Z timestamps of 30 วัน EP5 and EP6 indicate batch/scheduled publishing.

### Gaps
- Only 4 of 148 Instagram posts could be identified individually; no per-post view counts, durations or exact posting times are available first-hand; the bottom-performing Instagram clips are unknown.
- Instagram follower-time series by post could not be extracted from the owner's chart.
- Upload dates for pre-pivot YouTube items and both storytelling Shorts (ลุงเฉลย) are only known as YouTube relative ages.
- Whether the ชาเย็น reel really reached 1.38M views on its posting day (18 Oct) or the owner's "18 Oct" figure was refreshed later is unknowable from the page.

## Q4. Format fingerprint: visuals, voice, subtitles, music, hook, structure, CTA, captions/hashtags, titles

### Takeaway
Every clip is a Thai-narrated, AI-coded 2D vector/stick-rig animation (SVG puppets + game-style HUD stat cards, rendered 4K) in a calm second-person voice that moves "problem → fact → fix" every 3–5 seconds, uses one animal sidekick, a twist and a "ตอนต่อไป" ending; Instagram cuts are 60–70 s vertical with 1–3-line captions and 0–8 hashtags, while YouTube carries 8–60-minute 16:9 "4K" versions whose descriptions open with the hook sentence, list chapter timestamps, a sourced "ข้อมูลจริงในเรื่อง" fact block, a fiction disclaimer and the credit line "ภาพ เสียงบรรยาย และดนตรี สร้างด้วย AI · ตัวอย่างงาน AI โดย Prompt KUB".

### Cited Findings
- Structure as stated by the owner for brand clips: "ผู้เล่าเสียงสงบพาคนดูผ่าน ปัญหา → ข้อเท็จจริง → ทางแก้ ทุก 3–5 วินาที มีการ์ดแบบเกม สัตว์ 1 ตัว จุดหักมุม และ "ตอนต่อไป"" and "คลิปเล่าเรื่องเอาตัวรอด 60–70 วินาที" [OWNER] — [ygnos.com/brand](https://ygnos.com/brand).
- Hook length: "ถอดสูตรคลิปที่คนดูจนจบแล้วแชร์ต่อ: ฮุก 2 วินาทีแรก และเรื่องที่ชวนเล่าต่อ" and series logic "ทำเป็นซีรีส์ ให้คนรอดูตอนต่อไป", "จังหวะการโพสต์ และการเขียนแคปชัน", "อ่านสถิติ IG แล้วตัดสินใจว่าจะทำอะไรต่อ" [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop).
- Story engine taught in the course: "01 ทำไมคลิปนี้ทะลุครึ่งล้านวิว สูตร 6 ข้อ", "02 เครื่องยนต์เรื่อง: ปัญหา ข้อเท็จจริง ปัญหาใหม่ และความเป็นต้นฉบับ" [OWNER] — [ygnos.com](https://ygnos.com/).
- Visual style: "ชุดหุ่น SVG ฉาก และ HUD ด้วย HyperFrames", "ภาพสร้างด้วย Claude Code และ HyperFrames", "แตกช็อต แล้วให้ AI หลายตัวทำพร้อมกัน", "ตรวจงาน เรนเดอร์ 4K และโพสต์" [OWNER] — [ygnos.com](https://ygnos.com/); the Zombie reel caption: "ภาพทุกช็อตให้ AI เขียนโค้ดวาดขึ้นใหม่" [FH] — [reel embed](https://www.instagram.com/reel/DecTQRbOcXU/embed/captioned/). Image alt texts describe "ภาพมุมสูงของสวนทุเรียน จากคลิปแอนิเมชัน สวนสุดท้าย" and a HUD "การ์ดเกมโชว์ว่าแบตสำรอง 10,000 mAh ชาร์จมือถือได้ราว 1.8 รอบ" [OWNER] — [ygnos.com](https://ygnos.com/), [ygnos.com/brand](https://ygnos.com/brand).
- Voice/subtitles/music: "เสียงพากย์ AI ภาษาไทยที่ไม่สะดุด", "ซับตรงปาก: จาก script สู่ timing", "เพลง เสียงประกอบ และการมิกซ์"; "เสียงพากย์และเพลงใช้ AI ของ Magnific" [OWNER] — [ygnos.com](https://ygnos.com/); brand deliverable "ซับไทย + อังกฤษ", "ผู้บรรยายพูดชื่อสินค้าในเรื่อง" [OWNER] — [ygnos.com/brand](https://ygnos.com/brand). All four embeds label the sound "Original audio" (no trending audio) [FH] — [embed](https://www.instagram.com/reel/Den1l8AO-a1/embed/captioned/).
- Hook sentences (first line of the YouTube description, second person, conditional, Thai-specific, with a counterintuitive rule) [FH, RSS]: "ถ้าซอมบี้บุกกรุงเทพ คืนก่อนหยุดยาวปีใหม่ อย่าขับรถกลับบ้าน เพราะคนทั้งเมืองกำลังคิดแบบเดียวกับคุณ..." (450 กิโลถึงบ้าน EP1) — [5HndptcZwkM](https://www.youtube.com/watch?v=5HndptcZwkM); "ถ้าซอมบี้ขึ้นมาอยู่ในตึกเดียวกับคุณ อย่าเปิดไฟฉาย แม้จะมองไม่เห็นอะไรเลย เพราะ... ไฟฉายหนึ่งกระบอกคือป้ายบอกทางให้พวกมันทั้งตึก" (30 วัน EP2); "คุณอยู่ห้อง 1708 ชั้น 17 กับแมวส้มชื่อมะขาม และพวกมันเดินเข้าหาแสง" (30 วัน EP1); "ถ้าซอมบี้บุกกรุงเทพ แล้วไฟดับทั้งเมือง ที่ที่ปลอดภัยที่สุดคือรางลอยฟ้า" (รถไฟฟ้าขบวนสุดท้าย); "เย็นวันศุกร์ ซอมบี้บุกกรุงเทพ รถทุกคันติดอยู่บนถนน แต่แม่น้ำเจ้าพระยายังไหลอยู่ / คุณเป็นนายท้ายเรือด่วนเจ้าพระยา ลูกสาวเก้าขวบที่ว่ายน้ำไม่เป็นนั่งอยู่ท้ายเรือ" (เรือด่วน); "ห้าปีที่ไม่ได้กลับบ้าน แม่ส่งข้อความเสียงมาทุกคืน สองทุ่มตรง ส่วนเรา ตอบแค่สติกเกอร์" (บ้านที่ไม่เคยได้กลับ); "ถ้าคุณเป็นพนักงานกะดึก ของโรงแรมที่ไม่มีห้อง 704" (กฎกะดึก) — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- Instagram caption hooks are questions/premises: "ถ้า Zombie ระบาดหนัก จะเกิดอะไรขึ้น?", "เมื่อน้ำท่วมคอนโด ต้องทำไง?", "ก่อนลงดอย ขอแวะขายชาเย็นแปป … ตอน "อย่าแข่งกันถูก แข่งกันคุ้ม"" [FH] — embeds cited in Q3.
- Fact-block convention in descriptions: "ข้อมูลจริงในเรื่อง: • น้ำฝนที่รองไว้ควรกรองผ่านผ้าสะอาด แล้วต้มให้เดือดอย่างน้อย 1 นาทีก่อนดื่ม • ... แหล่งข้อมูล: CDC (Make Water Safe During an Emergency)…" (30 วัน EP4); "• ไก่ขันตามนาฬิกาในตัว ก่อนฟ้าสางราวสองชั่วโมง (Shimmura & Yoshimura, Current Biology 2013)" (450 ตอนพิเศษ); "• ในคืนที่มืดสนิท ตาคนมองเห็นแสงเทียนเล่มเดียวได้ไกลราว 2.6 กิโลเมตร (Krisciunas & Carona, 2015)" (30 วัน EP1); sources also cite "NFPA 101", "กรมพัฒนาที่ดิน" [FH] — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- Disclaimers/credits: "ซอมบี้ กฎของพวกมัน และเหตุการณ์ทั้งหมดเป็นเรื่องแต่ง" and "ภาพ เสียงบรรยาย และดนตรี สร้างด้วย AI · ตัวอย่างงาน AI โดย Prompt KUB" appear in multiple descriptions [FH] — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- Chapter markers in long features, e.g. "0:00 เปิดเรื่อง / 1:11 บทที่ 1 เที่ยวสุดท้าย / 4:19 บทที่ 2 ท่าโรงพยาบาล / 7:33 บทที่ 3 ทางเดียวที่ยังไหล / 10:51 บทที่ 4 สะพานแรก / 13:52 บทที่ 5 ฝนคน / 16:58 บทที่ 6 นกหวีด / 19:55 บทที่ 7 ..." (เรือด่วน) and "0:00 เปิดเรื่อง / 1:06 บทที่ 1 ปีหน้า / 3:45 บทที่ 2 เสียงแม่ที่ไม่เคยฟัง ..." (บ้านที่ไม่เคยได้กลับ) [FH] — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- Hashtag pattern: YouTube "#450กิโลถึงบ้าน #ซอมบี้ #เอาตัวรอด #แอนิเมชัน #ปีใหม่ #กรุงเทพ #PromptKUB" (series tag + genre + place + brand) [FH] — [5HndptcZwkM](https://www.youtube.com/watch?v=5HndptcZwkM); Instagram 0 (Zombie, น้ำท่วม) to 8 tags (#ค้างภู #ซอมบี้ #เดินป่า #กางเต็นท์ #เอาตัวรอด #animation #AIanimation #PromptKUB; #PromptKUB #ธุรกิจ #ค้าขาย #ชาเย็น #การตลาด #จิตวิทยาการตลาด #ขายของ #AIAnimation) [FH] — embeds cited in Q3.
- YouTube title style: Thai title + "4K" + bracketed length/format promise — "(เรื่องเต็ม 1 ชั่วโมง จบในตอน)", "(50 นาที เต็มเรื่อง ตอนเดียวจบ)", "(จบในตอนเดียว เปิดฟังได้ยาวๆ)", "ตอนที่ N 4K", clickbait variant "ถ้าคืนนี้อยากนอนหลับ อย่าดู!!" [FH] — [videos grid](https://www.youtube.com/@promptkub/videos).
- Recurring "one animal": "ชาวสวนกับสุนัข" (สวนสุดท้าย EP1) [OWNER] — [ygnos.com](https://ygnos.com/); "แมวส้มชื่อมะขาม" (30 วัน EP1), "หมาจรหนึ่งตัว" (จุดพักรถตีสาม) [FH] — [RSS](https://www.youtube.com/feeds/videos.xml?channel_id=UCnpJKj1chdaFWdFQj5BX5EQ).
- The Stickocalypse template the format descends from (per a third-party analysis dated 19 Oct 2026): Shorts of 60–100 s, side-view stick figures in flat colour layers with fog, third-person narrator, burned-in captions, cliffhanger per part, shot change every 2–3 s, ≥3 settings per episode, second-person counterintuitive hook [3P] — [vuela.ai blog](https://vuela.ai/blog/how-to-make-viral-stick-figure-series-with-ai).

### Inferences
- The visual style is NOT Pixar-like 3D: all evidence points to code-generated 2D vector (SVG) rigs — a Thai-localised evolution of the stick-figure survival genre — with the distinguishing additions of game-HUD stat cards and sourced real-world facts.
- No explicit "follow/กดติดตาม" call-to-action appears in any of the 4 Instagram captions or the 15 YouTube descriptions examined; retention is driven by the in-video "ตอนต่อไป" cliffhanger and series naming (EP.1, ตอนที่ N) instead.
- Themes cluster into: zombie outbreak in Bangkok/Thai settings (BTS, express boat, condo blackout, floating market, New Year highway), disaster how-to (condo flood), mountain/camping survival (ค้างภู, ลงดอย), fog/ghost horror (หมอก, ห้อง 704), and one business parable (ชาเย็น). The title "จุดพักรถตีสาม (แรงบันดาลใจ "หมอกในร้านสะดวกซื้อ")" shows a second case of openly adapting an existing story.

### Gaps
- No transcript or caption track could be obtained, so the literal first-3-second narration and the exact wording of the "ตอนต่อไป" sign-off are unverified; the hook sentences above are the first lines of descriptions, which closely track the narration but are not confirmed as it.
- Exact durations of the Instagram reels and whether Instagram and YouTube versions differ in edit (beyond length) are unverified.
- Music source and whether the narrator voice is one consistent AI voice across clips: owner-claimed (Magnific) only.

## Q5. What is "สวนสุดท้าย", how many episodes, and what is @stickocalypse_shorts; originality/repost risk

### Takeaway
"สวนสุดท้าย" (The Orchard) is Prompt KUB's zombie-survival series set in a Thai durian orchard with a farmer and his dog; episode 1 is an openly credited Thai re-telling of Stickocalypse's "The Last Farm" (Part 1 of the "STICKOCALYPSE MOVIE"), re-drawn by AI code with a Thai AI narrator; at least 3 episodes exist, and the source channel — a Jordan-registered stick-figure creator with 43.1K YouTube subscribers, 177K Instagram followers and a 6M-view Part 1 — licenses language versions, but the "with permission" claim comes only from Prompt KUB's side.

### Cited Findings
- Series description: "คอร์สทำคลิปแอนิเมชันเล่าเรื่องด้วย AI สูตรเดียวกับซีรีส์ สวนสุดท้าย", image alts "ภาพมุมสูงของสวนทุเรียน จากคลิปแอนิเมชัน สวนสุดท้าย", "ฉากจากคลิป สวนสุดท้าย ตอนที่ 1 ชาวสวนกับสุนัข", "ฉากจากคลิป สวนสุดท้าย ตอนที่ 3", and "สวนสุดท้าย ตอนที่ 1 ดัดแปลงโดยได้รับอนุญาตจาก @stickocalypse_shorts" [OWNER] — [ygnos.com](https://ygnos.com/).
- The IG caption of the viral clip: "ดัดแปลงเป็นเวอร์ชันไทยจาก THE LAST FARM ต้นฉบับโดย @stickocalypse_shorts — ภาพทุกช็อตให้ AI เขียนโค้ดวาดขึ้นใหม่ · เสียงบรรยายโดย AI · ขอบคุณต้นฉบับครับ" [FH] — [reel embed](https://www.instagram.com/reel/DecTQRbOcXU/embed/captioned/); the workshop page labels the same clip "คลิป Zombie ดัดแปลงโดยได้รับอนุญาตจาก @stickocalypse_shorts" [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop).
- Stickocalypse YouTube [FH 2026-10-31]: "Stickocalypse is where stick figures try to survive the end of the world.", country Jordan, 43.1K subscribers, 6,947,434 views, 8 videos, joined Oct 15, 2024, links to instagram.com/stickocalypse_shorts, tiktok.com/@stickocalypse_shorts, boosty.to/stickocalypse, t.me/Stickocalypse — [youtube.com/@Stickocalypse_Shorts/about](https://www.youtube.com/@Stickocalypse_Shorts/about). Shorts: "PART 1 STICKOCALYPSE MOVIE, CHAPTER 1 (THE LAST FARM) — EPS 1" 6M views; "The Barn Wasn't Empty… PART 2 … (THE LAST FARM) — EPS 2" 379K; "The City Went Silent… PART 4 … Chapter 2 (THE CITY)" 241K; Part 5 131K; Part 6 79K; "Part 8: They Split the Herd | Taking Back the Farm, Episode 2" 15K — [shorts](https://www.youtube.com/@Stickocalypse_Shorts/shorts).
- Stickocalypse TikTok [FH]: @stickocalypse_shorts, 24,615 followers, 242,366 likes, 7 videos, 2 following, bio "Welcome to Stickocalypse ☢️ Animated survival stories, end-of-the-world chaos.", account created 2026-10-12 — [tiktok.com/@stickocalypse_shorts](https://www.tiktok.com/@stickocalypse_shorts). Instagram [FH]: "stickocalypse_shorts · Stickocalypse · 177K followers • 8 posts" — [instagram.com/stickocalypse_shorts/embed/](https://www.instagram.com/stickocalypse_shorts/embed/).
- Stickocalypse growth check: on 19 Oct 2026 a third party recorded 35,600 subscribers and 4.2M views on Part 1 (vs 43.1K and 6M on 31 Oct) [3P] — [vuela.ai](https://vuela.ai/blog/how-to-make-viral-stick-figure-series-with-ai).
- Stickocalypse runs official language versions that credit the English original ("Официальный русский аккаунт Stickocalypse … English: @stickocalypse_shorts"; Spanish "Original en inglés: @stickocalypse") [FH via search snippets] — [tiktok.com/@stickocalypse_ru](https://www.tiktok.com/@stickocalypse_ru), [tiktok.com/@stickocalypse_es](https://www.tiktok.com/@stickocalypse_es).
- A separate copycat account "pickocalypse_shorts" posts "THE LAST FARM — Part 1 … Follow for Part 2" with the same premise — [tiktok.com/@pickocalypse_shorts](https://www.tiktok.com/@pickocalypse_shorts/video/7696072789014482197).
- Vuela's description of the original format: parts of 60–100 s, side-view stick figures, flat colour layers with fog, third-person narrator, burned-in captions, cliffhanger endings, shot change every 2–3 s [3P] — [vuela.ai](https://vuela.ai/blog/how-to-make-viral-stick-figure-series-with-ai).

### Inferences
- The adaptation is a translated and re-rendered re-telling (same premise — "would this farm be enough to survive?" → Thai durian orchard, farmer + dog), not a re-upload: visuals are regenerated as code-drawn SVG, narration is Thai AI voice, and the HUD/fact layer is Prompt KUB's addition.
- The Thai version (2.68M IG views by 25 Oct) is roughly 45% of the original Part 1's 6M YouTube views as of 31 Oct; both were growing in the same fortnight, implying the Thai clip rode the same global wave rather than a lagged repost.
- Originality risk: the permission claim is unilateral (no statement from Stickocalypse found); because Stickocalypse operates official RU/ES versions that credit the EN original, an authorised TH version is plausible, but the risk remains that the channel's breakout clip and course "proof" rest on borrowed IP. Subsequent series (450 กิโลถึงบ้าน, 30 วัน ห้ามเปิดไฟ, เรือด่วน, รถไฟฟ้า) appear original in premise, though one title credits another inspiration ("หมอกในร้านสะดวกซื้อ").

### Gaps
- Exact number of สวนสุดท้าย episodes (≥3 confirmed via alt text) and their individual performance are unknown; the series is not on YouTube under that name.
- No public acknowledgement from Stickocalypse of the Thai adaptation was found; Stickocalypse's own posting dates (e.g., when Part 1 went live) could not be read because YouTube blocked further watch-page requests.

## Q6. What the ygnos.com course reveals about workflow, tools, goals and business model

### Takeaway
The owner monetises the channel three ways — ฿650/฿1,250 online courses ("THE ORCHARD METHOD"), a ฿6,790 one-day Bangkok workshop ("ZERO TO VIRAL / 1M Club", first run 24 Oct sold out, EP.2 on 7 Nov 2026) and brand-placement clips at ฿6,500–฿25,000+ per clip posted on @promptkub — with a declared pipeline of Claude Code + HyperFrames (SVG rigs, HUD), Magnific AI (Thai voice-over and music), subtitle timing from script, multi-agent shot generation and 4K render, all sold by บริษัท วีเพย์ โพรฟิต จำกัด while the channel itself stays free on Instagram.

### Cited Findings
- Curriculum "4 บท 8 ตอน": Module 01 คิดเรื่อง (01 ทำไมคลิปนี้ทะลุครึ่งล้านวิว สูตร 6 ข้อ; 02 เครื่องยนต์เรื่อง: ปัญหา ข้อเท็จจริง ปัญหาใหม่ และความเป็นต้นฉบับ); Module 02 เสียงและจังหวะ (03 เสียงพากย์ AI ภาษาไทยที่ไม่สะดุด; 04 ซับตรงปาก: จาก script สู่ timing); Module 03 ภาพ (05 ชุดหุ่น SVG ฉาก และ HUD ด้วย HyperFrames; 06 แตกช็อต แล้วให้ AI หลายตัวทำพร้อมกัน); Module 04 เสียงประกอบและส่งงาน (07 เพลง เสียงประกอบ และการมิกซ์; 08 ตรวจงาน เรนเดอร์ 4K และโพสต์) [OWNER] — [ygnos.com](https://ygnos.com/).
- Tools and costs: "ภาพสร้างด้วย Claude Code และ HyperFrames ส่วนเสียงพากย์และเพลงใช้ AI ของ Magnific ค่าบริการ AI เหล่านี้ไม่รวมอยู่ในราคาคอร์ส"; requirement "บัญชี Claude Pro ราว US$20 ต่อเดือน จ่ายกับ Anthropic โดยตรง … แผนฟรีใช้ทำตามคอร์สไม่ได้"; "คอมพิวเตอร์ Windows หรือ Mac เพราะต้องติดตั้งโปรแกรมและเรนเดอร์คลิปบนเครื่อง" [OWNER] — [ygnos.com](https://ygnos.com/). The workshop page adds "ต้องมีบัญชี Claude Pro (ต้องเป็น Claude Pro เท่านั้น)" and "AI ช่วยคิดเรื่อง เขียนบท และทำเสียงพากย์ภาษาไทย … สร้างภาพแอนิเมชัน ซับ เพลง และเสียงประกอบด้วย AI" [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop).
- Pricing: "SURVIVAL KIT (฿650) • PLAYBOOK PDF 36 หน้า • Full Prompt Guide ทุก prompt"; "MASTERCLASS (฿1,250) • ทุกอย่างใน SURVIVAL KIT • คอร์สวิดีโอ UI สอน 22 บท (บทเริ่มต้น 14 + บทหลัก 8) พร้อมเสียงผู้สอน • โมดูลสอนสร้างรายได้จากการทำเพจ AI แบบนี้"; access "เข้าเรียนได้ 2 ปี" [OWNER] — [ygnos.com](https://ygnos.com/). Hub adds "FIGMA WEB CLASS ฿220" and "Prompt Guide with 33 prompts used in real clips" [OWNER] — [ygnos.com/hub](https://ygnos.com/hub).
- Workshop: "ZERO TO VIRAL EP.2 | คลาส 1M Club · เวิร์กช็อป AI 1 วัน", "เสาร์ 7 พ.ย. 2569 · 09:30–16:30", "Ascott Embassy Sathorn Bangkok", "20 ที่นั่ง", "EXTRA SEAT ฿6,790", "รอบแรก 24 ต.ค. เต็มแล้ว", "ผู้สอน 3 ท่าน ทีมงาน 2 คน"; three skills: viral AI clips, "ปั้นเพจจาก 0 ด้วยเคสจริงของ @promptkub", "เว็บระดับ Figma ด้วย AI" deployed on Vercel [OWNER] — [ygnos.com/workshop](https://ygnos.com/workshop). The IG-story alt text quotes a different price "4,590 บาท" [OWNER] — same page.
- Brand packages (ex-VAT): CAMEO ฿6,500/clip (product in 2–3 shots); THE FIX from ฿12,500 (product = the character's way out, narrator names product, HUD cards with real product numbers, 7- and 30-day reports); DEDICATED from ฿25,000 (first trial ฿20,000); STUDIO custom; 15-second cut ฿3,000; 10% off 3+ clips; all clips 60–70 s, posted on @promptkub with Paid partnership label, 2 revisions, buy-out asset file; production "เสร็จภายใน 1 วันหลังสรุปบรีฟ" [OWNER] — [ygnos.com/brand](https://ygnos.com/brand). Excluded categories include alcohol, tobacco/vapes, gambling, crypto/guaranteed-return investments, unregistered health products [OWNER] — same page.
- Positioning line: "สินค้าของคุณ = ทางรอดของตัวละคร"; brand site name "THE WAY OUT" [OWNER] — [ygnos.com/brand](https://ygnos.com/brand). First paid case: "Peaceful Day × Prompt KUB … แอนิเมชัน 72 วินาที · ซับไทย + อังกฤษ · งานที่แบรนด์จ้างจริง · ลงที่ IG @promptkub", closing line "อย่าพักให้ไกล พักให้บ่อย" [OWNER] — [ygnos.com/work/peaceful-day](https://ygnos.com/work/peaceful-day).
- Free-channel stance: "ตอนหลักดูฟรีเสมอ ซัพพอร์ตแล้วได้วิธีทำ … ผู้เรียน MASTERCLASS ได้ดูเบื้องหลังทุกตอน และเราสอนวิธีทำจริงทุกขั้น ไม่เก็บเป็นความลับครับ" [OWNER] — [ygnos.com](https://ygnos.com/).
- Seller/legal: "จำหน่ายโดย บริษัท วีเพย์ โพรฟิต จำกัด", payment by bank transfer with automatic slip check [OWNER] — [ygnos.com](https://ygnos.com/); registry: VPAY PROFIT COMPANY LIMITED, reg. 0225562000413, registered 13 Mar 2019, capital ฿1M, Chanthaburi [3P] — [dataforthai.com](https://www.dataforthai.com/company/0225562000413/).
- Mascot/persona: the hub page refers to the brand mascot "น้องคับ"; no individual instructor is named on any page [OWNER] — [ygnos.com/hub](https://ygnos.com/hub).

### Inferences
- The site went from channel launch (≈23 Sep) to a full course + workshop + brand-deal funnel within ~4 weeks (first paid workshop 24 Oct), and every stat on the site is framed as sales proof; the channel's growth is thus partly a lead-generation asset for a ฿650–฿6,790 education business and a ฿6,500–฿25,000 sponsorship business, not purely an audience play.
- Potential revenue scale [DERIVED]: a sold-out 20-seat workshop at ฿6,790 ≈ ฿135,800 gross per run; course prices are deliberately low-ticket.
- The stack is code-first (Claude Code writing SVG/HyperFrames scenes) rather than generative-video (no Veo/Kling/Runway named for the storytelling era), which explains the consistent flat vector look and the "1 day after brief" turnaround claim.

### Gaps
- ElevenLabs and Whisper were mentioned in the coordinator's brief but do not appear on any ygnos.com page fetched (only Magnific is named for voice/music); they may be inside the paid playbook, which was not accessible.
- Course sales volumes, revenue, and the instructor's identity are not disclosed.

## Q7. Press, podcasts, Facebook groups, Pantip/Blockdit or news coverage of Prompt KUB's growth

### Takeaway
No press, podcast, Pantip, Blockdit, Thai news or AI-community coverage of Prompt KUB or "สวนสุดท้าย" was found; the channel's growth story exists online only on its own ygnos.com pages, and searches for its clip titles returned nothing, so the channel is still below the radar of indexed Thai media despite ~75M claimed views.

### Cited Findings
- Searches for "promptkub", "Prompt KUB พร้อมท์ครับ AI", "สวนสุดท้าย AI แอนิเมชัน promptkub", "ตัวอย่างงาน AI โดย Prompt KUB", the clip titles "ชาเย็นก่อนลงดอย / ค้างภู EP.1 / ถ้าซอมบี้ระบาดหนัก", "30 วัน ห้ามเปิดไฟ / 450 กิโลถึงบ้าน / เรือด่วนเที่ยวสุดท้าย", and "promptkub pantip OR facebook OR blockdit" returned only ygnos.com, the YouTube channel and unrelated pages (an unrelated prompt-marketplace promptkub.com, crypto converters, Kubernetes tools) — e.g. [ygnos.com](https://ygnos.com/), [youtube.com/@Promptkub/shorts](https://www.youtube.com/@Promptkub/shorts), unrelated [promptkub.com](https://promptkub.com/).
- The only external write-up touching the format is Vuela's 19 Oct 2026 article on Stickocalypse, which does not mention Prompt KUB [3P] — [vuela.ai](https://vuela.ai/blog/how-to-make-viral-stick-figure-series-with-ai).
- The Facebook page "Prompt Kub" exists but shows only a login wall — [facebook.com/Promptkub](https://www.facebook.com/Promptkub).
- Note: an unrelated "promptkub.com" (AI prompt marketplace, domain listed for sale at $195) shares the name and pollutes search results — [promptkub.com](https://promptkub.com/).

### Inferences
- Discovery is almost entirely in-platform (Instagram Reels distribution), with the owner's own site as the sole narrative source; competitors could not learn the growth story from media, only from the ygnos pages.

### Gaps
- Facebook groups and closed LINE/Discord communities are not searchable; mentions there may exist.
- The session's web-search budget was exhausted before Thai news sites and Lemon8 could be searched exhaustively.
