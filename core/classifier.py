# classifier.py
import numpy as np
import math
import pyvista as pv
from scipy import ndimage
from typing import Sequence
import config


def get_silhouette_mask(plotter: pv.Plotter, actors: Sequence, visible_index: int) -> np.ndarray:
    for i, actor in enumerate(actors):
        actor.visibility = (i == visible_index)
    plotter.render()
    img = plotter.screenshot(transparent_background=True, return_img=True)
    for actor in actors:
        actor.visibility = True
    return img[:, :, 3] > 0


def mask_min_distance(mask_a: np.ndarray, mask_b: np.ndarray) -> float:
    if not mask_a.any() or not mask_b.any():
        return math.hypot(config.IMG_W, config.IMG_H)
    dist_field = ndimage.distance_transform_edt(~mask_a)
    return float(dist_field[mask_b].min())


def classify_2d(actors: Sequence, plotter: pv.Plotter) -> tuple[str, float | None]:
    if len(actors) == 1:
        return "ALONE", None

    mask_a = get_silhouette_mask(plotter, actors, 0)
    mask_b = get_silhouette_mask(plotter, actors, 1)
    plotter.render()

    if np.any(mask_a & mask_b):
        return "OVERLAP", 0.0

    dist_px = mask_min_distance(mask_a, mask_b)
    dist_norm = dist_px / math.hypot(config.IMG_W, config.IMG_H)

    concept = "CLOSE" if dist_norm <= config.THRESHOLD_2D_CLOSE_FAR else "FAR"
    return concept, dist_norm