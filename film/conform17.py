"""usage: [N=2052] python3 conform17.py <takes_root> <out_basename>
Film 17 conform: frames from conform_full.py (<takes_root>/sNN/{meta.json,take.mkv}, see film17/fetch_takes.sh), captions + narration +
music + SFX from film17/. Writes <out>.ass, <out>_silent.mp4, <out>_mix.json, <out>.wav, <out>.mp4.
env: N (frames, default 2052)  FRAMES=<dir of f_%04d.png> (skip conform_full)  VOICE_DB (-14.4)  MUSIC_DB (-31)
     NARR_DB (RMS of narration.wav; default = measured, ~-17.7)  MUSICF (abs path, default film17/audio/music.mp3)"""
import sys,json,os,subprocess
import numpy as np
P=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,P+"/audio"); import mixer
root,out=sys.argv[1],sys.argv[2]; N=int(os.environ.get("N","2052")); FPS=30; OFF=0.10; T=N/FPS
F17=P+"/film17"; NARR=F17+"/audio/narration.wav"; SFXD=F17+"/audio/sfx/"
tmp=os.environ.get("FRAMES")
if not tmp:
    subprocess.run([sys.executable,P+"/conform_full.py",root,out],check=True,env={**os.environ,"N":str(N)}); tmp=out+"_frames"
caps=json.load(open(F17+"/script/captions.json"))
ass=["[Script Info]","ScriptType: v4.00+","PlayResX: 720","PlayResY: 1280","WrapStyle: 2","","[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1","","[Events]",
"Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts=lambda t:f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
for c in caps:
    a=max(0,c["t"])+OFF; b=min(c["end"]+OFF,T)
    if a>=T: continue
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
open(out+".ass","w").write("\n".join(ass))
subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-i",f"{tmp}/f_%04d.png","-vf",f"ass={out}.ass:fontsdir={P}/fonts","-c:v","libx264","-pix_fmt","yuv420p","-crf","17","-movflags","+faststart",out+"_silent.mp4"],check=True)

# ---- SFX cue list. Times are NARRATION time (OFF added below); shot numbers refer to film17/shot_plan.md
# (file, narration t, peak_db, len, extra)
CUES=[
 # calipers click (shots 1, 3, 16-18, 24-26, 32-33)
 ("caliper_click",0.95,-20,1.2,{}),                       # 1  closes on the ear
 ("caliper_click2",3.35,-21,1.0,{}),                      # 3  first ear
 ("caliper_click",4.25,-21,1.0,{}),                       # 3  snap to next ear ("ทีละหู")
 ("caliper_click2",28.8,-21,1.0,{}),                      # 16 head length
 ("caliper_click",30.4,-22,1.0,{}),                       # 17 gauge / foot
 ("caliper_click2",32.2,-22,1.0,{}),                      # 18 arm-span
 ("caliper_click",45.25,-20,1.0,{}),                      # 24 calipers on dupont's head
 ("caliper_click2",47.3,-21,1.0,{}),                      # 25 finger measure
 ("caliper_click",49.2,-21,1.0,{}),                       # 26 ear
 ("caliper_click2",65.7,-20,1.2,{}),                      # 32 closes on the inspector's ear
 ("caliper_click",67.4,-18,1.2,{}),                       # 33 callback punch (cut on "ตัวเอง")
 # crowd laughter (9, 13, 21)
 ("crowd_laugh",14.9,-19,1.6,{}),
 ("crowd_laugh",21.7,-19,2.4,{}),
 ("crowd_laugh",38.5,-23,1.4,{}),                         # 21 gendarmes snicker
 # wagon wheels + horse (4-5)
 ("wagon_horse",4.8,-23,4.0,{"fade_out":0.5}),
 ("wagon_horse",8.9,-29,1.2,{"start":1.0,"fade_out":0.5}),
 # drawer slide (19, 24-25)
 ("drawer_slide",33.6,-19,1.7,{}),
 ("drawer_slide",45.7,-18,1.4,{}),
 ("drawer_slide",47.0,-20,1.2,{"start":0.4}),
 # paper flutter (26-27, 30)
 ("paper_flutter",49.6,-22,1.4,{}),
 ("paper_flutter",51.2,-25,1.0,{"start":0.6}),
 ("paper_flutter",60.0,-22,2.0,{}),
 # gasp (28)
 ("gasp",53.95,-19,1.6,{}),
 # sting on "มาร์แตง" (shot 28, word starts 53.36 in captions.json); not ducked
 ("sting",53.36,-16,2.2,{"noduck":1,"fade_out":0.4}),
 # whips / snaps
 ("whoosh",44.62,-27,0.6,{}),("whoosh",55.05,-27,0.6,{}),
 # clock tick bed under 20-21 (34.74-39.76)
 ("clock_tick",34.9,-28,4.0,{"fade_out":0.3}),
 ("clock_tick",38.8,-28,1.0,{"fade_out":0.3}),
]
sfx=[]
for f,t,db,ln,x in CUES:
    at=t+OFF
    if at<T: sfx.append({"file":SFXD+f+".mp3","at":at,"peak_db":db,"len":min(ln,T-at),"align":"onset","fade_out":0.08,**x})
# duck (same logic as conform10): SFX overlapping narration get -6 dB (-3 if >=3 s); laugh/gasp/paper extra -4
v=mixer.load(NARR); narr_db=20*np.log10(np.sqrt((v**2).mean()))
_env=np.sqrt(np.convolve(v.mean(1)[::6]**2,np.ones(800)/800,"same"))[::80]   # 8 kHz -> 100 Hz envelope
def _talk(a,ln):
    i0=int((a-OFF)*100); i1=int((a-OFF+ln)*100); seg=_env[max(0,i0):max(0,i1)]
    return seg.size>0 and (seg>0.02).mean()>0.3
for _x in sfx:
    if _x.pop("noduck",0): continue
    if _talk(_x["at"],_x["len"]):
        _x["peak_db"]-=6 if _x["len"]<3 else 3
        if any(k in _x["file"] for k in ("laugh","gasp","paper","wagon","clock")): _x["peak_db"]-=4
NARR_DB=float(os.environ.get("NARR_DB",narr_db)); VOICE_DB=float(os.environ.get("VOICE_DB","-14.4"))
spec={"duration":T,"out_wav":out+".wav","video_in":out+"_silent.mp4","video_out":out+".mp4",
 "voice":{"file":NARR,"at":OFF,"gain":10**((VOICE_DB-NARR_DB)/20)},
 "music":{"file":os.environ.get("MUSICF",F17+"/audio/music.mp3"),"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-31")),"fade_in":0.3,"fade_out":0.6},"sfx":sfx}
print(f"narration RMS {narr_db:.2f} dBFS (using NARR_DB {NARR_DB:.2f}), voice target {VOICE_DB}, gain {spec['voice']['gain']:.3f}, music {spec['music']['rms_db']}, sfx {len(sfx)}")
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
# true-peak safety: mixer's limiter is sample-peak -1 dBFS (0.89); a 2nd limiter at 0.80 keeps true peak (and AAC overshoot) under -1 dBTP
subprocess.run(["ffmpeg","-y","-v","error","-i",out+".wav","-af","alimiter=limit=0.80:attack=2:release=40:level=disabled","-ar","48000",out+"_tp.wav"],check=True)
os.replace(out+"_tp.wav",out+".wav")
subprocess.run(["ffmpeg","-y","-v","error","-i",out+"_silent.mp4","-i",out+".wav","-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out+".mp4"],check=True)
print("final",out+".mp4")
