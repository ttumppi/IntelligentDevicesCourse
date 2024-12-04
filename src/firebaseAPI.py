import firebase_admin
from firebase_admin import credentials, db





class FirebaseDB:

    def __init__(self, pathToServiceAccountFile, isListener):

        self.cred = credentials.Certificate(pathToServiceAccountFile)
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://intelligentdevicescourse-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        self.referenceToDB = db.reference("queue")

        if (isListener):
            self.referenceToDB.listen(self.VisitorReceivedListener)

        self.visitorReceivedListeners = []



    def AddVisitor(self, visitorMessage):
        
        self.referenceToDB.push({
            "visitor message": visitorMessage
        })
        print(f'Added message to database')

    def VisitorReceivedListener(self, event):
        if event.event_type == "put" and event.data:

            if (event.path == "/"): # Event is not triggered during insert but on startup of connection
                return

            for key, visitorMessage in event.data.items():
                if (visitorMessage):
                    
                    db.reference(f'queue/{event.path}').delete()
                    print("Visitor handled in server")

                    self.InvokeVisitorReceivedListeners(visitorMessage)

    def RegisterListenerForReceivedVisitors(self, listener):
        if (listener not in self.visitorReceivedListeners):
            self.visitorReceivedListeners.append(listener)

    def InvokeVisitorReceivedListeners(self, visitorMessage):
        for listener in self.visitorReceivedListeners:
            listener(visitorMessage)