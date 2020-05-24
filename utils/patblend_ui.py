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

import bpy, math, time, datetime, os
import bpy.utils.previews
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
from . import patblend_operators

custIcons = None
preview_collections = {}

def GetSize(theme, type):                                    # This function calculates the sizes for Size Theme.
    if theme == '0':       # (1, 1, 1, 1)
        return 1
    elif theme == '1':     # (1, 1, 1, 1.5)
        if type == 4:
            return 1.5
        else:
            return 1
    elif theme == '2':     # (1, 1, 1.5, 2)
        if type == 4:
            return 2
        elif type == 3:
            return 1.5
        else:
            return 1
    elif theme == '3':     # (1, 1.5, 2.5, 3.5)
        if type == 1:
            return 1
        elif type == 2:
            return 1.5
        elif type == 3:
            return 2.5
        elif type == 4:
            return 3.5
    elif theme == '4':     # (2, 3.5, 5, 6.5)
        return type * 1.5 + 0.5

def generate_previews():
    # We are accessing all of the information that we generated in the register function below
    pcoll = preview_collections["thumbnail_previews"]
    image_location = pcoll.images_location
    VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg')
    
    enum_items = []
    
    # Generate the thumbnails
    for i, image in enumerate(os.listdir(image_location)):
        if image.endswith(VALID_EXTENSIONS):
            filepath = os.path.join(image_location, image)
            thumb = pcoll.load(filepath, filepath, 'IMAGE')
            enum_items.append((image, image, "", thumb.icon_id, i))
            
    return enum_items

class Panel:                                                 # Base panel that shows up in Sidebar
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PatBlend"
    bl_options = {"DEFAULT_CLOSED"}

class PATBLEND_PT_Settings(Panel, bpy.types.Panel):          # Main Settings panel
    bl_idname = "PATBLEND_PT_Settings"
    bl_label = "Settings"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme

        activated = prop.activated
        if activated == False:
            layout.operator("patblend.activate")
            return

class PATBLEND_PT_SettingsQuick(Panel, bpy.types.Panel):     # Quick Settings panel
    bl_parent_id = "PATBLEND_PT_Settings"
    bl_label = "Quick Settings"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme

        activated = prop.activated
        if activated == False:
            return

        row = layout.row(align = True)    # Uninstall, Disable
        row.scale_y = GetSize(theme, 4)
        row.operator("patblend.uninstall_prompt", text = "Uninstall")
        row.operator("patblend.disable_prompt", text = "Disable")

        row = layout.row()                # Github checkbox
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "openGit")
        
        row = layout.row()                # Download Latest checkbox
        row.enabled = prop.openGit
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "downloadLatest")

        row = layout.row()                # Size Theme
        row.scale_y = GetSize(theme, 3)
        row.prop(prop, "sizeTheme")

        row = layout.row()                # Console, Text logging
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "consoleInfo", text = "Console Log")
        row.prop(prop, "textInfo", text = "Text Log")
        layout.separator()

class PATBLEND_PT_SettingsLinks(Panel, bpy.types.Panel):     # Links panel
    bl_parent_id = "PATBLEND_PT_Settings"
    bl_label = "PatBlend Links"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        ver = prop.version

        activated = prop.activated
        if activated == False:
            return
        
        layout.label(text = "Download")

        row = layout.row()           # Choose version
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "version")

        col = layout.column(align = True)  # Download latest, previous, all
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 4)
        row.operator("patblend.download_latest", text = "Latest")
        row.operator("patblend.download_previous", text = ver)
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 4)
        row.operator("patblend.download_all")

        layout.separator()
        layout.label(text = "Web Links")

        col = layout.column(align = True)    # All web links
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.open_git")
        row.operator("patblend.open_site")
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.documentation")
        row.operator("patblend.report_bug")
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.open_git_releases")
        layout.separator()

