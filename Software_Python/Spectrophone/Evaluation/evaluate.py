'''
Created on 23.05.2018

control of training and test of the new svm models

@author: Philipp Etgeton
'''
import os
import numpy as np
from Algorithm.svm_helper import readInData, multiclassROCcurve, calcConfMatrix
from Algorithm.csv_handler import read_CSV
from Algorithm.pdf_handler import createTestresults
from sklearn.svm import LinearSVC, SVC
from sklearn.externals import joblib
from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold, cross_val_score, LeaveOneOut, GridSearchCV




"""
    Procedure for training the model
"""
def trainModel(ledMode, lightMode):
    
    
    print("Read dataset path")
    annotations = read_CSV(os.path.abspath(r"Prepared/Annotations.csv"))
    
    
    
    print("Read csv files and create labels")
    images, labels = readInData(lightMode, ledMode, annotations)

    
    
    print("Split image dataset")
    sss = StratifiedShuffleSplit(n_splits = 1, test_size=0.3)
    for train_index, test_index in sss.split(images, labels):
        trainData, testData = images[train_index], images[test_index]
        trainLabel, testLabel = labels[train_index], labels[test_index]
    
    
    
    print("Train estimator")
    trainParam = ['linear', 60]
    clf = SVC(kernel=trainParam[0], C=trainParam[1])


    #clf = LinearSVC(C=trainParam[1])
    
    # function to find the best kernel parameter
    '''
    print("Tuning model parameter")
    param_grid = [
        {'C': [1, 10, 100, 500, 1000], 'kernel': ['linear']},
        {'C': [1, 10, 100, 500, 1000], 'gamma': [0.1, 0.01, 0.001, 0.0001], 'kernel': ['rbf']}]
    svc = SVC()
    grid = GridSearchCV(svc, param_grid)
    grid.fit(images, labels)
    print(grid)
    # summarize the results of the grid search
    print("Best Score")
    print(grid.best_score_)
    print("Best Params")
    print(grid.best_params_)
    input()
    '''
    
    print("Start KFold cross validation")
    crossVal = []
    k_fold = StratifiedKFold(n_splits=10, shuffle=True)
    crossValScore = cross_val_score(clf, images, labels, cv=k_fold)
    accuracy = np.mean(crossValScore)
    standD = np.std(crossValScore)
    crossVal.append([crossValScore, accuracy, standD])
    print("Accuracy KFold: " + str(accuracy))
    print("Standard deviation KFold: " + str(standD))
    
    
    # function for a leaveoneout cross validation
    '''
    print("Start LeaveOneOut cross validation")
    loo = LeaveOneOut()
    crossValScore = cross_val_score(clf, images, labels, cv=loo)
    accuracy = np.mean(crossValScore)
    standD = np.std(crossValScore)
    crossVal.append([crossValScore, accuracy, standD])
    print("Accuracy LOO: " + str(accuracy))
    print("Standard deviation LOO: " + str(standD))
    '''
    # leaveOneOut dummy data
    crossVal.append([0, 0, 0])
   
   
   
    print("Start training Model")
    clf.fit(trainData, trainLabel)
    


    print("Save Model")
    modelSavePath = os.path.abspath(r"Evaluation\Training") + "\\LED" + str(ledMode) + "_Light" + str(lightMode) + "\\"
    if not os.path.exists(modelSavePath):
        os.makedirs(modelSavePath)
    joblib.dump(clf, modelSavePath + 'model.pkl')
    


    print("Calculate confusion Matrix")
    confMatrix, keyNumbers, acc = calcConfMatrix(clf, testData, testLabel)


   
    print("Calculate ROC curves")
    rocData = multiclassROCcurve(clf, testData, testLabel, annotations)
    print("Model tested")
    
    
    
    print("Generate Documents")
    savePath = os.path.abspath(r"Evaluation Documents") + "\\" + trainParam[0] + "_C" + str(trainParam[1]) + "\\LED" + str(ledMode) + "_Light" + str(lightMode) + "\\"
    createTestresults(annotations, confMatrix, rocData, keyNumbers, acc, crossVal, savePath)
    print("Documents generated")
    
    pass
    
    

    

   


