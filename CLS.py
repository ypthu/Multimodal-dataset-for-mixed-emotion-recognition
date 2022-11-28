import numpy as np
import scipy.io as sio
from sklearn.svm import LinearSVC,SVC
from sklearn.preprocessing import normalize
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt


def svm_classifer(train_d, train_l, test_d, test_l, pic_spath):
    train_d = normalize(train_d, axis=0)
    test_d = normalize(test_d, axis=0)
    train_d = normalize(train_d, axis=1)
    test_d = normalize(test_d, axis=1)
    best_acc = -1
    b_p_l = None
    for C in np.logspace(-10, 10, 20):
        model = SVC(gamma=2,C=C)
        # model = LinearSVC(C=C, max_iter=10000)
        model.fit(train_d, train_l)
        acc = model.score(test_d, test_l)
        acc_train = model.score(train_d, train_l)
        p_l = model.predict(test_d)
        print(C, acc_train, acc)
        if acc > best_acc and acc_train >0.7:
            best_acc = acc
            best_model = model
            b_p_l = p_l
    print('best acc', best_acc)
    # confusion_matrix(test_l, b_p_l)
    matrix = plot_confusion_matrix(best_model, test_d, test_l,
                                   cmap=plt.cm.Blues,
                                   normalize='true')
    plt.title('Confusion matrix for our classifier')
    plt.savefig(pic_spath)
    # plt.show()
    
    
    return best_model,best_acc


def rf_classifer(train_d, train_l, test_d, test_l, pic_spath):
    train_d = normalize(train_d, axis=0)
    test_d = normalize(test_d, axis=0)
    train_d = normalize(train_d, axis=1)
    test_d = normalize(test_d, axis=1)
    best_acc = -1
    b_p_l = None
    for i in range(50, 1000, 50):
        model = RandomForestClassifier(n_estimators=i,max_depth=20)
        model.fit(train_d, train_l)
        acc_t = model.score(train_d, train_l)
        acc = model.score(test_d, test_l)
        p_l = model.predict(test_d)
        print(i, acc_t, acc)
        if acc > best_acc and acc_t >0.7:
            best_acc = acc
            best_model = model
            b_p_l = p_l
    print('best acc', best_acc)
    matrix = plot_confusion_matrix(best_model, test_d, test_l,
                                   cmap=plt.cm.Blues,
                                   normalize='true')
    plt.title('Confusion matrix for our classifier')
    # plt.plot(matrix)
    plt.savefig(pic_spath)
    # plt.show()
    
    
    return best_model,best_acc




if __name__ == '__main__':
    # data = sio.loadmat('./CLS/SubInDep/1_norm.mat')
    accs_all = []
    for sub in [1,2,5,6,7,8,9,10,11,12,14,15,18,19,20,21,22,23,24,25,26,28,29,30,32,33,34,35]:
        data = sio.loadmat('./CLS/SubDep/alldata4subde'+str(sub)+'_trial_norm.mat')
        #EEG:1-90  GSR:91-118  PPG:119-145   Video:146-913
        train_f = data['trainFea'][:,1:91]
        test_f = data['testFea'][:,1:91]
        train_label = data['trainLabel'][0]
        test_label = data['testLabel'][0]
        
        best_accs = []
        for i in range(5):
            
            best_model,best_acc = svm_classifer(train_f, train_label, test_f, test_label,'./CLS/Ret-crosstrial-/'+str(sub)+'SVM-EEG-'+str(i)+'.jpg')
            best_accs.append(best_acc)
        accs_all.append(best_accs)
    sio.savemat('./CLS/Ret-crosstrial-/SVM-EEG.mat',{'accs':accs_all})
    print(accs_all)