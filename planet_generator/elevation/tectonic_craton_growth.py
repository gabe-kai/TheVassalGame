# planet_generator/elevation/tectonic_craton_growth.py

from planet_generator import config
from collections import deque


def grow_cratons(faces, craton_seeds, adjacency, plate_types, face_elevations):
    """
    Orchestrates craton growth by selecting the configured method.

    Args:
        faces (list[tuple[int]]): Triangle face definitions.
        craton_seeds (list[int]): Seed face indices.
        adjacency (dict[int, list[int]]): Neighbor relationships between faces.
        plate_types (dict[int, str]): Mapping of craton seed to plate type.
        face_elevations (list[float]): Elevation array to update.

    Returns:
        list[int]: Craton ID assigned to each face.
    """
    base_elevations = compute_base_elevations(craton_seeds, plate_types)

    method = config.craton_growth_method.lower()
    if method == "bfs":
        return grow_cratons_bfs(faces, craton_seeds, adjacency, face_elevations, base_elevations)
    else:
        raise ValueError(f"Unsupported craton growth method: '{method}'")


def compute_base_elevations(craton_seeds, plate_types):
    """
    Computes the base elevation for each craton seed based on plate type.

    Args:
        craton_seeds (list[int]): List of seed face indices.
        plate_types (dict[int, str]): Mapping from craton seed to plate type.

    Returns:
        dict[int, float]: Mapping from craton seed to its base elevation.
    """
    return {
        cid: (-config.height_amplitude * 0.4 if plate_types[cid] == "oceanic" else config.height_amplitude * 0.1)
        for cid in craton_seeds
    }


def grow_cratons_bfs(faces, craton_seeds, adjacency, face_elevations, base_elevations):
    """
    Expands each craton from its seed using breadth-first search (BFS).

    Assigns all reachable faces to the same craton ID.
    Also sets an initial base elevation on each face during growth,
    depending on whether the craton is oceanic or continental.

    Args:
        faces (list[tuple[int]]): Triangle face definitions.
        craton_seeds (list[int]): Seed face indices.
        adjacency (dict[int, list[int]]): Neighbor relationships between faces.
        face_elevations (list[float]): Elevation array to update.
        base_elevations (dict[int, float]): Elevation base values per craton.

    Returns:
        list[int]: Craton ID assigned to each face (same as seed ID).
    """
    if config.debug_mode:
        print("[DEBUG] Growing cratons using BFS (breadth-first search)...")

    total_faces = len(faces)
    assigned_craton_faces = [-1] * total_faces
    queues = {seed: deque([seed]) for seed in craton_seeds}

    for seed in craton_seeds:
        assigned_craton_faces[seed] = seed
        face_elevations[seed] = base_elevations[seed]

    active = True
    while active:
        active = False
        for craton_id, queue in queues.items():
            if not queue:
                continue
            face = queue.popleft()
            for neighbor in adjacency[face]:
                if assigned_craton_faces[neighbor] == -1:
                    assigned_craton_faces[neighbor] = craton_id
                    queue.append(neighbor)
                    active = True
                    face_elevations[neighbor] = base_elevations[craton_id]

    if config.debug_mode:
        unassigned_indices = [i for i, c in enumerate(assigned_craton_faces) if c == -1]
        print(f"[DEBUG] Unassigned face count: {len(unassigned_indices)}")
        if unassigned_indices:
            some_face = unassigned_indices[0]
            print(f"[DEBUG] Example unassigned face: {some_face}")
            print(f"[DEBUG] Its neighbors: {adjacency[some_face]}")
            for nbr in adjacency[some_face]:
                print(f"    neighbor={nbr}, assigned_craton_faces[{nbr}]={assigned_craton_faces[nbr]}")

    if config.debug_mode:
        # Pick a sample face from craton seeds for symmetric adjacency check
        some_face = craton_seeds[0] if craton_seeds else 0
        for nbr in adjacency.get(some_face, []):
            if some_face not in adjacency.get(nbr, []):
                print(f"[DEBUG] Asymmetric adjacency: Face {nbr} doesn't list {some_face} as neighbor!")

    return assigned_craton_faces
