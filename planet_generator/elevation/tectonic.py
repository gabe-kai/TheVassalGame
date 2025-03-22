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
        print("[DEBUG] Assigning plate types...")
    plate_types = assign_plate_types(craton_seeds, rng)
    if config.debug_mode:
        print("[DEBUG] Building adjacency map...")
    adjacency = build_adjacency(faces)
    if config.debug_mode:
        print("[DEBUG] Growing cratons...")
    assigned = grow_cratons(faces, craton_seeds, adjacency)
    unassigned_count = sum(1 for cid in assigned if cid == -1)
    if config.debug_mode:
        print(f"[DEBUG] Unassigned faces after growth: {unassigned_count}")
    if config.debug_mode:
        print("[DEBUG] Assigning motion vectors...")
    motion_vectors = assign_motion_vectors(list(plate_types.keys()), rng)

    if config.debug_mode:
        print("[DEBUG] Applying boundary interactions...")
    face_elevations = [0.0 for _ in faces]
    apply_boundary_interactions(vertices, faces, adjacency, assigned, motion_vectors, face_elevations, rng, plate_types)
    if config.debug_mode:
        print("[DEBUG] Smoothing elevation boundaries...")
    smooth_boundaries(faces, adjacency, face_elevations)
    if config.debug_mode:
        print("[DEBUG] Slope-craton-center elevation pass...")
    slope_craton_centers(vertices, faces, assigned, plate_types, face_elevations, adjacency)

    return face_elevations, assigned, motion_vectors


# --- Helper Functions ---

def seed_cratons(total_faces, count, rng):
    """
    Selects `count` random face indices to act as tectonic plate seeds (cratons).
    """
    return rng.choice(total_faces, size=count, replace=False)


def assign_plate_types(craton_seeds, rng):
    """
    Assigns each craton (seed) as 'oceanic' or 'continental' up front
    based on config.oceanic_craton_fraction.
    Returns a dict {seed_face: 'oceanic'|'continental'}
    """
    if config.debug_mode:
        oceanic = 0
        continental = 0

    plate_types = {}
    for seed in craton_seeds:
        if rng.random() < config.oceanic_craton_fraction:
            plate_types[seed] = "oceanic"
            if config.debug_mode:
                oceanic += 1
            plate_types[seed] = "oceanic"
        else:
            plate_types[seed] = "continental"
            if config.debug_mode:
                continental += 1
    if config.debug_mode:
        print(f"[DEBUG] Plate types assigned: {continental} continental, {oceanic} oceanic")

    return plate_types


def build_adjacency(faces):
    """
    Builds an adjacency map for each face index based on shared vertices.
    Returns a dictionary: {face_index: set(neighbor_indices)}
    """
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
    """
    Grows each craton outward using BFS from its seed face, assigning all reachable faces.
    Returns a list: assigned[face_index] = craton_id
    """
    total_faces = len(faces)
    assigned = [-1] * total_faces
    queues = {seed: deque([seed]) for seed in craton_seeds}
    for seed in craton_seeds:
        assigned[seed] = seed

    active = True
    while active:
        active = False
        for craton_id, queue in queues.items():
            if not queue:
                continue
            face = queue.popleft()
            for neighbor in adjacency[face]:
                if assigned[neighbor] == -1:
                    assigned[neighbor] = craton_id
                    queue.append(neighbor)
                    active = True
    return assigned


def assign_motion_vectors(craton_ids, rng):
    """
    Assigns a normalized 3D motion vector to each craton ID.
    Returns a dictionary: {craton_id: vector (np.array)}
    """
    vectors = {}
    for craton_id in craton_ids:
        vec = rng.normal(size=3)
        vec /= np.linalg.norm(vec)
        vectors[craton_id] = vec
#    if config.debug_mode:
#        for cid, vec in vectors.items():
#            print(f"[DEBUG] Craton {cid} motion vector: ({vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f})")
    return vectors


