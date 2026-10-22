import json,sys,subprocess,time,urllib.request
STY=__import__('os').environ.get('STY','เล่าเรื่องแบบนักเล่าเรื่องลึกลับ น้ำเสียงต่ำ นุ่ม ฟังเพลิน ค่อยๆ บิ้วอารมณ์ให้ลุ้น เว้นจังหวะก่อนคำสำคัญ ไม่เร่งรีบ')
name,text=sys.argv[1],sys.argv[2]
body=json.dumps({"prompt":text,"style_instructions":STY,"voice":__import__("os").environ.get("VOICE","Charon"),"language_code":"Thai (Thailand)","temperature":0.8}).encode()
for attempt in range(3):
    req=urllib.request.Request("https://fal.run/fal-ai/gemini-3.1-flash-tts",data=body,headers={"Content-Type":"application/json"})
    try:
        r=json.load(urllib.request.urlopen(req,timeout=150))
        urllib.request.urlretrieve(r["audio"]["url"],name+".mp3"); break
    except Exception as e:
        print(name,"retry",attempt,e,file=sys.stderr); time.sleep(8)
else: sys.exit(1)
d=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",name+".mp3"]).decode().strip()
print(name,d)
