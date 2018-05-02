from readimg import sif
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#file=sif('/home/sebastian/ch3/2018-02-28/calib1.sif')
#file=sif('/home/sebastian/Documents/Data/paper1/20171030_refl_16.sif')
file=sif('/media/sebastian/Katalys 2TB/desy17/2017-10-30/20171030_refl_24.sif')

print(file.numimgframes())
print(file.getimgdata())
print(file.findoffsetbyte())
#print(file.readimg(0,200))

imagedata=np.swapaxes(file.readimg(1,200),0,2)


#pg.image(imagedata, title="LU SXRD Viewer")

fig=plt.figure()
ims = []

plt.subplot(221)
for i in range(imagedata.shape[0]):
    plt.subplot(221)
    im= plt.imshow(imagedata[i,:,:], animated=True)
    plt.subplot(223)
    ims.append([im])
    #plt.imshow(imagedata[i,:,:])
    #plt.pause(.1)
    #
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=1000)
plt.show()