# Multimodal-dataset-for-mixed-emotion-recognition
This file introduces the related source code of the project "Multimodal Dataset for Mixed Emotion Recognition".

## 1. General Information
This folder contains the source code (Matlab and Python scripts) used for data preprocessing, feature extraction and mixed emotion classification. Details for each script is as follows:
1. PreprocessEEG.m: Preprocess steps for raw EEG data, including channel selection (selected 18 channels from 24 channels) , re-reference operation, data filtering, and ICA etc.
2. Pip_ICARecon.m: Script for reconstruction of EEG data from ICA components obtained by last step.
3. Format_Data.m: The function of this script is to seperate the preprocessed  EEG data and original GSR and PPG data into individual trials. 
4. Format_video.py: This python script aims to divide the whole face video of a subject into sub video clips corresponding to each trial.
5. AlignAllData.py: This script align all signals (i.e., EEG, GSR, PPG and face video) of each trial with the end of the trial as reference point.
6. fea4eeg.py: This python script extracts differential entropy (DE) features from 5 frequency bands (i.e., \delta (1-3Hz), \theta (4-7Hz), \alpha (8-13Hz), \beta (14-30Hz) and \gamma (31-50Hz)) of each channel (totally 18 channels).
7. perifeaext.py: The function of this script is to extract both time domain and frequency domain features from GSR and PPG signals. Note that preprocessing steps (band pass filtering) are implemented for both GSR and PPG before feature extraction.
8. LBP-TOP.py: This script implements lbp-top features from video clips.
9. PrepareFeatures4Subj.m: This matlab script puts EEG features, GSR features, PPG features and LBP-TOP features together.
10. PrepareData4CLS_SubDep.m: The PrepareData3CLS_SubDep function helps to prepare the training set and test set for positive, negative and mixed emotion classification. The signal data of each trial is divided into two parts according to 4:1, and the first and second parts of all trials of a subject form the training and test set respectively. 
11. CLS.py: We implement emotion classification in this script. We test combinations of features from different modalities and two typical classifiers (SVM and RF). The experiment is carried out for each individual subject, and we use the average of 5 runs as the results for each subject. 
 

## Usage
1. The Matlab version is R2019b.
2. We use EEGLab Matlab toolbox for eeg signal processing, and the corresponding version is v2021.1.
3. Python 3.8 is used to run all python scripts, and to process face videos, opencv-python 4.5 is needed.
4. The scripts should to be run in the order in which they were introduced in section 'General Information'.
