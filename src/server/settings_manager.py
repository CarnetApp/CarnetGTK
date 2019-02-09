import json
class SettingsManager:

    def __init__(self):
        try:
            file = open('settings.json', 'r')
            text = file.read()
            file.close()
            self.settings = json.loads(text)
        except FileNotFoundError:
            self.settings = {}
        except json.decoder.JSONDecodeError:
            self.settings = {}

    def getSetting(self, key):
        try:
            return self.settings[key]
        except KeyError:
            return None

    def setSetting(self, key, value):
        self.settings[key] = value
        file = open('settings.json', 'w')
        file.write(json.dumps(self.settings))
        file.close()

    def setHeaderBarBG(self, bg):
        self.setSetting("headerbar_bg",bg)

    def getHeaderBarBG(self):
        return self.getSetting("headerbar_bg")

    def getNotePath(self):
        path = self.getSetting("note_path")
        if(path == None):
            path = "/home/phieelementary/Doggfgcuments/debug"
            self.setSetting("note_path",path)
        return path
    def getUUID(self):

        return "carnetgtk"
settingsManager = SettingsManager()
