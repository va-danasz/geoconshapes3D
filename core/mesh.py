import random
import trimesh
import config

def generate_cube() -> trimesh.Trimesh:
    cube_mesh = trimesh.creation.box(extents=random_cube_size())
    translation_matrix = trimesh.transformations.translation_matrix(random_pos())
    cube_mesh.apply_transform(translation_matrix)
    return cube_mesh

def generate_sphere() -> trimesh.Trimesh:
    sphere_mesh = trimesh.creation.icosphere(
        config.BASE_SUBDIVISIONS,
        random.uniform(*config.SPHERE_SIZE_RANGE)
    )
    translation_matrix = trimesh.transformations.translation_matrix(random_pos())
    sphere_mesh.apply_transform(translation_matrix)
    return sphere_mesh

def generate_cone() -> trimesh.Trimesh:
    cone_mesh = trimesh.creation.cone(
        random.uniform(*config.CONE_RADIUS_RANGE),
        random.uniform(*config.CONE_HEIGHT_RANGE),
        config.BASE_CONE_SECTIONS
    )
    translation_matrix = trimesh.transformations.translation_matrix(random_pos())
    cone_mesh.apply_transform(translation_matrix)
    return cone_mesh

def random_pos() -> tuple[float, float, float]:
    return (
        random.uniform(*config.POS_X_RANGE),
        random.uniform(*config.POS_Y_RANGE),
        random.uniform(*config.POS_Z_RANGE),
    )

def random_cube_size() -> tuple[float, float, float]:
    size = random.uniform(*config.CUBE_SIZE_RANGE)
    return size, size, size


def get_mesh(shape: str) -> trimesh.Trimesh:
    match shape:
        case "CUBE":
            mesh_generate = generate_cube()
        case "SPHERE":
            mesh_generate = generate_sphere()
        case "CONE":
            mesh_generate = generate_cone()
        case _:
            raise ValueError(f"Unknown shape: {shape}")
    return mesh_generate
