import trimesh
from config import *

def generate_cube(size: tuple[int,int,int] = BASE_CUBE_SIZE, pos: tuple[float,float,float] = BASE_SHAPE_POS):
    cube_mesh = trimesh.creation.box(extents=size)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    cube_mesh.apply_transform(translation_matrix)
    return cube_mesh

def generate_sphere(radius: int = BASE_RADIUS, pos: tuple[float,float,float] = BASE_SHAPE_POS, subdivisions: int = BASE_SUBDIVISIONS):
    sphere_mesh = trimesh.creation.icosphere(subdivisions, radius)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    sphere_mesh.apply_transform(translation_matrix)
    return sphere_mesh

def generate_cone(radius: int = BASE_RADIUS, height: int = BASE_CONE_HEIGHT, sections: int = BASE_CONE_SECTIONS, pos: tuple[float,float,float] = BASE_SHAPE_POS):
    cone_mesh = trimesh.creation.cone(radius, height, sections)
    translation_matrix = trimesh.transformations.translation_matrix(pos)
    cone_mesh.apply_transform(translation_matrix)
    return cone_mesh