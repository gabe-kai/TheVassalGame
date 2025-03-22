# planet_generator/elevation/tectonic.py

import math
import numpy as np
from collections import deque
from planet_generator import config


def compute_tectonic_elevation(vertices, faces):
    """
    Simulates tectonic elevation changes using craton seeding, motion vectors,
    boundary interactions, and smoothing.
    Returns:
        - face_elevations: list of elevation values per face
        - assigned: list of craton ID for each face
        - motion_vectors: dict of craton_id to motion vector
    """
    if config.debug_mode:
        print("[DEBUG] Starting tectonic elevation computation...")

    total_faces = len(faces)
    surface_area_km2 = 4 * math.pi * config.radius**2
    estimated_craton_count = config.craton_count or max(8, int(surface_area_km2 / 8e7))
    rng = np.random.default_rng(config.qi_pool_seed)

    if config.debug_mode:
        print("[DEBUG] Seeding cratons...")
    craton_seeds = seed_cratons(total_faces, estimated_craton_count, rng)
    if config.debug_mode:
        print("[DEBUG] Building adjacency map...")
    adjacency = build_adjacency(faces)
    if config.debug_mode:
        print("[DEBUG] Growing cratons...")
    assigned = grow_cratons(faces, craton_seeds, adjacency)
    if config.debug_mode:
        print("[DEBUG] Assigning oceanic cratons...")
    oceanic_cratons = assign_oceanic_cratons(estimated_craton_count, rng)
    if config.debug_mode:
        print("[DEBUG] Assigning motion vectors...")
    motion_vectors = assign_motion_vectors(estimated_craton_count, rng)

    if config.debug_mode:
        print("[DEBUG] Applying boundary interactions...")
    face_elevations = [0.0 for _ in faces]
    apply_boundary_interactions(vertices, faces, adjacency, assigned, motion_vectors, face_elevations, rng)
    if config.debug_mode:
        print("[DEBUG] Smoothing elevation boundaries...")
    smooth_boundaries(faces, adjacency, face_elevations)
    if config.debug_mode:
        print("[DEBUG] Applying ocean basin adjustments...")
    apply_ocean_basins(assigned, oceanic_cratons, face_elevations)
    if config.debug_mode:
        print("[DEBUG] Slope-craton-center elevation pass...")
    slope_craton_centers(vertices, faces, assigned, oceanic_cratons, face_elevations, adjacency)

    return face_elevations, assigned, motion_vectors


# --- Helper Functions ---

def seed_cratons(total_faces, count, rng):
    return rng.choice(total_faces, size=count, replace=False)


def build_adjacency(faces):
    adjacency = {i: set() for i in range(len(faces))}
    vertex_to_faces = {}
    for i, tri in enumerate(faces):
        for v in tri:
            vertex_to_faces.setdefault(v, set()).add(i)
    for i, tri in enumerate(faces):
        neighbors = set()
        for v in tri:
            neighbors.update(vertex_to_faces[v])
        neighbors.discard(i)
        adjacency[i] = neighbors
    return adjacency


def grow_cratons(faces, craton_seeds, adjacency):
    total_faces = len(faces)
    assigned = [-1] * total_faces
    queues = [deque([seed]) for seed in craton_seeds]
    for idx, seed in enumerate(craton_seeds):
        assigned[seed] = idx

    active = True
    while active:
        active = False
        for craton_id, queue in enumerate(queues):
            if not queue:
                continue
            face = queue.popleft()
            for neighbor in adjacency[face]:
                if assigned[neighbor] == -1:
                    assigned[neighbor] = craton_id
                    queue.append(neighbor)
                    active = True
    return assigned


def assign_oceanic_cratons(count, rng):
    num_oceanic = int(count * config.oceanic_craton_fraction)
    oceanic = set(rng.choice(count, size=num_oceanic, replace=False))
    if config.debug_mode:
        print(f"[DEBUG] Oceanic cratons: {sorted(oceanic)}")
    return oceanic


def assign_motion_vectors(count, rng):
    vectors = {}
    for craton_id in range(count):
        vec = rng.normal(size=3)
        vec /= np.linalg.norm(vec)
        vectors[craton_id] = vec
    if config.debug_mode:
        for cid, vec in vectors.items():
            print(f"[DEBUG] Craton {cid} motion vector: ({vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f})")
    return vectors


