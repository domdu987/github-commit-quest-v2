import json, os, subprocess, glob
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
first, last = 1239, 1348
n = last - first + 1
json.dump(dict(segment='H1', g0=1239, g1=1345, first_g=first, n_frames=n, handles_after=3, transition_in=dict(type='cut', frames=0), cam_out=dict(loc=[-2.0, 50.0, 4.6], look=[0.0, 22.0, 1.8], lens=22.0, note='ends exactly at P_NECK at g1345; g1346-1348 start the crane up'),
          cam_in='ride behind runners at hill_over shelf, see h1.py', world=['hill_over', 'bridge_end_north'], samples=32), open(H + '/meta.json', 'w'), indent=1)
json.dump(dict(cues=[dict(g=1239, cue='charge: running feet, spear shafts, gorse whips (5 Hz shake)'), dict(g=1278, cue='whoosh: the overtake and swoop to the bridge'), dict(g=1316, cue='spear-wall clack on the slam (narration 43.78)'), dict(g=1316, cue='English hop back, helmet rattle'), dict(g=1332, cue='sting settles (44.42 ~ g1348)')]), open(H + '/cues.json', 'w'), indent=1)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-start_number', str(first), '-i', H + '/raw_final/g_%04d.png', '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', H + '/take.mkv'], check=True)
fs = [H + '/raw_final/g_%04d.png' % g for g in range(first, last + 1, 6)]
ims = [Image.open(f).resize((180, 320)) for f in fs]; cols = 10; rows = (len(ims) + cols - 1) // cols
sh = Image.new('RGB', (180 * cols, 320 * rows))
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 180, (i // cols) * 320))
sh.save(H + '/contact.jpg', quality=88)
print('size', os.path.getsize(H + '/take.mkv') / 1e6)
