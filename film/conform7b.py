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
caps=json.load(open(P+"/film7b/script/captions.json")); T=N/FPS
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
B7=P+"/film7/audio/sfx/"
RULES=[(("laugh","jeer","mock"),"laugh.mp3",-19,2.5),(("gasp","shock"),"gasp.mp3",-18,2),(("hook","lift","frame off","unhook"),"frame.mp3",-16,1.2),
 (("unframe","pry","prise","glass"),"unframe.mp3",-17,1.5),(("rattle","locked","knob"),"rattle.mp3",-15,1.2),(("key","unlock","door swing","door open"),"key.mp3",-16,1.6),
 (("newspaper","paper","rustl"),"paper.mp3",-20,1),(("whistle",),"whistle.mp3",-18,1),(("search","drawer","rummag"),"search.mp3",-20,2.5),
 (("trunk","lid"),"trunk.mp3",-16,2),(("burst","bang","slam"),"thud.mp3",-14,1),(("sneak","footst","tiptoe","walk"),"footstep.mp3",-24,1.2),
 (("idea","realis","ding","sparkl"),"ding.mp3",-20,1),(("sting","gulp","nervous","sweat"),"sting.mp3",-22,1.5),(("whip","swish","whoosh","cut","framing"),"whoosh.mp3",-28,0.5)]
def pick(kind,lab):
    if kind in("ambience","music","end","transition","vocal","vocal-nonverbal") and not any(k in lab for k in("laugh","gasp")): return None
    for keys,f,db,ln in RULES:
        if any(k in lab for k in keys): return (B7+f,db,ln)
    return None
sfx=[]
def add(f,t,db,ln):
    if t<T: sfx.append({"file":B7+f,"at":t,"peak_db":db,"len":min(ln,T-t),"align":"onset","fade_out":0.08})
for f,t,db,ln in [("sting.mp3",0.3,-20,1.5),("footstep.mp3",1.8,-22,1.2),("whoosh.mp3",4.4,-24,0.6),("murmur.mp3",5.0,-30,4),("laugh.mp3",21.5,-18,2.5),
 ("frame.mp3",26.0,-16,1.2),("unframe.mp3",27.5,-17,1.5),("rattle.mp3",29.1,-15,1.2),("key.mp3",31.0,-16,1.6),("footstep.mp3",32.6,-22,1.2),
 ("sting.mp3",34.2,-22,1.5),("whistle.mp3",39.8,-18,1),("search.mp3",40.3,-20,2.5),("gasp.mp3",45.3,-18,2),("murmur.mp3",46.0,-26,4),
 ("paper.mp3",50.6,-18,1),("paper.mp3",51.6,-18,1),("trunk.mp3",50.5,-30,0.1),("thud.mp3",52.8,-14,1),("whistle.mp3",53.4,-18,1),("gasp.mp3",56.6,-17,2),("sting.mp3",57.3,-18,1.5)]:
    add(f,t,db,ln)
BEDS=[("museum",0.0,1.6),("street",1.6,4.38),("museum",4.38,24.87),("museum",24.87,39.67),("murmur",39.67,50.47),("street",50.47,52.0),("night",52.0,54.79),("museum",54.79,T)]
for n,a_,b_ in BEDS:
    t=a_
    while t<b_-0.5:
        sfx.append({"file":B7+n+".mp3","at":t,"peak_db":-32 if n!="murmur" else -29,"len":min(5.5,b_-t),"align":"onset","fade_out":0.4}); t+=5.4
spec={"duration":T,"out_wav":out+".wav","video_in":out+"_silent.mp4","video_out":out+".mp4",
 "voice":{"file":P+"/film7b/audio/narration.wav","at":OFF,"gain":10**((float(os.environ.get("VOICE_DB","-14.4"))-float(os.environ.get("NARR_DB","-17.2")))/20)},
 "music":{"file":P+os.environ.get("MUSICF","/film7/audio/music_suno.wav"),"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-38")),"fade_in":0.3,"fade_out":0.6},"sfx":sfx}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
