import math
import random
import pyvista as pv
import trimesh
import trimesh.visual.texture
import os
import csv
import numpy as np
from typing import Sequence, cast
import config
import core.classifier as classifier
from core.labels import Shape, Concept, Color
from core.schema import MeshMetaData, RenderMetaData

header_names_mesh = list(MeshMetaData.__annotations__.keys())
header_names_render = list(RenderMetaData.__annotations__.keys())

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

def extract_object_mesh(shape: trimesh.Trimesh, shape_name: Shape, shape_id: int, concept: Concept, color: Color|None,
                        bg_path: str|None, texture_path: str|None, mesh_id: int) -> MeshMetaData:
    extents = np.asarray(shape.extents)
    centroid = shape.centroid

    if extents is None or centroid is None:
        raise ValueError("Cannot extract mesh data: shape is empty.")

    w, l, h, radius, cone_sides = None, None, None, None, None

    if shape_name == Shape.CUBE:
        w, l, h = extents
    elif shape_name == Shape.CONE:
        h = extents[2]
        radius = extents[0] / 2.0
        cone_sides = int(config.BASE_CONE_SECTIONS)
    elif shape_name == Shape.SPHERE:
        radius = extents[0] / 2.0

    return {
        "id": f"{mesh_id:03d}", "concept": concept, "img_width": config.IMG_W, "img_height": config.IMG_H,
        "object_id": shape_id, "object_name": shape_name.lower(),
        "object_pos_x": centroid[0], "object_pos_y": centroid[1], "object_pos_z": centroid[2],
        "width": w, "length": l, "height": h, "radius": radius, "cone_sides": cone_sides,
        "bbox_size_x": extents[0], "bbox_size_y": extents[1], "bbox_size_z": extents[2],
        "color": color, "texture_name": texture_path, "background_name": bg_path
    }

def extract_object_render(shape_id: int, file_name: str, plotter: pv.Plotter, mesh_id: int, concept_2d: Concept, dist_norm: float|None) -> RenderMetaData:
    return {
        "mesh_id": f"{mesh_id:03d}", "image_name": file_name, "object_id": shape_id,
        "cam_pos_x": plotter.camera.position[0], "cam_pos_y": plotter.camera.position[1], "cam_pos_z": plotter.camera.position[2],
        "view_angle": config.VIEW_ANGLE,
        "target_x": plotter.camera.focal_point[0], "target_y": plotter.camera.focal_point[1], "target_z": plotter.camera.focal_point[2],
        "concept_2d": concept_2d, "dist_norm": dist_norm
    }
extract_object_mesh.counter = 0

