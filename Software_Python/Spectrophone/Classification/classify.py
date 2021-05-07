'''
Created on 06.06.2018

@author: Philipp
'''
import os
from sklearn.externals import joblib
from Algorithm.csv_handler import read_CSV, write_CSV
from Classification.connection import *
from Algorithm.histogram import calcHistogram



def classification():
    
    annotations = read_CSV(os.path.abspath(r"Prepared/Annotations.csv"))
    
    print("Open Connection to smartphone app")
    sock = setupServer()
    
    
    print("Check for classification request")
    conn = checkClassifyRequest(sock)

    while(1):
        print("Waiting for images from smartphone app")
        images, ledMode, lightMode = receiveData(conn)
    
        
        print("Extract image data")
        imageData = []
        for img in images:
            imageData.append(calcHistogram(img))
        
        
        print("Scale image data")
        #scaledImageData = scaleImageData(imageData, os.path.abspath(r"Prepared/scaleModel.pkl"))
        scaledImageData = imageData
        
        reshapedData = []
        for img in scaledImageData:
            reshapedData.extend(img)
            
        
        print("Calculate Prediction")
        prediction = calcPrediction([reshapedData], ledMode, lightMode)
        print("Predicted Class is: " + annotations[prediction[0]][0] + " number "+ str(prediction[0]))
        
        print("send classification result to smartphone app")
        sendClassification(annotations[prediction[0]][0]+ "\n", conn)
        
    pass


def renamefiles():
    for path, subdirs, files in os.walk(r"C:\Users\Philipp\Desktop\Spectrophone Datensatz Test"):
        for name in files:
                if name.endswith(".jpg"):
                    numberPos = [i for i, ltr in enumerate(name) if ltr == '_']
                    setNum = int(name[numberPos[0]+1:numberPos[0]+3])
                    if(setNum >= 51):
                        newSetNum = setNum - 20
                        newName = name.replace(str(setNum), str(newSetNum))
                        os.rename(os.path.join(path, name), os.path.join(path, newName))


def classifyFolder():
    
    annotations = read_CSV(os.path.abspath(r"Prepared/Annotations.csv"))
    

    imageData = []
    ledMode = 3
    lightMode = 1
    logData = []
    neededImages = []
    
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
    
    for path, subdirs, files in os.walk(r"C:\Users\Philipp\Desktop\Spectrophone Datensatz Test"):
        for name in files:
                if name.endswith("_" + str(neededImages[-1]) + ".jpg"):
                    print(os.path.join(path, name))
                    imageData.append(cv2.imread((os.path.join(path, name))))

                    imageCalc = []
                    for img in imageData:
                        imageCalc.append(calcHistogram(img))
                    
                    scaledImageData = scaleImageData(imageCalc, os.path.abspath(r"Prepared/scaleModel.pkl"))
                    
                    reshapedData = []
                    for img in scaledImageData:
                        reshapedData.extend(img)
                        
                    prediction = calcPrediction([reshapedData], ledMode, lightMode)
                    print("Predicted Class is: " + annotations[prediction[0]][0])
                    logData.append(str(annotations[prediction[0]][0]))
                    if name.endswith("40_15.jpg"):
                        logData.append("Das war Klasse: " + name)
                        logData.append("---------------------------------------")

                    imageData = []
                elif name.endswith(".jpg"):
                    numberPos = [i for i, ltr in enumerate(name) if ltr == '_']
                    setNum = int(name[numberPos[0]+1:numberPos[0]+3]) - 1
                    imgNum = int(name[numberPos[1]+1:numberPos[1]+3])
                    if(imgNum in neededImages):
                        print(os.path.join(path, name))
                        imageData.append(cv2.imread((os.path.join(path, name))))

    write_CSV(logData, os.path.abspath(r"Prepared/logFile.csv"))
   

    pass


"""
    Scale data to a given range from 0 to 1
"""    
def scaleImageData(unscaledData, savePath):
    
    min_max_scaler = joblib.load(savePath)
    scaledData = min_max_scaler.transform(unscaledData)
    
    return scaledData


def calcPrediction(imageData, ledMode, lightMode):
    
    modelSavePath = os.path.abspath(r"Evaluation\Training") + "\\LED" + str(ledMode) + "_Light" + str(lightMode) + "\\"
    clf = joblib.load(modelSavePath + 'model.pkl')
    prediction = clf.predict(imageData)
    
    return prediction
    
