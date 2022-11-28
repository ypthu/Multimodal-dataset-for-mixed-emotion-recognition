import os
import cv2
import scipy.io as sio
import numpy as np


EEG_SRATE=300
GSR_SRATE=4
PPG_SRATE=100

def videolen(vf, fps=30):
    camera = cv2.VideoCapture(vf)
    totalfrms = camera.get(cv2.CAP_PROP_FRAME_COUNT)
    return totalfrms/fps, totalfrms

def cutvideo(vf, target_file, bg_pos, frm_cnt):
    camera = cv2.VideoCapture(vf)
    camera.set(cv2.CAP_PROP_POS_FRAMES, bg_pos)

    video_format = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    hfile = cv2.VideoWriter()
    filepath = target_file
    frame_size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    hfile.open(filepath, video_format, 30, frame_size)

    curtotal = 0
    while camera.isOpened():
        sucess, video_frame = camera.read()
        if sucess is True and curtotal < frm_cnt:
            hfile.write(video_frame)
            curtotal = curtotal + 1
        else:
            hfile.release()
            camera.release()
    print(target_file, '-total frames:%d'%(curtotal))
    
    

def process4subj(subj, rootpath, savepath):
    data_path = rootpath + str(subj + 1) + '/sub%d' % (subj + 1) + '/splitraw/'
    data = sio.loadmat(data_path + 'eeg_data.mat')
    peri_aviable = True
    if data['gsr_datas'].shape[0]==0 or data['ppg_datas'].shape[0]==0:
        print('subject %d, invalid gsr and ppg.'%(subj))
        peri_aviable = False
    
    eeg = data['eeg_datas']
    eeg_datas = eeg[:, eeg[-1, :] == 40]
    
    if peri_aviable:
        gsr = data['gsr_datas']
        ppg = data['ppg_datas']
        gsr_fea = data['gsr_fea_datas']
        ppg_fea = data['ppg_fea_datas']
        gsr_datas = gsr[:, gsr[-1, :] == 40]
        ppg_datas = ppg[:, ppg[-1, :] == 40]
        gsr_fea_datas = gsr_fea[:, gsr_fea[-1, :] == 40]
        ppg_fea_datas = ppg_fea[:, ppg_fea[-1, :] == 40]
    else:
        gsr_datas = []
        ppg_datas = []
        gsr_fea_datas = []
        ppg_fea_datas = []
    
    
    for vid in range(32):
        eeg_cur = eeg[:, eeg[-1,:] == vid]
        if peri_aviable:
            gsr_cur = gsr[:, gsr[-1, :] == vid]
            ppg_cur = ppg[:, ppg[-1, :] == vid]
            gsr_fea_cur = gsr_fea[:, gsr_fea[-1, :] == vid]
            ppg_fea_cur = ppg_fea[:, ppg_fea[-1, :] == vid]
        
        eeg_len = eeg_cur.shape[1]/EEG_SRATE
        
        if peri_aviable:
            gsr_len = gsr_cur.shape[1]/GSR_SRATE
            ppg_len = ppg_cur.shape[1]/PPG_SRATE
            gsr_fea_len = gsr_fea_cur.shape[1]/51
            ppg_fea_len = ppg_fea_cur.shape[1]/45
        
        vlen, totalfrms = videolen(data_path+'%d.mp4'%(vid))
        
        if peri_aviable:
            data_length = int(min(eeg_len, gsr_len, gsr_fea_len, ppg_len, ppg_fea_len, vlen))
        else:
            data_length = int(min(eeg_len, vlen))
        
        eeg_cur = eeg_cur[:, -data_length*EEG_SRATE:]
        if peri_aviable:
            gsr_cur = gsr_cur[:, -data_length*GSR_SRATE:]
            ppg_cur = ppg_cur[:, -data_length*PPG_SRATE:]
            gsr_fea_cur = gsr_fea_cur[:, -data_length*51:]
            ppg_fea_cure = ppg_fea_cur[:, -data_length*45:]
        
        eeg_datas = np.hstack((eeg_datas, eeg_cur))
        if peri_aviable:
            gsr_datas = np.hstack((gsr_datas, gsr_cur))
            ppg_datas = np.hstack((ppg_datas, ppg_cur))
            gsr_fea_datas = np.hstack((gsr_fea_datas, gsr_fea_cur))
            ppg_fea_datas = np.hstack((ppg_fea_datas, ppg_fea_cur))
        
        if not os.path.exists(savepath + '%d/'%(subj+1)):
            os.mkdir(savepath + '%d/'%(subj+1))
        
        cutvideo(data_path + '%d.mp4'%(vid), savepath + '%d/'%(subj+1) + '%d.mp4'%(vid), totalfrms-data_length*30, data_length*30)
        
    sio.savemat(savepath+'%d/datas.mat'%(subj+1), {'eeg_datas':eeg_datas, 'gsr_datas':gsr_datas, 'gsr_fea_datas':gsr_fea_datas, 'ppg_datas':ppg_datas, 'ppg_fea_datas':ppg_fea_datas, 'dis_label':data['dis_label']})
        
    
    

# the main function for data alignment
def mainproc(rootpath='./', savepath='./'):
    # process for each subject
    for subj in [1,2,5,6,7,8,9,10,11,12,14,15,18,19,20,21,22,23,24,25,26,28,29,30,32,33,34,35]:
        process4subj(subj, rootpath, savepath)


if __name__ == '__main__':
    mainproc(savepath='F:/MixedEmoR/')