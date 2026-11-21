#!/usr/bin/env python3
"""ghost_shot_table.py : the SHOTS rows (see ghost_shots.py for the move model).  Local coordinates of each location."""
from ghost_shots import shot, C, M_

# ============================================================================= FIELDS (dawn)
# S01 BIGZOOM 1: extreme wide bird's-eye (column < 5 % of the frame height) -> descend + push along the lane past the poplars -> medium on the
# lead tank (col0 at (-18, -20), heading SSW, towed by a jeep), a soldier on its rear deck waves the column on.
shot(1, 0.00, 4.00, 'FIELDS', 'DAWN', C((-3, -118, 1693), (-3, 30, 0), 24),
     dict(path=[(0.0, C((-3, -118, 1693), (-3, 30, 0), 24)),
                (0.42, C((-110, -200, 230), (-10, 0, 0), 24)),
                (0.78, C((-62, -76, 24), (-17, -17, 1.5), 24)),
                (1.0, C((-31.5, -29.5, 4.4), (-17.0, -18.0, 3.0), 24))]),
     note='BIGZOOM 1: extreme wide high over the patchwork, descend + push along the lane past two poplars, end medium on the lead tank',
     marks=dict(rider=[M_(-18.0 + 2.6, -20.0 + 0.7, pose='wave', z=3.9, parent='col0')],
                walkers=[M_(-23.6, -17.0, pose='wave'), M_(-19.0, -4.0, pose='stand')]),
     state='column=0')
