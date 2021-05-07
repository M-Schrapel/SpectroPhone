'''
Created on 06.06.2018

all functions needed to use a svm

@author: Philipp
'''

import numpy as np
import os
from Algorithm.csv_handler import read_CSV
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support


"""
    tests the SVM with the given data and returns confusion matrix for a multiple class problem
"""
def calcConfMatrix(clf, testData, testLabel):
    
    y_pred = clf.predict(testData)
    
    # Compute confusion matrix
    confMatrix = confusion_matrix(testLabel, y_pred)
    np.set_printoptions(precision=2)
    acc = accuracy_score(testLabel, y_pred)

    keyNumbers = precision_recall_fscore_support(testLabel, y_pred)
    print("Accuracy: " + str(acc))


    return confMatrix, keyNumbers, acc


"""
    create data of the ROC curves
"""
def multiclassROCcurve(clf, testData, testLabel, annotations):
    rocData = []  
    
    # Binarize the output
    classes= np.arange(0, len(annotations))
    testLab = label_binarize(testLabel, classes)
    n_classes = testLab.shape[1]
    
    
    # Learn to predict each class against the other
    y_score = clf.decision_function(testData)
    
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], threshold = roc_curve(testLab[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    rocData.append(fpr)
    rocData.append(tpr)
    rocData.append(roc_auc)
    

    return rocData


"""
    Reshape data to one dimensional array and create labels
"""
def readInData(lightMode, ledMode, annotations):
    
    imageData = []
    neededImages = []
    numberSets = 30
    
    
    # check for needed images of tis led and light mode
    if lightMode == 1:
        if ledMode == 1:
            neededImages = [5]
        elif ledMode == 2:
            neededImages = [10]
        elif ledMode == 3:
            neededImages = [5,10,15]
    elif lightMode == 2:
        if ledMode == 1:
            neededImages = [1,5]
        elif ledMode == 2:
            neededImages = [6,10]
        elif ledMode == 3:
            neededImages = [1,5,6,10,11,15]
    elif lightMode == 3:
        if ledMode == 1:
            neededImages = [1,2,3,4,5]
        elif ledMode == 2:
            neededImages = [6,7,8,9,10]
        elif ledMode == 3:
            neededImages = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        
     
   # read in every needed image data path and put it in a list
    for className in annotations:
        filepathes = np.empty([numberSets, len(neededImages)], dtype = object)
        for path, subdirs, files in os.walk(os.path.abspath(r"Prepared//" + className[0])):
            for name in files:
                if name.endswith(".csv"):
                    numberPos = [i for i, ltr in enumerate(name) if ltr == '_']
                    setNum = int(name[numberPos[0]+1:numberPos[0]+3]) - 1
                    imgNum = int(name[numberPos[1]+1:numberPos[1]+3])
                    if(imgNum in neededImages and setNum < numberSets):
                        filepathes[setNum][neededImages.index(imgNum)] = os.path.join(path, name)    
                    
        imageData.append([int(className[1])-1, [filepathes]])
    
    
  
    images = []
    labels =[]
    
    # read in data of every needed image and create labels
    for imageClass in imageData:
        for imageSetOTClass in imageClass[1][0]:
            labels.append(imageClass[0])
            imageSet = []
            for imageOTClass in imageSetOTClass:
                for rgbChannel in read_CSV(str(imageOTClass)):
                    imageSet.extend(list(map(float, rgbChannel)))
            images.append(imageSet)


    npImages = np.asarray(images)
    npLabels = np.asarray(list(map(int, labels)))

    return npImages, npLabels

