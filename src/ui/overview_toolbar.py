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
@GtkTemplate(ui='/org/gnome/Carnetgtk/ui/res/overview_toolbar.ui')
class OverviewToolbar(Gtk.Box):
    __gtype_name__ = 'OverviewToolbar'

    def __init__(self):
        super().__init__()
        self.init_template()

    def set_window(self, window):
        self.window = window

    def on_create_note_clicked(self, view):
        print("on create note clicked")
        self.window.switch_to_editor()
