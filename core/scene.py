import math
import random
from typing import Sequence
import config
import pyvista as pv
import trimesh
import trimesh.visual.texture
import os
import csv

header_names = [
        "image_name", "img_width", "img_height", "concept",
        "object_id", "object_name", "object_pos_x", "object_pos_y", "object_pos_z",
        "width", "length", "height", "radius", "cone_sides", "bbox_size_x", "bbox_size_y", "bbox_size_z",
        "color", "texture_name", "background_name",
        "cam_pos_x", "cam_pos_y", "cam_pos_z",
        "view_angle", "target_x", "target_y", "target_z"
]

def get_random_file(folder_path: str) -> str | None:
    valid_extensions = (".png", ".jpg", ".jpeg")
    files = [f for f in os.listdir(folder_path) if
             os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(valid_extensions)]
    if not files:
        return None
    file = random.choice(files)
    return os.path.join(folder_path, file)

def camera_angle() -> tuple[float, float, float]:
    horizontal_deg = random.uniform(*config.HORIZONTAL_ANGLE_RANGE)
    elevation_deg = random.uniform(*config.ELEVATION_ANGLE_RANGE)
    horizontal = math.radians(horizontal_deg)
    elevation = math.radians(elevation_deg)

    dx = math.cos(elevation) * math.cos(horizontal)
    dy = math.cos(elevation) * math.sin(horizontal)
    dz = math.sin(elevation)
    return dx, dy, dz

def extract_object_data(shape: trimesh.Trimesh, shape_name: str, shape_id: int, file_name: str,
                        concept: str, color: str | None, plotter: pv.Plotter, bg_path: str, texture_path: str) -> dict:
    w, l, h, radius, cone_sides = None, None, None, None, None
    name = shape_name.lower()

    if name == "cube":
        w, l, h = shape.extents
    elif name == "cone":
        h = shape.extents[2]
        radius = shape.extents[0] / 2.0
        cone_sides = int(config.BASE_CONE_SECTIONS)
    elif name == "sphere":
        radius = shape.extents[0] / 2.0

    return {
        "image_name": file_name, "img_width": config.IMG_W, "img_height": config.IMG_H,
        "concept": concept, "object_id": shape_id, "object_name": shape_name,
        "object_pos_x": shape.centroid[0], "object_pos_y": shape.centroid[1], "object_pos_z": shape.centroid[2],
        "width": w, "length": l, "height": h, "radius": radius, "cone_sides": cone_sides,
        "bbox_size_x": shape.extents[0], "bbox_size_y": shape.extents[1], "bbox_size_z": shape.extents[2],
        "color": color, "texture_name": texture_path, "background_name": bg_path,
        "cam_pos_x": plotter.camera.position[0], "cam_pos_y": plotter.camera.position[1], "cam_pos_z": plotter.camera.position[2],
        "view_angle": config.VIEW_ANGLE,
        "target_x": plotter.camera.focal_point[0], "target_y": plotter.camera.focal_point[1], "target_z": plotter.camera.focal_point[2],
    }

