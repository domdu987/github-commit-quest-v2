# film17 s07 (shots 16-19) team 1 rework, g 844..1051 (first_g 844, 208 frames)
- g844-899 (shot 16): team 6's frames from 34bb2c8, unchanged. g900-1051: 3D inserts rendered here (720x1280, 16 samples + denoise), one location (measure room) + props built in shot.py; hard cuts 900/924/948/972/996.
- rhythm.py --cuts 900,924,948,972,996: in-shot median 7.88, p90 23.15. qa_auto PASS, magenta 0 %; soft frames g940-947, g976 are flat close-ups (floor/leather), sharp lines by eye.
- Mouths: 18a puppets wrapped in cast17.silent(); beam_fx shafts hidden; dust k 0.3; no motion blur anywhere (no whips).

## What each self-check frame shows (full res in full/)
- g910 (17a): gloved hand (cream glove + navy sleeve) grips the right end of the caliper bar; the thief's hand lies flat on the wooden gauge with the middle finger along the ruler; the sliding jaw is still open ~0.1 m from the fingertip.
- g920 (17a, not in full/): the sliding jaw plate touches the fingertip, the fixed jaw plate sits at the knuckle; glove still on the bar.
- g935 (17b): boot on the foot board, ruler with ticks, the walnut block with the gloved fist on its brass handle sliding toward the toe.
- g945 (17b): the block face touches the toe cap; glove on the handle.
- g960 (18a): prisoner_b in near-profile, the caliper jaws straddle his ear, Bertillon's gloved hand + sleeve on the bar (s01 S3A setup).
- g985 (18b): plain pen (no fletching) held by the gloved fist, nib on the card; rows of drawn marks appear as the nib sweeps (no readable text).
- g1005 (19): the glove holds the card above the pulled-out medium drawer (cards already inside).
- g1015 (19): the card has gone down behind the drawer front (not visible), glove lifting away; the medium drawer then closes g1022-1032.
- g1045 (19): pulled back: three drawer sizes (large ~180x120 px, medium ~105x70 px, small ~50x35 px), many drawers ajar with cards standing in them.

## Known weak spots
- Table inserts (17a, 18b) leave the lower third as empty table top; the hand/finger blobs are simple capsules; the glove is a cartoon blob with a thumb bump.
- 17b boot is a plain brown boot; 17b lower half is floor planks.
- The card in 19 vanishes by going down behind the drawer front (as the cards do in a card index); the glove arm is a long diagonal sleeve.
- g844-899 are team 6's frames (not re-checked here).

## R5 (after QA-tech R4): re-rendered g900-1051 (shot 16 frames g844-899 still team 6's)
- rhythm 6.92 / 23.15 (--cuts 900,924,948,972,996); qa_auto PASS, magenta 0 %, no soft frames flagged.
- B1 sleeve: the glove sleeves (17a, 17b, 18b pen, 19) are now ~2.5 m long and leave the frame (from lower right in 19); no free tube end in g1024-1046.
- B2 hand: 17a hand = cuffed jacket sleeve from the left frame edge, wrist, palm, thumb, three curled fingers and the middle finger along the ruler, jaw touching the fingertip at g920; gloves inside the frame. 17b boot = side-profile boot with laces, heel, sole line, ankle shaft + trouser leg rising out of frame; the block touches the toe from g945; glove with cuff and sleeve rising out of frame.
- Should-fix: samples 28 on g900-995 (moire reduced); card sinks to just behind the drawer front (no stray edge); wastebin removed from the cabinet (blue stub gone); chair near armrest + foot rail removed from the set mesh (orange plank mostly gone, a small bit of the chair foot still shows at the bottom-left in 18a).
- Still weak: lower third of 17a/18b is empty table top (the ledger/ink props sit below the frame); simple cartoon hand/glove.
- Full-res check frames in full/: g910 g915 g920 g935 g940 g945 g960 g985 g1005 g1015 g1030 g1040 g1045.
