#https://youtube.com/playlist?list=PLNizloUxMUXLHNHn2-0Wmdf2YtygXcmop 
#Reset User View To Default. Default Hotkey : Ctrl+Shift+Alt+Home. autorun=True
#autorun=True
#① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ This Operator is a part of CommandBox addon for Blender3d
#bpy.ops.view3d.modal_draw_operator('INVOKE_DEFAULT', text=textinfo_, duration=5)


import bpy
import math
from mathutils import Euler

class VIEW3D_OT_ResetViewToDefault(bpy.types.Operator):
    """Resets the 3D Viewport camera view to default (perspective)."""
    bl_idname = "view3d.reset_view_to_default"  # Technical ID
    bl_label = "Set Camera View To Default"    # User-friendly name
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region, 'scene': bpy.context.scene}
                        camera = context.scene.camera
                        if camera:
                            print("Camera object found:", camera)
                            print("Camera Name:", camera.name)
                        else:
                            print("ERROR: Camera object not found.")
                            self.report({'ERROR'}, "ERROR: Camera object not found.")
                            return {'CANCELLED'}
                        if area.spaces and hasattr(area.spaces[0], 'region_3d'):
                            region_3d = area.spaces[0].region_3d
                            view_rotation_deg = tuple(math.degrees(angle) for angle in region_3d.view_rotation)
                            
                            region_3d.view_location = (-0.7651, 0.3688, 1.7046)
                            
                            degrees = (63.526817658912385, 7.1112716314312746e-06, 66.16962275446542)
                            radians = tuple(math.radians(degree) for degree in degrees)
                            euler_rotation = Euler(radians)
                            quaternion_rotation = euler_rotation.to_quaternion()
                            region_3d.view_rotation = quaternion_rotation
                            
                            region_3d.view_distance = 17.986562728881836
                            
                            print(f"region_3d.view_location: {region_3d.view_location}")
                            print(f"region_3d.view_rotation (degrees): {view_rotation_deg}")
                            print(f"region_3d.view_camera_zoom: {region_3d.view_camera_zoom}")
                            print(f"region_3d.view_distance: {region_3d.view_distance}")
                            
                            camera.data.lens = 35
                            region_3d.view_camera_zoom = 1

                            region_3d.view_perspective = 'PERSP'  # Force perspective
                            print(f"Viewport perspective mode: {region_3d.view_perspective}")


                        if camera and area.spaces[0].region_3d.view_perspective not in ('PERSP','ORTHO'):
                            print("Camera is Active")
                        else:
                            print("User Camera is Active")

        return {'FINISHED'}


def register():
    bpy.utils.register_class(VIEW3D_OT_ResetViewToDefault)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        
        existing_kmi = None
        for kmi in km.keymap_items:
            if kmi.idname == VIEW3D_OT_ResetViewToDefault.bl_idname:
                existing_kmi = kmi
                break
        
        if not existing_kmi:
           kmi = km.keymap_items.new(VIEW3D_OT_ResetViewToDefault.bl_idname, 'HOME', 'PRESS', ctrl=True, shift=True, alt=True)
        else:
           print ("Shortcut already exists, skipping it.")
            

def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_ResetViewToDefault)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                if kmi.idname == VIEW3D_OT_ResetViewToDefault.bl_idname:
                    km.keymap_items.remove(kmi)
                    break


if __name__ == "__main__":
    register()

    bpy.ops.view3d.reset_view_to_default()