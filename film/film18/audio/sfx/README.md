# Film 18 SFX
fal.ai balance was exhausted on 2026-11-19 22:58 UTC, so gen_sfx.py (the film-18 library: moo, herd gallop, bronze pots, ignite, panic...) could not run.
Fallback: reused sounds from films 4-10 (copied here). Missing true matches: ox moo, herd gallop (stand-in: quake + running), bronze pots (stand-in: hammer + bells), reed ignite (stand-in: fuse).
When the client tops up fal.ai, run `python3 gen_sfx.py` here and the conform uses the new files automatically (same names where they exist).
