import numpy as np, cv2, json
from PIL import Image
SRC='/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/uploads/character_sheet.webp'
a=np.asarray(Image.open(SRC).convert('RGB')).astype(np.int16)
bg=np.array([253,243,232])
d=np.abs(a-bg).max(2)
fg=(d>28).astype(np.uint8)
fg[:120]=0; fg[690:]=0
n,lab,st,cen=cv2.connectedComponentsWithStats(fg,8)
for i in np.argsort(-st[:,4])[:15]:
    if i==0: continue
    print(i, st[i])
np.save('lab.npy',lab)
