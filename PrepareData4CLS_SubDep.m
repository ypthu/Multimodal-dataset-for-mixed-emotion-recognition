%% prepare data for subject dependent
function PrepareData4CLS_SubDep(rootpath, do_norm)
    if nargin < 2
       do_norm = false; 
    end
    subids = [1,2,5,6,7,8,9,10,11,12,14,15,18,19,20,21,22,23,24,25,26,28,29,30,32,33,34,35];
    labels = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2];
    totalsubs = length(subids);
    
    for k=1:totalsubs
        
        trainFea = [];
        trainLabel = [];
        testFea = [];
        testLabel = [];

        for i=k:k%totalsubs

           alldata = load(strcat(rootpath, '/features/', num2str(subids(i)),'.mat'));

           feas = alldata.feas;
           vids = alldata.vids;
           %dislabel = alldata.dis_label;
           %dataLabels = labels(vids'+1);

           for vid=0:31
               feas4v = feas(vids==vid,:);
               [r, c] = size(feas4v);
               if do_norm
                  min_ = min(feas4v);
                  max_ = max(feas4v);
                  feas4v = (feas4v-repmat(min_, r,1))./(repmat(max_-min_+0.0000001, r, 1));
               end

               [r,c] = size(feas4v);

               trainFea = [trainFea;feas4v(1:ceil(r*4/5),:)];
               trainLabel = [trainLabel, ones(1, ceil(r*4/5))*labels(vid+1)];
               testFea = [testFea;feas4v((ceil(r*4/5)+1):end,:)];
               testLabel = [testLabel, ones(1, r-ceil(r*4/5))*labels(vid+1)];

           end
        end
        if do_norm
            save(['./CLS/SubDep/alldata4subde', num2str(subids(k)), '_trial_norm.mat'], 'trainFea', 'trainLabel', 'testFea', 'testLabel');
        else
            save(['./CLS/SubDep/alldata4subde', num2str(subids(k)),'_trial_.mat'], 'trainFea', 'trainLabel', 'testFea', 'testLabel');
        end
    end
end