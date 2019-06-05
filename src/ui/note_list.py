from .note_manager import NoteManager
from .settings_manager import *
from .note_widget import *

class NoteList:
    def __init__(self, container, scrollview):
        self.container = container
        self.scrollview = scrollview
        self.objects = self.get_objects()
        row = 0
        while( row != len(self.objects)):
            noteManager = NoteManager(settingsManager.getNotePath()+"/"+self.objects[row])
            notear = {"shorttext":noteManager.getMetadata()['shorttext'], "title":"title "+str(row)}
            note = NoteWidget(notear)
            note.show_all()
            note.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse('white'))
            self.container.add_child(note)
            row = row+1


        self.scrollview.get_vadjustment().connect("value-changed",self.onChanged)
        self.container.show_all()


    def get_objects(self):
        return False

    def onChanged(self, adjustment):
        #what remains
        print(adjustment.get_upper() - adjustment.get_value() -  adjustment.get_page_size())
