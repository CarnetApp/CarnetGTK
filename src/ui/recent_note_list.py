
from .recent_db_manager import RecentDBManager
from .note_list import NoteList
class RecentNoteList(NoteList):

    def __init__(self, container, scrollview):
        super().__init__(container, scrollview)

    def get_objects(self):
        recentDBManager = RecentDBManager()
        return recentDBManager.getMyRecentDBNotes()

