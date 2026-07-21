import random
from core import mesh, scene

random.seed(12345)
IMG_W, IMG_H = 500, 500
SAMPLE_COUNT = 1
concepts = ["ALONE", "FAR", "CLOSE", "OVERLAP"]
shapes = ["CUBE", "SPHERE", "CONE"]
colors = ["red", "green", "blue"]

def get_mesh(shape: str):
    match shape:
        case "CUBE":
            mesh_generate = mesh.generate_cube()
        case "SPHERE":
            mesh_generate = mesh.generate_sphere(size=5, pos=(10, 10, 20))
        case "CONE":
            mesh_generate = mesh.generate_cone(radius=5, height=8, pos=(-10, -15, -5))
        case _:
            raise ValueError(f"Unknown shape: {shape}")
    return mesh_generate

def generate_group(shape1: str, shape2: str, c: str):
    mesh1 = get_mesh(shape1)
    mesh2 = get_mesh(shape2)

    for i in range(SAMPLE_COUNT):
        print(f"{shape1} - {shape2} [{c}]")
        scene.render_shapes([mesh1, mesh2], gen_color_list(len(shapes)))

def generate_single(shape: str):
    mesh_single = get_mesh(shape)
    for i in range(SAMPLE_COUNT):
        scene.render_shape(mesh_single, random.choice(colors))

def gen_color_list(shapes_count: int):
    gen_colors = []
    if shapes_count <= len(colors):
        for i in range(shapes_count):
            c = random.choice(colors)
            while c in gen_colors:
                c = random.choice(colors)
            gen_colors.append(c)
    else:
        for i in range(shapes_count):
            gen_colors.append(random.choice(colors))
    return gen_colors

for concept in concepts:
    for shape1_IDX in range(len(shapes)):
        if concept != "ALONE":
            for shape2_IDX in range(shape1_IDX, len(shapes)):
                generate_group(shapes[shape1_IDX], shapes[shape2_IDX], concept)
        else:
            generate_single(shapes[shape1_IDX])