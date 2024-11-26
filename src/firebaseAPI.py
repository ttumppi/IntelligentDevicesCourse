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



    def AddVisitor(self, visitor):
        
        self.referenceToDB.push({
            "visitor": visitor
        })
        print(f'Added {visitor} to database')

    def VisitorReceivedListener(self, event):
        if event.event_type == "put" and event.data:
            for key, visitor in event.data.items():
                if (visitor):
                    
                    db.reference(f'queue/{key}').delete()
                    print("Visitor handled in server")

                    self.InvokeVisitorReceivedListeners(visitor)

    def RegisterListenerForReceivedVisitors(self, listener):
        if (listener not in self.visitorReceivedListeners):
            self.visitorReceivedListeners.append(listener)

    def InvokeVisitorReceivedListeners(self, visitor):
        for listener in self.visitorReceivedListeners:
            listener(visitor)
