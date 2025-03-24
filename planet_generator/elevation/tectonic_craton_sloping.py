# planet_generator/elevation/tectonic_craton_sloping.py

import numpy as np
from planet_generator import config


# TODO: Instead of computing the face-centers multiple times, use the pre-computed face_centers that you should have
#       cached from the apply_boundary_interactions function.
# TODO: Change the slope method from center-to-edge to edge-based-inward gradients (which I hope will create foothill
#       ridges).
def slope_craton_centers(vertices, faces, assigned, plate_types, face_elevations, adjacency):
    """
    Applies an inward-to-outward elevation gradient within each craton.

    Continental plates slope down toward their edges (mountain-to-plain).
    Oceanic plates slope up toward their edges (deep ocean to shallows).

    Nearby mountains and trenches modify the base slope slightly,
    adding variation near strong features.

    Args:
        vertices (np.ndarray): Vertex positions.
        faces (list[tuple[int]]): Face definitions.
        assigned (list[int]): Craton ID assigned per face.
        plate_types (dict[int, str]): Craton type per seed ID.
        face_elevations (list[float]): Elevation values to modify in-place.
        adjacency (dict[int, list[int]]): Face adjacency map.
    """
    if config.debug_mode:
        print("[DEBUG] Slope-craton-center elevation pass...")

    craton_faces = {}
    for i, cid in enumerate(assigned):
        if cid not in craton_faces:
            craton_faces[cid] = []
        craton_faces[cid].append(i)

    for craton_id, face_indices in craton_faces.items():
        if not face_indices:
            continue
        centers = [np.mean(vertices[np.array(faces[i])], axis=0) for i in face_indices]
        plate_center = np.mean(centers, axis=0)

        for i in face_indices:
            face_center = np.mean(vertices[np.array(faces[i])], axis=0)
            dist = np.linalg.norm(plate_center - face_center)
            dist_weight = dist / config.radius

            plate_type = plate_types.get(craton_id, "continental")
            if plate_type == "oceanic":
                slope = -config.height_amplitude * 0.4 * (1 - dist_weight)  # slope UP to shore
            else:
                slope = config.height_amplitude * 0.2 * (1 - dist_weight)  # slope DOWN to shore

            # Optional: adjust slope based on nearby extremes (mountains/trenches)
            mountain_thresh = 0.6 * config.height_amplitude
            trench_thresh = -0.6 * config.height_amplitude
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
                            slope += config.height_amplitude * 0.01
                        elif elev <= trench_thresh:
                            slope -= config.height_amplitude * 0.01
                        next_frontier.add(neighbor)
                        visited.add(neighbor)
                frontier = next_frontier

            face_elevations[i] += slope