def save_render_meta_data(data: RenderMetaData) -> None:
    file_exists = os.path.exists(config.CSV_PATH_RENDER)
    with open(config.CSV_PATH_RENDER, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter[str](f, fieldnames=header_names_render)
        if not file_exists:
            writer.writeheader()
        writer.writerow(dict(data))
    f.close()

def save_mesh_meta_data(data: MeshMetaData) -> None:
    file_exists = os.path.exists(config.CSV_PATH_MESH)
    with open(config.CSV_PATH_MESH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter[str](f, fieldnames=header_names_mesh)
        if not file_exists:
            writer.writeheader()
        writer.writerow(dict(data))
    f.close()

def render_shape(shape: trimesh.Trimesh, shape_name: Shape, shape_color: Color|None, index: int = 0):
    if config.TEST_MODE:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H])
    else:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H], off_screen=True)

    background, texture, pv_mesh = "", "", ""
    if config.RENDER_TEXTURE:
        texture_path = get_random_file(config.TEXTURE_PATH)
        if texture_path:
            texture = texture_path.removeprefix(config.TEXTURE_PATH+"/")
            shape_color = None
            texture_img = pv.read_texture(texture_path)
            if shape_name == Shape.SPHERE:
                pv_mesh = pv.wrap(shape).texture_map_to_sphere()
            elif shape_name == Shape.CUBE:
                pv_mesh = pv.Cube(
                    center=np.asarray(shape.centroid),
                    x_length=shape.extents[0],
                    y_length=shape.extents[1],
                    z_length=shape.extents[2],
                    clean=False
                )

                t_coords = pv_mesh.active_texture_coordinates
                if t_coords is not None:
                    t_min, t_max = float(t_coords.min()), float(t_coords.max())
                    pv_mesh.active_texture_coordinates = (t_coords - t_min) / (t_max - t_min)
            else:
                pv_mesh = pv.wrap(shape).texture_map_to_plane()
            plotter.add_mesh(pv_mesh, texture=texture_img)
    if not config.RENDER_TEXTURE or texture == "":
        pv_mesh = pv.wrap(shape)
        plotter.add_mesh(pv_mesh, color=shape_color)

    target = shape.centroid

    if config.RENDER_BACKGROUND:
        bg_path = get_random_file(config.BACKGROUND_PATH)
        if bg_path:
            background = bg_path.removeprefix(config.BACKGROUND_PATH+"/")
            plotter.add_background_image(bg_path)

    current_mesh_id = extract_object_mesh.counter
    for render_index in range(config.RENDER_COUNT):
        dx, dy, dz = camera_angle()
        cam_pos = [target[0] + dx, target[1] + dy, target[2] + dz]

        plotter.camera_position = [cam_pos, target, (0.0, 0.0, 1.0)]
        plotter.camera.view_angle = config.VIEW_ANGLE
        plotter.reset_camera(render=config.TEST_MODE)

        if config.TEST_MODE:
            plotter.add_axes()
            plotter.show()
        else:
            file_name = f"alone_{shape_name.lower()}_{index}_{render_index}.png"
            file_path = os.path.join(config.OUTPUT_PATH, "alone", file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            plotter.screenshot(file_path)

            data_mesh = extract_object_mesh(shape, shape_name, 0, Concept.ALONE, shape_color, background, texture, current_mesh_id)
            data_render = extract_object_render(0, file_name, plotter, current_mesh_id, Concept.ALONE, None)
            if render_index == 0:
                save_mesh_meta_data(data_mesh)
            save_render_meta_data(data_render)

    extract_object_mesh.counter += 1
    plotter.close()

def render_shapes(shapes: Sequence[trimesh.Trimesh], shape_names: Sequence[Shape], colors: list[Color|None], concept: Concept, index: int = 0):
    if config.TEST_MODE:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H])
    else:
        plotter = pv.Plotter(window_size=[config.IMG_W, config.IMG_H], off_screen=True)

    textures = []
    actors = []
    background, texture, actor = "", "", ""
    for shape_id in range(len(shapes)):
        pv_mesh = pv.wrap(shapes[shape_id])
        if config.RENDER_TEXTURE:
            texture_path = get_random_file(config.TEXTURE_PATH)
            if texture_path:
                texture = texture_path.removeprefix(config.TEXTURE_PATH + "/")
                textures.append(texture)
                colors[shape_id] = None
                texture_img = pv.read_texture(texture_path)
                if shape_names[shape_id] == Shape.SPHERE:
                    pv_mesh = pv_mesh.texture_map_to_sphere()
                elif shape_names[shape_id] == Shape.CUBE:
                    pv_mesh = pv.Cube(
                        center=np.asarray(shapes[shape_id].centroid),
                        x_length=shapes[shape_id].extents[0],
                        y_length=shapes[shape_id].extents[1],
                        z_length=shapes[shape_id].extents[2],
                        clean=False
                    )
                    t_coords = pv_mesh.active_texture_coordinates
                    if t_coords is not None:
                        t_min, t_max = float(t_coords.min()), float(t_coords.max())
                        pv_mesh.active_texture_coordinates = (t_coords - t_min) / (t_max - t_min)
                else:
                    pv_mesh = pv_mesh.texture_map_to_plane()
                actor = plotter.add_mesh(pv_mesh, texture=texture_img)
        if not config.RENDER_TEXTURE or texture == "":
            textures.append("")
            actor = plotter.add_mesh(pv_mesh, color=colors[shape_id])
        actors.append(actor)

    combined_mesh = cast(trimesh.Trimesh, trimesh.util.concatenate(*shapes))
    target = combined_mesh.centroid

    if config.RENDER_BACKGROUND:
        bg_path = get_random_file(config.BACKGROUND_PATH)
        if bg_path:
            background = bg_path.removeprefix(config.BACKGROUND_PATH + "/")
            plotter.add_background_image(bg_path)

    current_mesh_id = extract_object_mesh.counter
    for render_index in range(config.RENDER_COUNT):
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
            file_name = f"{concept.lower()}_{shapes_concat}_{index}_{render_index}.png"
            file_path = os.path.join(config.OUTPUT_PATH, concept.lower(), file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            plotter.screenshot(file_path)
            for shape_id in range(len(shapes)):
                data_mesh = extract_object_mesh(shapes[shape_id], shape_names[shape_id], shape_id, concept,
                                                colors[shape_id], background, textures[shape_id], current_mesh_id)
                concept_2d, dist_2d = classifier.classify_2d(actors, plotter)
                data_render = extract_object_render(shape_id, file_name, plotter, current_mesh_id, concept_2d, dist_2d)
                if render_index == 0:
                    save_mesh_meta_data(data_mesh)
                save_render_meta_data(data_render)
    extract_object_mesh.counter += 1
    plotter.close()