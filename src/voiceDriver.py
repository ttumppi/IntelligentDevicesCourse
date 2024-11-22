import speech_recognition as sr
import pyaudio

class RecognizerAPI:

    def __init__(self):
        self.recogniser = sr.Recognizer()
        self.pyaudio = pyaudio.PyAudio()

    '''
    Blocks thread until set timeout is hit or speech stops after start of speech.
    Returns audio as variable, use SpeechToText to get it in text format
    '''
    def Listen(self, microphoneIndex):
        with sr.Microphone(device_index = microphoneIndex) as source:
            return self.recogniser.listen(source)
        

    def SpeechToText(self, audio):
        try:

            return self.recogniser.recognize_google(audio)
        
        except Exception as e:
            return "Could not understand"
    
    def GetAllDevices(self):
        deviceCount = self.pyaudio.get_device_count()

        devices = []
        for i in range(deviceCount):

            deviceInfo = self.pyaudio.get_device_info_by_index(i)

            if (deviceInfo["maxInputChannels"] > 0):
                devices.append({"name":deviceInfo["name"], "index":i})

        return devices