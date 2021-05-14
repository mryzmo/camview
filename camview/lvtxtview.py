import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyleFactory, \
    QGridLayout, QListWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidgetItem, QStatusBar, QProgressBar
#from PyQt5 import QStyleFactory
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg \
    import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random
import numpy as np
import pyqtgraph as pg
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import pyqtgraph.console
import matplotlib.image as mpimg
from os import listdir
from os.path import isfile, join
from camview.readimg import sbf, plifimg, sif
from camview.readlvfile import readlvfile
from camview.ImageViewPfaff import ImageViewPfaff
import pickle

class LVView(pg.GraphicsWindow):

    plots=[] #list of all plots
    sliders=[]
    def __init__(self,path='./testdata/2021-03-17/2021-03-17_real27.txt'):
        super().__init__()
        self.makeLVWindow(path)
        
    def LVtimeLineChanged(self, ev):
        for s in self.sliders:
            if s == ev:
                continue
            else:
                s.setPos(ev.getPos())

    def makeLVWindow(self,lvpath):
        #load LV data
        timeline,unitline,times,temps,currents,pressures,flows,msdata=readlvfile(lvpath)
        
        sepunits=unitline.split()

        #define window stuff
        pens=['r','b','g','y','c']
        self.resize(1000,600)
        self.setWindowTitle(lvpath)

        #first plot
        p1 = self.addPlot(title="Heating")
        p1.addLegend()
        p1.plot(times,temps,pen=(0,255,0),name='Temperature [°C]')
        p1.plot(times,currents*1000,pen=(255,0,0),name='Current [mA]')
        p1.setLabel('bottom',text='time',units='s')
        self.plots.append(p1)

        #second plot
        self.nextRow()
        p2 = self.addPlot(title="Flows")
        for i in range(0,5):
            p2.plot(times,flows[:,i],pen=pens[i],name=sepunits[i+11].split('[')[0])
        p2.setXLink(p1)
        p2.addLegend()
        self.plots.append(p2)

        #third plot
        self.nextRow()
        p3 = self.addPlot(title="MS")
        for i in range(0,5):
            p3.plot(times,np.log10(msdata[:,i]),pen=pens[i])
        p3.setXLink(p1)
        self.plots.append(p3)

        for plot in self.plots:
            timelineSlider=pg.InfiniteLine(0, movable=True)
            plot.addItem(timelineSlider)
            timelineSlider.sigPositionChanged.connect(self.LVtimeLineChanged)
            self.sliders.append(timelineSlider)
        self.trendScroll=self.sliders[0]
    def getWindow(self):
        return self.lvwin


class LVViewApp:
    def __init__(self):
        import os
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        app = QApplication(sys.argv)
        if len(sys.argv) > 1:
            win = LVView(sys.argv[1])
        else:
            win = LVView()
        app.setApplicationName('LU PLIF Viewer')
        #app.setWindowIcon(QIcon('PLIF-icon-256.png'))
        # sys.exit(app.exec_())
        app.exec_()

if __name__ == '__main__':
    app=LVViewApp()