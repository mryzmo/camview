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
            QLabel, QFormLayout, QSpinBox
#from PyQt5 import QStyleFactory
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon


import numpy as np
import pyqtgraph as pg

import pyqtgraph.console
import matplotlib.image as mpimg
from os import listdir
from os.path import isfile, join
from camview.readimg import sbf, plifimg, sif
from camview.readlvfile import readlvfile
from camview.ImageViewPfaff import ImageViewPfaff
import pickle
import pyqtgraph.ptime as ptime
from camview.CCCView import CCCView
import os

class PLIFView(CCCView):
    def __init__(self,LoadFile=None):
        super().__init__(LoadFile)
        self.PLIFFileName=''
        self.readRaw=False
        self.fromFrame=0
        self.toFrame=-1
        self.profileMode=0
        self.profileData=None
        self.numBg=1

        self.dispInvert=False
        self.dispDiff=False
        self.divProfile=True
        self.averagedProfiles={}
        self.pathBoxes=[]

        self.showProfile=False
        self.UseAltBg=False
        self.initUI()

    def initUI(self):
        #self.path = './testdata/2021-03-17/'
        MainGrid=super(PLIFView,self).initUI()

        self.setWindowTitle('PLIF Image Viewerz')

        def LoadBgCheckClicked(yes):
            self.readRaw=yes
            ProfileGroup.setEnabled(not yes)    

        
        

        def fileNameChangedFunc(filename):
            if '.img' in filename:
                PLIFBgFileNameWidget.setVisible(False)
            self.PLIFFileName=self.path+filename

        PLIFGroup = QGroupBox('PLIF')
        PLIFGroup.setMaximumWidth(400)
        PLIFLayout=QVBoxLayout(PLIFGroup)
        
        PLIFFileNameWidget=QWidget()
        PLIFFileNameLayout=QHBoxLayout(PLIFFileNameWidget)
        PLIFFileNameLayout.setContentsMargins(0,0,0,0)
        PLIFFileNameBox=QComboBox()
        PLIFFileNameBox.setMinimumWidth(250)
        PLIFFileNameLayout.addWidget(QLabel('Data file'))
        PLIFFileNameLayout.addWidget(PLIFFileNameBox)
        PLIFLayout.addWidget(PLIFFileNameWidget)
        PLIFFileNameBox.currentTextChanged.connect(fileNameChangedFunc)

        PLIFBgFileNameWidget=QWidget()
        PLIFBgFileNameLayout=QHBoxLayout(PLIFBgFileNameWidget)
        PLIFBgFileNameLayout.setContentsMargins(0,0,0,0)
        PLIFBgFileNameBox=QComboBox()
        self.pathBoxes.append(PLIFFileNameBox)
        self.pathBoxes.append(PLIFBgFileNameBox)
        PLIFBgFileNameBox.setMinimumWidth(250)
        PLIFBgFileNameLayout.addWidget(QLabel('Background file'))
        PLIFBgFileNameLayout.addWidget(PLIFBgFileNameBox)
        PLIFLayout.addWidget(PLIFBgFileNameWidget)

        def SetAvg(value):
            self.LoadAverage=value

        def SetAltBg(value):
            self.UseAltBg=value

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

        LoadBgCheck=QCheckBox('Raw FPA data (sbf only)')
        LoadBgCheck.setChecked(False)

        def NumBgBoxFunc(value):
            self.numBg=value

        BgBox=QWidget()
        BgBoxLayout=QHBoxLayout(BgBox)
        AltBgCheck=QCheckBox('Use alt. bg.')
        AltBgCheck.toggled.connect(SetAltBg)
        BgBoxLayout.addWidget(AltBgCheck)
        BgBoxLayout.setContentsMargins(0,0,0,0)
        NumBgBox=QSpinBox()
        NumBgBox.setValue(1)
        LaserImgBox=QSpinBox()
        LaserImgBox.setValue(0)
        BgBoxLayout.addWidget(QLabel("Number of Bg images")) #number of bg shots
        BgBoxLayout.addWidget(NumBgBox)
        NumBgBox.valueChanged.connect(NumBgBoxFunc)

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
        PLIFLayout.addWidget(BgBox)
        PLIFLayout.addWidget(LoadBgCheck)
        LoadBgCheck.stateChanged.connect(LoadBgCheckClicked)

        LoadButton=QPushButton('Load Data File')
        PLIFLayout.addWidget(LoadButton)
        LoadButton.pressed.connect(self.loadFile)
        RangeRadios[0].setChecked(True)

        MainGrid.addWidget(PLIFGroup,2,1)

        ################ PROFILE ########################

        ProfileGroup = QGroupBox('Profile')
        ProfileGroup.setMaximumWidth(400)
        ProfileGrid=QGridLayout(ProfileGroup)
        UseSingleProfile=QRadioButton('Average single profile file',ProfileGroup)
        SingleProfileFiles=QComboBox()
        ProfileGrid.addWidget(SingleProfileFiles,1,0)

        UseAsRampProfile=QRadioButton('Use a profile with the same ramp as data',ProfileGroup)
        RampProfileFiles=QComboBox()
        UseMultipleProfiles=QRadioButton('Use multiple profile files',ProfileGroup)
        ProfileGrid.addWidget(RampProfileFiles,3,0)
        profileRadios=[UseSingleProfile,UseAsRampProfile,UseMultipleProfiles]

        #ProfileListW=QListWidget()
        ProfileListW=QWidget()
        ProfileListLayout=QVBoxLayout(ProfileListW)
        ProfileListListW=QListWidget()
        
        ProfileListLayout.addWidget(ProfileListListW)

        ProfileButtonsW=QWidget()
        ProfileButtonsWLayout=QHBoxLayout(ProfileButtonsW)
        AddProfileButton=QPushButton('Add Profile')
        RemProfileButton=QPushButton('Remove Profile')
        ProfileButtonsWLayout.addWidget(RemProfileButton)
        ProfileButtonsWLayout.addWidget(AddProfileButton)
        ProfileListLayout.addWidget(ProfileButtonsW)
        #ProfileListW.setMaximumHeight(100)
        ProfileGrid.addWidget(ProfileListW,7,0,1,1)
        self.pathBoxes.append(SingleProfileFiles)
        self.pathBoxes.append(RampProfileFiles)
        self.pathBoxes.append(ProfileListListW)
        

        def ProfileRadioChanged():
            fields=[SingleProfileFiles, RampProfileFiles, ProfileListW]
            for i,field in enumerate(fields):
                if profileRadios[i].isChecked():
                    field.setVisible(True)
                    self.profileMode=i
                    if i < 2:
                        self.ProfileFileName=self.path+field.currentText()
                    else:
                        self.ProfileFileName=[]
                        for index in range(ProfileListListW.count()):
                            if ProfileListListW.item(index).checkState()==2:
                                self.ProfileFileName.append(ProfileListListW.item(index))
                else:
                    field.setVisible(False)

        for i,radio in enumerate(profileRadios):
            ProfileGrid.addWidget(radio,i*2,0)
            radio.toggled.connect(ProfileRadioChanged)

        def startLoadProfile():
            ProfileRadioChanged()
            self.LoadProfile()
        #ProfileListListW.itemSelectionChanged.connect(ProfileRadioChanged)
        ProfileButton=QPushButton('Load Profile')
        ProfileGrid.addWidget(ProfileButton,10,0,1,1)
        ProfileButton.pressed.connect(startLoadProfile)
        MainGrid.addWidget(ProfileGroup,3,1)
        UseAsRampProfile.setChecked(True)

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

        def showProfileChanged(diff):
            self.showProfile=diff
            self.redrawSheet()

        DisplayGroup = QGroupBox('Display')
        DisplayGrid=QGridLayout(DisplayGroup)

        ProfileCheck=QCheckBox('Divide by profile/range')
        ProfileCheck.setChecked(True)
        InvertCheck=QCheckBox('Invert')
        DiffCheck=QCheckBox('Show Difference')
        showProfileCheck=QCheckBox('Show profile')

        InvertCheck.toggled.connect(InvertChanged)
        DiffCheck.toggled.connect(DiffChanged)
        ProfileCheck.toggled.connect(ProfileChanged)
        showProfileCheck.toggled.connect(showProfileChanged)


        DisplayGrid.addWidget(InvertCheck,0,0)
        DisplayGrid.addWidget(DiffCheck,0,1)
        DisplayGrid.addWidget(ProfileCheck,1,0)
        DisplayGrid.addWidget(showProfileCheck,1,1)

        MainGrid.addWidget(DisplayGroup,4,1)

        ProfileRadioChanged()
        self.fillPathBoxes(self.path)
        if self.LoadFileName is not None:
            pass
        # restore()
        self.show()

    def fillPathBoxes(self,path):
        pathBoxes=self.pathBoxes
        for box in pathBoxes:
            box.clear()

        try:
            files = [f for f in listdir(path) if isfile(join(path, f)) and 'maestro' not in str(f)]
        except FileNotFoundError:
            return
        for thisfile in files:
            if 'profile' in thisfile:
                pathBoxes[2].addItem(thisfile)
                pathBoxes[3].addItem(thisfile)
                ProfileListItem=QListWidgetItem(thisfile)
                ProfileListItem.setCheckState(False)
                pathBoxes[4].addItem(ProfileListItem)

            if 'img' in thisfile or 'sif' in thisfile:
                pathBoxes[0].addItem(thisfile)
                pathBoxes[1].addItem(thisfile)


    def ROIDragged(self,draggedROI):
        dataItem=None
        listItem=None
        invfactor=1
        if self.dispInvert:
            invfactor = -1
        for ROI in self.ROIList:
            if ROI[1]==draggedROI:
                dataItem=ROI[2]
                listItem=ROI[0]
        profileROI=1
        if self.divProfile and not self.readRaw:
            profile, coords = draggedROI.getArrayRegion(data=self.profileData, img=self.img, axes=(1,2),returnMappedCoords=True)
            if self.profileMode==0:
                profileROI=np.mean(profile)
            else:
                profileROI=np.mean(profile, axis=(1,2))
        data, coords = draggedROI.getArrayRegion(data=self.showData, img=self.img, axes=(1,2),returnMappedCoords=True)
        meanData=np.mean(data,axis=(1,2))
        xROILocString='X: {:.0f}-{:.0f}'.format(np.min(coords[0]),np.max(coords[0]))
        yROILocString='Y: {:.0f}-{:.0f}'.format(np.min(coords[1]),np.max(coords[1]))
        listItem.setText(xROILocString+', '+yROILocString)
        dataItem.setData(self.timeAxis,invfactor*meanData/profileROI)

    def LoadPLIF(self):
        if self.PLIFFileName.endswith('.sif'):
            file = sif(self.PLIFFileName)
        else:
            file = sbf(self.PLIFFileName,numbgframes=self.numBg)
            file.findPLIFframe()
        if self.readRaw:
            if self.UseAltBg:
                startimg = 1
            else:
                startimg = 0
            if self.numBg==1:    
                plifdata = file.readraw(self.fromFrame,self.toFrame)#[:,:,startimg::2]
            else:
                plifdata = file.readraw(self.fromFrame,self.toFrame)
        else:
            plifdata = plifimg.readimgav(file, self.fromFrame,self.toFrame, self.LoadAverage,altbg=self.UseAltBg)
        return plifdata.swapaxes(0,2).swapaxes(1,2),file

    def LoadProfile(self):
        if self.profileMode==2:
            for file in self.ProfileFileName:
                filename=self.path+file.text
            return

        if self.ProfileFileName.endswith('.sif'):
            file = sif(self.ProfileFileName)
        else:
            file = sbf(self.ProfileFileName,numbgframes=self.numBg)
        if self.profileMode==0:
            self.profileData=np.squeeze(plifimg.readimgav(file,0,-1,-1)).swapaxes(1,2)
        if self.profileMode==1:
            self.profileData=plifimg.readimgav(file,self.fromFrame,self.toFrame,self.LoadAverage).swapaxes(0,2)#.swapaxes(1,2)

        #return profiledata

    def getProfile(self,frame):
        if self.profileData is None:
            return 1
        if self.profileMode==0:
            return self.profileData
        if self.profileMode==1:
            TempProfile=self.profileData[int(frame)]
            #TempProfile[TempProfile<10]=10
            return TempProfile

    def loadFile(self):
        self.setWindowTitle('PLIF Image Viewer - '+ self.PLIFFileName.split('/')[-1])
        plifdata,file = self.LoadPLIF()
        self.showData = plifdata

        if self.readRaw:
            starttime=self.fromFrame//(self.numBg+1)//10
            if self.toFrame==-1:
                endtime=(file.numimgframes(rawcount=True)-1)//(self.numBg+1)//10
                print(file.numimgframes(True))
            else:
                endtime=self.toFrame//(self.numBg+1)//10
        else:
            starttime=self.fromFrame/10
            if self.toFrame==-1:
                endtime=file.numimgframes()/10
            else:
                endtime=self.toFrame/10
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

        if self.readRaw:
            framenr=int(self.trendScroll.getPos()[0]*(self.numBg+1)*10)-self.fromFrame
        else:
            framenr=int(10*self.trendScroll.getPos()[0]//(self.LoadAverage))-self.fromFrame//(self.LoadAverage)

        if framenr>np.shape(self.showData)[0]-1: #prevent overflow
            framenr=np.shape(self.showData)[0]-1
        profileFactor=1
        print('nr: '+str(framenr))
        if self.divProfile and not self.profileData is None and not self.readRaw:
            profileFactor=self.getProfile(framenr)

        if self.showProfile and not self.profileData is None and not self.readRaw:
            profileFactor=self.getProfile(framenr)
            self.img.setImage(invfactor/profileFactor,autoLevels=sender is not None)
            return

        if self.dispDiff:
            if framenr==0:
                framenr=1
            self.img.setImage(invfactor/profileFactor*(self.showData[framenr, :, :]-self.showData[framenr-1, :, :]),autoLevels=False)
        else:
            self.img.setImage(invfactor/profileFactor*self.showData[framenr, :, :],autoLevels=sender is not None)

class PLIFViewApp:
    def __init__(self):
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        app = QApplication(sys.argv)
        app.setApplicationName('LU PLIF Viewer')
        app.setWindowIcon(QIcon('PLIF-icon-256.png'))
        plifv = PLIFView()
        # sys.exit(app.exec_())
        app.exec_()

if __name__ == '__main__':
    app=PLIFViewApp()


# https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
