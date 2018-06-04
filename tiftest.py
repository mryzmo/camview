from readimg import sif,plifimg,mptif16
import pyqtgraph as pg
import ImageViewPfaff
import numpy as np
import os.path
import matplotlib.pyplot as plt
#file=sif('/home/sebastian/ch3/2018-02-28/calib1.sif')
#file=sif('/home/sebastian/Documents/Data/paper1/20171030_refl_16.sif')
#file=mptif16('C:/Users/Catalysis/Pictures/oxtest1.tif')
#file=mptif16('C:/Users/Catalysis/Desktop/Data/SOR/2018-05-24/sor_4.tif')
#file=mptif16('E:\Raw_data/2018 LED AAO\Data 180530\Sample4/ox8.tif')
file=mptif16('E:\sorjonas/ox6.tif')

print(file.numimgframes())
print(file.getimgdata())
print(file.getnumfiles())
#print(file.readimg(0,200))
print(file.numimgframesperfile())
print(file.whichfile(1500))

#imagedata=np.swapaxes(file.readimg(0,-1),0,2) #read all
#imagedata=np.swapaxes(file.readimg(1400,1499),0,2)
imagedata=np.swapaxes(plifimg.readimgav(file,0,100,10),0,2)
# imagedataB=np.roll(np.swapaxes(plifimg.readimgav(fileB,1,500,1),0,2),-2,1)
# plt.imshow(imagedata[0,:,:])
# plt.show()
pg.image
ImageViewPfaff.image(imagedata, title="LU SOR Viewer")

# #pg.image(np.append(imagedata,imagedataB,0), title="LU SXRD Viewer")

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        try:
            pg.QtGui.QApplication.exec_()
        except Exception:
            sys.exc_clear()
        

#plt.imshow(imagedata[0,:,:])
#plt.show()
