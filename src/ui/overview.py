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
@GtkTemplate(ui='/org/gnome/Carnetgtk/ui/res/overview.ui')
class Overview(Gtk.Box):
    __gtype_name__ = 'Overview'

    note_container = GtkTemplate.Child()
    scroll = GtkTemplate.Child()
    main_view = GtkTemplate.Child()
    current_list = None
    def __init__(self):
        super().__init__()
        self.init_template()

        #settingsManager.setHeaderBarBG(self.convert_to_hex(self.header_bar.get_style_context().get_background_color(Gtk.StateFlags.ACTIVE)))
        #self.switch_to_browser()
        self.current_list = RecentNoteList(self.note_container, self.scroll)
        self.current_list.set_window(self.window)

    def set_window(self, window):
        self.window = window
        if(self.current_list != None):
            self.current_list.set_window(window)
    def onResized(self):

        self.note_container.onResized()

