"""usage: python3 conform.py <g_end_exclusive> <out_basename> <cue_files...>   frames from v3/film2/*/frames (later takes override earlier)"""
import sys,json,glob,os,subprocess
P=os.path.dirname(os.path.abspath(__file__)); N=int(sys.argv[1]); out=sys.argv[2]; FPS=30; OFF=0.10
tmp=out+"_frames"; os.makedirs(tmp,exist_ok=True)
src={}
for d in sorted(glob.glob(P+"/v3/film2/s*/frames")):
    for f in glob.glob(d+"/g_*.png"): src[int(f[-8:-4])]=f
for g in range(N):
    l=f"{tmp}/f_{g:04d}.png"
    if os.path.lexists(l): os.remove(l)
    os.symlink(src[g],l)
caps=json.load(open(P+"/script/captions.json")); T=N/FPS
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
A=P+"/audio/sfx/"
LIB={"hammer_hit":("hammer.mp3",-12,0.35),"hammer_hit_far":("hammer.mp3",-30,0.3),"camera_snap":("whoosh.mp3",-17,0.6),"cut":(None,),"dissolve":("whoosh.mp3",-24,0.8),
     "strike":("strike.mp3",-6,2.5),"thunder":("thunder.mp3",-16,3.5),"bells":("bells.mp3",-20,4),"rain":("rain.mp3",-30,6),"crowd":("crowd.mp3",-20,3),
     "explosion":("explosion.mp3",-5,5),"crackle":("crackle.mp3",-18,2),"rope":("rope.mp3",-18,2),"page":("page.mp3",-18,1),"birds":("birds.mp3",-28,4),"laugh":("crowd.mp3",-22,2)}
sfx=[]
for cf in sys.argv[3:]:
    for c in json.load(open(cf))["cues"]:
        k=c["kind"]; e=LIB.get(k)
        if not e or not e[0] or c["time"]>=T: continue
        sfx.append({"file":A+e[0],"at":c["time"],"peak_db":e[1],"len":min(e[2],T-c["time"]),"align":"onset","fade_out":0.08})
spec={"duration":T,"out_wav":out+".wav","video_in":out+"_silent.mp4","video_out":out+".mp4",
 "voice":{"file":P+"/audio/narration.wav","at":OFF,"gain":10**((-17.4-(-17.2))/20)},
 "music":{"file":P+"/audio/music.mp3","at":0,"rms_db":-36,"fade_in":0.3,"fade_out":0.6},"sfx":sfx}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
