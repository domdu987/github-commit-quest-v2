import json, sys, numpy as np, os
P='__PROJ__'
OUT=P+'/v3/film/out'
sys.path.insert(0,P+'/audio'); import mixer
from mixer import load, fades, SR, db2
spec=json.load(open(OUT+'/mix_film.json')); n=int(spec['duration']*SR)
dB=lambda v:20*np.log10(v+1e-12)
def render(e):
    x=load(e["file"]); mono=x.mean(1)
    if e.get("align")=="onset":
        pk=np.abs(mono).max(); on=int(np.argmax(np.abs(mono)>0.25*pk)); x=x[max(0,on-int(0.005*SR)):]
    x=x[int(e.get("start",0)*SR):]
    if e.get("len"): x=x[:int(e["len"]*SR)]
    x=x.copy(); mono=x.mean(1)
    if "peak_db" in e: x*=db2(e["peak_db"])/max(np.abs(mono).max(),1e-9)
    else: x*=db2(e.get("rms_db",-26))/max(np.sqrt((mono**2).mean()),1e-9)
    x=fades(x,e.get("fade_in",0.005),e.get("fade_out",0.03))
    p=e.get("pan",0.0); x[:,0]*=min(1.0,1-p); x[:,1]*=min(1.0,1+p)
    buf=np.zeros((n,2)); mixer.place(buf,x,e["at"]); return buf
tim=json.load(open(P+'/audio/th/full_v2/narration_timing.json'))['phrases']
speech=np.zeros(n,bool)
for p in tim: speech[int((p['t0']+0.1)*SR):int((p['t1']+0.1)*SR)]=True
# voice track
v=spec['voice']; vx=load(v['file'])*v['gain']; vb=np.zeros((n,2)); mixer.place(vb,vx,v['at'])
hop=480; m=n//hop
venv=np.sqrt((vb[:m*hop].mean(1).reshape(m,hop)**2).mean(1))
vact=np.repeat(dB(venv)>-40,hop); vact=np.concatenate([vact,np.zeros(n-len(vact),bool)])
mix=load(spec['out_wav'])[:n]
print('final duration', len(load(spec['out_wav']))/SR)
print('overall RMS %.1f dBFS, peak %.2f dBFS (%.3f)'%(dB(np.sqrt((mix.mean(1)**2).mean())),dB(np.abs(mix).max()),np.abs(mix).max()))
print('voice RMS (voice track alone, active frames) %.1f; whole file %.1f; voice peak %.2f'%(dB(np.sqrt((vb.mean(1)[vact]**2).mean())),dB(np.sqrt((vx.mean(1)**2).mean())),dB(np.abs(vb).max())))
print('mix RMS while voice active %.1f'%dB(np.sqrt((mix.mean(1)[vact]**2).mean())))
gap=~vact; gap[:int(0.1*SR)]=False; gap[int(65.45*SR):]=False
# gaps between words: voice-inactive runs of >=50 ms inside the narration span
runs=[];i=0;g=gap
idx=np.flatnonzero(np.diff(np.concatenate([[0],g.astype(int),[0]])))
gm=np.zeros(n,bool); cnt=0
for a,b in zip(idx[::2],idx[1::2]):
    if (b-a)/SR>=0.05: gm[a:b]=True; cnt+=1
print('gaps between words: %d runs, %.2f s total, mix RMS in gaps %.1f dBFS'%(cnt,gm.sum()/SR,dB(np.sqrt((mix.mean(1)[gm]**2).mean()))))
# music bed level alone
mu=spec['music']; mx=load(mu['file']); full=mx; mx=mx[:n].copy(); mx*=db2(mu['rms_db'])/np.sqrt((full.mean(1)**2).mean())
print('music bed RMS over film %.1f'%dB(np.sqrt((mx.mean(1)**2).mean())))
rows=[]; worst=[]
for k,e in enumerate(spec['sfx']):
    b=render(e); a=np.abs(b).max(1)
    nz=np.flatnonzero(a>0); t0=nz[0]/SR if len(nz) else e['at']; t1=nz[-1]/SR if len(nz) else e['at']
    pk=dB(a.max()); seg=b.mean(1)[nz[0]:nz[-1]+1]; rms=dB(np.sqrt((seg**2).mean()))
    ps=dB(a[speech].max()) if (a[speech]>0).any() else -200
    rows.append(dict(i=k,sound=os.path.basename(e['file'])[:-4],at=e['at'],t0=round(t0,3),t1=round(t1,3),peak=round(pk,1),rms=round(rms,1),peak_in_speech=round(ps,1)))
    if ps>-10: worst.append(rows[-1])
json.dump(rows,open('effects_measured.json','w'),indent=0)
print('effects', len(rows), 'exceeding -10 dBFS during speech:', worst)
print('max effect peak in speech %.1f'%max(r['peak_in_speech'] for r in rows))
# sum of all effects during speech
eb=sum(render(e) for e in spec['sfx'])
print('summed effects peak in speech %.1f, outside %.1f'%(dB(np.abs(eb[speech]).max()),dB(np.abs(eb[~speech]).max())))
# hook check: effects-only first 5 s vs approved hook effects
op=json.load(open(P+'/v3/out/mix_opening.json'))
hb=sum(render(e) for e in op['sfx'])
k5=int(5*SR); print('hook 0-5 s effects identical (max abs diff):', np.abs(hb[:k5]-eb[:k5]).max())
k5=int(5*SR)
print('summed effects peak in speech after 5 s: %.1f'%dB(np.abs(eb[k5:][speech[k5:]]).max()))
i=np.argmax(np.abs(eb).max(1)*speech); print('loudest summed effect sample in speech at %.3f s'%(i/SR))
# per-second loudness of mix for sanity
for name,(a,b) in {'hook 0-5':(0,5),'gap s08 16.74-16.97':(16.84,16.97)}.items():
    seg=mix[int(a*SR):int(b*SR)].mean(1); print(name,'%.1f'%dB(np.sqrt((seg**2).mean())))
a=np.abs(eb).max(1)*speech; a[:k5]=0
hop=4800
blk=a[:len(a)//hop*hop].reshape(-1,hop).max(1)
for j in np.flatnonzero(dB(blk)>-10.5): print('summed over -10.5 at %.1f s: %.1f'%(j*0.1,dB(blk[j])))
