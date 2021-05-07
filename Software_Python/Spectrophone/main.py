'''
Created on 23.05.2018

python server application for a master thesis at the Leibniz University Hanover
detecting spectroscopic features of surfaces with smartphone cameras

main menue for the server application

@author: Philipp Etgeton
'''

import sys
import os
from sys import platform
from Evaluation.evaluate import trainModel
from Classification.classify import classification, classifyFolder, renamefiles
from Algorithm.prepare import prepareData
from Algorithm.histogram import calcSpectrum



if __name__ == '__main__':
    pass

def main():
   mainMenu()


def mainMenu():
    
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')
    
    print("************Spectrophone Server*************")
    print()

    choice = input("""
                      1: Start classification mode
                      2: Train Model
                      3: Prepare Dataset
                      4: Classify Folder
                      5: Show spectrum of folder
                      6: Exit

                      Please enter your choice: """)

    if choice == "1":
        classification()
    elif choice == "2":
        ledMenu()
    elif choice=="3":
        prepareData()
    elif choice=="4":
        classifyFolder()
    elif choice=="5":
        calcSpectrum()
    elif choice=="6":
        sys.exit
    else:
        print("Invalid Choice!")
        print("Please try again")
        mainMenu()
        
        

def ledMenu():
    
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')
        
    print("************LED Mode*************")
    print()

    choice = input("""
                      1: coldwhite LED
                      2: warmwhite LED
                      3: both LED
                      4: Exit

                      Please enter your choice: """)

    if choice == "1":
        lightMenu(1)
    elif choice == "2":
        lightMenu(2)
    elif choice == "3":
        lightMenu(3)
    elif choice=="4":
        sys.exit
    else:
        print("Invalid Choice!")
        print("Please try again")
        ledMenu()   
        
        
def lightMenu(ledMode):
    
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')
        
        
    print("************Light Mode*************")
    print()

    choice = input("""
                      1: One illuminance level
                      2: Two illuminance level
                      3: Five illuminance level
                      4: Exit

                      Please enter your choice: """)

    if choice == "1":
        trainModel(ledMode, 1)
    elif choice == "2":
        trainModel(ledMode, 2)
    elif choice == "3":
        trainModel(ledMode, 3)
    elif choice=="4":
        sys.exit
    else:
        print("Invalid Choice!")
        print("Please try again")
        ledMenu(ledMode)   



main()