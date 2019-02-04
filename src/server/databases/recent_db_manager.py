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