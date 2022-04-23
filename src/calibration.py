import math

import bpy
import cv2
import mathutils
import mutils as mutils
import numpy as np
def camera_intrinsics_matrix():
    # https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera
    f_mm = bpy.context.scene.camera.data.lens
    x_res_px = bpy.context.scene.render.resolution_x
    y_res_px = bpy.context.scene.render.resolution_y
    render_scale = bpy.context.scene.render.resolution_percentage / 100.0
    aspect_ratio = bpy.context.scene.render.pixel_aspect_x / bpy.context.scene.render.pixel_aspect_y

    if bpy.context.scene.camera.data.sensor_fit == 'VERTICAL':
        s_u = x_res_px / bpy.context.scene.camera.data.sensor_width * (1.0 / aspect_ratio) * render_scale
        s_v = y_res_px / bpy.context.scene.camera.data.sensor_height * render_scale
    else:  # 'HORIZONTAL', 'AUTO;
        s_u = x_res_px / bpy.context.scene.camera.data.sensor_width * render_scale
        s_v = y_res_px / bpy.context.scene.camera.data.sensor_height * aspect_ratio * render_scale

    f_u = f_mm * s_u
    f_v = f_mm * s_v
    u_0 = x_res_px / 2.0 * render_scale
    v_0 = y_res_px / 2.0 * render_scale
    skew = 0

    return np.array([
        [f_u, skew, u_0],
        [0.0, f_v, v_0],
        [0.0, 0.0, 1.0]
    ])


def camera_extrinsics_matrix():
    camera = bpy.context.scene.camera
    pose_location, pose_rotation_q = camera.matrix_world.decompose()[0:2]

    inv_rotation = pose_rotation_q.to_matrix().transposed()
    inv_translation = -1 * inv_rotation @ pose_location

    blender_2_cv_rotation = mathutils.Matrix((
        (1, 0, 0),
        (0, -1, 0),
        (0, 0, -1)
    ))

    extrinsic_rotation = blender_2_cv_rotation @ inv_rotation
    extrinsic_translation = blender_2_cv_rotation @ inv_translation

    extrinsic_matrix = np.array([
        [extrinsic_rotation[i][j] for j in range(3)] + [extrinsic_translation[i]] for i in range(3)
    ])

    return extrinsic_matrix



import bpy
import bpy_extras
from mathutils import Matrix
from mathutils import Vector


# ---------------------------------------------------------------
# 3x4 P matrix from Blender camera
# ---------------------------------------------------------------

# Build intrinsic camera parameters from Blender camera data
#
# See notes on this in
# blender.stackexchange.com/questions/15102/what-is-blenders-camera-projection-matrix-model
def get_calibration_matrix_K_from_blender(camd):
    f_in_mm = camd.lens
    print("focal", f_in_mm)
    scene = bpy.context.scene
    resolution_x_in_px = scene.render.resolution_x
    resolution_y_in_px = scene.render.resolution_y
    scale = scene.render.resolution_percentage / 100
    sensor_width_in_mm = camd.sensor_width
    sensor_height_in_mm = camd.sensor_height
    pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
    if (camd.sensor_fit == 'VERTICAL'):
        # the sensor height is fixed (sensor fit is horizontal),
        # the sensor width is effectively changed with the pixel aspect ratio
        s_u = resolution_x_in_px * scale / sensor_width_in_mm / pixel_aspect_ratio
        s_v = resolution_y_in_px * scale / sensor_height_in_mm
    else:  # 'HORIZONTAL' and 'AUTO'
        # the sensor width is fixed (sensor fit is horizontal),
        # the sensor height is effectively changed with the pixel aspect ratio
        pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        s_u = resolution_x_in_px * scale / sensor_width_in_mm
        s_v = resolution_y_in_px * scale * pixel_aspect_ratio / sensor_height_in_mm

    # Parameters of intrinsic calibration matrix K
    alpha_u = f_in_mm * s_u
    alpha_v = f_in_mm * s_v
    u_0 = resolution_x_in_px * scale / 2
    v_0 = resolution_y_in_px * scale / 2
    skew = 0  # only use rectangular pixels

    K = Matrix(
        ((alpha_u, skew, u_0),
         (0, alpha_v, v_0),
         (0, 0, 1)))
    return K


# Returns camera rotation and translation matrices from Blender.
#
# There are 3 coordinate systems involved:
#    1. The World coordinates: "world"
#       - right-handed
#    2. The Blender camera coordinates: "bcam"
#       - x is horizontal
#       - y is up
#       - right-handed: negative z look-at direction
#    3. The desired computer vision camera coordinates: "cv"
#       - x is horizontal
#       - y is down (to align to the actual pixel coordinates
#         used in digital images)
#       - right-handed: positive z look-at direction
def get_3x4_RT_matrix_from_blender(cam):
    # bcam stands for blender camera
    R_bcam2cv = Matrix(
        ((1, 0, 0),
         (0, -1, 0),
         (0, 0, -1)))

    # Transpose since the rotation is object rotation,
    # and we want coordinate rotation
    # R_world2bcam = cam.rotation_euler.to_matrix().transposed()
    # T_world2bcam = -1*R_world2bcam * location
    #
    # Use matrix_world instead to account for all constraints
    location, rotation = cam.matrix_world.decompose()[0:2]
    R_world2bcam = rotation.to_matrix().transposed()

    # Convert camera location to translation vector used in coordinate changes
    # T_world2bcam = -1*R_world2bcam*cam.location
    # Use location from matrix_world to account for constraints:
    T_world2bcam = -1 * R_world2bcam @ location

    # Build the coordinate transform matrix from world to computer vision camera
    # NOTE: Use * instead of @ here for older versions of Blender
    # TODO: detect Blender version
    R_world2cv = R_bcam2cv @ R_world2bcam
    T_world2cv = R_bcam2cv @ T_world2bcam

    # put into 3x4 matrix
    RT = Matrix((
        R_world2cv[0][:] + (T_world2cv[0],),
        R_world2cv[1][:] + (T_world2cv[1],),
        R_world2cv[2][:] + (T_world2cv[2],)
    ))
    return RT


