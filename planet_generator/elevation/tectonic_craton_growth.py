# planet_generator/elevation/tectonic_craton_growth.py

from planet_generator import config
from collections import deque
import numpy as np
from noise import snoise3  # Simplex noise for smooth spatial distortion


def grow_cratons(faces, craton_seeds, adjacency, plate_types, face_elevations, vertices):
    """
    Orchestrates craton growth by selecting the configured method.

    Args:
        faces (list[tuple[int]]): Triangle face definitions.
        craton_seeds (list[int]): Seed face indices.
        adjacency (dict[int, list[int]]): Neighbor relationships between faces.
        plate_types (dict[int, str]): Mapping of craton seed to plate type.
        face_elevations (list[float]): Elevation array to update.
        vertices (np.ndarray): Array of vertex coordinates.

    Returns:
        list[int]: Craton ID assigned to each face.
    """
    base_elevations = compute_base_elevations(craton_seeds, plate_types)

    method = config.craton_growth_method.lower()
    if method == "bfs":
        return grow_cratons_bfs(faces, craton_seeds, adjacency, face_elevations, base_elevations)
    elif method == "voronoi":
        return grow_cratons_voronoi(faces, craton_seeds, face_elevations, base_elevations, vertices)
    else:
        raise ValueError(f"Unsupported craton growth method: '{method}'")


def compute_base_elevations(craton_seeds, plate_types):
    return {
        cid: (-config.height_amplitude * 0.4 if plate_types[cid] == "oceanic" else config.height_amplitude * 0.1)
        for cid in craton_seeds
    }


def grow_cratons_bfs(faces, craton_seeds, adjacency, face_elevations, base_elevations):
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
        some_face = craton_seeds[0] if craton_seeds else 0
        for nbr in adjacency.get(some_face, []):
            if some_face not in adjacency.get(nbr, []):
                print(f"[DEBUG] Asymmetric adjacency: Face {nbr} doesn't list {some_face} as neighbor!")

    return assigned_craton_faces


def grow_cratons_voronoi(faces, craton_seeds, face_elevations, base_elevations, vertices):
    if config.debug_mode:
        print("[DEBUG] Growing cratons using Voronoi method with simplex distortion...")

    face_centers = np.mean(vertices[np.array(faces)], axis=1)
    face_centers /= np.linalg.norm(face_centers, axis=1, keepdims=True)

    seed_centers = face_centers[craton_seeds]  # shape (num_seeds, 3)
    dot_products = np.dot(face_centers, seed_centers.T)  # (num_faces, num_seeds)

    # Coherent simplex noise-based distortion per (face, seed) pair
    distortion = np.zeros_like(dot_products)
    for seed_idx, seed_center in enumerate(seed_centers):
        dx, dy, dz = seed_center * 2.0  # Tuned frequency multiplier
        for face_idx, (x, y, z) in enumerate(face_centers):
            distortion[face_idx, seed_idx] = snoise3(x + dx, y + dy, z + dz)

    # Optionally apply weights to seeds for variable plate influence
    seed_weights = np.random.uniform(0.8, 1.2, size=len(craton_seeds))  # Random weights per seed
    weighted_scores = dot_products * seed_weights[None, :]

    # Blend distorted score into weighted dot products
    noisy_scores = weighted_scores + distortion * 0.05

    closest_indices = np.argmax(noisy_scores, axis=1)
    assigned_craton_faces = [craton_seeds[i] for i in closest_indices]

    for i, craton_id in enumerate(assigned_craton_faces):
        face_elevations[i] = base_elevations[craton_id]

    return assigned_craton_faces
