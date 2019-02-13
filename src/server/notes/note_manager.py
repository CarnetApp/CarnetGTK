

from zipfile import ZipFile
import re
from .html2text import html2text
import json
import os

class NoteManager():

    def __init__(self, notePath):
        self.notePath = notePath

    def getMetadata(self):
        with ZipFile(self.notePath) as zipnote:
            try:
                with zipnote.open('metadata.json') as meta:
                    ret = {}
                    ret['metadata'] = json.loads(meta.read().decode("utf-8"))
                    with zipnote.open('index.html') as index:
                        ret['shorttext'] = html2text(index.read().decode("utf-8")).strip()[0:150]
                        return ret
            except KeyError:
                print ("no metadata")
                with zipnote.open('index.html') as index:
                    ret['shorttext'] = html2text(index.read().decode("utf-8")).strip()[0:150]
                    return ret
    #returns html + metadata

    def saveTextAndMetadataToOpenedNote(self, text, metadatastr, tmp_path):

        index  = open(tmp_path+"/index.html", "w")
        index.write(text)
        index.close()
        metadata  = open(tmp_path+"/metadata.json", "w")
        metadata.write(metadatastr)
        metadata.close()
        zip_ref = ZipFile(self.notePath+".tmp", 'w')
        self.zipdir(tmp_path, zip_ref)
        zip_ref.close()
        try:
            os.remove(self.notePath)
        except FileNotFoundError:
            print("not existing")
        os.rename(self.notePath+".tmp", self.notePath)
        print("saved to "+self.notePath)


    def zipdir(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                print(file)
                print(root)
                ziph.write(os.path.join(root, file), os.path.join(root[len(path):], file))

    def extractNote(self, to):
        import shutil
        try:
            shutil.rmtree(to)
        except FileNotFoundError:
            print ("not found")
        os.makedirs(to)
        self.lastExtractedDest = to
        ret = {}
        zip_ref = ZipFile(self.notePath, 'r')
        zip_ref.extractall(to)
        zip_ref.close()
        try:
            file = open(to+"/metadata.json", 'r')
            text = file.read()
            file.close()
            ret['metadata'] = json.loads(text)
        except FileNotFoundError:
            ret['metadata'] = {}

        try:
            file = open(to+"/index.html", 'r')
            text = file.read()
            file.close()
            ret['html'] = text
        except FileNotFoundError:
            ret['html'] = ""
        return ret