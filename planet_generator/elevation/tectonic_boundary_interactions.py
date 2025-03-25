# planet_generator/elevation/tectonic_boundary_interactions.py

from planet_generator import config
import numpy as np
from .utils import get_height_amplitude


def assign_motion_vectors(craton_ids, rng):
    """
    Generates and normalizes a random 3D motion vector for each craton.

    Motion vectors determine tectonic interaction types (e.g. converging/diverging).

    Args:
        craton_ids (list[int]): List of craton identifiers.
        rng (np.random.Generator): Random number generator.

    Returns:
        dict[int, np.ndarray]: Mapping from craton ID to normalized 3D vector.
    """
    if config.debug_mode:
        print("[DEBUG] Assigning motion vectors...")

    vectors = {}
    for craton_id in craton_ids:
        vec = rng.normal(size=3)
        vec /= np.linalg.norm(vec)
        vectors[craton_id] = vec
#    if config.debug_mode:
#        for cid, vec in vectors.items():
#            print(f"[DEBUG] Craton {cid} motion vector: ({vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f})")

    return vectors


# TODO: Move the threshold and decay values from being hard-coded here to user config values from config.py
def apply_boundary_interactions(face_centers, adjacency, assigned, motion_vectors, face_elevations, rng, plate_types):
    """
    Modifies elevation based on tectonic boundary interactions.

    Detects and classifies boundaries between adjacent cratons
    (converging, diverging, or transform) and applies
    corresponding elevation adjustments based on plate types.

    Args:
        face_centers (np.ndarray): Precomputed 3D face centers (unit vectors).
        adjacency (dict[int, list[int]]): Face adjacency map.
        assigned (list[int]): Craton ID for each face.
        motion_vectors (dict[int, np.ndarray]): 3D vector per craton.
        face_elevations (list[float]): Elevation values to modify in-place.
        rng (np.random.Generator): Random number generator.
        plate_types (dict[int, str]): Mapping of craton IDs to 'continental' or 'oceanic'.
    """
    if config.debug_mode:
        print("[DEBUG] Applying boundary interactions...")

    height_amplitude = get_height_amplitude()
    threshold = 0.1
    debug_count = 0
    debug_count_display_limit = 10

    # Converging lifts
    cont_cont_converge = height_amplitude * 1.2                  # big mountains for continental collision
    cont_ocean_converge_cont_side = height_amplitude * 1.4       # tall coastal mountains
    cont_ocean_converge_ocean_side = -height_amplitude * 1.0     # trench
    ocean_ocean_converge_ratio = 0.1                             # relative to ocean base height

    # Diverging lowers or forms ridges
    cont_cont_diverge = -height_amplitude * 0.2                  # continental rift
    ocean_ocean_diverge = height_amplitude * 0.1                 # mid-ocean ridge
    cont_ocean_diverge = -height_amplitude * 0.1                 # mild rift near coasts

    # Transform gets random fracturing
    transform_variation = height_amplitude * 0.05

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
            pos_a = face_centers[face_idx]
            pos_b = face_centers[neighbor_idx]
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
                variation_a = rng.normal(loc=1.1, scale=0.1)
                variation_b = rng.normal(loc=1.1, scale=0.1)
                if ptype_a == "continental" and ptype_b == "continental":
                    # Big collision mountains
                    face_elevations[face_idx] += cont_cont_converge * variation_a
                    face_elevations[neighbor_idx] += cont_cont_converge * variation_b

                elif ptype_a == "continental" and ptype_b == "oceanic":
                    # Mountain on continental side, trench on ocean side
                    face_elevations[face_idx] += cont_ocean_converge_cont_side * variation_a
                    face_elevations[neighbor_idx] += cont_ocean_converge_ocean_side * variation_b

                elif ptype_a == "oceanic" and ptype_b == "continental":
                    # Trench on plate_a, mountain on plate_b
                    face_elevations[face_idx] += cont_ocean_converge_ocean_side * variation_a
                    face_elevations[neighbor_idx] += cont_ocean_converge_cont_side * variation_b

                else:  # oceanic-oceanic
                    base_a = face_elevations[face_idx]
                    base_b = face_elevations[neighbor_idx]
                    rise = height_amplitude * ocean_ocean_converge_ratio
                    face_elevations[face_idx] += (rise * (1 - abs(base_a) / height_amplitude)) * variation_a
                    face_elevations[neighbor_idx] += (rise * (1 - abs(base_b) / height_amplitude)) * variation_b

            elif interaction == "diverging":
                # Similar logic for plate combos
                variation_a = rng.normal(loc=1.1, scale=0.1)
                variation_b = rng.normal(loc=1.1, scale=0.1)
                if ptype_a == "continental" and ptype_b == "continental":
                    face_elevations[face_idx] += cont_cont_diverge * variation_a
                    face_elevations[neighbor_idx] += cont_cont_diverge * variation_b

                elif ptype_a == "oceanic" and ptype_b == "oceanic":
                    # mid-ocean ridge
                    face_elevations[face_idx] += ocean_ocean_diverge * variation_a
                    face_elevations[neighbor_idx] += ocean_ocean_diverge * variation_b

                else:
                    # oceanic <-> continental
                    face_elevations[face_idx] += cont_ocean_diverge * variation_a
                    face_elevations[neighbor_idx] += cont_ocean_diverge * variation_b

            else:  # transform
                noise = rng.uniform(-transform_variation, transform_variation)
                face_elevations[face_idx] += noise
                face_elevations[neighbor_idx] += noise

            if config.debug_mode and debug_count < debug_count_display_limit:
                print(f"[DEBUG] Face {face_idx}↔{neighbor_idx}: {interaction.upper()} ({ptype_a} vs {ptype_b}) Δv•dir = {relative_motion:.3f}")
                debug_count += 1

    if config.debug_mode:
        print(f"[DEBUG] First  {debug_count_display_limit} boundary interactions displayed...")


def smooth_boundaries(faces, adjacency, face_elevations):
    """
    Smooths elevation transitions at tectonic boundaries.

    Uses a layered propagation algorithm to blend sharp elevation
    differences outward into neighboring regions. Avoids altering
    extreme peaks or trenches to preserve geological detail.

    Args:
        faces (list[tuple[int]]): Triangle face definitions.
        adjacency (dict[int, list[int]]): Face adjacency map.
        face_elevations (list[float]): Elevation values to smooth in-place.
    """
    if config.debug_mode:
        print("[DEBUG] Smoothing elevation boundaries...")

    max_smoothing_layers = 6
    decay_factor = 0.07
    total_faces = len(faces)
    height_amplitude = get_height_amplitude()
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
                    if abs(face_elevations[face]) > 0.8 * height_amplitude:
                        continue
                    falloff = decay_factor ** layer
                    influence[neighbor] += face_elevations[face] * falloff
                    next_frontier.add(neighbor)
                    visited[neighbor] = True
        current_frontier = next_frontier

    for i in range(total_faces):
        face_elevations[i] = influence[i]
