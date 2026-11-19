"""finish.py: encode take.mkv for the three takes from frames/ and write meta.json (in each take folder s25 / s28 / s29)."""
import os, json, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
T = {'s25': dict(g0=1329, g1=1509, first=1323, last=1517, tin=dict(type='cut', frames=0)),
     's28': dict(g0=1510, g1=1585, first=1502, last=1593, tin=dict(type='dissolve', frames=11)),
     's29': dict(g0=1586, g1=1803, first=1578, last=1811, tin=dict(type='dissolve', frames=11))}
for name, t in T.items():
    d = os.path.join(ROOT, name); os.makedirs(d, exist_ok=True)
    seqd = os.path.join(HERE, 'work', 'seq_' + name); shutil.rmtree(seqd, ignore_errors=True); os.makedirs(seqd)
    for g in range(t['first'], t['last'] + 1):
        src = os.path.join(HERE, 'frames', 'g_%04d.png' % g)
        if not (t['g0'] <= g <= t['g1']) and not (name == 's25' and g < t['g0']):                       # handle frames come from this take's own shot set-up
            sh = {'s25': 27, 's28': 28, 's29': 29 if g < t['g0'] else 31}[name]; src = os.path.join(HERE, 'frames_x', str(sh), 'g_%04d.png' % g)
        if not os.path.exists(src) and t['g0'] <= g <= t['g1']: raise SystemExit('missing ' + src)
        if not os.path.exists(src): raise SystemExit('missing ' + src)
        os.symlink(src, os.path.join(seqd, 'g_%04d.png' % g))
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-start_number', str(t['first']), '-i', os.path.join(seqd, 'g_%04d.png'),
                           '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', os.path.join(d, 'take.mkv')])
    json.dump(dict(take=name, g0=t['g0'], g1=t['g1'], first_g=t['first'], n_frames=t['last'] - t['first'] + 1, transition_in=t['tin'],
                   handle_in=t['g0'] - t['first'], handle_out=t['last'] - t['g1']), open(os.path.join(d, 'meta.json'), 'w'), indent=1)
    print(name, os.path.getsize(os.path.join(d, 'take.mkv')) // 1000000, 'MB')
