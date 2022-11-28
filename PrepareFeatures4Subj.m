% prepare features for subject

function PrepareFeatures4Subj(rootpath)
    subids = [1,2,5,6,7,8,9,10,11,12,14,15,18,19,20,21,22,23,24,25,26,28,29,30,32,33,34,35];
    totalsubs = length(subids);
    
    for i=1:totalsubs
       eeg_fea = load(strcat(rootpath, num2str(subids(i)), '/eegfea.mat'));
       per_fea = load(strcat(rootpath, num2str(subids(i)), '/perifea.mat'));
       video_fea = load(strcat(rootpath, num2str(subids(i)), '/videoFea.mat'));
       datas = load(strcat(rootpath, num2str(subids(i)), '/datas.mat'));
       
       feas = [];
       vids = [];
       for vid=0:31
           eeg_f_ = eeg_fea.feas(eeg_fea.vids==vid,:,:);
           [r,c,p] = size(eeg_f_);
           eeg_f_ = reshape(eeg_f_, [r, c*p]);
           gsr_f_ = per_fea.feas_gsr(per_fea.vids==vid, :);
           ppg_f_ = per_fea.feas_ppg(per_fea.vids==vid, :);
           video_f = video_fea.lbps_all(video_fea.vids==vid, :);
           feas = [feas;[eeg_f_(5:end,:), gsr_f_, ppg_f_, video_f(5:end,:)]];
           
           vids = [vids;ones(r-4,1)*vid];
       end
       save(strcat(rootpath, '/features/', num2str(subids(i)),'.mat'), 'feas', 'vids');
    end
end