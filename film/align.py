import json,numpy as np,subprocess
from pythainlp.tokenize import word_tokenize
sr=16000
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","audio/narration.wav","-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout,np.float32)
hop=160; env=np.sqrt(np.convolve(x**2,np.ones(320)/320,'same'))[::hop]; voiced=env>0.012
L=[l.rstrip('\n').split('|') for l in open('script/script_th.txt')]
groups=json.load(open('script/groups.json')); segs=json.load(open('audio/segments.json'))
CAPFIX={"ปีหนึ่งเจ็ดหกเก้า":"ปี 1769","เก้าสิบตัน":"90 ตัน","รัว":"รัว ๆ"}
def phrases(s):
    s=s.replace('ปีหนึ่งเจ็ดหกเก้า','ปี1769').replace('เก้าสิบตัน','90ตัน')
    out=[]
    for p in s.replace(' ๆ','ๆ').split(' '):
        p=p.replace('ๆ',' ๆ')
        if len(p)<=14: out.append(p); continue
        cur=''
        for w in word_tokenize(p.replace(' ๆ','ๆ'),engine='newmm'):
            if len(cur)+len(w)>12 and cur: out.append(cur); cur=w
            else: cur+=w
        if cur: out.append(cur)
    m=[]
    for p in out:
        if m and len(p.replace(' ','').replace('ๆ',''))<=3 and len(m[-1])+len(p)<=17: m[-1]+=p
        else: m.append(p)
    out=m
    return [CAPFIX.get(p,p).replace('ปี1769','ปี 1769').replace('90ตัน','90 ตัน').replace('ๆ',' ๆ').replace('  ',' ') for p in out]
sent=[];caps=[]
for ci,g in enumerate(groups):
    cs=[s for s in segs if s[0]==ci]; t0=cs[0][1]; t1=cs[-1][2]
    # voiced frames in chunk
    fr=np.arange(int(t0*100),min(len(voiced),int(t1*100)+1)); v=fr[voiced[fr]]
    items=[]
    for k in g:
        for p in phrases(L[k][1]): items.append((k,p))
    w=np.array([len(p.replace(' ','')) for _,p in items],float); cum=np.concatenate([[0],np.cumsum(w)])/w.sum()
    # map cumulative fraction to time over voiced frames
    starts=[v[min(len(v)-1,int(c*len(v)))]/100 for c in cum[:-1]]
    # snap each start to the nearest onset (unvoiced->voiced) within 0.25s
    on=np.flatnonzero(~voiced[:-1]&voiced[1:])/100+0.0
    for (k,p),st in zip(items,starts):
        if len(on): 
            j=np.argmin(abs(on-st)); st=on[j]-0.02 if abs(on[j]-st)<0.25 else st
        caps.append({"t":round(float(st),2),"text":p,"sent":k,"beat":L[k][0]})
for i in range(1,len(caps)):
    if caps[i]["t"]<=caps[i-1]["t"]: caps[i]["t"]=round(caps[i-1]["t"]+0.15,2)
for i,c in enumerate(caps): c["end"]=caps[i+1]["t"] if i+1<len(caps) else 66.9
json.dump(caps,open('script/captions.json','w'),ensure_ascii=False,indent=0)
for c in caps: print(c["t"],c["beat"],c["text"])
