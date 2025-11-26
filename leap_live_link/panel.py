import bpy

class LEAP_PT_Panel(bpy.types.Panel):
    bl_label = "Leap Motion Link"
    bl_idname = "LEAP_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Leap Link"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "leap_port")
        layout.prop(scene, "leap_target_rig")
        
        if context.window_manager.leap_listening:
            layout.operator("leap.stop_receiver", text="Stop Receiver", icon='PAUSE')
        else:
            layout.operator("leap.start_receiver", text="Start Receiver", icon='PLAY')

        layout.separator()
        layout.label(text="Debug Tools")
        layout.operator("leap.create_debug_hand", text="Generate Debug Hand", icon='HAND')

def register():
    bpy.types.Scene.leap_port = bpy.props.IntProperty(name="Port", default=9009)
    bpy.types.Scene.leap_target_rig = bpy.props.PointerProperty(name="Target Rig", type=bpy.types.Object)
    bpy.types.WindowManager.leap_listening = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(LEAP_PT_Panel)

def unregister():
    bpy.utils.unregister_class(LEAP_PT_Panel)
    del bpy.types.Scene.leap_port
    del bpy.types.Scene.leap_target_rig
    del bpy.types.WindowManager.leap_listening
