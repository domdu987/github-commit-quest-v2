python3 - "$@" <<'P'
import sys
from PIL import Image
gs=[int(x) for x in sys.argv[1:]] if len(sys.argv)>1 else [395,444,469]
ims=[Image.open('work/st/g_%04d.png'%g) for g in gs]
w,h=ims[0].size
S=Image.new('RGB',(w*len(ims),h))
for i,im in enumerate(ims):S.paste(im,(i*w,0))
S.save('work/st/sheet.png')
P
