import pyvista as pv
UP = (0.0, 0.0, 1.0)

def show_shape(shape, c ="blue"):
    interactive_plotter = pv.Plotter()
    interactive_plotter.camera_position = [
        (40.0, -40.0, 40.0),
        (0.0, 0.0, 0.0),
        UP
    ]
    interactive_plotter.add_mesh(shape, color=c)
    interactive_plotter.add_axes()
    interactive_plotter.show()