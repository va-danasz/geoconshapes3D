import random
import shutil
import os
from typing import Sequence
import config
from core import mesh, scene, validator
from core.labels import Concept, Shape, Color

def generate_group(shapes: Sequence[Shape], conc: Concept, on_step=None):
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
        if on_step:
            on_step()

def generate_single(shape: Shape, on_step=None):
    for i in range(config.SAMPLE_COUNT):
        mesh_single = mesh.get_mesh(shape)
        scene.render_shape(mesh_single, shape, random.choice(COLORS), i)
        if on_step:
            on_step()

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

def print_progress(done: int, total: int):
    BAR_WIDTH = 50
    filled = round(done / total * BAR_WIDTH)
    bar = "■" * filled + "□" * (BAR_WIDTH - filled)
    percent = round(done / total * 100)
    print(f"\r{bar} {percent}%", end="", flush=True)

def step():
    global done_steps
    done_steps += 1
    print_progress(done_steps, total_steps)

if os.path.exists(config.OUTPUT_PATH):
    shutil.rmtree(config.OUTPUT_PATH)
random.seed(config.SEED)
CONCEPTS = list(Concept)
SHAPES = list(Shape)
COLORS = list(Color)

print("Generating shapes...")
print(f"Total image count: {21 * config.SAMPLE_COUNT*(config.RENDER_COUNT+(6 if config.ENABLE_DIRECTIONS else 0))}")
total_steps = (len(SHAPES) + ((len(CONCEPTS)-1) * (len(SHAPES)*(len(SHAPES)-1)))) * config.SAMPLE_COUNT
done_steps = 0

print_progress(0, total_steps)
for concept in CONCEPTS:
    for shape1_IDX in range(len(SHAPES)):
        if concept != Concept.ALONE:
            for shape2_IDX in range(shape1_IDX, len(SHAPES)):
                generate_group([SHAPES[shape1_IDX], SHAPES[shape2_IDX]], concept, step)
        else:
            generate_single(SHAPES[shape1_IDX], step)
print()