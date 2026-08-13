import math
import random
from typing import Sequence
import config
import pyvista as pv
import trimesh
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
                        concept: str, color: str | None, plotter: pv.Plotter) -> dict:
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
        "color": color, "texture_name": None, "background_name": None,
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

    pv_mesh = pv.wrap(shape)
    plotter.add_mesh(pv_mesh, color=c)

    target = shape.centroid
    dx, dy, dz = camera_angle()
    cam_pos = [target[0] + dx, target[1] + dy, target[2] + dz]

    plotter.camera_position = [cam_pos, target, (0.0, 0.0, 1.0)]
    plotter.camera.view_angle = config.VIEW_ANGLE
    plotter.reset_camera(render=config.TEST_MODE)

    if config.TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        file_name = f"alone_{shape_name.lower()}_{index + 1}.png"
        file_path = os.path.join(config.OUTPUT_PATH, "alone", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plotter.screenshot(file_path)

        data = extract_object_data(shape, shape_name, 0, file_name, "ALONE", c, plotter)
        save_meta_data(data)
    plotter.close()

def render_shapes(shapes: Sequence[trimesh.Trimesh], shape_names: Sequence[str], colors: Sequence[str], concept: str, index: int = 0):
    if config.TEST_MODE:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H])
    else:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H], off_screen=True)

    for i in range(len(shapes)):
        pv_mesh = pv.wrap(shapes[i])
        plotter.add_mesh(pv_mesh, color=colors[i % len(colors)])

    combined_mesh = trimesh.util.concatenate(*shapes)
    target = combined_mesh.centroid
    dx, dy, dz = camera_angle()
    cam_pos = [target[0] + dx, target[1] + dy, target[2] + dz]

    plotter.camera_position = [cam_pos, target, (0.0, 0.0, 1.0)]
    plotter.camera.view_angle = config.VIEW_ANGLE
    plotter.reset_camera(render=config.TEST_MODE)

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

            data = extract_object_data(shapes[i], shape_names[i], i, file_name, concept, colors[i], plotter)
            save_meta_data(data)
    plotter.close()