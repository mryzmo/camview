import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.widgets.PlotWidget import *
from pyqtgraph.imageview import *
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from pyqtgraph.widgets.GraphicsView import GraphicsView
QAPP = None

class ImageViewPfaff(pg.ImageView):
    def normalize(self, image):
            """
            Process *image* using the normalization options configured in the
            control panel.
            
            This can be repurposed to process any data through the same filter.
            """
            if self.ui.normOffRadio.isChecked():
                return image
                
            div = self.ui.normDivideRadio.isChecked()
            norm = image.view(np.ndarray).copy()
            #if div:
                #norm = ones(image.shape)
            #else:
                #norm = zeros(image.shape)
            if div:
                norm = norm.astype(np.float32)
                
            if self.ui.normTimeRangeCheck.isChecked() and image.ndim == 3:
                (sind, start) = self.timeIndex(self.normRgn.lines[0])
                (eind, end) = self.timeIndex(self.normRgn.lines[1])
                #print start, end, sind, eind
                #n = image[sind:eind+1].mean(axis=0)
                print('averaging time range...')
                if eind<sind: #swap order if it is wrong
                    sind,eind=eind,sind
                n = np.nanmean(image[sind:eind+1],axis=0)
                n.shape = (1,) + n.shape
                if div:
                    print('performing division...')
                    norm /= n
                else:
                    norm=norm.astype(np.float64)
                    norm -= n
                    
            if self.ui.normFrameCheck.isChecked() and image.ndim == 3:
                n = image.mean(axis=1).mean(axis=1)
                n.shape = n.shape + (1, 1)
                if div:
                    norm /= n
                else:
                    norm -= n
                
            if self.ui.normROICheck.isChecked() and image.ndim == 3:
                n = self.normRoi.getArrayRegion(norm, self.imageItem, (1, 2)).mean(axis=1).mean(axis=1)
                n = n[:,np.newaxis,np.newaxis]
                #print start, end, sind, eind
                if div:
                    norm /= n
                else:
                    norm -= n
                    
            return norm

def mkQApp():
    if QtGui.QApplication.instance() is None:
        global QAPP
        QAPP = QtGui.QApplication([])

class ImageWindow(ImageViewPfaff):
    def __init__(self, *args, **kargs):
        mkQApp()
        self.win = QtGui.QMainWindow()
        self.win.resize(800,600)
        if 'title' in kargs:
            self.win.setWindowTitle(kargs['title'])
            del kargs['title']
        ImageView.__init__(self, self.win)
        if len(args) > 0 or len(kargs) > 0:
            self.setImage(*args, **kargs)
        self.win.setCentralWidget(self)
        for m in ['resize']:
            setattr(self, m, getattr(self.win, m))
        #for m in ['setImage', 'autoRange', 'addItem', 'removeItem', 'blackLevel', 'whiteLevel', 'imageItem']:
            #setattr(self, m, getattr(self.cw, m))
        self.win.show()
images = []
def image(*args, **kargs):
    """
    Create and return an :class:`ImageWindow <pyqtgraph.ImageWindow>` 
    (this is just a window with :class:`ImageView <pyqtgraph.ImageView>` widget inside), show image data inside.
    Will show 2D or 3D image data.
    Accepts a *title* argument to set the title of the window.
    All other arguments are used to show data. (see :func:`ImageView.setImage() <pyqtgraph.ImageView.setImage>`)
    """
    mkQApp()
    w = ImageWindow(*args, **kargs)
    images.append(w)
    w.show()
    return w