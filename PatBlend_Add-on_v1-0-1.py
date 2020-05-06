########## Metadata ##########
bl_info = {
    "name":        "PatBlend Add-ons",
    "description": "A compilation of all Add-ons made by PatBlend",
    "author":      "Patrick Huang, PatBlend <https://sites.google.com/view/patblend>",
    "version":     (1, 0, 0),
    "blender":     (2, 80, 0),
    "location":    "3D View >> Sidebar >> PatBlend",
    "warning":     "",
    "wiki_url":    "https://drive.google.com/drive/folders/1EQd16cotHF_j7FOSmEMaYHfoJJgCYE9l",
    "tracker_url": "https://sites.google.com/view/patblend",
    "category":    "PatBlend"}
    

########## Library Import ##########
import bpy, math
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty)
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup)
##################################################################
# Properties
##################################################################
class PatBlendAddonProperties(PropertyGroup):
    ########## Render Setup Properties ##########
    # Eevee Begin
    E_samp: IntProperty(
        name="Samples",
        description="How many times Blender calculates in the render.",
        default=64, min=2, max=8192)
        
    E_viewSamp: IntProperty(
        name="Viewport Samples",
        description="How many times Blender calculates in the viewport.",
        default=8192, min=2, max=16777216)
        
    E_ao: BoolProperty(
        name="Use Ambient Occlusion",
        description="Adjust the brightness of colors according to the amount the normals are bent.",
        default=False)
        
    E_blm: BoolProperty(
        name="Bloom",
        description="Makes emission appear to have a glow.",
        default=False)
    
    E_ssr: BoolProperty(
        name="Screen Space Reflections",
        description="Allow transparency and reflection.",
        default=True)
    
    E_mb: BoolProperty(
        name="Motion Blur",
        description="Makes moving objects blurry.",
        default=True)
    
    E_trnsWrld: BoolProperty(
        name="Transparent World",
        description="Makes the world transparent.",
        default=False)
    
    E_outSize: EnumProperty(
        name="Output Size", 
        description="Pixel resolution of the final render.",
        items=[
            ('2', "1080×1920px", ""), 
            ('1', "720×1280px", ""), 
            ('0', "540×960px", ""), 
            ('3', "2160×3840px", ""),])
            
    E_custOutX: IntProperty(
        name="Output Size X",
        description="Horizontal pixel resolution of the final render.",
        default=1920)
        
    E_custOutY: IntProperty(
        name="Output Size Y",
        description="Vertical pixel resolution of the final render.",
        default=1080)
            
    E_animEnd: IntProperty(
        name="Animation Length",
        description="The end frame of the animation.",
        default=5000, min=2, max=100000)
        
    E_fps: IntProperty(
        name = "Frames per Second", 
        description = "Frame rate of the animation.", 
        default = 30, 
        min = 12, max = 240)
    
    E_backCol: FloatVectorProperty(
        name = "World Color", 
        subtype = 'COLOR', 
        description = "The color that shows up in the background.",
        default = (0.0, 0.0, 0.0), 
        min = 0.0, max = 1.0,)
    
    E_backStr: FloatProperty(
        name = "World Strength", 
        description = "The strength of background lighting.", 
        default = 1, 
        min = 0, max = 5)
        
    # Workbench Begin
    W_samp: EnumProperty(
        name="Sampling Type", 
        description="How Workbench samples the scene.",
        items=[
            ('0', "No Anti-Aliasing", ""), 
            ('1', "Anti-Aliasing", ""), 
            ('2', "5 Samples", ""), 
            ('3', "8 Samples", ""),
            ('4', "11 Samples", ""),
            ('5', "16 Samples", ""),
            ('6', "32 Samples", ""),])
            
    W_trnsWrld: BoolProperty(
        name="Transparent World",
        description="Makes the world transparent.",
        default=False)
            
    W_custOutX: IntProperty(
        name="Output Size X",
        description="Horizontal pixel resolution of the final render.",
        default=1920)
        
    W_custOutY: IntProperty(
        name="Output Size Y",
        description="Vertical pixel resolution of the final render.",
        default=1080)
            
    W_animEnd: IntProperty(
        name="Animation Length",
        description="The end frame of the animation.",
        default=5000, min=2, max=100000)
        
    W_fps: IntProperty(
        name = "Frames per Second", 
        description = "Frame rate of the animation.", 
        default = 30, 
        min = 12, max = 240)
    
    W_backCol: FloatVectorProperty(
        name = "World Color", 
        subtype = 'COLOR', 
        description = "The color that shows up in the background.",
        default = (0.0, 0.0, 0.0), 
        min = 0.0, max = 1.0,)
    
    W_backStr: FloatProperty(
        name = "World Strength", 
        description = "The strength of background lighting.", 
        default = 1, 
        min = 0, max = 5)
        
    # Cycles Begin
    C_device: EnumProperty(
        name="Render Device", 
        description="What device to render with", 
        items=[
            ('1', "GPU Compute", ""), 
            ('0', "CPU", ""),])
            
    C_samp: IntProperty(
        name="Samples",
        description="How many times Blender calculates in the render.",
        default=64, min=2, max=8192)
        
    C_viewSamp: IntProperty(
        name="Viewport Samples",
        description="How many times Blender calculates in the viewport.",
        default=8192, min=2, max=16777216)
        
    C_sampType: EnumProperty(
        name="Sampling Type", 
        description="Path Tracing or Branched Path Tracing", 
        items=[
            ('1', "Branched Path Tracing", ""), 
            ('0', "Path Tracing", ""),])
            
    C_bounces: IntProperty(
        name = "Light Bounces", 
        description="How many times light bounces.", 
        default = 3, 
        min = 0, max = 20)
    
    C_caustics: BoolProperty(
        name="Use Caustics", 
        description="Calculates light reflection and refraction patterns.", 
        default = False)
    
    C_mb: BoolProperty(
        name="Motion Blur",
        description="Makes moving objects blurry.",
        default=True)
    
    C_trnsWrld: BoolProperty(
        name="Transparent World",
        description="Makes the world transparent.",
        default=False)
        
    C_outSize: EnumProperty(
        name="Output Size", 
        description="Pixel resolution of the final render.",
        items=[
            ('2', "1080×1920px", ""), 
            ('1', "720×1280px", ""), 
            ('0', "540×960px", ""), 
            ('3', "2160×3840px", ""),])
            
    C_custOutX: IntProperty(
        name="Output Size X",
        description="Horizontal pixel resolution of the final render.",
        default=1920)
        
    C_custOutY: IntProperty(
        name="Output Size Y",
        description="Vertical pixel resolution of the final render.",
        default=1080)
            
    C_animEnd: IntProperty(
        name="Animation Length",
        description="The end frame of the animation.",
        default=5000, min=2, max=100000)
        
    C_fps: IntProperty(
        name = "Frames per Second", 
        description = "Frame rate of the animation.", 
        default = 30, 
        min = 12, max = 240)
    
    C_backCol: FloatVectorProperty(
        name = "World Color", 
        subtype = 'COLOR', 
        description = "The color that shows up in the background.",
        default = (0.0, 0.0, 0.0), 
        min = 0.0, max = 1.0,)
    
    C_backStr: FloatProperty(
        name = "World Strength", 
        description = "The strength of background lighting.", 
        default = 1, 
        min = 0, max = 5)
        
    ########## Search Properties ##########
    search_url: StringProperty(
        name="Query",
        description="URL",
        )
        
    ########## Unit Converter Properties ##########
    inputType: EnumProperty(
        name = "From",
        description = "Input unit type",
        items = [
            ('0', "Milimeter", ""),
            ('1', "Centimeter", ""),
            ('2', "Meter", ""),
            ('3', "Kilometer", ""),
            ('4', "Inch", ""),
            ('5', "Foot", ""),
            ('6', "Yard", ""),
            ('7', "Mile", "")])
            
    outputType: EnumProperty(
        name = "To",
        description = "Output unit type",
        items = [
            ('0', "Milimeter", ""),
            ('1', "Centimeter", ""),
            ('2', "Meter", ""),
            ('3', "Kilometer", ""),
            ('4', "Inch", ""),
            ('5', "Foot", ""),
            ('6', "Yard", ""),
            ('7', "Mile", "")])
            
    input: FloatProperty(
        name = "Input",
        description = "Input value",
        default = 10,
        min = 0)
        
    precision: IntProperty(
        name = "Decimal Precision",
        description = "Amount of decimal places to display",
        default = 3,
        min = 0, max = 20)
        
    console: BoolProperty(
        name = "Show info in console",
        description = "Shows important information in the system console as the add-on functions.",
        default = True)
        
        
        

