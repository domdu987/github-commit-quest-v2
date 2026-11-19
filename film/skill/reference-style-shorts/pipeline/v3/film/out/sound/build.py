import json, sys, numpy as np
P='__PROJ__'
OUT=P+'/v3/film/out'
sys.path.insert(0,P+'/audio'); import mixer
S=lambda n: P+'/audio/sfx/'+n+'.wav'
op=json.load(open(P+'/v3/out/mix_opening.json'))
vg=json.load(open(P+'/audio/music/mix_settings.json'))['voice_gain']
cues=json.load(open(OUT+'/cues_all.json'))['cues']
sfx=[]; table=[]
for e in op['sfx']:
    assert e['at']<5.0
    e2=dict(e); sfx.append(e2)
# hook cue labels for the table (nearest cue at same time)
def cue_at(t):
    c=min(cues,key=lambda c:abs(c['t']-t)); return c
for e in sfx: table.append(cue_at(e['at']))
# (at, sound, params, cue time, kind)  -- film after the hook, t >= 5.0
KEEP=[6.6, 7.9, 11.35, 13.05, 14.95, 18.4, 21.675, 23.25, 26.5, 28.1, 29.05, 32.58, 36.3, 37.42, 39.6, 43.3, 46.55, 48.1, 50.6, 53.72, 55.79, 57.35, 58.1, 60.1, 62.08, 64.0]
F=[
 # ambiences
 (5.0, 'office_tone', dict(rms_db=-34, start=0.3, len=1.65, fade_in=0.3, fade_out=0.4), 4.30, 'amb'),
 (13.3,'beach_calm',  dict(rms_db=-32, start=0.0, len=3.55, fade_in=0.8, fade_out=0.6), 13.30, 'amb'),
 (31.6,'rain_drizzle',dict(rms_db=-34, start=0.0, len=5.85, fade_in=0.4, fade_out=0.3), 31.60, 'amb'),
 (31.95,'office_tone',dict(rms_db=-34, start=0.0, len=1.85, fade_in=0.3, fade_out=0.4), 31.95, 'amb'),
 (33.77,'beach_calm', dict(rms_db=-34, start=1.5, len=2.45, fade_in=0.4, fade_out=0.5), 33.77, 'amb'),
 (36.2, 'office_tone',dict(rms_db=-33, start=2.0, len=1.24, fade_in=0.3, fade_out=0.03), 36.20, 'amb'),
 (39.62,'wind_storm', dict(rms_db=-33, start=0.0, len=5.0, fade_in=3.0, fade_out=1.0), 39.62, 'amb'),
 (45.0, 'wind_storm', dict(rms_db=-30, start=0.0, len=5.55, fade_in=2.5, fade_out=0.6), 47.50, 'amb'),
 (59.55,'rain_drizzle',dict(rms_db=-32, start=0.0, len=3.0, fade_in=0.3, fade_out=0.3), 59.55, 'amb'),
 (62.55,'wave_roar',  dict(rms_db=-31, start=1.6, len=1.85, fade_in=0.2, fade_out=0.8), 62.55, 'amb'),
 # point effects
 (5.66, 'thump_jab',  dict(peak_db=-15, align='onset', len=0.25), 5.66, 'pt'),
 (6.6,  'whoosh_whip',dict(peak_db=-13, pan=0.3), 6.60, 'pt'),
 (7.9,  'thunder_low',dict(peak_db=-20, align='onset', len=1.8, fade_out=0.8), 7.90, 'pt'),
 (9.15, 'pop_surprise',dict(peak_db=-16, len=0.35, fade_out=0.1, pan=-0.2), 9.15, 'pt'),
 (10.62,'thump_jab',  dict(peak_db=-14, align='onset', len=0.25), 10.62, 'pt'),
 (11.35,'pencil_scratch',dict(rms_db=-26, start=0.2, len=0.85, fade_out=0.1), 11.35, 'pt'),
 (12.43,'whoosh_fast',dict(peak_db=-16, len=0.4), 12.43, 'pt'),
 (13.05,'thump_jab',  dict(peak_db=-12, align='onset', len=0.25), 13.05, 'pt'),
 (14.95,'whoosh_fast',dict(peak_db=-15, len=0.5), 14.95, 'pt'),
 (17.78,'whoosh_fast',dict(peak_db=-13, len=0.5, pan=0.2), 17.78, 'pt'),
 (18.4, 'pencil_scratch',dict(rms_db=-25, start=0.5, len=0.9, fade_out=0.1), 18.40, 'pt'),
 (19.4, 'whoosh_whip',dict(peak_db=-15, pan=-0.2), 19.40, 'pt'),
 (21.675,'eraser_rub',dict(rms_db=-26, start=0.3, len=0.38, fade_out=0.06), 21.675, 'pt'),
 (23.25,'eraser_rub', dict(rms_db=-25, start=0.0, len=0.6, fade_out=0.08, pan=-0.2), 23.25, 'pt'),
 (23.85,'pencil_scratch',dict(rms_db=-25, start=0.3, len=0.55, fade_out=0.08, pan=0.2), 23.85, 'pt'),
 (24.85,'eraser_rub', dict(rms_db=-24, start=0.6, len=0.45, fade_out=0.08, pan=-0.2), 24.85, 'pt'),
 (25.35,'pencil_scratch',dict(rms_db=-24, start=1.0, len=0.27, fade_out=0.05, pan=0.2), 25.35, 'pt'),
 (26.5, 'crowd_chuckle',dict(peak_db=-15, len=1.48, fade_in=0.08, fade_out=0.5), 26.50, 'pt'),
 (27.6, 'paper_slide',dict(rms_db=-27, len=0.45, fade_out=0.1), 27.60, 'pt'),
 (28.1, 'thump_jab',  dict(peak_db=-12, align='onset', len=0.25), 28.10, 'pt'),
 (29.05,'teletype',   dict(rms_db=-28, start=0.0, len=2.45, fade_in=0.15, fade_out=0.3), 29.05, 'pt'),
 (29.92,'thump_jab',  dict(peak_db=-13, align='onset', len=0.25), 29.92, 'pt'),
 (30.15,'whoosh_fast',dict(peak_db=-15, len=0.45), 30.15, 'pt'),
 (32.58,'whoosh_fast',dict(peak_db=-17, len=0.5), 32.58, 'pt'),
 (34.74,'whoosh_fast',dict(peak_db=-19, len=0.5), 34.74, 'pt'),
 (36.3, 'whistle_tune',dict(peak_db=-14, start=0.0, len=1.12, fade_in=0.05, fade_out=0.02, pan=0.25), 36.30, 'pt'),
 (37.42,'whoosh_fast',dict(peak_db=-14, len=0.5), 37.50, 'pt'),
 (39.6, 'thunder_low',dict(peak_db=-14, align='onset', len=2.4, fade_out=1.0), 39.60, 'pt'),
 (41.05,'whoosh_fast',dict(peak_db=-17, len=0.4), 41.05, 'pt'),
 (41.1, 'thump_jab',  dict(peak_db=-17, align='onset', len=0.2, pan=0.3), 41.10, 'pt'),
 (41.8, 'thump_jab',  dict(peak_db=-17, align='onset', len=0.2, pan=-0.3), 41.80, 'pt'),
 (43.3, 'thump_jab',  dict(peak_db=-11, align='onset', len=0.4, pan=-0.3), 43.30, 'pt'),
 (43.7, 'thump_jab',  dict(peak_db=-11, align='onset', len=0.4, pan=0.3), 43.70, 'pt'),
 (44.5, 'map_marker', dict(rms_db=-25, len=0.68, fade_out=0.08), 44.50, 'pt'),
 (45.95,'whoosh_fast',dict(peak_db=-17, len=0.4), 45.95, 'pt'),
 (46.55,'thump_jab',  dict(peak_db=-14, align='onset', len=0.25, pan=0.3), 46.55, 'pt'),
 (46.95,'thump_jab',  dict(peak_db=-14, align='onset', len=0.25, pan=-0.3), 46.95, 'pt'),
 (48.1, 'thump_jab',  dict(peak_db=-13, align='onset', len=0.35), 48.10, 'pt'),
 (49.2, 'whoosh_whip',dict(peak_db=-14, pan=0.4), 49.20, 'pt'),
 (50.6, 'whoosh_whip',dict(peak_db=-13, pan=-0.3), 50.60, 'pt'),
 (50.87,'riser_tension',dict(peak_db=-15, len=1.58, fade_in=0.2, fade_out=0.05), 51.90, 'pt'),
 (53.72,'shimmer_reveal',dict(peak_db=-14, len=1.0, fade_out=0.3), 53.72, 'pt'),
 (55.79,'riser_tension',dict(peak_db=-16, len=1.56, fade_in=0.3, fade_out=0.03), 56.26, 'pt'),
 (57.35,'thump_jab',  dict(peak_db=-11, align='onset', len=0.35), 57.35, 'pt'),
 (57.7, 'whoosh_fast',dict(peak_db=-14, len=0.6), 57.70, 'pt'),
 (58.1, 'wave_roar',  dict(peak_db=-12, len=3.1, fade_in=0.4, fade_out=0.7), 58.40, 'pt'),
 (59.55,'whoosh_fast',dict(peak_db=-13, len=0.5, pan=0.5), 59.55, 'pt'),
 (59.8, 'pencil_scratch',dict(rms_db=-26, start=0.0, len=1.6, fade_in=0.1, fade_out=0.15), 59.80, 'pt'),
 (60.1, 'thunder_low',dict(peak_db=-16, align='onset', len=2.2, fade_out=0.9), 60.10, 'pt'),
 (61.25,'whoosh_fast',dict(peak_db=-16, len=0.45), 61.25, 'pt'),
 (62.08,'thump_jab',  dict(peak_db=-12, align='onset', len=0.4), 62.08, 'pt'),
 (62.4, 'thunder_low',dict(peak_db=-13, align='onset', len=2.5, fade_out=1.2), 62.40, 'pt'),
 (63.38,'whoosh_fast',dict(peak_db=-17, len=0.5), 63.38, 'pt'),
 (64.0, 'paper_slide',dict(rms_db=-28, len=0.7, fade_out=0.15), 64.00, 'pt'),
]
F=[f for f in F if f[4]=='amb' or any(abs(f[0]-k)<1e-6 for k in KEEP)]
assert sum(f[4]=='pt' for f in F)==len(KEEP)
for at,snd,par,ct,k in F:
    e=dict(file=S(snd),at=at); e.update(par); sfx.append(e)
    c=[c for c in cues if abs(c['t']-ct)<0.011]; assert c,(ct,snd); table.append(c[0])
