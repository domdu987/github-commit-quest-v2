# re-time captions.json phrase starts from ElevenLabs STT word timestamps (per sentence), narration seconds
import json,subprocess,os,re,difflib,base64,concurrent.futures as cf
T=json.load(open('audio/timing.json')); C=json.load(open('script/captions.json'))
L=[l.rstrip('\n').split('|')[1] for l in open('script/script_th.txt')]
norm=lambda s: re.sub(r"[\s\.,!?\"“”ๆ]","",s)
def stt(k):
    a,b=T['sent_start'][k],T['sent_end'][k]
    mp=f'/tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/rt{k}.mp3'
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-to",str(b),"-i","audio/narration.wav","-ac","1","-b:a","96k",mp],check=True)
    body={"audio_url":"data:audio/mpeg;base64,"+base64.b64encode(open(mp,'rb').read()).decode(),"language_code":"tha","tag_audio_events":False}
    jf=mp+'.json'; json.dump(body,open(jf,'w'))
    r=subprocess.run(["curl","-sS","-m","300","-X","POST","https://fal.run/fal-ai/elevenlabs/speech-to-text","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d","@"+jf],capture_output=True,text=True)
    return k,a,json.loads(r.stdout)
res={}
with cf.ThreadPoolExecutor(5) as ex:
    for k,a,d in ex.map(stt,range(len(L))): res[k]=(a,d)
out=[]
for k in range(len(L)):
    a,d=res[k]; chars=[];times=[]
    for w in d.get("words",[]):
        t=re.sub(r"(?i)chicago","ชิคาโก",w.get("text","")); n=norm(t)
        if not n: continue
        s,e=w["start"],w["end"]
        for i,ch in enumerate(n): chars.append(ch); times.append(a+s+(e-s)*i/len(n))
    stxt=''.join(chars); ref=norm(L[k])
    sm=difflib.SequenceMatcher(None,ref,stxt,autojunk=False)
    m={}
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        for i in range(i1,i2):
            j=j1+(i-i1) if tag=='equal' else min(j2-1,j1+int((i-i1)*(j2-j1)/max(1,i2-i1))) if j2>j1 else j1
            m[i]=min(max(j,0),len(times)-1)
    phr=[c for c in C if c['sent']==k]; off=0
    for c in phr:
        old=c['t']; c['t']=round(times[m[off]]-0.03,2) if times else old
        out.append((k,c['text'],old,c['t'])); off+=len(norm(c['text']))
for i,c in enumerate(C):
    if i+1<len(C): c['end']=C[i+1]['t']
    if i>0 and c['t']<C[i-1]['t']+0.15: c['t']=round(C[i-1]['t']+0.15,2); C[i-1]['end']=c['t']
C[0]['t']=max(0,C[0]['t'])
json.dump(C,open('script/captions.json','w'),ensure_ascii=False,indent=0)
for o in out: print(o[0],o[1],o[2],'->',o[3],round(o[3]-o[2],2))
