#!/usr/bin/env python3
import imageio
import numpy as np
from scanf import scanf
import time
import os.path
#from readimg import sbf, plifimg
from camview.winspec import SpeFile

class imformat:
    """Function skeleton for image reader class
    """
    def __init__(self, filename):
        """[summary]

        Args:
            filename (string): image filename to open
        """
        self.f=open(filename,'rb')

    def imageType(self):
        """get the image type

        Returns:
            string: image type
        """
        return 'None'

    def getimgdata(self):
        """Returns width and height as a tuple.
        Returns:
        tuple: width, height
        """
        pass

    def numimgframes(self):
        """get number of frames in dataset
        Returns:
        int: number of frames
        """
        pass

    def readimg(self,startimg=0,stopimg=1):
        """[summary]

        Args:
            startimg (int, optional): [description]. Defaults to 0.
            stopimg (int, optional): [description]. Defaults to 1.
        """
        pass

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
        return self.stacksize

    def readimg(self,startimg=0,stopimg=-1,offset=0):
        imageDims=self.getimgdata()
        NumFrames=self.numimgframes()
        if stopimg<0:
            stopimg=NumFrames
        self.f=open(self.filename,'rb')
        self.f.seek(4*startimg*imageDims[0]*imageDims[1]+self.m_offset+offset,0) #zyla file
        rs=np.zeros((imageDims[1],imageDims[0],stopimg-startimg),dtype='f')
        for i in range(stopimg-startimg):
            imageraw=self.f.read(4*imageDims[0]*imageDims[1])
            image=np.frombuffer(imageraw,dtype='f')
            rs[:,:,i]=np.reshape(image,(imageDims[1],imageDims[0]))
        #f.close()
        return rs

class lvsor: #SOR images created by labview, these are always 16 bits
    """Reads the custom format created by the Catalysis Group LabView program for SOR images.
    """
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

class mptif16:
    """Class to read multi-page TIFF files as produced by the Thorcam software by Thorlabs. One dataset can be split into many subfiles.
    """
    def __init__(self, filename):
        self.filename = filename
        self.f=imageio.get_reader(self.filename,'tiff','I')
        self.subfiles=[self]
        numfiles=1
        while True:
            if os.path.isfile(str(filename).split('.tif')[0]+'_'+str(numfiles)+'.tif'):
                self.subfiles.append(mptif16(str(self.filename).split('.tif')[0]+'_'+str(numfiles)+'.tif'))
                numfiles+=1
            else:
                break
        self.numfiles=numfiles
        self.imagedata=self.f.get_next_data()

    def getnumfiles(self):
        """Get number of subfiles in dataset.

        Returns:
            int: Number of subfiles
        """
        return self.numfiles

    def imageType(self):
        return 'MPTIF'

    def numimgframes(self,onlythis=False):
        """Get number of frames in the dataset.

        Args:
            onlythis (bool, optional): Whether to consider subfiles. Defaults to False.

        Returns:
            int: nunber of frames
        """
        if self.numfiles==1 or onlythis:
            return self.f.get_length()
        else:
            total=self.f.get_length()
            for i in range(self.getnumfiles()-1):
                nextfile=mptif16(str(self.filename).split('.tif')[0]+'_'+str(i+1)+'.tif')
                total=total+nextfile.numimgframes(onlythis=True)
            return total

    def numimgframesperfile(self):
        """Gets number of frames per subfile.

        Returns:
            int: number of frames
        """
        if self.numfiles==1:
            return self.f.get_length()
        else:
            total=[]
            total.append(self.f.get_length())
            for i in range(self.getnumfiles()-1):
                nextfile=mptif16(str(self.filename).split('.tif')[0]+'_'+str(i+1)+'.tif')
                total.append(nextfile.numimgframes(onlythis=True))
            return total

    def getimgdata(self): #returns width,height
        """Get image dimensions

        Returns:
            tuple: (width,height)
        """
        return np.shape(self.imagedata)

    def whichfile(self,frame):
        """Check which subfile contains a certain frame.

        Args:
            frame (int): The frame to check

        Returns:
            int: subfile number with that frame.
        """
        if self.numfiles==1:
            return 0
        framenums=self.numimgframesperfile()
        imgfile=0
        currframe=frame
        while True:
            currframe-=framenums[imgfile]
            if currframe<=0:
                return imgfile,framenums[imgfile]+currframe
            imgfile+=1
        return 0

    def readimg(self,startimg=0,stopimg=-1,onlythis=False):
        """Read image sequence. Will automatically consider subfiles.

        Args:
            startimg (int, optional): Read from this image number. Defaults to 0 (beginning of file).
            stopimg (int, optional): Read to this image number, -1 reads entire file. Defaults to -1 (eof).
            onlythis (bool, optional): Ignore subfiles. Defaults to False.

        Returns:
            numpy array: Array with all the images. Axis order is (x,y,t).
        """
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
                #print('.', end='',flush=True)
            #f.close()
        return rs

