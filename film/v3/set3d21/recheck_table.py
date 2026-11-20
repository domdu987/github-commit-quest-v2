#!/usr/bin/env python3
"""camp_table re-check: renders the tile with Cressingham and without (the empty ending table) -> styleboard/table_with.png, table_empty.png, table_pair.jpg (phone size)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, stirling as K
from PIL import Image
out = []
for ph, nm in ((True, 'table_with'), (False, 'table_empty')):
    A = K.build_for_cli('camp_table', placeholders=ph); K.STATE['preset'] = 'camp_table'; f = os.path.join(HERE, 'styleboard', nm + '.png'); dt = K.render(f, 'final', 40); print(nm, round(dt), flush=True); out.append(Image.open(f).convert('RGB').resize((360, 640), Image.LANCZOS))
S = Image.new('RGB', (728, 640), (18, 18, 22)); [S.paste(im, (i * 368, 0)) for i, im in enumerate(out)]; S.save(os.path.join(HERE, 'styleboard', 'table_pair.jpg'), quality=92)