##################################################################
# Other Functions
##################################################################

########## Unit Converter ##########
def GetUnitName(unit):
    unit = int(unit)
    if unit == 0:
        value = "Milimeter"
    elif unit == 1:
        value = "Centimeter"
    elif unit == 2:
        value = "Meter"
    elif unit == 3:
        value = "Kilometer"
    elif unit == 4:
        value = "Inch"
    elif unit == 5:
        value = "Foot"
    elif unit == 6:
        value = "Yard"
    elif unit == 7:
        value ="Mile"
    return value

def ToMeter(unit, value):
    unit = int(unit)
    if unit == 0:
        value /= 1000
    elif unit == 1:
        value /= 100
    elif unit == 2:
        value = value
    elif unit == 3:
        value *= 1000
    elif unit == 4:
        value *= 2.54
        value /= 100
    elif unit == 5:
        value *= 12
        value *= 2.54
        value /= 100
    elif unit == 6:
        value *= 36
        value *= 2.54
        value /= 100
    elif unit == 7:
        value *= 1600
    return value

def FromMeter(unit, value):
    unit = int(unit)
    if unit == 0:
        value *= 1000
    elif unit == 1:
        value *= 100
    elif unit == 2:
        value = value
    elif unit == 3:
        value /= 1000
    elif unit == 4:
        value /= 2.54
        value *= 100
    elif unit == 5:
        value /= 12
        value /= 2.54
        value *= 100
    elif unit == 6:
        value /= 36
        value /= 2.54
        value *= 100
    elif unit == 7:
        value /= 1600
    return value



