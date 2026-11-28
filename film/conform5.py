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
caps=json.load(open(P+"/film5/script/captions.json")); T=N/FPS
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
A=P+"/audio/sfx/"; B3=P+"/film3/audio/sfx/"; B4=P+"/film4/audio/sfx/"; B5=P+"/film5/audio/sfx/"
LIB={"hammer_hit":("hammer.mp3",-12,0.35),"hammer_hit_far":("hammer.mp3",-30,0.3),"camera_snap":("whoosh.mp3",-17,0.6),"cut":(None,),"dissolve":("whoosh.mp3",-24,0.8),
     "strike":("strike.mp3",-6,2.5),"thunder":("thunder.mp3",-16,3.5),"bells":("bells.mp3",-20,4),"rain":("rain.mp3",-30,float(os.environ.get("RAINLEN","6"))),"crowd":("crowd.mp3",-20,3),
     "explosion":("explosion.mp3",-5,5),"crackle":("crackle.mp3",-18,2),"rope":("rope.mp3",-18,2),"page":("page.mp3",-18,1),"birds":("birds.mp3",-28,4),"laugh":("crowd.mp3",-22,2),"bell":("bells.mp3",-18,2.5),"thunder_far":("thunder.mp3",-26,3.5),"thunder_rumble":("thunder.mp3",-20,4),"lightning":("strike.mp3",-12,2),"bolt_far":("thunder.mp3",-24,3),"crowd_laugh":("crowd.mp3",-17,3),"crackle_soft":("crackle.mp3",-26,1.5),"crackle_faint":("crackle.mp3",-30,1.5),"crackle_branch":("crackle.mp3",-20,1.5),"crackle_up":("crackle.mp3",-20,1.5),"whip":("whoosh.mp3",-14,0.8),"impact":("strike.mp3",-14,1.2),"debris":("explosion.mp3",-20,3),"pull":("rope.mp3",-20,1),"riser":("whoosh.mp3",-20,1.5)}

LIB.update({k:(B3+v[0],)+v[1:] for k,v in {"drip":("drip.mp3",-26,1.2),"groan":("groan.mp3",-18,3),"groan_low":("groan.mp3",-24,3),"rivets":("rivets.mp3",-8,3),"rivet":("rivets.mp3",-12,1),"burst":("burst.mp3",-6,3),"wave":("wave.mp3",-8,5),"flood":("wave.mp3",-8,5),"kick":("kick.mp3",-12,2),"clatter":("kick.mp3",-14,2),"brush":("brush.mp3",-20,2),"paint":("brush.mp3",-20,2),"train":("train.mp3",-22,4),"harbor":("harbor.mp3",-30,6),"laugh":("laugh.mp3",-18,3),"workers_laugh":("laugh.mp3",-18,3),"crowd_laugh":("laugh.mp3",-18,3),"pour":("drip.mp3",-24,2),"creak":("groan.mp3",-26,2),"rivet_shot":("rivets.mp3",-16,0.6),"rumble":("groan.mp3",-20,3),"overflow":("drip.mp3",-24,2),"drip_slide":("drip.mp3",-26,1.5),"squirts":("drip.mp3",-24,1.5),"splash":("wave.mp3",-18,1.5),"bucket":("kick.mp3",-22,1),"clank":("kick.mp3",-22,0.8),"bucket_scrape":("kick.mp3",-24,1)}.items()})

LIB.update({k:(B4+v[0],)+v[1:] for k,v in {"quake":("quake.mp3",-10,4),"impact":("hammer.mp3",-14,0.6),"footstep":("running.mp3",-24,1),"laugh":("crowd.mp3",-17,3),"crack":("creak.mp3",-14,2),"chain":("chain.mp3",-18,1.5),"rattle":("bells.mp3",-20,2),"snap":("collapse.mp3",-6,2),"fall":("collapse.mp3",-6,5),"dust":("collapse.mp3",-16,3),"camera_snap":("whoosh.mp3",-18,0.6),"dissolve":("whoosh.mp3",-26,0.8),"creak":("creak.mp3",-16,3),"trowel":("trowel.mp3",-18,2),"bells":("bells.mp3",-22,3)}.items()})

LIB.update({k:(B5+v[0],)+v[1:] for k,v in {"sing":("chirp.mp3",-16,2.5),"song":("chirp.mp3",-16,2.5),"chirp":("chirp1.mp3",-16,1),"note":("chirp1.mp3",-18,1),"bird":("chirp1.mp3",-18,1),"lamp":("lamp.mp3",-20,2),"flame":("lamp.mp3",-18,2),"blast":("blast.mp3",-4,5),"explosion":("blast.mp3",-4,5),"fireball":("blast.mp3",-4,5),"pick":("pick.mp3",-22,1.5),"footstep":("run.mp3",-20,1.2),"run":("run.mp3",-16,2),"laugh":("laugh.mp3",-17,3),"cage":("cage.mp3",-20,1),"rattle":("cage.mp3",-20,1),"camera_snap":("whoosh.mp3",-18,0.6),"whoosh":("whoosh.mp3",-16,0.8),"bird_song":("chirp.mp3",-17,2.5),"laughter":("laugh.mp3",-17,3),"impact":("blast.mp3",-10,2),"shout":("whoosh.mp3",-24,0.5),"oxygen":("oxygen.mp3",-14,2),"hiss":("oxygen.mp3",-14,2)}.items()})
sfx=[]
for cf in sys.argv[3:]:
    for c in json.load(open(cf))["cues"]:
        k=c["kind"]; lab=c.get("label","").lower()
        if k=="ambience": k=None
        if k=="foley" and "trowel" in lab: k="trowel"
        if k=="fx" and ("blast" in lab or "fire" in lab or "explo" in lab): k="blast"
        if k=="foley" and ("oxygen" in lab or "hiss" in lab): k="oxygen"
        if k=="prop" and "cage" in lab: k="cage"
        e=LIB.get(k)
        if not e or not e[0] or c["time"]>=T: continue
        sfx.append({"file":(e[0] if e[0].startswith("/") else A+e[0]),"at":c["time"],"peak_db":e[1],"len":min(e[2],T-c["time"]),"align":"onset","fade_out":0.08})
spec={"duration":T,"out_wav":out+".wav","video_in":out+"_silent.mp4","video_out":out+".mp4",
 "voice":{"file":P+"/film5/audio/narration_bankky.wav","at":OFF,"gain":10**((float(os.environ.get("VOICE_DB","-14.4"))-float(os.environ.get("NARR_DB","-17.2")))/20)},
 "music":{"file":P+os.environ.get("MUSICF","/film4/audio/music_suno.wav"),"at":0,"rms_db":float(os.environ.get("MUSIC_DB","-38")),"fade_in":0.3,"fade_out":0.6},"sfx":sfx}
json.dump(spec,open(out+"_mix.json","w"),indent=1)
subprocess.run([sys.executable,P+"/audio/mixer.py",out+"_mix.json"],check=True)
