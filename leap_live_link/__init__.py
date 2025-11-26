bl_info = {
    "name": "Leap Motion Live Link",
    "author": "fnoji",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Leap Link",
    "description": "Live link for Ultraleap Leap Motion",
    "category": "Animation",
}

import bpy
from . import panel, operator

def register():
    operator.register()
    panel.register()

def unregister():
    panel.unregister()
    operator.unregister()

if __name__ == "__main__":
    register()
