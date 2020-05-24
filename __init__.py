# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name":        "PatBlend Add-on",                                 # Name of the Add-on
    "description": "A compilation of all Add-ons made by PatBlend",   # Description of the Add-on
    "author":      "Patrick Huang",                                   # Author(s)
    "version":     (1, 0, 2),                                         # Current Version
    "blender":     (2, 80, 0),                                        # Minimum Blender version required to run
    "location":    "3D View >> Sidebar >> PatBlend",                  # Where to find the content of the Add-on
    "warning":     "",                                                # Warning icon in Preferences
    "wiki_url":    "https://github.com/PatBlend/Patblend_Add-on",     # Documentation link
    "tracker_url": "https://forms.gle/rGULhrpfpCta7CWj9",             # Report a Bug link
    "category":    "PatBlend"}                                        # Category of the Add-on


import bpy

from .utils import patblend_ops_props
from .utils import patblend_operators
from .utils import patblend_ui


def register():                                              # Runs each class
    patblend_ops_props.register()
    patblend_ui.register()

def unregister():                                            # Unruns each class
    patblend_ui.unregister()
    patblend_ops_props.unregister()
    
if __name__ == "__main__":                                   # Calls Register
    register()