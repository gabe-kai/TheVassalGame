# planet_generator/elevation/tectonic.py

import numpy as np
from collections import deque
from planet_generator import config

from .tectonic_craton_seeding import seed_cratons_with_types
from .tectonic_craton_growth import grow_cratons
from .tectonic_boundary_interactions import assign_motion_vectors, apply_boundary_interactions, smooth_boundaries
from .tectonic_craton_sloping import slope_craton_centers, normalize_elevations
from .utils import estimate_craton_count, get_height_amplitude


def compute_tectonic_elevation(vertices, faces, face_centers, adjacency):
    """
    Simulates tectonic elevation changes on a planet surface.

    This process includes:
        - Seeding tectonic cratons
        - Assigning continental vs oceanic plates
        - Growing cratons across the face network
        - Computing relative plate motion vectors
        - Applying elevation change from plate interactions
        - Smoothing boundaries
        - Sloping craton interiors toward edges

    Args:
        vertices (np.ndarray): Array of shape (N, 3) with vertex coordinates.
        faces (list[tuple[int]]): List of face index groups (triplets of vertex indices).
        face_centers (np.ndarray): Precomputed 3D face centers (unit vectors).
        adjacency (dict[int, list[int]]): Map of face index to neighboring face indices.

    Returns:
        face_elevations: List of float elevation values per face
        craton_faces: List of craton IDs per face
        motion_vectors: Dict of craton_id to 3D motion vector
    """
    if config.debug_mode:
        print("[DEBUG] Starting tectonic elevation computation...")
        print("[DEBUG] Checking for faces with no neighbors...")
        for fidx, nbrs in adjacency.items():
            if not nbrs:
                print(f"Face {fidx} has NO neighbors!")

        debug_disconnected_regions(adjacency, faces)

    vertices: np.ndarray = np.array(vertices, dtype=np.float64)
    total_faces = len(faces)
    estimated_craton_count = estimate_craton_count(total_faces, config.radius)
    rng = np.random.default_rng()  # Map generation seed, set to a static number to get the same map repeatedly.

    # Seed the craton starting spots on random faces, and then assign face types (Continental or Oceanic).
    craton_seeds, plate_types = seed_cratons_with_types(total_faces, estimated_craton_count, rng)

    # Initialize elevations and then grow the cratons until they fill the map
    face_elevations = [0.0 for _ in faces]
    craton_faces = grow_cratons(faces, craton_seeds, adjacency, plate_types, face_elevations, vertices)
    if config.debug_mode:
        unassigned_count = sum(1 for cid in craton_faces if cid == -1)
        print(f"[DEBUG] Unassigned faces after growth: {unassigned_count}")

    # Assign a motion vector to each craton to determine collision.
    motion_vectors = assign_motion_vectors(list(plate_types.keys()), rng)

    # Converge, diverge, or transform the cratons where they interact
    apply_boundary_interactions(face_centers, adjacency, craton_faces, motion_vectors, face_elevations, rng, plate_types)

    # Smooth the boundaries between mountains and landmasses or seas
    smooth_boundaries(faces, adjacency, face_elevations)

    # Slope the cratons so they have shores and high or low points
    slope_craton_centers(face_centers, craton_faces, plate_types, face_elevations, adjacency)

    # Normalize the face elevations to within the expected range, a function of the planet radius.
    face_elevations[:] = normalize_elevations(face_elevations)

    if config.debug_mode:
        debug_elevation_summary(face_elevations, craton_faces, plate_types)

    return face_elevations, craton_faces, motion_vectors


def debug_disconnected_regions(adjacency, faces):
    print("[DEBUG] Checking for disconnected regions across the entire planet mesh...")
    visited_global = set()
    components = []
    total_faces = len(faces)
    for face_idx in range(total_faces):
        if face_idx not in visited_global:
            queue = deque([face_idx])
            visited_local = set([face_idx])
            visited_global.add(face_idx)
            while queue:
                current = queue.popleft()
                for neigh in adjacency[current]:
                    if neigh not in visited_global:
                        visited_global.add(neigh)
                        visited_local.add(neigh)
                        queue.append(neigh)
            components.append(visited_local)
    print(f"[DEBUG] Found {len(components)} disconnected region(s).")
    for i, comp in enumerate(components):
        print(f"        Region {i+1} has {len(comp)} faces.")


def debug_elevation_summary(face_elevations, craton_faces, plate_types):
    elevations = np.array(face_elevations)
    min_elev = elevations.min()
    max_elev = elevations.max()

    sea_level = config.sea_level
    height_amplitude = get_height_amplitude()
    mountain_thresh = sea_level + height_amplitude * config.mountain_zone_threshold
    trench_thresh = sea_level - height_amplitude * config.trench_zone_threshold

    ocean_indices = [i for i, cid in enumerate(craton_faces) if plate_types.get(cid) == "oceanic"]
    cont_indices = [i for i, cid in enumerate(craton_faces) if plate_types.get(cid) == "continental"]

    ocean_main = [i for i in ocean_indices if elevations[i] >= trench_thresh]
    cont_main = [i for i in cont_indices if elevations[i] <= mountain_thresh]

    ocean_depths = elevations[ocean_main] if ocean_main else np.array([])
    cont_heights = elevations[cont_main] if cont_main else np.array([])

    avg_ocean = ocean_depths.mean() if len(ocean_depths) > 0 else 0.0
    avg_cont = cont_heights.mean() if len(cont_heights) > 0 else 0.0

    trench_avg = elevations[
        [i for i in ocean_indices if elevations[i] < avg_ocean]].mean() if ocean_indices else 0.0
    mount_avg = elevations[[i for i in cont_indices if elevations[i] > avg_cont]].mean() if cont_indices else 0.0

    print("[DEBUG] Elevation Summary:")
    print(f"         Lowest: {min_elev:.3f}km")
    print(f"         Highest: {max_elev:.3f}km")
    print(f"         Avg Ocean Depth: {avg_ocean:.3f}km")
    print(f"         Avg Cont. Height: {avg_cont:.3f}km")
    print(f"         Avg Ocean Trench: {trench_avg:.3f}km")
    print(f"         Avg Cont. Mountain: {mount_avg:.3f}km")

    print("[DEBUG] Terrain Classification Thresholds (in km):")
    print(f"         Lowland/Plains Threshold:  {sea_level + height_amplitude * config.plains_zone_threshold:.3f}km")
    print(f"         Foothill Threshold:        {sea_level + height_amplitude * config.foothills_zone_threshold:.3f}km")
    print(f"         Mountain Threshold:        {sea_level + height_amplitude * config.mountain_zone_threshold:.3f}km")
    print(f"         Mountain Peak Threshold:   {sea_level + height_amplitude * config.mountain_peak_threshold:.3f}km")
    print(f"         Ocean Trench Threshold:    {sea_level - height_amplitude * config.trench_zone_threshold:.3f}km")
