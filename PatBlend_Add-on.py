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
    "name":        "PatBlend Add-on Experimental",
    "description": "A compilation of all Add-ons made by PatBlend",
    "author":      "Patrick Huang, PatBlend <https://sites.google.com/view/patblend>",
    "version":     (1, 0, 2),
    "blender":     (2, 80, 0),
    "location":    "3D View >> Sidebar >> PatBlend",
    "warning":     "This Add-on is still in Alpha, and new features are constantly being added.",
    "wiki_url":    "https://github.com/PatBlend/Patblend_Add-on",
    "tracker_url": "https://docs.google.com/forms/d/e/1FAIpQLScJGRE0jJu17OvDQ5o-BK56fIaUuzbP086LXhQdzMB_ySBbrw/viewform?usp=sf_link",
    "category":    "PatBlend"}


import bpy, math, time, datetime
from bpy.props import (StringProperty,      # Import Blender python properties
                       BoolProperty, 
                       IntProperty, 
                       FloatProperty, 
                       FloatVectorProperty, 
                       EnumProperty, 
                       PointerProperty
                       )
from bpy.types import (Panel,               # Import Blender UI Types
                       Menu, 
                       Operator, 
                       PropertyGroup
                       )
activated = False


########## Properties ##########
class PatBlendProps(PropertyGroup):
    # Add-on Settings
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
            ('0', "No anti-aliasing", "Bare image"),
            ('1', "Single Pass anti-aliasing", "Smooths edges"),
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
            ('2', "PatBlend 3", "PatBlend codec number 3")
        ]
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


########## Other Functions ##########
def GetSize(theme, type):
    if theme == '0':
        return 1
    elif theme == '1':
        if type == 4:
            return 1.5
        else:
            return 1
    elif theme == '2':
        if type == 4:
            return 2
        elif type == 3:
            return 1.5
        else:
            return 1
    elif theme == '3':
        if type == 1:
            return 1
        elif type == 2:
            return 1.5
        elif type == 3:
            return 2.5
        elif type == 4:
            return 3.5
    elif theme == '4':
        return type * 1.5 + 0.5

def GetDateTime():
    raw = str(datetime.datetime.now())
    date = raw[0:10]
    time = raw[11:19]
    return [date, time]

def CheckText():
    if "PatBlend_Logging" in bpy.data.texts:
        PatText = bpy.data.texts['PatBlend_Logging']
    else:
        PatText = bpy.data.texts.new("PatBlend_Logging")
    return PatText

########## Operators ##########
class PATBLEND_OT_Activate(Operator):
    bl_label = "Activate Add-on"
    bl_idname = "patblend.activate"

    def execute(self, context):
        global activated
        activated = True
        
        return {'FINISHED'}

class PATBLEND_OT_DisablePrompt(Operator):
    bl_label = "Disable Add-on"
    bl_idname = "patblend.disable_prompt"
    bl_description = "Unchecks the checkbox in User Preferences."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Pressed Button Disable\n")
        text.write("______________________________\n\n")

        bpy.ops.patblend.disable_warning('INVOKE_DEFAULT')
        
        return {'FINISHED'}

class PATBLEND_OT_Disable(Operator):
    bl_label = "Are you sure?"
    bl_idname = "patblend.disable_warning"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1
        col.label(text = "The add-on will be disabled until you enable it again.")
        col.label(text = "You can find it in preferences by searching \"PatBlend\".")

    def execute(self, context):
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Disabled PatBlend Add-on\n")
        text.write("______________________________\n\n")
        
        bpy.ops.preferences.addon_disable(module = "PatBlend_Add-on")
        return {'FINISHED'}

class PATBLEND_OT_UninstallPrompt(Operator):
    bl_label = "Uninstall Add-on"
    bl_idname = "patblend.uninstall_prompt"
    bl_description = "Removes the Add-on from the system."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Pressed Button Uninstall\n")
        text.write("______________________________\n\n")

        bpy.ops.patblend.uninstall_warning('INVOKE_DEFAULT')

        return {'FINISHED'}

