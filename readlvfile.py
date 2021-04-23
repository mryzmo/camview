#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 16:11:07 2018

@author: sebastian
"""
import numpy as np
def readlvfile(filename):
    lvfile = open(filename)
    lvlines=lvfile.readlines()
    timeline=lvlines[0]
    unitline=lvlines[1]
    
    #remove top two lines
    lvlines.pop(0)
    lvlines.pop(0)
    
    filelen=len(lvlines)
    
    columns=[]
    
    for line in lvlines:
        line=line.strip()
        columns.append(line.split())
    
    #define rows
    
    times=np.empty(filelen)
    temps=np.empty(filelen)
    currents=np.empty(filelen)
    
    pressures=np.empty((filelen,4))
    flows=np.empty((filelen,5))
    msdata=np.empty((filelen,5))
    
    #time,temp,current
    for i in range(filelen):
        times[i]=columns[i][0]
        temps[i]=columns[i][1]
        currents[i]=columns[i][2]
        for j in range(3,7):
            pressures[i,j-3]=float(columns[i][j])
        for j in range(7,12):
            flows[i,j-7]=columns[i][j]
        if len(columns[i]) > 12:
            for j in range(12,17):
                msdata[i,j-12]=float(columns[i][j])
        
    return (timeline,unitline,times,temps,currents,pressures,flows,msdata)

def readmaestrofile(filename):
    maestrofile = open(filename)
    maestrolines=maestrofile.readlines()

    
    filelen=len(maestrolines)
    energies=np.empty(filelen)
        
    #for line in maestrolines:
    #    line=line.strip()
        
    for i in range(filelen):
        energies[i]=float(maestrolines[i])

    return (energies)