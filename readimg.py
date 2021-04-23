#!/usr/bin/env python3
import imageio
import numpy as np
from scanf import scanf
<<<<<<< HEAD
import time
import os.path
#from readimg import sbf, plifimg

class sif: #sif files made by the andor software. WIP, ask Sebastian how fucked up the Andor file format is....
    """
    A class that reads the contents and metadata of an Andor .sif file. Compatible with images as well as spectra.
    Exports data as numpy array or xarray.DataArray.
    Example: SIFFile('my_spectrum.sif').read_all()
    In addition to the raw data, SIFFile objects provide a number of meta data variables:
    :ivar x_axis: the horizontal axis (can be pixel numbers or wavelength in nm)
    :ivar original_filename: the original file name of the .sif f ile
    :ivar date: the date the file was recorded
    :ivar model: camera model
    :ivar temperature: sensor temperature in degrees Celsius
    :ivar exposuretime: exposure time in seconds
    :ivar cycletime: cycle time in seconds
    :ivar accumulations: number of accumulations
    :ivar readout: pixel readout rate in MHz
    :ivar xres: horizontal resolution
    :ivar yres: vertical resolution
    :ivar width: image width
    :ivar height: image height
    :ivar xbin: horizontal binning
    :ivar ybin: vertical binning
    :ivar gain: EM gain level
    :ivar vertical_shift_speed: vertical shift speed
    :ivar pre_amp_gain: pre-amplifier gain
    :ivar stacksize: number of frames
    :ivar filesize: size of the file in bytes
    :ivar m_offset: offset in the .sif file to the actual data
    
    #some code from https://github.com/lightingghost/sifreader/blob/master/sifreader/sifreader.py
    #self.f=open(self.filename,'rb')
    #Pixel number6
    # Counts12
    # Pixel number65541 1 2160 2560 1 12000 1 1239264000 103272
    # 65538 730 1780 1722 845 3 3 0
    """
    def __init__(self, filepath, verbose=False,offsetshift=0):
        self.filepath = filepath
        self.filename = filepath
        self._read_header(filepath, verbose, offsetshift)

    def __repr__(self):
        info = (('Original Filename', self.original_filename),
                ('Date', self.date),
                ('Camera Model', self.model),
                ('Temperature (deg.C)', '{:f}'.format(self.temperature)),
                ('Exposure Time', '{:f}'.format(self.exposuretime)),
                ('Cycle Time', '{:f}'.format(self.cycletime)),
                ('Number of accumulations', '{:d}'.format(self.accumulations)),
                ('Pixel Readout Rate (MHz)', '{:f}'.format(self.readout)),
                ("Horizontal Camera Resolution", '{:d}'.format(self.xres)),
                ("Vertical Camera Resolution", '{:d}'.format(self.yres)),
                ("Image width", '{:d}'.format(self.width)),
                ("Image Height", '{:d}'.format(self.height)),
                ("Horizontal Binning", '{:d}'.format(self.xbin)),
                ("Vertical Binning", '{:d}'.format(self.ybin)),
                ("EM Gain level", '{:f}'.format(self.gain)),
                ("Vertical Shift Speed", '{:f}'.format(self.vertical_shift_speed)),
                ("Pre-Amplifier Gain", '{:f}'.format(self.pre_amp_gain)),
                ("Stacksize", '{:d}'.format(self.stacksize)),
                ("Offset to Image Data", '{:f}'.format(self.m_offset)))
        desc_len = max([len(d) for d in list(zip(*info))[0]]) + 3
        res = ''
        for description, value in info:
            res += ('{:' + str(desc_len) + '}{}\n').format(description + ': ', value)

        res = super().__repr__() + '\n' + res
        return res

    def _read_header(self, filepath, verbose, offsetshift=0):
        f = open(filepath, 'rb')
        headerlen = 50
        spool = 0
        i = 0
        pxnumline=0
        while i < headerlen + spool:
            line = f.readline().strip()
            if verbose:
                print(str(i)+':'+str(f.tell())+': '+str(line))
            if i == 0:
                if line != b'Andor Technology Multi-Channel File':
                    f.close()
                    raise Exception('{} is not an Andor SIF file'.format(filepath))
            elif i == 2:
                tokens = line.split()
                self.temperature = float(tokens[5])
                self.date = time.strftime('%c', time.localtime(float(tokens[4])))
                self.exposuretime = float(tokens[12])
                self.cycletime = float(tokens[13])
                self.accumulations = int(tokens[15])
                self.readout = 1 / float(tokens[18]) / 1e6
                self.gain = float(tokens[21])
                self.vertical_shift_speed = float(tokens[41])
                self.pre_amp_gain = float(tokens[43])
            elif i == 3:
                self.model = line.decode('utf-8')
            elif i == 5:
                self.original_filename = line.decode('utf-8')
            elif i == 7:
                tokens = line.split()
                if len(tokens) >= 1 and tokens[0] == 'Spooled':
                    spool = 1
            elif line.startswith(b'Pixel number') and pxnumline==0:
                pxnumline=i
            elif i == pxnumline+2 and pxnumline>0:
                tokens=scanf('Pixel number%d %d %d %d %d %d %d %d %d', s=str(line), collapseWhitespace=False)
                self.yres = int(tokens[2])
                self.xres = int(tokens[3])
                self.stacksize = int(tokens[5])
            elif i == pxnumline+3 and pxnumline>0:
                tokens = scanf('%d %d %d %d %d %d %d', s=str(line), collapseWhitespace=False)
                if len(tokens) < 7:
                    raise Exception("Not able to read Image dimensions.")
                self.left = int(tokens[1])
                self.top = int(tokens[2])
                self.right = int(tokens[3])
                self.bottom = int(tokens[4])
                self.xbin = int(tokens[5])
                self.ybin = int(tokens[6])
            elif i>=pxnumline+4 and pxnumline > 0:# and str(line)==b'0':
                #'End of header, looking for start of data!'
                for i in range(self.stacksize):
                    f.readline()
                #'Header end: '+str(f.tell()))
                self.m_offset = f.tell()+offsetshift
                break;
            i += 1

        f.close()

        width = self.right - self.left + 1
        mod = width % self.xbin
        self.width = int((width - mod) / self.ybin)
        height = self.top - self.bottom + 1
        mod = height % self.ybin
        self.height = int((height - mod) / self.xbin)
