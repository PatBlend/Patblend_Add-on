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

import bpy, math, time, datetime
from bpy.props import (StringProperty,                       # Import Blender python properties
                       BoolProperty, 
                       IntProperty, 
                       FloatProperty, 
                       FloatVectorProperty, 
                       EnumProperty, 
                       PointerProperty)
from bpy.types import (Panel,                                # Import Blender UI Types
                       Menu, 
                       Operator, 
                       PropertyGroup)

class PatBlendProps(PropertyGroup):
    # Add-on Settings
    activated: BoolProperty(
        name = "Activated",
        default = False
    )
    
    consoleInfo: BoolProperty(
        name = "Show info in Console",
        description = "Prints information about status and the add-on in the system Console.",
        default = True
    )

    textInfo: BoolProperty(
        name = "Log info in text",
        description = "Creates a text datablock and logs information in the text.",
        default = True
    )

    openGit: BoolProperty(
        name = "Open GitHub after uninstalling",
        description = "Opens the PatBlend GitHub in your browser after uninstalling to download the latest version",
        default = True
    )

    downloadLatest: BoolProperty(
        name = "Download after uninstalling",
        description = "Automatically downloads the latest version after uninstallation is done.",
        default = True
    )

    sizeTheme: EnumProperty(
        name = "Size",
        description = "Various layout sizes to fit your needs.",
        items = [
            ('0', "Minimal", "All items are single line sized. (1, 1, 1, 1)"),
            ('1', "Compact", "Most items are single, but major ones are larger. (1, 1, 1, 1.5)"),
            ('2', "Normal", "Various sizes (1, 1, 1.5, 2)"),
            ('3', "Comfortable", "A large layout (1, 1.5, 2.5, 3.5)"),
            ('4', "Large Print", "All items are overly large (2, 3.5, 5, 6.5)")
        ]
    )

    version: EnumProperty(
        name = "Version",
        description = "Choose which release to download.",
        items = [
            ('1.0.0', "1.0.0", "Version 1.0.0"),
            ('1.0.1', "1.0.1", "Version 1.0.1"),
            ('1.0.2 Alpha', "1.0.2 Alpha", "Version 1.0.2 Alpha"),
            ('1.0.2', "1.0.2", "Version 1.0.2"),
            ('Master', "Master", "Latest development version")
        ]
    )

    # Render Setup Settings
    engine: EnumProperty(
        name = "Render Engine",
        description = "Choose which engine to setup.",
        items = [
            ('0', "Eevee", "Realtime Engine"),
            ('1', "Workbench", "Studio Lighting Engine"),
            ('2', "Cycles", "Raytraced Engine")
        ],
        default = {'0'},
        options = {'ENUM_FLAG'}
    )

    intSamples: IntProperty(
        name = "Samples",
        description = "Amount of time to repeat calculations in rendering.",
        default = 64, min = 2, max = 8192
    )

    workSamples: EnumProperty(
        name = "Samples",
        description = "How workbench renders the image",
        items = [
            #('0', "No anti-aliasing", "Bare image"),
            #('1', "Single Pass anti-aliasing", "Smooths edges"),
            ('2', "5 Samples", "5 Samples"),
            ('3', "8 Samples", "8 Samples"),
            ('4', "11 Samples", "11 Samples"),
            ('5', "16 Samples", "16 Samples"),
            ('6', "32 Samples", "32 Samples")
        ]
    )

    ao: BoolProperty(
        name = "Ambient Occlusion",
        description = "Shades objects based on normals.",
        default = False
    )

    ssr: BoolProperty(
        name = "Screen Space Reflections",
        description = "Allows the transparency of objects.",
        default = True
    )

    shadowQual: EnumProperty(
        name = "Shadow Quality",
        description = "Quality of shadows. The render time and memory usage increases with quality.",
        items = [
            ('0', "Low", "Uses 1024px maps and low bitdepth."),
            ('1', "Medium", "Uses 2048px maps and high bitdepth."),
            ('2', "High", "Uses 4096px maps and high bitdepth")
        ]
    )

    cyclesDevice: EnumProperty(
        name = "Device",
        description = "Choose whether to use CPU or GPU for rendering.",
        items = [
            ('0', "CPU", "Use CPU"),
            ('1', "GPU Compute", "Use GPU")
        ]
    )

    bounces: IntProperty(
        name = "Light Bounces",
        description = "How many times light bounces before it is omitted.",
        default = 3
    )

    caustics: BoolProperty(
        name = "Caustics",
        description = "Calculates light patterns through transparent objects.",
        default = False
    )

    outX: IntProperty(
        name = "X Output",
        description = "Pixel resolution of the horizontal dimension.",
        default = 1920
    )

    outY: IntProperty(
        name = "Y Output",
        description = "Pixel resolution of the vertical dimension.",
        default = 1080
    )
    
    fps: IntProperty(
        name = "FPS",
        description = "Frames per second",
        default = 30, min = 12, max = 240
    )

    worldCol: FloatVectorProperty(
        name = "World Color",
        description = "Color of the background",
        default = (0, 0, 0), min = 0, max = 1,
        subtype = 'COLOR'
    )

    worldStr: FloatProperty(
        name = "World Strength",
        description = "Strength of the background lighting",
        default = 1, min = 0
    )

    # Unit Manipulator
    lengthFunc: EnumProperty(
        name = "Function",
        description = "What the Length Manipulator performs.",
        items = [
            ('0', "Convert", "Converts from one unit to another."),
            ('1', "Comparing", "Compares units to common objects.")
        ],
        options = {'ENUM_FLAG'},
        default = {'0'}
    )

    lengthType1: EnumProperty(
        name = "From",
        description = "The input is in this unit.",
        items = [
            ('0', "Milimeter", "One thousandth of a meter"),
            ('1', "Centimeter", "One hundreth of a meter"),
            ('2', "Meter", "Distance light travels in a vacuum in 1 / 299,792,458"),
            ('3', "Kilometer", "One thousand meters"),
            ('4', "Inch", "One inch"),
            ('5', "Foot", "Twelve inches"),
            ('6', "Yard", "Three Feet"),
            ('7', "Mile", "1,760 Yards")
        ]
    )

    lengthType2: EnumProperty(
        name = "To",
        description = "The input is in this unit.",
        items = [
            ('0', "Milimeter", "One thousandth of a meter"),
            ('1', "Centimeter", "One hundreth of a meter"),
            ('2', "Meter", "Distance light travels in a vacuum in 1 / 299,792,458"),
            ('3', "Kilometer", "One thousand meters"),
            ('4', "Inch", "One inch"),
            ('5', "Foot", "Twelve inches"),
            ('6', "Yard", "Three Feet"),
            ('7', "Mile", "1,760 Yards")
        ]
    )
    
    lengthNum: FloatProperty(
        name = "Input",
        description = "Input value. The unit is defined above.",
        default = 12.5, min = 0
    )

    lengthPrec: IntProperty(
        name = "Non-Zero Decimal Places",
        description = "Amount of non-zero numbers after the decimal point to display.",
        default = 3, min = 0, max = 7
    )

    timeFunc: EnumProperty(
        name = "Function",
        description = "What the time manipulator does",
        items = [
            ('0', "Number to standard", "Converts a number of seconds, minutes, or hours into a standard time format."),
            ('1', "Standard to number", "Converts a standard time format into a number of seconds, minutes, or hours."),
            #('2', "Time arithmetic", "Adds or subtracts different amounts of time.")
        ]
    )
    
    timeStandard: StringProperty(
        name = "Time",
        description = "Enter time in the format hh:mm:ss.ss"
    )

    timeNumType: EnumProperty(
        name = "Unit",
        description = "What unit the below number is in.",
        items = [
            ('0', "Seconds", "Seconds"),
            ('1', "Minutes", "Minutes"),
            ('2', "Hours", "Hours")
        ]
    )

    timeNum: FloatProperty(
        name = "Time",
        description = "Enter a time in the form of a float. The unit is defined above.",
        default = 12.5, min = 0
    )

    # Quick Search
    address: StringProperty(
        name = "Address",
        description = "Put in what you want to be searched.",
    )

    searchForce: EnumProperty(
        name = "Force State",
        description = "Forces the searcher to search either a non-url or a url.",
        items = [
            ('0', "Auto", "Automatically identifies whether the address is a url or keyword."),
            ('1', "URL", "Searches as a url"),
            ('2', "Keyword", "Searches as a keyword")
        ]
    )

    # Codec
    function: EnumProperty(
        name = "Function",
        description = "What the codec performs.",
        items = [
            ('0', "Encoding", "Takes human language and codes it into a PatBlend code."),
            ('1', "Decoding", "Takes PatBlend code and decodes it into human language.")
        ],
        default = {'0'},
        options = {'ENUM_FLAG'}
    )

    codeType: EnumProperty(
        name = "Codec",
        description = "Choose which PatBlend codec to use.",
        items = [
            ('0', "PatBlend 1", "PatBlend codec number 1"),
            ('1', "PatBlend 2", "PatBlend codec number 2"),
            ('2', "PatBlend 3", "PatBlend codec number 3"),
            ('3', "Custom", "Choose custom code offset.")
        ]
    )

    custCodeOffset: IntProperty(
        name = "Ascii Offset",
        description = "Amount of offset to do for the Ascii. Uncommon number is recommended.",
        default = 0, min = -94, max = 94
    )

    codeIn: StringProperty(
        name = "Input",
        description = "String to pass to the codec."
    )

    dateTimeStamp: BoolProperty(
        name = "Create Datetime Stamp in Text",
        description = "Creates a log of when and what day the code was created.",
        default = False
    )

    # Timer
    timerHour: IntProperty(
        name = "Hours",
        description = "Amount of hours to start the timer with.",
        default = 0, min = 0
    )

    timerMin: IntProperty(
        name = "Minutes",
        description = "Amount of minutes to start the timer with",
        default = 0, min = 0, max = 59
    )

    timerSec: FloatProperty(
        name = "Seconds",
        description = "Amount of seconds to start the timer with.",
        default = 0, min = 0, max = 60
    )

    libAsset: EnumProperty(
        name = "Asset Name",
        description = "The name of the asset",
        items = [
            ('pear001', "Pear001", "Pear001"),
            ('rock001', "Rock001", "Rock001")
        ]
    )


def register():                                              # Runs each class
    print("BLAH")
    bpy.utils.register_class(PatBlendProps)
    bpy.types.Scene.patblend = PointerProperty(type = PatBlendProps)
    print("Props Registered")
    
def unregister():                                            # Unruns each class
    from bpy.utils import unregister_class
    unregister_class(PatBlendProps)
    del bpy.types.Scene.patblend