class PATBLEND_PT_RenderSetup(Panel, bpy.types.Panel):       # Main Render Setup
    bl_idname = "PATBLEND_PT_RenderSetup"
    bl_label = "Render Setup"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        engine = prop.engine

        activated = prop.activated
        if activated == False:
            return

        if engine in [{'1'}, {'2'}, {'0'}]:
            row = layout.row()
            row.scale_y = GetSize(theme, 3)
            row.operator("patblend.render_setup")
            layout.separator()
        else:
            layout.label(text = "Select exactly one render engine.")
            layout.separator()

class PATBLEND_PT_RenderEngine(Panel, bpy.types.Panel):      # Engine settings panel
    bl_parent_id = "PATBLEND_PT_RenderSetup"
    bl_label = "Engine Specific"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        engine = prop.engine

        activated = prop.activated
        if activated == False:
            return

        if engine in [{'1'}, {'2'}, {'0'}]:
            row = layout.row()
            row.scale_y = GetSize(theme, 2)
            row.prop(prop, "engine")

            row = layout.row()
            row.scale_y = GetSize(theme, 1)

            if engine == {'1'}:
                #row.prop(prop, "workSamples")
                a = 0
            else:
                row.prop(prop, "intSamples")

            if engine == {'2'}:
                row = layout.row()
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "cyclesDevice")

            row = layout.row()
            row.scale_y = GetSize(theme, 1)
            if engine == {'0'}:
                row.prop(prop, "ao")
                row.prop(prop, "ssr")
            elif engine == {'2'}:
                row.prop(prop, "bounces")
                row.prop(prop, "caustics")
            layout.separator()
        else:
            row = layout.row()
            row.scale_y = GetSize(theme, 2)
            row.prop(prop, "engine")
            layout.label(text = "Select exactly one render engine.")
            layout.separator()

class PATBLEND_PT_OutputSettings(Panel, bpy.types.Panel):    # Output settings
    bl_parent_id = "PATBLEND_PT_RenderSetup"
    bl_label = "Output Settings"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme

        activated = prop.activated
        if activated == False:
            return

        row = layout.row(align = True)
        row.scale_y = GetSize(theme, 1)
        row.prop(prop, "outX")
        row.prop(prop, "outY")

        layout.separator()

        row = layout.row(align = True)
        row.scale_y = GetSize(theme, 1)
        row.prop(prop, "fps")
        
        layout.separator()

        col = layout.column(align = True)
        col.scale_y = GetSize(theme, 1)
        col.prop(prop, "worldCol")
        col.prop(prop, "worldStr")

        layout.separator()

class PATBLEND_PT_Search(Panel, bpy.types.Panel):            # Quick Search
    bl_idname = "PATBLEND_PT_Search"
    bl_label = "Quick Search"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme

        activated = prop.activated
        if activated == False:
            return

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "address")

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "searchForce")

        row = layout.row()
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.search")

        layout.separator()

