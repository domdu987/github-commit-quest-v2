#!/usr/bin/env python3
"""deliver.py <take> -- frames work/f<NN>/g_%04d.png -> take.mkv, meta.json, cues.json, contact.jpg in the take folder."""
import sys, os, json, subprocess, glob, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0], 'range'] + sys.argv[1:]
take = sys.argv[2]
import shot as S
g0, g1, ga, gz = S.take_range(take); k = S.TAKES[take]; num = take[1:]
src = os.path.join(HERE, 'work', 'f' + num); dst = os.path.join(HERE, '..', take); os.makedirs(dst, exist_ok=True)
fr = sorted(glob.glob(os.path.join(src, 'g_*.png'))); assert len(fr) == gz - ga + 1, (len(fr), gz - ga + 1)
out = os.path.join(dst, 'take.mkv')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(ga), '-i', os.path.join(src, 'g_%04d.png'), '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', out], check=True)
if os.path.getsize(out) > 45e6:
    subprocess.run(['split', '-b', '40M', out, out + '.part'], check=True); os.remove(out)
sh = {str(n): [S.B[n], S.B[n + 1] - 1] for n in k['shots']}
tin = dict(type='dissolve', frames=11, note='plan: shot 17 DIS from shot 16 (A->B); in-handle %d frames' % k['hin']) if take == 's17' else dict(type='cut', frames=0)
meta = dict(take=take, film=15, shots=list(k['shots']), first_g=ga, n_frames=gz - ga + 1, g0=g0, g1=g1, handle_in=k['hin'], handle_out=k['hout'],
            transition_in=tin, transition_out=dict(type='cut', frames=0), shot_ranges=sh, light=k['light'], samples=12, resolution=[720, 1280], fps=30, dof='none',
            denoiser='OpenImageDenoise', narration='film15/audio/narration.wav at +0.10 s', set='v3/set3d15 (B %s)' % k['light'], cast='v3/cast15 cards (c15.py)',
            events=dict(mouth_window_g=[S.gof(40.38), S.gof(42.25)] if take == 's21' else None))
json.dump(meta, open(os.path.join(dst, 'meta.json'), 'w'), indent=1)
