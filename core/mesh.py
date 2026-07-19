import trimesh

def generate_cube(size = (10, 10, 10), pos = (0, 0, 0)):
    cube_mesh = trimesh.creation.box(extents=size)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    cube_mesh.apply_transform(translation_matrix)
    return cube_mesh

def generate_sphere(size = 10, pos = (0, 0, 0), subdivisions = 5):
    sphere_mesh = trimesh.creation.icosphere(subdivisions, size)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    sphere_mesh.apply_transform(translation_matrix)
    return sphere_mesh

def generate_cone(radius = 10, height = 10, sections = 4, pos = (0, 0, 0)):
    cone_mesh = trimesh.creation.cone(radius, height, sections)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    cone_mesh.apply_transform(translation_matrix)
    return cone_mesh