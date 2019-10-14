
from .recent_db_manager import RecentDBManager
from .note_list import NoteList
import os, sys
from stat import *
from .settings_manager import *
class RecentNoteList(NoteList):

    def __init__(self, container, scrollview):
        super().__init__(container, scrollview)

    def get_objects(self):
        recentDBManager = RecentDBManager()
        recentDBManager.merge()
        recentDBManager = RecentDBManager()
        return recentDBManager.getMyRecentDBNotes()


