import sys, json
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d18')
import jimo_shots as S
def fm(m):
    return '(%g, %g, %g)' % tuple(m[:3]) + (' yaw %g' % m[3] if len(m) > 3 else '') + (' s%g' % m[4] if len(m) > 4 else '')
out = []
out.append('## Cameras and stand marks per shot (generated from jimo_shots.py)\n')
out.append('Camera poses are `loc -> look_at` (D) and lens (mm). `start` is the pose at t = 0 of the shot, `end` at t = 1; `J.shot_camera(name, t)` poses the scene camera for any t and `J.key_camera(name)` keys the whole move. '
           'Marks are world points (x, y, z) with the card yaw (deg about z; a person card faces -y at yaw 0, the printed yaw turns it to face the START camera; ox / herd cards: yaw = direction of travel from +x, side view), '
           'ox marks may carry a scale. For long lists only the first 6 are printed here; `jimo_shots.marks_for("sNN")` returns them all.\n')
for k, sh in S.SHOTS.items():
    c = S.pose_at(sh, 0.0); e = S.pose_at(sh, 1.0); mv = sh['move']
    out.append('### %s  (frames %d-%d, %s, %s)' % (k, sh['f0'], sh['f1'], sh['loc'], sh['light']))
    out.append('- %s' % sh['note'])
    out.append('- camera start %s -> %s lens %g; end %s -> %s; move: push %+g /s, slide %+g px/s%s; fg prop: %s; state at mid: `%s`' % (tuple(c['loc']), tuple(c['look_at']), c['lens'], tuple(e['loc']), tuple(e['look_at']), mv.get('push', 0), mv.get('slide', 0),
               (', extra ' + str(mv['moves'])) if mv.get('moves') else '', sh['fg'] or 'none', sh['state'] or '-'))
    mk = S.marks_for(k)
    for role, lst in mk.items():
        if isinstance(lst, str): continue
        out.append('  - %s (%d): %s%s' % (role, len(lst), '; '.join(fm(m) for m in lst[:6]), ' ...' if len(lst) > 6 else ''))
    out.append('')
open('/home/user/github-commit-quest-v2/film/v3/set3d18/set_work/api_marks.md', 'w').write('\n'.join(out))
print(len(out))
