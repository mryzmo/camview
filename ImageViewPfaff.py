#!/usr/bin/env python3
import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.widgets.PlotWidget import *
from pyqtgraph.imageview import *
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from pyqtgraph.graphicsItems.GradientEditorItem import addGradientListToDocstring
from pyqtgraph.widgets.GraphicsView import GraphicsView
import matplotlib.cm
import collections
QAPP = None

class ImageViewPfaff(pg.ImageView):
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

    def buildMenu(self):
        super(ImageViewPfaff, self).buildMenu()

        self.trendAction = QtGui.QAction("Trend", self.menu)
        self.trendAction.setCheckable(True)
        self.trendAction.toggled.connect(self.trendToggled)
        self.menu.addAction(self.trendAction)

    def __init__(self,additionalCmaps=[], setColormap=None, **kargs):
        super(ImageViewPfaff, self).__init__(**kargs)
        self.trendroi=pg.LineROI([0, 60], [20, 80], width=5)
        self.trendroi.setZValue(30)
        self.view.addItem(self.trendroi)
        self.trendroi.hide()

        self.gradientEditorItem = self.ui.histogram.item.gradient

        self.activeCm = "grey"
        self.mplCmaps = {}

        if len(additionalCmaps) > 0:
            self.registerCmap(additionalCmaps)

        if setColormap is not None:
            self.gradientEditorItem.restoreState(setColormap)

    def registerCmap(self, cmapNames):
        """ Add matplotlib cmaps to the GradientEditors context menu"""
        self.gradientEditorItem.menu.addSeparator()
        savedLength = self.gradientEditorItem.length
        self.gradientEditorItem.length = 100

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
                self.gradientEditorItem.restoreState(self.mplCmaps[cmapName])
                grad = self.gradientEditorItem.getGradient()
                brush = QtGui.QBrush(grad)
                p.fillRect(QtCore.QRect(0, 0, 100, 15), brush)
                p.end()
                label = QtGui.QLabel()
                label.setPixmap(px)
                label.setContentsMargins(1, 1, 1, 1)
                act = QtGui.QWidgetAction(self.gradientEditorItem)
                act.setDefaultWidget(label)
                act.triggered.connect(self.cmapClicked)
                act.name = cmapName
                self.gradientEditorItem.menu.addAction(act)
        self.gradientEditorItem.length = savedLength
        


    def cmapClicked(self, b=None):
        """onclick handler for our custom entries in the GradientEditorItem's context menu"""
        act = self.sender()
        self.gradientEditorItem.restoreState(self.mplCmaps[act.name])
        self.activeCm = act.name

    def setColorMap(self, colormap):
        """Set the color map.

        ============= =========================================================
        **Arguments**
        colormap      (A ColorMap() instance) The ColorMap to use for coloring
                      images.
        ============= =========================================================
        """
        self.ui.histogram.gradient.setColorMap(colormap)

    def getProcessedImage(self):
        """Returns the image data after it has been processed by any normalization options in use.
        """
        if self.imageDisp is None:
            image = self.normalize(self.image)
            self.imageDisp = image
            self._imageLevels = self.quickMinMax(self.imageDisp)
            self.levelMin = 0
            self.levelMax = 2
            
        return self.imageDisp


    @addGradientListToDocstring()

    def setPredefinedGradient(self, name):
        """Set one of the gradients defined in :class:`GradientEditorItem <pyqtgraph.graphicsItems.GradientEditorItem>`.
        Currently available gradients are:
        """
        self.ui.histogram.gradient.loadPreset(name)

    def trendToggled(self):
        showRoiPlot = False
        if self.trendAction.isChecked():
            print('showing trendroi')
            showRoiPlot = True
            self.trendroi.show()
            #self.ui.roiPlot.show()
            self.ui.roiPlot.setMouseEnabled(True, True)
            self.ui.splitter.setSizes([self.height()*0.6, self.height()*0.4])
            self.roiCurve.show()
            self.roiChanged()
            self.ui.roiPlot.showAxis('left')
        else:
            self.trendroi.hide()
            self.ui.roiPlot.setMouseEnabled(False, False)
            self.roiCurve.hide()
            self.ui.roiPlot.hideAxis('left')

        if self.hasTimeAxis():
            showRoiPlot = True
            mn = self.tVals.min()
            mx = self.tVals.max()
            self.ui.roiPlot.setXRange(mn, mx, padding=0.01)
            self.timeLine.show()
            self.timeLine.setBounds([mn, mx])
            self.ui.roiPlot.show()
            if not self.trendAction.isChecked():
                self.ui.splitter.setSizes([self.height()-35, 35])
        else:
            self.timeLine.hide()
            #self.ui.roiPlot.hide()

        self.ui.roiPlot.setVisible(showRoiPlot)

    # def normalize(self, image):
    #         """
    #         Process *image* using the normalization options configured in the
    #         control panel.

    #         This can be repurposed to process any data through the same filter.
    #         """
    #         if self.ui.normOffRadio.isChecked():
    #             return image

    #         div = self.ui.normDivideRadio.isChecked()
    #         norm = image.view(np.ndarray).copy()
    #         #if div:
    #             #norm = ones(image.shape)
    #         #else:
    #             #norm = zeros(image.shape)
    #         if div:
    #             norm = norm.astype(np.float64)

    #         if self.ui.normTimeRangeCheck.isChecked() and image.ndim == 3:
    #             (sind, start) = self.timeIndex(self.normRgn.lines[0])
    #             (eind, end) = self.timeIndex(self.normRgn.lines[1])
    #             #print start, end, sind, eind
    #             #n = image[sind:eind+1].mean(axis=0)
    #             print('averaging time range...')
    #             if eind<sind: #swap order if it is wrong
    #                 sind,eind=eind,sind
    #             n = np.nanmean(image[sind:eind+1],axis=0)
    #             n.shape = (1,) + n.shape
    #             if div:
    #                 print('performing division...')
    #                 norm /= n
    #             else:
    #                 norm=norm.astype(np.float64)
    #                 norm -= n

    #         if self.ui.normFrameCheck.isChecked() and image.ndim == 3:
    #             n = image.mean(axis=1).mean(axis=1)
    #             n.shape = n.shape + (1, 1)
    #             if div:
    #                 norm /= n
    #             else:
    #                 norm -= n

    #         if self.ui.normROICheck.isChecked() and image.ndim == 3:
    #             n = self.normRoi.getArrayRegion(norm, self.imageItem, (1, 2)).mean(axis=1).mean(axis=1)
    #             n = n[:,np.newaxis,np.newaxis]
    #             #print start, end, sind, eind
    #             if div:
    #                 norm /= n
    #             else:
    #                 norm -= n

    #         return norm

    def quickMinMax(self, data):
        """
        Estimate the min/max values of *data* by subsampling.
        """
        while data.size > 1e6:
            ax = np.argmax(data.shape)
            sl = [slice(None)] * data.ndim
            sl[ax] = slice(None, None, 2)
            data = data[sl]
            if data.dtype=='float64':
                data[~np.isfinite(data)] = np.nan
        return np.nanmin(data), np.nanmax(data)

    # def updateNorm(self):
    #     if self.ui.normTimeRangeCheck.isChecked():
    #         self.normRgn.show()
    #     else:
    #         self.normRgn.hide()

    #     if self.ui.normROICheck.isChecked():
    #         self.normRoi.show()
    #     else:
    #         self.normRoi.hide()

    #     if not self.ui.normOffRadio.isChecked():
    #         self.imageDisp = None
    #         self.updateImage(autoHistogramRange=False)
    #         self.autoLevels()
    #         self.roiChanged()
    #         self.sigProcessingChanged.emit(self)


def mkQApp():
    if QtGui.QApplication.instance() is None:
        global QAPP
        QAPP = QtGui.QApplication([])

class ImageWindow(ImageViewPfaff):
    #sigClosed = QtCore.Signal(object)

    """
    (deprecated; use :class:`~pyqtgraph.ImageView` instead)
    """
    def __init__(self, *args, **kargs):
        mkQApp()
        ImageView.__init__(self)
        if 'title' in kargs:
            self.setWindowTitle(kargs['title'])
            del kargs['title']
        if len(args) > 0 or len(kargs) > 0:
            self.setImage(*args, **kargs)
        self.show()

    def closeEvent(self, event):
        ImageView.closeEvent(self, event)
        self.sigClosed.emit(self)


def cmapToColormap(cmap, nTicks=16):
    """
    Converts a Matplotlib cmap to pyqtgraphs colormaps. No dependency on matplotlib.
    Parameters:
    *cmap*: Cmap object. Imported from matplotlib.cm.*
    *nTicks*: Number of ticks to create when dict of functions is used. Otherwise unused.
    """

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