##############################################################
# Buttons
##############################################################

########## Render Setup ##########
# Eevee Simple Setup
class PATBLEND_OT_ESimpExecute(Operator):
    bl_label = "Setup Eevee"
    bl_idname = "wm.patblend_eevee_simp_setup"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("########## PatBlend Add-on logging start")
            print("Request recieved to setup Eevee, working.")
            
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'           # Use Eevee
        bpy.context.scene.eevee.taa_render_samples = prop.E_samp    # Render Samples to User Input
        bpy.context.scene.eevee.taa_samples = 8192                  # Viewport Samples to 8192
        bpy.context.scene.eevee.use_gtao = False                    # AO = False
        bpy.context.scene.eevee.use_bloom = False                   # Bloom = False
        bpy.context.scene.eevee.use_ssr = True                      # Screen Space Reflections = True
        bpy.context.scene.eevee.use_ssr_refraction = True           # Refraction = True
        bpy.context.scene.eevee.use_motion_blur = True              # Motion Blur = True
        bpy.context.scene.eevee.shadow_cube_size = '4096'           # Shadow Map Size to max
        bpy.context.scene.eevee.shadow_cascade_size = '4096'
        bpy.context.scene.eevee.use_shadow_high_bitdepth = True     # High Bitdepth
        bpy.context.scene.render.film_transparent = False           # Non-transparent world
        if prop.E_outSize == '0':                                   # Resolution
            bpy.context.scene.render.resolution_x = 960
            bpy.context.scene.render.resolution_y = 540
        if prop.E_outSize == '1':
            bpy.context.scene.render.resolution_x = 1280
            bpy.context.scene.render.resolution_y = 720
        if prop.E_outSize == '2':
            bpy.context.scene.render.resolution_x = 1920
            bpy.context.scene.render.resolution_y = 1080
        if prop.E_outSize == '3':
            bpy.context.scene.render.resolution_x = 3840
            bpy.context.scene.render.resolution_y = 2160
        bpy.context.scene.frame_end = prop.E_animEnd                # Animation End
        bpy.context.scene.render.fps = prop.E_fps                   # Frames per second
        bpy.context.scene.render.image_settings.compression = 70    # Image compression
        bc = prop.E_backCol                                         # World color and strength
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (bc[0], bc[1], bc[2], 1)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = prop.E_backStr
        
        if show:
            print("Done!")
            print("########## PatBlend Add-on logging end")
            print()
        
        return {'FINISHED'}

