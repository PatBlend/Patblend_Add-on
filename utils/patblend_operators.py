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

def GetDateTime():                                           # Gets Date and Time from datetime module and converts it into a list of strings.
    raw = str(datetime.datetime.now())  # yyyy-mm-dd hh:mm:ss.ssssss
    date = raw[0:10]                    # Gets yyyy-mm-dd
    time = raw[11:19]                   # Gets hh:mm:ss.ss
    return [date, time]

def CheckText():                                             # Checks if there is a PatBlend logging text. If not, creates one.
    if "PatBlend_Logging" in bpy.data.texts:
        PatText = bpy.data.texts['PatBlend_Logging']     # Creates new text
        PatText.cursor_set(1234567890, character = 1234567890)
    else:
        PatText = bpy.data.texts.new("PatBlend_Logging") # Sets "PatText" as the text
        PatText.cursor_set(1234567890, character = 1234567890)
    return PatText

class PATBLEND_OT_Activate(Operator):                        # Activates the Add-on
    bl_label = "Activate Add-on"
    bl_idname = "patblend.activate"
    bl_description = "Activates the Add-on"

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend

        prop.activated = True
        return {'FINISHED'}

class PATBLEND_OT_DisablePrompt(Operator):                   # Prompts a pop-up to disable the Add-on
    bl_label = "Disable Add-on"
    bl_idname = "patblend.disable_prompt"
    bl_description = "Unchecks the checkbox in User Preferences."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        
        textWrite = prop.textInfo
        if textWrite:
            text = CheckText()
            dateTime = GetDateTime()
            dateTime = dateTime[0] + " " + dateTime[1]

            text.write(dateTime + "\n")
            text.write("Pressed Button Disable\n")
            text.write("______________________________\n\n")

        bpy.ops.patblend.disable_warning('INVOKE_DEFAULT')
        
        return {'FINISHED'}

class PATBLEND_OT_Disable(Operator):                         # Disables Add-on
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
        scene = context.scene
        prop = scene.patblend
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Disabled PatBlend Add-on\n")
            text.write("______________________________\n\n")
        
        bpy.ops.preferences.addon_disable(module = "PatBlend_Add-on")
        return {'FINISHED'}

class PATBLEND_OT_UninstallPrompt(Operator):                 # Prompts a pop-up to uninstall the Add-on
    bl_label = "Uninstall Add-on"
    bl_idname = "patblend.uninstall_prompt"
    bl_description = "Removes the Add-on from the system."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Pressed Button Uninstall\n")
            text.write("______________________________\n\n")

        bpy.ops.patblend.uninstall_warning('INVOKE_DEFAULT')

        return {'FINISHED'}

class PATBLEND_OT_Uninstall(Operator):                       # Uninstalls Add-on
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

        textWrite = prop.textInfo
        if textWrite:
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

class PATBLEND_OT_LinkGit(Operator):                         # Opens PatBlend GitHub
    bl_label = "GitHub"
    bl_idname = "patblend.open_git"
    bl_description = "Opens the PatBlend GitHub."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Opened PatBlend GitHub\n")
            text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
        return {'FINISHED'}

class PATBLEND_OT_LinkReleases(Operator):                    # Opens Releases page in GitHub
    bl_label = "Releases"
    bl_idname = "patblend.open_git_releases"
    bl_description = "Opens the GitHub Releases page."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Opened PatBlend GitHub Releases\n")
            text.write("______________________________\n\n")

        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/releases")
        return {'FINISHED'}

class PATBLEND_OT_LinkSite(Operator):                        # Opens PatBlend Website
    bl_label = "Website" 
    bl_idname = "patblend.open_site"
    bl_description = "Opens the PatBlend Website."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Opened PatBlend Website\n")
            text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://sites.google.com/view/patblend")
        return {'FINISHED'}

class PATBLEND_OT_Documentation(Operator):                   # Opens documentation document
    bl_label = "Documentation"
    bl_idname = "patblend.documentation"
    bl_description = "Opens a document with documentation"

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Opened Add-on Documentation\n")
            text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://docs.google.com/document/d/1XOM4b5h3V0qt4dcGYBnKsm38zUuzH1tuJu2kfg3YACA/edit")
        return {'FINISHED'}

class PATBLEND_OT_ReportBug(Operator):                       # Opens Report a Bug form
    bl_label = "Report a Bug"
    bl_idname = "patblend.report_bug"
    bl_description = "Goes to the page to report a bug."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Opened Report a Bug Form\n")
            text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://forms.gle/rGULhrpfpCta7CWj9")
        return {'FINISHED'}

class PATBLEND_OT_DownloadLatest(Operator):                  # Downloads the master branch
    bl_label = "Download Latest Version"
    bl_idname = "patblend.download_latest"
    bl_description = "Downloads the master branch in GitHub."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Downloaded Master Branch\n")
            text.write("______________________________\n\n")
        
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/master.zip")
        return {'FINISHED'}

