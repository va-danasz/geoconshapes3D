from typing import Sequence
import pyvista as pv
import trimesh

UP = (0.0, 0.0, 1.0)

def render_shape(shape: trimesh.Trimesh, c: str ="blue"):
    interactive_plotter = pv.Plotter()
    interactive_plotter.camera_position = [
        (40.0, -40.0, 40.0),
        shape.centroid,
        UP
    ]
    pv_mesh = pv.wrap(shape)
    interactive_plotter.add_mesh(pv_mesh, color=c)
    interactive_plotter.add_axes()
    interactive_plotter.show()

def render_shapes(shapes: Sequence[trimesh.Trimesh], colors: Sequence[str]):
    if colors is None:
        colors = ["blue"]
    interactive_plotter = pv.Plotter()
    interactive_plotter.camera_position = [
        (40.0, -40.0, 40.0),
        (0.0, 0.0, 0.0),
        UP
    ]
    for i in range(len(shapes)):
        pv_mesh = pv.wrap(shapes[i])
        interactive_plotter.add_mesh(pv_mesh, color=colors[i % len(colors)])
    interactive_plotter.add_axes()
    interactive_plotter.show()