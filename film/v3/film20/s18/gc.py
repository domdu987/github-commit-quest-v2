"""ground check driver for s03: python3 gc.py [extra ground_check args]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
extra = sys.argv[1:]
sys.argv = ['shot.py', 'x']
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
import shot, bpy
import ground_check as GC
import re
def _sp(node, frame):
    p = bpy.path.abspath(node.image.filepath)
    d, b = os.path.split(p)
    return os.path.join(d, re.sub(r'_\d+\.png$', '_%04d.png' % int(frame), b))
GC._sprite_path = _sp
Tk = shot.Take("preview")
gs = list(range(1361, shot.G_LAST + 1, 8))
Tk.pose(gs)
args = ['--frame-list', ','.join(str(shot.bf(g)) for g in gs), '--out', os.path.join(HERE, 'GROUND.md')] + extra
for n in ('bz_glow','bz_shaft','bz_up','beacon_beacon_g'):
    o = bpy.data.objects.get(n)
    if o is not None:
        o['gc_role'] = 'skip'
for o in bpy.data.objects:
    if o.name.startswith(('hut_', 'wagon_', 'antenna_fix', 'team8_fg_lamp', 'team8_keybase')):
        o['gc_role'] = 'skip'      # merged set meshes / wire stay / lamp head; verified by eye
    if o.name.startswith('tel_'):
        o['gc_gap'] = 0.3          # seated at the desk: sits on the hidden seat box (FLOOR_Z + SEAT_H)
GC.run_cli(args)
