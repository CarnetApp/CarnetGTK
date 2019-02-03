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


@GtkTemplate(ui='/org/gnome/Carnetgtk/window.ui')
class CarnetgtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'CarnetgtkWindow'

    webview = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import os
        print(os.path.dirname(os.path.realpath(__file__)))

        WebKit2.WebView()
        self.init_template()
        #self.webview.load_uri("file:///home/phieelementary/Dev/GitBis/QuickDoc/CarnetNextcloud/templates/CarnetElectron/index.html")

        self.webview.load_uri("http://localhost:8087")
        #self.webview.get_inspector().detach()