import os
import numpy as np
from scipy import io as sio
from scipy.signal import butter, lfilter, hann

from typing import List, Tuple

def extract_psd_feature(raw_data: np.array, sample_freq: int, window_size: int,
                        freq_bands: List[Tuple[int, int]], stft_n=256):
    n_channels, n_samples = raw_data.shape
    
    point_per_window = int(sample_freq * window_size)
    window_num = int(n_samples // point_per_window)
    psd_feature = np.zeros((window_num, len(freq_bands), n_channels))
    
    for window_index in range(window_num):
        start_index, end_index = point_per_window * window_index, point_per_window * (window_index + 1)
        window_data = raw_data[:, start_index:end_index]
        hdata = window_data * hann(point_per_window)
        fft_data = np.fft.fft(hdata, n=stft_n)
        energy_graph = np.abs(fft_data[:, 0: int(stft_n / 2)])
        
        for band_index, band in enumerate(freq_bands):
            band_ave_psd = _get_average_psd(energy_graph, band, sample_freq, stft_n)
            psd_feature[window_index, band_index, :] = band_ave_psd
    return psd_feature


def extract_de_feature(raw_data: np.array, sample_freq: int, window_size: int,
                       freq_bands: List[Tuple[int, int]], stft_n=256):
    psd_feature = extract_psd_feature(raw_data, sample_freq, window_size, freq_bands, stft_n)
    return 0.5 * np.log(psd_feature) + 0.5 * np.log(2 * np.pi * np.exp(1) / round(sample_freq / stft_n))


def _get_average_psd(energy_graph, freq_bands, sample_freq, stft_n=256):
    start_index = int(np.floor(freq_bands[0] / sample_freq * stft_n))
    end_index = int(np.floor(freq_bands[1] / sample_freq * stft_n))
    # ave_psd = np.mean(energy_graph[:, start_index - 1:end_index] ** 2, axis=1)
    ave_psd = np.mean(energy_graph[:, start_index:end_index+1] ** 2, axis=1)
    return ave_psd


def fea4subj(datafile):
    data = sio.loadmat(datafile)
    eeg_datas = data['eeg_datas']

    freq_bands = [(1, 4), (4, 8), (8, 14), (14, 31), (31, 49)]
    data = {}
    vids = []
    de_feas = None
    for i in range(32):
        data[i] = eeg_datas[:, eeg_datas[-1,:]==i]
        de_fea = extract_de_feature(data[i][:-1, :], 300, 1, freq_bands)
        if de_feas is None:
            de_feas = de_fea
        else:
            de_feas = np.concatenate((de_feas, de_fea))
        vids = np.append(vids, np.ones(de_fea.shape[0], np.int32)*i)
        
    fparts = os.path.split(datafile)
    savepath = os.path.join(fparts[0], 'eegfea.mat')
    sio.savemat(savepath, {'feas':de_feas, 'vids':vids})
    

def fea4subjs(rootpath):
    for i in range(35):
        filepath = rootpath+str(i+1)+'/datas.mat'
        fea4subj(filepath)

if __name__=='__main__':
    fea4subjs('../')