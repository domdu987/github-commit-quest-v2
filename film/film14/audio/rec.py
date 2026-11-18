# record per-sentence Bankky takes: python3 audio/rec.py [ids]   (run from film14/)
import sys,os,json,subprocess,concurrent.futures as cf
sys.path.insert(0,'../audio/v3'); from gen import tts
VOICE="RwilAvCC3o05RLuACpAn"
T=json.load(open('script/tts_bankky_orig.json'))
ids=[int(a) for a in sys.argv[1:]] or range(len(T))
def go(i):
    o=f'audio/bk0/s{i:02d}'; d=tts(T[i],VOICE,o,1.15)
    subprocess.run(["ffmpeg","-v","error","-y","-i",o+".mp3","-ar","48000","-ac","1",o+".wav"]); return i,bool(d)
with cf.ThreadPoolExecutor(5) as ex:
    for r in ex.map(go,ids): print(r,flush=True)
