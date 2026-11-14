"""Keyed hooks test + hook stills (preview 360x640): python3 louvre_work/t_anim.py
Checks the values between keys, then renders one still per hook state into louvre_work/hooks/ and a sheet hooks.jpg."""
import sys, os; HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import louvre as L, bpy, math
from mathutils import Vector
sc = bpy.context.scene; out = os.path.join(L.WORK, 'hooks'); os.makedirs(out, exist_ok=True); ok = True
def chk(name, cond):
    global ok; ok &= bool(cond); print('%-48s %s' % (name, 'ok' if cond else 'FAIL'), flush=True)
def at(f): sc.frame_set(f); bpy.context.view_layer.update()
shots = []
def still(tag, A, cam=None):
    L.setup_render(sc, 'preview'); cs = A['cams'][cam or A['cam_name']]; L.make_camera(cs); L.stage_placeholders(A, cam or A['cam_name'], cs['loc'])
    p = os.path.join(out, tag + '.png'); L.render(p); shots.append(p)
# --- gallery: Mona present -> lifted -> gone
A = L.build('louvre', 'wall_eye'); S = L.STATE
L.set_mona(True, frame=1); L.set_mona_lift(0.0, frame=1); L.set_mona_lift(0.8, frame=30); L.set_mona(False, frame=40); L.set_flames(1.0, frame=1); L.set_flames(1.0, frame=40)
at(15); z15 = S['mona']['pivot'].location.z; at(30); z30 = S['mona']['pivot'].location.z
chk('mona lift eases between keys', S['mona']['pivot']['wrest'][2] < z15 < z30)
at(35); chk('mona visible at 35', not S['mona']['objs'][0].hide_render and S['mona']['patch'].hide_render)
at(45); chk('mona gone at 45, patch shown, hooks stay', S['mona']['objs'][0].hide_render and not S['mona']['patch'].hide_render and not S['objects']['mona_hooks'].hide_render)
at(1); L.clear_keys(); L.set_mona_lift(0.0); still('mona_present', A)
L.set_mona_lift(0.5); still('mona_lift_0.5', A)
L.set_mona(False); still('mona_gone', A)
# --- street papers
A = L.build('paris', 'kiosk'); L.set_papers(0, frame=1); L.set_papers(12, frame=20); L.set_papers(24, frame=40)
at(10); n10 = sum(not o.hide_render for o in L.STATE['papers']); at(25); n25 = sum(not o.hide_render for o in L.STATE['papers']); at(41); n41 = sum(not o.hide_render for o in L.STATE['papers'])
chk('papers 0 -> 12 -> 24 (%d %d %d)' % (n10, n25, n41), (n10, n25, n41) == (0, 12, 24))
at(1); L.clear_keys(); L.set_papers(0); still('papers_0', A); L.set_papers(8); still('papers_8', A)
# --- exit door
A = L.build('louvre', 'exit_door'); L.set_door(0, frame=1); L.set_door(90, frame=31)
at(16); a16 = math.degrees(-L.STATE['door']['pivot'].rotation_euler.z); at(31); a31 = math.degrees(-L.STATE['door']['pivot'].rotation_euler.z)
chk('door 0 -> 90 eases (%.1f, %.1f)' % (a16, a31), 0 < a16 < 90 and abs(a31 - 90) < 0.01)
at(1); L.clear_keys(); L.set_door(85); still('door_open_85', A)
# --- trunk
A = L.build('room', 'under_bed_insert'); L.set_trunk(0.0, 0.0, frame=1); L.set_trunk(1.0, 95.0, frame=30)
at(15); x15 = L.STATE['trunk']['pivot'].location.x; chk('trunk pull eases', L.STATE['trunk']['pivot']['wrest'][0] < x15 < L.STATE['trunk']['pivot']['wrest'][0] + 1.9)
at(1); L.clear_keys(); L.set_trunk(1.0, 95.0); still('trunk_open', A, 'under_bed_insert')
# --- shop panel, stair frame, flames keyed
A = L.build('room', 'dealer_shop'); L.set_panel(False); still('shop_no_panel', A)
A = L.build('louvre', 'staircase'); L.set_frame_on_stairs(False, frame=1); L.set_frame_on_stairs(True, frame=10); at(5); chk('stair frame hidden at 5', L.STATE['stair_frame'][0].hide_render)
L.set_flames(0.0, frame=1); L.set_flames(1.0, frame=11); at(6); e = L.STATE['flames'][0][0].data.energy; chk('flames ramp (%.1f W)' % e, 0 < e < L.STATE['flames'][0][1] * 1.2)
print('ALL OK' if ok else 'SOME FAILED')
import subprocess
subprocess.run(['python3', os.path.join(L.PROJ, 'v3', 'set3d6', 'bakery_work', 'sheet.py'), os.path.join(L.WORK, 'hooks.jpg')] + shots, env=dict(os.environ, W='240', H='427', COLS='8'))