# Eevee Adv Setup
class PATBLEND_OT_EAdvExecute(Operator):
    bl_label = "Setup Eevee"
    bl_idname = "wm.patblend_eevee_adv_setup"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("########## PatBlend Add-on logging start")
            print("Request recieved to setup Eevee, working.")
        
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'           # Use Eevee
        bpy.context.scene.eevee.taa_render_samples = prop.E_samp    # Render Samples to User Input
        bpy.context.scene.eevee.taa_samples = prop.E_viewSamp       # Viewport Samples to UI
        bpy.context.scene.eevee.use_gtao = prop.E_ao                # AO = UI
        bpy.context.scene.eevee.use_bloom = prop.E_blm              # Bloom = False
        bpy.context.scene.eevee.use_ssr = prop.E_ssr                # Screen Space Reflections = True
        bpy.context.scene.eevee.use_ssr_refraction = prop.E_ssr     # Refraction = True
        bpy.context.scene.eevee.use_motion_blur = prop.E_mb         # Motion Blur = True
        bpy.context.scene.eevee.shadow_cube_size = '4096'           # Shadow Map Size to max
        bpy.context.scene.eevee.shadow_cascade_size = '4096'
        bpy.context.scene.eevee.use_shadow_high_bitdepth = True     # High Bitdepth
        bpy.context.scene.render.film_transparent = prop.E_trnsWrld # Non-transparent world
        bpy.context.scene.render.resolution_x = prop.E_custOutX     # Output size
        bpy.context.scene.render.resolution_y = prop.E_custOutY
        bpy.context.scene.frame_end = prop.E_animEnd                # Animation End
        bpy.context.scene.render.fps = prop.E_fps                   # Frames per second
        bpy.context.scene.render.image_settings.compression = 70    # Image compression
        bc = prop.E_backCol                                         # World color and strength
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (bc[0], bc[1], bc[2], 1)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = prop.E_backStr
        
        if show:
            print("Done!")
            print("########## PatBlend Add-on logging end")
            print()
        
        return {'FINISHED'}


# Workbench Setup
class PATBLEND_OT_WExecute(Operator):
    bl_label = "Setup Workbench"
    bl_idname = "wm.patblend_workbench_setup"

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("########## PatBlend Add-on logging start")
            print("Request recieved to setup Workbench, working.")
        
        bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'       # Use Workbench
        if prop.W_samp  == 0:                                        # Render Samples
            bpy.context.scene.render_aa = 'OFF'
        if prop.W_samp == 1:
            bpy.context.scene.render_aa = 'FXAA'
        if prop.W_samp == 2:
            bpy.context.scene.render_aa = '5'
        if prop.W_samp == 3:
            bpy.context.scene.render_aa = '8'
        if prop.W_samp == 4:
            bpy.context.scene.render_aa = '11'
        if prop.W_samp == 5:
            bpy.context.scene.render_aa = '16'
        if prop.W_samp == 6:
            bpy.context.scene.render_aa = '32'
        bpy.context.scene.render.film_transparent = prop.W_trnsWrld # Non-transparent world
        bpy.context.scene.render.resolution_x = prop.W_custOutX     # Output size
        bpy.context.scene.render.resolution_y = prop.W_custOutY
        bpy.context.scene.frame_end = prop.W_animEnd                # Animation End
        bpy.context.scene.render.fps = prop.W_fps                   # Frames per second
        bpy.context.scene.render.image_settings.compression = 70    # Image compression
        bc = prop.W_backCol                                         # World color and strength
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (bc[0], bc[1], bc[2], 1)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = prop.W_backStr
        
        if show:
            print("Done!")
            print("########## PatBlend Add-on logging end")
            print()
        
        return {'FINISHED'}

