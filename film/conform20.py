"""Film 20. FRAMES=<conform_full frames dir> MUSICF=<rel path or empty>. usage: python3 conform20.py <g_end_exclusive> <out_basename> <cue_files...>   frames from v3/film2/*/frames (later takes override earlier)"""
import sys,json,glob,os,subprocess
P=os.path.dirname(os.path.abspath(__file__)); N=int(sys.argv[1]); out=sys.argv[2]; FPS=30; OFF=0.10
tmp=os.environ.get("FRAMES") or out+"_frames"; os.makedirs(tmp,exist_ok=True)
src={}
for d in sorted(glob.glob(P+"/v3/film20/s*/frames")):
    for f in glob.glob(d+"/g_*.png"): src[int(f[-8:-4])]=f
for g in ([] if os.environ.get("FRAMES") else range(N)):
    l=f"{tmp}/f_{g:04d}.png"
    if os.path.lexists(l): os.remove(l)
    os.symlink(src[g],l)
caps=json.load(open(P+"/film20/script/captions.json")); T=N/FPS
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
B9=P+"/film20/audio/sfx/"
sfx=[]
def add(f,t,db,ln):
    if t<T: sfx.append({"file":B9+f,"at":t,"peak_db":db,"len":min(ln,T-t),"align":"onset","fade_out":0.08})
for f,t,db,ln in [
 ("hmph",1.75,-18,0.6),("whoosh_soft",0.85,-28,0.8),("cutlery_clink",3.5,-18,0.8),("whoosh_whip",4.55,-26,0.6),("happy_hum",4.9,-20,1.2),
 ("whoosh_soft",5.9,-30,0.8),("crane_creak",7.0,-22,2.5),("rivet_hammer",9.6,-20,1.2),("whoosh_soft",11.4,-26,0.8),("forge_whoosh",12.2,-24,2.0),
 ("newspaper_rustle",13.6,-20,1.5),("artists_outrage",14.6,-22,2.5),("quill_scratch",15.6,-20,1.2),("quill_scratch",16.4,-22,1.0),("artists_outrage",17.9,-22,2.0),
 ("chair_scrape",20.3,-18,0.8),("whoosh_punch",24.3,-22,0.5),("crowd_laugh_street",25.3,-20,2.5),("whoosh_punch",26.62,-18,0.5),
 ("crane_creak",27.6,-22,2.5),("girder_clank",29.0,-18,1.0),("rivet_catch",30.4,-16,0.8),("rivet_hammer",30.9,-18,1.2),
 ("whoosh_whip",31.5,-24,0.6),("whoosh_whip",32.15,-24,0.6),("whoosh_whip",32.65,-22,0.6),("seal_stamp",34.4,-16,0.6),("gulp",35.6,-18,0.6),
 ("artists_laugh",37.0,-20,2.5),("crowbar_clank",41.2,-20,1.2),("wire_twang",44.2,-18,1.2),("whoosh_whip",44.7,-22,0.6),("morse_key",46.2,-18,2.0),
 ("spark_gap",46.6,-18,1.6),("whoosh_whip",47.8,-22,0.6),("radio_hum",48.0,-22,4.0),("tools_drop",52.3,-16,1.2),("salute_stomp",53.6,-16,0.5),
 ("wagon_roll",54.4,-22,3.0),("seal_stamp",56.0,-18,0.6),("whoosh_soft",57.8,-28,0.8),("cutlery_clink",60.6,-18,0.8),("happy_hum",61.3,-20,1.2),
 ("glass_toast",64.4,-18,0.6),("whoosh_whip",65.7,-22,0.6),("happy_hum",67.0,-20,1.0)]:
    add(f+".mp3",t,db,ln)
BEDS=[("paris_day",0,2.67),("resto_bed",2.67,5.93),("site_bed",5.93,13.47),("cafe_bed",13.47,25.09),("site_bed",25.09,33.21),("fair_crowd",33.21,36.44),("cafe_bed",36.44,40.7),("dusk_wind",40.7,52.02),("fair_crowd",55.21,57.75),("resto_bed",57.75,65.6),("paris_day",65.6,68.2)]
for n,a_,b_ in BEDS:
    t=a_
    while t<b_-0.5:
        sfx.append({"file":B9+n+".mp3","at":t,"peak_db":-32,"len":min(5.5,b_-t),"align":"onset","fade_out":0.4}); t+=5.4
spec_voice_file=P+"/film20/audio/narration.wav"
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
 "voice":{"file":P+"/film20/audio/narration.wav","at":OFF,"gain":10**((float(os.environ.get("VOICE_DB","-14.4"))-float(os.environ.get("NARR_DB","-17.3")))/20)},
 "sfx":sfx}
if os.environ.get("MUSICF"): spec["music"]={"file":P+os.environ["MUSICF"],"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-31")),"fade_in":0.3,"fade_out":0.6}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
# true-peak guard (film 20): trim the mixed audio so the final is <= -1 dBTP; video stream copied
import re as _re
def _tp(f):
    r=subprocess.run(["ffmpeg","-v","info","-nostats","-i",f,"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
    return float(_re.findall(r"Peak:\s+(-?[\d.]+) dBFS",r)[-1])
_p=_tp(out+".mp4"); _q=_p
for _lim in (0.80,0.75,0.70):              # 4x-oversampled limiter on the mix wav, one AAC encode, video copied
    if _q<=-1.0: break
    subprocess.run(["ffmpeg","-y","-v","error","-i",out+"_silent.mp4","-i",out+".wav","-map","0:v","-map","1:a","-c:v","copy","-af",f"aresample=192000,alimiter=limit={_lim}:attack=1:release=50:level=disabled,aresample=48000","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",out+"_tp.mp4"],check=True)
    os.replace(out+"_tp.mp4",out+".mp4"); _q=_tp(out+".mp4")
print(f"true peak before {_p:.2f} dBTP, after {_q:.2f} dBTP")
