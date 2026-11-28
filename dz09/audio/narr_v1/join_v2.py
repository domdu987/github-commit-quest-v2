import json, sys, subprocess, numpy as np, wave
sys.path.insert(0,'../th'); import tts_fal
SR=48000
TEMPO={"s01":1.20,"s02":0.97,"s03":1.12,"s04":1.10,"s05":1.06,"s06":1.02,"s07":1.10,"s08":0.90,"s09":1.00,"s10":0.94,"s11":1.18,"s12":1.00,"s13":0.95,"s14":0.88,"s15":1.22,"s16":1.00}
script={s['id']:s for s in json.load(open('script.json'))}
rep=json.load(open('verify_report.json'))
# gap after each sentence (seconds, before tempo); dramatic beats get longer holds
GAP={"s01":0.50,"s02":0.55,"s03":0.15,"s04":0.20,"s05":0.30,"s06":0.20,"s07":0.15,"s08":0.65,"s09":0.25,"s10":0.60,"s11":0.15,"s12":0.30,"s13":0.35,"s14":0.80,"s15":0.50}
def load(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768; return x
def trim(x, thr=0.01):
    env=np.convolve(np.abs(x),np.ones(240)/240,'same'); idx=np.where(env>thr)[0]
    a=max(0,idx[0]-int(0.02*SR)); b=min(len(x),idx[-1]+int(0.04*SR)); return x[a:b], a
def tighten(x):  # shorten silences over 0.14 s to 0.10 s
    env=np.convolve(np.abs(x),np.ones(480)/480,'same'); quiet=env<0.006
    out=[]; i=0; n=len(x); keep=[]
    while i<n:
        if quiet[i]:
            j=i
            while j<n and quiet[j]: j+=1
            L=j-i
            keep.append((i,j, int(0.10*SR) if L>0.14*SR else L)); i=j
        else:
            j=i
            while j<n and not quiet[j]: j+=1
            keep.append((i,j,j-i)); i=j
    return keep
pieces=[]; caps=[]; t=0.0
for r in rep:
    sid=r['id']; base=r['take']
    x=load(base+'.wav'); x,off=trim(x)
    # caption alignment inside the sentence (original timing)
    cl=[{"text":c} for c in script[sid]['captions']]
    al,ratio,_=tts_fal.align(base, cl)
    # tighten and build a time map original->new
    segs=tighten(x); y=[]; tmap=[]; pos=0
    for a,b,L in segs:
        seg=x[a:b] if L==b-a else np.concatenate([x[a:a+L//2], x[b-(L-L//2):b]])
        tmap.append((off+a, off+b, pos, pos+L)); y.append(seg); pos+=L
    y=np.concatenate(y); tp=TEMPO[sid]
    open('/tmp/_s.raw','wb').write(y.astype(np.float64).tobytes())
    y=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-f','f64le','-ar','48000','-ac','1','-i','/tmp/_s.raw','-af',f'atempo={tp}','-f','f64le','-'],capture_output=True).stdout,dtype=np.float64)
    def mapt(ts):
        s=int(ts*SR)
        for a,b,c,d in tmap:
            if s<=b: return (c+ (min(max(s,a),b)-a)*(d-c)/max(b-a,1))/SR
        return pos/SR
    for q in al:
        caps.append({"id":sid,"text":q['text'],"t0":t+max(0,mapt(q['t0']))/tp})
    pieces.append(y); t+=len(y)/SR
    g=GAP.get(sid,0.18); pieces.append(np.zeros(int(g*SR))); t+=g
sig=np.concatenate(pieces)
r=np.sqrt((sig**2).mean()); sig*=10**(-17.4/20)/r; sig=np.clip(sig,-0.98,0.98)
subprocess.run(['ffmpeg','-v','error','-y','-f','f64le','-ar','48000','-ac','1','-i','-','narr_natural.wav'],input=sig.tobytes())
subprocess.run(['cp','narr_natural.wav','narr_final.wav'])
for i,c in enumerate(caps):
    c['t0']=round(c['t0'],3)
for i,c in enumerate(caps):
    c['t1']=caps[i+1]['t0'] if i+1<len(caps) else round(len(sig)/SR,3)
json.dump(caps,open('captions_timing.json','w'),ensure_ascii=False,indent=1)
print('natural',round(len(sig)/SR,2),'final',round(len(sig)/SR,2))
for c in caps: print(f"{c['t0']:6.2f}-{c['t1']:6.2f} {c['id']} {c['text']}")
