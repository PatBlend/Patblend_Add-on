########## Metadata ##########
bl_info = {
    "name":        "PatBlend Add-on 1.0.1",
    "description": "A compilation of all Add-ons made by PatBlend",
    "author":      "Patrick Huang, PatBlend <https://sites.google.com/view/patblend>",
    "version":     (1, 0, 1),
    "blender":     (2, 80, 0),
    "location":    "3D View >> Sidebar >> PatBlend",
    "warning":     "",
    "wiki_url":    "https://drive.google.com/drive/folders/1EQd16cotHF_j7FOSmEMaYHfoJJgCYE9l",
    "tracker_url": "https://sites.google.com/view/patblend",
    "category":    "PatBlend"}
    

########## Library Import ##########
import bpy, math, time
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
            ('2', "1080×1920px", "Standard HD"), 
            ('1', "720×1280px", "HD"), 
            ('0', "540×960px", "Low Resolution"), 
            ('3', "2160×3840px", "High Resolution"),])
            
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
            ('0', "No Anti-Aliasing", "Bare Image"), 
            ('1', "Anti-Aliasing", "Makes edges smoother"), 
            ('2', "5 Samples", "5 Samples"), 
            ('3', "8 Samples", "8 Samples"),
            ('4', "11 Samples", "11 Samples"),
            ('5', "16 Samples", "16 Samples"),
            ('6', "32 Samples", "32 Samples"),])
            
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
            ('1', "GPU Compute", "Uses GPU, tends to be faster"), 
            ('0', "CPU", "Uses CPU, tends to be slower"),])
            
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
            ('2', "1080×1920px", "Standard HD"), 
            ('1', "720×1280px", "HD"), 
            ('0', "540×960px", "Low Resolution"), 
            ('3', "2160×3840px", "High Resolution"),])
            
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
        name="",
        description="Enter anything. To search a hyperlink, start with \"https://\"",
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

    openGit: BoolProperty(
        name = "Open GitHub after uninstalling",
        description = "Blender opens GitHub when uninstalling to download the latest version.",
        default = True)
        
    time_convert_type: EnumProperty(
        name = "Conversion Type",
        description = "Type of action that the computer performs",
        items = [
            ('0', "Seconds to Standard", "From a float number to hh:mm:ss.ss"),
            ('1', "Standard to Seconds", "From hh:mm:ss.ss to a float number")])

    time_num_time: FloatProperty(
        name = "Seconds",
        description = "Number of seconds to convert",
        default = 125, min = 0)

    time_str_time: StringProperty(
        name = "Time",
        description = "Enter time exactly in the fomat hh:mm:ss.ss")

    time_mult: FloatProperty(
        name = "Multiplier",
        description = "Amount to be multiplied with the input time in seconds.",
        default = 1, min = 0)

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
            print("------------------- PatBlend Logging Start -------------------")
            print("Setting up Eevee...")
            
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
            print("Eevee has been successfully setup.")
            print("------------------- PatBlend Logging End -------------------")
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
            print("------------------- PatBlend Logging Start -------------------")
            print("Setting up Eevee...")
        
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
            print("Eevee has been successfully setup.")
            print("------------------- PatBlend Logging End -------------------")
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
            print("------------------- PatBlend Logging Start -------------------")
            print("Setting up Workbench...")
        
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
            print("Workbench has been successfully setup.")
            print("------------------- PatBlend Logging End -------------------")
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
            print("------------------- PatBlend Logging Start -------------------")
            print("Setting up Cycles...")
        
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
            print("Cycles has been successfully setup.")
            print("------------------- PatBlend Logging End -------------------")
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
            print("------------------- PatBlend Logging Start -------------------")
            print("Setting up Cycles...")
        
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
            print("Cycles has been successfully setup.")
            print("------------------- PatBlend Logging End -------------------")
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
            print("------------------- PatBlend Logging Start -------------------")
            print("Searching...")
        
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
            print("Successfully searched.")
            print("------------------- PatBlend Logging End -------------------")
            print()
        
        return {'FINISHED'}
    
    
########## Settings ##########
class PATBLEND_OT_GitHub(Operator):
    bl_label = "GitHub"
    bl_idname = "wm.patblend_github"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("------------------- PatBlend Logging Start -------------------")
            print("Redirecting to https://github.com/PatBlend/Patblend_Add-on")
        
        bpy.ops.wm.url_open(url="https://github.com/PatBlend/Patblend_Add-on")
        
        if show:
            print("Redirection Successful")
            print("------------------- PatBlend Logging End -------------------")
            print()
        
        return {'FINISHED'}

