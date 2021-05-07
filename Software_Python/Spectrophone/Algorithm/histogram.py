'''
Created on 23.05.2018

all functions about color histograms

@author: Philipp
'''
from matplotlib import pyplot as plt
import cv2
import os


'''
returns the data of a color histogram generated out of an image
'''
def calcHistogram(image):

    '''
    resolution = 480, 640
    resizedImage = cv2.resize(image, resolution)
    '''
    # get data of color channels
    bins = 64
    histo_b = cv2.calcHist([image],[0],None,[bins],[0,255])
    histo_g = cv2.calcHist([image],[1],None,[bins],[0,255])
    histo_r = cv2.calcHist([image],[2],None,[bins],[0,255])
    
    # reshape data
    histo_out = []
    for i in range(bins):
        histo_out.append(histo_b[i][0])
    for i in range(bins):
        histo_out.append(histo_g[i][0])
    for i in range(bins):
        histo_out.append(histo_r[i][0])

    return histo_out


'''
generates and shows color histogramms of single images
'''
def calcSpectrum():
    imgData = []
    bins = 64
    
    #check folder for images to create histogram
    for path, subdirs, files in os.walk(os.path.abspath(r"Spektren//")):
        for name in files:
            if name.endswith(".jpg"):
                image = cv2.imread((os.path.join(path, name)))
                histo_b = cv2.calcHist([image],[0],None,[bins],[0,255])
                histo_g = cv2.calcHist([image],[1],None,[bins],[0,255])
                histo_r = cv2.calcHist([image],[2],None,[bins],[0,255])
                imgData.append([[histo_r, histo_g, histo_b],name])
    
    
    # plot histogram
    for image in imgData:
        fig = plt.figure()
        plt.clf()
        plt.plot(image[0][0],'r')
        plt.plot(image[0][1],'g')
        plt.plot(image[0][2],'b')
        plt.xlim([0,63])
        #plt.xticks([])
        #plt.yticks([])
        #plt.axis('off')
        plt.title(image[1])
        plt.draw()
    
    plt.show()
    
    pass