class PATBLEND_PT_Codec(Panel, bpy.types.Panel):             # Codec
    bl_idname = "PATBLEND_PT_Codec"
    bl_label = "Coder-Decoder"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        codeType = prop.codeType

        activated = prop.activated
        if activated == False:
            return


        ########## Initialize
        PatAscii = ['1', '>', 'X', 'D', 'P', 'h', '3', 'F', ')', 'g', '/', 'U', 'M', 'I', 'z', 's', 'j', '-', ':', 'E', 'x', 'S', '\\', '.', 'W', '%', 
                    "'", '<', 'Z', '}', '?', 'd', '@', '5', '|', 'L', ']', '#', 'a', ' ', 'f', '9', 't', '7', 'J', 'l', 'w', 'K', ';', '&', 'm', 'T', 
                    'e', '"', '!', '6', 'C', 'Q', '(', ',', 'i', 'r', 'O', 'H', '*', '2', 'o', 'n', '=', 'u', 'A', '[', '$', 'b', 'p', '+', 'B', 'k', 
                    '_', 'v', 'N', '4', '^', 'V', '{', 'y', '8', '0', 'Y', 'c', 'G', 'R', 'q', '`', '~']

        PatScramAscii = ['A', 'R', 'V', 'W', '(', 'Z', ']', '7', '`', 'S', 'z', 'u', '$', 'U', '|', 'o', 'J', 'p', '=', 'l', '>', 'j', "'", 'q', 'c', 
                         'b', 'N', '<', 'i', 'k', '3', '+', 'r', '}', 'E', 't', 'x', 'n', 'F', '~', '"', '{', 'I', 'Q', 'C', '8', '&', '\\', '2', '/', 
                         'P', '6', '.', '4', ':', 'X', 'G', 'H', ',', 'T', '!', '5', '%', 'w', '#', '1', '?', 'Y', 'K', '^', 'h', 'v', '*', 'm', 'a', 
                         '9', ' ', 's', '[', '@', ')', 'y', ';', '0', 'e', 'O', 'g', 'M', 'd', '_', 'f', 'B', '-', 'D', 'L']
        
        def GetPos(char):
            for i in range(len(PatAscii)):
                if PatAscii[i] == char:
                    return i

        def GetScramPos(char):
            for i in range(len(PatScramAscii)):
                if PatScramAscii[i] == char:
                    return i
        
        def PatCodec1(decode, input):
            output = ""
            for i in range(len(input)):
                char = input[i]
                char = GetPos(char)
                if decode == True:
                    char = (char - 74) % len(PatAscii)
                else:
                    char = (char + 74) % len(PatAscii)
                char = PatAscii[char]
                output += char

            return output

        def PatCodec2(decode, input):
            output = ""
            for i in range(len(input)):
                char = input[i]
                char = GetPos(char)
                if decode == True:
                    char = (char - 13) % len(PatAscii)
                else:
                    char = (char + 13) % len(PatAscii)
                char = PatAscii[char]
                output += char
            return output

        def PatCodec3(decode, input):
            output = ""
            for i in range(len(input)):
                char = input[i]
                if decode:
                    char = GetScramPos(char)
                    char = PatAscii[char]
                else:
                    char = GetPos(char)
                    char = PatScramAscii[char]
                output += char
            return output

        def PatCodecCust(decode, input, offset):
            output = ""
            for i in range(len(input)):
                char = input[i]
                char = GetPos(char)
                if decode == True:
                    char = (char - offset) % len(PatAscii)
                else:
                    char = (char + offset) % len(PatAscii)
                char = PatAscii[char]
                output += char
            return output

        decode = prop.function == {'1'}
        input = prop.codeIn
        if codeType == '0':
            coded = PatCodec1(decode, input)
        
        elif codeType == '1':
            coded = PatCodec2(decode, input)
        
        elif codeType == '2':
            coded = PatCodec3(decode, input)
        
        elif codeType == '3':
            offset =  prop.custCodeOffset
            coded = PatCodecCust(decode, input, offset)
        
        global PatBlendCodecCoded
        PatBlendCodecCoded = coded

        

        ########## Drawing
        row = layout.row()
        row.scale_y = GetSize(theme, 3)
        row.prop(prop, "function", expand = True)

        if prop.function not in [{'0'}, {'1'}]:
            layout.label(text = "Select exactly one function.")
            return
        
        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "codeType")
        
        if codeType == '3':
            row = layout.row()
            row.scale_y = GetSize(theme, 1)
            row.prop(prop, "custCodeOffset")

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "codeIn")
        
        row = layout.row()
        row.scale_y = GetSize(theme, 1)
        row.prop(prop, "dateTimeStamp")

        layout.label(text = coded)

        row = layout.row()
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.create_text")

        layout.separator()

class PATBLEND_PT_UnitMani(Panel, bpy.types.Panel):          # Unit Main
    bl_idname = "PATBLEND_PT_UnitMani"
    bl_label = "Unit Manipulator"

    def draw(self, context):
        scene = context.scene
        prop = scene.patblend

        activated = prop.activated
        if activated == False:
            return

