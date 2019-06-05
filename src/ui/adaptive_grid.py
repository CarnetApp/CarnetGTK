# adaptive_grid.py
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


class AdaptiveGrid(Gtk.Box):
    __gtype_name__ = 'AdaptiveGrid'
    children = list()
    def __init__(self):
        super().__init__()
        self.set_columns_count(4)

    def set_columns_count(self, count):
        self.column_rows = list()
        self.columns = list()

        for i in range(0,count):
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.column_rows.append(0)
            self.columns.append(box)
            self.pack_start(box, True, True, 10)


    def add_child(self, child):

        column = self.column_rows.index(min(self.column_rows))
        self.columns[column].pack_start(child, False, False, 0)
        height = child.size_request().height
        self.column_rows[column] = self.column_rows[column]+height



    
