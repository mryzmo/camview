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
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import pyqtgraph.console
import matplotlib.image as mpimg
from os import listdir
from os.path import isfile, join
from camview.readimg import sbf, plifimg, sif, lvsor, mptif16, spe
from camview.readlvfile import readlvfile
from camview.ImageViewPfaff import ImageViewPfaff
import pickle
import pyqtgraph.ptime as ptime
from camview.CCCView import CCCView

class SORView(CCCView):
    def __init__(self,LoadFile=None):
        super().__init__(LoadFile)

        self.PLIFFileName=''
        self.fromFrame=0
        self.toFrame=-1
        self.LoadFps=10

        self.divData=1
        self.dispInvert=False
        self.dispDiff=False
        self.divProfile=False
        self.showData=np.random.rand(256,256,256)
        self.initUI()

    def cmapClicked(self, b=None):
        """onclick handler for our custom entries in the GradientEditorItem's context menu"""
        act = self.sender()
        self.hist.gradient.restoreState(self.mplCmaps[act.name])
        if act.name == 'turbo':
            self.hist.gradient.showTicks(show=False)

    def initUI(self):
        self.setWindowTitle('SOR Image Viewer')
        MainGrid=super(SORView,self).initUI()
        print(MainGrid.itemAtPosition(0,1))
        # self.status = QStatusBar(self)
        # self.statusProgress = QProgressBar()
        # self.status.addWidget(self.statusProgress)
        # MainGrid.addWidget(self.status,20,0,1,2)
        # self.status.showMessage('TestStatus')


        def divRegionChanged():
            if self.divProfile:
                fromframe=int(divRegion.getRegion()[0]/self.LoadAverage*10)-1
                toframe=int(divRegion.getRegion()[1]/self.LoadAverage*10)-1
                print(fromframe)
                print(toframe)
                self.divData=np.mean(self.showData[fromframe:toframe,:,:],axis=0)
                self.redrawSheet()

        divRegion=pg.LinearRegionItem()
        self.trendPlot.addItem(divRegion)
        divRegion.sigRegionChangeFinished.connect(divRegionChanged)
        #self.path = './testdata/2021-03-17/'
        if len(sys.argv) > 1:
            self.path = sys.argv[1]
        
        def fileNameChangedFunc(filename):
            self.PLIFFileName=self.path+filename
            print(self.PLIFFileName)

        PLIFGroup = QGroupBox('SOR')
        PLIFGroup.setMaximumWidth(400)
        PLIFLayout=QVBoxLayout(PLIFGroup)
        
        PLIFFileNameWidget=QWidget()
        PLIFFileNameLayout=QHBoxLayout(PLIFFileNameWidget)
        PLIFFileNameLayout.setContentsMargins(0,0,0,0)
        self.PLIFFileNameBox=QComboBox()
        self.PLIFFileNameBox.setMinimumWidth(250)
        PLIFFileNameLayout.addWidget(QLabel('Data file'))
        PLIFFileNameLayout.addWidget(self.PLIFFileNameBox)
        PLIFLayout.addWidget(PLIFFileNameWidget)
        self.PLIFFileNameBox.currentTextChanged.connect(fileNameChangedFunc)

        def SetAvg(value):
            self.LoadAverage=value
        
        def SetFps(value):
            self.LoadFps=value

        AvgWidget=QWidget()
        AvgBox=QSpinBox()
        AvgBox.valueChanged.connect(SetAvg)
        AvgBox.setValue(10)
        AvgBox.setRange(0,100000)
        AvgLayout=QHBoxLayout(AvgWidget)
        AvgLayout.addWidget(QLabel('Average every'))
        AvgLayout.addWidget(AvgBox)
        AvgLayout.addWidget(QLabel('frames'))
        AvgLayout.setContentsMargins(0,0,0,0)
        PLIFLayout.addWidget(AvgWidget)

        FpsWidget=QWidget()
        FpsBox=QSpinBox()
        FpsBox.setRange(1,400)
        FpsBox.valueChanged.connect(SetFps)
        FpsLayout=QHBoxLayout(FpsWidget)
        FpsLayout.addWidget(QLabel('Footage is'))
        FpsLayout.addWidget(FpsBox)
        FpsLayout.addWidget(QLabel('fps'))
        FpsLayout.setContentsMargins(0,0,0,0)
        PLIFLayout.addWidget(FpsWidget)

        LoadBgCheck=QCheckBox('Load IR background (sbf only)')
        LoadBgCheck.setChecked(False)

        def RangeRadioChange():
                for i,radio in enumerate(RangeRadios):
                    if i == 1 and radio.isChecked():
                        FromBox.setEnabled(True)
                        ToBox.setEnabled(True)
                        self.fromFrame=FromBox.value()
                        self.toFrame=ToBox.value()
                    if i == 0 and radio.isChecked():
                        FromBox.setEnabled(False)
                        ToBox.setEnabled(False)
                        self.fromFrame=0
                        self.toFrame=-1

        RangeWidget=QWidget()
        RangeLayout=QHBoxLayout(RangeWidget)
        RangeLayout.setContentsMargins(0,0,0,0)
        RangeRadios=[QRadioButton('All frames'),QRadioButton('Range')]
        for i,radio in enumerate(RangeRadios):
            RangeLayout.addWidget(radio)
            radio.toggled.connect(RangeRadioChange)

        FromBox=QSpinBox()
        ToBox=QSpinBox()
        FromBox.valueChanged.connect(RangeRadioChange)
        ToBox.valueChanged.connect(RangeRadioChange)

        ToBox.setRange(0,1000000)
        FromBox.setRange(0,1000000)

        RangeLayout.addWidget(FromBox)
        dashLabel=QLabel('to')
        dashLabel.setMaximumWidth(15)
        RangeLayout.addWidget(dashLabel)
        RangeLayout.addWidget(ToBox)
        PLIFLayout.addWidget(RangeWidget)
        PLIFLayout.addWidget(LoadBgCheck)

        LoadButton=QPushButton('Load Data File')
        PLIFLayout.addWidget(LoadButton)
        LoadButton.pressed.connect(self.loadFile)
        RangeRadios[0].setChecked(True)

        MainGrid.addWidget(PLIFGroup,2,1)

        ################ DISPLAY ########################
        def ProfileChanged(profile):
            self.divProfile=profile
            self.redrawSheet()

        def InvertChanged(invert):
            self.dispInvert=invert
            self.redrawSheet()

        def DiffChanged(diff):
            self.dispDiff=diff
            self.redrawSheet()

        DisplayGroup = QGroupBox('Display')
        DisplayGrid=QGridLayout(DisplayGroup)

        ProfileCheck=QCheckBox('Divide by region')
        ProfileCheck.setChecked(False)
        InvertCheck=QCheckBox('Invert')
        DiffCheck=QCheckBox('Show Difference')

        InvertCheck.toggled.connect(InvertChanged)
        DiffCheck.toggled.connect(DiffChanged)
        ProfileCheck.toggled.connect(ProfileChanged)


        DisplayGrid.addWidget(InvertCheck,0,0)
        DisplayGrid.addWidget(DiffCheck,0,1)
        DisplayGrid.addWidget(ProfileCheck,1,0)

        MainGrid.addWidget(DisplayGroup,4,1)

        self.fillPathBoxes(self.path)

    def fillPathBoxes(self,path):
        self.PLIFFileNameBox.clear()
        try:
            files = [f for f in listdir(path) if isfile(join(path, f)) and 'maestro' not in str(f)]
        except FileNotFoundError:
            return
        for thisfile in files:
            if 'sor' in thisfile or 'sif' in thisfile or 'tif' in thisfile:
                self.PLIFFileNameBox.addItem(thisfile)

    def LoadPLIF(self):
        plifdata=None
        if self.PLIFFileName.endswith('.sif'):
            file = sif(self.PLIFFileName)
        if self.PLIFFileName.endswith('.SPE') or self.PLIFFileName.endswith('.spe'):
            file = spe(self.PLIFFileName)
        if self.PLIFFileName.endswith('.tif'):
            file = mptif16(self.PLIFFileName)
        else:
            print(self.PLIFFileName)
            file = lvsor(self.PLIFFileName)

        plifdata = plifimg.readimgav(file, self.fromFrame,self.toFrame, self.LoadAverage)
        return plifdata.swapaxes(0,2).swapaxes(1,2),file

    def loadFile(self):
        self.setWindowTitle('SOR Image Viewer - '+ self.PLIFFileName.split('/')[-1])
        plifdata,file = self.LoadPLIF()
        self.showData = plifdata
        #if self.p['PLIF', 'ProfileDivision'] and not self.p['PLIF', 'ReadRaw']:
        #    profiledata=self.LoadProfile()
        #    self.showData=np.true_divide(plifdata,profiledata)
        #    self.showData[self.showData < -10] = 20
        #    self.showData[self.showData > 20] = -10
        starttime=self.fromFrame/self.LoadAverage/self.LoadFps
        if self.toFrame>-1:
            endtime=self.toFrame/self.LoadAverage/self.LoadFps#-(1/self.LoadAverage*self.LoadFps)
        else:
            endtime=file.numimgframes()//10
        self.timeAxis=np.linspace(starttime,endtime,np.shape(plifdata)[0])
        self.trendPlot.setXRange(starttime,endtime)
        self.trendScroll.setBounds((starttime,endtime))
        self.showData = np.swapaxes(self.showData, 2, 1)

        self.redrawSheet()

    def redrawSheet(self,sender=None):
        #print(sender)
        if self.dispInvert:
            invfactor = -1
        else:
            invfactor = 1
        if self.toFrame==-1:
            endframe=np.shape(self.showData)[0]
        else:
            endframe=self.toFrame-1

        framenr=int(self.trendScroll.getPos()[0]/self.LoadAverage*self.LoadFps)-self.fromFrame
        print(framenr)
        profileFactor=1

        if self.divProfile and self.divData != 1:
            profileFactor=self.divData

        if self.dispDiff:
            if framenr==0:
                framenr=1
            self.img.setImage(invfactor/profileFactor*(self.showData[framenr, :, :]-self.showData[framenr-1, :, :].astype(np.intc)),autoLevels=False)
        else:
            self.img.setImage(invfactor/profileFactor*self.showData[framenr, :, :],autoLevels=False)

#%%
class SORViewApp:
    def __init__(self):
        import os
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        app = QApplication(sys.argv)
        app.setApplicationName('LU SOR Viewer')
        app.setWindowIcon(QIcon('PLIF-icon-256.png'))
        plifv = SORView()
        # sys.exit(app.exec_())
        app.exec_()

if __name__ == '__main__':
    app=SORViewApp()


# https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