class PATBLEND_PT_UnitLength(Panel, bpy.types.Panel):        # Length
    bl_label = "Length"
    bl_parent_id = "PATBLEND_PT_UnitMani"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        function = prop.lengthFunc

        activated = prop.activated
        if activated == False:
            return
        
        dec = prop.lengthPrec
        unit1 = prop.lengthType1
        unit2 = prop.lengthType2
        num = round(prop.lengthNum, dec)

        toMeterMult = [1000, 100, 1, 0.001, 39.37, 3.28, 1.09, 0.000625]

        meters = num / toMeterMult[int(unit1)]
        unit2s = round(meters * toMeterMult[int(unit2)], dec)

        if num == 1:
            if unit1 == '0':
                text1 = str(num) + " " + "Milimeter"
            if unit1 == '1':
                text1 = str(num) + " " + "Centimeter"
            if unit1 == '2':
                text1 = str(num) + " " + "Meter"
            if unit1 == '3':
                text1 = str(num) + " " + "Kilometer"
            if unit1 == '4':
                text1 = str(num) + " " + "Inch"
            if unit1 == '5':
                text1 = str(num) + " " + "Foot"
            if unit1 == '6':
                text1 = str(num) + " " + "Yard"
            if unit1 == '7':
                text1 = str(num) + " " + "Mile"
        else:
            if unit1 == '0':
                text1 = str(num) + " " + "Milimeters"
            if unit1 == '1':
                text1 = str(num) + " " + "Centimeters"
            if unit1 == '2':
                text1 = str(num) + " " + "Meters"
            if unit1 == '3':
                text1 = str(num) + " " + "Kilometers"
            if unit1 == '4':
                text1 = str(num) + " " + "Inches"
            if unit1 == '5':
                text1 = str(num) + " " + "Feet"
            if unit1 == '6':
                text1 = str(num) + " " + "Yards"
            if unit1 == '7':
                text1 = str(num) + " " + "Miles"
            

        if unit2s == 1:
            if unit2 == '0':
                text2 = str(unit2s) + " " + "Milimeter"
            if unit2 == '1':
                text2 = str(unit2s) + " " + "Centimeter"
            if unit2 == '2':
                text2 = str(unit2s) + " " + "Meter"
            if unit2 == '3':
                text2 = str(unit2s) + " " + "Kilometer"
            if unit2 == '4':
                text2 = str(unit2s) + " " + "Inch"
            if unit2 == '5':
                text2 = str(unit2s) + " " + "Foot"
            if unit2 == '6':
                text2 = str(unit2s) + " " + "Yard"
            if unit2 == '7':
                text2 = str(unit2s) + " " + "Mile"
        else:
            if unit2 == '0':
                text2 = str(unit2s) + " " + "Milimeters"
            if unit2 == '1':
                text2 = str(unit2s) + " " + "Centimeters"
            if unit2 == '2':
                text2 = str(unit2s) + " " + "Meters"
            if unit2 == '3':
                text2 = str(unit2s) + " " + "Kilometers"
            if unit2 == '4':
                text2 = str(unit2s) + " " + "Inches"
            if unit2 == '5':
                text2 = str(unit2s) + " " + "Feet"
            if unit2 == '6':
                text2 = str(unit2s) + " " + "Yards"
            if unit2 == '7':
                text2 = str(unit2s) + " " + "Miles"


        row = layout.row(align = True)
        row.scale_y = GetSize(theme, 3)
        row.prop(prop, "lengthFunc")

        if function in [{'0'}, {'1'}]:
            if function == {'0'}:
                row = layout.row(align = True)
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "lengthType1", text = "From")

                row = layout.row(align = True)
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "lengthType2", text = "To")

                row = layout.row(align = True)
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "lengthNum")
                row.prop(prop, "lengthPrec")
                
                layout.label(text = text1)
                layout.label(text = "Equals")
                layout.label(text = text2)
            
            elif function == {'1'}:
                row = layout.row(align = True)
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "lengthType1", text = "Unit")

                if unit1 == '0':
                    layout.label(text = "One milimeter is")
                    layout.label(text = "  - 0.001 meters")
                    layout.label(text = "  - Width of a staple")
                    layout.label(text = "  - Thickness of a Dime")
                elif unit1 == '1':
                    layout.label(text = "One centimeter is")
                    layout.label(text = "  - 0.01 Meters")
                    layout.label(text = "  - Pencil Diameter")
                    layout.label(text = "  - Length of a staple")
                elif unit1 == '2':
                    layout.label(text = "One meter is")
                    layout.label(text = "  - 1 Meter")
                    layout.label(text = "  - Height of a kitchen counter")
                    layout.label(text = "  - Circumference of a Car Wheel")
                elif unit1 == '3':
                    layout.label(text = "One kilometer is")
                    layout.label(text = "  - 1000 meters")
                    layout.label(text = "  - 2 KM: Height of the lowest clouds.")
                elif unit1 == '4':
                    layout.label(text = "One inch is")
                    layout.label(text = "  - One inch")
                    layout.label(text = "  - Rubber Eraser Width")
                    layout.label(text = "  - Water Bottle Cap")
                elif unit1 == '5':
                    layout.label(text = "One foot is")
                    layout.label(text = "  - 12 Inches")
                    layout.label(text = "  - A standard ruler")
                    layout.label(text = "  - A standard paper's length")
                elif unit1 == '6':
                    layout.label(text = "One yard is")
                    layout.label(text = "  - 36 Inches")
                    layout.label(text = "  - A yardstick")
                    layout.label(text = "  - Height of a 5 year old")
                elif unit == '7':
                    layout.label(text = "One mile is")
                    layout.label(text = "  - 1760 Yards")
                    layout.label(text = "  - 1600 Meters")
                    layout.label(text = "  - Used for measuring speed (mph)")
            layout.separator()
        else:
            layout.label(text = "Please select exactly one function.")
            layout.separator()

