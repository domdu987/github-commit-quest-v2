import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
R='/tmp/claude-0/-home-user-github-commit-quest-v2/9c3eda1a-2051-532f-961a-8e1f745caea6/scratchpad/'
F=R+'mw/hf/rig/assets/fonts/f3.ttf'
W,H=1920,1080
bg=Image.open(R+'cov_b14.png').convert('RGB')
bg=ImageEnhance.Color(bg).enhance(1.15); bg=ImageEnhance.Contrast(bg).enhance(1.05)
# vignette darker top-left for text
v=Image.new('L',(W,H),0); d=ImageDraw.Draw(v)
d.ellipse((-700,620,1300,1500),fill=185); d.rounded_rectangle((280,610,580,800),60,fill=215); v=v.filter(ImageFilter.GaussianBlur(160))
dark=Image.new('RGB',(W,H),(22,12,40)); bg=Image.composite(dark,bg,v)
e=Image.new('L',(W,H),0); ImageDraw.Draw(e).rectangle((0,0,W,H),fill=110); ImageDraw.Draw(e).ellipse((150,80,W-150,H-40),fill=0)
bg=Image.composite(Image.new('RGB',(W,H),(10,6,20)),bg,e.filter(ImageFilter.GaussianBlur(140)))
# warm glow behind hero + paper
g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse((560,300,820,560),fill=110); g=g.filter(ImageFilter.GaussianBlur(70))
bg=Image.composite(Image.new('RGB',(W,H),(255,215,120)),bg,g)
img=bg.convert('RGBA')
def text_layer(txt,size,x,y,fill,stroke=16,grad=None):
    f=ImageFont.truetype(F,size,layout_engine=ImageFont.Layout.RAQM)
    L=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(L)
    # glow
    gl=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(gl).text((x,y),txt,font=f,fill=(255,200,80,200) if grad else (255,255,255,150),stroke_width=stroke+14,stroke_fill=(255,200,80,200) if grad else (255,255,255,120))
    gl=gl.filter(ImageFilter.GaussianBlur(22))
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((x+10,y+14),txt,font=f,fill=(0,0,0,200),stroke_width=stroke,stroke_fill=(0,0,0,200)); sh=sh.filter(ImageFilter.GaussianBlur(6))
    dd.text((x,y),txt,font=f,fill=(20,10,30,255),stroke_width=stroke,stroke_fill=(20,10,30,255))
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).text((x,y),txt,font=f,fill=255)
    if grad:
        bb=m.getbbox(); col=Image.new('RGBA',(W,H))
        cd=ImageDraw.Draw(col)
        for yy in range(bb[1],bb[3]+1):
            t=(yy-bb[1])/max(1,bb[3]-bb[1]); c=tuple(int(grad[0][i]*(1-t)+grad[1][i]*t) for i in range(3))
            cd.line((0,yy,W,yy),fill=c+(255,))
        L=Image.composite(col,L,m)
        # gloss highlight top
        hl=Image.new('L',(W,H),0); ImageDraw.Draw(hl).rectangle((0,bb[1],W,bb[1]+(bb[3]-bb[1])*0.38),fill=70); hl=ImageChops.multiply(hl,m)
        L=Image.composite(Image.new('RGBA',(W,H),(255,255,255,255)),L,hl)
    else:
        L=Image.composite(Image.new('RGBA',(W,H),fill),L,m)
    return gl,sh,L,m.getbbox()
out=img
l1=text_layer('ขายประกัน',122,48,640,(255,255,255,255))
l2=text_layer('ให้มังกร!?',200,40,795,None,stroke=20,grad=((255,236,90),(255,160,20)))
for gl,sh,L,bb in (l1,l2):
    out=Image.alpha_composite(out,gl); out=Image.alpha_composite(out,sh)
# swooshes
sw=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sw)
b1=l1[3]; b2=l2[3]
sd.line([(b1[0]+40,b1[3]+26),(b1[2]-60,b1[3]+14)],fill=(230,40,40,255),width=12)
sd.line([(b2[0]+30,b2[3]+30),(b2[2]+20,b2[3]+12)],fill=(255,210,40,255),width=14)
out=Image.alpha_composite(out,sw.filter(ImageFilter.GaussianBlur(1.2)))
for gl,sh,L,bb in (l1,l2): out=Image.alpha_composite(out,L)
# sparkle ticks
sp=Image.new('RGBA',(W,H),(0,0,0,0)); pd=ImageDraw.Draw(sp)
import math
cx,cy=b2[2]+30,b2[1]+40
for a in (-70,-35,0):
    r=math.radians(a); pd.line([(cx+30*math.cos(r),cy+30*math.sin(r)),(cx+80*math.cos(r),cy+80*math.sin(r))],fill=(255,220,60,255),width=12)
cx,cy=790,380
for a in (-150,-110,-70):
    r=math.radians(a); pd.line([(cx+30*math.cos(r),cy+30*math.sin(r)),(cx+70*math.cos(r),cy+70*math.sin(r))],fill=(255,240,140,255),width=9)
out=Image.alpha_composite(out,sp)
print(b1,b2)
out.convert('RGB').save(sys.argv[1],quality=93)
