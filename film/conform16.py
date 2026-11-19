"""Film 16. FRAMES=<conform_full frames dir> MUSICF=<rel path or empty>. usage: python3 conform16.py <g_end_exclusive> <out_basename> <cue_files...>   frames from v3/film2/*/frames (later takes override earlier)"""
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
caps=json.load(open(P+"/film16/script/captions.json")); T=N/FPS
ass=["[Script Info]","ScriptType: v4.00+","PlayResX: 720","PlayResY: 1280","WrapStyle: 2","","[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1","","[Events]",
"Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts=lambda t:f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
for c in caps:
    a=c["t"]+OFF; b=min((c["end"] if c.get("end") is not None else T)+OFF,T)
    if a>=T: continue
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
open(out+".ass","w").write("\n".join(ass))
subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-i",f"{tmp}/f_%04d.png","-vf",f"ass={out}.ass:fontsdir={P}/fonts","-c:v","libx264","-pix_fmt","yuv420p","-crf","17","-movflags","+faststart",out+"_silent.mp4"],check=True)
B9=P+"/film16/audio/sfx/"
sfx=[]
def add(f,t,db,ln):
    if t<T: sfx.append({"file":B9+f,"at":t,"peak_db":db,"len":min(ln,T-t),"align":"onset","fade_out":0.08})
for f,t,db,ln in [("glass_clink",1.6,-16,0.7),("wire_twang",2.1,-20,0.8),("whoosh_fast",2.3,-26,0.6),("train_chug",3.7,-20,2.0),("train_whistle",5.0,-22,1.2),
 ("whoosh_fast",5.6,-28,0.6),("quill_scratch",8.6,-22,1.2),("letter_open",10.6,-20,1.0),("palette_drop",12.0,-18,0.8),("spark_zap",14.9,-18,0.6),
 ("chamber_tone",15.9,-30,2.3),("belly_laugh",18.0,-17,1.8),("chamber_laugh",23.3,-18,2.8),("gavel",26.2,-18,0.5),("coins_bag",27.0,-17,0.9),
 ("plough_dig",27.8,-20,2.0),("mule_bray",28.6,-22,1.2),("whoosh_fast",29.75,-26,0.5),("whoosh_fast",30.7,-26,0.5),("whoosh_fast",31.25,-26,0.5),
 ("telegraph_click",32.4,-22,0.5),("electric_crackle",33.6,-20,2.0),("bag_shake",35.9,-19,1.0),("buggy_rattle",37.3,-24,3.0),("belly_laugh",38.3,-20,1.2),
 ("pole_thud",41.9,-18,0.7),("electric_crackle",42.6,-22,2.0),("telegraph_click",45.0,-24,0.4),("glint_shimmer",46.3,-20,1.0),("glass_clink",49.6,-16,0.7),
 ("wire_twang",50.9,-20,0.8),("pulse_zip",51.4,-18,1.0),("glint_shimmer",52.2,-22,1.0),("train_chug",54.0,-20,2.8),("pulse_zip",56.0,-20,1.0),
 ("telegraph_click",57.66,-16,0.8),("crowd_gasp",58.2,-20,1.2),("train_whistle",59.0,-22,1.2),("crowd_cheer",59.4,-22,0.8),("whoosh_fast",60.2,-28,0.6),
 ("coins_bag",61.0,-24,0.8),("whoosh_fast",63.2,-26,0.6),("crowd_gasp",65.1,-22,0.9),("telegraph_click",66.3,-22,1.5),("yawn",67.4,-20,1.6),("telegraph_click",68.8,-22,1.0)]:
    add(f+".mp3",t,db,ln)
BEDS=[("field_day",0,5.6),("studio_tone",5.6,15.86),("chamber_tone",18.0,26.2),("field_day",27.7,31.9),("silence_wind",31.9,40.9),("rain_heavy",42.2,46.0),("field_day",46.0,56.9),("chamber_tone",56.9,58.9),("field_day",58.9,60.2),("chamber_tone",60.2,66.0),("candle_night",66.0,70.0)]
for n,a_,b_ in BEDS:
    t=a_
    while t<b_-0.5:
        sfx.append({"file":B9+n+".mp3","at":t,"peak_db":-32,"len":min(5.5,b_-t),"align":"onset","fade_out":0.4}); t+=5.4
spec_voice_file=P+"/film16/audio/narration.wav"
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
 "voice":{"file":P+"/film16/audio/narration.wav","at":OFF,"gain":10**((float(os.environ.get("VOICE_DB","-14.4"))-float(os.environ.get("NARR_DB","-17.2")))/20)},
 "sfx":sfx}
if os.environ.get("MUSICF"): spec["music"]={"file":P+os.environ["MUSICF"],"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-31")),"fade_in":0.3,"fade_out":0.6}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
