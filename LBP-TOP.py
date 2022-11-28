import cv2
import numpy as np
import math
import scipy.io as sio
import argparse

def LBP_TOP(VolData, xRadius = 1, yRadius = 1, tInterval = 4, NeighborPoints = [8, 8, 8], TimeLength = 4, BorderLength = 1):
    
    #
    length, height, width = VolData.shape
    
    XYNeighborPoints = NeighborPoints[0]
    XTNeighborPoints = NeighborPoints[1]
    YTNeighborPoints = NeighborPoints[2]
    
    nDim = 2 ** (YTNeighborPoints)
    Histogram = np.zeros((3, nDim), float)
    
    for t in range(TimeLength, length -TimeLength):
        for yc in range(BorderLength, height-BorderLength):
            for xc in range(BorderLength, width - BorderLength):
                CenterVal = VolData[t, yc, xc]
                
                #LBP from XY
                BasicLBP = 0
                FeaBin = 0
                
                for p in range(0, XYNeighborPoints):
                    X = int(xc+xRadius*math.cos((2*math.pi*p)/XYNeighborPoints)+0.5)
                    Y = int(yc-yRadius*math.cos((2*math.pi*p)/XYNeighborPoints)+0.5)
                    
                    CurrentVal = VolData[t, Y, X]
                    
                    if CurrentVal >= CenterVal:
                        BasicLBP += 2**FeaBin
                    FeaBin += 1
                Histogram[0, BasicLBP] = Histogram[0, BasicLBP]+1
                
                # LBP from XT
                BasicLBP = 0
                FeaBin = 0
                
                for p in range(0, XTNeighborPoints):
                    X = int(xc + xRadius*math.cos((2*math.pi*p)/XTNeighborPoints)+0.5)
                    Z = int(t + tInterval*math.sin((2*math.pi*p)/XTNeighborPoints)+0.5)
                    
                    CurrentVal = VolData[Z, yc, X]
                    
                    if CurrentVal >= CenterVal:
                        BasicLBP += 2**FeaBin
                        
                    FeaBin+=1
                Histogram[1, BasicLBP] = Histogram[1, BasicLBP] + 1
                
                # LBP from YT
                BasicLBP = 0
                FeaBin = 0
                
                for p in range(0, YTNeighborPoints):
                    Y = int(yc - yRadius*math.cos((2*math.pi*p)/YTNeighborPoints)+0.5)
                    Z = int(t + tInterval*math.sin((2*math.pi*p)/YTNeighborPoints)+0.5)
                    
                    CurrentVal = VolData[Z, Y, xc]
                    
                    if CurrentVal >= CenterVal:
                        BasicLBP += 2**FeaBin
                    
                    FeaBin += 1
                
                Histogram[2, BasicLBP] = Histogram[2, BasicLBP]+1
            
    for j in range(0, 3):
        Histogram[j, :] = (Histogram[j,:]*1.0)/sum(Histogram[j, :])
    
    return  Histogram


def videoframes(vf):
    camera = cv2.VideoCapture(vf)
    
    frms = None
    while camera.isOpened():
        sucess, video_frame = camera.read()
        if sucess is False:
            camera.release()
        else:
            frm_gray = cv2.cvtColor(video_frame, cv2.COLOR_RGB2GRAY)
            if frms is None:
                frms = np.array([frm_gray])
            else:
                frms = np.concatenate((frms, [frm_gray]))
        
    return frms

def ExtLBP_TOP4Video(vf):
    fps = 30
    frms = videoframes(vf)
    frms_cnts = frms.shape[0]
    segs = frms_cnts//fps
    lbps = None
    for i in range(segs):
        frms_seg = frms[i*fps:(i+1)*fps,:,:]
        lbp = LBP_TOP(frms_seg)
        lbp = lbp.reshape(1,-1)
        if lbps is None:
            lbps = lbp
        else:
            lbps = np.vstack((lbps, lbp))
    return lbps
    
def ExtLBP_TOP4Subj(rootpath):
    vids = []
    lbps_all = None
    for i in range(32):
        vf = rootpath + str(i) + '.mp4'
        lbps = ExtLBP_TOP4Video(vf)
        if lbps_all is None:
            lbps_all = lbps
        else:
            lbps_all = np.vstack((lbps_all, lbps))
        
        vids = np.append(vids, np.ones(lbps.shape[0], np.int32)*i)

    sio.savemat(rootpath+'videoFea.mat', {'lbps_all':lbps_all, 'vids':vids})
    
def ExtLBP_TOP4AllSubjs(rootpath, sub_b=1, sub_e=35):
    for i in range(sub_b, sub_e+1):
        ExtLBP_TOP4Subj(rootpath+ str(i)+ '/')
        
def ExtLBP_TOP4AllSubjs_(rootpath, subs):
    for i in subs:
        ExtLBP_TOP4Subj(rootpath+ str(i)+ '/')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('--subj_b', type=int, default=1, help='begin subject index')
    #parser.add_argument('--subj_e', type=int, default=35, help='end subject index')
    #args = parser.parse_args()
    #print(args.subj_b, args.subj_e)
    subs = [1,2,5,6,7,8,9,10,11,12,14,15,18,19,20,21,22,23,24,25,26,28,29,30,32,33,34,35]
    ExtLBP_TOP4AllSubjs_('F:/MixedEmoR-V2/', subs)