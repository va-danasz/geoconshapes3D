from typing import Sequence
import config
import pyvista as pv
import trimesh
import os

def render_shape(shape: trimesh.Trimesh, shape_name: str, c: str = config.BASE_COLOR_SINGLE, index: int = 0):
    if config.TEST_MODE:
        plotter = pv.Plotter()
    else:
        plotter = pv.Plotter(off_screen=True)

    plotter.camera_position = [
        config.BASE_CAMERA_XYZ,
        shape.centroid,
        config.UP
    ]
    pv_mesh = pv.wrap(shape)
    plotter.add_mesh(pv_mesh, color=c)

    if config.TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        file_path = os.path.join(config.OUTPUT_DIR, "alone", f"alone_{shape_name.lower()}_{index + 1}.png")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plotter.screenshot(file_path)
    plotter.close()

def render_shapes(shapes: Sequence[trimesh.Trimesh], shape_names: Sequence[str], colors: Sequence[str], concept: str, index: int = 0):
    if colors is None:
        colors = config.BASE_COLORS_GROUP

    if config.TEST_MODE:
        plotter = pv.Plotter()
    else:
        plotter = pv.Plotter(off_screen=True)

    plotter.camera_position = [
        config.BASE_CAMERA_XYZ,
        config.BASE_CAMERA_LOOK,
        config.UP
    ]
    for i in range(len(shapes)):
        pv_mesh = pv.wrap(shapes[i])
        plotter.add_mesh(pv_mesh, color=colors[i % len(colors)])

    if config.TEST_MODE:
        plotter.add_axes()
        plotter.show()
    else:
        shapes_concat = "_".join([s.lower() for s in shape_names])
        file_path = os.path.join(config.OUTPUT_DIR, concept.lower(), f"{concept.lower()}_{shapes_concat}_{index+1}.png")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plotter.screenshot(file_path)
    plotter.close()