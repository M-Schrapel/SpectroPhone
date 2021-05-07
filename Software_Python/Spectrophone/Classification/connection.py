'''
Created on 06.06.2018

@author: Philipp
'''
import socket
import numpy as np
import cv2


def sendClassification(predClass, conn):
    conn.send(predClass.encode())  # echo
    
    pass



def setupServer():
    
    serverIp = socket.gethostbyname(socket.gethostname()) 
    serverPort = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((serverIp, serverPort))
    
    print(serverIp)
    print(serverPort)
    
    return sock
    
    
    
def checkClassifyRequest(sock):
    
    sock.listen(1)
    conn, addr = sock.accept()
    print('Connection address:', addr)
        
    return conn



def recvall(conn, count):
    
    buf = b''
    while count:
        newbuf = conn.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf



def receiveData(conn):
    images = []
    ledMode = int.from_bytes(recvall(conn, 4), byteorder='big')
    print("LEDMode: " + str(ledMode))
    lightMode = int.from_bytes(recvall(conn, 4), byteorder='big')
    print("LightMode: " + str(lightMode))
    pictureCount = int.from_bytes(recvall(conn, 4), byteorder='big')
    print("Number of pictures: " + str(pictureCount))
    
    
    for i in range(pictureCount):
        length = recvall(conn, 4)
        stringData = recvall(conn, int.from_bytes(length, byteorder='big'))
        data = np.fromstring(stringData, dtype='uint8')
    
        images.append(cv2.imdecode(data,1)) 
        print("Picture " + str(i+1) + " received")
        
    return images, ledMode, lightMode