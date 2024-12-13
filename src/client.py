import urllib.request
import threading

import base64
import hashlib
import time
import json

class HttpClient:

    def __init__(self, ip, port, callback):
        self.ip = ip
        self.port = port
        self.shutdown = False
        self.callback = callback

    def Shutdown(self):
        self.shutdown = True

    def Start(self):
        thread = threading.Thread(target=self.PollForData)
        thread.start()

    def PollForData(self):
        creds = self.EncryptCredentials()
        GETRequest = urllib.request.Request(f"http://{self.ip}:{self.port}/data", None, {"Content-Type": "application/json", "Authorization": creds}, None, None, "GET")
        
       

        while (self.shutdown == False):
            try:

                response = urllib.request.urlopen(GETRequest)
                responseData = response.read()
                responsePayload = responseData.decode("utf-8")

                jsonData = json.loads(responsePayload)

                for item in jsonData:
                    self.callback(item["message"])

                    DELETERequest = urllib.request.Request(f"http://{self.ip}:{self.port}/data/{item['id']}", None,
                                                            {"Content-Type": "application/json", "Authorization": creds}, None, None, "DELETE")
                    urllib.request.urlopen(DELETERequest)
            except Exception as e:
                print(e)
            
            
            time.sleep(5)

    def UploadMessage(self, message):
        creds = self.EncryptCredentials()
        someJson = {"message":message}

        jsonDump = json.dumps(someJson).encode("utf-8")
        POSTRequest = urllib.request.Request(f"http://{self.ip}:{self.port}/data", jsonDump, {"Content-Type": "application/json", "Authorization": creds}, None, None, "POST")
        urllib.request.urlopen(POSTRequest)
            


    def EncryptCredentials(self):
        encodedCredentials = base64.b64encode("secretUser:GoVeryNice>:(".encode("ascii")).decode()
        
        return f"Basic {encodedCredentials}"