# Cycles Simp Setup
class PATBLEND_OT_CSimpExecute(Operator):
    bl_label = "Setup Cycles"
    bl_idname = "wm.patblend_cycles_simp_setup"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("########## PatBlend Add-on logging start")
            print("Request recieved to setup Cycles, working.")
        
        bpy.context.scene.render.engine = 'CYCLES'
        if int(prop.C_device) == 0:
            bpy.context.scene.cycles.device = 'CPU'
            bpy.context.scene.render.tile_y = 32
            bpy.context.scene.render.tile_x = 32
        elif int(prop.C_device) == 1:
            bpy.context.scene.cycles.device = 'GPU'
            bpy.context.scene.render.tile_y = 256
            bpy.context.scene.render.tile_x = 256
        bpy.context.scene.cycles.progressive = 'BRANCHED_PATH'
        bpy.context.scene.cycles.aa_samples = prop.C_samp
        bpy.context.scene.cycles.preview_aa_samples = 8192
        bpy.context.scene.cycles.transmission_samples = 2
        hBounce = math.floor(prop.C_bounces * 1.5)
        mBounce = prop.C_bounces
        lBounce = math.floor(prop.C_bounces / 1.5)
        bpy.context.scene.cycles.max_bounces = hBounce
        bpy.context.scene.cycles.diffuse_bounces = mBounce
        bpy.context.scene.cycles.glossy_bounces = mBounce
        bpy.context.scene.cycles.transparent_max_bounces = hBounce
        bpy.context.scene.cycles.transmission_bounces = hBounce
        bpy.context.scene.cycles.volume_bounces = lBounce
        bpy.context.scene.cycles.caustics_reflective = False
        bpy.context.scene.cycles.caustics_refractive = False
        bpy.context.scene.cycles_curves.use_curves = False
        bpy.context.scene.render.use_motion_blur = True
        bpy.context.scene.render.film_transparent = False
        if prop.C_outSize == '0':                                   # Resolution
            bpy.context.scene.render.resolution_x = 960
            bpy.context.scene.render.resolution_y = 540
        if prop.C_outSize == '1':
            bpy.context.scene.render.resolution_x = 1280
            bpy.context.scene.render.resolution_y = 720
        if prop.C_outSize == '2':
            bpy.context.scene.render.resolution_x = 1920
            bpy.context.scene.render.resolution_y = 1080
        if prop.C_outSize == '3':
            bpy.context.scene.render.resolution_x = 3840
            bpy.context.scene.render.resolution_y = 2160
        bpy.context.scene.frame_end = prop.C_animEnd
        bpy.context.scene.render.fps = 30
        bpy.context.scene.render.image_settings.compression = 70
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
        
        if show:
            print("Done!")
            print("########## PatBlend Add-on logging end")
            print()
        
        return {'FINISHED'}
        
