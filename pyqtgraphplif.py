#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:41:45 2017

@author: sebastian
"""
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
from readimg import sbf, plifimg
from readlvfile import readlvfile
from ImageViewPfaff import ImageViewPfaff
import pickle


class PLIFView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1300, 900)
        self.move(500, 300)
        self.setWindowTitle('PLIF Image Viewer')
        self.status = QStatusBar(self)
        self.statusProgress = QProgressBar()
        self.status.addWidget(self.statusProgress)

        grid= QGridLayout(self)
        img = ImageViewPfaff(
            view=pg.PlotItem(), additionalCmaps=['viridis', 'jet'])

        grid.addWidget(img,0,0,2,1)
        path = '/home/sebastian/Documents/Data/PdDiamond'
        if len(sys.argv) > 1:
            path = sys.argv[1]

        def initPanel(self):
            files = [f for f in listdir(path) if isfile(join(path, f)) and '.val' not in str(f)]

            params = [
            {'name': 'Geometry', 'type': 'group', 'children': [
                {'name': 'SheetTop', 'type': 'int', 'value': 0},
                {'name': 'SheetBottom', 'type': 'int', 'value': 250},
                {'name': 'String', 'type': 'str', 'value': "hi"},
                #{'name': 'Named List', 'type': 'list', 'values': {"one": 1, "two": "twosies", "three": [3,3,3]}, 'value': 2},
                {'name': 'Autoscale', 'type': 'bool',
                    'value': True, 'tip': "This is a checkbox"},
                {'name': 'ColorMapMax', 'type': 'int',
                    'value': 5},
                {'name': 'ColorMapMin', 'type': 'int',
                    'value': 0},
                {'name': 'CatalystSize', 'type': 'float', 'value': 10e-3,
                    'step': 1e-3, 'siPrefix': True, 'suffix': 'm'},
                {'name': 'DistPerPx', 'type': 'float', 'value': 80e-6, 'step': 1e-8,
                    'siPrefix': True, 'suffix': 'm/px'},
                #{'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
                #{'name': 'Gradient', 'type': 'colormap'},
                #{'name': 'Subgroup', 'type': 'group', 'children': [
                #    {'name': 'Sub-param 1', 'type': 'int', 'value': 10},
                #    {'name': 'Sub-param 2', 'type': 'float', 'value': 1.2e6},
                #]},
                #
                {'name': 'ForceRedraw', 'type': 'action'},
            ]},
            {'name': 'PLIFFile', 'type': 'group', 'children': [
                {'name': 'Path', 'type': 'str', 'value': path},
                {'name': 'RealFileName', 'type': 'list',
                    'values': files},
                {'name': 'ProfileFileName', 'type': 'list',
                    'values': files},
                {'name': 'LVFileName', 'type': 'list',
                    'values': files},
                {'name': 'Refresh', 'type': 'action'},
                {'name': 'ProfileDivision', 'type': 'bool', 'value': True,
                    'tip': "Divide each frame by the profile image"},
                {'name': 'ReadRaw', 'type': 'bool', 'value': False,
                    'tip': "No background subtraction"},
                {'name': 'Invert', 'type': 'bool',
                    'value': True, 'tip': "Invert image"},
                {'name': 'BgFileName', 'type': 'str', 'value': "hi"},
                {'name': 'BeginFrame', 'type': 'int', 'value': 0},
                {'name': 'EndFrame', 'type': 'int', 'value': 500},
                {'name': 'NumAverage', 'type': 'int', 'value': 10},
                #{'name': 'PLIFCode', 'type': 'text', 'value': ''},
                {'name': 'LoadFile', 'type': 'action'},
                {'name': 'LoadLVFile', 'type': 'action'},
                #{'name': 'Units + SI prefix', 'type': 'float', 'value': 1.2e-6, 'step': 1e-6, 'siPrefix': True, 'suffix': 'V'},
                #{'name': 'Limits (min=7;max=15)', 'type': 'int', 'value': 11, 'limits': (7, 15), 'default': -6},
                #{'name': 'DEC stepping', 'type': 'float', 'value': 1.2e6, 'dec': True, 'step': 1, 'siPrefix': True, 'suffix': 'Hz'},
            ]},
            {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
                {'name': 'Save', 'type': 'action'},
                {'name': 'Restore', 'type': 'action', 'children': [
                    {'name': 'Add missing items', 'type': 'bool', 'value': True},
                    {'name': 'Remove extra items', 'type': 'bool', 'value': True},
                ]},
            ]}
            #{'name': 'Extra Parameter Options', 'type': 'group', 'children': [
            #    {'name': 'Read-only', 'type': 'float', 'value': 1.2e6,
            #        'siPrefix': True, 'suffix': 'Hz', 'readonly': True},
            #    {'name': 'Renamable', 'type': 'float', 'value': 1.2e6,
            #        'siPrefix': True, 'suffix': 'Hz', 'renamable': True},
            #    {'name': 'Removable', 'type': 'float', 'value': 1.2e6,
            #        'siPrefix': True, 'suffix': 'Hz', 'removable': True},
            #]}
            # ComplexParameter(name='Custom parameter group (reciprocal values)'),
            # ScalableGroup(name="Expandable Parameter Group", children=[
            #     {'name': 'ScalableParam 1', 'type': 'str', 'value': "default param 1"},
            #     {'name': 'ScalableParam 2', 'type': 'str', 'value': "default param 2"},
            # ]),
            ]
            self.p = Parameter.create(name='params', type='group', children=params)
            self.t = ParameterTree()
            self.p.sigTreeStateChanged.connect(change)
            self.t.setParameters(self.p, showTop=False)
            self.t.setMaximumSize(400, 30000)

        def LVtimeLineChanged(self):
            (ind, time) = img.timeIndex(self)
            img.setCurrentIndex(ind)
        
        def AddLV():
            timeline,unitline,times,temps,currents,pressures,flows,msdata=readlvfile(self.p['PLIFFile', 'LVFileName'])
            #plot(times,temps,times,currents*1000)
            pens=['r','b','g','y','c']
            win = pg.GraphicsWindow(title="Measurement Parameters")
            win.resize(1000,600)
            win.setWindowTitle('Labview Reader')
            p1 = win.addPlot(title="Heating")
            p1.addLegend()
            p1.plot(times,temps,pen=(0,255,0),name='Temperature [°C]')
            p1.plot(times,currents*1000,pen=(255,0,0),name='Current [mA]')
            p1.setLabel('bottom',text='time',units='s')
            win.nextRow()
            p2 = win.addPlot(title="Flows")
            for i in range(0,5):
                p2.plot(times,flows[:,i],pen=pens[i])
            p2.setXLink(p1)
            win.nextRow()
            p3 = win.addPlot(title="MS")
            for i in range(0,5):
                p3.plot(times,np.log10(msdata[:,i]),pen=pens[i])
            p2.setXLink(p1)
            self.LVtimeLine = pg.InfiniteLine(0, movable=True)
            self.LVtimeLine2 = pg.InfiniteLine(0, movable=True)
            self.LVtimeLine3 = pg.InfiniteLine(0, movable=True)
            p1.addItem(self.LVtimeLine)
            p2.addItem(self.LVtimeLine2)
            p3.addItem(self.LVtimeLine3)
            self.LVtimeLine.sigPositionChanged.connect(LVtimeLineChanged)
            self.LVtimeLine2.sigPositionChanged.connect(LVtimeLineChanged)
            self.LVtimeLine3.sigPositionChanged.connect(LVtimeLineChanged)
            QtGui.QApplication.instance().exec_()

        def getNumFrames():
            file = sbf(self.p.child('PLIFFile', 'Path').value() +
                       '/'+self.p.child('PLIFFile', 'RealFileName').value())
            return file.numimgframes()

        def LoadPLIF():
            file = sbf(self.p.child('PLIFFile', 'Path').value() +
                       '/'+self.p.child('PLIFFile', 'RealFileName').value())
            # plifdata=file.readimg(self.p.child('PLIFFile','BeginFrame').value(),
            #    self.p.child('PLIFFile','EndFrame').value())
            if self.p['PLIFFile', 'ReadRaw']:
                plifdata = file.readraw(self.p.child('PLIFFile', 'BeginFrame').value(),
                                         self.p.child('PLIFFile', 'EndFrame').value())
            else:
                plifdata = plifimg.readimgav(file, self.p.child('PLIFFile', 'BeginFrame').value(),
                                         self.p.child('PLIFFile', 'EndFrame').value(), self.p['PLIFFile', 'NumAverage'])
            return plifdata

        def LoadProfile():
            file = sbf(self.p.child('PLIFFile', 'Path').value() +
                       '/'+self.p.child('PLIFFile', 'ProfileFileName').value())
            profiledata = plifimg.readimgav(file, 0, -1, -1)
            return profiledata

        def loadFile():
            plifdata = LoadPLIF()
            self.showData = plifdata
            if self.p['PLIFFile', 'ProfileDivision']:
                profiledata = LoadProfile()
                self.showData=np.true_divide(plifdata,profiledata)
                self.showData[self.showData < -10] = 20
                self.showData[self.showData > 20] = -10
            # img.setImage(np.squeeze(divided[:,:,800]))
            self.showData = np.swapaxes(self.showData, 0, 2)
            redrawSheet()

        def change(param, changes):
            for param, change, data in changes:
                childName = param.name()
                if childName == 'SheetTop':
                    redrawSheet()
                if childName == 'SheetBottom':
                    redrawSheet()
                if childName == 'Invert':
                    redrawSheet()
                if childName == 'LoadFile':
                    loadFile()
                if childName == 'LoadLVFile':
                    AddLV()
                if childName == 'Save':
                    save()
                if childName == 'Restore':
                    restore()
                if childName == 'ForceRedraw':
                    redrawSheet()
                if childName == 'Refresh':
                    hlayout.removeWidget(self.t)
                    initPanel(self)
                    hlayout.addWidget(self.t)

        def save():
            global state
            state = self.p.saveState()
            with open(path+'/'+self.p.child('PLIFFile', 'RealFileName').value()+'.val', 'wb') as f:
                pickle.dump(state, f)

        def restore():
            global state
            with open(path+'/'+self.p.child('PLIFFile', 'RealFileName').value()+'.val', 'rb') as f:
                state = pickle.load(f)
            #self.p.restoreState(state, addChildren=add, removeChildren=rem)
            self.p.restoreState(state, addChildren=False, removeChildren=False)

        def redrawSheet():
            top = self.p.child('Geometry', 'SheetTop').value()
            bottom = self.p.child('Geometry', 'SheetBottom').value()
            if self.p['PLIFFile', 'Invert']:
                invfactor = -1
            else:
                invfactor = 1
            if self.p.child('PLIFFile', 'EndFrame').value()==-1:
                endframe=getNumFrames()//2
            else:
                endframe=self.p.child('PLIFFile', 'EndFrame').value()
            img.setImage(invfactor*self.showData[:, :, top:bottom],
                         autoHistogramRange=False,
                         xvals=np.linspace(self.p.child('PLIFFile', 'BeginFrame').value()/10,
                                           endframe/10, self.showData.shape[0]))
            hist = img.getHistogramWidget()
            hist.setLevels(self.p['Geometry', 'ColorMapMin'], self.p['Geometry', 'ColorMapMax'])
        # self.p.child('Geometry','SheetTop').sigValueChanging.connect(redrawSheet)
        # self.p.child('Geometry','SheetBottom').sigValueChanging.connect(redrawSheet)
        initPanel(self)
        grid.addWidget(self.t,0,1)
        w = pg.TableWidget()
        grid.addWidget(w,1,1)
        # restore()


        self.show()


#%%
if __name__ == '__main__':
    app = QApplication(sys.argv)
    plifv = PLIFView()
    # sys.exit(app.exec_())
    app.exec_()


# https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
