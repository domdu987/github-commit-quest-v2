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
caps=json.load(open(P+"/film9/script/captions.json")); T=N/FPS
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
B9=P+"/film9/audio/sfx/"
sfx=[]
def add(f,t,db,ln):
    if t<T: sfx.append({"file":B9+f,"at":t,"peak_db":db,"len":min(ln,T-t),"align":"onset","fade_out":0.08})
for f,t,db,ln in [("bubble",0.2,-20,3),("pour",2.0,-18,1.5),("trowel",3.0,-20,1.2),("whoosh",3.7,-24,0.6),("drums",7.0,-26,3),
 ("laugh",11.0,-18,2.5),("crowd_laugh",14.6,-19,2.5),("brick",18.0,-20,1.2),("bubble",21.0,-24,2),("brick",24.0,-20,1.2),("brick",25.4,-20,1.2),
 ("laugh",28.0,-20,2.5),("thunder",29.6,-22,3),("laugh",33.0,-20,2),("drums",34.8,-20,4),("fuse",36.5,-20,1.5),
 ("cannon",39.4,-14,2),("impact",40.0,-13,1.5),("crack",40.6,-15,1.5),("cannon",43.6,-15,2),("dent",44.2,-14,1.2),("shimmer",44.5,-20,2),
 ("birds",47.3,-26,4),("cannon",52.0,-15,2),("impact",52.6,-13,1.5),("crack",53.0,-15,1.5),("cannon",54.0,-15,2),("crack",54.6,-14,1.5),
 ("cannon",55.8,-15,2),("collapse",56.3,-11,3),("helmet",57.6,-18,1.2)]:
    add(f+".mp3",t,db,ln)
BEDS=[("site",0,9.01),("site",9.01,29.57),("rain",29.57,34.7),("site",47.11,51.79)]
for n,a_,b_ in BEDS:
    t=a_
    while t<b_-0.5:
        sfx.append({"file":B9+n+".mp3","at":t,"peak_db":-32,"len":min(5.5,b_-t),"align":"onset","fade_out":0.4}); t+=5.4
spec_voice_file=P+"/film9/audio/narration.wav"
# duck: SFX overlapping narration get -6 dB, beds -3 dB
import numpy as _np
_v=_np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",spec_voice_file,"-ac","1","-ar","8000","-f","f32le","-"],capture_output=True).stdout,_np.float32)
_env=_np.sqrt(_np.convolve(_v**2,_np.ones(800)/800,"same"))[::80]
def _talk(a,ln):
    i0=int((a-OFF)*100); i1=int((a-OFF+ln)*100)
    seg=_env[max(0,i0):max(0,i1)]
    return seg.size>0 and (seg>0.02).mean()>0.3
for _x in sfx:
    if _talk(_x["at"],_x["len"]): _x["peak_db"]-=6 if _x["len"]<3 else 3
    if _talk(_x["at"],_x["len"]) and any(k in _x["file"] for k in ("laugh","gasp","drag","paper","cheer","murmur","search")): _x["peak_db"]-=4
sfx=[_x for _x in sfx if "trunk" not in _x["file"] or _x["len"]>0.5]
spec={"duration":T,"out_wav":out+".wav","video_in":out+"_silent.mp4","video_out":out+".mp4",
 "voice":{"file":P+"/film9/audio/narration.wav","at":OFF,"gain":10**((float(os.environ.get("VOICE_DB","-14.4"))-float(os.environ.get("NARR_DB","-17.2")))/20)},
 "music":{"file":P+os.environ.get("MUSICF","/film6/audio/music_suno_full.wav"),"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-38")),"fade_in":0.3,"fade_out":0.6},"sfx":sfx}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
