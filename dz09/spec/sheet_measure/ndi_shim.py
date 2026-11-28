import numpy as np, cv2
def label(m):
    n, lab = cv2.connectedComponents(m.astype(np.uint8), connectivity=8); return lab, n-1
def sum(m, lab, idx): return [int((lab==i).sum()) for i in idx]
def binary_closing(m, iterations=1):
    k=np.ones((3,3),np.uint8); return cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, k, iterations=iterations)>0
def binary_fill_holes(m):
    m=m.astype(np.uint8); h,w=m.shape; ff=np.zeros((h+2,w+2),np.uint8); inv=(1-m).copy()
    pad=np.pad(inv,1,constant_values=1); cv2.floodFill(pad, None, (0,0), 2)
    return (pad[1:-1,1:-1]!=2)
def find_objects(lab):
    out=[]
    for i in range(1, lab.max()+1):
        ys,xs=np.nonzero(lab==i)
        out.append((slice(ys.min(),ys.max()+1), slice(xs.min(),xs.max()+1)) if len(ys) else None)
    return out