class PATBLEND_OT_DownloadPrevious(Operator):                # Downloads a previous version of the Add-on
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

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Downloaded " + version + "\n")
            text.write("______________________________\n\n")

        if version == '1.0.0':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.0.zip"
        elif version == '1.0.1':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.1.zip"
        elif version == '1.0.2 Alpha':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.2-alpha.zip"
        elif version == 'Master':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/master.zip"
        elif version == '1.0.2':
            url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.2.zip"
        
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
        bpy.ops.wm.url_open(url = url)
        return {'FINISHED'}

class PATBLEND_OT_DownloadAll(Operator):                     # Downloads all versions of the Add-on
    bl_label = "Download All!"
    bl_idname = "patblend.download_all"
    bl_description = "Downloads all versions including previous versions and the current version."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Pressed Button Download all\n")
            text.write("______________________________\n\n")

        bpy.ops.patblend.download_all_confirm('INVOKE_DEFAULT')

        return {'FINISHED'}

class PATBLEND_OT_DownloadAllConfirm(Operator):              # Confirms Download all
    bl_label = "Are you sure?"
    bl_idname = "patblend.download_all_confirm"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1
        col.label(text = "This will download the following 5 files:")
        col.label(text = "    PatBlend_Add-on-master")
        col.label(text = "    PatBlend_Add-on-v1.0.0")
        col.label(text = "    PatBlend_Add-on-v1.0.1")
        col.label(text = "    PatBlend_Add-on-v1.0.2-alpha")
        col.label(text = "    PatBlend_Add-on-v1.0.2")
        col.label(text = "")
        col.label(text = "The combined file size is 107 KB")

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        version = prop.version

        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Downloaded all versions\n")
            text.write("______________________________\n\n")

        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.0.zip")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.1.zip")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.2-alpha.zip")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/v1.0.2.zip")
        bpy.ops.wm.url_open(url = "https://github.com/PatBlend/Patblend_Add-on/archive/master.zip")

        return {'FINISHED'}

class PATBLEND_OT_RenderSetup(Operator):                     # Operator for Render Setup
    bl_label = "Setup"
    bl_idname = "patblend.render_setup"
    bl_description = "Setup the render engine according to the settings."

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        
        text = CheckText()
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Set up render engines\n")
            text.write("______________________________\n\n")
        
        if prop.engine == {'0'}:
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.eevee.taa_render_samples = prop.intSamples
            bpy.context.scene.eevee.taa_samples = 8192
            bpy.context.scene.eevee.use_gtao = prop.ao
            bpy.context.scene.eevee.use_ssr = prop.ssr
            bpy.context.scene.eevee.use_ssr_refraction = prop.ssr
            bpy.context.scene.eevee.use_motion_blur = True

            if prop.shadowQual == '0':
                bpy.context.scene.eevee.shadow_cube_size = '1024'
                bpy.context.scene.eevee.shadow_cascade_size = '1024'
                bpy.context.scene.eevee.use_shadow_high_bitdepth = False
            elif prop.shadowQual == '1':
                bpy.context.scene.eevee.shadow_cube_size = '2048'
                bpy.context.scene.eevee.shadow_cascade_size = '2048'
                bpy.context.scene.eevee.use_shadow_high_bitdepth = True
            elif prop.shadowQual == '1':
                bpy.context.scene.eevee.shadow_cube_size = '4096'
                bpy.context.scene.eevee.shadow_cascade_size = '4096'
                bpy.context.scene.eevee.use_shadow_high_bitdepth = True

        elif prop.engine == {'1'}:
            bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
            #bpy.context.scene.render_aa = '32'
            #bpy.context.scene.viewport_aa = '32'

        elif prop.engine == {'2'}:
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.aa_samples = prop.intSamples
            bpy.context.scene.cycles.preview_aa_samples = 8192
            
            if prop.cyclesDevice == '0':
                bpy.context.scene.cycles.device = 'CPU'
                bpy.context.scene.render.tile_x = 32
                bpy.context.scene.render.tile_y = 32
            elif prop.cyclesDevice == '1':
                bpy.context.scene.cycles.device = 'GPU'
                bpy.context.scene.render.tile_x = 256
                bpy.context.scene.render.tile_y = 256
            bpy.context.scene.cycles.progressive = 'BRANCHED_PATH'
            bpy.context.scene.cycles.transmission_samples = 2

            minBounce = math.floor(prop.bounces / 1.5)
            medBounce = prop.bounces
            maxBounce = math.floor(prop.bounces * 1.5)

            bpy.context.scene.cycles.max_bounces = maxBounce
            bpy.context.scene.cycles.diffuse_bounces = medBounce
            bpy.context.scene.cycles.glossy_bounces = medBounce
            bpy.context.scene.cycles.transparent_max_bounces = maxBounce
            bpy.context.scene.cycles.transmission_bounces = maxBounce
            bpy.context.scene.cycles.volume_bounces = minBounce

            bpy.context.scene.cycles.caustics_reflective = prop.caustics
            bpy.context.scene.cycles.caustics_refractive = prop.caustics
            bpy.context.scene.render.use_motion_blur = True

        bpy.context.scene.render.resolution_x = prop.outX
        bpy.context.scene.render.resolution_y = prop.outY

        bpy.context.scene.render.fps = prop.fps

        wrldCol = prop.worldCol
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (wrldCol[0], wrldCol[1], wrldCol[2], 1)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = prop.worldStr

        return {'FINISHED'}