# Cycles Adv Setup
class PATBLEND_OT_CAdvExecute(Operator):
    bl_label = "Setup Cycles"
    bl_idname = "wm.patblend_cycles_adv_setup"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("########## PatBlend Add-on logging start")
            print("Request recieved to setup Cycles, working.")
        
        bpy.context.scene.render.engine = 'CYCLES'                     # Use Cycles
        if prop.C_device == '0':                                         # GPU or CPU
            bpy.context.scene.cycles.device = 'CPU'
            bpy.context.scene.render.tile_y = 32
            bpy.context.scene.render.tile_x = 32
        elif prop.C_device == '1':
            bpy.context.scene.cycles.device = 'GPU'
            bpy.context.scene.render.tile_y = 256
            bpy.context.scene.render.tile_x = 256
        if prop.C_sampType == '1':                                       # Branched
            bpy.context.scene.cycles.progressive = 'BRANCHED_PATH'
            bpy.context.scene.cycles.aa_samples = prop.C_samp
            bpy.context.scene.cycles.preview_aa_samples = prop.C_viewSamp
            bpy.context.scene.cycles.transmission_samples = 2
        elif prop.C_sampType == '0':
            bpy.context.scene.cycles.progressive = 'PATH'
            bpy.context.scene.cycles.samples = prop.C_samp
            bpy.context.scene.cycles.preview_samples = prop.C_viewSamp
        hBounce = math.floor(prop.C_bounces * 1.5)                          # Light Bounces
        mBounce = prop.C_bounces
        lBounce = math.floor(prop.C_bounces / 1.5)
        bpy.context.scene.cycles.max_bounces = hBounce
        bpy.context.scene.cycles.diffuse_bounces = mBounce
        bpy.context.scene.cycles.glossy_bounces = mBounce
        bpy.context.scene.cycles.transparent_max_bounces = hBounce
        bpy.context.scene.cycles.transmission_bounces = hBounce
        bpy.context.scene.cycles.volume_bounces = lBounce
        bpy.context.scene.cycles.caustics_reflective = prop.C_caustics       # Caustics
        bpy.context.scene.cycles.caustics_refractive = prop.C_caustics
        bpy.context.scene.cycles_curves.use_curves = False                      # Hair
        bpy.context.scene.render.use_motion_blur = prop.C_mb                       # Motion Blur
        bpy.context.scene.render.film_transparent = prop.C_trnsWrld
        bpy.context.scene.render.resolution_x = prop.C_custOutX           # Output size
        bpy.context.scene.render.resolution_y = prop.C_custOutY
        bpy.context.scene.frame_end = prop.C_animEnd
        bpy.context.scene.render.fps = prop.C_fps                                       # Fps
        bpy.context.scene.render.image_settings.compression = 70                         # Compression
        bc = prop.C_backCol
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (bc[0], bc[1], bc[2], 1)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = prop.C_backStr
        
        if show:
            print("Done!")
            print("########## PatBlend Add-on logging end")
            print()
        
        return {'FINISHED'}
        

########## Search ##########
class PATBLEND_OT_SearchExecute(Operator):
    bl_label = "Search"
    bl_idname = "wm.patblend_search"

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        url = prop.search_url
        show = prop.console
        
        if show:
            print()
            print("########## PatBlend Add-on logging start")
            print("Request recieved to search, working.")
        
        if url == "":
            return {'FINISHED'}
        if url[0] == "h" and url[1] == "t" and url[2] == "t" and url[3] == "p" and url[4] == "s" and url[5] == ":" and url[6] == "/" and url[7] == "/":
            blah = True
        else:
            blah = False
        if blah:
            bpy.ops.wm.url_open(url=url)
        else:
            realUrl = "https://www.google.com/search?q=" + url
            bpy.ops.wm.url_open(url=realUrl)
        
        if show:
            print("Done!")
            print("########## PatBlend Add-on logging end")
            print()
        
        return {'FINISHED'}
    
    
########## Settings ##########
class PATBLEND_OT_AddonUpdate(Operator):
    bl_label = "Download latest version"
    bl_idname = "wm.patblend_download_addon"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("########## PatBlend Add-on logging start")
            print("Request recieved to download latest version of add-on, working.")
        
        bpy.ops.wm.url_open(url="https://drive.google.com/open?id=1EQd16cotHF_j7FOSmEMaYHfoJJgCYE9l")
        
        if show:
            print("Done!")
            print("########## PatBlend Add-on logging end")
            print()
        
        return {'FINISHED'}
    
