from typing import TypedDict
from core.labels import Concept
class MeshMetaData(TypedDict):
    id: str
    concept: Concept
    img_width: int
    img_height: int
    object_id: int
    object_name: str
    object_pos_x: float
    object_pos_y: float
    object_pos_z: float
    width: float | None
    length: float | None
    height: float | None
    radius: float | None
    cone_sides: int | None
    bbox_size_x: float
    bbox_size_y: float
    bbox_size_z: float
    color: str | None
    texture_name: str | None
    background_name: str | None

class RenderMetaData(TypedDict):
    mesh_id: str
    image_name: str
    cam_pos_x: float
    cam_pos_y: float
    cam_pos_z: float
    view_angle: float
    target_x: float
    target_y: float
    target_z: float
    concept_2d: Concept
    dist_norm: float | None