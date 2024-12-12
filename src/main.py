from voiceDriver import RecognizerAPI
from firebaseAPI import FirebaseDB
from gpiozero import Button
from client import HttpClient
import sys
import select
import os


recog = None
firebaseDB = None
selectedMicrophoneIndex = 0
startFunction = None
client = None


def InitDB():
    global recog
    global client

    


    recog = RecognizerAPI()
    client = HttpClient("192.168.1.100", "8080", None)


def SelectMicrophone():

    global selectedMicrophoneIndex

    microphones = recog.GetAllDevices()

    if (len(microphones) == 0):
        print("No microphones found, exiting")
        return

    


    print("Please select microphone to use with the corresponding number:")

    availableMicrophoneIndexes = []
    
    while (True):

        for i in range(len(microphones)):

            print(f'{microphones[i]["index"]} : {microphones[i]["name"]}.')

            availableMicrophoneIndexes.append(microphones[i]["index"])

        inputtedValue = input("Enter desired microphone number:   ")

        if (inputtedValue == "S"):
            return
        
        inputtedValue = int(inputtedValue)

        if (availableMicrophoneIndexes.__contains__(inputtedValue)):
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

    button = Button(4)
    button.when_pressed = StartRecording
    while (True):

        

        inputKey = input("Press 'S' to shutdown:  ")

        
       
            
        if inputKey == "S":
            print("Shutting down")
            break


def StartRecording():
        
        global client
    
        audio = recog.Listen(selectedMicrophoneIndex, 3)

        text = recog.SpeechToText(audio)

        if (text == ""):
            print("Could not convert audio")

        client.UploadMessage(text)

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