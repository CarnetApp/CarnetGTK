import json
class NoteMetadata():

    def __init__(self):
        self.creation_date = 0
        self.last_modification_date = 0
        self.keywords = []
        self.rating = -1
        self.todolists = []
        self.color = "none"
        self.text = ""

    def toString(self):
        return json.dumps(self.__dict__)
    def fromString(string):
        print(string)
        metadata = NoteMetadata()
        obj = json.loads(string)
        metadata.creation_date = obj.creation_date
        metadata.last_modification_date = obj.last_modification_date
        metadata.rating = obj.rating
        metadata.keywords = obj.keywords
        metadata.todolists = obj.todolists
        metadata.color = obj.color
        #metadata.creation_date = obj.creation_date
