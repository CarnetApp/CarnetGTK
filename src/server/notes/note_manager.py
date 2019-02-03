
from .note_metadata import NoteMetadata
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