class PATBLEND_PT_UnitTime(Panel, bpy.types.Panel):          # Time
    bl_label = "Time"
    bl_parent_id = "PATBLEND_PT_UnitMani"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        function = prop.timeFunc

        activated = prop.activated
        if activated == False:
            return

        row = layout.row(align = True)
        row.scale_y = GetSize(theme, 3)
        row.prop(prop, "timeFunc")

        layout.separator()

        if function == '0':
            unit = prop.timeNumType          # Get number seconds
            numUnits = prop.timeNum
            if unit == '0':
                seconds = numUnits
            elif unit == '1':
                seconds = numUnits * 60
            elif unit == '2':
                seconds = numUnits * 3600

            hours = math.floor(seconds / 3600) # Get hours
            seconds -= hours * 3600
            minutes = math.floor(seconds / 60)  # Get minutes
            seconds -= minutes * 60
            seconds = round(seconds, 2)

            if hours < 10:
                hours = "0" + str(hours)
            else:
                hours = str(hours)
            if minutes < 10:
                minutes = "0" + str(minutes)
            else:
                minutes = str(minutes)
            if seconds < 10:
                seconds = "0" + str(seconds)
            else:
                seconds = str(seconds)

            text = hours + " : " + minutes + " : " + seconds

            row = layout.row(align = True)
            row.scale_y = GetSize(theme, 2)
            row.prop(prop, "timeNumType")

            row = layout.row(align = True)
            row.scale_y = GetSize(theme, 1)
            row.prop(prop, "timeNum")

            layout.separator()
            layout.label(text = text)
            layout.separator()

        elif function == '1':
            strTime = prop.timeStandard
            unit = prop.timeNumType

            if len(strTime) != 11:
                row = layout.row(align = True)
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "timeStandard")

                row = layout.row(align = True)
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "timeNumType", text = "Out")

                layout.separator()
                layout.label(text = "Please enter a valid time.")
                return

            if strTime[2] != ":" or strTime[5] != ":" or strTime[8] != ".":
                row = layout.row(align = True)
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "timeStandard")

                row = layout.row(align = True)
                row.scale_y = GetSize(theme, 2)
                row.prop(prop, "timeNumType", text = "Out")

                layout.separator()
                layout.label(text = "Please enter a valid time.")
                return

            numHour = int(strTime[0:2])
            numMin = int(strTime[3:5])
            numSec = float(strTime[6:11])

            if unit == '0':
                finalNum = numSec + numMin * 60 + numHour * 3600
            elif unit == '1':
                finalNum = numSec / 60 + numMin + numHour * 60
            elif unit == '2':
                finalNum = numSec / 3600 + numMin / 60 + numHour

            row = layout.row(align = True)
            row.scale_y = GetSize(theme, 2)
            row.prop(prop, "timeStandard")

            row = layout.row(align = True)
            row.scale_y = GetSize(theme, 2)
            row.prop(prop, "timeNumType", text = "Out")

            layout.separator()
            layout.label(text = str(round(finalNum, 2)))
            layout.separator()

        elif function == '2':
            layout.label(text = "will be added later")
            layout.separator()

