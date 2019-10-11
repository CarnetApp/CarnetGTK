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
from .adaptive_grid import *
from .overview import *
from .overview_toolbar import *
from .editor_toolbar import *
from .recent_db_manager import RecentDBManager
from .recent_note_list import RecentNoteList
@GtkTemplate(ui='/org/gnome/Carnetgtk/ui/res/window.ui')
class CarnetgtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'CarnetgtkWindow'


    overview = GtkTemplate.Child()
    editor_toolbar = GtkTemplate.Child()
    overview_toolbar = GtkTemplate.Child()
    main_view = GtkTemplate.Child()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #WebKit2.WebView()
        self.init_template()

        css_provider = Gtk.CssProvider.get_default()
        css_provider.load_from_data(b""".note{border-radius: 5px;border:solid 1px #e0f0ff;}""")

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )



        #self.webview.load_uri("file:///home/phieelementary/Dev/GitBis/QuickDoc/CarnetNextcloud/templates/CarnetElectron/index.html")
        #self.webview.connect("notify::title", self.window_title_change) #only way to receive messages...
        #self.webview.load_uri("http://localhost:8087")
        self.connect('check-resize', self.resized)
        self.overview_toolbar.set_window(self)
        self.overview.set_window(self)
        #self.webview.get_inspector().detach()
        #self.note_container.insert_row(1)
        #self.note_container.insert_column(1)
        self.editor_toolbar.hide()
    def resized(self, window):

        self.overview.onResized()

    def convert_to_hex(self, rgba_color) :
        red = int(rgba_color.red*255)
        green = int(rgba_color.green*255)#self.webview.load_uri("file:///home/phieelementary/Dev/GitBis/QuickDoc/CarnetNextcloud/templates/CarnetElectron/index.html")
        #self.webview.connect("notify::title", self.window_title_change) #only way to receive messages...
        #self.webview.load_uri("http://localhost:8087")
        self.switch_to_browser()
        RecentNoteList(self.note_container, self.scroll)
        #self.webview.get_inspector().detach()
        blue = int(rgba_color.blue*255)
        return '{r:02x}{g:02x}{b:02x}'.format(r=red,g=green,b=blue)


    def toggle_toolbar(self, toolbar):
        self.webview.run_javascript("writer.toolbarManager.toggleToolbar(writerFrame.contentWindow.document.getElementById('"+toolbar+"'))")

    def window_title_change(self, v, param):
        print("on title changed")
        if not v.get_title():
            return
        if v.get_title().startswith("msgtopython:::"):
            message = v.get_title().split(":::",1)[1]
            # Now, send a message back to JavaScript
            if(message == "noteloaded"):
                print('loaded')
            elif(message == "exit"):
                self.switch_to_browser()

    def switch_to_editor(self, path):
        if(not hasattr(self, "webview")):
            self.webview = WebKit2.WebView()
            self.webview.load_uri("http://localhost:8089/reader/reader.html?path="+path)
            self.webview.connect("notify::title", self.window_title_change) #only way to receive messages...
            self.main_view.add(self.webview)
            self.main_view.show_all()

        self.overview.hide()
        self.overview_toolbar.hide()
        self.webview.show()
        self.editor_toolbar.show()
        self.webview.get_inspector().detach()
        #for child in self.header_bar.get_children():
        #    if(child.get_name() == "new-note"):
        #        child.hide()
        #    elif(child.get_name() == "new-folder"):
        #        child.hide()
        #for child in self.header_bar.get_custom_title().get_children():
        #    if(child.get_name() == "title-label"):
        #        child.hide()
        #    elif(child.get_name() == "editor-box"):
        #        child.show()
    def switch_to_browser(self):
        for child in self.header_bar.get_children():
            if(child.get_name() == "new-note"):
                child.show()
            elif(child.get_name() == "new-folder"):
                child.show()
        for child in self.header_bar.get_custom_title().get_children():
            if(child.get_name() == "title-label"):
                child.show()
            elif(child.get_name() == "editor-box"):
                child.hide()

