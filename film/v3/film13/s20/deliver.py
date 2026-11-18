import os, sys, json, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); FILM = os.path.dirname(os.path.dirname(V))
B = {20:(1300,1362),21:(1362,1416),22:(1416,1467),23:(1467,1537),24:(1537,1602),25:(1602,1680)}
CUES = {20:[dict(t=44.69,dur=1.2,label="whistle"),dict(t=43.3,dur=1.5,label="cellar room tone, oil lamps")],
 21:[dict(t=45.5,dur=1.8,label="ratchet clicks in sync, 500 men"),dict(t=45.3,dur=1.8,label="wood creak")],
 22:[dict(t=47.1,dur=1.7,label="ratchet pawl + iron screw groan"),dict(t=48.0,dur=0.8,label="beam creak")],
 23:[dict(t=48.8,dur=2.3,label="long wood creak, dust trickle")],24:[dict(t=51.13,dur=2.1,label="low timber settle, distant street")],
 25:[dict(t=53.3,dur=2.6,label="thousands of ratchets, rising swell")]}
for s in B:
    g0, g1 = B[s]; fg = g0 - 6; lg = g1 - 1 + 6; d = os.path.join(V, "s%d" % s); os.makedirs(d, exist_ok=True)
    raw = os.path.join(HERE, "raw", "s%d" % s)
    mk = os.path.join(d, "take.mkv")
    subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-start_number",str(fg),"-i",raw+"/g_%04d.png","-c:v","libx264rgb","-crf","6","-preset","slow",mk],check=True)
    if os.path.getsize(mk) > 45e6:
        subprocess.run("split -b 40M take.mkv take.mkv.part && rm take.mkv", shell=True, cwd=d)
    json.dump(dict(take="s%d"%s, film=13, shots=[s], first_g=fg, n_frames=lg-fg+1, g0=g0, g1=g1, handle_in=6, handle_out=6,
        transition_in=dict(type="cut", frames=0)), open(d+"/meta.json","w"), indent=1)
    json.dump(CUES[s], open(d+"/cues.json","w"), indent=1)
    for f in ("shot.py","c13.py","deliver.py"):
        if s == 20 or f == "shot.py": shutil.copy(os.path.join(HERE, f), d) if os.path.abspath(d) != HERE else None
