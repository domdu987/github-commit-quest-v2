# film17 s01 (shots 1-3, hook) QA, round 2 (after gate round 1)
- 720x1280, 16 samples + denoise, ~55 s/frame; g 0-143 + 6 handle frames (144-149); cuts at g 48, 93.
- rhythm (rhythm.py --cuts 48,93): in-shot median 6.22, p90 14.31 (target >= 4 / >= 12).
- qa_auto: PASS, magenta 0 %; soft frames g131-132 = the whip's motion blur (intended).
- Fixes vs round 1: shot 1 calipers held in Bertillon's hand, jaws closing on the near ear g14-40 (sliding jaw animated), headrest pad moved behind the head (sitter card 0.14 m toward camera), Bertillon stands on the dais (coat skirt solid), beam_fx shafts hidden (director's systemic fix), mouths wrapped in silent(), dust k=0.3.
  Shot 2: 3 prisoners on the bench + gendarme mid-room (door cannot share the frame with the bench at 22 mm), gas lamp enters at the right third, room stool/ledger pile deleted from the room mesh, wide pull-out then a 13-frame snap in (g60-73) onto Bertillon + sitter.
  Shot 3: low raking near-profile on the ear (camera ~0.2 m below ear, swung ~60 deg), jaws straddle the ear, Bertillon's hand visible, one eye visible; 18-frame whip g118-136 with camera motion blur, sitter swap prisoner_a -> prisoner_c at g127 (peak of the whip); stray disc gone.
- Known limits: jaws open along the beam so they straddle the ear front/back (director accepted); in shot 1 the jaws only partly reach the ear (solver err ~0.4 D); the gendarme is not at a door; cartoon ears are a sprite underlay (puppet has none).
- Full-res frames for the re-check: full/g15 g40 g70 g105 g135 .png. Reassemble: cat take.mkv.part* > take.mkv
