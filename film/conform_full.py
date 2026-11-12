"""usage: python3 conform_full.py <takes_root> <out_basename>  -> <out>_frames/f_%04d.png (N=1968), dissolves centred on each take's g0"""
import sys,os,json,glob,subprocess,numpy as np
from PIL import Image
root,out=sys.argv[1],sys.argv[2]; N=1968
T=[]
for d in sorted(glob.glob(root+"/s*/meta.json")):
    m=json.load(open(d)); td=os.path.dirname(d); fr=td+"/frames"
    if not glob.glob(fr+"/g_*.png"):
        os.makedirs(fr,exist_ok=True)
        subprocess.run(["ffmpeg","-v","error","-y","-i",td+"/take.mkv","-start_number",str(m["first_g"]),fr+"/g_%04d.png"],check=True)
    m["have"]={int(f[-8:-4]):f for f in glob.glob(fr+"/g_*.png")}; m["name"]=os.path.basename(td); T.append(m)
T.sort(key=lambda m:m["g0"])
os.makedirs(out+"_frames",exist_ok=True); missing=[]; blends=0
for g in range(N):
    dst=f"{out}_frames/f_{g:04d}.png"
    if os.path.lexists(dst): os.remove(dst)
    idx=[i for i,t in enumerate(T) if t["g0"]<=g<t["g1"]]
    if not idx: missing.append(g); continue
    i=idx[0]; cur=T[i]; src=cur["have"].get(g)
    # am I inside the dissolve INTO the next take (first half) or FROM the previous take (second half)?
    pair=None
    if i+1<len(T):
        nx=T[i+1]; ti=nx.get("transition_in",{})
        if ti.get("type")=="dissolve":
            n=ti["frames"]; a=nx["g0"]-n//2
            if a<=g<nx["g0"]: pair=(cur,nx,(g-a+1)/(n+1))
    ti=cur.get("transition_in",{})
    if ti.get("type")=="dissolve" and i>0:
        n=ti["frames"]; a=cur["g0"]-n//2
        if cur["g0"]<=g<a+n: pair=(T[i-1],cur,(g-a+1)/(n+1))
    if pair and g in pair[0]["have"] and g in pair[1]["have"]:
        A,B,p=pair; p=p*p*(3-2*p)
        a_=np.asarray(Image.open(A["have"][g]).convert("RGB"),float); b_=np.asarray(Image.open(B["have"][g]).convert("RGB"),float)
        Image.fromarray(np.clip(a_*(1-p)+b_*p+0.5,0,255).astype(np.uint8)).save(dst); blends+=1; continue
    if src is None: missing.append(g); continue
    os.symlink(os.path.abspath(src),dst)
print("takes",[t["name"] for t in T],"blended",blends,"missing",len(missing),(missing[0],missing[-1]) if missing else "")
