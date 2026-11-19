"""assemble take s32: B frames 1796-1938, 11-frame dissolve 1934-1944 (B shot 33 -> A shot 34), A frames to 2101; encode take.mkv, meta.json, contact.jpg"""
import os, json, subprocess, shutil
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.join(H, 'work'); T = os.path.join(W, 'take'); shutil.rmtree(T, ignore_errors=True); os.makedirs(T)
G0, G1 = 1796, 2101
for g in range(G0, G1 + 1):
    if g <= 1933: im = Image.open(f'{W}/fB/g_{g}.png')
    elif g >= 1945: im = Image.open(f'{W}/fA/g_{g}.png')
    else:
        u = (g - 1933) / 12.0; im = Image.blend(Image.open(f'{W}/fB/g_{g}.png').convert('RGB'), Image.open(f'{W}/fA/g_{g}.png').convert('RGB'), u)
    im.convert('RGB').save(f'{T}/g_{g:04d}.png')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-start_number', str(G0), '-i', f'{T}/g_%04d.png', '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', os.path.join(H, 'take.mkv')], check=True)
gs = list(range(1804, 2096, 6)); cols = 10; w, h = 180, 320
S = Image.new('RGB', (cols * w, ((len(gs) + cols - 1) // cols) * h))
for i, g in enumerate(gs): S.paste(Image.open(f'{T}/g_{g:04d}.png').resize((w, h)), ((i % cols) * w, (i // cols) * h))
S.save(os.path.join(H, 'contact.jpg'), quality=85)
meta = dict(take='s32', film=15, shots=[32, 33, 34, 35, 36], first_g=G0, n_frames=G1 - G0 + 1, g0=1804, g1=2095, handle_in=8, handle_out=6,
            transition_in=dict(type='dissolve', frames=11), transition_out=dict(type='cut', frames=0, note='hard cut on the last word; handle g 2095-2101 rendered'),
            transitions=[dict(at=1875, type='cut'), dict(at=1939, type='dissolve', frames=11, note='baked into take.mkv: B shot 33 -> A shot 34, g 1934-1944'), dict(at=1988, type='cut'), dict(at=2040, type='cut')],
            shot_ranges={'32': [1804, 1874], '33': [1875, 1938], '34': [1939, 1987], '35': [1988, 2039], '36': [2040, 2095]},
            set='set3d15 B DAY (32-33), A GOLDEN (34-36)', samples=12, resolution=[720, 1280], fps=30, dof='none')
json.dump(meta, open(os.path.join(H, 'meta.json'), 'w'), indent=1)
