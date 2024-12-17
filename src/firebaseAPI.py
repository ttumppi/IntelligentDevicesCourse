import firebase_admin
from firebase_admin import credentials, db





class FirebaseDB:

    def __init__(self, pathToServiceAccountFile, isListener):

        self.cred = credentials.Certificate(pathToServiceAccountFile) # creates needed credentials from API key
        firebase_admin.initialize_app(self.cred, { # Initialize connection
            'databaseURL': 'https://intelligentdevicescourse-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        self.referenceToDB = db.reference("queue") # Reference to db key eg. {"queue":{"unique firebase gen key": "a message"}}

        if (isListener): # Only refers to email server, listener is invoked if application needs to know when data is added to db
            self.referenceToDB.listen(self.VisitorReceivedListener)

        self.visitorReceivedListeners = []



    def AddVisitor(self, visitorMessage):
        '''
        Adds  Message to Google Firebase database
        '''
        
        self.referenceToDB.push({ 
            "visitor message": visitorMessage
        })
        print(f'Added message to database')

    def VisitorReceivedListener(self, event):
        if event.event_type == "put" and event.data:

            if (event.path == "/"): # If true, vent is not triggered during insert but on startup of connection
                return

            for key, visitorMessage in event.data.items(): # Go through each unique key made by firebase db and it's message
                if (visitorMessage): # Check for real value (not null) and delete it from the db. Also invoke listener function if registered about new message
                    
                    db.reference(f'queue/{event.path}').delete()
                    print("Visitor handled in server")

                    self.InvokeVisitorReceivedListeners(visitorMessage)

    def RegisterListenerForReceivedVisitors(self, listener): # Add listener function
        if (listener not in self.visitorReceivedListeners):
            self.visitorReceivedListeners.append(listener)

    def InvokeVisitorReceivedListeners(self, visitorMessage): # Invoke all listener functions if any
        for listener in self.visitorReceivedListeners:
            listener(visitorMessage)