=======
import os.path
#from readimg import sbf, plifimg

class sif: #sif files made by the andor software. WIP
    def __init__(self, filename):
        self.filename = filename

        #self.f=open(self.filename,'rb')
        #Pixel number6
        # Counts12
        # Pixel number65541 1 2160 2560 1 12000 1 1239264000 103272
        # 65538 730 1780 1722 845 3 3 0
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5

    def imageType(self):
        return 'AndorSIF'

    def getimgdata(self): #returns width,height
        line=''
        self.f=open(self.filename,mode='r',errors='ignore')
        while True:
            line=self.f.readline()
            if line.startswith('Pixel number'):
                line=self.f.readline()
                line=self.f.readline()
                line=self.f.readline()
                out=scanf('%d %d %d %d %d %d %d', s=line, collapseWhitespace=False)
                leftPixel = out[1];
                topPixel = out[2];
                rightPixel = out[3];
                bottomPixel = out[4];
                vBin = out[6]
                hBin=vBin
                width = (rightPixel - leftPixel + 1)/hBin
                height = (topPixel - bottomPixel + 1)/vBin;
                self.f.close()
                return (int(width),int(height))
        self.f.close()
        return -1

    def numimgframes(self):
<<<<<<< HEAD
        return self.stacksize

    def readimg(self,startimg=0,stopimg=-1,offset=0):
        imageDims=self.getimgdata()
        NumFrames=self.numimgframes()
        if stopimg<0:
            stopimg=NumFrames
        self.f=open(self.filename,'rb')
        self.f.seek(4*startimg*imageDims[0]*imageDims[1]+self.m_offset+offset,0) #zyla file
