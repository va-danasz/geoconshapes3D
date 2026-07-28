import trimesh
from typing import Sequence
import config

def get_min_distance(mesh1: trimesh.Trimesh, mesh2: trimesh.Trimesh) -> float:
    manager = trimesh.collision.CollisionManager()
    manager.add_object('m1', mesh1)
    min_distance = manager.min_distance_single(mesh2)
    return min_distance

def get_overlap_depth(mesh1: trimesh.Trimesh, mesh2: trimesh.Trimesh) -> float:
    manager = trimesh.collision.CollisionManager()
    manager.add_object('m1', mesh1)

    is_colliding, contacts = manager.in_collision_single(mesh2, return_names=False, return_data=True)

    if not is_colliding:
        return 0.0

    max_depth = max(c.depth for c in contacts)
    return max_depth

def validate_overlap(current_meshes: Sequence[trimesh.Trimesh]) -> bool:
    overlap_depth = 0
    for mesh1 in range(len(current_meshes)):
        for mesh2 in range(mesh1 + 1, len(current_meshes)):
            overlap_depth = get_overlap_depth(current_meshes[mesh1], current_meshes[mesh2])
    return overlap_depth > 1.0

def validate_close(current_meshes: Sequence[trimesh.Trimesh]) -> bool:
    distance = 0
    for mesh1 in range(len(current_meshes)):
        for mesh2 in range(mesh1 + 1, len(current_meshes)):
            distance = get_min_distance(current_meshes[mesh1], current_meshes[mesh2])
    return 0 < distance < config.CLOSE_THRESHOLD

def validate_far(current_meshes: Sequence[trimesh.Trimesh]) -> bool:
    distance = 0
    for mesh1 in range(len(current_meshes)):
        for mesh2 in range(mesh1 + 1, len(current_meshes)):
            distance = get_min_distance(current_meshes[mesh1], current_meshes[mesh2])
    return distance >= config.FAR_THRESHOLD


def validate(current_meshes: Sequence[trimesh.Trimesh], concept: str) -> bool:
    valid = False
    match concept:
        case "OVERLAP":
            valid = validate_overlap(current_meshes)
        case "CLOSE":
            valid = validate_close(current_meshes)
        case "FAR":
            valid = validate_far(current_meshes)
        case _:
            valid = False
    return valid