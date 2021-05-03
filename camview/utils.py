#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:30:14 2018

@author: sebastian
"""
def nm2invcm(nmin):
    return 1.0/nmin*1e7

def invcm2nm(invcmin):
    return 1.0/invcmin*1e7

def makeIRCamFunc(roomtemp=300): #this functions takes in a fraction of IR Cam intensity at HT/RT
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.signal
    from scipy.interpolate import interp1d

    lambdaspace=np.linspace(3000e-9,5000e-9,2000)

    theconstants=6.62607004e-34*3e8/lambdaspace/1.38064852e-23 #hc/lambda*Kb

    transmissionnr=.87
    transmission=np.zeros(2000)
    transmission[1260-70:1260+70]=transmissionnr

    intensities=np.zeros(1000)
    templist = range(200,1000)

    #roomtemp=300

    roomtempint=np.mean((1/lambdaspace**5/np.exp(theconstants/roomtemp)-1)*transmission)
    #plt.figure()

    for simtemps in templist: #0 K to 1000 K
        simintensity=(1/lambdaspace**5/np.exp(theconstants/simtemps)-1)
        intensities[simtemps]=np.mean(simintensity*transmission)

    #print(roomtempint)
    measuredintfrac=intensities/roomtempint
    #plt.figure()    

    #plt.xlim(0,10)
    #plt.ylim(200,400)
    return interp1d(measuredintfrac[200:1000],templist)

import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1

def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)

def microshow(imdata,scale=1,colorbar=True,**kwargs):
    """Plot microscopy image"""
    from matplotlib_scalebar.scalebar import ScaleBar
    im=plt.imshow(imdata,**kwargs)
    plt.yticks(())
    plt.xticks(())
    scalebar = ScaleBar(scale,location='lower right',box_alpha=0.7) # 1 pixel = 0.2 meter
    plt.gca().add_artist(scalebar)
    if colorbar:
        cbar=add_colorbar(im)
        return im, cbar
    else:
        return None,im