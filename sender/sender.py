import leap
import sys
import time
import json
import socket
import math

# Configuration
IP = "127.0.0.1"
PORT = 9009

def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return sock

def format_bone(bone):
    # Leap Motion Quaternion is (x, y, z, w) - Wait, usually it's (w, x, y, z) in API, but let's check.
    # The bindings might expose it differently. 
    # Let's assume standard quaternion for now.
    
    # Calculate length from joints
    dx = bone.next_joint.x - bone.prev_joint.x
    dy = bone.next_joint.y - bone.prev_joint.y
    dz = bone.next_joint.z - bone.prev_joint.z
    length = math.sqrt(dx*dx + dy*dy + dz*dz)

    return {
        "rotation": [bone.rotation.w, bone.rotation.x, bone.rotation.y, bone.rotation.z],
        "position": [bone.prev_joint.x, bone.prev_joint.y, bone.prev_joint.z],
        "next_joint": [bone.next_joint.x, bone.next_joint.y, bone.next_joint.z],
        "width": 10.0, # Default width as attribute is missing
        "length": length
    }

def format_hand(hand):
    hand_type = "Left" if hand.type == leap.HandType.Left else "Right"
    
    fingers_data = {}
    # 0: Thumb, 1: Index, 2: Middle, 3: Ring, 4: Pinky
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    
    for i, digit in enumerate(hand.digits):
        finger_name = finger_names[i]
        bones = {}
        # 0: Metacarpal, 1: Proximal, 2: Intermediate, 3: Distal
        bone_names = ["Metacarpal", "Proximal", "Intermediate", "Distal"]
        
        for j, bone in enumerate(digit.bones):
            bones[bone_names[j]] = format_bone(bone)
            
        fingers_data[finger_name] = bones

    # Arm / Wrist
    arm_data = format_bone(hand.arm)

    return {
        "id": hand.id,
        "type": hand_type,
        "palm_position": [hand.palm.position.x, hand.palm.position.y, hand.palm.position.z],
        "palm_rotation": [hand.palm.orientation.w, hand.palm.orientation.x, hand.palm.orientation.y, hand.palm.orientation.z],
        "fingers": fingers_data,
        "arm": arm_data
    }

class MyListener(leap.Listener):
    def __init__(self):
        self.sock = create_socket()
        print(f"Sending data to {IP}:{PORT}")

    def on_connection_event(self, event):
        print("Connected to Leap Motion Service")

    def on_device_event(self, event):
        try:
            with event.device.open():
                info = event.device.get_info()
        except leap.LeapCannotOpenDeviceError:
            info = event.device.get_info()
        print(f"Found device {info.serial}")

    def on_tracking_event(self, event):
        data = {
            "timestamp": time.time(),
            "hands": []
        }
        
        for hand in event.hands:
            data["hands"].append(format_hand(hand))
            
        if len(data["hands"]) > 0:
            try:
                message = json.dumps(data).encode('utf-8')
                self.sock.sendto(message, (IP, PORT))
            except Exception as e:
                print(f"Error sending data: {e}")

def main():
    listener = MyListener()
    connection = leap.Connection()
    connection.add_listener(listener)

    print("Connecting to Leap Motion...")
    with connection.open():
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()
