#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:34:28 2018

@author: sebastian
"""
from scipy.interpolate import interp1d
from readimg import sbf,plifimg,sif
import numpy as np

def makeprofilefunc(currents,files):
    """Creates a function that returns profiles for a given set of currents."""
    #assume all profiles have the same dimensions
    dimensions=files[0].getimgdata()
    profiles=np.zeros((len(files),dimensions[0],dimensions[1]))
    
    #read every profile
    for i,f in enumerate(files):
        profiles[i,:,:]=np.squeeze(plifimg.readimgav(f,0,-1,-1))
    
    interpfunc=interp1d(currents,profiles,axis=0)
    return interpfunc
    
#profilefunc=makeprofilefunc(
#        currents=(.6,1.5),
#        files=(sbf('20180910_profile7.img'),sbf('20180910_profile8.img')))