def apply_boundary_interactions(vertices, faces, adjacency, assigned, motion_vectors, face_elevations, rng):
    converging_lift = config.height_amplitude * 0.75
    diverging_trench = -config.height_amplitude * 0.5
    transform_variation = config.height_amplitude * 0.1
    threshold = 0.1
    debug_count = 0

    for face_idx, neighbors in adjacency.items():
        for neighbor_idx in neighbors:
            plate_a = assigned[face_idx]
            plate_b = assigned[neighbor_idx]
            if plate_a == -1 or plate_b == -1 or plate_a == plate_b:
                continue

            pos_a = np.mean(vertices[faces[face_idx]], axis=0)
            pos_b = np.mean(vertices[faces[neighbor_idx]], axis=0)
            direction = pos_b - pos_a
            if np.linalg.norm(direction) == 0:
                continue
            direction /= np.linalg.norm(direction)

            vec_a = motion_vectors[plate_a]
            vec_b = motion_vectors[plate_b]
            relative_motion = np.dot(vec_b - vec_a, direction)

            interaction = "transform"
            if relative_motion > threshold:
                interaction = "diverging"
            elif relative_motion < -threshold:
                interaction = "converging"

            if interaction == "converging":
                face_elevations[face_idx] += converging_lift
                face_elevations[neighbor_idx] += converging_lift
            elif interaction == "diverging":
                face_elevations[face_idx] += diverging_trench
                face_elevations[neighbor_idx] += diverging_trench
            elif interaction == "transform":
                noise = rng.uniform(-transform_variation, transform_variation)
                face_elevations[face_idx] += noise
                face_elevations[neighbor_idx] += noise

            if config.debug_mode and debug_count < 20:
                print(f"[DEBUG] Face {face_idx} ↔ {neighbor_idx}: {interaction.upper()} (Δv • dir = {relative_motion:.3f})")
                debug_count += 1


def smooth_boundaries(faces, adjacency, face_elevations):
    """
    Spreads elevation outward from boundary zones using layered smoothing.
    This version avoids spreading from very high elevation (mountain) peaks,
    to preserve sharp summits while allowing wide foothill regions.
    """
    max_smoothing_layers = 6
    decay_factor = 0.07
    total_faces = len(faces)
    influence = [0.0] * total_faces
    visited = [False] * total_faces

    initial_frontier = [i for i, e in enumerate(face_elevations) if e != 0.0]
    for i in initial_frontier:
        visited[i] = True
        influence[i] = face_elevations[i]

    current_frontier = set(initial_frontier)
    for layer in range(1, max_smoothing_layers + 1):
        next_frontier = set()
        for face in current_frontier:
            for neighbor in adjacency[face]:
                if not visited[neighbor]:
                    # Skip spreading from high peaks to preserve sharp mountains
                    if abs(face_elevations[face]) > 0.8 * config.height_amplitude:
                        continue
                    falloff = decay_factor ** layer
                    influence[neighbor] += face_elevations[face] * falloff
                    next_frontier.add(neighbor)
                    visited[neighbor] = True
        current_frontier = next_frontier

    for i in range(total_faces):
        face_elevations[i] = influence[i]


def apply_ocean_basins(assigned, oceanic_cratons, face_elevations):
    ocean_depth = -config.height_amplitude * 0.5
    for i, craton_id in enumerate(assigned):
        if craton_id in oceanic_cratons:
            face_elevations[i] += ocean_depth


def slope_craton_centers(vertices, faces, assigned, oceanic_cratons, face_elevations, adjacency):
    craton_faces = {}
    for i, cid in enumerate(assigned):
        if cid not in craton_faces:
            craton_faces[cid] = []
        craton_faces[cid].append(i)

    for craton_id, face_indices in craton_faces.items():
        if not face_indices:
            continue
        centers = [np.mean(vertices[faces[i]], axis=0) for i in face_indices]
        plate_center = np.mean(centers, axis=0)

        for i in face_indices:
            face_center = np.mean(vertices[faces[i]], axis=0)
            dist = np.linalg.norm(plate_center - face_center)
            dist_weight = dist / config.radius

            if craton_id in oceanic_cratons:
                slope = -config.height_amplitude * 0.2 * (1 - dist_weight)  # slope UP to shore
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
