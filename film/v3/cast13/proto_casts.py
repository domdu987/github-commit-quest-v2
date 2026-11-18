import copy, sys
sys.path.insert(0,"/home/user/github-commit-quest-v2/film/v3/cast10")
import cast10, puppet as P, cast_ext as CE
FL=dict(_cast10=True,_cast9=True,_cast8=True,_cast7=True,_cast6=True,_cast5=True,_cast4=True,_cast3=True)
def mk(base, **kw):
    c=copy.deepcopy(P.CAST[base]); c.update(FL)
    for k,v in kw.items():
        if isinstance(v,dict) and isinstance(c.get(k),dict): c[k].update(v)
        else: c[k]=v
    return c
C={}
C["pullman"]=mk("gentleman", seed=61.3, chain=False, hat_style="bowler", moustache_style="bushy", tache_scale=0.55, mouth="smile",
   hat_colors=dict(base="#3a2e2a",dark="#241c1a",light="#6a5a52",band="#141018",brim="#30261f",edge="#7a6a60",shine="#9a8a80"),
   hair=dict(color="#4a3224"),
   sleeve=dict(color="#f1e6cf",cuff="#f1e6cf",dark="#cdbf9f",len=0.50,roll=True,w=0.15),
   colors=dict(base="#3b3438",dark="#262024",lapel="#2f292d",vest="#a8552f",vest_b="#e3c88a",tie="#2c7a78",tie_dark="#1a4e4c",moustache="#4a3224",pants="#5a5058"))
C["rich"]=mk("boss", seed=9.9, torso_w=1.55, torso_h=1.16, hat_style="tophat7", hat="newsboy",
   sideburns=dict(color="#b8b0a4",dark="#8a8478"),
   hat_colors=dict(base="#2a2428",dark="#161216",light="#4e4650",band="#7a1e2a",brim="#221c20",shine="#8a8090"),
   hair=dict(color="#b8b0a4"), colors=dict(base="#1f9a56",dark="#126a3a",lapel="#0f5a32",stripe="#f2d45c",tie="#c9352e",moustache="#a8a094"))
for n,c in C.items(): P.CAST[n]=c
if __name__=="__main__":
    D=110; o=[]
    names=list(C)+["gentleman","boss"]
    for i,n in enumerate(names):
        f=P.figure(n,{"yaw":0.3,"expr":"smug" if n=="rich" else "neutral"},"u%d"%i)
        x=150+i*250;y=520
        o.append('<g transform="translate(%d %d) scale(%d)">%s</g>'%(x-f["anchors"]["feet"][0]*D,y-f["feet_y"]*D,D,f["svg"]))
    W=150+len(names)*250
    open("/tmp/claude-0/s/t2.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="560"><rect width="100%%" height="100%%" fill="#cfccc6"/>%s</svg>'%(W,"".join(o)))
    P._raster("/tmp/claude-0/s/t2.svg","/tmp/claude-0/s/t2.png",W,560,1)
