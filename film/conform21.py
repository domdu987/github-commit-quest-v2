"""usage: [N=1848] python3 conform21.py <takes_root> <out_basename>
Film 21 conform: frames from conform_full.py (<takes_root>/sNN/{meta.json,take.mkv}, see film21/fetch_takes.sh), captions + narration +
music + SFX from film21/. Writes <out>.ass, <out>_silent.mp4, <out>_mix.json, <out>.wav, <out>.mp4.
env: N (frames, default 2052)  FRAMES=<dir of f_%04d.png> (skip conform_full)  VOICE_DB (-14.4)  MUSIC_DB (-31)
     NARR_DB (RMS of narration.wav; default = measured, ~-17.7)  MUSICF (abs path, default film21/audio/music.mp3)"""
import sys,json,os,subprocess
import numpy as np
P=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,P+"/audio"); import mixer
root,out=sys.argv[1],sys.argv[2]; N=int(os.environ.get("N","1848")); FPS=30; OFF=0.10; T=N/FPS
F17=P+"/film21"; NARR=F17+"/audio/narration.wav"; SFXD=F17+"/audio/sfx/"
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

# ---- SFX cue list. Times are NARRATION time (OFF added below); shot numbers refer to film21/shot_plan.md
# (file, narration t, peak_db, len, extra)
CUES=[
 # hooves on planks (shots 1 bridge far, 9, 20, 26)
 ("hooves_planks",1.2,-28,2.5,{"fade_out":0.6}),
 ("hooves_planks",16.6,-21,1.5,{}),
 ("hooves_planks",38.0,-24,1.8,{"fade_out":0.4}),
 ("wood_creak",50.6,-21,2.0,{}),                         # 26 the jam
 ("hooves_planks",50.8,-24,1.6,{}),
 ("wood_creak",52.6,-23,1.8,{"fade_out":0.4}),           # 27
 # coins (10, 28)
 ("coin_clink",18.4,-21,1.2,{}),
 ("coin_clink",19.6,-23,1.0,{}),
 # crowd laughs (13, 18)
 ("crowd_laugh",26.4,-19,2.4,{}),
 ("crowd_laugh",34.75,-19,1.6,{}),
 # river bed ambience under the count (15-17) and the ending (29-30)
 ("river_bed",29.4,-32,5.0,{"fade_out":0.8}),
 ("river_bed",56.9,-31,3.6,{"fade_out":0.4}),
 # the horn (21), charge (22), spear wall (23)
 ("horn_blast",39.69,-13,2.3,{"noduck":1,"fade_out":0.6}),
 ("whoosh",41.15,-24,0.6,{}),
 ("charge_run",41.3,-20,2.0,{"fade_out":0.5}),
 ("spear_wall",43.78,-16,1.2,{}),
 # reveal sting on the bridgehead closing + whoosh into BIGZOOM 2
 ("sting",44.42,-18,2.0,{"fade_out":0.4}),
 ("whoosh",47.45,-25,0.7,{}),
 # ending: scale tips + chest slams (28)
 ("chest_slam",56.22,-17,1.2,{}),
 # splashes (30) and the three "ตูม" (31)
 ("splash_big",59.2,-18,1.2,{}),
 ("splash_big",59.75,-19,1.2,{}),
 ("splash_big",60.6,-14,0.9,{"noduck":1}),
 ("splash_big",60.9,-14,0.9,{"noduck":1}),
 ("splash_big",61.2,-13,0.45,{"noduck":1}),
 # nickname punch-in whoosh (14) and snaps
 ("whoosh",27.8,-25,0.6,{}),
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
        if any(k in _x["file"] for k in ("laugh","river_bed","charge")): _x["peak_db"]-=4
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
