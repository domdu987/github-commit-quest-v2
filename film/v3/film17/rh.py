import sys,subprocess,numpy as np
d0=sys.argv[1]; first=int(sys.argv[2]); out=sys.argv[3]
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-start_number",str(first),"-i",d0+"/g_%04d.png","-c:v","libx264","-crf","12",out])
raw=subprocess.run(["ffmpeg","-v","error","-i",out,"-vf","scale=90:160","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
v=np.frombuffer(raw,np.uint8).reshape(-1,160,90).astype(float); d=np.abs(np.diff(v,axis=0)).mean((1,2))
print(' '.join('%d:%.0f'%(i+first+1,x) for i,x in enumerate(d)))
