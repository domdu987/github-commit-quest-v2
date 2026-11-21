# QA-art sH1 (film-13 QA, 5d1d82b)
Take: gate/sH1/film/v3/film21/sH1/take.mkv (v4, g1239-1348, 110 frames). Viewed: the 1 fps sheet, every 5th frame, all frames g1300-1348 (full size at the slam, g1327 and g1346), H1 vs H2a (take frames 0-11, g1342-1353) side by side at g1342-1348, per-frame diff numbers, face-white row scan against y 880, a solid-black block scan. Colour and exposure are left to the conform.

## Verdict: FIX-FIRST (one small render fix; the three earlier blockers are fixed)

| earlier blocker | v4 |
|---|---|
| B2 handle camera vs H2a, g1338-1348 | FIXED. Same pose and path on every handle frame (mean diff H1 vs H2a 4.1-4.8 at g1342-1345, 6.6-8.8 at g1346-1348 against 29-38 of camera motion per frame; the residue is the wall content, see N1). |
| B3 grey "gravestone" bodies over the Scots cards, g1317-1330 | FIXED. The camera-side ranks are blue Scots cards with faces and level spears; the 3D bodies stay behind them. The slam reads (g1316-1322). |
| B4 chins below y 880, g1329-1336 | FIXED. Lowest face-white row is y 853 (g1330-1332); all faces above 880 through g1345. |

## Blocking
**B5, g1311-1314 and g1324-1328: solid black rectangles at the right edge of the slam.** Pure black (RGB < 10) blocks about 25-50 x 25-60 px at x 640-720, y 555-680, right beside the English faces (clearest at g1313, g1314 and g1327, where a 35 x 50 px black box sits between two helmeted heads). It is a render error, not a shadow: likely a card with no image or no alpha on those frames (check the pop helmet cards, the right-edge English card e9 and any 3D body with no material). Fix: find the object at those pixels (object-index pass or click-select in Blender at g1313 and g1327), give it its image/alpha or hide it, and re-render g1309-1330. Check: no 10x10 pure-black block outside hair and moustaches anywhere in the take.

## Non-blocking
- N1 (for H2a, not H1), g1342-1348: H1's wall has card faces, H2a's still shows the navy slabs. In the D6 the Scots faces fade into a navy band during the crane-up. It is small and fast, so it does not block; the clean fix is for H2a to copy H1's two card ranks (the call is in sH1 QA.md) on g1342-1357. H2a g1346 also has the front Englishman's face at about y 1000-1080 for one frame (inherited from H2a's camera, mostly H2a in the blend).
- N2, g1317-1327: the dust puffs form a continuous row of tan lumps in front of the Scots legs, reading like sandbags. Make them break up: varied sizes, expand and fade within 4-6 frames.
- N3, g1306-1310: the gorse wipe is a flat green polygon filling up to the whole frame; a textured or leafier shape would help (deliberate pass, kept).
- Carried: saltire banners still near-black navy (set item), English still wear the painted helmet after the pop.

## Scores
set density/ornament 7 / lighting and colour 7 / composition and framing 7 / character acting 8 / key moment (the reveal) 7 / match to references 7. Phone legibility: charge 8, slam 7, spear wall 7, English reaction 7.
