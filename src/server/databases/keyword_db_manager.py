from .settings_manager import SettingsManager
import os, sys
import json

class KeywordDBManager():
    settingsManager = SettingsManager()


    def merge(self):
        my_db = self.getMyKeywordDB()
        has_changed = False
        files = os.listdir(self.settingsManager.getNotePath()+"/quickdoc/keywords/")
        ret = []
        for name in files:
            if(name == self.settingsManager.getUUID()):
                continue

            this_db = self.getKeywordDB(name)
            for action in this_db["data"]:
                is_in = False
                for my_action in my_db["data"]:
                    try:
                        if(my_action['time'] == action['time'] and my_action['path'] == action['path'] and my_action['keyword'] == action['keyword'] and my_action['action'] == action['action']):
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
        file = self.getMyKeywordDBFile('w')
        print(string)
        file.write(string)
        file.close()


    def getMyKeywordDB(self):
         return json.loads(self.getMyKeywordDBString())

    def getMyKeywordDBString(self):

        return self.getKeywordDBString(self.settingsManager.getUUID())

    def getMyKeywordDBFile(self, mode):
        return self.getKeywordDBFile(self.settingsManager.getUUID(), mode)

    def getKeywordDB(self, id):
         return json.loads(self.getKeywordDBString(id))

    def getKeywordDBString(self, id):
        try:
            file = self.getKeywordDBFile(id, 'r')
            text = file.read()
            file.close()
        except FileNotFoundError:
            text = "{\"data\":[]}"
        return text

    def getKeywordDBFile(self, id, mode):
        return open(self.settingsManager.getNotePath()+"/quickdoc/keywords/"+id, mode, encoding='utf8')

