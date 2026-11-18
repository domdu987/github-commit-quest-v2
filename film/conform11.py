"""Film 11 conform. usage: FRAMES=<conform_full frames dir> python3 conform11.py <N> <out_basename>
   captions + SFX + mix. Music: MUSICF=<path relative to film/> (client's Suno track); omitted -> no music bed."""
import sys,json,os,subprocess
import numpy as _np
P=os.path.dirname(os.path.abspath(__file__)); N=int(sys.argv[1]); out=sys.argv[2]; FPS=30; OFF=0.10
tmp=os.environ["FRAMES"]
caps=json.load(open(P+"/film11/script/captions.json")); T=N/FPS
ass=["[Script Info]","ScriptType: v4.00+","PlayResX: 720","PlayResY: 1280","WrapStyle: 2","","[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1","","[Events]",
"Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts=lambda t:f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
for c in caps:
    a=c["t"]+OFF; b=min((c["end"] or T)+OFF,T)
    if a>=T: continue
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
open(out+".ass","w").write("\n".join(ass))
subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-i",f"{tmp}/f_%04d.png","-frames:v",str(N),"-vf",f"ass={out}.ass:fontsdir={P}/fonts","-c:v","libx264","-pix_fmt","yuv420p","-crf","17","-movflags","+faststart",out+"_silent.mp4"],check=True)
B=P+"/film11/audio/sfx/"; sfx=[]
def add(f,t,db,ln):
    if t<T: sfx.append({"file":B+f+".mp3","at":t+OFF,"peak_db":db,"len":min(ln,T-t-OFF),"align":"onset","fade_out":0.08})
for f,t,db,ln in [("milk",0.2,-22,2.2),("lancet",1.8,-18,0.6),("whoosh",2.55,-26,0.6),("lancet",3.6,-17,0.6),
 ("moo",11.4,-22,2),("belly_laugh",13.7,-17,2.4),("boing",17.0,-18,0.8),("moo",17.5,-22,1.5),
 ("crowd_laugh",18.3,-19,2.4),("quill",19.8,-24,1.2),("quill",22.6,-24,1.2),
 ("fever",25.9,-24,3),("door",28.0,-20,1.2),("rooster",29.95,-22,2),("run",30.7,-20,1.6),
 ("lancet",35.8,-17,0.6),("crowd_gasp",40.0,-19,1.5),
 ("milk",41.2,-22,2.2),("shimmer",43.45,-20,1.2),("moo",46.2,-23,2),("whoosh",49.5,-26,0.6),
 ("crowd_laugh",52.2,-26,1.5),("cow_chew",60.2,-24,2.2),("moo",60.8,-23,1.4)]:
    add(f,t,db,ln)
BEDS=[("barn",0,2.6),("village",2.6,10.6),("barn",10.6,13.58),("village",13.58,20.71),("night",20.71,25.86),("night",25.86,29.95),
 ("village",29.95,41.06),("barn",41.06,52.0),("village",52.0,60.2),("barn",60.2,62.5)]
for n,a_,b_ in BEDS:
    t=a_
    while t<b_-0.3:
        ln=min(5.8,b_-t); sfx.append({"file":B+n+".mp3","at":t+OFF,"peak_db":-32,"len":ln,"align":"onset","fade_out":0.3}); t+=ln
vf=P+"/film11/audio/narration.wav"
_v=_np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",vf,"-ac","1","-ar","8000","-f","f32le","-"],capture_output=True).stdout,_np.float32)
_env=_np.sqrt(_np.convolve(_v**2,_np.ones(800)/800,"same"))[::80]
def _talk(a,ln):
    seg=_env[max(0,int((a-OFF)*100)):max(0,int((a-OFF+ln)*100))]
    return seg.size>0 and (seg>0.02).mean()>0.3
for x in sfx:
    if _talk(x["at"],x["len"]):
        x["peak_db"]-=6 if x["len"]<3 else 3
        if any(k in x["file"] for k in ("laugh","gasp","crowd")): x["peak_db"]-=4
spec={"duration":T,"out_wav":out+".wav","video_in":out+"_silent.mp4","video_out":out+".mp4",
 "voice":{"file":vf,"at":OFF,"gain":10**((float(os.environ.get("VOICE_DB","-14.4"))-float(os.environ.get("NARR_DB","-17.2")))/20)},"sfx":sfx}
if os.environ.get("MUSICF"):
    spec["music"]={"file":P+os.environ["MUSICF"],"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-31")),"fade_in":0.3,"fade_out":0.6}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
