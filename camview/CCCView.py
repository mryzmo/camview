#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:41:45 2017

@author: sebastian
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyleFactory, \
    QGridLayout, QListWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidgetItem, \
        QStatusBar, QProgressBar, QSplitter, QGroupBox, QCheckBox, QRadioButton, QComboBox, QLineEdit,\
            QLabel, QFormLayout, QSpinBox, QFileDialog
#from PyQt5 import QStyleFactory
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon


import numpy as np
import pyqtgraph as pg
import matplotlib.image as mpimg
from os import listdir
import os
from os.path import isfile, join
from camview.readimg import sbf, plifimg, sif, lvsor, mptif16
from camview.readlvfile import readlvfile
from camview.ImageViewPfaff import ImageViewPfaff
import pickle
import pyqtgraph.ptime as ptime

class CCCView(QWidget):
    def __init__(self,LoadFile=None):
        super().__init__()
        self.LoadFileName=LoadFile
        self.noRepeatKeys = [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left, QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]
        self.keysPressed = {}
        self.playTimer = QtCore.QTimer()
        self.playRate = 0
        self.fps = 1 # 1 Hz by default
        self.lastPlayTime = 0
        self.playTimer.timeout.connect(self.timeout)

        self.PLIFFileName=''
        self.readRaw=False
        self.fromFrame=0
        self.toFrame=-1
        self.profileMode=0
        self.profileData=None

        self.dispInvert=False
        self.dispDiff=False
        self.divProfile=True
        self.showData=np.random.rand(256,256,256)
        self.averagedProfiles={}
        self.childViews=[]
        self.path = '.'
        #self.initUI()

        if len(sys.argv) > 1:
            self.path = sys.argv[1]
        if self.LoadFileName is not None:
            print(self.LoadFileName)
            self.path=os.path.dirname(self.LoadFileName)

    def cmapClicked(self,LoadFile=None):
        """onclick handler for our custom entries in the GradientEditorItem's context menu"""
        act = self.sender()
        self.hist.gradient.restoreState(self.mplCmaps[act.name])
        if act.name == 'turbo':
            self.hist.gradient.showTicks(show=False)

    def initUI(self):
        self.ROIList=[]
        self.timeAxis=None #will contain the time for each frame

        self.resize(1300, 900)
        self.move(500, 300)

        MainGrid=QGridLayout(self)

        win = pg.GraphicsLayoutWidget()

        # self.status = QStatusBar(self)
        # self.statusProgress = QProgressBar()
        # self.status.addWidget(self.statusProgress)
        # MainGrid.addWidget(self.status,20,0,1,2)
        # self.status.showMessage('TestStatus')


        self.imgPlot=win.addPlot(row=0,col=0)
        self.img=pg.ImageItem()
        self.imgPlot.addItem(self.img)
        self.imgPlot.setAspectLocked()

        self.hist = pg.HistogramLUTItem()
        self.mplCmaps = {}

        def registerCmap(gradientEditor, cmapNames):
            import matplotlib
            """ Add matplotlib cmaps to the GradientEditors context menu"""
            #gradientEditor.menu.addSeparator()
            savedLength = gradientEditor.length
            gradientEditor.length = 100

            
            def cmapToColormap(cmap, nTicks=16):
                """
                Converts a Matplotlib cmap to pyqtgraphs colormaps. No dependency on matplotlib.
                Parameters:
                *cmap*: Cmap object. Imported from matplotlib.cm.*
                *nTicks*: Number of ticks to create when dict of functions is used. Otherwise unused.
                """
                import collections
                # Case #1: a dictionary with 'red'/'green'/'blue' values as list of ranges (e.g. 'jet')
                # The parameter 'cmap' is a 'matplotlib.colors.LinearSegmentedColormap' instance ...
                if hasattr(cmap, '_segmentdata'):
                    colordata = getattr(cmap, '_segmentdata')
                    if ('red' in colordata) and isinstance(colordata['red'], collections.Sequence):
                        # print("[cmapToColormap] RGB dicts with ranges")

                        # collect the color ranges from all channels into one dict to get unique indices
                        posDict = {}
                        for idx, channel in enumerate(('red', 'green', 'blue')):
                            for colorRange in colordata[channel]:
                                posDict.setdefault(colorRange[0], [-1, -1, -1])[idx] = colorRange[2]

                        indexList = list(posDict.keys())
                        indexList.sort()
                        # interpolate missing values (== -1)
                        for channel in range(3):  # R,G,B
                            startIdx = indexList[0]
                            emptyIdx = []
                            for curIdx in indexList:
                                if posDict[curIdx][channel] == -1:
                                    emptyIdx.append(curIdx)
                                elif curIdx != indexList[0]:
                                    for eIdx in emptyIdx:
                                        rPos = (eIdx - startIdx) / (curIdx - startIdx)
                                        vStart = posDict[startIdx][channel]
                                        vRange = (posDict[curIdx][channel] - posDict[startIdx][channel])
                                        posDict[eIdx][channel] = rPos * vRange + vStart
                                    startIdx = curIdx
                                    del emptyIdx[:]
                        for channel in range(3):  # R,G,B
                            for curIdx in indexList:
                                posDict[curIdx][channel] *= 255

                        posList = [[i, posDict[i]] for i in indexList]
                        return posList

                    # Case #2: a dictionary with 'red'/'green'/'blue' values as functions (e.g. 'gnuplot')
                    elif ('red' in colordata) and isinstance(colordata['red'], collections.Callable):
                        # print("[cmapToColormap] RGB dict with functions")
                        indices = np.linspace(0., 1., nTicks)
                        luts = [np.clip(np.array(colordata[rgb](indices), dtype=np.float), 0, 1) * 255 \
                                for rgb in ('red', 'green', 'blue')]
                        return list(zip(indices, list(zip(*luts))))

                # If the parameter 'cmap' is a 'matplotlib.colors.ListedColormap' instance, with the attributes 'colors' and 'N'
                elif hasattr(cmap, 'colors') and hasattr(cmap, 'N'):
                    colordata = getattr(cmap, 'colors')
                    # Case #3: a list with RGB values (e.g. 'seismic')
                    if len(colordata[0]) == 3:
                        # print("[cmapToColormap] list with RGB values")
                        indices = np.linspace(0., 1., len(colordata))
                        scaledRgbTuples = [(rgbTuple[0] * 255, rgbTuple[1] * 255, rgbTuple[2] * 255) for rgbTuple in colordata]
                        return list(zip(indices, scaledRgbTuples))

                    # Case #4: a list of tuples with positions and RGB-values (e.g. 'terrain')
                    # -> this section is probably not needed anymore!?
                    elif len(colordata[0]) == 2:
                        # print("[cmapToColormap] list with positions and RGB-values. Just scale the values.")
                        scaledCmap = [(idx, (vals[0] * 255, vals[1] * 255, vals[2] * 255)) for idx, vals in colordata]
                        return scaledCmap

                # Case #X: unknown format or datatype was the wrong object type
                else:
                    raise ValueError("[cmapToColormap] Unknown cmap format or not a cmap!")

            # iterate over the list of cmap names and check if they're avaible in MPL
            for cmapName in cmapNames:
                if not hasattr(matplotlib.cm, cmapName):
                    print('[MplCmapImageView] Unknown cmap name: \'{}\'. Your Matplotlib installation might be outdated.'.format(cmapName))
                else:
                    # create a Dictionary just as the one at the top of GradientEditorItem.py
                    cmap = getattr(matplotlib.cm, cmapName)
                    self.mplCmaps[cmapName] = {'ticks': cmapToColormap(cmap), 'mode': 'rgb'}

                    # Create the menu entries
                    # The following code is copied from pyqtgraph.ImageView.__init__() ...
                    px = QtGui.QPixmap(100, 15)
                    p = QtGui.QPainter(px)
                    gradientEditor.restoreState(self.mplCmaps[cmapName])
                    grad = gradientEditor.getGradient()
                    brush = QtGui.QBrush(grad)
                    p.fillRect(QtCore.QRect(0, 0, 100, 15), brush)
                    p.end()
                    label = QtGui.QLabel()
                    label.setPixmap(px)
                    label.setContentsMargins(1, 1, 1, 1)
                    labelName = QtGui.QLabel(cmapName)
                    hbox = QtGui.QHBoxLayout()
                    hbox.addWidget(labelName)
                    hbox.addWidget(label)
                    widget = QtGui.QWidget()
                    widget.setLayout(hbox)
                    act = QtGui.QWidgetAction(gradientEditor)
                    act.setDefaultWidget(widget)
                    act.triggered.connect(self.cmapClicked)
                    act.name = cmapName
                    gradientEditor.menu.addAction(act)
            gradientEditor.length = savedLength
            gradientEditor.menu.removeAction(gradientEditor.rgbAction)
            gradientEditor.menu.removeAction(gradientEditor.hsvAction)

        registerCmap(self.hist.gradient,['jet','turbo'])

        self.hist.setImageItem(self.img)
        self.hist.setMaximumWidth(200)
        self.hist.gradient.showTicks(show=False)
        self.imgPlot=win.addItem(self.hist,row=0,col=1)


        self.trendPlot=win.addPlot(row=1,col=0)
        self.trendScroll=pg.InfiniteLine(movable=True)
        self.trendPlot.addItem(self.trendScroll)
        self.trendPlot.setMaximumHeight(300)

        MainGrid.addWidget(win,0,0,8,1)

        self.trendScroll.sigPositionChanged.connect(self.sliderDragged)

        if len(sys.argv) > 1:
            self.path = sys.argv[1]

        def pathChanged(text):
            if text[-1]=='/':
                self.path=text
            else:
                self.path=text+'/'
            self.fillPathBoxes(text)


        GlobalGroup=QGroupBox('Global')
        GlobalGroup.setMaximumWidth(400)
        GlobalLayout=QFormLayout(GlobalGroup)
        PathBox=QLineEdit(self.path)
        PathBox.textChanged.connect(pathChanged)
        GlobalLayout.addRow('Path',PathBox)
        MainGrid.addWidget(GlobalGroup,0,1)

        ################ ROI ########################

        ROIGroup = QGroupBox('Region of Interest')
        ROIGrid=QGridLayout(ROIGroup)
        MainGrid.addWidget(ROIGroup,5,1)

        addROIbtn=QPushButton('Add ROI')
        delROIbtn=QPushButton('Delete ROI')
        self.ROIListW=QListWidget()
        #self.ROIListW.setMaximumHeight(100)
        self.ROIListW.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        ROIGrid.addWidget(self.ROIListW,1,0,1,2)
        ROIGrid.addWidget(addROIbtn,0,0)
        ROIGrid.addWidget(delROIbtn,0,1)

        addROIbtn.clicked.connect(self.addROI)
        delROIbtn.clicked.connect(self.delROI)

        OtherData = QGroupBox('Additional Data')
        OtherLayout=QHBoxLayout(OtherData)
        LoadOtherButton=QPushButton('Load LV/SOR/PMIRRAS')
        OtherLayout.addWidget(LoadOtherButton)
        LoadOtherButton.pressed.connect(self.LoadOther)
        MainGrid.addWidget(OtherData,7,1)


        # restore()
        self.show()
        return MainGrid
    def sliderDragged(self):
        """Handles what happens when the time slider is dragged. Synchs will all children."""
        #self.trendScroll.sigPositionChanged.disconnect()
        for child in self.childViews:
            child.trendScroll.setPos(self.trendScroll.getPos()[0])
        #self.trendScroll.sigPositionChanged.connect(self.sliderDragged)
        self.redrawSheet()

    def addROI(self):
        """Handles adding a ROI and creates entry in a tuple containing 
        (The MenuItem in the ROI menu, the ROI element in the plot, the plot showing the trend, and the pen used to draw the ROI and the plot)"""
        numROIs=len(self.ROIList)
        ROIMenuItem=QListWidgetItem('ROI '+str(numROIs))
        ROIMenuItem.setFlags(ROIMenuItem.flags() | QtCore.Qt.ItemIsEditable)
        #ROIMenuItem.setCheckState(True)
        self.ROIListW.addItem(ROIMenuItem)
        actualROI=pg.RectROI((0,0),(20,20))
        ROIPlot=pg.PlotDataItem()
        ROIpen=pg.mkPen(pg.intColor(numROIs))
        ROIPlot.setPen(ROIpen)
        actualROI.setPen(ROIpen)
        appendTuple=(ROIMenuItem,actualROI,ROIPlot,ROIpen)
        self.ROIList.append(appendTuple)
        self.img.getViewBox().addItem(actualROI)
        actualROI.sigRegionChanged.connect(self.ROIDragged)
        self.trendPlot.addItem(ROIPlot)

    def delROI(self):
        for ROIEntry in self.ROIListW.selectedItems():
            for jdx,ROI in enumerate(self.ROIList):
                if ROI[0]==ROIEntry:
                    self.img.getViewBox().removeItem(ROI[1])
                    self.ROIListW.takeItem(self.ROIListW.row(ROIEntry))
                    self.ROIList.pop(jdx)
                    self.trendPlot.removeItem(ROI[2])

    def ROIDragged(self,draggedROI):
        """Handles dragging the ROI. Overload this in the specific class. Otherwise it will just display a trend of showData"""
        dataItem=None
        listItem=None
        for ROI in self.ROIList:
            if ROI[1]==draggedROI:
                dataItem=ROI[2]
                listItem=ROI[0]
        data, coords = draggedROI.getArrayRegion(data=self.showData, img=self.img, axes=(1,2),returnMappedCoords=True) #slice the image
        dataItem.setData(self.timeAxis,np.mean(data,axis=(1,2)))  #plot the ROI trend
        xROILocString='X: {:.0f}-{:.0f}'.format(np.min(coords[0]),np.max(coords[0]))
        yROILocString='Y: {:.0f}-{:.0f}'.format(np.min(coords[1]),np.max(coords[1]))
        listItem.setText(xROILocString+', '+yROILocString)

    def LVtimeLineChanged(self,sender):
        pos=sender.getPos()[0]
        self.trendScroll.setPos(pos)
        
    def LoadPLIF(self):
        """Loads the data and return it in format (time, x, y). Overload it."""
        pass

    def LoadOther(self):
        """Add another file, LV, PLIF, SOR, and in the future PMIRRAS"""
        file=(QFileDialog.getOpenFileName(None,"Select a file...",self.path, filter="SOR Files (*.sor *.tif *.sif);;PLIF Files (*.img *.sif);;LabView Logs (*.txt)"))
        childView=None
        if 'LabView Logs (*.txt)' in file[1]:
            from lvtxtview import LVView
            childView=LVView(file[0])
            for slider in childView.sliders:
                slider.sigPositionChanged.connect(self.LVtimeLineChanged)
            childView.show()
            self.childViews.append(childView)
            return
        if 'SOR Files' in file[1]:
            from pyqtgraphSOR import SORView
            childView=SORView(os.path.dirname(file[0])+'/')
        if 'PLIF Files (*.img *.sif)' in file[1]:
            from PLIFViewer import PLIFView
            childView=PLIFView(os.path.dirname(file[0])+'/')
        childView.trendScroll.sigPositionChanged.connect(self.LVtimeLineChanged)
        childView.show()
        self.childViews.append(childView)


    def setCurrentIndex(self,index):
        """"Move in time. Overload if necessary."""
        self.trendScroll.setPos(index)

    def keyPressEvent(self, ev):
        #print ev.key()
        if ev.key() == QtCore.Qt.Key_Space:
            if self.playRate == 0:
                self.play()
            else:
                self.play(0)
            ev.accept()
        elif ev.key() == QtCore.Qt.Key_Home:
            self.setCurrentIndex(0)
            self.play(0)
            ev.accept()
        elif ev.key() == QtCore.Qt.Key_End:
            self.setCurrentIndex(self.getProcessedImage().shape[0]-1)
            self.play(0)
            ev.accept()
        elif ev.key() in self.noRepeatKeys:
            ev.accept()
            if ev.isAutoRepeat():
                return
            self.keysPressed[ev.key()] = 1
            self.evalKeyState()
        else:
            QtGui.QWidget.keyPressEvent(self, ev)

    def keyReleaseEvent(self, ev):
        if ev.key() in [QtCore.Qt.Key_Space, QtCore.Qt.Key_Home, QtCore.Qt.Key_End]:
            ev.accept()
        elif ev.key() in self.noRepeatKeys:
            ev.accept()
            if ev.isAutoRepeat():
                return
            try:
                del self.keysPressed[ev.key()]
            except:
                self.keysPressed = {}
            self.evalKeyState()
        else:
            QtGui.QWidget.keyReleaseEvent(self, ev)
    
    def jumpFrames(self,n):
        self.trendScroll.setPos(self.trendScroll.getPos()[0]+n)

    def evalKeyState(self):
        if len(self.keysPressed) == 1:
            key = list(self.keysPressed.keys())[0]
            if key == QtCore.Qt.Key_Right:
                self.play(20)
                self.jumpFrames(1)
                self.lastPlayTime = ptime.time() + 0.2  ## 2ms wait before start
                                                        ## This happens *after* jumpFrames, since it might take longer than 2ms
            elif key == QtCore.Qt.Key_Left:
                self.play(-20)
                self.jumpFrames(-1)
                self.lastPlayTime = ptime.time() + 0.2
            elif key == QtCore.Qt.Key_Up:
                self.play(-100)
            elif key == QtCore.Qt.Key_Down:
                self.play(100)
            elif key == QtCore.Qt.Key_PageUp:
                self.play(-1000)
            elif key == QtCore.Qt.Key_PageDown:
                self.play(1000)
        else:
            self.play(0)

    def play(self, rate=None):
        """Begin automatically stepping frames forward at the given rate (in fps).
        This can also be accessed by pressing the spacebar."""
        #print "play:", rate
        if rate is None: 
            rate = self.fps
        self.playRate = rate

        if rate == 0:
            self.playTimer.stop()
            return
            
        self.lastPlayTime = ptime.time()
        if not self.playTimer.isActive():
            self.playTimer.start(16)

    def timeout(self):
        now = ptime.time()
        dt = now - self.lastPlayTime
        if dt < 0:
            return
        n = int(self.playRate * dt)
        if n != 0:
            self.lastPlayTime += (float(n)/self.playRate)
            if int(self.trendScroll.getPos()[0])+n > self.showData.shape[2]:
                self.play(0)
            self.jumpFrames(n)

#%%
#code here is just for testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('LU PLIF Viewer')
    app.setWindowIcon(QIcon('PLIF-icon-256.png'))
    plifv = CCCView()
    plifv.initUI()
    # sys.exit(app.exec_())
    app.exec_()

# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
# https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