=======
        line=''
        self.f=open(self.filename,mode='r',errors='ignore')
        while True:
            line=self.f.readline()
            if line.startswith('Pixel number'):
                line=self.f.readline()
                line=self.f.readline()
                out=scanf('Pixel number%d %d %d %d %d %d %d %d %d', s=line, collapseWhitespace=False)
                self.f.close()
                return out[int(5)]
        self.f.close()
        return -1

    def findoffsetbyte(self):
        imageDims=self.getimgdata()
        NumFrames=self.numimgframes()
        self.f=open(self.filename,'rb')
        for offset in {0,1,2,3}:
            self.f.seek(2*0*imageDims[0]*imageDims[1]+2832+1*32*NumFrames,0)
            self.f.seek(offset,1)
            imageraw=self.f.read(4*imageDims[0]*imageDims[1])
            image=np.frombuffer(imageraw,dtype='f')
            testimage=np.reshape(image,(imageDims[1],imageDims[0]))
            testmean=np.mean(np.mean(testimage))
            if testmean < 66000 and testmean > 100:
                return offset
        return 0

    def readimg(self,startimg=0,stopimg=-1):
        #num_bytes_to_skip_for_curr_frame = 4 * ((currentFrameNumber(1)-1) * info.pixelPerFrame);
        #fseek(f, num_bytes_to_skip_for_curr_frame+1*2832+1*32*NumFrames, 'bof');
        imageDims=self.getimgdata()
        NumFrames=self.numimgframes()
        OffsetByte=self.findoffsetbyte()
        if stopimg<0:
            stopimg=NumFrames
        self.f=open(self.filename,'rb')
        self.f.seek(4*startimg*imageDims[0]*imageDims[1]+2832+1*32*NumFrames,0) #zyla file
        #self.f.seek(4*startimg*imageDims[0]*imageDims[1]+22000+0*32*NumFrames,0) #istar file
        #figure out the "weird" byte
        self.f.seek(OffsetByte,1)
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
        rs=np.zeros((imageDims[1],imageDims[0],stopimg-startimg),dtype='f')
        for i in range(stopimg-startimg):
            imageraw=self.f.read(4*imageDims[0]*imageDims[1])
            image=np.frombuffer(imageraw,dtype='f')
<<<<<<< HEAD
=======
            #imagebg=f.read(65536*2)
            #imdb=np.subtract(np.frombuffer(image,dtype='h'),np.frombuffer(imagebg,dtype='h'))
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
            rs[:,:,i]=np.reshape(image,(imageDims[1],imageDims[0]))
        #f.close()
        return rs

<<<<<<< HEAD
class lvsor: #SOR images created by labview, these are always 16 bits
    def __init__(self, filename):
        self.f=open(filename,'rb')

    def imageType(self):
        return 'LVSor'

    def getimgdata(self): #returns width,height
        self.f.seek(14,0)
        width=np.frombuffer(self.f.read(2),dtype='h').item(0)
        height=np.frombuffer(self.f.read(2),dtype='h').item(0)
        return(width,height)

    def numimgframes(self):
        self.f.seek(-4,2)
        return(int.from_bytes(self.f.read(4),byteorder='little'))

    def readimg(self,startimg=0,stopimg=1):
        width=self.getimgdata()[0]
        height=self.getimgdata()[1]
        if startimg > self.numimgframes():
            return np.zeros(getimgdata(self),dtype='uint16')
        if stopimg > self.numimgframes():
            stopimg=stopimg=self.numimgframes()
        f=self.f
        if stopimg<0:
            stopimg=self.numimgframes()
        #header is 16 words aka 32 bytes
        f.seek(32+height*width*2*startimg,0)
        rs=np.zeros((height,width,stopimg-startimg),dtype='uint16')
        for i in range(stopimg-startimg):
            image=f.read(height*width*2)
            imdb=np.frombuffer(image,dtype='uint16')
            rs[:,:,i]=np.reshape(imdb,(height,width))
        #f.close()
        return rs
=======
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5

class mptif16: #support for multipage tifs in several files made by the thorlabs software
    def __init__(self, filename):
        self.filename = filename
<<<<<<< HEAD
        self.f=imageio.get_reader(self.filename,'tiff','I')
        self.subfiles=[self]
        numfiles=1
        while True:
            #print(str(filename).split('.tif')[0]+'_'+str(numfiles)+'.tif')
            if os.path.isfile(str(filename).split('.tif')[0]+'_'+str(numfiles)+'.tif'):
                self.subfiles.append(mptif16(str(self.filename).split('.tif')[0]+'_'+str(numfiles)+'.tif'))
