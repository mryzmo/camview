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


def readlvfile2(filename):
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
    msdata=np.empty((filelen,6))
    heats=np.empty(filelen)
    steppers=np.empty(filelen)
    sor=np.empty(filelen)
    
    #time,temp,current
    for i in range(filelen):
        times[i]=columns[i][0]
        temps[i]=columns[i][1]
        currents[i]=columns[i][2]
        for j in range(3,7):
            pressures[i,j-3]=float(columns[i][j])
        for j in range(7,14):
            flows[i,j-7]=columns[i][j]
        if len(columns[i]) > 15:
            for j in range(14,20):
                msdata[i,j-12]=float(columns[i][j])
        heats[i]=columns[i][20]
        steppers[i]=columns[i][21]
        sor[i]=columns[i][21]
        
    return (timeline,unitline,times,temps,currents,pressures,flows,msdata,heats,steppers,sor)

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


def readlvfile2dict(filename):
    lvfile = open(filename)
    lvlines=lvfile.readlines()
    lvInfo={}
    lvInfo['timeline']=lvlines[0].rstrip()
    lvInfo['unitline']=lvlines[1]
    
    #remove top two lines
    lvlines.pop(0)
    lvlines.pop(0)
    
    filelen=len(lvlines)
    
    columns=[]
    
    for line in lvlines:
        line=line.strip()
        columns.append(line.split())
    
    #define rows
    lvInfo['times']=np.empty(filelen)
    lvInfo['temps']=np.empty(filelen)
    lvInfo['currents']=np.empty(filelen)
    lvInfo['pressures']=np.empty((filelen,4))
    lvInfo['flows']=np.empty((filelen,5))
    lvInfo['msdata']=np.empty((filelen,6))
    lvInfo['heats']=np.empty(filelen)
    lvInfo['steppers']=np.empty(filelen)
    
    #time,temp,current
    for i in range(filelen):
        lvInfo['times'][i]=columns[i][0]
        lvInfo['temps'][i]=columns[i][1]
        lvInfo['currents'][i]=columns[i][2]
        for j in range(3,7):
            lvInfo['pressures'][i,j-3]=float(columns[i][j])
        for j in range(7,12):
            lvInfo['flows'][i,j-7]=columns[i][j]
        if len(columns[i]) > 12:
            for j in range(12,18):
                lvInfo['msdata'][i,j-12]=float(columns[i][j])
        if len(columns[i]) > 19:
            lvInfo['heats'][i]=columns[i][18]
            lvInfo['steppers'][i]=columns[i][19]
        elif len(columns[i]) > 17:
            lvInfo['heats'][i]=columns[i][17]
            lvInfo['steppers'][i]=columns[i][18]
        
    return (lvInfo)