from voiceDriver import RecognizerAPI
def Start():
    recog = RecognizerAPI()

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

        print("Please say something, or press 'S' to shutdown")

        audio = recog.Listen(selectedMicrophoneIndex)

        text = recog.SpeechToText(audio)

        print(text)

        # if (input() == "S"):
        #     print("Shutting down")
        #     break


Start()