class PATBLEND_OT_PatBlendSite(Operator):
    bl_label = "Website"
    bl_idname = "wm.patblend_site"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("------------------- PatBlend Logging Start -------------------")
            print("Redirecting to https://sites.google.com/view/patblend")
        
        bpy.ops.wm.url_open(url="https://sites.google.com/view/patblend")
        
        if show:
            print("Redirection Successful")
            print("------------------- PatBlend Logging End -------------------")
            print()
        
        return {'FINISHED'}

class PATBLEND_OT_PatBlendDownload(Operator):
    bl_label = "Download Latest Version"
    bl_idname = "wm.patblend_download"

    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console
        
        if show:
            print()
            print("------------------- PatBlend Logging Start -------------------")
            print("Redirecting to https://github.com/PatBlend/Patblend_Add-on/archive/master.zip")

        bpy.ops.wm.patblend_download_ask('INVOKE_DEFAULT')

        if show:
            print("Redirection Successful")
            print("------------------- PatBlend Logging End -------------------")
            print()

        return {'FINISHED'}

class PATBLEND_OT_DownloadAsk(bpy.types.Operator):
    bl_label = "Confirmation"
    bl_idname = "wm.patblend_download_ask"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1

    def execute(self, context):
        bpy.ops.wm.url_open(url="https://github.com/PatBlend/Patblend_Add-on")
        bpy.ops.wm.url_open(url="https://github.com/PatBlend/Patblend_Add-on/archive/master.zip")
        
        return {'FINISHED'}
    

########## Uninstallation ##########
# Prompt
class PATBLEND_OT_Uninstall_Prompt(Operator):
    bl_label = "Uninstall"
    bl_idname = "wm.patblend_uninstall_prompt"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console

        if show:
            print()
            print("------------------- PatBlend Logging Start -------------------")
            print("Uninstalling...")
            print("------------------- PatBlend Logging End -------------------")
            print()

        bpy.ops.wm.patblend_uninstall_warning('INVOKE_DEFAULT')
        return {'FINISHED'}

# Warning 1
class PATBLEND_OT_Uninstall_Warning(bpy.types.Operator):
    bl_label = "Are you sure?"
    bl_idname = "wm.patblend_uninstall_warning"
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1
        col.label(text = "The add-on will be gone until you install it again.")
        col.label(text = "Note: Blender may crash when uninstalling.")
    
    def execute(self, context):
        bpy.ops.wm.patblend_uninstall_warning_2('INVOKE_DEFAULT')
        return {'FINISHED'}
    
# Warning 2 and Uninstall
class PATBLEND_OT_Uninstall_Warning_2(bpy.types.Operator):
    bl_label = "Are you very sure?"
    bl_idname = "wm.patblend_uninstall_warning_2"
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1
        col.label(text = "This action cannot be undone.")
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        open = prop.openGit
        
        if open:
            bpy.ops.wm.url_open(url="https://github.com/PatBlend/Patblend_Add-on")
        time.sleep(0.1)
        bpy.ops.preferences.addon_disable(module = "PatBlend_Add-on")
        time.sleep(0.1)
        bpy.ops.preferences.addon_remove(module = "PatBlend_Add-on")
        time.sleep(0.1)
        return {'FINISHED'}



########## Disable ##########
class PATBLEND_OT_DisablePrompt(bpy.types.Operator):
    bl_label = "Disable"
    bl_idname = "wm.patblend_disable_prompt"
    
    def execute(self, context):
        scene = context.scene
        prop = scene.patblend
        show = prop.console

        if show:
            print()
            print("------------------- PatBlend Logging Start -------------------")
            print("Disabling...")
            print("------------------- PatBlend Logging End -------------------")
            print()
        
        bpy.ops.wm.patblend_disable_warning('INVOKE_DEFAULT')
        return {'FINISHED'}
    
