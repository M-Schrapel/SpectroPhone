'''
Created on 03.07.2018

all functions to prepare the images before classification

@author: Philipp
'''
import os
import cv2
from sklearn.externals import joblib
from Algorithm.histogram import calcHistogram
from Evaluation.evaluate import *
from Algorithm.csv_handler import writeImageData, write_CSV
from sklearn import preprocessing



'''
 Procedure for data preparation
'''
def prepareData():
    
    print("Load images from dataset")
    imageData, labels, names, annotations = loadImage(r"C:\Users\Philipp\Desktop\Spectrophone Datensatz")
        
    
    print("Scale image data")
    scaledImageData = scaleImageData(imageData, os.path.abspath(r"Prepared/scaleModel.pkl"))
    

    print("Create Folder")
    for folder in annotations:
        if not os.path.exists(os.path.abspath(r"Prepared/" + str(folder[0]))):
            os.makedirs(os.path.abspath(r"Prepared/" + str(folder[0])))
    
    
    print("Save data")
    for index, images in enumerate(scaledImageData):
        writeImageData(images, os.path.abspath(r"Prepared/" + annotations[labels[index]-1][0] + "/" + names[index] + ".csv"))
        
        
    print("Save annotations")
    write_CSV(annotations, os.path.abspath(r"Prepared/Annotations.csv"))
        
    print("Preparation done")
    
    
    
"""
    Load images from given path to an array
"""    
def loadImage(folderPath):
    imageData = []
    labels = []
    names = []
    annotations = read_CSV(folderPath + r"\Annotations.csv")
    numberSets = 30

    
    for path, subdirs, files in os.walk(folderPath):
        for name in files:
            if name.endswith(".jpg"):
                numberPos = [i for i, ltr in enumerate(name) if ltr == '_']
                setNum = int(name[numberPos[0]+1:numberPos[0]+3]) - 1
                imgNum = int(name[numberPos[1]+1:numberPos[1]+3])
                if(setNum < numberSets):
                    print(os.path.join(path, name))
                    names.append(name)
                    imageData.append(calcHistogram(cv2.imread((os.path.join(path, name)))))
                    for prefix in range(len(annotations)):
                        if name.startswith(annotations[prefix][0]):
                            labels.append(annotations[prefix][1])
            
    labels = list(map(int, labels))
    return imageData, labels, names, annotations




"""
    Scale data to a given range from 0 to 1
"""    
def scaleImageData(unscaledData, savePath):
    
    min_max_scaler = preprocessing.MinMaxScaler()
    scaledData = min_max_scaler.fit_transform(unscaledData)
    
    joblib.dump(min_max_scaler, savePath)
    
    return scaledData

