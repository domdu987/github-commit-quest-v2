# POST QUEUE — คิวคลิปรอโพสต์ (อ่านโดย AI extension ทุกชั่วโมง)

## คำสั่งสำหรับ AI ที่มาอ่านไฟล์นี้ / Instructions for the posting agent
1. Look at the table below. Take rows whose status is `READY`, oldest first. Post at most **1 clip per check**.
2. **Before posting, prevent duplicates:** open YouTube Studio → Content and search for the exact **Title**.
   If a video with that title already exists, the clip is already posted: skip it (and mark it POSTED, see step 5).
3. Download the video from the **Video** link. Chrome must be logged in to GitHub; the repo is private.
4. Upload it as a YouTube Short, vertical 9:16, about 60 s.
   - Title = the **Title** column.
   - Description = the full caption text under that clip's heading below.
   - Audience: "No, it's not made for kids".
   - Visibility: Public.
5. After it is published, edit this file on GitHub (pencil icon) and change that row's status from `READY` to `POSTED <date>`. Commit directly to the same branch.
6. If a captcha or "verify you are human" appears: STOP, do not try to solve or bypass it, and tell the owner. If another error happens (upload error, file picker blocked), do NOT retry more than once. Leave the status as `READY` and stop until the next hour.

Branch: `claude/new-session-73ou27`. Only rows with status `READY` may be posted. `WAIT` means not finished yet.

| # | Film | Title | Video | Status |
|---|---|---|---|---|
| 10 | ไอ้ช่างม้าลาย | (filled in when ready) | (link when ready) | WAIT |

## Captions
(Each READY clip gets a heading here, `### <#> <Title>`, followed by the exact description text to paste.)
