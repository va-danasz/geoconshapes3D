import random
import shutil
import os
from typing import Sequence
import config
from core import mesh, scene, validator
from core.labels import Concept, Shape, Color

def generate_group(shapes: Sequence[Shape], conc: Concept):
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

def generate_single(shape: Shape):
    for i in range(config.SAMPLE_COUNT):
        mesh_single = mesh.get_mesh(shape)
        scene.render_shape(mesh_single, shape, random.choice(COLORS), i)

def gen_color_list(shapes_count: int) -> list[Color]:
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


if os.path.exists(config.OUTPUT_PATH):
    shutil.rmtree(config.OUTPUT_PATH)
random.seed(config.SEED)
print("Generating shapes...")
CONCEPTS = list(Concept)
SHAPES = list(Shape)
COLORS = list(Color)
for concept in CONCEPTS:
    for shape1_IDX in range(len(SHAPES)):
        if concept != Concept.ALONE:
            for shape2_IDX in range(shape1_IDX, len(SHAPES)):
                generate_group([SHAPES[shape1_IDX], SHAPES[shape2_IDX]], concept)
        else:
            generate_single(SHAPES[shape1_IDX])