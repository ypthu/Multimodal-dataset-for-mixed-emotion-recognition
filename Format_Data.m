% format preprocessed data

rootpath = 'C:/学习/多模态情绪识别/多模态情绪分布数据集建立/MultiData/'

invalid = []
for j=[1,2,5,6,7,8,9,10,11,12,14,15,18,19,20,21,22,23,24,25,26,28,29,30,32,33,34,35]
   %% EEG
   file_name = '1_ICA_remcop.set'
   file_name_o = '1_ICA.set'
   EEG = pop_loadset('filename',file_name, 'filepath',[rootpath num2str(j) '/sub' num2str(j) '/']) 
   EEG_o = pop_biosig([rootpath num2str(j) '/sub' num2str(j) '/1_raw.edf']); 
   triggers =EEG_o.data(25,:);
   tri_inds = find(triggers > 0);
   tris = triggers(tri_inds);
   bg = find(tris==60);
   ed = size(tris,2);
   tri_inds_t= [];
   tris_t = [];
   for cur = bg:ed-1
       if (tris(cur+1)-tris(cur)) == 90
           tri_inds_t = [tri_inds_t, tri_inds(cur),tri_inds(cur+1)];
           tris_t = [tris_t, tris(cur), tris(cur+1)];
       end
   end
   tri_inds = tri_inds_t;%tri_inds(bg:end);
   tris = tris_t;%tris(bg:end);
   
   eeg_datas = [];
   if size(tri_inds, 2) == 68
       assert(tris(3)==50)
       for i=3:2:68
          assert((tris(i+1)-tris(i)) == 90)
          eeg_data = EEG.data(:, tri_inds(i):tri_inds(i+1)-1);
          vids = ones(1, size(eeg_data, 2))*(tris(i)-10);
          eeg_datas = [eeg_datas, [eeg_data;vids]];
       end
   end
   if ~exist([rootpath num2str(j) '/sub' num2str(j) '/splitraw'], 'dir')
      mkdir([rootpath num2str(j) '/sub' num2str(j) '/splitraw']) 
   end
%    save([rootpath num2str(j) '/sub' num2str(j) '/splitraw/eeg_data.mat'], 'eeg_datas');
   
   %% PPG and GSR
   gsr_ = csvread([rootpath num2str(j) '/' num2str(j) '/raw_gsr.csv']);
   gsr_data = gsr_(:,2)';
   triggers = gsr_(:,3)';
   tri_inds = find(triggers > 0);
   tris = triggers(tri_inds);
   bg = find(tris==60);
   ed = size(tris,2);
   tri_inds_t= [];
   tris_t = [];
   for cur = bg:ed-1
       if (tris(cur+1)-tris(cur)) == 90
           tri_inds_t = [tri_inds_t, tri_inds(cur),tri_inds(cur+1)];
           tris_t = [tris_t, tris(cur), tris(cur+1)];
       end
   end
   tri_inds = tri_inds_t;
   tris = tris_t;
   assert(tris(3)==50)
   gsr_datas = []
   if size(tri_inds, 2)==68
       for i=3:2:68
          assert((tris(i+1)-tris(i)) == 90)
          data_ = gsr_data(:, tri_inds(i):tri_inds(i+1)-1);
          vids = ones(1, size(data_, 2))*(tris(i)-10);
          gsr_datas = [gsr_datas, [data_;vids]];
       end
   end
   
   
   %%PPG
   ppg_ = csvread([rootpath num2str(j) '/' num2str(j) '/raw_ppg.csv']);
   ppg_data = ppg_(:,2)';
   triggers = ppg_(:,3)';
   tri_inds = find(triggers > 0);
   tris = triggers(tri_inds);
   bg = find(tris==60);
   ed = size(tris,2);
   tri_inds_t= [];
   tris_t = [];
   for cur = bg:ed-1
       if (tris(cur+1)-tris(cur)) == 90
           tri_inds_t = [tri_inds_t, tri_inds(cur),tri_inds(cur+1)];
           tris_t = [tris_t, tris(cur), tris(cur+1)];
       end
   end
   tri_inds = tri_inds_t;
   tris = tris_t;
   assert(tris(3)==50)
   ppg_datas = []
   if size(tri_inds, 2) ==68
       for i=3:2:68
          assert((tris(i+1)-tris(i)) == 90)
          data_ = ppg_data(:, tri_inds(i):tri_inds(i+1)-1);
          vids = ones(1, size(data_, 2))*(tris(i)-10);
          ppg_datas = [ppg_datas, [data_;vids]];
       end
   end
   
   
   if size(gsr_datas, 2)==0 || size(ppg_datas, 2)==0
       invalid = [invalid, j];
   end
   
   
   save([rootpath num2str(j) '/sub' num2str(j) '/splitraw/eeg_data.mat'], 'eeg_datas', 'gsr_datas', 'ppg_datas');
end

