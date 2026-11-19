# generate per-sentence Bankky takes: python3 audio/gen_bk0.py [ids...]  (run from film13/)
import sys,json,subprocess,concurrent.futures as cf
sys.path.insert(0,'../audio/v3'); from gen import tts
T=json.load(open('script/tts_bankky_orig.json'))
ids=[int(a) for a in sys.argv[1:]] or range(len(T))
def go(i):
    d=tts(T[i],"RwilAvCC3o05RLuACpAn",f"audio/bk0/s{i:02d}",1.15)
    if d: subprocess.run(["ffmpeg","-v","error","-y","-i",f"audio/bk0/s{i:02d}.mp3","-ac","1","-ar","48000",f"audio/bk0/s{i:02d}.wav"])
    return i,bool(d)
import os; os.makedirs('audio/bk0',exist_ok=True)
with cf.ThreadPoolExecutor(6) as ex: print(list(ex.map(go,ids)))
