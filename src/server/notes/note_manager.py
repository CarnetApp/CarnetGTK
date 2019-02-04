

from zipfile import ZipFile
import re
from .html2text import html2text
import json
class NoteManager():

    def __init__(self, notePath):
        self.notePath = notePath

    def getMetadata(self):
        with ZipFile(self.notePath) as zipnote:
            with zipnote.open('metadata.json') as meta:
                ret = {}
                ret['metadata'] = json.loads(meta.read().decode("utf-8"))
                with zipnote.open('index.html') as index:
                    ret['shorttext'] = html2text(index.read().decode("utf-8")).strip()[0:150]
                    return ret
    #returns html + metadata
    def extractNote(self, to):
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