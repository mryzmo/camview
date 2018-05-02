import numpy as np
import pickle
import os,sys
import scipy.misc
import pyqtgraph as pg

timestep=float(input('XRD Δt: '))

pg.setConfigOptions(imageAxisOrder='row-major')

if os.path.isfile('thisfolder.npy'):
    loaded=True
    final=np.load('thisfolder.npy')
else:
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        final=np.zeros([len(dirs),2048,2048])
        foldernum=0
        for name in sorted(dirs):
            print(os.path.join(root, name))
            numfiles=0
            tiffolder=(os.listdir(os.path.join(root, name)))
            for filename in tiffolder: #count tiff files
                if filename.endswith('.tif') and not filename.endswith('dark.tif'):
                    numfiles=numfiles+1
            temp=np.zeros([numfiles,2048,2048])
            img=0
            for filename in tiffolder:
                if filename.endswith('.tif') and not filename.endswith('dark.tif'):
                    #print(str(filename))
                    temp[img,:,:]=np.rot90(scipy.misc.imread(os.path.join(root, name)+'/'+filename,mode='I'),k=3,axes=(0,1))
                    img=img+1
            final[foldernum,:,:]=np.max(temp,0)
            foldernum=foldernum+1
            #if foldernum>2:
            #    break
    np.save('thisfolder.npy', final)

pg.image(final, title="LU SXRD Viewer",xvals=np.linspace(0,timestep*final.shape[0],final.shape[0]))


if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
