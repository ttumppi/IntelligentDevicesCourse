import speech_recognition as sr
import pyaudio

class RecognizerAPI:

    def __init__(self):
        self.recogniser = sr.Recognizer() # Ready made library using AI
        self.pyaudio = pyaudio.PyAudio()    # Ready made library for recording audio

    '''
    Blocks thread until set timeout is hit or speech stops after start of speech.
    Returns audio as variable, use SpeechToText to get it in text format
    '''
    def Listen(self, microphoneIndex, timeoutInSeconds):
        try:

            with sr.Microphone(device_index = microphoneIndex) as source: # Listens to microphone until speech stops
                return self.recogniser.listen(source, timeout=timeoutInSeconds)
        except sr.WaitTimeoutError as e:
            return
        
        

    def SpeechToText(self, audio):
        try:

            return self.recogniser.recognize_google(audio) # queries google AI API to turn speech to text
        
        except Exception as e:
            return ""
    
    def GetAllDevices(self):
        deviceCount = self.pyaudio.get_device_count() # Gets all microphone devices

        devices = []
        for i in range(deviceCount):

            deviceInfo = self.pyaudio.get_device_info_by_index(i) # A dictionary with plethora of settings and options

            if (deviceInfo["maxInputChannels"] > 0): # filter if device is a real microphone capable of recording audio
                devices.append({"name":deviceInfo["name"], "index":i})

        return devices