"""refE_measure.py -- sample character vs surroundings in reference E frames.
Each sample: 31x31 window, median of the pixels above the window's 55th luma percentile (drops ink lines/straps).
Writes out/refE_measure.json and tmp/flat/refE_marks.png (the sample windows drawn on the frames)."""
import numpy as np, colorsys, json, os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
P=H+"/../../ref/e/frames2/f_%03d.png"
S={ 60:dict(kind="night alley",face=(140,702),cloth=(162,853),wall=(324,324)),
    84:dict(kind="night alley, warm window beside",face=(209,605),cloth=(101,778),wall=(360,162)),
    89:dict(kind="night alley",face=(148,702),cloth=(158,821),wall=(396,162)),
    26:dict(kind="night street + door light",face=(216,518),face_shadow=(119,540),cloth=(162,691),wall=(40,700)),
     1:dict(kind="night alley fg",face=(65,626),face_shadow=(12,650),cloth=(54,778),wall=(250,200)),
    66:dict(kind="night, back view toward warm window",cloth=(241,756),wall=(101,432)),
    53:dict(kind="interior, back view to night door",cloth=(158,702),cloth2=(396,691),wall=(60,330)),
    37:dict(kind="interior",face=(126,572),cloth=(126,713),wall=(72,324)),
    45:dict(kind="interior close",face=(270,605),cloth=(173,778),wall=(65,300)),
    50:dict(kind="interior",face=(112,637),cloth=(133,734),face2=(457,648),cloth2=(500,745),wall=(252,486)),
    30:dict(kind="interior low angle",face=(403,583),cloth=(371,778),wall=(560,420))}
out={}; tiles=[]
for k,d in S.items():
    pim=Image.open(P%k).convert("RGB"); im=np.asarray(pim).astype(float)/255
    L=im@[0.2126,0.7152,0.0722]; dr=ImageDraw.Draw(pim)
    r=dict(kind=d["kind"],frame_L_mean=round(float(L.mean()),3),frame_L_med=round(float(np.median(L)),3))
    for n,xy in d.items():
        if n=="kind": continue
        x,y=xy; x=max(15,x)
        w=im[y-15:y+16,x-15:x+16].reshape(-1,3); l=w@[0.2126,0.7152,0.0722]
        p=np.median(w[l>=np.percentile(l,55)],0)
        h,s,v=colorsys.rgb_to_hsv(*p)
        r[n]=dict(rgb=[int(round(c*255)) for c in p],L=round(float(p@[0.2126,0.7152,0.0722]),3),hue=round(h*360),sat=round(s,3))
        dr.rectangle((x-15,y-15,x+15,y+15),outline=(0,255,0)); dr.text((x-14,y-14),n[:6],fill=(0,255,0))
    out[k]=r; tiles.append(pim.resize((360,640)))
    print(k,json.dumps(r))
W=Image.new("RGB",(360*6,1280))
for i,t in enumerate(tiles): W.paste(t,((i%6)*360,(i//6)*640))
W.save(H+"/tmp/flat/refE_marks.png")
json.dump(out,open(H+"/out/refE_measure.json","w"),indent=1)
