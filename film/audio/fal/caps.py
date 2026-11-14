import json,sys,subprocess
sys.path.insert(0,'audio/th'); import tts_fal
c=json.load(open('audio/narration.chars.json'))
import re
t=''.join(c['chars']); keep=[True]*len(t)
for m in re.finditer(r'\[[^\]]*\]',t):
    for k in range(m.start(),m.end()): keep[k]=False
c={'chars':[x for x,k in zip(c['chars'],keep) if k],'t0':[x for x,k in zip(c['t0'],keep) if k]}
caps=json.load(open('script/captions.json'))
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","audio/narration.wav"],capture_output=True,text=True).stdout)
json.dump({"text":"".join(c["chars"]),"chars":c["chars"],"t0":c["t0"],"t1":c["t0"][1:]+[dur],"duration":dur},open('audio/narr_tmp.chars.json','w'),ensure_ascii=False)
spk={"ปี 1769":"ปีหนึ่งเจ็ดหกเก้า","เกือบ 90 ตัน":"เกือบเก้าสิบตัน"}
qq=[{"text":spk.get(p["text"],p["text"]),**p} for p in caps]
for q,p in zip(qq,caps): q["text"]=spk.get(p["text"],p["text"])
out,ratio,_=tts_fal.align('audio/narr_tmp',qq)
res=[{"t":o["t0"],"end":o["t1"],"text":p["text"],"beat":p["beat"],"sent":p["sent"]} for o,p in zip(out,caps)]
json.dump(res,open('script/captions.json','w'),ensure_ascii=False,indent=0)
d={}
for x in res: d.setdefault(x['beat'],round(x['t'],2))
print("ratio",round(ratio,3),"dur",round(dur,2)); print(d)
