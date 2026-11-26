"""User decision (after seeing v13 row, v14 cards, v15 pictograms): NO status icons in the film.
Only the biohazard title mark stays, from the title hit on (drawn by v13/icons/icons13, which is unchanged).
Same API as icons13 so finish.icons() can use it."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "v13", "icons"))
import icons13 as _I

T, LAYOUT, cue_table, close = _I.T, _I.LAYOUT, _I.cue_table, _I.close
G_TITLE = int(round(_I.T.TITLE * 24))                      # 1217: first frame of the title hit


def overlay(g, W, H, aspect="916"):
    return _I.overlay(g, W, H, aspect) if g >= G_TITLE else None


def over(rgb, g, aspect=None):
    return _I.over(rgb, g, aspect) if g >= G_TITLE else rgb