=======
        self.subfiles=[self]
        if os.path.isfile(str(filename).split('.tif')[0]+'_0.tif'):
            self.f=imageio.get_reader(str(filename).split('.tif')[0]+'_0.tif','tiff','I')
        else:
            self.f=imageio.get_reader(str(filename),'tiff','I')
        numfiles=1
        while True:
            if os.path.isfile(str(filename).split('.tif')[0]+'_'+str(numfiles-1)+'.tif'):
                self.subfiles.append(mptif16(str(self.filename).split('.tif')[0]+'_'+str(numfiles-1)+'.tif'))
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
                numfiles+=1
            else:
                break
        self.numfiles=numfiles
        self.imagedata=self.f.get_next_data()
        # if numfiles>1:
        #     for s in self.subfiles:
        #         print(s.numimgframes(onlythis=True))
        #flagga om subfil
    def getnumfiles(self):
        return self.numfiles

    def imageType(self):
        return 'MPTIF'

    def numimgframes(self,onlythis=False):
        if self.numfiles==1 or onlythis:
            return self.f.get_length()
        else:
            total=self.f.get_length()
<<<<<<< HEAD
            for i in range(self.getnumfiles()-1):
                nextfile=mptif16(str(self.filename).split('.tif')[0]+'_'+str(i+1)+'.tif')
=======
            for i in range(self.getnumfiles()-2):
                nextfile=mptif16(str(self.filename).split('.tif')[0]+'_'+str(i)+'.tif')
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
                total=total+nextfile.numimgframes(onlythis=True)
            return total

    def numimgframesperfile(self):
        if self.numfiles==1:
            return self.f.get_length()
        else:
            total=[]
            total.append(self.f.get_length())
            for i in range(self.getnumfiles()-1):
<<<<<<< HEAD
                nextfile=mptif16(str(self.filename).split('.tif')[0]+'_'+str(i+1)+'.tif')
=======
                nextfile=mptif16(str(self.filename).split('.tif')[0]+'_'+str(i)+'.tif')
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
                total.append(nextfile.numimgframes(onlythis=True))
            return total

    def getimgdata(self): #returns width,height
        return np.shape(self.imagedata)

    def whichfile(self,frame):
        if self.numfiles==1:
            return 0
        framenums=self.numimgframesperfile()
        imgfile=0
        currframe=frame
        while True:
            currframe-=framenums[imgfile]
<<<<<<< HEAD
            if currframe<=0:
=======
            if currframe<0:
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
                return imgfile,framenums[imgfile]+currframe
            imgfile+=1
        return 0

    def readimg(self,startimg=0,stopimg=-1,onlythis=False):
        imageDims=self.getimgdata()
        if stopimg<0:
            if onlythis:
                stopimg=self.numimgframes(onlythis=True)
            else:
                 stopimg=self.numimgframes()

        if self.numfiles>1 and not onlythis: #not a subfile
            rs=np.empty((imageDims[0],imageDims[1],0),dtype='uint16')
            startdata=self.whichfile(startimg)
            stopdata=self.whichfile(stopimg)
            globalindex=startimg
            currentfile=startdata[0]
            localstartindex=startdata[1]
            while currentfile<stopdata[0]:
                rs=np.append(rs,self.subfiles[currentfile].readimg(localstartindex,-1,True),2)
                localstartindex=0
                currentfile+=1
            if currentfile==stopdata[0]:
                rs=np.append(rs,self.subfiles[currentfile].readimg(localstartindex,stopdata[1],True),2)
        else:
            self.f.set_image_index(startimg)
            rs=np.zeros((imageDims[0],imageDims[1],stopimg-startimg),dtype='uint16')
            for i in range(stopimg-startimg):
                rs[:,:,i]=self.f.get_next_data()
<<<<<<< HEAD
                #print('.', end='',flush=True)
=======
                print('.', end='',flush=True)
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
            #f.close()
        return rs

