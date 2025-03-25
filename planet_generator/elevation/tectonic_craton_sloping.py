# planet_generator/elevation/tectonic_craton_sloping.py

import numpy as np
from planet_generator import config
from .utils import get_height_amplitude


# TODO: Change the slope method from center-to-edge to edge-based-inward gradients (which I hope will create foothill
#       ridges).
def slope_craton_centers(vertices, faces, face_centers, assigned, plate_types, face_elevations, adjacency):
    """
    Applies an inward-to-outward elevation gradient within each craton.

    Continental plates slope down toward their edges (mountain-to-plain).
    Oceanic plates slope up toward their edges (deep ocean to shallows).

    Nearby mountains and trenches modify the base slope slightly,
    adding variation near strong features.

    Args:
        vertices (np.ndarray): Vertex positions.
        faces (list[tuple[int]]): Face definitions.
        face_centers (np.ndarray): Precomputed unit vectors representing face centers.
        assigned (list[int]): Craton ID assigned per face.
        plate_types (dict[int, str]): Craton type per seed ID.
        face_elevations (list[float]): Elevation values to modify in-place.
        adjacency (dict[int, list[int]]): Face adjacency map.
    """
    if config.debug_mode:
        print("[DEBUG] Slope-craton-center elevation pass...")

    height_amplitude = get_height_amplitude()

    craton_faces = {}
    for i, cid in enumerate(assigned):
        if cid not in craton_faces:
            craton_faces[cid] = []
        craton_faces[cid].append(i)

    for craton_id, face_indices in craton_faces.items():
        if not face_indices:
            continue
        centers = face_centers[face_indices]
        plate_center = np.mean(centers, axis=0)

        for i in face_indices:
            face_center = face_centers[i]
            dist = np.linalg.norm(plate_center - face_center)
            dist_weight = dist / config.radius

            plate_type = plate_types.get(craton_id, "continental")
            if plate_type == "oceanic":
                slope = -height_amplitude * 0.4 * (1 - dist_weight)  # slope UP to shore
            else:
                slope = height_amplitude * 0.2 * (1 - dist_weight)  # slope DOWN to shore

            # Optional: adjust slope based on nearby extremes (mountains/trenches)
            mountain_thresh = 0.6 * height_amplitude
            trench_thresh = -0.6 * height_amplitude
            max_search_depth = 3
            visited = set()
            frontier = {i}
            for _ in range(max_search_depth):
                next_frontier = set()
                for f in frontier:
                    for neighbor in adjacency[f]:
                        if neighbor in visited or assigned[neighbor] != craton_id:
                            continue
                        elev = face_elevations[neighbor]
                        if elev >= mountain_thresh:
                            slope += height_amplitude * 0.01
                        elif elev <= trench_thresh:
                            slope -= height_amplitude * 0.01
                        next_frontier.add(neighbor)
                        visited.add(neighbor)
                frontier = next_frontier

            face_elevations[i] += slope


def normalize_elevations(face_elevations):
    """
    Rescales elevation values to the range [-height_amplitude, +height_amplitude],
    preserving proportional differences and biasing toward sea level (0.0).

    Args:
        face_elevations (list[float]): Elevation values to normalize.

    Returns:
        list[float]: Normalized elevation values.
    """
    if config.debug_mode:
        print("[DEBUG] Normalizing face elevations...")

    height_amplitude = get_height_amplitude()
    elev_array = np.array(face_elevations)
    min_elev = elev_array.min()
    max_elev = elev_array.max()

    if min_elev == max_elev:
        return elev_array.tolist()  # avoid divide-by-zero

    # Normalize to range [-1, 1], centered at 0, then bias upward toward sea-level
    scaled = 2 * (elev_array - min_elev) / (max_elev - min_elev) - 1
    scaled += 0.15  # bias toward raising average continental elevation
    scaled = np.clip(scaled, -1, 1)
    normalized = scaled * height_amplitude

    return normalized.tolist()