from mixer import load, fades, SR, db2
def rpeak(e):
    x=load(e["file"]); mono=x.mean(1)
    if e.get("align")=="onset":
        pk=np.abs(mono).max(); on=int(np.argmax(np.abs(mono)>0.25*pk)); x=x[max(0,on-int(0.005*SR)):]
    x=x[int(e.get("start",0)*SR):]
    if e.get("len"): x=x[:int(e["len"]*SR)]
    x=x.copy(); mono=x.mean(1)
    if "peak_db" in e: x*=db2(e["peak_db"])/max(np.abs(mono).max(),1e-9)
    else: x*=db2(e.get("rms_db",-26))/max(np.sqrt((mono**2).mean()),1e-9)
    x=fades(x,e.get("fade_in",0.005),e.get("fade_out",0.03))
    p=e.get("pan",0.0); x[:,0]*=min(1.0,1-p); x[:,1]*=min(1.0,1+p)
    return 20*np.log10(np.abs(x).max())
nh=len(op['sfx'])
for (at,snd,par,ct,k),e in zip(F,sfx[nh:]):
    cap=-14 if k=='amb' else -11
    p=rpeak(e)
    if p>cap:
        key='rms_db' if 'rms_db' in e else 'peak_db'
        e[key]=round(e[key]-(p-cap)-0.05,1)
        print('capped',snd,at,key,e[key])
spec={"duration":65.5,"out_wav":OUT+'/film_mix.wav',"video_in":OUT+'/film_silent.mp4',"video_out":P+'/deliver/film_v1_thai.mp4',
 "voice":{"file":P+'/audio/th/full_v2/narration.wav',"at":0.1,"gain":vg},
 "music":{"file":P+'/audio/music/music_fit.wav',"at":0.0,"start":0.0,"rms_db":-38,"fade_out":0.4},
 "sfx":sfx}
json.dump(spec,open(OUT+'/mix_film.json','w'),indent=1,ensure_ascii=False)
json.dump([dict(cue_t=c['t'],take=c['take'],kind=c['kind'],label=c['label']) for c in table],open('table_cues.json','w'),ensure_ascii=False,indent=0)
print(len(sfx),'sfx;', sum(1 for f in F if f[4]=='pt'),'point after hook;', sum(1 for f in F if f[4]=='amb'),'amb')