class PATBLEND_OT_Uninstall(Operator):
    bl_label = "Are you sure?"
    bl_idname = "patblend.uninstall_warning"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        scene = context.scene
        prop = scene.patblend
        open = prop.openGit
        down = prop.downloadLatest
        
        col = self.layout.column()
        col.scale_y = 1
        col.label(text = "The add-on will be gone until you install it again.")
        col.label(text = "Note: Blender may crash when uninstalling.")
        col.label(text = "Note: This action cannot be undone.")
        if open:
            col.label(text = "Confirming will also open the PatBlend GitHub.")
            if down:
                col.label(text = "Blender will also automatically download the latest version.")

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        open = prop.openGit
        down = prop.downloadLatest

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Uninstalled PatBlend Add-on\n")
        text.write("______________________________\n\n")

        if open:
            bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
            if down:
                bpy.ops.wm.url_open(url="https://github.com/PatBlend/Patblend_Add-on/archive/master.zip")
        time.sleep(0.15)
        bpy.ops.preferences.addon_disable(module = "PatBlend_Add-on")
        time.sleep(0.15)
        bpy.ops.preferences.addon_remove(module = "PatBlend_Add-on")
        time.sleep(0.15)
        return {'FINISHED'}

class PATBLEND_OT_LinkGit(Operator):
    bl_label = "GitHub"
    bl_idname = "patblend.open_git"
    bl_description = "Opens the PatBlend GitHub."

    def execute(self, context):
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Opened PatBlend GitHub\n")
        text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
        return {'FINISHED'}

class PATBLEND_OT_LinkSite(Operator):
    bl_label = "Website"
    bl_idname = "patblend.open_site"
    bl_description = "Opens the PatBlend Website."

    def execute(self, context):
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Opened PatBlend Website\n")
        text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://sites.google.com/view/patblend")
        return {'FINISHED'}

class PATBLEND_OT_Documentation(Operator):
    bl_label = "Documentation"
    bl_idname = "patblend.documentation"
    bl_description = "Opens a document with documentation"

    def execute(self, context):
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Opened Add-on Documentation\n")
        text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://docs.google.com/document/d/1XOM4b5h3V0qt4dcGYBnKsm38zUuzH1tuJu2kfg3YACA/edit")
        return {'FINISHED'}

class PATBLEND_OT_ReportBug(Operator):
    bl_label = "Report a Bug"
    bl_idname = "patblend.report_bug"
    bl_description = "Goes to the page to report a bug."

    def execute(self, context):
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Opened Report a Bug Form\n")
        text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://docs.google.com/forms/d/e/1FAIpQLScJGRE0jJu17OvDQ5o-BK56fIaUuzbP086LXhQdzMB_ySBbrw/viewform?usp=sf_link")
        return {'FINISHED'}

class PATBLEND_OT_DownloadLatest(Operator):
    bl_label = "Download Latest Version"
    bl_idname = "patblend.download_latest"
    bl_description = "Downloads the master branch in GitHub."

    def execute(self, context):
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Downloaded Master Branch\n")
        text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/master.zip")
        return {'FINISHED'}

class PATBLEND_OT_DownloadPrevious(Operator):
    bl_label = "Download Previous Version"
    bl_idname = "patblend.download_previous"
    bl_description = "Downloads the selected version."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        version = prop.version

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Downloaded " + version + "\n")
        text.write("______________________________\n\n")

        if version == '1.0.0':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.0.zip"
        if version == '1.0.1':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.1.zip"
        if version == '1.0.2 Alpha':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.2-alpha.zip"
        if version == 'Master':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/master.zip"
        
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
        bpy.ops.wm.url_open(url = url)
        return {'FINISHED'}

class PATBLEND_OT_DownloadAll(Operator):
    bl_label = "Download All!"
    bl_idname = "patblend.download_all"
    bl_description = "Downloads all versions including previous versions and the current version."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Pressed Button Download all\n")
        text.write("______________________________\n\n")

        bpy.ops.patblend.download_all_confirm('INVOKE_DEFAULT')

        return {'FINISHED'}

class PATBLEND_OT_DownloadAllConfirm(Operator):
    bl_label = "Are you sure?"
    bl_idname = "patblend.download_all_confirm"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1
        col.label(text = "This will download the following 4 files:")
        col.label(text = "    PatBlend_Add-on-master")
        col.label(text = "    PatBlend_Add-on-v1.0.0")
        col.label(text = "    PatBlend_Add-on-v1.0.1")
        col.label(text = "    PatBlend_Add-on-v1.0.2-alpha")
        col.label(text = "")
        col.label(text = "The combined file size is 80.4 KB")

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        version = prop.version

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Downloaded all versions\n")
        text.write("______________________________\n\n")

        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.0.zip")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.1.zip")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.2-alpha.zip")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/master.zip")

        return {'FINISHED'}

