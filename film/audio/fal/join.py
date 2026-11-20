import json,subprocess,numpy as np,sys,re
sys.path.insert(0,'audio/fal'); import tl as B  # tighten()
P='.'; SR=48000; GAP=0.12
def wav(f):
    x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True).stdout,np.int16).astype(np.float64)/32768; return x
L=[l.rstrip('\n').split('|') for l in open('script/script_th.txt')]; G=json.load(open('script/groups.json'))
allc=[];allt=[];parts=[];t=0
for i in range(6):
    d=json.load(open(f'audio/fal/c{i}.json')); ch=[];t0=[];t1=[]
    for s in [d["timestamps"]] if isinstance(d["timestamps"],dict) else d["timestamps"]:
        ch+=s["characters"]; t0+=s["character_start_times_seconds"]; t1+=s["character_end_times_seconds"]
    x=wav(f'audio/fal/c{i}.mp3'); x=x/np.sqrt((x**2).mean())*0.13
    y,a,b,cut=B.tighten(x,SR,t0,t1)
    parts+=[y,np.zeros(int(GAP*SR))]; allc+=ch; allt+=[t+v for v in a]; t+=len(y)/SR+GAP
z=np.concatenate(parts[:-1]); raw=len(z)/SR
target=float(sys.argv[1]) if len(sys.argv)>1 else 66.5; tempo=max(1.0,raw/target)
subprocess.run(["ffmpeg","-v","error","-y","-f","f64le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={tempo:.4f}","-ar","48000","audio/narration.wav"],input=z.tobytes(),check=True)
json.dump({"chars":allc,"t0":[v/tempo for v in allt],"tempo":tempo,"raw":raw},open('audio/narration.chars.json','w'),ensure_ascii=False)
print("raw",round(raw,2),"tempo",round(tempo,3),"final",round(raw/tempo,2))