class sbf:
    """Class to read files made by the WinIR 3.x software by Santa Barbara Focalplane.
    """
    def __init__(self, filename,numbgframes=1):
        self.numbgframes=numbgframes
        self.filename = filename
        self.f=open(self.filename,'rb')

    def imageType(self):
        return 'SBF'

    def numimgframes(self, rawcount=False):
        self.f.seek(42,0)
        if rawcount:
            return(int.from_bytes(self.f.read(4),byteorder='little'))
        else:
            return(int.from_bytes(self.f.read(4),byteorder='little'))//(self.numbgframes+1)

    def getimgdata(self): #returns width,height
        return (256,256)

    def findPLIFframe(self):
        """This function checks the PLIF data in three places (25% in, 50% in and 75% in.
        It then tries to find which frame is the one with PLIF data in it (and not bg)

        Returns:
            int: first frame with laser
        """
        cycleframes=self.numbgframes+1
        fractions=np.array([.25,.5,.75]) #where to check
        startframes=self.numimgframes(True)*fractions//cycleframes*cycleframes
        #now load 10 cycles at every spot and find the maximum of each cycle
        allmax=[]
        for startframe in startframes:
            for cycle in range(10):
                cycledata=self.readraw(int(startframe+cycle*cycleframes),int(startframe+(cycle*cycleframes)+cycleframes))
                roi=np.mean(cycledata[100:120,100:120,:],axis=(0,1))
                allmax.append(np.argmax(roi))
        return np.argmax(np.bincount(np.array(allmax)))


    def readraw(self,startimg=0,stopimg=1):
        stopimg=stopimg
        if startimg > self.numimgframes(rawcount=True):
            return np.zeros((256,256),dtype='h')
        if stopimg > self.numimgframes(rawcount=True):
            stopimg=stopimg=self.numimgframes(rawcount=True)
        f=self.f
        if stopimg<0:
            stopimg=self.numimgframes(rawcount=True)
        #f.seek(512,0)
        f.seek(512+65536*2*startimg,0)
        rs=np.zeros((256,256,stopimg-startimg),dtype='h')
        for i in range(stopimg-startimg):
            image=f.read(65536*2)
            imdb=np.frombuffer(image,dtype='h')
            rs[:,:,i]=np.reshape(imdb,(256,256))
        #f.close()
        return rs
    
    def readimg(self,startimg=0,stopimg=-1,altbg=False,raw=False):
        """Reads the SBF format images

        Args:
            startimg (int, optional): Read from this image number. Defaults to 0 (beginning of file).
            stopimg (int, optional): Read to this image number, -1 reads entire file. Defaults to -1 (eof).
            altbg (bool, optional): Use the background before the data frame rather than that after. Defaults to False.
            numbgframes (int, optional): Number of background frames between PLIF frames. Defaults to 1.
            plifframe (int, optional): Which frame is the PLIF frame in each frame cycle. Defaults to 0.

        Returns:
            numpy array: Array with all the images. Axis order is (x,y,t)
        """
        if raw:
            return self.readraw(startimg,stopimg)

        cycleframes=self.numbgframes+1 #number of frames in 100 ms, usually 2 unless hifps on IR camera
        skipframes=cycleframes-2 #background frames to skip 
        #initialskip = plifframe%cycleframes #make sure the skip is periodic
        initialskip = self.findPLIFframe() #make sure the skip is periodic
        if altbg:
            plifframe=plifframe-1
        if startimg > self.numimgframes():
            return np.zeros((256,256),dtype='h')
        if stopimg > self.numimgframes():
            stopimg=self.numimgframes()//cycleframes
        f=self.f
        if stopimg<0:
            stopimg=self.numimgframes()//cycleframes
        #skip 512 byte header, then skip one cycle/frame, then skip the initialskip
        f.seek(512+65536*2*cycleframes*startimg+65536*2*initialskip,0)
        rs=np.zeros((256,256,stopimg-startimg),dtype='h')
        for i in range(stopimg-startimg):
            if altbg:
                imagebg=f.read(65536*2)
                image=f.read(65536*2)
            else:
                image=f.read(65536*2)
                imagebg=f.read(65536*2)
            imdb=np.subtract(np.frombuffer(image,dtype='h'),np.frombuffer(imagebg,dtype='h'))
            rs[:,:,i]=np.reshape(imdb,(256,256))
            f.seek(65536*2*skipframes,1)
        #f.close()
        return rs