class PATBLEND_PT_LibraryMain(Panel, bpy.types.Panel):
    bl_label = "PatBlend Library"
    bl_idname = "PATBLEND_PT_LibraryMain"

    def draw(self, context):
        global custIcons
        layout = self.layout
        prop = context.scene.patblend
        theme = prop.sizeTheme

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "libWord")
        
        row = layout.row()
        row.template_icon_view(context.scene, 'my_thumbnails')

        row = layout.row(align = True)
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.library_preview")
        row.operator("patblend.library_download")


classess = (PATBLEND_PT_Settings,           # Settings
            PATBLEND_PT_SettingsQuick,
            PATBLEND_PT_SettingsLinks,
            
            PATBLEND_PT_RenderSetup,        # Render Setup
            PATBLEND_PT_RenderEngine,
            PATBLEND_PT_OutputSettings,
    
            PATBLEND_PT_Search,             # Search
            
            PATBLEND_PT_Codec,              # Codec
            
            PATBLEND_PT_UnitMani,           # Unit Manipulator
            PATBLEND_PT_UnitLength,
            PATBLEND_PT_UnitTime,

            PATBLEND_PT_LibraryMain)        # Library
            
def register():                                              # Runs each class
    from bpy.types import Scene
    from bpy.props import StringProperty, EnumProperty
    from bpy.utils import register_class
    
    global custIcons
    custIcons = bpy.utils.previews.new()
    scriptPath = bpy.path.abspath(os.path.dirname(__file__))
    iconsDir = os.path.join(os.path.dirname(scriptPath), "icons")
    custIcons.load("icon", os.path.join(iconsDir, "icon.png"), 'IMAGE')

    pcoll = bpy.utils.previews.new()
    pcoll.images_location = os.path.join(os.path.dirname(__file__), "assets")
    preview_collections["thumbnail_previews"] = pcoll
    bpy.types.Scene.my_thumbnails = EnumProperty(
        items=generate_previews()
    )

    patblend_operators.register()
    for cls in classess:
        register_class(cls)
    
def unregister():                                            # Unruns each class
    from bpy.types import WindowManager
    from bpy.utils import unregister_class
    
    global custIcons
    bpy.utils.previews.remove(custIcons)
    patblend_operators.unregister()
    
    for pcoll in previewCollections.values():
        bpy.utils.previews.remove(pcoll)
    previewCollections.clear()
    del bpy.types.Scene.my_thumbnails
    
    for cls in reversed(classess):
        unregister_class(cls)