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
"Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1","","[Events]",
"Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts=lambda t:f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
for c in caps:
    a=c["t"]+OFF; b=min(c["end"]+OFF,T)
    if a>=T: continue
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
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
def add(f,t,db,ln): sfx.append({"file":B6+f,"at":t,"peak_db":db,"len":ln,"align":"onset","fade_out":0.08})
for f,t,db,ln in [("loaf.mp3",1.6,-16,0.7),("loaf.mp3",2.3,-16,0.7),("whoosh.mp3",4.1,-24,0.6),("laugh.mp3",8.0,-19,2.5),("splat.mp3",9.0,-14,0.8),("splat.mp3",9.9,-14,0.8),
 ("clink.mp3",12.2,-20,0.8),("clink.mp3",13.4,-20,0.8),("scale.mp3",14.3,-20,1.5),("whoosh.mp3",18.0,-20,0.6),("thud.mp3",23.4,-18,1),("thud.mp3",23.8,-18,1),("thud.mp3",24.2,-18,1),
 ("laugh.mp3",27.4,-20,2),("loaf.mp3",29.6,-17,0.7),("hood.mp3",33.6,-18,0.8),("loaf.mp3",36.3,-16,0.7),("scale.mp3",36.8,-16,2),("gasp.mp3",38.2,-17,2),("drag.mp3",39.4,-19,2),
 ("scale.mp3",43.6,-19,1.5),("ding.mp3",41.6,-22,1),("steam.mp3",47.4,-20,2),("steam.mp3",49.5,-20,2),("ding.mp3",53.9,-20,1),("scale.mp3",54.2,-17,2),("cheer.mp3",56.0,-21,2.5),
 ("thud.mp3",60.9,-17,1),("laugh.mp3",61.4,-20,2.5),("splat.mp3",62.6,-12,0.8),("splat.mp3",63.6,-12,0.8)]:
    if t<T: add(f,t,db,min(ln,T-t))
BAK=[(0,4.12),(10.6,20.66),(26.42,31.57),(41.19,47.41)]
MKT=[(4.12,10.6),(20.66,26.42),(31.57,41.19),(53.99,T)]
for a_,b_ in MKT: sfx.append({"file":B6+"market.mp3","at":a_,"peak_db":-32,"len":min(6,b_-a_),"align":"onset","fade_out":0.3})
for a_,b_ in BAK: sfx.append({"file":B6+"oven.mp3","at":a_,"peak_db":-32,"len":min(4,b_-a_),"align":"onset","fade_out":0.3})
spec={"duration":T,"out_wav":out+".wav","video_in":out+"_silent.mp4","video_out":out+".mp4",
 "voice":{"file":P+"/film6b/audio/narration.wav","at":OFF,"gain":10**((float(os.environ.get("VOICE_DB","-14.4"))-float(os.environ.get("NARR_DB","-17.2")))/20)},
 "music":{"file":P+os.environ.get("MUSICF","/film6/audio/music_suno_full.wav"),"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-38")),"fade_in":0.3,"fade_out":0.6},"sfx":sfx}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