class sbf: #files made by the SBF IR camera software
    def __init__(self, filename):
        self.filename = filename
        self.f=open(self.filename,'rb')

    def imageType(self):
        return 'SBF'

    def numimgframes(self):
        self.f.seek(42,0)
        return(int.from_bytes(self.f.read(4),byteorder='little'))

    def getimgdata(self): #returns width,height
        return (256,256)

    def readraw(self,startimg=0,stopimg=1):
        if startimg > self.numimgframes():
            return np.zeros((256,256),dtype='h')
        if stopimg > self.numimgframes():
            stopimg=stopimg=self.numimgframes()
        f=self.f
        if stopimg<0:
            stopimg=self.numimgframes()
        #f.seek(512,0)
        f.seek(512+65536*2*startimg,0)
        rs=np.zeros((256,256,stopimg-startimg),dtype='h')
        for i in range(stopimg-startimg):
            image=f.read(65536*2)
            imdb=np.frombuffer(image,dtype='h')
            rs[:,:,i]=np.reshape(imdb,(256,256))
        #f.close()
        return rs

<<<<<<< HEAD
    def readimg(self,startimg=0,stopimg=-1,altbg=False):
        if startimg > self.numimgframes():
            return np.zeros((256,256),dtype='h')
        if stopimg > self.numimgframes():
            stopimg=self.numimgframes()//2
=======
    def readimg(self,startimg=0,stopimg=-1):
        if startimg > self.numimgframes():
            return np.zeros((256,256),dtype='h')
        if stopimg > self.numimgframes():
            stopimg=stopimg=self.numimgframes()//2
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
        f=self.f
        if stopimg<0:
            stopimg=self.numimgframes()//2
        #f.seek(512,0)
        f.seek(512+65536*4*startimg,0)
        rs=np.zeros((256,256,stopimg-startimg),dtype='h')
        for i in range(stopimg-startimg):
<<<<<<< HEAD
            if altbg:
                imagebg=f.read(65536*2)
                image=f.read(65536*2)
            else:
                image=f.read(65536*2)
                imagebg=f.read(65536*2)
=======
            image=f.read(65536*2)
            imagebg=f.read(65536*2)
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
            imdb=np.subtract(np.frombuffer(image,dtype='h'),np.frombuffer(imagebg,dtype='h'))
            rs[:,:,i]=np.reshape(imdb,(256,256))
        #f.close()
        return rs

<<<<<<< HEAD
class plifimg:
    def readimgav(img,startimg=0,stopimg=-1,numavg=10,altbg=False,status=True,binning=None,forcefunc=False):
=======
    # def readimgav(self,startimg=0,stopimg=-1,numavg=10):
    #     if stopimg<0: #if -1, read to end
    #         stopimg=self.numimgframes()//2
    #     rs=np.zeros((256,256,(stopimg-startimg)//numavg),dtype='h')
    #     for i in range((stopimg-startimg)//numavg):
    #         frame=i*numavg+startimg
    #         temp=self.readimg(frame,frame+numavg-1)
    #         rs[:,:,i]=np.mean(temp,axis=2)
    #     return rs
    # def close(self):
    #     self.f.close()