class plifimg:
    """This class contains static utility functions that are nice to have when handling PLIF images.
    """
    @staticmethod
    def readimgav(img,startimg=0,stopimg=-1,numavg=10,status=True,binning=None,forcefunc=False,**kwargs):
        """Reads an image file and averages a number of frames in time. This conserves memory when reading large files.

        Args:
            img (imformat): Image file to read
            startimg (int, optional): Read from this image, default is start of file. Defaults to 0.
            stopimg (int, optional): Read to this frame, -1 will read the entire file. Defaults to -1.
            numavg (int, optional): Number of images to average. Defaults to 10.
            status (bool, optional): Verbose status prints. Defaults to True.
            binning ([type], optional): Binning in space. Not implemented. Defaults to None.
            forcefunc (bool, optional): Force the use of the averaging function even for numavg=1. Defaults to False.

        Returns:
            numpy array: Array with all the images. Axis order is (x,y,t)
        """
        if 'raw' in kwargs:
            numframes=img.numimgframes(rawcount=kwargs.get("raw"))
        else:
            numframes=img.numimgframes()
        if stopimg<0 or \
         (img.imageType()=='SBF' and stopimg>numframes//2) or \
         stopimg>numframes:  #if -1, read to end
            stopimg=numframes
        if numavg==1 and not forcefunc: #1 average one = no average
            rs=img.readimg(startimg,stopimg,**kwargs)
            return rs
        if numavg==-1: #if -1, average all
            numavg=numframes
        imageDims=img.getimgdata()
        if img.imageType()=='AndorSIF' or img.imageType()=='LVSor':
            rs=np.zeros((imageDims[1],imageDims[0],(stopimg-startimg)//numavg),dtype='float64')
        else:
            rs=np.zeros((imageDims[0],imageDims[1],(stopimg-startimg)//numavg),dtype='float64')

        for i in range((stopimg-startimg)//numavg):
            frame=i*numavg+startimg
            if (status):
                print('reading '+str(frame)+' to '+str(frame+numavg-1))
            temp=img.readimg(frame,frame+numavg-1,**kwargs)
            rs[:,:,i]=np.nanmean(temp,axis=2)
        return rs
    
    @staticmethod
    def makeProfileFunction(profileMeta,labView=None,plifLength=None,numAvg=10):
        """[summary]

        Args:
            profileMeta ([type]): [description]
            labView ([type], optional): [description]. Defaults to None.
            plifLength ([type], optional): [description]. Defaults to None.
            numAvg (int, optional): [description]. Defaults to 10.

        Returns:
            [type]: [description]
        """
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

class spe(SpeFile):

    def __init__(self, filename):
        super().__init__(filename)
        self.f=open(filename,'rb')

    def imageType(self):
        return 'SPE'

    def getimgdata(self): #returns width,height
        return(self.header.xdim,self.header.ydim)

    def numimgframes(self):
        return(self.header.NumFrames)

    def readimg(self,startimg=0,stopimg=1):
        width=self.getimgdata()[0]
        height=self.getimgdata()[1]
        if startimg > self.numimgframes():
            return np.zeros(self.getimgdata(),dtype='uint16')
        if stopimg > self.numimgframes():
            stopimg=stopimg=self.numimgframes()
        f=self.f
        if stopimg<0:
            stopimg=self.numimgframes()
        #header is 16 words aka 32 bytes
        f.seek(4100+height*width*2*startimg,0)
        rs=np.zeros((height,width,stopimg-startimg),dtype='uint16')
        for i in range(stopimg-startimg):
            image=f.read(height*width*2)
            imdb=np.frombuffer(image,dtype='uint16')
            rs[:,:,i]= np.fliplr(np.rot90(np.reshape(imdb,(height,width)),k = -2))
        #f.close()
        return rs

class speMany:
    def __init__(self, filename,fromFrame,toFrame,LoadAverage):
        self.file = filename
        self.data = []
        self.len = 0 
        self.fromFrame = fromFrame
        self.toFrame = toFrame
        self.LoadAverage = LoadAverage
        for fname in os.listdir(self.file):
            if fname.endswith(".SPE"):
                self.xdim = spe(os.path.join(self.file,fname)).getimgdata()[0] 
                self.ydim = spe(os.path.join(self.file,fname)).getimgdata()[1] 
                self.len += spe(os.path.join(self.file,fname)).numimgframes()
        # self.data = self.data.reshape((self.xdim,self.ydim,len(self.data)))
 
          
    def imageType(self):
        return 'SPE'

    def getimgdata(self): #returns width,height
        return(self.xdim,self.ydim)

    def numimgframes(self):
        return(self.len)

    def readimg(self,startimg=0,stopimg=1):
        data = np.zeros((self.len,self.xdim,self.ydim))
        temp = 0
        j = 0
        for fname in os.listdir(self.file):
            if fname.endswith(".SPE"):
                file = spe(os.path.join(self.file,fname))
                temp = plifimg.readimgav(file,self.fromFrame,self.toFrame,self.LoadAverage).swapaxes(0,2).swapaxes(1,2)
                i = 0
                for i in range(temp.shape[0]):
                    data[j,:,:] = temp[i,:,:]
                    j += 1
                    i += 1
        
        return data

        # return self.data.reshape((self.xdim,self.ydim,len(self.data)))

