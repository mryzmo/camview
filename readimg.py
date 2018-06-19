import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import imageio
import numpy as np
from scanf import scanf
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
        rs=np.zeros((imageDims[1],imageDims[0],stopimg-startimg),dtype='f')
        for i in range(stopimg-startimg):
            imageraw=self.f.read(4*imageDims[0]*imageDims[1])
            image=np.frombuffer(imageraw,dtype='f')
            #imagebg=f.read(65536*2)
            #imdb=np.subtract(np.frombuffer(image,dtype='h'),np.frombuffer(imagebg,dtype='h'))
            rs[:,:,i]=np.reshape(image,(imageDims[1],imageDims[0]))
        #f.close()
        return rs


class mptif16: #support for multipage tifs in several files made by the thorlabs software
    def __init__(self, filename):
        self.filename = filename
        self.f=imageio.get_reader(self.filename,'tiff','I')
        self.subfiles=[self]
        numfiles=1
        while True:
            if os.path.isfile(str(filename).split('.tif')[0]+'_'+str(numfiles-1)+'.tif'):
                self.subfiles.append(mptif16(str(self.filename).split('.tif')[0]+'_'+str(numfiles-1)+'.tif'))
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
            for i in range(self.getnumfiles()-2):
                nextfile=mptif16(str(self.filename).split('.tif')[0]+'_'+str(i)+'.tif')
                total=total+nextfile.numimgframes(onlythis=True)
            return total

    def numimgframesperfile(self):
        if self.numfiles==1:
            return self.f.get_length()
        else:
            total=[]
            total.append(self.f.get_length())       
            for i in range(self.getnumfiles()-1):
                nextfile=mptif16(str(self.filename).split('.tif')[0]+'_'+str(i)+'.tif')
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
            if currframe<0:
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
                print('.', end='',flush=True)
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

    def readimg(self,startimg=0,stopimg=-1):
        if startimg > self.numimgframes():
            return np.zeros((256,256),dtype='h')
        if stopimg > self.numimgframes():
            stopimg=stopimg=self.numimgframes()//2
        f=self.f
        if stopimg<0:
            stopimg=self.numimgframes()//2
        #f.seek(512,0)
        f.seek(512+65536*4*startimg,0)
        rs=np.zeros((256,256,stopimg-startimg),dtype='h')
        for i in range(stopimg-startimg):
            image=f.read(65536*2)
            imagebg=f.read(65536*2)
            imdb=np.subtract(np.frombuffer(image,dtype='h'),np.frombuffer(imagebg,dtype='h'))
            rs[:,:,i]=np.reshape(imdb,(256,256))
        #f.close()
        return rs

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
        print('Starting average read...')
        #img.readimg(1400,1499)
        if stopimg<0:  #if -1, read to end
            stopimg=img.numimgframes()
            if img.imageType()=='SBF':
                stopimg=img.numimgframes()//2
        if numavg==1: #1 averager = no average
            rs=img.readimg(startimg,stopimg)
            return rs
        if numavg==-1: #if -1, average all
            numavg=img.numimgframes()
            if img.imageType()=='SBF':
                numavg=img.numimgframes()//2
        imageDims=img.getimgdata()
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


#sbfi=sbf('/home/sebastian/Documents/Data/20171029_real_14.img')
#
#rs=plifimg.readimgav(sbfi,11000)
#
#
##rs=sbfi.readimgav(11000)
##rs=readimgav('/home/sebastian/Documents/Data/20171029_real_14.img',11000,-1,10)
#plt.imshow(rs[:,:,1])
#plt.colorbar()
#print(numimgframes('/home/sebastian/Documents/Data/20171029_real_14.img'))
    #print(f.read(65536))
