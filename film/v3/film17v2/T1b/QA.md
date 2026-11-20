# T1b QA self-check (film 17 v2, take T1, g172-342)

Render: 171 frames, 720x1280, 30 fps, 16 samples + OIDN, adaptive 0.03. Motion blur 0.5 on g172-278 only. Cast: real cast17 cards through `stage_cast2` on every frame, with `clear_cast()` (the stale-actor leak fix) before every call. Mouths closed everywhere (no quote window in T1).
`take.mkv`: libx264 crf 14, 10.5 MB (no split).

## Numbers (qa_stats2 metric: 90x160 bilinear, mean of R, G, B)
- Part mean **117.9**, min 108.6 (g295), max 145.9 (g178). Target 95-112, so it is over. The director ruled to keep as is and trim at conform.
- By 20-frame block: g172 131.4, g192 112.4, g212 113.5, g232 116.3, g252 122.9, g272 118.2, g292 112.9, g312 115.3, g332 117.9.
- Near-black area (max channel < 12): 0.00 % on every frame (no slabs). White (all channels >= 250): max 1.27 % (g276). Blue channel pinned at 255 on 25-36 % of pixels (cobalt surfaces), accepted by the director.
- Largest frame-to-frame luma jump 6.5 (g178 to g179).
- `rhythm.py`: in-shot median 10.88, p90 33.18 (target >= 4 / >= 12).
- `qa_auto.py` result: **FAIL**, reason "suspected blur on 21 frames, e.g. g173-187". That is the planned shutter-0.5 motion blur on the crane (g152-278). It is expected there. Other notes: the planned cut at g336 shows no visible change within +-2 frames (this part ends there; g337-342 are handles), magenta share 0.0 %.

## Façade sign rule
PRÉFECTURE DE POLICE whole and readable, cap height >= 28 px: by projection plus a raycast for occluders, g249-274 (26 consecutive frames). I looked at g262 at full size: the whole band is in frame, readable, cap about 35-45 px. Changes made for this: camera key k255 replaced by a hold key at g269, and the door-arch stones shrunk so they no longer clip the letters. Both are in `prefecture17.py` on this branch.

## Frames viewed (full 720x1280 and the same frames at 360x640)
- **g180:** crane pull-out at the façade with heavy planned motion blur. The sign is huge and blurred ("PRÉF" legible), a street lamp swings through the lower right, a small dark figure group is visible in a lit window at left. At phone size the blur reads as a fast move and the sign is still legible.
- **g215:** high crane top over the street. The balcony hides the sign (expected, the sign window starts g249). Wagon, gendarmes, citizens, lamps and a pale refuge island are visible; cards stand on the pavement and cobbles. An inverted figure near the lamp base is a puddle reflection, I believe (not isolated). At phone size the cards are tiny but readable as figures.
- **g262:** inside the sign window. Whole band readable, two door gendarmes front-on at the door, a green gendarme at left, sentry box and lamp, barrel. At phone size the lettering is clearly readable.
- **g295:** low street view past a foreground lamp post (large dark blue column at left, an accepted foreground prop). Wagon, a prisoner with a green gendarme beside him (both front-on, mouths closed), a puddle reflecting the wagon. PRÉFECT... cut by the top edge, as in the planned swoop.
- **g322:** the prisoner, a green gendarme and a blue gendarme at the right in front of the door, all front-on. The blue gendarme's head is cut by the right frame edge (about 40 % of the face is out). The sign shows "PRÉFEC" at top, cut by the frame.
- **g342 (handle frame, after the planned cut at g336):** same setup, the right gendarme's head is again cut by the right edge, a second kepi is visible beyond the edge. This follows the prepared camera and staging, so I did not change it; the director should decide.

## Not verified
- I did not watch the full clip for OIDN shimmer, only a g199/g200 crop (smooth) and the frames above.
- The inverted figure near the lamp base in g215 and the key still g230 is assumed to be a puddle reflection; the director said it is fine as is.
