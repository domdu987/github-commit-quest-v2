# T7 QA self-check, fix round 2 (g1689-1874, 186 frames, 720x1280, 16 samples + OIDN)

Checks: check_take('T7') no hits, check_face('T7') PASS. Motion blur 0.5 on g1800-1867 only. clear_cast() before every stage_cast2. beam_fx off for the whole take.
Fix round 2 (round 3 timing): lights ramp 1.0 to 0.72 over g1796-1806, hold to g1838, back to 1.0 by g1850; the Dupont stool was removed (not moved or seated); banners within 2.4 m of the camera are hidden; the MOYEN banner is hidden from g1823 to the end of the take; Bertillon has a card bob and head roll.
Luma (RGB mean at 90x160): take mean 95.8 (min 73.0, max 104.4). 7a g1689-1791: 96.7 (94.1-98.3). g1800-1812: 101.8-104.4. g1809-1839: 102.6 (101.1-104.4). Under 88 only at g1852-1867 (73-87): the top-down end is dark with the lights at 1.0, because the ramp already reached 1.0 by g1845 in the previous render and those frames did not change. g1868-1874 are handle frames (81-80) with the original lighting and the stool kept. Shimmer was not re-measured.
qa_auto still FAILs on blur (57 frames) and pops (g1797-1806, 1828, 1829, 1833): the planned motion blur and the fast crane. rhythm.py reports 0 cuts detected.
Known caveats: the thieves and escort are tiny (1-3 %H) in top-down frames; the moustache reads mostly as part of the beard.

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
