from typing import Sequence
from config import *
import pyvista as pv
import trimesh
import os

def render_shape(shape: trimesh.Trimesh, shape_name: str, c: str = BASE_COLOR_SINGLE):
    if TEST_MODE:
        plotter = pv.Plotter()
    else:
        plotter = pv.Plotter(off_screen=True)

    plotter.camera_position = [
        BASE_CAMERA_XYZ,
        shape.centroid,
        UP
    ]
    pv_mesh = pv.wrap(shape)
    plotter.add_mesh(pv_mesh, color=c)

    if TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        file_path = os.path.join(OUTPUT_DIR, f"alone_{shape_name.lower()}.png")
        plotter.screenshot(file_path)
    plotter.close()

def render_shapes(shapes: Sequence[trimesh.Trimesh], shape_names: Sequence[str], colors: Sequence[str], concept: str):
    if colors is None:
        colors = BASE_COLORS_GROUP

    if TEST_MODE:
        plotter = pv.Plotter()
    else:
        plotter = pv.Plotter(off_screen=True)

    plotter.camera_position = [
        BASE_CAMERA_XYZ,
        BASE_CAMERA_LOOK,
        UP
    ]
    for i in range(len(shapes)):
        pv_mesh = pv.wrap(shapes[i])
        plotter.add_mesh(pv_mesh, color=colors[i % len(colors)])

    if TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        shapes_concat = "_".join([s.lower() for s in shape_names])
        file_path = os.path.join(OUTPUT_DIR, f"{concept.lower()}_{shapes_concat}.png")
        plotter.screenshot(file_path)
    plotter.close()