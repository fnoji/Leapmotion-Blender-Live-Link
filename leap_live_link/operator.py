import bpy
import socket
import json
import math
import mathutils

# Global socket variable to manage connection
sock = None

class LEAP_OT_CreateDebugHand(bpy.types.Operator):
    bl_idname = "leap.create_debug_hand"
    bl_label = "Create Debug Hand"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Create Armature
        if "Leap_Debug_Rig" in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects["Leap_Debug_Rig"], do_unlink=True)
            
        bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
        arm_obj = context.active_object
        arm_obj.name = "Leap_Debug_Rig"
        arm_data = arm_obj.data
        arm_data.name = "Leap_Debug_Rig_Data"
        
        # Remove default bone
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.armature.delete()
        
        edit_bones = arm_data.edit_bones
        
        # Define structure for both hands
        sides = [("Left", "L", -0.3), ("Right", "R", 0.3)]
        
        fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        bone_types = ["Metacarpal", "Proximal", "Intermediate", "Distal"]
        
        for side_name, prefix, x_offset in sides:
            # Wrist
            wrist_name = f"{prefix}_Wrist"
            wrist = edit_bones.new(wrist_name)
            wrist.head = (x_offset, 0, 0)
            wrist.tail = (x_offset, 0.05, 0) # Pointing +Y
            
            # Finger Offsets (Relative to Wrist)
            # Spread fingers out in X
            f_x_offsets = {"Thumb": -0.04, "Index": -0.02, "Middle": 0, "Ring": 0.02, "Pinky": 0.04}
            
            for f_name in fingers:
                parent = wrist
                
                # Calculate base position for finger chain
                fx = x_offset + f_x_offsets[f_name]
                fy = 0.05 # Start at end of wrist
                
                for b_type in bone_types:
                    b_name = f"{prefix}_{f_name}_{b_type}"
                    bone = edit_bones.new(b_name)
                    bone.parent = parent
                    bone.use_connect = True # Connect bones for visual hand shape
                    
                    length = 0.03
                    if f_name == "Thumb":
                        length = 0.025
                    
                    bone.head = (fx, fy, 0)
                    bone.tail = (fx, fy + length, 0)
                    
                    fy += length
                    parent = bone
                
        bpy.ops.object.mode_set(mode='OBJECT')
        context.scene.leap_target_rig = arm_obj
        
        # Ensure the object is at 0,0,0 and no rotation for direct mapping
        arm_obj.location = (0,0,0)
        arm_obj.rotation_euler = (0,0,0)
        
        return {'FINISHED'}

class LEAP_OT_StartReceiver(bpy.types.Operator):
    bl_idname = "leap.start_receiver"
    bl_label = "Start Receiver"
    
    _timer = None
    _sock = None
    
    def modal(self, context, event):
        if not context.window_manager.leap_listening:
            self.stop(context)
            return {'CANCELLED'}
            
        if event.type == 'TIMER':
            self.receive_data(context)
            
        return {'PASS_THROUGH'}

    def receive_data(self, context):
        try:
            # Non-blocking receive
            while True:
                try:
                    data, addr = self._sock.recvfrom(65535)
                    json_data = json.loads(data.decode('utf-8'))
                    self.apply_pose(context, json_data)
                except BlockingIOError:
                    break
                except socket.error:
                    break
        except Exception as e:
            print(f"Error receiving: {e}")

    def apply_pose(self, context, data):
        rig = context.scene.leap_target_rig
        if not rig:
            return
            
        hands = data.get("hands", [])
        
        # Coordinate Conversion Matrix
        to_blender_mat = mathutils.Matrix((
            (1, 0, 0),
            (0, 0, -1),
            (0, 1, 0)
        ))
        
        scale = 0.001

        def convert_position(pos_list):
            p = mathutils.Vector(pos_list) * scale
            return to_blender_mat @ p

        def convert_rotation(rot_list):
            q = mathutils.Quaternion(rot_list)
            rot_mat = q.to_matrix().to_3x3()
            return to_blender_mat @ rot_mat @ to_blender_mat.transposed()

        # Process all hands
        for hand in hands:
            h_type = hand["type"] # "Left" or "Right"
            prefix = "L" if h_type == "Left" else "R"
            
            # Wrist (Root) - Use Rotation for this one as it has no single "next"
            wrist_name = f"{prefix}_Wrist"
            if wrist_name in rig.pose.bones:
                pb = rig.pose.bones[wrist_name]
                
                w_p = convert_position(hand["palm_position"])
                w_r_mat = convert_rotation(hand["palm_rotation"])
                # Apply a correction for the Wrist bone if needed.
                # Leap Z (Bone Dir) -> Blender Y (Bone Dir).
                # Rotate -90 degrees around X axis maps Y -> Z.
                axis_correction = mathutils.Matrix.Rotation(math.radians(-90), 3, 'X')
                w_r_mat = w_r_mat @ axis_correction
                
                pb.matrix = w_r_mat.to_4x4()
                pb.matrix.translation = w_p

            # Fingers
            fingers = hand.get("fingers", {})
            for f_name, bones in fingers.items():
                for b_type, b_data in bones.items():
                    bone_name = f"{prefix}_{f_name}_{b_type}"
                    if bone_name in rig.pose.bones:
                        pb = rig.pose.bones[bone_name]
                        
                        # Vector Alignment with Roll Preservation
                        # 1. Get Direction (Y-axis) from positions
                        if "next_joint" in b_data:
                            p_start = convert_position(b_data["position"])
                            p_end = convert_position(b_data["next_joint"])
                            direction = p_end - p_start
                            
                            if direction.length > 0.0001:
                                # Simplified Vector Alignment
                                direction.normalize()
                                
                                # Align Bone Y to Direction. 
                                # Use Z as Up vector hint (Leap Y is Up, which maps to Blender Z).
                                rot_quat = direction.to_track_quat('Y', 'Z')
                                
                                mat = rot_quat.to_matrix().to_4x4()
                                mat.translation = p_start
                                pb.matrix = mat
                        else:
                            # Fallback
                            r_mat = convert_rotation(b_data["rotation"])
                            axis_correction = mathutils.Matrix.Rotation(math.radians(-90), 3, 'X')
                            r_mat = r_mat @ axis_correction
                            pb.matrix = r_mat.to_4x4()




    def execute(self, context):
        port = context.scene.leap_port
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setblocking(False)
        try:
            self._sock.bind(("127.0.0.1", port))
        except OSError as e:
            self.report({'ERROR'}, f"Could not bind port {port}: {e}")
            return {'CANCELLED'}
            
        context.window_manager.leap_listening = True
        self._timer = context.window_manager.event_timer_add(0.016, window=context.window)
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}

    def stop(self, context):
        if self._sock:
            self._sock.close()
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        context.window_manager.leap_listening = False

class LEAP_OT_StopReceiver(bpy.types.Operator):
    bl_idname = "leap.stop_receiver"
    bl_label = "Stop Receiver"

    def execute(self, context):
        context.window_manager.leap_listening = False
        return {'FINISHED'}

def register():
    bpy.utils.register_class(LEAP_OT_CreateDebugHand)
    bpy.utils.register_class(LEAP_OT_StartReceiver)
    bpy.utils.register_class(LEAP_OT_StopReceiver)

def unregister():
    bpy.utils.unregister_class(LEAP_OT_CreateDebugHand)
    bpy.utils.unregister_class(LEAP_OT_StartReceiver)
    bpy.utils.unregister_class(LEAP_OT_StopReceiver)
