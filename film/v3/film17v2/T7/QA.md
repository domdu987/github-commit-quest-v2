# T7 QA self-check (g1689-1874, 186 frames, 720x1280, 16 samples + OIDN)

Checks: `check_take('T7')` no hits, `check_face('T7')` PASS. Render: motion blur 0.5 on g1800-1867 only; clear_cast() before every stage_cast2 (cast-object leak fix); beam_fx forced to 0 for the whole take (g1820 beam-0 diff was 9.5/255: the beams veiled the crane; g1730 diff 0.0).
Luma (director metric: RGB mean at 90x160): take 103.8 (min 79.7, max 162.1). 7a g1689-1791: 96.2. Crane g1792-1874: 113.1 (top-down floor is bright, peak ~130-162 at g1810-1830); the target 88-105 is met by the take mean and 7a, not by the crane alone (director: overage is trimmed at conform). Shimmer: frame-to-frame flat-wall diff 0.47 grey levels on the first 30 frames, no OIDN shimmer seen.

## Frames viewed (full 720x1280 unless stated; phone = 360x640)
- **g1718 (full):** Bertillon centre-left holding the card up, Dupont right, fully inside the frame, big bushy brown beard on, surprised mouth. Nothing crosses Bertillon. Feet on the floor.
- **g1750 (full):** the beard is sliding down over Dupont's chest and shrinking; his mouth is open and clean above it. The card is unchanged.
- **g1760 (phone):** Dupont clean-shaven and smirking, Bertillon holding the card. Both readable.
- **g1795 (phone):** Bertillon fist up (triumphant), eyes closed, no card; Dupont smirking. A figure is cut by the right edge (gend_b).
- **g1830 (full):** crane in motion with strong blur. The MOYEN banner fills the middle of the frame, cut off at both edges ("MOYE"). Above it the group at the GRAND end is visible; below it, sparks and cards. Flying cards read only as small paper bits.
- **g1850 (phone):** top-down hall. ARCHIVES, GRAND and MOYEN banners upright and readable, the marching line on the carpet, cards and drawers around. The vault is cut away so the sides of the frame are dark navy.
- **g1860 (full):** top-down, banners upright. The marching gendarme and thieves are small, 1-3 % of frame height (planned crane path).
- **g1874 (phone):** the final high top-down frame, banners upright (PETIT visible), line of figures on the carpet.
Also viewed: a contact sheet of 12 frames (g1692-1874), no veil and no shaft wedges seen.

## Known issues (not hidden)
- qa_auto FAIL: "suspected blur" on 24 frames from g1800. This is the planned 0.5 motion blur on g1800-1867. It also flags the crane's fast camera as pops (g1796-1825 and later), also planned.
- qa_auto notes the planned cuts (g1695, g1868) show no change within 2 frames, because they are the take boundaries and the render range starts 6 frames before the cut. Rhythm: median 1.27, p90 22.28 (the crane drives p90).
- Thieves and the escort are tiny in the top-down frames, and the pop-open drawers show as yellow slabs; I saw no calipers.
- The moustache reads mostly as part of the beard (same dark brown).
