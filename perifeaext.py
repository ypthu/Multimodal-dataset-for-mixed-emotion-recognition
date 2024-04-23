import os
import fnmatch
# from ppg import BASE_DIR
# from ppg.utils import exist, load_json, dump_json
# from ppg.signal import smooth_ppg_signal, extract_ppg_single_waveform
from scipy import io as sio
from scipy import signal
from scipy.interpolate import CubicSpline
import numpy as np

from scipy import io as sio
from scipy.signal import butter, lfilter, hann
from typing import List, Tuple
        

def butter_lowpass(data, cutfreq, fs, order=3):
    cutfreq = cutfreq/(0.5*fs)
    b, a = signal.butter(order, cutfreq, btype='low')
    
    data_filtered = signal.filtfilt(b, a, data)
    return data_filtered


def butter_bandpass(data, lowcut, highcut, fs, order=3):
    nyq = 0.5*fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    
    data_filtered = signal.filtfilt(b, a, data)
    return data_filtered

def featurefromgsr(gsr_data, fs=4, wndsize=5, slide=1):
    n_samples = gsr_data.shape[0]
    point_per_window = int(fs*wndsize)
    window_num = int((n_samples - point_per_window) // int(fs * slide))+1
    
    feas = None
    for window_index in range(window_num):
        start_index, end_index = (fs * slide) * window_index, (fs * slide) * window_index + point_per_window
        window_data = gsr_data[start_index:end_index]
        
        fea = statisfeatures(window_data)
        fea_1d = statisfeatures(np.diff(window_data))
        fea_2d = statisfeatures(np.diff(np.diff(window_data)))
        fea_freq = freqfeatures(window_data)
        freqs, psd = signal.welch(window_data, 4)
        avg_psd = np.mean(psd)
        fea_row = [fea['median'], fea['mean'], fea['std'], fea['min'], fea['max'], fea['minratio'], fea['maxratio'],
                   fea_1d['median'], fea_1d['mean'], fea_1d['std'], fea_1d['min'], fea_1d['max'], fea_1d['minratio'], fea_1d['maxratio'],
                   fea_2d['median'], fea_2d['mean'], fea_2d['std'], fea_2d['min'], fea_2d['max'], fea_2d['minratio'], fea_2d['maxratio'],
                   fea_freq['median'], fea_freq['mean'], fea_freq['std'], fea_freq['min'], fea_freq['max'], fea_freq['range'],
                   avg_psd]

        if feas is None:
            feas = np.array(fea_row)
        else:
            feas = np.vstack((feas, fea_row))
    return feas
        
        
        

def featurefromppg(ppg_data, fs=100, wndsize=5, slide=1):
    n_samples = ppg_data.shape[0]
    point_per_window = int(fs * wndsize)
    window_num = int((n_samples - point_per_window) // int(fs * slide)) + 1
    ppg_data = butter_bandpass(ppg_data, 0.5, 8, 100)

    feas = None
    for window_index in range(window_num):
        start_index, end_index = (fs * slide) * window_index, (fs * slide) * window_index + point_per_window
        window_data = ppg_data[start_index:end_index]

        fea = statisfeatures(window_data)
        fea_1d = statisfeatures(np.diff(window_data))
        fea_2d = statisfeatures(np.diff(np.diff(window_data)))
        fea_freq = freqfeatures(window_data)
        fea_row = [fea['median'], fea['mean'], fea['std'], fea['min'], fea['max'], fea['minratio'], fea['maxratio'],
                   fea_1d['median'], fea_1d['mean'], fea_1d['std'], fea_1d['min'], fea_1d['max'], fea_1d['minratio'], fea_1d['maxratio'],
                   fea_2d['median'], fea_2d['mean'], fea_2d['std'], fea_2d['min'], fea_2d['max'], fea_2d['minratio'], fea_2d['maxratio'],
                   fea_freq['median'], fea_freq['mean'], fea_freq['std'], fea_freq['min'], fea_freq['max'], fea_freq['range']]
        
        if feas is None:
            feas = np.array(fea_row)
        else:
            feas = np.vstack((feas, fea_row))
        
    return feas

def perifeaext(rootpath):
    invalidSub = []
    for i in range(35):
        filepath = rootpath+str(i+1)+'/datas.mat'
        data_org = sio.loadmat(filepath)
        ppg_datas = data_org['ppg_datas']
        gsr_datas = data_org['gsr_datas']
        
        if ppg_datas.shape[0] == 0:
            invalidSub = np.append(invalidSub, i+1)
            continue
        
        
        feas_gsr = None
        feas_ppg = None
        vids = []
        for j in range(32):
            print(i,'===',j)
            data_ppg = ppg_datas[0, ppg_datas[1,:]==j]
            # data_ppg_s = smooth_ppg_signal(signal=data_ppg[i], sample_rate=100)
            ds_ppg = data_ppg #butter_bandpass(data_ppg, 0.5, 8, 100)
            data_gsr = gsr_datas[0, gsr_datas[1,:]==j]
            ds_gsr = data_gsr #butter_lowpass(data_gsr, 1.0, 4)
            gsr_fea = featurefromgsr(ds_gsr)
            ppg_fea = featurefromppg(ds_ppg)
            vids = np.append(vids, np.ones(gsr_fea.shape[0], np.int32) * j)
            if feas_gsr is None:
                feas_gsr = gsr_fea
            else:
                feas_gsr = np.vstack((feas_gsr, gsr_fea))
            
            if feas_ppg is None:
                feas_ppg = ppg_fea
            else:
                feas_ppg = np.vstack((feas_ppg, ppg_fea))

        savepath = os.path.join(rootpath+str(i+1), 'perifea.mat')
        sio.savemat(savepath, {'feas_gsr': feas_gsr, 'feas_ppg': feas_ppg, 'vids': vids})
    print('Invalid subjects:', invalidSub)
                
            



def extract_psd_feature(raw_data: np.array, sample_freq: int, window_size: int,
                        freq_bands: List[Tuple[int, int]], slide = 1, stft_n=256):
    n_samples = raw_data.shape[0]
    
    point_per_window = int(sample_freq * window_size)
    window_num = int((n_samples - point_per_window) // int(sample_freq * slide))+1
    psd_feature = np.zeros((window_num))
    
    for window_index in range(window_num):
        start_index, end_index = (sample_freq *slide) * window_index, (sample_freq *slide) * window_index + point_per_window
        window_data = raw_data[start_index:end_index]
        # hdata = window_data * hann(point_per_window)
        freqs, psd = signal.welch(window_data, 4)
        avg_psd = np.mean(psd)
        psd_feature[window_index] = avg_psd
        # L = len(hdata)
        #_stft_n = int(np.power(2, nextpow2(L)))
        # fft_data = np.fft.fft(hdata, n=stft_n)
        # energy_graph = np.abs(fft_data[0: int(stft_n / 2)])
        #
        # for band_index, band in enumerate(freq_bands):
        #     band_ave_psd = _get_average_psd(energy_graph, band, sample_freq, int(stft_n/2))
        #     psd_feature[window_index, band_index, :] = band_ave_psd
    return psd_feature

def _get_average_psd(energy_graph, freq_bands, sample_freq, stft_n=256):
    start_index = int(np.floor(freq_bands[0] / sample_freq * stft_n))
    end_index = int(np.floor(freq_bands[1] / sample_freq * stft_n))
    # ave_psd = np.mean(energy_graph[:, start_index - 1:end_index] ** 2, axis=1)
    ave_psd = np.mean(energy_graph[start_index:end_index] ** 2)
    return ave_psd

def nextpow2(a):
    if a == 0:
        return 0
    else:
        return np.ceil(np.log2(a))
    
def statisfeatures(data):
    fea = {}
    fea['median'] = np.median(data)
    fea['mean'] = np.mean(data)
    fea['std'] = np.std(data)
    fea['min'] = np.min(data)
    fea['max'] = np.max(data)
    fea['minratio'] = np.sum(data == fea['min'])/len(data)
    fea['maxratio'] = np.sum(data == fea['max'])/len(data)
    return fea
    
    
def freqfeatures(data, useamp=False):
    fre_data = np.fft.fft(data)
    fre_fea = {}
    
    if useamp:
        fre_fea['median'] = abs(np.median(fre_data))
        fre_fea['mean'] = abs(np.mean(fre_data))
        fre_fea['std'] = abs(np.std(fre_data))
        fre_fea['min'] = abs(np.min(fre_data))
        fre_fea['max'] = abs(np.max(fre_data))
        fre_fea['range'] = abs(fre_fea['max'] - fre_fea['min'])
        return fre_fea
    else:
        fre_fea['median'] = np.median(fre_data)
        fre_fea['mean'] = np.mean(fre_data)
        fre_fea['std'] = np.std(fre_data)
        fre_fea['min'] = np.min(fre_data)
        fre_fea['max'] = np.max(fre_data)
        fre_fea['range'] = fre_fea['max'] - fre_fea['min']
        return fre_fea

    

if __name__=='__main__':
    perifeaext('../')
