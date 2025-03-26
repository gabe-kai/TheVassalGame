# planet_generator/elevation/__init__.py

from planet_generator import config

from .perlin import compute_perlin_elevation
from .tectonic import compute_tectonic_elevation


def select_elevation_method(vertices, faces, face_centers, adjacency=None):
    """
    Dispatches to the correct elevation method based on config.elevation_method.
    Returns:
        - face_elevations: list of elevation values per face
        - assigned: face-to-craton ID map (or None)
        - motion_vectors: craton motion vectors (or None)
    """
    if config.elevation_method == "perlin":
        face_elevations = compute_perlin_elevation(vertices, faces)
        return face_elevations, None, None

    elif config.elevation_method == "tectonic":
        return compute_tectonic_elevation(vertices, faces, face_centers, adjacency)

    else:
        raise ValueError(f"Unknown elevation method: {config.elevation_method}")