class plifimg:
    def readimgav(img,startimg=0,stopimg=-1,numavg=10):
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
        if stopimg<0 or \
         (img.imageType()=='SBF' and stopimg>img.numimgframes()//2) or \
         stopimg>img.numimgframes():  #if -1, read to end
            stopimg=img.numimgframes()
            if img.imageType()=='SBF':
                stopimg=img.numimgframes()//2
<<<<<<< HEAD
        if numavg==1 and not forcefunc: #1 average one = no average
=======
        if numavg==1: #1 average one = no average
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
            rs=img.readimg(startimg,stopimg)
            return rs
        if numavg==-1: #if -1, average all
            numavg=img.numimgframes()
            if img.imageType()=='SBF':
                numavg=img.numimgframes()//2
        imageDims=img.getimgdata()
<<<<<<< HEAD
        if img.imageType()=='AndorSIF' or img.imageType()=='LVSor':
            rs=np.zeros((imageDims[1],imageDims[0],(stopimg-startimg)//numavg),dtype='float64')
        else:
            rs=np.zeros((imageDims[0],imageDims[1],(stopimg-startimg)//numavg),dtype='float64')

        for i in range((stopimg-startimg)//numavg):
            frame=i*numavg+startimg
            if (status):
                print('reading '+str(frame)+' to '+str(frame+numavg-1))
            temp=img.readimg(frame,frame+numavg-1)
            if altbg:
                temp=img.readimg(frame,frame+numavg-1,True)
            rs[:,:,i]=np.nanmean(temp,axis=2)
        return rs
    
    def makeProfileFunction(profileMeta,labView=None,plifLength=None,numAvg=10):
            from readlvfile2 import readlvfile2dict
            from scipy.interpolate import interp1d
            if np.size(profileMeta)==1: #assume single filename, just load and average all
                if profileMeta.endswith('sif'):
                    return np.abs(np.squeeze(plifimg.readimgav(sif(profileMeta),numavg=-1,status=False)))
                else:
                    return np.abs(np.squeeze(plifimg.readimgav(sbf(profileMeta),numavg=-1,status=False)))


            if np.size(profileMeta)==2 and profileMeta[1]=='ramp': #assume its a ramp, just return it with x avg
                if profileMeta[0].endswith('sif'):
                    return np.swapaxes(np.swapaxes(np.abs(np.squeeze(plifimg.readimgav(sif(profileMeta[0]),numavg=numAvg,status=False))), 0, 2), 1, 2)
                else:
                    return np.swapaxes(np.swapaxes(np.abs(np.squeeze(plifimg.readimgav(sbf(profileMeta[0]),numavg=numAvg,status=False))), 0, 2), 1, 2)

            else: #assume multiple profiles in a tuple.
                profileData=np.zeros([len(profileMeta[0]),256,256])
                for prf in range(len(profileMeta[0])):
                    profileData[prf,:,:]=np.abs(np.squeeze(plifimg.readimgav(sbf(profileMeta[0][prf]),numavg=-1,status=False)))
                lvInfo=readlvfile2dict(labView)
                profileValueFunction=interp1d(np.linspace(profileMeta[1][1][0],profileMeta[1][1][1],len(profileMeta[0])),profileData,axis=0,fill_value='extrapolate',bounds_error=False)
                valueFunction=interp1d(readlvfile2dict(labView)['times'],readlvfile2dict(labView)[profileMeta[1][0]],fill_value='extrapolate',bounds_error=False)
                timeFrame=np.linspace(0,int(np.max(readlvfile2dict(labView)['times'])))
                #plifLength=sbf(plifFile).numimgframes()//20 #length in seconds
                #plifTimeValues=interp1d(range(plifLength),valueFunction(range(plifLength)))
                profileFunction=interp1d(timeFrame,profileValueFunction(valueFunction(timeFrame)),axis=0)
                if (plifLength==None):
                    return profileFunction
                else:
                    plifSpace=np.arange(0,plifLength,numAvg/10)
                    return profileFunction(plifSpace)
=======
        rs=np.zeros((imageDims[0],imageDims[1],(stopimg-startimg)//numavg),dtype='float64')
        for i in range((stopimg-startimg)//numavg):
            frame=i*numavg+startimg
            print('reading '+str(frame)+' to '+str(frame+numavg-1))
            temp=img.readimg(frame,frame+numavg-1)
            rs[:,:,i]=np.nanmean(temp,axis=2)
        return rs

from pims import FramesSequence, Frame
class SBFReader(FramesSequence):
    def __init__(self, filename):
        self.sbffile=sbf(filename)
        self.filename = filename
        self._len = self.sbffile.numimgframes()//2 # however many frames there will be
        self._dtype =  'h'# the numpy datatype of the frames
        self._frame_shape =(256,256)  # the shape, like (512, 512), of an
                             # individual frame -- maybe get this by
                             # opening the first frame
        # Do whatever setup you need to do to be able to quickly access
        # individual frames later.

    def get_frame(self, i):
        # Access the data you need and get it into a numpy array.
        # Then return a Frame like so:
        framearray=self.sbffile.readimg(i,i+1)
        return Frame(framearray[:,:,0], frame_no=i)

    def __len__(self):
         return self._len

    def close(self):
        self.sbffile.close()


    @property
    def frame_shape(self):
         return self._frame_shape

    @property
    def pixel_type(self):
         return self._dtype

    @classmethod
    def class_exts(self):
        return {'img'} | super().class_exts()
>>>>>>> a9dfd698b53791532ba867d26c1413cf6d5511f5
