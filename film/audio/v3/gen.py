import sys,os,json,subprocess
def tts(text,voice,out,speed=1.15,stab=None):
    body={"text":text,"voice":voice,"language_code":"th","timestamps":True,"speed":speed}
    if stab is not None: body["stability"]=stab
    r=subprocess.run(["curl","-sS","-m","300","-X","POST","https://fal.run/fal-ai/elevenlabs/tts/eleven-v3","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps(body,ensure_ascii=False),"-w","\n%{http_code}"],capture_output=True,text=True)
    t,c=r.stdout.rsplit("\n",1)
    if c!="200": print(out,c,t[:300]); return None
    d=json.loads(t); json.dump(d,open(out+".json","w"),ensure_ascii=False)
    subprocess.run(["curl","-sS","-o",out+".mp3",d["audio"]["url"]]); return d
if __name__=="__main__":
    tts(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]) if len(sys.argv)>4 else 1.15)
