# re-time captions from script/caption_phrases.txt (one line per sentence, phrases split by '/') using voiced frames, like build_bk0.py
import json,subprocess,numpy as np
L=[l.rstrip('\n').split('|') for l in open('script/script_th.txt')]
P=[l.rstrip('\n').split('/') for l in open('script/caption_phrases.txt')]
T=json.load(open('audio/timing.json')); start,ends=T['sent_start'],T['sent_end']
x16=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","audio/narration.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
env=np.sqrt(np.convolve(x16**2,np.ones(320)/320,'same'))[::160]; voiced=env>0.012
caps=[]
for k,((b,s),ph) in enumerate(zip(L,P)):
    assert ''.join(ph).replace(' ','').replace('45','สี่สิบห้า')==s.replace(' ',''), (k,ph)
    fr=np.arange(int(start[k]*100),min(len(voiced),int(ends[k]*100))); v=fr[voiced[fr]]
    w=np.array([len(p.replace(' ','').replace('45','สี่สิบห้า')) for p in ph],float); cum=np.concatenate([[0],np.cumsum(w)])/w.sum()
    for p,f in zip(ph,cum[:-1]): caps.append({"t":max(0.0,round(float(v[min(len(v)-1,int(f*len(v)))]/100)-0.03,2)),"text":p,"beat":b,"sent":k})
for i,c in enumerate(caps): c["end"]=caps[i+1]["t"] if i+1<len(caps) else round(ends[-1]+0.2,2)
json.dump(caps,open('script/captions.json','w'),ensure_ascii=False,indent=0); print(len(caps),'captions')