def save_meta_data(data: dict):
    file_exists = os.path.exists(config.CSV_PATH)
    with open(config.CSV_PATH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header_names)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def render_shape(shape: trimesh.Trimesh, shape_name: str, c: str = config.BASE_COLOR_SINGLE, index: int = 0):
    if config.TEST_MODE:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H])
    else:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H], off_screen=True)

    background, texture, pv_mesh = "", "", ""
    if config.RENDER_TEXTURE:
        texture_path = get_random_file(config.TEXTURE_PATH)
        if texture_path:
            texture = texture_path.removeprefix(config.TEXTURE_PATH+"/")
            c = ""
            texture_img = pv.read_texture(texture_path)
            if shape_name.lower() == "sphere":
                pv_mesh = pv.wrap(shape).texture_map_to_sphere()
            elif shape_name.lower() == "cube":
                pv_mesh = pv.Cube(
                    center=shape.centroid,
                    x_length=shape.extents[0],
                    y_length=shape.extents[1],
                    z_length=shape.extents[2],
                    clean=False
                )
                t_coords = pv_mesh.active_texture_coordinates
                t_min, t_max = t_coords.min(), t_coords.max()
                pv_mesh.active_texture_coordinates = (t_coords - t_min) / (t_max - t_min)
            else:
                pv_mesh = pv.wrap(shape).texture_map_to_plane()
            plotter.add_mesh(pv_mesh, texture=texture_img)
    if not config.RENDER_TEXTURE or texture == "":
        plotter.add_mesh(pv_mesh, color=c)

    target = shape.centroid
    dx, dy, dz = camera_angle()
    cam_pos = [target[0] + dx, target[1] + dy, target[2] + dz]

    plotter.camera_position = [cam_pos, target, (0.0, 0.0, 1.0)]
    plotter.camera.view_angle = config.VIEW_ANGLE
    plotter.reset_camera(render=config.TEST_MODE)

    if config.RENDER_BACKGROUND:
        bg_path = get_random_file(config.BACKGROUND_PATH)
        if bg_path:
            background = bg_path.removeprefix(config.BACKGROUND_PATH+"/")
            plotter.add_background_image(bg_path)

    if config.TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        file_name = f"alone_{shape_name.lower()}_{index + 1}.png"
        file_path = os.path.join(config.OUTPUT_PATH, "alone", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plotter.screenshot(file_path)


        data = extract_object_data(shape, shape_name, 0, file_name, "ALONE", c, plotter, background, texture)
        save_meta_data(data)
    plotter.close()

def render_shapes(shapes: Sequence[trimesh.Trimesh], shape_names: Sequence[str], colors: list[str], concept: str, index: int = 0):
    if config.TEST_MODE:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H])
    else:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H], off_screen=True)

    textures = []
    background, texture = "", ""
    for i in range(len(shapes)):
        pv_mesh = pv.wrap(shapes[i])
        if config.RENDER_TEXTURE:
            texture_path = get_random_file(config.TEXTURE_PATH)
            if texture_path:
                texture = texture_path.removeprefix(config.TEXTURE_PATH + "/")
                textures.append(texture)
                colors[i] = ""
                texture_img = pv.read_texture(texture_path)
                if shape_names[i].lower() == "sphere":
                    pv_mesh = pv_mesh.texture_map_to_sphere()
                elif shape_names[i].lower() == "cube":
                    pv_mesh = pv.Cube(
                        center=shapes[i].centroid,
                        x_length=shapes[i].extents[0],
                        y_length=shapes[i].extents[1],
                        z_length=shapes[i].extents[2],
                        clean=False
                    )
                    t_coords = pv_mesh.active_texture_coordinates
                    t_min, t_max = t_coords.min(), t_coords.max()
                    pv_mesh.active_texture_coordinates = (t_coords - t_min) / (t_max - t_min)
                else:
                    pv_mesh = pv_mesh.texture_map_to_plane()
                plotter.add_mesh(pv_mesh, texture=texture_img)
        if not config.RENDER_TEXTURE or texture == "":
            textures.append("")
            plotter.add_mesh(pv_mesh, color=colors[i])

    combined_mesh = trimesh.util.concatenate(*shapes)
    target = combined_mesh.centroid
    dx, dy, dz = camera_angle()
    cam_pos = [target[0] + dx, target[1] + dy, target[2] + dz]

    plotter.camera_position = [cam_pos, target, (0.0, 0.0, 1.0)]
    plotter.camera.view_angle = config.VIEW_ANGLE
    plotter.reset_camera(render=config.TEST_MODE)

    if config.RENDER_BACKGROUND:
        bg_path = get_random_file(config.BACKGROUND_PATH)
        if bg_path:
            background = bg_path.removeprefix(config.BACKGROUND_PATH + "/")
            plotter.add_background_image(bg_path)

    if config.TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        shapes_concat = "_".join([s.lower() for s in shape_names])
        file_name = f"{concept.lower()}_{shapes_concat}_{index+1}.png"
        file_path = os.path.join(config.OUTPUT_PATH, concept.lower(), file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plotter.screenshot(file_path)
        for i in range(len(shapes)):
            data = extract_object_data(shapes[i], shape_names[i], i, file_name, concept, colors[i], plotter, background, textures[i])
            save_meta_data(data)
    plotter.close()