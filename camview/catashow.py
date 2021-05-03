#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 11:42:36 2018

@author: sebastian
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np;
from mpl_toolkits.axes_grid1 import make_axes_locatable
#top bottom, left right
def catashow(image,cataloc,vmin=0, vmax=1,cmap='plasma',crop=[0,0,0,0],
             catamm=6,mmaxis=True,colorbar=True,giveback=False,curved=None):
    dim=np.shape(image)
    
    #default should not crop at all
    if crop[1]==0:
        crop[1]=dim[0]
    if crop[3]==0:
        crop[3]=dim[1]
   

    imout=plt.imshow(image,vmin=vmin,vmax=vmax,cmap=cmap,interpolation='none')

    scale=(cataloc[1]-cataloc[0])/catamm
    
    catathickness=int(1*scale)
    
    #put in rects, set limits    
    catarect=patches.Rectangle((cataloc[0],crop[1]-1),cataloc[1]-cataloc[0],catathickness,fc='w')
    bottomrect=patches.Rectangle((crop[2],crop[1]-1),crop[3]-crop[2],catathickness,fc='k')
    plt.gca().add_patch(bottomrect)
    plt.gca().add_patch(catarect)
    if (curved != None):
        cataellipse=patches.Ellipse((cataloc[0]+(cataloc[1]-cataloc[0])/2,crop[1]),cataloc[1]-cataloc[0],curved,fc='w')
        plt.gca().add_patch(cataellipse)
    
    if mmaxis:
        hcatapxsize=(cataloc[1]-cataloc[0])/2
        catacenter=int((cataloc[0]+cataloc[1])/2)
        labelpositions=range(catacenter+int(-2*hcatapxsize),catacenter+int(3*hcatapxsize),int(hcatapxsize))
        plt.xticks(labelpositions,(-catamm,-catamm/2,0,catamm/2,catamm))
        plt.xlabel('$x$ [mm]')
        plt.ylabel('$h$ [mm]')
        plt.yticks((range(crop[1]-1,crop[0]-1,-int(scale))),range(0,10,1))
    
    plt.ylim((crop[1]+catathickness-1,crop[0]))
    plt.xlim((crop[2],crop[3]-1))

    if colorbar:
        #add colorbar to a new axis to the rihgt
        ax = plt.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(cax=cax)
        plt.sca(ax)
    
    if giveback:
        return imout,(bottomrect,catarect)
#catashow(np.polyval(calibfit,np.mean(divplif[1000:1400,100:200,:],axis=0)),
#         vmin=100,vmax=230,cmap='plasma',crop=[20,0,40,230],cataloc=(97,175))


    
