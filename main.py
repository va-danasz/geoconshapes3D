from core import mesh, scene

IMG_W, IMG_H = 500, 500
SAMPLE_COUNT = 1
concepts = ["ALONE", "FAR", "CLOSE", "OVERLAP"]
shapes = ["CUBE", "SPHERE", "CONE"]
colors = ["red", "green", "blue"]


def generate_group(s1, s2, c):
    for i in range(SAMPLE_COUNT):
        print(f"{s1} - {s2} [{c}]")

for shape1_IDX in range(len(shapes)):
    for shape2_IDX in range(shape1_IDX, len(shapes)):
        for concept in concepts:
            generate_group(shapes[shape1_IDX], shapes[shape2_IDX], concept)

cube = mesh.generate_cube()
sphere = mesh.generate_sphere(size=5)
cone = mesh.generate_cone(radius=5, height=8)

scene.show_shape(cube)
scene.show_shape(sphere, colors[0])
scene.show_shape(cone, colors[1])