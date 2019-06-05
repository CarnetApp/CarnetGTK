from .settings_manager import SettingsManager
import os, sys
import json

class RecentDBManager():
    settingsManager = SettingsManager()


    def merge(self):
        my_db = self.getMyRecentDB()
        has_changed = False
        files = os.listdir(self.settingsManager.getNotePath()+"/quickdoc/recentdb/")
        ret = []
        for name in files:
            if(name == self.settingsManager.getUUID()):
                continue

            this_db = self.getRecentDB(name)
            for action in this_db["data"]:
                is_in = False
                for my_action in my_db["data"]:
                    try:
                        if(my_action['time'] == action['time'] and my_action['path'] == action['path'] and my_action['action'] == action['action']):
                            is_in = True
                            break;
                    except KeyError:
                        is_in = True
                if(not is_in):
                    has_changed = True;
                    my_db['data'].append(action)


        if(True):
            my_db['data'].sort(key=lambda x: int(x['time']), reverse=False)
            self.writeMyDB(my_db)

        return has_changed;

    def writeMyDB(self, db):
        self.writeMyDBString(json.dumps(db, ensure_ascii=False))


    def writeMyDBString(self, string):
        file = self.getMyRecentDBFile('w')
        print(string)
        file.write(string)
        file.close()


    def getMyRecentDB(self):
         return json.loads(self.getMyRecentDBString())

    def getMyRecentDBNotes(self):
        flaten = []
        pin = []
        for item in self.getMyRecentDB()['data']:
            try:
                index = flaten.index(item['path'])
            except ValueError:
                index = -1
            try:
                indexPin = pin.index(item['path'])
            except ValueError:
                indexPin = -1
            if (item["action"] == "add"):
                if (index > -1):
                    del flaten[index]
                flaten.append(item['path'])
            elif (item['action'] == "remove"):
                if (index > -1):
                    del flaten[index]
                if (indexPin > -1):
                    del pin[indexPin]
            elif (item['action'] == "move"):
                if (index > -1):
                    flaten[index] = item['newPath']
                if (indexPin > -1):
                    pin[indexPin] = item['newPath']
            elif (item['action'] == "pin"):
                if (indexPin > -1):
                    del pin[indexPin]
                pin.append(item.path)
            elif (item['action'] == "unpin"):
                if (indexPin > -1):
                    del pin[indexPin]
        flaten.reverse()
        pin.reverse()
        pin.extend(flaten)
        return pin
    def getMyRecentDBString(self):

        return self.getRecentDBString(self.settingsManager.getUUID())

    def getMyRecentDBFile(self, mode):
        return self.getRecentDBFile(self.settingsManager.getUUID(), mode)

    def getRecentDB(self, id):
         return json.loads(self.getRecentDBString(id))

    def getRecentDBString(self, id):
        try:
            file = self.getRecentDBFile(id, 'r')
            text = file.read()
            file.close()
        except FileNotFoundError:
            text = "{\"data\":[]}"
        return text

    def getRecentDBFile(self, id, mode):
        return open(self.settingsManager.getNotePath()+"/quickdoc/recentdb/"+id, mode, encoding='utf8')

    def  addActionsToMyDB(self, actions):
        recent = self.getMyRecentDB();

        for item in actions:
            recent["data"].append(item)
        self.writeMyDB(recent)

        
