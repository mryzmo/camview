from readimg import sif,plifimg
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
#file=sif('/home/sebastian/ch3/2018-02-28/calib1.sif')
#file=sif('/home/sebastian/Documents/Data/paper1/20171030_refl_16.sif')
#file=sif('/media/sebastian/Katalys 8TB/data/raw/desy17/2017-10-30/20171030_refl_24.sif')
file=sif('/media/sebastian/Katalys 8TB/data/raw/desy17/2017-10-30/20171030_refl_14.sif')
print(file.numimgframes())
print(file.getimgdata())
print(file.findoffsetbyte())
#print(file.readimg(0,200))

#fileB=sif('/media/sebastian/Katalys 2TB/desy17/2017-10-30/20171030_refl_14.sif')

#imagedata=np.swapaxes(file.readimg(),0,2)
imagedata=np.swapaxes(plifimg.readimgav(file,1,30000,50),0,2)
#imagedataB=np.roll(np.swapaxes(plifimg.readimgav(fileB,1,500,1),0,2),-2,1)
#plt.imshow(imagedata[0,:,:])

pg.image(imagedata, title="LU SOR Viewer")
#pg.image(np.append(imagedata,imagedataB,0), title="LU SXRD Viewer")

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()

#plt.imshow(imagedata[0,:,:])
#plt.show()
