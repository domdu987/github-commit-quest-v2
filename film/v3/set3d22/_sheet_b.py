import os, glob, sys
from PIL import Image, ImageDraw, ImageFont
import stats as ST
C='contact'; fs=sorted(glob.glob(C+'/B_*.png'), key=lambda p:(p.split('_')[1], {'start':0,'mid':1,'end':2}[p.split('_')[2][:-4]]))
W,H=720,1280; cols=6; rows=(len(fs)+cols-1)//cols; LAB=70
sheet=Image.new('RGB',(W*cols//2,(H+LAB)*rows//2),'#10102a'); ph=Image.new('RGB',(360*cols,640*rows),'#10102a')
ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16); fn=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
txt=[]
for i,p in enumerate(fs):
    im=Image.open(p).convert('RGB'); st=ST.stats(p); nm=os.path.basename(p)[2:-4].replace('_',' ')
    c=im.copy(); ImageDraw.Draw(c).line((0,880,W,880),fill=(0,255,255),width=3)
    t=c.resize((W//2,H//2)); x=(i%cols)*W//2; y=(i//cols)*(H+LAB)//2
    sheet.paste(t,(x,y)); d=ImageDraw.Draw(sheet); d.text((x+4,y+H//2+2),nm,font=ft,fill='white')
    d.text((x+4,y+H//2+22),'sat %.2f luma %.0f vivid %.0f%% hue %.0f'%(st['sat'],st['luma'],st['vivid'],st['shade_hue']),font=fn,fill=(170,200,255))
    pt=im.resize((360,640)); ph.paste(pt,((i%cols)*360,(i//cols)*640)); ImageDraw.Draw(ph).text(((i%cols)*360+4,(i//cols)*640+4),nm,font=ft,fill='white')
    txt.append('%s sat %.3f luma %.1f vivid %.1f shade_hue %.1f'%(nm,st['sat'],st['luma'],st['vivid'],st['shade_hue']))
sheet.save('contact_sheet_B.jpg',quality=88); ph.save('contact_phone_B.jpg',quality=88); open('hue_rows_B.txt','w').write('\n'.join(txt)+'\n'); print('\n'.join(txt))
