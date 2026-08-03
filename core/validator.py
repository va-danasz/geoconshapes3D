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
    depths = []
    for mesh1 in range(len(current_meshes)):
        for mesh2 in range(mesh1 + 1, len(current_meshes)):
            depths.append(get_overlap_depth(current_meshes[mesh1], current_meshes[mesh2]))
    return any(d > 1.0 for d in depths)

def validate_close(current_meshes: Sequence[trimesh.Trimesh]) -> bool:
    distances = []
    for mesh1 in range(len(current_meshes)):
        for mesh2 in range(mesh1 + 1, len(current_meshes)):
            distances.append(get_min_distance(current_meshes[mesh1], current_meshes[mesh2]))
    return all(config.CLOSE_THRESHOLD[0] <= d <= config.CLOSE_THRESHOLD[1] for d in distances)

def validate_far(current_meshes: Sequence[trimesh.Trimesh]) -> bool:
    distances = []
    for mesh1 in range(len(current_meshes)):
        for mesh2 in range(mesh1 + 1, len(current_meshes)):
            distances.append(get_min_distance(current_meshes[mesh1], current_meshes[mesh2]))
    return all(config.FAR_THRESHOLD[0] <= d <= config.FAR_THRESHOLD[1] for d in distances)


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