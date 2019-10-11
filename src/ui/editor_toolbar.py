# overview.py
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
from .gi_composites import GtkTemplate
from .adaptive_grid import *
from .recent_db_manager import RecentDBManager
from .recent_note_list import RecentNoteList
@GtkTemplate(ui='/org/gnome/Carnetgtk/ui/res/editor_toolbar.ui')
class EditorToolbar(Gtk.Box):
    __gtype_name__ = 'EditorToolbar'

    def __init__(self):
        super().__init__()
        self.init_template()



    def on_format_clicked(self, view):
        print("on format clicked")
        self.toggle_toolbar("format-toolbar")

    def on_edit_clicked(self, view):
        print("on format clicked")
        self.toggle_toolbar("edit-toolbar")

    def on_media_clicked(self, view):
        print("on format clicked")
        self.toggle_toolbar("media-toolbar")

    def on_tools_clicked(self, view):
        print("on format clicked")
        self.toggle_toolbar("tools-toolbar")
