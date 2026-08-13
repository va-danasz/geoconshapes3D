import random
import shutil
from typing import Sequence
import config
from core import mesh, scene, validator
import os

def generate_group(shapes: Sequence[str], conc: str):
    for i in range(config.SAMPLE_COUNT):
        valid = False
        validation_count = 0
        current_meshes = []

        while not valid and validation_count < config.MAX_VALIDATIONS:
            current_meshes = []
            validation_count += 1
            for j in range(len(shapes)):
                current_meshes.append(mesh.get_mesh(shapes[j]))
            valid = validator.validate(current_meshes, conc)

        if valid:
            scene.render_shapes(current_meshes, shapes, gen_color_list(len(shapes)), conc, i)
        else:
            print(f"Unable to generate group with concept {conc}")

def generate_single(shape: str):
    for i in range(config.SAMPLE_COUNT):
        mesh_single = mesh.get_mesh(shape)
        scene.render_shape(mesh_single, shape, random.choice(config.COLORS), i)

def gen_color_list(shapes_count: int) -> Sequence[str]:
    gen_colors = []
    if shapes_count <= len(config.COLORS):
        for i in range(shapes_count):
            c = random.choice(config.COLORS)
            while c in gen_colors:
                c = random.choice(config.COLORS)
            gen_colors.append(c)
    else:
        for i in range(shapes_count):
            gen_colors.append(random.choice(config.COLORS))
    return gen_colors


if os.path.exists(config.OUTPUT_PATH):
    shutil.rmtree(config.OUTPUT_PATH)
random.seed(config.SEED)
for concept in config.CONCEPTS:
    for shape1_IDX in range(len(config.SHAPES)):
        if concept != "ALONE":
            for shape2_IDX in range(shape1_IDX, len(config.SHAPES)):
                generate_group([config.SHAPES[shape1_IDX], config.SHAPES[shape2_IDX]], concept)
        else:
            generate_single(config.SHAPES[shape1_IDX])