from voiceDriver import RecognizerAPI
from firebaseAPI import FirebaseDB

import sys
import select
import os
import threading
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


recog = None
firebaseDB = None
selectedMicrophoneIndex = 0
startFunction = None


def InitDB():
    global recog #Global file variable for voice conversion and retrieval of microphone devices
    global firebaseDB #Global file variable for interaction with Google Firebase Database

    pathToFireBaseSDKKey = ""

    while(True): # Loop until correct path to API file is entered by user

        pathToFireBaseSDKKey = input("Please input path to Firebase SDK key:  ")

        if (os.path.isfile(pathToFireBaseSDKKey) == False):
            print(f'File {pathToFireBaseSDKKey} could not be found, please try again')
            continue

        break


    recog = RecognizerAPI() # Wrapper for AI library to convert audio
    firebaseDB = FirebaseDB(pathToFireBaseSDKKey, False) # Wrapper to interact with Google Firebase database

    


def SelectMicrophone():

    global selectedMicrophoneIndex # global variable for selected microphone index

    microphones = recog.GetAllDevices()

    if (len(microphones) == 0): # Exit if no microphone plugged in
        print("No microphones found, exiting")
        return

    


    print("Please select microphone to use with the corresponding number:")

    availableMicrophoneIndexes = []
    
    while (True): # loop through found microphones and display each with a selectable number

        for i in range(len(microphones)):

            print(f'{microphones[i]["index"]} : {microphones[i]["name"]}.')

            availableMicrophoneIndexes.append(microphones[i]["index"])

        inputtedValue = input("Enter desired microphone number:   ")

        if (inputtedValue == "S"):
            return
        
        inputtedValue = int(inputtedValue)

        if (availableMicrophoneIndexes.__contains__(inputtedValue)): # If found microphone list contains user inputted number, use that as the recording microphone
            selectedMicrophoneIndex = inputtedValue
            break
        else:
            print("Selected microphone number was not from the list, please try again, or enter 'S' to shutdown")


def StartKeyboard():

    

    while (True):

        

        inputKey = input("Press R to start recording, or press 'S' to shutdown:  ")

        if (inputKey == "R"):
           StartRecording()
       
            
        if inputKey == "S":
            print("Shutting down")
            break

def StartExternalSwitch():

    t1 = threading.Thread(target=CheckButtonPress, args=(StartRecording,))
    t1.start()

    while (True):

        inputKey = input("Press 'S' to shutdown:   ")

        if inputKey == "S":
            print("Shutting down")
            break

def CheckButtonPress(callback):
    while (True):
        if (GPIO.input(16) == GPIO.HIGH) :
            callback()


def StartRecording():
    
        audio = recog.Listen(selectedMicrophoneIndex, 3) # Start recording audio from microphone, function exits once speech has a pause

        text = recog.SpeechToText(audio) # returns "" if can't convert audio, otherwise returns speech as text

        if (text == ""):
            print("Could not convert audio")

        firebaseDB.AddVisitor(text) # add text to Google firebase database

def ConfigureInputMode():

    global startFunction 

    while (True):

        print("1. Keyboard")
        print("2. External switch")
        inputKey = input("Please select input mode number: ")

        if (inputKey == "1"):
            startFunction = StartKeyboard
            return

        if (inputKey == "2"):
            startFunction = StartExternalSwitch
            return

        print("Please input correct number")
        
        



InitDB()
SelectMicrophone()
ConfigureInputMode()
startFunction()