class PATBLEND_OT_RenderSetup(Operator):
    bl_label = "Setup"
    bl_idname = "patblend.render_setup"
    bl_description = "Setup the render engine according to the settings."

    def execute(self, context):
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Set up render engines\n")
        text.write("______________________________\n\n")
        
        return {'FINISHED'}

class PATBLEND_OT_Search(Operator):
    bl_label = "Search"
    bl_idname = "patblend.search"
    bl_description = "Searches whatever is in the address box."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        address = prop.address
        force = prop.searchForce

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Searched\n")
        text.write("______________________________\n\n")

        def CheckUrl(address):
            url = False
            tld = ['.com', '.org', '.co', '.it', '.net', '.gov', '.im', '.io', '.edu']
            for string in tld:
                if string in address:
                    url = True
            return url

        
        if force == '0':
            url = CheckUrl(address)
            if not url:
                address = "http://www.google.com/search?q=" + address
            if not "http://" in address:
                address = "http://" + address
        elif force == '1':
            if not "http://" in address and not "https://" in address:
                address = "http://" + address
        elif force == '2':
            address = "http://www.google.com/search?q=" + address
        
        bpy.ops.wm.url_open(url = address)

        return {'FINISHED'}

class PATBLEND_OT_CreateText(Operator):
    bl_label = "Create Text"
    bl_description = "Creates a text datablock with the code."
    bl_idname = "patblend.create_text"

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        dts = prop.dateTimeStamp

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        text.write(dateTime + "\n")
        text.write("Created codec Text\n")
        text.write("______________________________\n\n")

        dateTime = GetDateTime()
        if "PatBlend_Add-on_Coder" in bpy.data.texts:
            newText = bpy.data.texts["PatBlend_Add-on_Coder"]
        else:
            newText = bpy.data.texts.new("PatBlend_Add-on_Coder")
        
        if dts:
            newText.write("Created on " + dateTime[0] + ", " + dateTime[1] + "\n\n")
        newText.write(PatBlendCodecCoded + "\n")
        newText.write("__________________________________________________" + "\n\n")

        return {'FINISHED'}



########## Panels ##########
class Panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PatBlend"
    bl_options = {"DEFAULT_CLOSED"}

class PATBLEND_PT_Activate(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_Activate"
    bl_label = "Activate Add-on"

    def draw(self, context):
        layout = self.layout
        layout.operator("patblend.activate")

class PATBLEND_PT_Settings(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_Settings"
    bl_label = "Settings"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme

class PATBLEND_PT_SettingsQuick(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_Settings"
    bl_label = "Quick Settings"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme

        row = layout.row(align = True)
        row.scale_y = GetSize(theme, 4)
        row.operator("patblend.uninstall_prompt", text = "Uninstall")
        row.operator("patblend.disable_prompt", text = "Disable")

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "openGit")
        
        row = layout.row()
        row.enabled = prop.openGit
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "downloadLatest")

        row = layout.row()
        row.scale_y = GetSize(theme, 3)
        row.prop(prop, "sizeTheme")

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "consoleInfo")

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "textInfo")

class PATBLEND_PT_SettingsLinks(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_Settings"
    bl_label = "PatBlend Links"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        ver = prop.version

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "version")

        layout.label(text = "Download")

        col = layout.column(align = True)
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 4)
        row.operator("patblend.download_latest", text = "Latest")
        row.operator("patblend.download_previous", text = ver)
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 4)
        row.operator("patblend.download_all")

        layout.separator()
        layout.label(text = "Web Links")

        col = layout.column(align = True)
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.open_git")
        row.operator("patblend.open_site")
        row = col.row(align = True)
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.documentation")
        row.operator("patblend.report_bug")

