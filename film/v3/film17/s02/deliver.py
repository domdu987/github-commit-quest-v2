import os, json, subprocess, glob, sys
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); fr = os.path.join(H, "frames"); os.makedirs(fr, exist_ok=True)
for f in glob.glob(fr + "/*"): os.remove(f)
for loc in ("street", "desk"):
    for p in glob.glob(f"{H}/raw/{loc}/g_*.png"): os.symlink(p, os.path.join(fr, os.path.basename(p)))
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-start_number","138","-i",fr+"/g_%04d.png","-c:v","libx264rgb","-crf","6","-preset","slow",H+"/take.mkv"],check=True)
meta=dict(take="s02",shots=[4,5,6],g0=144,g1=336,first_g=138,n_frames=204,handle=6,fps=30,size=[720,1280],transition_in=dict(type="dissolve",frames=11),cuts=[222,285],narration_s=[4.71,11.10])
json.dump(meta,open(H+"/meta.json","w"),indent=1)
def sheet(gs,out,n,w):
    ims=[Image.open(f"{fr}/g_{g:04d}.png").convert("RGB") for g in gs]; h=int(w*1280/720); rows=(len(ims)+n-1)//n
    S=Image.new("RGB",(n*w,rows*h))
    for i,im in enumerate(ims):
        t=im.resize((w,h)); d=ImageDraw.Draw(t); d.text((4,4),str(gs[i]),fill=(255,255,0)); d.line([(0,h*880/1280)]*2+[(w,h*880/1280)],fill=(0,255,255)); S.paste(t,((i%n)*w,(i//n)*h))
    S.save(out,quality=88)
sheet(list(range(138,342,6)),H+"/contact.jpg",12,160)
sheet([144,170,196,222,240,258,285,300,318,336],H+"/phone_sheet.jpg",5,288)
