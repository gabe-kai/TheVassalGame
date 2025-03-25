# planet_generator/elevation/tectonic_craton_sloping.py

import numpy as np
from collections import deque
from planet_generator import config
from .utils import get_height_amplitude


def slope_craton_centers(face_centers, assigned, plate_types, face_elevations, adjacency):
    """
    Applies an edge-inward elevation gradient within each craton.

    Continental plates slope upward from edges toward the interior (creating inland ridges and mountains).
    Oceanic plates slope downward from edges toward the interior (creating deep sea basins).

    Nearby mountains and trenches modify the base slope slightly,
    adding variation near strong features.

    Args:
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

        plate_type = plate_types.get(craton_id, "continental")

        # Step 1: Detect edge faces
        edge_faces = [
            i for i in face_indices
            if any(assigned[n] != craton_id for n in adjacency[i])
        ]

        # Step 2: BFS from edge inward
        distances = {i: np.inf for i in face_indices}
        queue = deque()
        for face in edge_faces:
            distances[face] = 0
            queue.append(face)

        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor in distances and distances[neighbor] > distances[current] + 1:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        max_dist = max(distances.values()) or 1

        # Bias slope strength by plate size
        face_count = len(face_indices)
        size_scale = np.clip(1.0 / np.sqrt(face_count), 0.4, 1.0)  # Smaller plates = larger value

        # Seed RNG with craton ID for consistent randomness per plate
        rng = np.random.default_rng(craton_id)
        slope_strength = rng.uniform(0.05, 0.15) * size_scale  # variability for more natural shapes

        for i in face_indices:
            # Nonlinear falloff: sharper slope at edge, smoother center
            raw_weight = 1.0 - (distances[i] / max_dist)
            dist_weight = raw_weight ** 2

            if plate_type == "oceanic":
                base = -0.25 * height_amplitude
                slope = -0.2 * height_amplitude * dist_weight
            else:
                base = 0.2 * height_amplitude
                # Inverted slope direction: raise interior more than edge
                slope = slope_strength * height_amplitude * (1.0 - dist_weight)

                # Flatten the central interior slightly
                if dist_weight < 0.05:
                    slope *= 0.5

                # Soften shorelines to prevent cliffy edges
                if dist_weight > 0.95:
                    slope = min(slope, 0.0)

            # Adjust slope based on nearby extremes (mountains/trenches)
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

            face_elevations[i] += base + slope


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

    # Normalize to range [-1, 1], centered at 0, then bias toward sea-level
    scaled = 2 * (elev_array - min_elev) / (max_elev - min_elev) - 1
    scaled = np.clip(scaled, -1, 1)
    normalized = scaled * height_amplitude

    return normalized.tolist()
