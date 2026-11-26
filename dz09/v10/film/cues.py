"""cues.py -- picture cues of the finish (film seconds).  The on-screen graphics are the flat v13 status strip
(PROJ/v13/icons, top-left row; its word-synced cues come from audio/narr_ohm/captions_timing.json + 0.30 s and its
picture cues are fixed: battery 16.30 / 16.50 / 16.70, radio cut 3.243, screen dark 31.75, red eye 41.657, lunge 43.445,
title 50.72).  The v12 gauge tubes, the phone-voice badge and the v12 title mark are gone (v3)."""
STATIC = (3.243, 3.393)                                    # radio dies
LUNGE_FLASH = 43.445 + 2.0 / 24                            # S21: the frame the driver bursts out of the door (g 1045): one white / red frame
BITE = 43.795                                              # scream / bite flash
TITLE = 50.72
HARD_CUTS = {"S21", "S22"}                                 # shots that START on a hard cut (everything else joins with a blurred push)
# the icon strip's box in frame fractions (9:16): nothing a principal's FACE does may enter it
STRIP = dict(x0=0.05, x1=0.80, y0=0.08, y1=0.19)
