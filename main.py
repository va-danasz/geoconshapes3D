import random
from config import *
from core import mesh, scene

def get_mesh(shape: str):
    match shape:
        case "CUBE":
            mesh_generate = mesh.generate_cube()
        case "SPHERE":
            mesh_generate = mesh.generate_sphere(radius=5, pos=(10, 10, 20))
        case "CONE":
            mesh_generate = mesh.generate_cone(radius=5, height=8, pos=(-10, -15, -5))
        case _:
            raise ValueError(f"Unknown shape: {shape}")
    return mesh_generate

def generate_group(shape1: str, shape2: str, conc: str):
    mesh1 = get_mesh(shape1)
    mesh2 = get_mesh(shape2)

    for i in range(SAMPLE_COUNT):
        scene.render_shapes([mesh1, mesh2], [shape1, shape2], gen_color_list(len(SHAPES)), conc)

def generate_single(shape: str):
    mesh_single = get_mesh(shape)
    for i in range(SAMPLE_COUNT):
        scene.render_shape(mesh_single, shape, random.choice(COLORS))

def gen_color_list(shapes_count: int):
    gen_colors = []
    if shapes_count <= len(COLORS):
        for i in range(shapes_count):
            c = random.choice(COLORS)
            while c in gen_colors:
                c = random.choice(COLORS)
            gen_colors.append(c)
    else:
        for i in range(shapes_count):
            gen_colors.append(random.choice(COLORS))
    return gen_colors

for concept in CONCEPTS:
    for shape1_IDX in range(len(SHAPES)):
        if concept != "ALONE":
            for shape2_IDX in range(shape1_IDX, len(SHAPES)):
                generate_group(SHAPES[shape1_IDX], SHAPES[shape2_IDX], concept)
        else:
            generate_single(SHAPES[shape1_IDX])