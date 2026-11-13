import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
R='/tmp/claude-0/-home-user-github-commit-quest-v2/9c3eda1a-2051-532f-961a-8e1f745caea6/scratchpad/'
FD=R+'mw/hf/rig/assets/fonts/'
def F(n,s): return ImageFont.truetype(FD+n,s,layout_engine=ImageFont.Layout.RAQM)
W,H=1920,1080; FPS=60; DUR=5.4
last=Image.open(R+'ep1yt/long_last.png').convert('RGB')
blur=ImageEnhance.Brightness(last.filter(ImageFilter.GaussianBlur(26))).enhance(0.72)
tint=Image.new('RGB',(W,H),(60,25,20)); blur=Image.blend(blur,tint,0.18)
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def back(x):
    x=max(0,min(1,x)); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def textimg(txt,font,fill,stroke=0,sf=(0,0,0)):
    b=font.getbbox(txt,stroke_width=stroke); w,h=b[2]-b[0]+40,b[3]-b[1]+40
    im=Image.new('RGBA',(w,h)); ImageDraw.Draw(im).text((20-b[0],20-b[1]),txt,font=font,fill=fill,stroke_width=stroke,stroke_fill=sf); return im
def shadowed(im,off=8,r=10,a=150):
    sh=Image.new('RGBA',im.size); sh.putalpha(im.getchannel('A').point(lambda v:v*a//255)); sh=sh.filter(ImageFilter.GaussianBlur(r))
    out=Image.new('RGBA',(im.width+off*2,im.height+off*2)); out.alpha_composite(sh,(off*2,off*2)); out.alpha_composite(im,(off,off)); return out
def pill(txt,font,bg,fg,padx=34,pady=14,dot=None):
    t=textimg(txt,font,fg); w=t.width+padx*2+(30 if dot else 0); h=t.height+pady*2-20
    im=Image.new('RGBA',(w,h)); d=ImageDraw.Draw(im); d.rounded_rectangle((0,0,w-1,h-1),h//2,fill=bg)
    x=padx-20
    if dot: d.ellipse((padx-4,h//2-9,padx+14,h//2+9),fill=dot); x+=30
    im.alpha_composite(t,(x,(h-t.height)//2)); return shadowed(im,6,8,120)
P1=pill('ดูต่อได้ที่',F('f2.ttf',46),(205,45,45,255),(255,255,255,255),dot=(255,255,255,255))
T1=shadowed(textimg('ดูเรื่องเต็ม',F('f2.ttf',190),(255,255,255,255)),10,14,170)
T2=shadowed(textimg('ทาง YouTube',F('f2.ttf',130),(255,206,60,255)),9,12,170)
P2=pill('ติดตามต่อได้ใน YouTube',F('f2.ttf',44),(255,255,255,240),(30,20,20,255))
# play badge + channel
def badge():
    im=Image.new('RGBA',(560,130)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,15,140,115),30,fill=(230,30,30,255)); d.polygon([(52,40),(52,90),(98,65)],fill=(255,255,255,255))
    im.alpha_composite(textimg('Rod Mai Club',F('f3.ttf',58),(255,255,255,255)),(150,-6))
    im.alpha_composite(textimg('เรื่องเต็มทุกตอน',F('f1.ttf',36),(240,230,220,255)),(152,58))
    return shadowed(im,6,8,140)
B=badge()
LBL=textimg('สกิลจอมโกหก · EP.1',F('f2.ttf',26),(255,255,255,200))
LBLbg=Image.new('RGBA',(LBL.width,LBL.height-10)); ImageDraw.Draw(LBLbg).rounded_rectangle((0,0,LBL.width-1,LBL.height-11),14,fill=(0,0,0,110)); LBLbg.alpha_composite(LBL,(0,-5))
# logo card
def logo():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): c=int(18+14*(1-abs(y-H/2)/(H/2))); d.line((0,y,W,y),fill=(c,c+2,c+6))
    cx,cy=W//2,400; d.ellipse((cx-95,cy-95,cx+95,cy+95),outline=(240,190,50),width=9)
    q=textimg('?',F('f3.ttf',130),(240,190,50)); im.paste(q,(cx-q.width//2,cy-q.height//2-10),q)
    t=textimg('Rod Mai Club',F('f3.ttf',110),(255,255,255)); im.paste(t,(cx-t.width//2,540),t)
    s=textimg('ถ้าวันหนึ่ง… คุณจะรอดไหม?',F('f1.ttf',46),(220,215,205)); im.paste(s,(cx-s.width//2,690),s)
    return im
LOGO=logo()
def put(fr,im,cx,cy,alpha=1,scale=1,wipe=1):
    if alpha<=0 or wipe<=0: return
    if scale!=1: im=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.LANCZOS)
    if wipe<1:
        m=Image.new('L',im.size,0); ImageDraw.Draw(m).rectangle((0,0,int(im.width*wipe),im.height),fill=255)
        a=im.getchannel('A'); from PIL import ImageChops; im=im.copy(); im.putalpha(ImageChops.multiply(a,m))
    if alpha<1: im=im.copy(); im.putalpha(im.getchannel('A').point(lambda v:int(v*alpha)))
    fr.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2)))
N=int(round(DUR*FPS))
for i in range(N):
    t=i/FPS
    if t>=4.55:
        fr=LOGO.copy()
        if t<4.85: fr=Image.blend(Image.open(R+'ep1yt/fr/%04d.png'%(int(4.54*FPS))).convert('RGB'),LOGO,ease((t-4.55)/0.3))
        fr.save(R+'ep1yt/fr/%04d.png'%i); continue
    k=ease(t/0.45); bg=Image.blend(last,blur,k)
    z=1+0.03*t/4.5; bg=bg.resize((int(W*z),int(H*z)),Image.BILINEAR); ox,oy=(bg.width-W)//2,(bg.height-H)//2; bg=bg.crop((ox,oy,ox+W,oy+H))
    fr=bg.convert('RGBA')
    put(fr,P1,W/2,250,alpha=ease((t-0.3)/0.2),scale=back((t-0.3)/0.35))
    put(fr,T1,W/2,420,wipe=ease((t-0.55)/0.4))
    put(fr,T2,W/2,590,wipe=ease((t-0.95)/0.4))
    u=ease((t-1.25)/0.35)
    if u>0:
        d=ImageDraw.Draw(fr); x0=W/2-300; d.line((x0,672,x0+600*u,664),fill=(220,40,40,255),width=10)
    put(fr,P2,W/2,770,alpha=ease((t-1.5)/0.3),scale=0.9+0.1*ease((t-1.5)/0.3))
    put(fr,B,W/2,900,alpha=ease((t-1.8)/0.3),scale=back((t-1.8)/0.4))
    fr.alpha_composite(LBLbg,(24,H-LBLbg.height-22))
    fr.convert('RGB').save(R+'ep1yt/fr/%04d.png'%i)
print(N)
