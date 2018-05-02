from pyqtgraph.graphicsItems.ImageItem import *
from pyqtgraph.graphicsItems.ROI import *
from pyqtgraph.graphicsItems.LinearRegionItem import *
from pyqtgraph.graphicsItems.InfiniteLine import *
from pyqtgraph.graphicsItems.ViewBox import *
from pyqtgraph.graphicsItems.GradientEditorItem import addGradientListToDocstring
from pyqtgraph import ptime as ptime
from pyqtgraph import debug as debug
from pyqtgraph.SignalProxy import SignalProxy
from pyqtgraph import getConfigOption

import pyqtgraph as pg
import collections
import matplotlib.cm
import numpy as np

from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QStyleFactory, \
QGridLayout, QListWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidgetItem

from PyQt5 import QtCore

try:
    from bottleneck import nanmin, nanmax
except ImportError:
    from numpy import nanmin, nanmax

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(726, 588)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = GraphicsView(self.layoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 2, 1)
        self.histogram = HistogramLUTWidget(self.layoutWidget)
        self.histogram.setObjectName("histogram")
        self.gridLayout.addWidget(self.histogram, 0, 1, 1, 2)
        self.roiBtn = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.roiBtn.sizePolicy().hasHeightForWidth())
        self.roiBtn.setSizePolicy(sizePolicy)
        self.roiBtn.setCheckable(True)
        self.roiBtn.setObjectName("roiBtn")
        self.gridLayout.addWidget(self.roiBtn, 1, 1, 1, 1)
        self.normBtn = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.normBtn.sizePolicy().hasHeightForWidth())
        self.normBtn.setSizePolicy(sizePolicy)
        self.normBtn.setCheckable(True)
        self.normBtn.setObjectName("normBtn")
        self.gridLayout.addWidget(self.normBtn, 1, 2, 1, 1)
        self.roigf=pg.GraphicsLayoutWidget(self.splitter)
        #self.roiPlot = PlotWidget(self.splitter)
        self.roiPlot = self.roigf.addPlot()
        self.roigf.nextRow()
        self.lreg = pg.LinearRegionItem([100,200])
        self.roiPlot.addItem(self.lreg)
        self.zoomplot=self.roigf.addPlot()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roiPlot.sizePolicy().hasHeightForWidth())
        #self.roiPlot.setSizePolicy(sizePolicy)
        #self.roiPlot.setMinimumSize(QtCore.QSize(0, 40))
        self.roiPlot.setObjectName("roiPlot")
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        self.normGroup = QtWidgets.QGroupBox(Form)
        self.normGroup.setObjectName("normGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.normGroup)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.normSubtractRadio = QtWidgets.QRadioButton(self.normGroup)
        self.normSubtractRadio.setObjectName("normSubtractRadio")
        self.gridLayout_2.addWidget(self.normSubtractRadio, 0, 2, 1, 1)
        self.normDivideRadio = QtWidgets.QRadioButton(self.normGroup)
        self.normDivideRadio.setChecked(False)
        self.normDivideRadio.setObjectName("normDivideRadio")
        self.gridLayout_2.addWidget(self.normDivideRadio, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.normROICheck = QtWidgets.QCheckBox(self.normGroup)
        self.normROICheck.setObjectName("normROICheck")
        self.gridLayout_2.addWidget(self.normROICheck, 1, 1, 1, 1)
        self.normXBlurSpin = QtWidgets.QDoubleSpinBox(self.normGroup)
        self.normXBlurSpin.setObjectName("normXBlurSpin")
        self.gridLayout_2.addWidget(self.normXBlurSpin, 2, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.normGroup)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.normGroup)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 3, 1, 1)
        self.normYBlurSpin = QtWidgets.QDoubleSpinBox(self.normGroup)
        self.normYBlurSpin.setObjectName("normYBlurSpin")
        self.gridLayout_2.addWidget(self.normYBlurSpin, 2, 4, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.normGroup)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 5, 1, 1)
        self.normOffRadio = QtWidgets.QRadioButton(self.normGroup)
        self.normOffRadio.setChecked(True)
        self.normOffRadio.setObjectName("normOffRadio")
        self.gridLayout_2.addWidget(self.normOffRadio, 0, 3, 1, 1)
        self.normTimeRangeCheck = QtWidgets.QCheckBox(self.normGroup)
        self.normTimeRangeCheck.setObjectName("normTimeRangeCheck")
        self.gridLayout_2.addWidget(self.normTimeRangeCheck, 1, 3, 1, 1)
        self.normFrameCheck = QtWidgets.QCheckBox(self.normGroup)
        self.normFrameCheck.setObjectName("normFrameCheck")
        self.gridLayout_2.addWidget(self.normFrameCheck, 1, 2, 1, 1)
        self.normTBlurSpin = QtWidgets.QDoubleSpinBox(self.normGroup)
        self.normTBlurSpin.setObjectName("normTBlurSpin")
        self.gridLayout_2.addWidget(self.normTBlurSpin, 2, 6, 1, 1)
        self.gridLayout_3.addWidget(self.normGroup, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.roiBtn.setText(_translate("Form", "ROI"))
        self.normBtn.setText(_translate("Form", "Norm"))
        self.normGroup.setTitle(_translate("Form", "Normalization"))
        self.normSubtractRadio.setText(_translate("Form", "Subtract"))
        self.normDivideRadio.setText(_translate("Form", "Divide"))
        self.label_5.setText(_translate("Form", "Operation:"))
        self.label_3.setText(_translate("Form", "Mean:"))
        self.label_4.setText(_translate("Form", "Blur:"))
        self.normROICheck.setText(_translate("Form", "ROI"))
        self.label_8.setText(_translate("Form", "X"))
        self.label_9.setText(_translate("Form", "Y"))
        self.label_10.setText(_translate("Form", "T"))
        self.normOffRadio.setText(_translate("Form", "Off"))
        self.normTimeRangeCheck.setText(_translate("Form", "Time range"))
        self.normFrameCheck.setText(_translate("Form", "Frame"))

from pyqtgraph.widgets.HistogramLUTWidget import HistogramLUTWidget
from pyqtgraph.widgets.PlotWidget import PlotWidget
from pyqtgraph.widgets.GraphicsView import GraphicsView

class PlotROI(ROI):
    def __init__(self, size):
        ROI.__init__(self, pos=[0,0], size=size) #, scaleSnap=True, translateSnap=True)
        self.addScaleHandle([1, 1], [0, 0])
        self.addRotateHandle([0, 0], [0.5, 0.5])



class ImageViewPLIF(QWidget):
    """
    Widget used for display and analysis of image data.
    Implements many features:

    * Displays 2D and 3D image data. For 3D data, a z-axis
      slider is displayed allowing the user to select which frame is displayed.
    * Displays histogram of image data with movable region defining the dark/light levels
    * Editable gradient provides a color lookup table
    * Frame slider may also be moved using left/right arrow keys as well as pgup, pgdn, home, and end.
    * Basic analysis features including:

        * ROI and embedded plot for measuring image values across frames
        * Image normalization / background subtraction

    Basic Usage::

        imv = pg.ImageView()
        imv.show()
        imv.setImage(data)

    **Keyboard interaction**

    * left/right arrows step forward/backward 1 frame when pressed,
      seek at 20fps when held.
    * up/down arrows seek at 100fps
    * pgup/pgdn seek at 1000fps
    * home/end seek immediately to the first/last frame
    * space begins playing frames. If time values (in seconds) are given
      for each frame, then playback is in realtime.
    """
    sigTimeChanged = QtCore.Signal(object, object)
    sigProcessingChanged = QtCore.Signal(object)


    def __init__(self, parent=None, name="ImageView", view=None, imageItem=None, *args):
        """
        By default, this class creates an :class:`ImageItem <pyqtgraph.ImageItem>` to display image data
        and a :class:`ViewBox <pyqtgraph.ViewBox>` to contain the ImageItem.

        ============= =========================================================
        **Arguments**
        parent        (QWidget) Specifies the parent widget to which
                      this ImageView will belong. If None, then the ImageView
                      is created with no parent.
        name          (str) The name used to register both the internal ViewBox
                      and the PlotItem used to display ROI data. See the *name*
                      argument to :func:`ViewBox.__init__()
                      <pyqtgraph.ViewBox.__init__>`.
        view          (ViewBox or PlotItem) If specified, this will be used
                      as the display area that contains the displayed image.
                      Any :class:`ViewBox <pyqtgraph.ViewBox>`,
                      :class:`PlotItem <pyqtgraph.PlotItem>`, or other
                      compatible object is acceptable.
        imageItem     (ImageItem) If specified, this object will be used to
                      display the image. Must be an instance of ImageItem
                      or other compatible object.
        ============= =========================================================

        Note: to display axis ticks inside the ImageView, instantiate it
        with a PlotItem instance as its view::

            pg.ImageView(view=pg.PlotItem())
        """
        super().__init__()
        self.levelMax = 4096
        self.levelMin = 0
        self.name = name
        self.image = None
        self.axes = {}
        self.imageDisp = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.scene = self.ui.graphicsView.scene()

        self.ignoreTimeLine = False

        if view is None:
            self.view = ViewBox()
        else:
            self.view = view
        self.ui.graphicsView.setCentralItem(self.view)
        self.view.setAspectLocked(True)
        self.view.invertY()

        if imageItem is None:
            self.imageItem = ImageItem()
        else:
            self.imageItem = imageItem
        self.view.addItem(self.imageItem)
        self.currentIndex = 0

        self.ui.histogram.setImageItem(self.imageItem)

        self.menu = None

        #self.ui.normGroup.hide()

        self.roi = PlotROI(10)
        self.roi.setZValue(20)
        self.view.addItem(self.roi)
        self.roi.hide()
        self.normRoi = PlotROI(10)
        self.normRoi.setPen('y')
        self.normRoi.setZValue(20)
        self.view.addItem(self.normRoi)
        self.normRoi.hide()
        self.roiCurve = self.ui.roiPlot.plot()
        self.zoomCurve=self.ui.zoomplot.plot()
        self.timeLine = InfiniteLine(0, movable=True)
        self.timeLine.setPen((255, 255, 0, 200))
        self.timeLine.setZValue(1)
        self.ui.roiPlot.addItem(self.timeLine)
        self.ui.splitter.setSizes([self.height()-35, 35])
        self.ui.roiPlot.hideAxis('left')

        self.ui.lreg.hide()
        #self.ui.zoomplot.hideAxis('left')

        self.keysPressed = {}
        self.playTimer = QtCore.QTimer()
        self.playRate = 0
        self.lastPlayTime = 0

        self.normRgn = LinearRegionItem()
        self.normRgn.setZValue(0)
        self.ui.roiPlot.addItem(self.normRgn)
        self.normRgn.hide()


        ## wrap functions from view box
        for fn in ['addItem', 'removeItem']:
            setattr(self, fn, getattr(self.view, fn))

        ## wrap functions from histogram
        for fn in ['setHistogramRange', 'autoHistogramRange', 'getLookupTable', 'getLevels']:
            setattr(self, fn, getattr(self.ui.histogram, fn))

        self.timeLine.sigPositionChanged.connect(self.timeLineChanged)
        self.ui.roiBtn.clicked.connect(self.roiClicked)
        self.roi.sigRegionChanged.connect(self.roiChanged)
        #self.ui.normBtn.toggled.connect(self.normToggled)
        #self.ui.menuBtn.clicked.connect(self.menuClicked)
        self.ui.normDivideRadio.clicked.connect(self.normRadioChanged)
        self.ui.normSubtractRadio.clicked.connect(self.normRadioChanged)
        self.ui.normOffRadio.clicked.connect(self.normRadioChanged)
        self.ui.normROICheck.clicked.connect(self.updateNorm)
        self.ui.normFrameCheck.clicked.connect(self.updateNorm)
        self.ui.normTimeRangeCheck.clicked.connect(self.updateNorm)
        self.playTimer.timeout.connect(self.timeout)

        self.normProxy = SignalProxy(self.normRgn.sigRegionChanged, slot=self.updateNorm)
        self.normRoi.sigRegionChangeFinished.connect(self.updateNorm)

        self.ui.roiPlot.registerPlot(self.name + '_ROI')
        self.view.register(self.name)

        self.noRepeatKeys = [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left, QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]

        self.roiClicked() ## initialize roi plot to correct shape / visibility


    def setImage(self, img, autoRange=True, autoLevels=True, levels=None, axes=None, xvals=None, pos=None, scale=None, transform=None, autoHistogramRange=True):
        """
        Set the image to be displayed in the widget.

        ================== ===========================================================================
        **Arguments:**
        img                (numpy array) the image to be displayed. See :func:`ImageItem.setImage` and
                           *notes* below.
        xvals              (numpy array) 1D array of z-axis values corresponding to the third axis
                           in a 3D image. For video, this array should contain the time of each frame.
        autoRange          (bool) whether to scale/pan the view to fit the image.
        autoLevels         (bool) whether to update the white/black levels to fit the image.
        levels             (min, max); the white and black level values to use.
        axes               Dictionary indicating the interpretation for each axis.
                           This is only needed to override the default guess. Format is::

                               {'t':0, 'x':1, 'y':2, 'c':3};

        pos                Change the position of the displayed image
        scale              Change the scale of the displayed image
        transform          Set the transform of the displayed image. This option overrides *pos*
                           and *scale*.
        autoHistogramRange If True, the histogram y-range is automatically scaled to fit the
                           image data.
        ================== ===========================================================================

        **Notes:**

        For backward compatibility, image data is assumed to be in column-major order (column, row).
        However, most image data is stored in row-major order (row, column) and will need to be
        transposed before calling setImage()::

            imageview.setImage(imagedata.T)

        This requirement can be changed by the ``imageAxisOrder``
        :ref:`global configuration option <apiref_config>`.

        """
        profiler = debug.Profiler()

        if hasattr(img, 'implements') and img.implements('MetaArray'):
            img = img.asarray()

        if not isinstance(img, np.ndarray):
            required = ['dtype', 'max', 'min', 'ndim', 'shape', 'size']
            if not all([hasattr(img, attr) for attr in required]):
                raise TypeError("Image must be NumPy array or any object "
                                "that provides compatible attributes/methods:\n"
                                "  %s" % str(required))

        self.image = img
        self.imageDisp = None

        profiler()

        if axes is None:
            x,y = (0, 1) if self.imageItem.axisOrder == 'col-major' else (1, 0)

            if img.ndim == 2:
                self.axes = {'t': None, 'x': x, 'y': y, 'c': None}
            elif img.ndim == 3:
                # Ambiguous case; make a guess
                if img.shape[2] <= 4:
                    self.axes = {'t': None, 'x': x, 'y': y, 'c': 2}
                else:
                    self.axes = {'t': 0, 'x': x+1, 'y': y+1, 'c': None}
            elif img.ndim == 4:
                # Even more ambiguous; just assume the default
                self.axes = {'t': 0, 'x': x+1, 'y': y+1, 'c': 3}
            else:
                raise Exception("Can not interpret image with dimensions %s" % (str(img.shape)))
        elif isinstance(axes, dict):
            self.axes = axes.copy()
        elif isinstance(axes, list) or isinstance(axes, tuple):
            self.axes = {}
            for i in range(len(axes)):
                self.axes[axes[i]] = i
        else:
            raise Exception("Can not interpret axis specification %s. Must be like {'t': 2, 'x': 0, 'y': 1} or ('t', 'x', 'y', 'c')" % (str(axes)))

        for x in ['t', 'x', 'y', 'c']:
            self.axes[x] = self.axes.get(x, None)
        axes = self.axes

        if xvals is not None:
            self.tVals = xvals
        elif axes['t'] is not None:
            if hasattr(img, 'xvals'):
                try:
                    self.tVals = img.xvals(axes['t'])
                except:
                    self.tVals = np.arange(img.shape[axes['t']])
            else:
                self.tVals = np.arange(img.shape[axes['t']])

        profiler()

        self.currentIndex = 0
        self.updateImage(autoHistogramRange=autoHistogramRange)
        if levels is None and autoLevels:
            self.autoLevels()
        if levels is not None:  ## this does nothing since getProcessedImage sets these values again.
            self.setLevels(*levels)

        if self.ui.roiBtn.isChecked():
            self.roiChanged()

        profiler()

        if self.axes['t'] is not None:
            #self.ui.roiPlot.show()
            self.ui.roiPlot.setXRange(self.tVals.min(), self.tVals.max())
            self.timeLine.setValue(0)
            #self.ui.roiPlot.setMouseEnabled(False, False)
            if len(self.tVals) > 1:
                start = self.tVals.min()
                stop = self.tVals.max() + abs(self.tVals[-1] - self.tVals[0]) * 0.02
            elif len(self.tVals) == 1:
                start = self.tVals[0] - 0.5
                stop = self.tVals[0] + 0.5
            else:
                start = 0
                stop = 1
            for s in [self.timeLine, self.normRgn]:
                s.setBounds([start, stop])
        #else:
            #self.ui.roiPlot.hide()
        profiler()

        self.imageItem.resetTransform()
        if scale is not None:
            self.imageItem.scale(*scale)
        if pos is not None:
            self.imageItem.setPos(*pos)
        if transform is not None:
            self.imageItem.setTransform(transform)

        profiler()

        if autoRange:
            self.autoRange()
        self.roiClicked()

        profiler()


    def clear(self):
        self.image = None
        self.imageItem.clear()


    def play(self, rate):
        """Begin automatically stepping frames forward at the given rate (in fps).
        This can also be accessed by pressing the spacebar."""
        #print "play:", rate
        self.playRate = rate
        if rate == 0:
            self.playTimer.stop()
            return

        self.lastPlayTime = ptime.time()
        if not self.playTimer.isActive():
            self.playTimer.start(16)



    def autoLevels(self):
        """Set the min/max intensity levels automatically to match the image data."""
        self.setLevels(self.levelMin, self.levelMax)



    def setLevels(self, min, max):
        """Set the min/max (bright and dark) levels."""
        self.ui.histogram.setLevels(min, max)



    def autoRange(self):
        """Auto scale and pan the view around the image such that the image fills the view."""
        image = self.getProcessedImage()
        self.view.autoRange()



    def getProcessedImage(self):
        """Returns the image data after it has been processed by any normalization options in use.
        This method also sets the attributes self.levelMin and self.levelMax
        to indicate the range of data in the image."""
        if self.imageDisp is None:
            image = self.normalize(self.image)
            self.imageDisp = image
            self.levelMin, self.levelMax = list(map(float, self.quickMinMax(self.imageDisp)))

        return self.imageDisp



    def close(self):
        """Closes the widget nicely, making sure to clear the graphics scene and release memory."""
        self.ui.roiPlot.close()
        self.ui.graphicsView.close()
        self.scene.clear()
        del self.image
        del self.imageDisp
        super(ImageView, self).close()
        self.setParent(None)


    def keyPressEvent(self, ev):
        #print ev.key()
        if ev.key() == QtCore.Qt.Key_Space:
            if self.playRate == 0:
                fps = (self.getProcessedImage().shape[0]-1) / (self.tVals[-1] - self.tVals[0])
                self.play(fps)
                #print fps
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

    def timeout(self):
        now = ptime.time()
        dt = now - self.lastPlayTime
        if dt < 0:
            return
        n = int(self.playRate * dt)
        if n != 0:
            self.lastPlayTime += (float(n)/self.playRate)
            if self.currentIndex+n > self.image.shape[0]:
                self.play(0)
            self.jumpFrames(n)


    def setCurrentIndex(self, ind):
        """Set the currently displayed frame index."""
        self.currentIndex = np.clip(ind, 0, self.getProcessedImage().shape[self.axes['t']]-1)
        self.updateImage()
        self.ignoreTimeLine = True
        self.timeLine.setValue(self.tVals[self.currentIndex])
        self.ignoreTimeLine = False



    def jumpFrames(self, n):
        """Move video frame ahead n frames (may be negative)"""
        if self.axes['t'] is not None:
            self.setCurrentIndex(self.currentIndex + n)


    def normRadioChanged(self):
        self.imageDisp = None
        self.updateImage()
        self.autoLevels()
        self.roiChanged()
        self.sigProcessingChanged.emit(self)

    def updateNorm(self):
        if self.ui.normTimeRangeCheck.isChecked():
            self.normRgn.show()
        else:
            self.normRgn.hide()

        if self.ui.normROICheck.isChecked():
            self.normRoi.show()
        else:
            self.normRoi.hide()

        if not self.ui.normOffRadio.isChecked():
            self.imageDisp = None
            self.updateImage()
            self.autoLevels()
            self.roiChanged()
            self.sigProcessingChanged.emit(self)

    def normToggled(self, b):
        self.ui.normGroup.setVisible(b)
        self.normRoi.setVisible(b and self.ui.normROICheck.isChecked())
        self.normRgn.setVisible(b and self.ui.normTimeRangeCheck.isChecked())

    def hasTimeAxis(self):
        return 't' in self.axes and self.axes['t'] is not None

    def roiClicked(self):
        showRoiPlot = False
        if self.ui.roiBtn.isChecked():
            showRoiPlot = True
            self.roi.show()
            #self.ui.roiPlot.show()
            self.ui.roiPlot.setMouseEnabled(True, True)
            self.ui.splitter.setSizes([self.height()*0.6, self.height()*0.4])
            self.roiCurve.show()
            self.roiChanged()
            self.ui.roiPlot.showAxis('left')
            self.ui.zoomplot.show()
            self.ui.lreg.show()
        else:
            self.roi.hide()
            self.ui.roiPlot.setMouseEnabled(False, False)
            self.roiCurve.hide()
            self.ui.lreg.hide()
            self.ui.zoomplot.hide()
            self.ui.roiPlot.hideAxis('left')

        if self.hasTimeAxis():
            showRoiPlot = True
            mn = self.tVals.min()
            mx = self.tVals.max()
            self.ui.roiPlot.setXRange(mn, mx, padding=0.01)
            self.timeLine.show()
            self.timeLine.setBounds([mn, mx])
            self.ui.roiPlot.show()
            if not self.ui.roiBtn.isChecked():
                self.ui.splitter.setSizes([self.height()-35, 35])
        else:
            self.timeLine.hide()
            #self.ui.roiPlot.hide()

        self.ui.roiPlot.setVisible(showRoiPlot)

    def roiChanged(self):
        if self.image is None:
            return

        image = self.getProcessedImage()
        if image.ndim == 2:
            axes = (0, 1)
        elif image.ndim == 3:
            axes = (1, 2)
        else:
            return

        data, coords = self.roi.getArrayRegion(image.view(np.ndarray), self.imageItem, axes, returnMappedCoords=True)
        if data is not None:
            while data.ndim > 1:
                data = data.mean(axis=1)
            if image.ndim == 3:
                self.roiCurve.setData(y=data, x=self.tVals)
                self.zoomCurve.setData(y=data, x=self.tVals)
            else:
                while coords.ndim > 2:
                    coords = coords[:,:,0]
                coords = coords - coords[:,0,np.newaxis]
                xvals = (coords**2).sum(axis=0) ** 0.5
                self.roiCurve.setData(y=data, x=xvals)
        def updatePlot():
            self.ui.zoomplot.setXRange(*self.ui.lreg.getRegion(), padding=0)
        def updateRegion():
            self.ui.lreg.setRegion(self.ui.zoomplot.getViewBox().viewRange()[0])
        self.ui.lreg.sigRegionChanged.connect(updatePlot)
        self.ui.zoomplot.sigXRangeChanged.connect(updateRegion)
        #updatePlot()

    def quickMinMax(self, data):
        """
        Estimate the min/max values of *data* by subsampling.
        """
        while data.size > 1e6:
            ax = np.argmax(data.shape)
            sl = [slice(None)] * data.ndim
            sl[ax] = slice(None, None, 2)
            data = data[sl]
        return nanmin(data), nanmax(data)



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
            n = image[sind:eind+1].mean(axis=0)
            n.shape = (1,) + n.shape
            if div:
                norm /= n
            else:
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


    def timeLineChanged(self):
        #(ind, time) = self.timeIndex(self.ui.timeSlider)
        if self.ignoreTimeLine:
            return
        self.play(0)
        (ind, time) = self.timeIndex(self.timeLine)
        if ind != self.currentIndex:
            self.currentIndex = ind
            self.updateImage()
        #self.timeLine.setPos(time)
        #self.emit(QtCore.SIGNAL('timeChanged'), ind, time)
        self.sigTimeChanged.emit(ind, time)

    def updateImage(self, autoHistogramRange=True):
        ## Redraw image on screen
        if self.image is None:
            return

        image = self.getProcessedImage()

        if autoHistogramRange:
            self.ui.histogram.setHistogramRange(self.levelMin, self.levelMax)

        # Transpose image into order expected by ImageItem
        if self.imageItem.axisOrder == 'col-major':
            axorder = ['t', 'x', 'y', 'c']
        else:
            axorder = ['t', 'y', 'x', 'c']
        axorder = [self.axes[ax] for ax in axorder if self.axes[ax] is not None]
        image = image.transpose(axorder)

        # Select time index
        if self.axes['t'] is not None:
            self.ui.roiPlot.show()
            image = image[self.currentIndex]

        self.imageItem.updateImage(image)


    def timeIndex(self, slider):
        ## Return the time and frame index indicated by a slider
        if self.image is None:
            return (0,0)

        t = slider.value()

        xv = self.tVals
        if xv is None:
            ind = int(t)
        else:
            if len(xv) < 2:
                return (0,0)
            totTime = xv[-1] + (xv[-1]-xv[-2])
            inds = np.argwhere(xv < t)
            if len(inds) < 1:
                return (0,t)
            ind = inds[-1,0]
        return ind, t


    def getView(self):
        """Return the ViewBox (or other compatible object) which displays the ImageItem"""
        return self.view



    def getImageItem(self):
        """Return the ImageItem for this ImageView."""
        return self.imageItem



    def getRoiPlot(self):
        """Return the ROI PlotWidget for this ImageView"""
        return self.ui.roiPlot



    def getHistogramWidget(self):
        """Return the HistogramLUTWidget for this ImageView"""
        return self.ui.histogram



    def export(self, fileName):
        """
        Export data from the ImageView to a file, or to a stack of files if
        the data is 3D. Saving an image stack will result in index numbers
        being added to the file name. Images are saved as they would appear
        onscreen, with levels and lookup table applied.
        """
        img = self.getProcessedImage()
        if self.hasTimeAxis():
            base, ext = os.path.splitext(fileName)
            fmt = "%%s%%0%dd%%s" % int(np.log10(img.shape[0])+1)
            for i in range(img.shape[0]):
                self.imageItem.setImage(img[i], autoLevels=False)
                self.imageItem.save(fmt % (base, i, ext))
            self.updateImage()
        else:
            self.imageItem.save(fileName)


    def exportClicked(self):
        fileName = QtGui.QFileDialog.getSaveFileName()
        if fileName == '':
            return
        self.export(fileName)

    def buildMenu(self):
        self.menu = QtGui.QMenu()
        self.normAction = QtGui.QAction("Normalization", self.menu)
        self.normAction.setCheckable(True)
        self.normAction.toggled.connect(self.normToggled)
        self.menu.addAction(self.normAction)
        self.exportAction = QtGui.QAction("Export", self.menu)
        self.exportAction.triggered.connect(self.exportClicked)
        self.menu.addAction(self.exportAction)

    def menuClicked(self):
        if self.menu is None:
            self.buildMenu()
        self.menu.popup(QtGui.QCursor.pos())



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


class MplCmapImageViewPLIF(ImageViewPLIF):
    def __init__(self, additionalCmaps=[], setColormap=None, **kargs):
        super(MplCmapImageViewPLIF, self).__init__(**kargs)

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


    @addGradientListToDocstring()

    def setPredefinedGradient(self, name):
        """Set one of the gradients defined in :class:`GradientEditorItem <pyqtgraph.graphicsItems.GradientEditorItem>`.
        Currently available gradients are:
        """
        self.ui.histogram.gradient.loadPreset(name)
