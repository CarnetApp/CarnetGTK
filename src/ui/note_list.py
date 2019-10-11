from .note_manager import NoteManager
from .settings_manager import *
from .note_widget import *
import os, sys
from stat import *
class NoteList:
    def __init__(self, container, scrollview):
        self.container = container

        self.scrollview = scrollview
        self.objects = self.get_objects()
        row = 0
        while( row != len(self.objects)):
            path = self.objects[row]
            s = os.stat(settingsManager.getNotePath()+"/"+path)
            if(S_ISDIR(s.st_mode)):
                row = row + 1
                continue
            noteManager = NoteManager(settingsManager.getNotePath()+"/"+path)
            note = noteManager.getMetadata()
            note['path'] = path
            note_widget = NoteWidget(note)
            note_widget.show_all()
            note_widget.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse('white'))
            note_widget.connect("button-release-event", self.on_note_clicked)
            self.container.add_child(note_widget)
            row = row+1


        self.scrollview.get_vadjustment().connect("value-changed",self.onChanged)
        self.container.show_all()

    def set_window(self, window):
        self.window = window

    def on_note_clicked(self, note_widget, bla):
        print("clicked ! "+note_widget.note['path'])
        self.window.switch_to_editor(note_widget.note['path'])
    def get_objects(self):
        return False

    def onChanged(self, adjustment):
        #what remains
        print(adjustment.get_upper() - adjustment.get_value() -  adjustment.get_page_size())
