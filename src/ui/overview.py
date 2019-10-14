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
from gi.repository import GObject
from .gi_composites import GtkTemplate
from .adaptive_grid import *
from .recent_db_manager import RecentDBManager
from .recent_note_list import RecentNoteList
from .browser_note_list import BrowserNoteList
from gi.repository.Handy import Column
@GtkTemplate(ui='/org/gnome/Carnetgtk/ui/res/overview.ui')
class Overview(Gtk.Box):
    __gtype_name__ = 'Overview'

    note_container = GtkTemplate.Child()
    header_bar = GtkTemplate.Child()
    main_view = GtkTemplate.Child()
    browser_view = GtkTemplate.Child()
    keywords_view = GtkTemplate.Child()
    squeezer = GtkTemplate.Child()
    switcher_bar = GtkTemplate.Child()
    title_label = GtkTemplate.Child()
    current_list = None
    def _make_property(name):
        def getter(self):
            return self.gtkBuilder.get_object(name).get_text()
        def setter(self, text):
            return self.gtkBuilder.get_object(name).set_text(text)
        return property(getter, setter)

    reveal_bla= GObject.Property(type=Gtk.Widget, default=None)
    def __init__(self):
        super().__init__()

        self.init_template()

        self.current_stack = None
        GObject.GObject.bind_property(self.squeezer, "visible-child",
                               self,
                               "reveal_bla",
                               GObject.BindingFlags.SYNC_CREATE, self.fromfu, self.to)
        self.switcher_bar.set_reveal(False)


    def fromfu(self, arg1, arg2):

        self.switcher_bar.set_reveal(self.title_label == GObject.GObject.get_property(self.squeezer,"visible-child"))
    def to(self):
        print ("from")
    def open_recent(self):
        if(self.current_list != None):
            self.note_container.reset()
        self.current_list = RecentNoteList(self.note_container, None)
        self.current_list.set_window(self.window)
        self.note_container.get_parent().remove(self.note_container)
        self.main_view.add(self.note_container)

    def open_browser(self):
        if(self.current_list != None):
            self.note_container.reset()
        self.current_list = BrowserNoteList(self.note_container, None)
        self.current_list.set_window(self.window)
        self.note_container.get_parent().remove(self.note_container)
        self.browser_view.add(self.note_container)
    def on_row_activated(self, one, row):
        if(row.get_child().get_name() == "browser"):
            self.open_browser()
        elif(row.get_child().get_name() == "recent"):
            self.open_recent()
    def set_window(self, window):
        self.window = window
        if(self.current_list != None):
            self.current_list.set_window(window)
    def onResized(self):

        self.note_container.onResized()

    def on_widget_show(self, view, arg2):
        print("show "+str(view))
        if(self.current_stack == view):
            return

        self.current_stack = view
        if(view == self.browser_view):
            self.open_browser()
        if(view == self.keywords_view):
            print("keywords")
        if(view == self.main_view):
            self.open_recent()

