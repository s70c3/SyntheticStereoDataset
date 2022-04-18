import math
import os
import sys

import bpy
import numpy as np
bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink = True)

def create_object_material(material_name, rgba):
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    nodes["Principled BSDF"].inputs['Base Color'].default_value = rgba
    nodes["Principled BSDF"].inputs['Subsurface'].default_value = 0.5
    nodes["Principled BSDF"].inputs['Subsurface Color'].default_value = rgba


    nodes["Principled BSDF"].inputs['Clearcoat'].default_value = 0.5
    return (mat)


def create_floor_material(material_name, rgba):
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    nodes["Principled BSDF"].inputs['Base Color'].default_value = rgba
    nodes["Principled BSDF"].inputs['Clearcoat'].default_value = 0.5
    return (mat)


def create_object(file_path, location, rotation, rgba, index):
    # Load the mesh
    bpy.ops.import_mesh.ply(filepath=file_path)
    ob = bpy.context.active_object  # Set active object to variable

    ob.scale = (1, 1, 1)
    ob.location = location
    ob.rotation_euler = rotation

    # Assign the object an index, which is used to generate a semantic segmentation map
    bpy.context.object.pass_index = index

    # Create and add material to the object
    mat = create_object_material('Object_' + str(index) + '_Material', rgba=rgba)
    ob.data.materials.append(mat)


def create_floor():
    bpy.ops.mesh.primitive_plane_add(size=1000, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                     scale=(10, 10, 1))
    mat = create_floor_material(material_name='Floor', rgba=(0.9, 0.9, 0.9, 0))
    activeObject = bpy.context.active_object  # Set active object to variable
    activeObject.data.materials.append(mat)



def configure_light():
    bpy.data.objects["Light"].data.type = 'AREA'
    bpy.data.objects["Light"].scale[0] = 30
    bpy.data.objects["Light"].scale[1] = 30

def configure_render(bg):
    from random import uniform, randint
    # Selecting the camera and adding the background
    cam = bpy.context.scene.camera
    filepath = bg


    # Locations
    cam.location.x = -0.71
    cam.location.y = -12
    cam.location.z = 5.5

    # Rotations
    cam.rotation_euler[0] = math.radians(64)
    cam.rotation_euler[1] = math.radians(-0)
    cam.rotation_euler[2] = math.radians(-3)
    img = bpy.data.images.load(filepath)
    cam.data.show_background_images = True
    bg = cam.data.background_images.new()
    bg.image = img

    bpy.context.scene.render.use_multiview = True
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.camera.data.stereo.convergence_mode = 'PARALLEL'
    bpy.context.scene.render.engine = 'CYCLES'
    # bpy.context.scene.render.filepath = os.getcwd() + "/Metadata"

    # Output open exr .exr files
    bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
    # bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.cycles.samples = 10

    # Configure renderer to record object index
    bpy.context.scene.view_layers["View Layer"].use_pass_object_index = True

    # Switch on nodes and get reference
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    for every_node in tree.nodes:
        tree.nodes.remove(every_node)
    # Create a node for the output from the renderer
    RenderLayers_node = tree.nodes.new('CompositorNodeRLayers')
    RenderLayers_node.location = -300, 300

    AplhaOver_node = tree.nodes.new(type="CompositorNodeAlphaOver")
    AplhaOver_node.location = 150, 450

    Scale_node = tree.nodes.new(type="CompositorNodeScale")
    bpy.data.scenes["Scene"].node_tree.nodes["Scale"].space = 'RENDER_SIZE'
    Scale_node.location = -150, 500

    Image_node = tree.nodes.new(type="CompositorNodeImage")
    Image_node.image = img
    Image_node.location = -550, 500

    # Create a node for outputting the rendered image
    image_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
    image_output_node.label = "Image_Output"
    image_output_node.base_path = "Metadata/Image"
    image_output_node.location = 400, 0

    # Create a node for outputting the depth of each pixel from the camera
    depth_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
    depth_output_node.label = "Depth_Output"
    depth_output_node.base_path = "Metadata/Depth"

    depth_output_node.location = 400, -100

    links = tree.links
    links.new(RenderLayers_node.outputs[0], AplhaOver_node.inputs[2])
    links.new(AplhaOver_node.outputs[0], image_output_node.inputs[0])
    links.new(Scale_node.outputs[0], AplhaOver_node.inputs[1])
    links.new(Image_node.outputs[0], Scale_node.inputs[0])

    # Link all the nodes together

    links.new(RenderLayers_node.outputs['Depth'], depth_output_node.inputs['Image'])


from random import uniform, randint, random


def reset_blend():
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
        else:
            obj.select_set(False)
    bpy.ops.object.delete()


def render(files, bg):
    for f, i in zip(files, range(len(files))):
        l = uniform(-2, 2),  uniform(-2, 2),  uniform(-2, 2)
        create_object(f, location=l, rotation=(np.radians(randint(0, 270)), 0, np.radians(randint(0,270))),
                      rgba=(random(), random(), random(), 1), index=i)
    # configure_camera()
    configure_light()

    # configure_bg()
    configure_render(bg)
    render = bpy.context.scene.render
    scale = render.resolution_percentage / 100

    # bpy.context.scene.render.filepath = "test"
    bpy.ops.render.render(write_still=True)
    reset_blend()

