import cv2, numpy as np, json, sys
R="../../../ref/e/frames2/f_%03d.png"
def load(i): return cv2.imread(R%i)
def stats(bgr, mask_caption=True):
    im=bgr.astype(np.float32)/255
    if mask_caption: im=im.copy(); 
    hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV).astype(np.float32); H=hsv[...,0]*2; S=hsv[...,1]/255; V=hsv[...,2]/255
    L=0.2126*im[...,2]+0.7152*im[...,1]+0.0722*im[...,0]
    m=np.ones(L.shape,bool); m[850:960,180:560]=False  # caption
    def hue_med(mask):
        mask=mask&m&(S>0.15)
        if mask.sum()<50: return None
        a=np.deg2rad(H[mask]); return round(float(np.rad2deg(np.arctan2(np.sin(a).mean(),np.cos(a).mean()))%360),0)
    sh=(V<0.35); lit=(V>0.75)
    h,w=L.shape
    cen=L[int(h*.3):int(h*.7),int(w*.25):int(w*.75)].mean()
    cor=np.mean([L[:int(h*.12),:int(w*.2)].mean(),L[:int(h*.12),-int(w*.2):].mean(),L[-int(h*.12):,:int(w*.2)].mean(),L[-int(h*.12):,-int(w*.2):].mean()])
    g=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
    lap=np.abs(cv2.Laplacian(g,cv2.CV_32F,ksize=3))
    bands=[round(float(lap[int(h*a):int(h*b)].mean()),2) for a,b in ((0,.2),(.2,.4),(.4,.6),(.6,.8),(.8,1))]
    # thin dark outlines: blackhat 5px
    bh=cv2.morphologyEx(g,cv2.MORPH_BLACKHAT,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
    ol=float((bh>28)[m].mean())
    ed=float((cv2.Canny(g,60,150)>0)[m].mean())
    hueshare={}
    col=(S>0.2)&(V>0.12)&m
    for nm,(a,b) in dict(red=(345,20),orange=(20,50),yellow=(50,70),green=(70,170),cyan=(170,200),blue=(200,250),violet=(250,290),magenta=(290,345)).items():
        hh=((H>=a)|(H<b)) if a>b else ((H>=a)&(H<b)); hueshare[nm]=round(float((hh&col).sum()/m.sum()*100),1)
    return dict(L_mean=round(float(L[m].mean()),3),L_p5=round(float(np.percentile(L[m],5)),3),L_p50=round(float(np.percentile(L[m],50)),3),L_p95=round(float(np.percentile(L[m],95)),3),L_p99=round(float(np.percentile(L[m],99)),3),
        deep=round(float((L[m]<0.05).mean()),3), S_mean=round(float(S[m].mean()),3), S_shadow=round(float(S[sh&m].mean()),3) if (sh&m).sum() else None, S_lit=round(float(S[lit&m].mean()),3) if (lit&m).sum() else None,
        hue_shadow=hue_med(sh),hue_mid=hue_med((V>=.35)&(V<=.75)),hue_lit=hue_med(lit), lit_share=round(float((lit&m).mean()),3), shadow_share=round(float((sh&m).mean()),3),
        vign=round(float(cor/cen),3), sharp_bands=bands, outline=round(ol,4), edge=round(ed,4), hues=hueshare)
if __name__=="__main__":
    out={}
    for i in [2,4,6,8,10,15,20,24,27,31,36,42,46,52,55,57,60,64,68,72,76,78,82,84,86,89]:
        out[i]=stats(load(i)); s=out[i]
        print(i,s["L_mean"],s["L_p5"],s["L_p50"],s["L_p95"],"deep",s["deep"],"S",s["S_mean"],s["S_shadow"],s["S_lit"],"hue",s["hue_shadow"],s["hue_mid"],s["hue_lit"],"vig",s["vign"],"ol",s["outline"],"ed",s["edge"],s["sharp_bands"])
        print("   ",s["hues"])
    json.dump(out,open("frame_stats.json","w"),indent=1)
