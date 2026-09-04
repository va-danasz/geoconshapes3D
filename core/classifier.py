import numpy as np
import numpy.typing as npt
import math
import pyvista as pv
from pyvista import Actor
from scipy import ndimage
import config
from core.labels import Concept


def get_silhouette_mask(plotter: pv.Plotter, actors: list[Actor], visible_index: int) -> npt.NDArray[np.bool_]:
    for i, actor in enumerate(actors):
        actor.visibility = (i == visible_index)
    plotter.render()
    img = plotter.screenshot(transparent_background=True, return_img=True)
    for actor in actors:
        actor.visibility = True
    assert img is not None, "screenshot() returned None, plotter not rendering"
    return img[:, :, 3] > 0


def mask_min_distance(mask_a: npt.NDArray[np.bool_], mask_b: npt.NDArray[np.bool_]) -> float:
    if not mask_a.any() or not mask_b.any():
        return math.hypot(config.IMG_W, config.IMG_H)
    dist_field = ndimage.distance_transform_edt(~mask_a)
    return float(dist_field[mask_b].min())


def classify_2d(actors: list[Actor], plotter: pv.Plotter) -> tuple[Concept, float | None]:
    if len(actors) == 1:
        return Concept.ALONE, None

    mask_a = get_silhouette_mask(plotter, actors, 0)
    mask_b = get_silhouette_mask(plotter, actors, 1)
    plotter.render()

    if np.any(mask_a & mask_b):
        return Concept.OVERLAP, 0.0

    dist_px = mask_min_distance(mask_a, mask_b)
    dist_norm = dist_px / math.hypot(config.IMG_W, config.IMG_H)

    concept = Concept.CLOSE if dist_norm <= config.THRESHOLD_2D_CLOSE_FAR else Concept.FAR
    return concept, dist_norm