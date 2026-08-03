import math
import random
from typing import Sequence
import config
import pyvista as pv
import trimesh
import os

def camera_angle() -> tuple[float, float, float]:
    horizontal_deg = random.uniform(*config.HORIZONTAL_ANGLE_RANGE)
    elevation_deg = random.uniform(*config.ELEVATION_ANGLE_RANGE)
    horizontal = math.radians(horizontal_deg)
    elevation = math.radians(elevation_deg)

    dx = math.cos(elevation) * math.cos(horizontal)
    dy = math.cos(elevation) * math.sin(horizontal)
    dz = math.sin(elevation)
    return dx, dy, dz

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

    plotter.camera_position = [cam_pos, target, config.UP]
    plotter.camera.view_angle = config.VIEW_ANGLE
    plotter.reset_camera(render=config.TEST_MODE)

    if config.TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        file_path = os.path.join("output", "alone", f"alone_{shape_name.lower()}_{index + 1}.png")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plotter.screenshot(file_path)
    plotter.close()

def render_shapes(shapes: Sequence[trimesh.Trimesh], shape_names: Sequence[str], colors: Sequence[str], concept: str, index: int = 0):
    if colors is None:
        colors = config.BASE_COLORS_GROUP

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

    plotter.camera_position = [cam_pos, target, config.UP]
    plotter.camera.view_angle = config.VIEW_ANGLE
    plotter.reset_camera(render=config.TEST_MODE)

    if config.TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        shapes_concat = "_".join([s.lower() for s in shape_names])
        file_path = os.path.join("output", concept.lower(), f"{concept.lower()}_{shapes_concat}_{index+1}.png")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plotter.screenshot(file_path)
    plotter.close()