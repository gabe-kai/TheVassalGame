# planet_generator/elevation/tectonic_craton_growth.py

from planet_generator import config
from collections import deque


# TODO: Change the recompute of base_elevation for every propagated neighbor from being inside the loop
#       to a precompute outside the loop that runs once and stores the results in a dict.
# TODO: some_face = 0 assumes that face 0 exists. Change it to sample a face from craton_seeds instead.
def grow_cratons(faces, craton_seeds, adjacency, plate_types, face_elevations):
    """
    Expands each craton from its seed using breadth-first search (BFS).

    Assigns all reachable faces to the same craton ID.
    Also sets an initial base elevation on each face during growth,
    depending on whether the craton is oceanic or continental.

    Args:
        faces (list[tuple[int]]): Triangle face definitions.
        craton_seeds (list[int]): Seed face indices.
        adjacency (dict[int, list[int]]): Neighbor relationships between faces.
        plate_types (dict[int, str]): Mapping of craton seed to plate type.
        face_elevations (list[float]): Elevation array to update.

    Returns:
        list[int]: Craton ID assigned to each face (same as seed ID).
    """
    if config.debug_mode:
        print("[DEBUG] Growing cratons...")

    total_faces = len(faces)
    assigned_craton_faces = [-1] * total_faces
    queues = {seed: deque([seed]) for seed in craton_seeds}
    for seed in craton_seeds:
        assigned_craton_faces[seed] = seed
        base_elevation = -config.height_amplitude * 0.3 if plate_types[seed] == "oceanic" else config.height_amplitude * 0.1
        face_elevations[seed] = base_elevation

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
                    # Propagate base elevation
                    base_elevation = -config.height_amplitude * 0.4 if plate_types[craton_id] == "oceanic" else config.height_amplitude * 0.1
                    face_elevations[neighbor] = base_elevation

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
        some_face = 0
        for nbr in adjacency[some_face]:
            if some_face not in adjacency[nbr]:
                print(f"[DEBUG] Asymmetric adjacency: Face {nbr} doesn't list {some_face} as neighbor!")

    return assigned_craton_faces
