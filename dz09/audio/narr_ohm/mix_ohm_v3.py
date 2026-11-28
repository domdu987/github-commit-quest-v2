import numpy as np, subprocess, json
SR=48000; OFF=0.30; DUR=53.32
def load(f,ch=2):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ar','48000','-ac',str(ch),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,ch).astype(float)
N=int(SR*DUR); voice=np.zeros((N,2)); amb=np.zeros((N,2)); fx=np.zeros((N,2)); mus=np.zeros((N,2))
v=load('narr_final.wav'); i=int(OFF*SR); voice[i:i+len(v)]=v[:N-i]
# radio colour on the cold-open sentence only (0.3 to 3.6 s)
a,b=int(OFF*SR),int(3.55*SR)
seg=voice[a:b].copy(); open('_r.raw','wb').write(seg.astype(np.float32).tobytes())
r=subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar','48000','-ac','2','-i','_r.raw','-af','highpass=f=450,lowpass=f=2800,volume=3,alimiter=limit=0.5,volume=1.7','-f','f32le','-'],capture_output=True).stdout
voice[a:b]=np.frombuffer(r,dtype=np.float32).reshape(-1,2)[:b-a]
S='../ep1_hook/sfx/'
def put(buf,f,t,g,loop_to=None):
    x=load(S+f)*g; i=int(t*SR); end=int(loop_to*SR) if loop_to else N
    while i<end:
        n=min(len(x),end-i); buf[i:i+n]+=x[:n]
        if not loop_to: break
        i+=n
put(fx,'radio_static_cut.wav',0.0,0.5); put(fx,'radio_static_cut.wav',3.24,0.9)
put(amb,'rain_heavy_road.wav',5.49,1.0,50.72); put(amb,'sirens_city_far.wav',6.14,0.35,50.72)
put(fx,'hydraulic_cutter.wav',15.05,0.7); put(fx,'car_alarm_far.wav',11.10,0.15)
put(fx,'phone_vibrate.wav',17.65,0.4); put(fx,'rain_on_hood.wav',30.35,0.8)
put(fx,'car_door_pry.wav',34.51,0.75); put(fx,'heartbeat_low.wav',38.68,0.8); put(fx,'heartbeat_low.wav',40.68,0.9)
put(fx,'zombie_lunge.wav',43.45,1.0); put(fx,'man_scream_bite.wav',43.80,0.75); put(fx,'hit_trailer.wav',50.72,0.5)
# ---- v3: the user's Suno tracks replace the synthesised bed
M='../suno/'
def seg(f,t_film,t_src,dur,fin=0.05,fout=0.05,g=1.0):
    x=load(M+f); a=int(t_src*SR); n=min(int(dur*SR),len(x)-a,N-int(t_film*SR)); y=x[a:a+n].copy()*g
    k=int(fin*SR); y[:k]*=np.linspace(0,1,k)[:,None]; k=int(fout*SR); y[-k:]*=np.linspace(1,0,k)[:,None]
    i=int(t_film*SR); mus[i:i+n]+=y
# 1 tension bed: its hits (every 8 s from 2.0) land on the radio cut 3.243, "ก้อง" 11.24, "4 สาย" 19.24
seg('Rain_on_the_Concrete.mp3',1.243,0.0,20.6,fin=0.3,fout=2.2)
# 3 father and daughter: under the call, out as she hangs up
seg('Unsent_Letter.mp3',20.4,30.0,13.0,fin=2.0,fout=1.6,g=1.25)
# 1 again from the junior's shout: hit on 35.445 and on the lunge 43.445, decays under the cliffhanger line
seg('Rain_on_the_Concrete.mp3',33.0,31.555,17.4,fin=0.8,fout=1.6)
# 4 title: its riser (0-3.8 s) climbs under "จะไม่ใช่คนอีกต่อไป", its hit lands on the title 50.72
ti=int(46.92*SR); mus_t=np.zeros((N,2)); x=load(M+'The_Shadows_Pulse.mp3'); n=N-ti; y=x[:n].copy(); k=int(0.35*SR); y[-k:]*=np.linspace(1,0,k)[:,None]; mus_t[ti:ti+n]=y
rms=lambda x:np.sqrt((x**2).mean())
amb*=10**(-36/20)/rms(amb[int(8*SR):int(40*SR)])          # loud rain, as asked
gm=10**(-27.5/20)/rms(mus[int(8*SR):int(40*SR)]); mus*=gm; mus_t*=gm*10**(8/20)
# duck ambience and music 5 dB under the voice (sidechain from the voice envelope)
env=np.convolve(np.abs(voice.mean(1)),np.ones(int(0.12*SR))/int(0.12*SR),'same')
duck=10**(-9/20*np.clip(env/0.02,0,1)); fxduck=10**(-10/20*np.clip(env/0.02,0,1))
# scare drop: everything but heartbeat falls away 37.9-39.35 s, then slams back on the lunge
t=np.arange(N)/SR; drop=np.ones(N); m1=(t>=40.08)&(t<43.45); drop[m1]=np.interp(t[m1],[40.08,43.30,43.45],[1,10**(-20/20),10**(-20/20)])
voice*=10**(4/20); fx*=10**(-7/20)
tduck=10**(-6/20*np.clip(env/0.02,0,1))
bed=amb*(duck*drop)[:,None]+mus*(duck*drop)[:,None]+mus_t*tduck[:,None]+fx*fxduck[:,None]
sp=env>0.02; print('VOICE over BED while speaking: %.1f dB'%(20*np.log10(rms(voice[sp])/rms(bed[sp]))))
for a in range(0,52,4):
    m=sp.copy(); m[:a*SR]=False; m[(a+4)*SR:]=False
    if m.sum()>SR//2: print(a,'%.1f'%(20*np.log10(rms(voice[m])/(rms(bed[m])+1e-9))),end=' | ')
print()
mix=voice+bed
k=int(0.004*SR); from numpy.lib.stride_tricks import sliding_window_view as sw
g=np.minimum(1,10**(-1/20)/np.maximum(np.abs(mix).max(1),1e-9)); g=sw(np.pad(g,(k,k),mode='edge'),2*k+1).min(1); mix*=g[:,None]
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s16le','mix_ohm_v3.wav'],input=mix.astype(np.float32).tobytes())
mono=mix.mean(1)
for a in range(0,int(DUR),4):
    s=mono[a*SR:(a+4)*SR]; print(f"{a:2d}-{a+4:2d}s {20*np.log10(rms(s)+1e-9):6.1f} dB")
