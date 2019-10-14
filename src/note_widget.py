# window.py
#
# Copyright 2019 Phie
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import gi
from gi.repository import Gtk, Gdk
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2
from .gi_composites import GtkTemplate
from .settings_manager import *
from os import path
@GtkTemplate(ui='/org/gnome/Carnetgtk/note_widget.ui')
class NoteWidget(Gtk.EventBox):
    __gtype_name__ = 'NoteWidget'
    title_label = GtkTemplate.Child()
    text_label = GtkTemplate.Child()
    def __init__(self, note):
        super().__init__()
        self.init_template()
        self.note = note
        self.get_style_context().add_class("note2")
        if(str(note["metadata"]["color"]) != "None"):
            self.get_style_context().add_class("note_"+note["metadata"]["color"])

        self.text_label.set_text(note["shorttext"])
        self.text_label.set_line_wrap(True)
        self.title_label.set_text(path.basename(note['path']))
        self.title_label.set_line_wrap(True)