class PATBLEND_OT_Disable(bpy.types.Operator):
    bl_label = "Are you sure?"
    bl_idname = "wm.patblend_disable_warning"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1
        col.label(text = "The add-on will be disabled until you enable it again.")
        col.label(text = "You can find it in preferences by searching \"PatBlend\".")

    def execute(self, context):
        bpy.ops.preferences.addon_disable(module = "PatBlend_Add-on")
        return {'FINISHED'}


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
class PATBLEND_PT_PatBlendOptionsPanel(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_PatBlendOptionsPanel"
    bl_label = "Add-on Settings"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend

class PATBLEND_PT_PatBlendQuickOptions(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_PatBlendOptionsPanel"
    bl_label = "Quick Settings"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend

        layout.prop(prop, "console")
        layout.prop(prop, "openGit")
        row = layout.row(align = True)
        row.scale_y = 10
        row.operator("wm.patblend_disable_prompt")
        row.operator("wm.patblend_uninstall_prompt")

class PATBLEND_PT_PatBlendLinks(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_PatBlendOptionsPanel"
    bl_label = "PatBlend Links"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend

        row = layout.row()
        row.scale_y = 1.2
        row.operator("wm.patblend_github")
        row.operator("wm.patblend_site")
        row = layout.row()
        row.scale_y = 4
        row.operator("wm.patblend_download")

########## Render Setup Panels ##########
class PATBLEND_PT_RenderMainPanel(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Render Setup"
    
    def draw(self, context):
        layout = self.layout
        
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
        row = layout.row(align = True)
        row.prop(prop, "E_backCol")
        row.prop(prop, "E_backStr")
        row = layout.row()
        row.scale_y = 1.5
        row.operator("wm.patblend_eevee_simp_setup")
        layout.separator()
        
class PATBLEND_PT_RenderEeveeAdvPanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Eevee Advanced"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        row = layout.row(align = True)
        row.prop(prop, "E_samp")
        row.prop(prop, "E_viewSamp")
        layout.prop(prop, "E_ao")
        layout.prop(prop, "E_blm")
        layout.prop(prop, "E_ssr")
        layout.prop(prop, "E_mb")
        layout.prop(prop, "E_trnsWrld")
        layout.separator()
        row = layout.row(align = True)
        row.prop(prop, "E_custOutX")
        row.prop(prop, "E_custOutY")
        layout.prop(prop, "E_animEnd")
        layout.prop(prop, "E_fps")
        layout.separator()
        row = layout.row(align = True)
        row.prop(prop, "E_backCol")
        row.prop(prop, "E_backStr")
        row = layout.row()
        row.scale_y = 1.5
        row.operator("wm.patblend_eevee_adv_setup")
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
        row = layout.row(align = True)
        row.prop(prop, "W_custOutX")
        row.prop(prop, "W_custOutY")
        layout.prop(prop, "W_animEnd")
        layout.prop(prop, "W_fps")
        layout.separator()
        row = layout.row(align = True)
        row.prop(prop, "W_backCol")
        row.prop(prop, "W_backStr")
        row = layout.row()
        row.scale_y = 1.5
        row.operator("wm.patblend_workbench_setup")
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
        layout.prop(prop, "C_fps")
        row = layout.row()
        row.scale_y = 1.5
        row.operator("wm.patblend_cycles_simp_setup")
        layout.separator()
        
class PATBLEND_PT_RenderCyclesAdvPanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_RenderMainPanel"
    bl_label = "Cycles Advanced"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
        layout.prop(prop, "C_device")
        row = layout.row(align = True)
        layout.prop(prop, "C_sampType")
        row.prop(prop, "C_samp")
        row.prop(prop, "C_viewSamp")
        layout.prop(prop, "C_bounces")
        layout.prop(prop, "C_caustics")
        layout.prop(prop, "C_mb")
        layout.prop(prop, "C_trnsWrld")
        layout.separator()
        row = layout.row(align = True)
        row.prop(prop, "C_custOutX")
        row.prop(prop, "C_custOutY")
        layout.prop(prop, "C_animEnd")
        layout.prop(prop, "C_fps")
        layout.separator()
        row = layout.row(align = True)
        row.prop(prop, "C_backCol")
        row.prop(prop, "C_backStr")
        row = layout.row()
        row.scale_y = 1.5
        row.operator("wm.patblend_cycles_adv_setup")
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
        row = layout.row()
        row.scale_y = 2
        row.operator("wm.patblend_search")
        layout.separator()
        
        
########## Unit Converter Panels ##########
class PATBLEND_PT_UnitMainPanel(Panel, bpy.types.Panel):
    bl_idname = "PATBLEND_PT_UnitMainPanel"
    bl_label = "Unit Converter"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend

class PATBLEND_PT_UnitLengthPanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_UnitMainPanel"
    bl_label = "Units of Length"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend
        
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

        row = layout.row(align = True)
        row.prop(prop, "inputType")
        row.prop(prop, "outputType")
        row = layout.row(align=True)
        row.prop(prop, "input")
        row.prop(prop, "precision")
        
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
        
class PATBLEND_PT_UnitTimePanel(Panel, bpy.types.Panel):
    bl_parent_id = "PATBLEND_PT_UnitMainPanel"
    bl_label = "Units of Time"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.patblend

        layout.prop(prop, "time_convert_type")
        
        if prop.time_convert_type == '0':
            row = layout.row(align = True)
            row.prop(prop, "time_num_time")
            row.prop(prop, "time_mult")
            sec = prop.time_num_time * prop.time_mult

            hour = math.floor(sec / 3600)        # Find Hours
            sec -= hour * 3600                   # Subtract from seconds

            min = math.floor(sec / 60)           # Find minutes
            sec -= min * 60                      # Subtract from minutes

            if hour <= 9:                        # Grammar Issues
                hour = "0" + str(hour)
            else:
                hour = str(hour)
            if min <= 9:
                min = "0" + str(min)
            else:
                min = str(min)
            if sec <= 9:
                sec = "0" + str(round(sec, 2))
            else:
                sec = str(round(sec, 2))

            if prop.time_num_time == 1:          # Text 1: 56 seconds is
                text1 = str(round(prop.time_num_time, 2)) + " second is"
            else:                                
                text1 = str(round(prop.time_num_time, 2)) + " seconds is"

            text2 = hour + " : " + min + " : " + sec      # Text 2 : 46 : 24 : 75.25

            layout.label(text = text1)
            layout.label(text = text2)

        elif prop.time_convert_type == '1':
            time = prop.time_str_time
            nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            '00:00:00.00'
            layout.label(text = "Note: Time must be in")
            layout.label(text = "the form hh:mm:ss.ss.")
            layout.separator()
            layout.label(text = "This will be improved")
            layout.label(text = "in the future.")
            layout.separator()
            layout.prop(prop, "time_str_time")
            time = prop.time_str_time
            if len(time) == 11:
                if time[0] in nums and time[1] in nums and time[3] in nums and time[4] in nums and time[6] in nums and time[7] in nums and time[9] in nums and time[10] in nums and time[2] == ":" and time[5] == ":" and time[8] == ".":
                    hour = int(time[0] + time[1])
                    min = int(time[3] + time[4])
                    sec = float(time[6] + time[7] + "." + time[9] + time[10])
                    totalSec = 3600 * hour + 60 * min + sec
                    text = str(totalSec) + " Seconds."
                    layout.label(text = text)
                else:
                    layout.label(text = "Invalid Time")
            else:
                layout.label(text = "Invalid Time")
            
        
        
##############################################################
# Register/Unregister
##############################################################


classes = (PatBlendAddonProperties,
           PATBLEND_OT_ESimpExecute,
           PATBLEND_OT_EAdvExecute,
           PATBLEND_OT_WExecute,
           PATBLEND_OT_CSimpExecute,
           PATBLEND_OT_CAdvExecute,
           PATBLEND_OT_GitHub,
           PATBLEND_OT_PatBlendSite,
           PATBLEND_OT_PatBlendDownload,
           PATBLEND_OT_DownloadAsk,
           PATBLEND_OT_Uninstall_Prompt,
           PATBLEND_OT_Uninstall_Warning,
           PATBLEND_OT_Uninstall_Warning_2,

           PATBLEND_OT_DisablePrompt,
           PATBLEND_OT_Disable,
           
           PATBLEND_PT_PatBlendOptionsPanel,
           PATBLEND_PT_PatBlendQuickOptions,
           PATBLEND_PT_PatBlendLinks,
           
           PATBLEND_PT_RenderMainPanel,
           PATBLEND_PT_RenderEeveeSimpPanel,
           PATBLEND_PT_RenderEeveeAdvPanel,
           PATBLEND_PT_RenderWorkbenchPanel,
           PATBLEND_PT_RenderCyclesSimpPanel,
           PATBLEND_PT_RenderCyclesAdvPanel,
           
           PATBLEND_OT_SearchExecute,
           PATBLEND_PT_SearchMainPanel,
           
           PATBLEND_PT_UnitMainPanel,
           PATBLEND_PT_UnitLengthPanel,
           PATBLEND_PT_UnitTimePanel)
           

custIcons = None
def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.patblend = PointerProperty(type = PatBlendAddonProperties)
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.patblend
    
if __name__ == "__main__":
    register()