class PATBLEND_PT_RenderSetup(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_RenderSetup"
    bl_label = "Render Setup"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        engine = prop.engine

        if engine in [{'1'}, {'2'}, {'0'}]:
            row = layout.row()
            row.scale_y = GetSize(theme, 3)
            row.operator("patblend.render_setup")
        else:
            layout.label(text = "Select exactly one render engine.")

class PATBLEND_PT_RenderEngine(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderSetup"
    bl_label = "Engine Specific"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        engine = prop.engine

        if engine in [{'1'}, {'2'}, {'0'}]:
            row = layout.row()
            row.scale_y = GetSize(theme, 2)
            row.prop(prop, "engine")

            row = layout.row()
            row.scale_y = GetSize(theme, 1)

            if engine == {'1'}:
                row.prop(prop, "workSamples")
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
        else:
            row = layout.row()
            row.scale_y = GetSize(theme, 2)
            row.prop(prop, "engine")
            layout.label(text = "Select exactly one render engine.")

class PATBLEND_PT_OutputSettings(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderSetup"
    bl_label = "Output Settings"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme

        row = layout.row(align = True)
        row.scale_y = GetSize(theme, 1)
        row.prop(prop, "outX")
        row.prop(prop, "outY")

        row = layout.row(align = True)
        row.scale_y = GetSize(theme, 1)
        row.prop(prop, "fps")
        
        col = layout.column(align = True)
        col.scale_y = GetSize(theme, 1)
        col.prop(prop, "worldCol")
        col.prop(prop, "worldStr")

class PATBLEND_PT_Search(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_Search"
    bl_label = "Quick Search"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "address")

        row = layout.row()
        row.scale_y = GetSize(theme, 2)
        row.prop(prop, "searchForce")

        row = layout.row()
        row.scale_y = GetSize(theme, 3)
        row.operator("patblend.search")

class PATBLEND_PT_Codec(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_Codec"
    bl_label = "Coder-Decoder"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        codeType = prop.codeType


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

        decode = prop.function == {'1'}
        input = prop.codeIn
        if codeType == '0':
            coded = PatCodec1(decode, input)
        elif codeType == '1':
            coded = PatCodec2(decode, input)
        elif codeType == '2':
            coded = PatCodec3(decode, input)
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

class PATBLEND_PT_UnitMani(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_UnitMani"
    bl_label = "Unit Manipulator"

    def draw(self, context):
        scene = context.scene
        prop = scene.patblend

class PATBLEND_PT_UnitLength(Panel, bpy.types.Panel):
    bl_label = "Length"
    bl_parent_id = "PATBLEND_PT_UnitMani"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        theme = prop.sizeTheme
        function = prop.lengthFunc
        
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
        else:
            layout.label(text = "Please select exactly one function.")

class PATBLEND_PT_UnitTime(Panel, bpy.types.Panel):
    bl_label = "Time"
    bl_parent_id = "PATBLEND_PT_UnitMani"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        layout.label(text = "Will be added later.")



classess = (PatBlendProps,        # There is an extra 's' to keep the letter count a multiple of 4.
           
            PATBLEND_OT_DisablePrompt,
            PATBLEND_OT_Disable,
            PATBLEND_OT_UninstallPrompt,
            PATBLEND_OT_Uninstall,
            PATBLEND_OT_LinkGit,
            PATBLEND_OT_LinkSite,
            PATBLEND_OT_Documentation,
            PATBLEND_OT_ReportBug,
            PATBLEND_OT_DownloadLatest,
            PATBLEND_OT_DownloadPrevious,
            PATBLEND_OT_DownloadAll,
            PATBLEND_OT_DownloadAllConfirm,
            PATBLEND_OT_RenderSetup,
            PATBLEND_OT_CreateText,
            
            PATBLEND_OT_Search,

            PATBLEND_PT_Settings,
            PATBLEND_PT_SettingsQuick,
            PATBLEND_PT_SettingsLinks,
            PATBLEND_PT_RenderSetup,
            PATBLEND_PT_RenderEngine,
            PATBLEND_PT_OutputSettings,
            PATBLEND_PT_Search,
            PATBLEND_PT_Codec,
            PATBLEND_PT_UnitMani,
            PATBLEND_PT_UnitLength,
            PATBLEND_PT_UnitTime)


def register():
    from bpy.utils import register_class
    for cls in classess:
        register_class(cls)
    bpy.types.Scene.patblend = PointerProperty(type = PatBlendProps)
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classess):
        unregister_class(cls)
    del bpy.types.Scene.patblend
    
if __name__ == "__main__":
    register()