class PATBLEND_OT_Uninstall_Prompt(Operator):
    bl_label = "Uninstall this add-on"
    bl_idname = "wm.patblend_uninstall_prompt"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        
        bpy.ops.wm.patblend_uninstall_warning('INVOKE_DEFAULT')

class PATBLEND_OT_Uninstall_Warning(bpy.types.Operator):
    bl_label = "Are you sure?"
    bl_idname = "wm.patblend_uninstall_warning"
    
    def execute(self, context):
        bpy.ops.wm.patblend_uninstall()
        
class PATBLEND_OT_Uninstall(bpy.types.Operator):
    bl_idname = "wm.patblend_uninstall"
    bl_label = "Uninstalling"
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        bpy.ops.preferences.addon_remove(module = "PatBlend_Add-on_v1-0-1")


##############################################################
# Panels
##############################################################

########## Main PatBlend Panel ##########
class Panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PatBlend"
    bl_options = {"DEFAULT_CLOSED"}
    
########## Add-on Options Panel ##########
class PATBLEND_PT_OptionsPanel(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_OptionsPanel"
    bl_label = "Add-on Settings"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        layout.prop(prop, "console")
        #layout.prop(prop, "enabled")
        layout.operator("wm.patblend_download_addon")
        layout.operator("wm.patblend_uninstall_prompt")

########## Render Setup Panels ##########
class PATBLEND_PT_RenderMainPanel(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Render Setup"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Setup the render engines.")
        
class PATBLEND_PT_RenderEeveeSimpPanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Eevee Simple"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        layout.prop(prop, "E_samp")
        layout.separator()
        layout.prop(prop, "E_outSize")
        layout.prop(prop, "E_animEnd")
        layout.prop(prop, "E_fps")
        layout.separator()
        layout.prop(prop, "E_backCol")
        layout.prop(prop, "E_backStr")
        layout.operator("wm.patblend_eevee_simp_setup")
        layout.separator()
        
class PATBLEND_PT_RenderEeveeAdvPanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Eevee Advanced"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        layout.prop(prop, "E_samp")
        layout.prop(prop, "E_viewSamp")
        layout.prop(prop, "E_ao")
        layout.prop(prop, "E_blm")
        layout.prop(prop, "E_ssr")
        layout.prop(prop, "E_mb")
        layout.prop(prop, "E_trnsWrld")
        layout.separator()
        layout.prop(prop, "E_custOutX")
        layout.prop(prop, "E_custOutY")
        layout.prop(prop, "E_animEnd")
        layout.prop(prop, "E_fps")
        layout.separator()
        layout.prop(prop, "E_backCol")
        layout.prop(prop, "E_backStr")
        layout.operator("wm.patblend_eevee_adv_setup")
        layout.separator()
        
class PATBLEND_PT_RenderWorkbenchPanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Workbench"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        layout.prop(prop, "W_samp")
        layout.prop(prop, "W_trnsWrld")
        layout.separator()
        layout.prop(prop, "W_custOutX")
        layout.prop(prop, "W_custOutY")
        layout.prop(prop, "W_animEnd")
        layout.prop(prop, "W_fps")
        layout.separator()
        layout.prop(prop, "W_backCol")
        layout.prop(prop, "W_backStr")
        layout.operator("wm.patblend_workbench_setup")
        layout.separator()
        
class PATBLEND_PT_RenderCyclesSimpPanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Cycles Simple"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        layout.prop(prop, "C_device")
        layout.prop(prop, "C_samp")
        layout.prop(prop, "C_bounces")
        layout.separator()
        layout.prop(prop, "C_outSize")
        layout.prop(prop, "C_animEnd")
        layout.operator("wm.patblend_cycles_simp_setup")
        layout.separator()
        
class PATBLEND_PT_RenderCyclesAdvPanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Cycles Advanced"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        layout.prop(prop, "C_device")
        layout.prop(prop, "C_sampType")
        layout.prop(prop, "C_samp")
        layout.prop(prop, "C_viewSamp")
        layout.prop(prop, "C_bounces")
        layout.prop(prop, "C_caustics")
        layout.prop(prop, "C_mb")
        layout.prop(prop, "C_trnsWrld")
        layout.separator()
        layout.prop(prop, "C_custOutX")
        layout.prop(prop, "C_custOutY")
        layout.prop(prop, "C_animEnd")
        layout.prop(prop, "C_fps")
        layout.separator()
        layout.prop(prop, "C_backCol")
        layout.prop(prop, "C_backStr")
        layout.operator("wm.patblend_cycles_adv_setup")
        layout.separator()
        

########## Search Panels ##########
class PATBLEND_PT_SearchMainPanel(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_SearchMainPanel"
    bl_label = "Search"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        layout.prop(prop, "search_url")
        layout.operator("wm.patblend_search")
        layout.separator()
        
        
########## Unit Converter Panels ##########
class PATBLEND_PT_UnitMainPanel(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_UnitMainPanel"
    bl_label = "Unit Converter"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Convert between different units.")
        scene = context.scene
        prop = scene.patblend
        
        layout.prop(prop, "inputType")
        layout.prop(prop, "outputType")
        layout.prop(prop, "input")
        layout.prop(prop, "precision")
        
        type1 = prop.inputType
        type2 = prop.outputType
        value = prop.input
        prec = prop.precision
        
        input = prop.input
        inputMeters = ToMeter(type1, value)
        output = FromMeter(type2, inputMeters)
        
        inputType = GetUnitName(type1)
        outputType = GetUnitName(type2)
        
        if input == 1:
            text1 = str(round(input, prec)) + "  " + inputType
        else:
            text1 = str(round(input, prec)) + "  " + inputType + "s"
        
        if output == 1:
            text2 = str(round(output, prec)) + "  " + outputType
        else:
            text2 = str(round(output, prec)) + "  " + outputType + "s"
        layout.label(text = text1)
        layout.label(text = "Equals")
        layout.label(text = text2)
        layout.separator()
        
        
        
##############################################################
# Register/Unregister
##############################################################


classes = (PatBlendAddonProperties,
               PATBLEND_OT_ESimpExecute,
               PATBLEND_OT_EAdvExecute,
               PATBLEND_OT_WExecute,
               PATBLEND_OT_CSimpExecute,
               PATBLEND_OT_CAdvExecute,
               PATBLEND_OT_AddonUpdate,
               PATBLEND_OT_Uninstall_Prompt,
               PATBLEND_OT_Uninstall_Warning,
               PATBLEND_OT_Uninstall,
               
               PATBLEND_PT_OptionsPanel,
               
               PATBLEND_PT_RenderMainPanel,
               PATBLEND_PT_RenderEeveeSimpPanel,
               PATBLEND_PT_RenderEeveeAdvPanel,
               PATBLEND_PT_RenderWorkbenchPanel,
               PATBLEND_PT_RenderCyclesSimpPanel,
               PATBLEND_PT_RenderCyclesAdvPanel,
               
               PATBLEND_OT_SearchExecute,
               PATBLEND_PT_SearchMainPanel,
               
               PATBLEND_PT_UnitMainPanel)
           
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.patblend = PointerProperty(type = PatBlendAddonProperties)
    
def unregister():
    for i in range(10):
        print()
    print("Thanks for using PatBlend Add-ons!")
    print("If you haven't already, you can sign up for a PatBlend account to gain access to a whole library of premium 3D assets.")
    print("To do that, click the \"Report a Bug\" button in the Add-ons section of preferences.")
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.patblend
    
if __name__ == "__main__":
    register()