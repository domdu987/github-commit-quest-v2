import sys, os, time
ROOT = '/home/user/github-commit-quest-v2'
sys.path.insert(0, ROOT + '/film/v3/set3d17'); os.chdir(ROOT + '/film/v3/set3d17')
import prefecture17 as P, bpy
take = 'T3'
# gate fix v1 (director fix list items 1-3): constant offset of the measuring chair + its sitter, so the 2 m rear post leaves Bertillon's head line
# (g790-795) and the head-rest pad no longer crosses the sitter's face from the east camera (g811-826). Applies over the whole part.
CHAIR_D = (-0.4, 0.0); PRIS_D = (-0.15, 0.0)   # chair geometry dx,dy; sitter card dx,dy (card = chair offset +0.25 m: armrest rail stays in front of the card at g816, pad behind it, face >=70 % visible off the post at g793)
_kc = P.K.measuring_chair
P.K.measuring_chair = lambda B, c, **kw: _kc(B, (c[0] + CHAIR_D[0], c[1] + CHAIR_D[1]), **kw) if abs(c[0] - 0.7) < 1e-6 and abs(c[1] - 2.4) < 1e-6 else _kc(B, c, **kw)
# gate fix v2 item 1 (from T3, ec3f44d): raise the measuring-room gasolier (-0.35, 1.0) by 0.6 m (pendant drop 1.45 -> 0.85) so its lamps clear gend_b's face at g741-761. Other gasolier untouched.
GAS_DZ = 0.6; _kg = P.K.gasolier
P.K.gasolier = lambda B, c, **kw: _kg(B, c, **dict(kw, drop=kw.get('drop', 1.45) - GAS_DZ)) if abs(c[0] + 0.35) < 1e-6 and abs(c[1] - 1.0) < 1e-6 else _kg(B, c, **kw)
OUT = os.environ.get('OUT', ROOT + '/film/v3/film17v2/T3b/frames')
def assign_for(g):
    a = {'bertillon': ('bertillon_measuring', {'mirror': True}),
         'prisoner_chair': ('prisoner_sitting_b', {'seated': 'chair'}),
         'prisoner_b': ('prisoner_sitting_a', {'seated': 'bench'}),
         'prisoner_q': ('prisoner_sitting_c', {'seated': 'bench'})}
    if g < 725:   # 3a: whole room laughs
        a['inspector'] = ('inspector_laughing', {}); a['gend_a'] = ('gendarme_laughing_a', {})
        a['gend_b'] = ('gendarme_laughing_b', {}); a['prankster'] = ('gendarme_laughing_b', {})
    else:         # 3b/3c: room back to work, prefect in
        a['inspector'] = ('inspector_arms_crossed', {}); a['gend_a'] = ('gendarme_standing_a', {})
        a['gend_b'] = ('gendarme_standing_b', {}); a['prankster'] = ('gendarme_standing_b', {})
        a['prefect'] = ('prefect_finger_up_three', {}) if g < 792 else ('prefect_stern', {})
    a['prisoner_chair'] = (a['prisoner_chair'][0], dict(a['prisoner_chair'][1], dx=PRIS_D[0], dy=PRIS_D[1]))
    return a
def clear_cast():
    # stage_cast2 builds NEW actors every call and never removes the old ones: stale shadow proxies/cards pile up (black slabs by ~g660). Remove them first.
    sys.path.insert(0, ROOT + '/film/v3/stage'); import actors
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
RAMP_LO, RAMP_G0, RAMP_G1 = 0.4, 750, 800   # lights x0.4 through g750, easing to x1.0 at g800 (high bird's-eye views run luma 120-135, the low g800 view ~95)
DN_G0, DN_G1, DN_HI = 825, 835, float(os.environ.get("DN_HI", 0.8))   # gate fix v2 (director item 2): lights x1.0 at g825 easing to x0.8 at g835, held to g856 (g835-849 ran 125-142)
def ramp_f(g):
    up = RAMP_LO if g <= RAMP_G0 else 1.0 if g >= RAMP_G1 else RAMP_LO + (1 - RAMP_LO) * (g - RAMP_G0) / (RAMP_G1 - RAMP_G0)
    dn = 1.0 if g <= DN_G0 else DN_HI if g >= DN_G1 else 1.0 + (DN_HI - 1.0) * (g - DN_G0) / (DN_G1 - DN_G0)
    return up * dn
def apply_ramp():
    # every light's energy keys x ramp_f(frame-1); lights with no animation get a key per frame inside the ramp. Lights only: no haze, no saturation.
    for o in [o for o in bpy.data.objects if o.type == 'LIGHT']:
        d = o.data; ad = d.animation_data
        if ad and ad.action:
            for ly in ad.action.layers:
                for st in ly.strips:
                    for cb in st.channelbags:
                        for fc in cb.fcurves:
                            if fc.data_path != 'energy': continue
                            for kp in fc.keyframe_points:
                                f = ramp_f(int(round(kp.co.x)) - 1); kp.co.y *= f; kp.handle_left.y *= f; kp.handle_right.y *= f
                            fc.update()
        else:
            e = d.energy
            for g in range(645, 860): d.energy = e * ramp_f(g); d.keyframe_insert('energy', frame=g + 1)
def main(gs):
    assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take); P.key_take(take); P.setup_render2((720, 1280), samples=int(os.environ.get('SAMPLES', 16)), threads=2)
    if min(gs) <= RAMP_G1 or max(gs) > DN_G0: apply_ramp()
    for g in gs:
        fn = '%s/g_%04d.png' % (OUT, g)
        if os.path.exists(fn) and os.path.getsize(fn) > 50000: continue
        t0 = time.time(); bpy.context.scene.frame_set(g + 1); clear_cast(); P.stage_cast2(take, g, assign_for(g))
        bpy.context.scene.render.filepath = fn; bpy.ops.render.render(write_still=True); P.grade2(fn)
        print('g%d %.1fs' % (g, time.time() - t0), flush=True)
if __name__ == '__main__':
    a = sys.argv[1:]
    gs = [int(x) for x in a[0].split(',')] if ',' in a[0] or len(a) == 1 else range(int(a[0]), int(a[1]) + 1)
    main(gs)
