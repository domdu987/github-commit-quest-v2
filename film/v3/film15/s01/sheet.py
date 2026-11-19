import sys,os,subprocess,concurrent.futures as cf
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__))
frames=[int(x) for x in sys.argv[1].split(',')]; tag=sys.argv[2] if len(sys.argv)>2 else 'sh'
def one(g):
    subprocess.run(['python3',os.path.join(HERE,'shot.py'),'still',str(g)],cwd=HERE,capture_output=True)
with cf.ThreadPoolExecutor(2) as ex: list(ex.map(one,frames))
ims=[Image.open(os.path.join(HERE,'work','still_%03d.png'%g)) for g in frames]
S=Image.new('RGB',(360*len(ims),640));d=ImageDraw.Draw(S)
for i,(g,im) in enumerate(zip(frames,ims)): S.paste(im,(i*360,0)); d.text((i*360+6,6),str(g),fill=(255,255,255))
S.save(os.path.join(HERE,'work',tag+'.jpg'),quality=88); print(S.size)