def apply_boundary_interactions(vertices, faces, adjacency, assigned, motion_vectors, face_elevations, rng, plate_types):
    """
    Applies tectonic elevation changes at boundaries,
    using plate type logic for more realistic mountains/trenches.
    """
    threshold = 0.1
    debug_count = 0

    # Example constants (tweak as desired)
    # Converging lifts
    cont_cont_converge = config.height_amplitude * 0.8       # big mountains for continental collision
    cont_ocean_converge_cont_side = config.height_amplitude  # tall coastal mountains
    cont_ocean_converge_ocean_side = -config.height_amplitude * 0.6  # trench
    ocean_ocean_converge = config.height_amplitude * 0.3      # island arcs

    # Diverging lowers or forms ridges
    cont_cont_diverge = -config.height_amplitude * 0.2        # continental rift
    ocean_ocean_diverge = config.height_amplitude * 0.2       # mid-ocean ridge
    cont_ocean_diverge = -config.height_amplitude * 0.1       # mild rift near coasts

    # Transform gets random fracturing
    transform_variation = config.height_amplitude * 0.1

    for face_idx, neighbors in adjacency.items():
        plate_a = assigned[face_idx]
        if plate_a == -1:
            continue
        ptype_a = plate_types.get(plate_a, "continental")

        for neighbor_idx in neighbors:
            plate_b = assigned[neighbor_idx]
            if plate_b == -1 or plate_b == plate_a:
                continue
            ptype_b = plate_types.get(plate_b, "continental")

            # Face centers
            pos_a = np.mean(vertices[faces[face_idx]], axis=0)
            pos_b = np.mean(vertices[faces[neighbor_idx]], axis=0)
            direction = pos_b - pos_a
            norm_dir = np.linalg.norm(direction)
            if norm_dir == 0:
                continue
            direction /= norm_dir

            # Relative motion
            vec_a = motion_vectors[plate_a]
            vec_b = motion_vectors[plate_b]
            relative_motion = np.dot(vec_b - vec_a, direction)

            # Classify boundary
            interaction = "transform"
            if relative_motion > threshold:
                interaction = "diverging"
            elif relative_motion < -threshold:
                interaction = "converging"

            if interaction == "converging":
                # Each pair of plate types has custom logic
                if ptype_a == "continental" and ptype_b == "continental":
                    # Big collision mountains
                    face_elevations[face_idx] += cont_cont_converge
                    face_elevations[neighbor_idx] += cont_cont_converge

                elif ptype_a == "continental" and ptype_b == "oceanic":
                    # Mountain on continental side, trench on ocean side
                    face_elevations[face_idx] += cont_ocean_converge_cont_side
                    face_elevations[neighbor_idx] += cont_ocean_converge_ocean_side

                elif ptype_a == "oceanic" and ptype_b == "continental":
                    # Trench on plate_a, mountain on plate_b
                    face_elevations[face_idx] += cont_ocean_converge_ocean_side
                    face_elevations[neighbor_idx] += cont_ocean_converge_cont_side

                else:  # oceanic-oceanic
                    face_elevations[face_idx] += ocean_ocean_converge
                    face_elevations[neighbor_idx] += ocean_ocean_converge

            elif interaction == "diverging":
                # Similar logic for plate combos
                if ptype_a == "continental" and ptype_b == "continental":
                    face_elevations[face_idx] += cont_cont_diverge
                    face_elevations[neighbor_idx] += cont_cont_diverge

                elif ptype_a == "oceanic" and ptype_b == "oceanic":
                    # mid-ocean ridge
                    face_elevations[face_idx] += ocean_ocean_diverge
                    face_elevations[neighbor_idx] += ocean_ocean_diverge

                else:
                    # oceanic <-> continental
                    face_elevations[face_idx] += cont_ocean_diverge
                    face_elevations[neighbor_idx] += cont_ocean_diverge

            else:  # transform
                noise = rng.uniform(-transform_variation, transform_variation)
                face_elevations[face_idx] += noise
                face_elevations[neighbor_idx] += noise

            debug_count_display_limit = 10
            if config.debug_mode and debug_count < debug_count_display_limit:
                print(f"[DEBUG] Face {face_idx}↔{neighbor_idx}: {interaction.upper()} ({ptype_a} vs {ptype_b}) Δv•dir = {relative_motion:.3f}")
                debug_count += 1

    if config.debug_mode:
        print(f"[DEBUG] First  {debug_count_display_limit} boundary interactions displayed...")



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


def slope_craton_centers(vertices, faces, assigned, plate_types, face_elevations, adjacency):
    """
    Applies elevation slope from the center of each craton outward.
    Oceanic plates slope up toward the edge; continental plates slope down.
    Also factors in nearby mountain/trench elevation to adjust slope locally.
    """
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

            plate_type = plate_types.get(craton_id, "continental")
            if plate_type == "oceanic":
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