class PATBLEND_OT_Search(Operator):                          # Operator for Quick Search
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

        textWrite = prop.textInfo
        if textWrite:
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
        
        address = address.replace("+", "%2B")
        address = address.replace(" ", "+")
        
        bpy.ops.wm.url_open(url = address)

        return {'FINISHED'}

class PATBLEND_OT_CreateText(Operator):                      # Creates text for the Codec
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

        textWrite = prop.textInfo
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Created codec Text\n")
            text.write("______________________________\n\n")

        dateTime = GetDateTime()
        if "PatBlend_Add-on_Coder" in bpy.data.texts:
            newText = bpy.data.texts["PatBlend_Add-on_Coder"]
            newText.cursor_set(1234567890, character = 1234567890)
        else:
            newText = bpy.data.texts.new("PatBlend_Add-on_Coder")
            newText.cursor_set(1234567890, character = 1234567890)
        
        if dts:
            newText.write("Created on " + dateTime[0] + ", " + dateTime[1] + "\n\n")
        newText.write(PatBlendCodecCoded + "\n")
        newText.write("__________________________________________________" + "\n\n")

        return {'FINISHED'}

class PATBLEND_OT_LibPreview(Operator):
    bl_label = "Preview"
    bl_description = "Observe preview images of the asset"
    bl_idname = "patblend.library_preview"

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        name = context.scene.my_thumbnails
        name = name.replace('.jpg', '')
        name = name.replace('.png', '')
        name = name.replace('.jpeg', '')
        
        text = CheckText()
        textWrite = prop.textInfo
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Viewed Preview Image\n")
            text.write("______________________________\n\n")

        bpy.ops.wm.url_open(url = "https://tinyurl.com/patblend-" + name + "-preview")
        return {'FINISHED'}

class PATBLEND_OT_LibDownload(Operator):
    bl_label = "Download"
    bl_description = "Download the complete asset"
    bl_idname = "patblend.library_download"

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        word = prop.libWord
        
        name = context.scene.my_thumbnails
        name = name.replace('.jpg', '')
        name = name.replace('.png', '')
        name = name.replace('.jpeg', '')
        
        text = CheckText()
        textWrite = prop.textInfo
        dateTime = GetDateTime()
        dateTime = dateTime[0] + " " + dateTime[1]
        if textWrite:
            text.write(dateTime + "\n")
            text.write("Downloaded asset\n")
            text.write("______________________________\n\n")

        if prop.libWord == "PatBlendLibrary":
            bpy.ops.wm.url_open(url = "https://tinyurl.com/patblend-" + name + "-download")
        else:
            bpy.ops.patblend.library_fail_notice('INVOKE_DEFAULT')
        return {'FINISHED'}

class PATBLEND_OT_LibraryFail(Operator):              # Confirms Download all
    bl_label = "Library Failed"
    bl_idname = "patblend.library_fail_notice"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column()
        col.label(text = "The activation word is incorrect.")

    def execute(self, context):
        return {'FINISHED'}

classess = (PATBLEND_OT_Activate,           # Activate button
            
            PATBLEND_OT_DisablePrompt,      # Disable/Uninstall
            PATBLEND_OT_Disable,
            PATBLEND_OT_UninstallPrompt,
            PATBLEND_OT_Uninstall,
            
            PATBLEND_OT_LinkGit,            # Links
            PATBLEND_OT_LinkReleases,
            PATBLEND_OT_LinkSite,
            PATBLEND_OT_Documentation,
            PATBLEND_OT_ReportBug,
            
            PATBLEND_OT_DownloadLatest,     # Download
            PATBLEND_OT_DownloadPrevious,
            PATBLEND_OT_DownloadAll,
            PATBLEND_OT_DownloadAllConfirm,
            
            PATBLEND_OT_RenderSetup,        # Render Setup
            
            PATBLEND_OT_CreateText,         # Codec
            
            PATBLEND_OT_Search,
            PATBLEND_OT_LibDownload,
            PATBLEND_OT_LibPreview,
            PATBLEND_OT_LibraryFail)

def register():                                              # Runs each class
    from bpy.utils import register_class
    for cls in classess:
        register_class(cls)
    
def unregister():                                            # Unruns each class
    from bpy.utils import unregister_class
    for cls in reversed(classess):
        unregister_class(cls)