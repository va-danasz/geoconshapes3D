import trimesh

def generate_cube(size: tuple[int,int,int] = (10, 10, 10), pos: tuple[float,float,float] = (0.0, 0.0, 0.0)):
    cube_mesh = trimesh.creation.box(extents=size)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    cube_mesh.apply_transform(translation_matrix)
    return cube_mesh

def generate_sphere(size: int = 10, pos: tuple[float,float,float] = (0.0, 0.0, 0.0), subdivisions: int = 5):
    sphere_mesh = trimesh.creation.icosphere(subdivisions, size)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    sphere_mesh.apply_transform(translation_matrix)
    return sphere_mesh

def generate_cone(radius: int = 10, height: int = 10, sections: int = 4, pos: tuple[float,float,float] = (0.0, 0.0, 0.0)):
    cone_mesh = trimesh.creation.cone(radius, height, sections)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    cone_mesh.apply_transform(translation_matrix)
    return cone_mesh