def get_3x4_P_matrix_from_blender(cam):
    K = get_calibration_matrix_K_from_blender(cam.data)
    RT = get_3x4_RT_matrix_from_blender(cam)
    return K @ RT, K, RT


# ----------------------------------------------------------
# Alternate 3D coordinates to 2D pixel coordinate projection code
# adapted from https://blender.stackexchange.com/questions/882/how-to-find-image-coordinates-of-the-rendered-vertex?lq=1
# to have the y axes pointing up and origin at the top-left corner
def project_by_object_utils(cam, point):
    scene = bpy.context.scene
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, point)
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    return Vector((co_2d.x * render_size[0], render_size[1] - co_2d.y * render_size[1]))


# ----------------------------------------------------------
def camera_calibration():
    # Insert your camera name here
    cam = bpy.context.scene.camera

    # Locations
    cam.location.x = -0.71
    cam.location.y = -12
    cam.location.z = 5.5

    # Rotations
    cam.rotation_euler[0] = math.radians(64)
    cam.rotation_euler[1] = math.radians(0)
    cam.rotation_euler[2] = math.radians(0)
    bpy.context.scene.render.use_multiview = True
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.camera.data.stereo.convergence_mode = 'OFFAXIS'
    bpy.context.scene.camera.data.stereo.interocular_distance = 0.065
    bpy.context.scene.camera.data.stereo.convergence_distance = 1.95


    print("Pixel per mm")
    print(pixel_size_mm_per_px(bpy.context.scene))

    print("Intristic")
    K = camera_intrinsics_matrix()
    print("Extristic")
    RT = camera_extrinsics_matrix()

    P, K_mat, RT_mat = get_3x4_P_matrix_from_blender(cam)
    print("K")
    print(K)
    print("RT")
    print(RT)
    print("P")
    print(P)

    print("==== Tests ====")
    e1 = Vector((1, 0, 0, 1))
    e2 = Vector((0, 1, 0, 1))
    e3 = Vector((0, 0, 1, 1))
    O = Vector((0, 0, 0, 1))

    p1 = P @ e1
    p1 /= p1[2]
    print("Projected e1")
    print(p1)
    print("proj by object_utils")
    print(project_by_object_utils(cam, Vector(e1[0:3])))

    p2 = P @ e2
    p2 /= p2[2]
    print("Projected e2")
    print(p2)
    print("proj by object_utils")
    print(project_by_object_utils(cam, Vector(e2[0:3])))

    p3 = P @ e3
    p3 /= p3[2]
    print("Projected e3")
    print(p3)
    print("proj by object_utils")
    print(project_by_object_utils(cam, Vector(e3[0:3])))

    pO = P @ O
    pO /= pO[2]
    print("Projected world origin")
    print(pO)
    print("proj by object_utils")
    print(project_by_object_utils(cam, Vector(O[0:3])))

    # Bonus code: save the 3x4 P matrix into a plain text file
    # Don't forget to import numpy for this
    nP = np.matrix(P)

    # np.savetxt("/tmp/P3x4.txt", nP)  # to select precision, use e.g. fmt='%.2f'
    new_camera_matrix_r, roi = cv2.getOptimalNewCameraMatrix(K,1,(1920,1080),1,(1920,1080))
    return new_camera_matrix_r, K


""" Defining fuctions to obtain ground truth data """
def get_scene_resolution(scene):
    resolution_scale = (scene.render.resolution_percentage / 100.0)
    resolution_x = scene.render.resolution_x * resolution_scale # [pixels]
    resolution_y = scene.render.resolution_y * resolution_scale # [pixels]
    return int(resolution_x), int(resolution_y)


def get_sensor_size(sensor_fit, sensor_x, sensor_y):
    if sensor_fit == 'VERTICAL':
        return sensor_y
    return sensor_x


def get_sensor_fit(sensor_fit, size_x, size_y):
    if sensor_fit == 'AUTO':
        if size_x >= size_y:
            return 'HORIZONTAL'
        else:
            return 'VERTICAL'
    return sensor_fit


def pixel_size_mm_per_px(scene):
    """ Get intrinsic camera parameters: focal length and principal point. """
    # ref: https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera/120063#120063
    focal_length = scene.camera.data.lens # [mm]
    res_x, res_y = get_scene_resolution(scene)
    cam_data = scene.camera.data
    sensor_size_in_mm = get_sensor_size(cam_data.sensor_fit, cam_data.sensor_width, cam_data.sensor_height)
    sensor_fit = get_sensor_fit(
        cam_data.sensor_fit,
        scene.render.pixel_aspect_x * res_x,
        scene.render.pixel_aspect_y * res_y
    )
    pixel_aspect_ratio = scene.render.pixel_aspect_y / scene.render.pixel_aspect_x
    if sensor_fit == 'HORIZONTAL':
        view_fac_in_px = res_x
    else:
        view_fac_in_px = pixel_aspect_ratio * res_y
    pixel_size_mm_per_px = (sensor_size_in_mm / focal_length) / view_fac_in_px

    return pixel_size_mm_per_px

camera_calibration()