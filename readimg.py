import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scanf import scanf
#from readimg import sbf, plifimg

class sif:
    def __init__(self, filename):
        self.filename = filename

        #self.f=open(self.filename,'rb')
        #Pixel number6
        # Counts12
        # Pixel number65541 1 2160 2560 1 12000 1 1239264000 103272
        # 65538 730 1780 1722 845 3 3 0

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

class sbf:
    def __init__(self, filename):
        self.filename = filename
        self.f=open(self.filename,'rb')

    def numimgframes(self):
        self.f.seek(42,0)
        return(int.from_bytes(self.f.read(4),byteorder='little'))

    def getimgdata(self): #returns width,height
        return (256,256)

    def readimg(self,startimg=0,stopimg=-1):
        #f=open(self.filename,'rb')
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
        if stopimg<0:  #if -1, read to end
            stopimg=img.numimgframes()//2
        if numavg==1: #1 averager = no average
            rs=img.readimg(startimg,stopimg)
            return rs
        if numavg==-1: #if -1, average all
            numavg=img.numimgframes()//2
        imageDims=img.getimgdata()
        rs=np.zeros((imageDims[1],imageDims[0],(stopimg-startimg)//numavg),dtype='h')
        for i in range((stopimg-startimg)//numavg):
            frame=i*numavg+startimg
            temp=img.readimg(frame,frame+numavg-1)
            rs[:,:,i]=np.mean(temp,axis=2)
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
