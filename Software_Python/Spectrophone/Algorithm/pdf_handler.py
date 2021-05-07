'''
Created on 06.06.2018

all functions to create pdfs to save any kind of data

@author: Philipp
'''
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools

'''
main method to control which documents will be created
'''
def createTestresults(annotations, confMatrix, rocData, keyNumbers, acc, crossVal, folderpath): 
  
    #check that save path exists
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        
    plotKeyNumbers(annotations, keyNumbers, acc, folderpath)
    plotROCCurves(rocData, annotations, folderpath)
    plotConfMatrix(confMatrix, annotations, folderpath, False)
    plotConfMatrix(confMatrix, annotations, folderpath, True)
    plotCrossValidation(crossVal, folderpath)
    pass
    
    
'''
plots all informations about cross validations
'''
def plotCrossValidation(crossVal, folderpath):
    fig = plt.figure(1)
    plt.clf()
    
    columns = ('Accuracy', 'Standard deviation')
    rows = ('10-KFold', 'LeaveOneOut')
    data = []
    data.append([np.round(crossVal[0][1],3), np.round(crossVal[0][2],4)])
    data.append([np.round(crossVal[1][1],3), np.round(crossVal[1][2],4)])
    
    #Table - Main table
    fig.subplots_adjust(left=0.2,top=0.8, wspace=1)
    ax = plt.subplot2grid((4,3), (0,0), colspan=2, rowspan=2)
    ax.table(cellText=data, rowLabels=rows, colLabels=columns, loc="upper center")
    ax.axis("off")
    
    plt.title("Cross Validation")   
    plt.savefig(folderpath + 'Cross_Validation.pdf', format='pdf', bbox_inches="tight")
    plt.close(fig)
    pass


'''
plots the confusion matrix of the model
'''
def plotConfMatrix(confMatrix, annotations, folderpath, normalize=False, cmap=plt.cm.get_cmap('Blues')):
    """
    Normalization can be applied by setting `normalize=True`.
    """
    fig = plt.figure()
    plt.rcParams.update({'font.size': 5})

    
    if normalize:
        confMatrix = confMatrix.astype('float') / confMatrix.sum(axis=1)[:, np.newaxis]
        confMatrix = np.rint(np.multiply(confMatrix,100))
        confMatrix = confMatrix.astype(int)
        plt.title("Confusion Matrix normalized", fontsize=15)
    else:
        plt.title("Confusion Matrix", fontsize=15)


    plt.imshow(confMatrix, interpolation='nearest', cmap=cmap)
    
    plt.colorbar()
    
    plt.xticks(range(len(annotations)), [column[0] for column in annotations], rotation=90)
    plt.yticks(range(len(annotations)), [column[0] for column in annotations])
    plt.tick_params(axis = 'both', which = 'major', labelsize = 5)

    fmt = 'd'
    thresh = confMatrix.max() / 2.
    for i, j in itertools.product(range(confMatrix.shape[0]), range(confMatrix.shape[1])):
        plt.text(j, i, format(confMatrix[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if confMatrix[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.ylabel("Classes", fontsize=10)
    plt.xlabel("Predicted Classes", fontsize=10)
    if normalize:
        plt.savefig(folderpath + 'Confusion_Matrix_Norm.pdf', format='pdf', bbox_inches="tight")
    else:
        plt.savefig(folderpath + 'Confusion_Matrix_Abs.pdf', format='pdf', bbox_inches="tight")
    plt.close(fig)
    pass




'''
plots all informations about single keynumbers
'''
def plotKeyNumbers(annotations, keyNumbers, accuracy, folderpath):
    
    
    columns = ('Precision', 'Recall', 'F1-Score', 'Support')
    rows = []
    data = []
    
    for className in annotations:
        rows.append(className[0])
        
    
    row = [] 
    for c in range(len(annotations)):
        row.insert(len(row),round(keyNumbers[0][c],2))
        row.insert(len(row),round(keyNumbers[1][c],2))
        row.insert(len(row),round(keyNumbers[2][c],2))
        row.insert(len(row),round(keyNumbers[3][c],2))
        
        data.append(row)
        row = []
    
    
    fig = plt.figure(1)
    plt.clf()
    plt.rcParams.update({'font.size': 5})
    
    
    #Table - Main table
    fig.subplots_adjust(left=0.2,top=0.8, wspace=1)
    ax = plt.subplot2grid((4,3), (0,0), colspan=2, rowspan=2)
    ax.table(cellText=data, rowLabels=rows, colLabels=columns, loc="upper center")
    ax.axis("off")

    plt.title('Key Numbers\nTotal model accuracy: ' + str(round(accuracy,3)) + "%", fontsize=15)   
    plt.savefig(folderpath + 'Key_Numbers.pdf', format='pdf', bbox_inches="tight")
    plt.close(fig)
    
    
'''
plots the roc curves of the model
'''
def plotROCCurves(rocData, annotations, folderpath):
    
    fpr = rocData[0]
    tpr = rocData[1]
    roc_auc = rocData[2]
    fig = plt.figure()
    lw = 2
    for i in range(len(annotations)):
        plt.plot(fpr[i], tpr[i], lw=lw, label= annotations[i][0] + ' (AUC = %0.2f)' % roc_auc[i])
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=10)
        plt.ylabel('True Positive Rate', fontsize=10)
        plt.title('Receiver operating characteristic', fontsize=15)
        plt.legend(loc="lower right")
        plt.savefig(folderpath + "ROC_Curves" + ".pdf", format='pdf', bbox_inches="tight")
    plt.close(fig)
    pass
    
    