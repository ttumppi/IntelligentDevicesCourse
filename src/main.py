from voiceDriver import RecognizerAPI
from firebaseAPI import FirebaseDB
import sys
import select
import os
def Start():

    pathToFireBaseSDKKey = ""

    while(True):

        pathToFireBaseSDKKey = input("Please input path to Firebase SDK key:  ")

        if (os.path.isfile(pathToFireBaseSDKKey) == False):
            print(f'File {pathToFireBaseSDKKey} could not be found, please try again')
            continue

        break


    recog = RecognizerAPI()
    firebaseDB = FirebaseDB(pathToFireBaseSDKKey, False)

    microphones = recog.GetAllDevices()

    if (len(microphones) == 0):
        print("No microphones found, exiting")
        return

    selectedMicrophoneIndex = 0


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

    while (True):

        

        inputKey = input("Press R to start recording, or press 'S' to shutdown:  ")

        if (inputKey == "R"):
            audio = recog.Listen(selectedMicrophoneIndex, 3)

            

            text = recog.SpeechToText(audio)

            if (text == ""):
                print("Could not convert audio")
                continue

            firebaseDB.AddVisitor(text)
       
            
        if inputKey == "S":
            print("Shutting down")
            break




Start()