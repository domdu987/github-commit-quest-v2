import cv2,numpy as np,glob,sys
fs=sorted(glob.glob((sys.argv[1] if len(sys.argv)>1 else 'frames')+'/g_*.png')); n=len(fs); sel=[fs[int(i*(n-1)/9)] for i in range(10)]
ims=[cv2.resize(cv2.imread(f),(216,384)) for f in sel]
cv2.imwrite('contact.jpg',np.vstack([np.hstack(ims[:5]),np.hstack(ims[5:])]),[cv2.IMWRITE_JPEG_QUALITY,80])
cv2.imwrite('phone_sheet.jpg',np.hstack(ims[::2]),[cv2.IMWRITE_JPEG_QUALITY,80])
