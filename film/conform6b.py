"""usage: python3 conform.py <g_end_exclusive> <out_basename> <cue_files...>   frames from v3/film2/*/frames (later takes override earlier)"""
import sys,json,glob,os,subprocess
P=os.path.dirname(os.path.abspath(__file__)); N=int(sys.argv[1]); out=sys.argv[2]; FPS=30; OFF=0.10
tmp=os.environ.get("FRAMES") or out+"_frames"; os.makedirs(tmp,exist_ok=True)
src={}
for d in sorted(glob.glob(P+"/v3/film2/s*/frames")):
    for f in glob.glob(d+"/g_*.png"): src[int(f[-8:-4])]=f
for g in ([] if os.environ.get("FRAMES") else range(N)):
    l=f"{tmp}/f_{g:04d}.png"
    if os.path.lexists(l): os.remove(l)
    os.symlink(src[g],l)
caps=json.load(open(P+"/film6b/script/captions.json")); T=N/FPS
ass=["[Script Info]","ScriptType: v4.00+","PlayResX: 720","PlayResY: 1280","WrapStyle: 2","","[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Pop,Kanit Black,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1","","[Events]",
"Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts=lambda t:f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
from pythainlp.tokenize import word_tokenize
words=[]
for c in caps:
    ws=[w for w in word_tokenize(c["text"].replace(" ",""),engine="newmm") if w.strip()]
    m=[]
    for w in ws:
        if m and (len(m[-1])<=2 or len(w)<=2) and len(m[-1])+len(w)<=9: m[-1]+=w
        else: m.append(w)
    tot=sum(len(w) for w in m); a=c["t"]; d=c["end"]-c["t"]; acc=0
    for w in m:
        words.append((a+d*acc/tot,a+d*(acc+len(w))/tot,w)); acc+=len(w)
for a,b,w in words:
    a+=OFF; b=min(b+OFF,T)
    if a>=T: continue
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{w}")
open(out+".ass","w").write("\n".join(ass))
subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-i",f"{tmp}/f_%04d.png","-vf",f"ass={out}.ass:fontsdir={P}/fonts","-c:v","libx264","-pix_fmt","yuv420p","-crf","17","-movflags","+faststart",out+"_silent.mp4"],check=True)
B6=P+"/film6/audio/sfx/"; B5=P+"/film5/audio/sfx/"
RULES=[(("splat","hits","tomato","cabbage hit"),"splat.mp3",-14,0.8),(("throw","swish","whoosh","hood"),"whoosh.mp3",-22,0.6),
 (("laugh","jeer"),"laugh.mp3",-19,2.5),(("gasp","ooh"),"gasp.mp3",-18,2),(("cheer","relief"),"cheer.mp3",-18,2.5),
 (("beam","balance","scale","needle","pan rises","creak"),"scale.mp3",-17,2),(("crumb","weights","tick","clink","tap"),"clink.mp3",-20,0.8),
 (("loaf","loaves","basket"),"loaf.mp3",-16,0.7),(("steam","droplet","plip","fwoomp","shimmer"),"steam.mp3",-22,2),
 (("running","run","footst","skid","hops"),"run.mp3",-20,1.5),(("dragged","drag","mail","trembling"),"drag.mp3",-20,2),
 (("pillory","slam","board"),"thud.mp3",-16,1),(("idea","eyes go wide","realisation","sparkl","beams","ding"),"ding.mp3",-20,1),
 (("crow","caw"),B5+"chirp1.mp3",-40,0),(("wink","grin","glance","cut","framing"),"whoosh.mp3",-28,0.5)]
def pick(kind,lab):
    if kind in("ambience","music","end","transition","vocal","vocal-nonverbal","gesture") and not any(k in lab for k in("laugh","jeer","gasp")): return None
    for keys,f,db,ln in RULES:
        if ln and any(k in lab for k in keys): return (f if f.startswith("/") else B6+f,db,ln)
    return None
sfx=[]
for cf in sys.argv[3:]:
    for c in json.load(open(cf))["cues"]:
        e=pick(c["kind"],(c["kind"]+" "+c.get("label","")).lower())
        if not e or c["time"]>=T: continue
        sfx.append({"file":e[0],"at":c["time"],"peak_db":e[1],"len":min(e[2],T-c["time"]),"align":"onset","fade_out":0.08})
BAK=[(0,4.1),(10.48,20.74),(26.56,32.15),(34.3,36.1),(41.27,48.6),(53.11,56.8)]
MKT=[(4.1,10.48),(20.74,26.56),(32.15,34.3),(36.1,41.27),(56.8,T)]
for a_,b_ in MKT: sfx.append({"file":B6+"market.mp3","at":a_,"peak_db":-32,"len":min(6,b_-a_),"align":"onset","fade_out":0.3})
for a_,b_ in BAK: sfx.append({"file":B6+"oven.mp3","at":a_,"peak_db":-32,"len":min(4,b_-a_),"align":"onset","fade_out":0.3})
spec={"duration":T,"out_wav":out+".wav","video_in":out+"_silent.mp4","video_out":out+".mp4",
 "voice":{"file":P+"/film6b/audio/narration.wav","at":OFF,"gain":10**((float(os.environ.get("VOICE_DB","-14.4"))-float(os.environ.get("NARR_DB","-17.2")))/20)},
 "music":{"file":P+os.environ.get("MUSICF","/film6/audio/music_suno_full.wav"),"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-38")),"fade_in":0.3,"fade_out":0.6},"sfx":sfx}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
