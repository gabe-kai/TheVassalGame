# planet_generator/elevation/tectonic.py

import math
import numpy as np
from collections import deque
from planet_generator import config

from .tectonic_craton_seeding import seed_cratons_with_types
from .tectonic_craton_growth import grow_cratons
from .tectonic_boundary_interactions import assign_motion_vectors, apply_boundary_interactions, smooth_boundaries
from .tectonic_craton_sloping import slope_craton_centers

def compute_tectonic_elevation(vertices, faces, adjacency):
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

        # DEBUG: Check for disconnected regions across the entire planet mesh
        print("[DEBUG] Checking for disconnected regions across the entire planet mesh...")
        visited_global = set()
        components = []
        total_faces = len(faces)
        for face_idx in range(total_faces):
            if face_idx not in visited_global:
                # BFS from face_idx to find all connected faces
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

    vertices: np.ndarray = np.array(vertices, dtype=np.float64)
    total_faces = len(faces)
    surface_area_km2 = 4 * math.pi * config.radius**2
    estimated_craton_count = config.craton_count or max(8, int(surface_area_km2 / 8e7))
    rng = np.random.default_rng()  # Map generation seed, set to a static number to get the same map repeatedly.

    # Seed the craton starting spots on random faces, and then assign face types (Continental or Oceanic).
    craton_seeds, plate_types = seed_cratons_with_types(total_faces, estimated_craton_count, rng)

    # Initialize elevations and then grow the cratons until they fill the map
    face_elevations = [0.0 for _ in faces]
    craton_faces = grow_cratons(faces, craton_seeds, adjacency, plate_types, face_elevations, vertices)
    if config.debug_mode:
        unassigned_count = sum(1 for cid in craton_faces if cid == -1)
        print(f"[DEBUG] Unassigned faces after growth: {unassigned_count}")

    # Assign motion vectors, calculate boundary interactions, smooth the boundaries, and slope the cratons
    motion_vectors = assign_motion_vectors(list(plate_types.keys()), rng)
    apply_boundary_interactions(vertices, faces, adjacency, craton_faces, motion_vectors, face_elevations, rng, plate_types)
    smooth_boundaries(faces, adjacency, face_elevations)
    slope_craton_centers(vertices, faces, craton_faces, plate_types, face_elevations, adjacency)

    if config.debug_mode:
        elevations = np.array(face_elevations)
        min_elev = elevations.min()
        max_elev = elevations.max()
        ocean_indices = [i for i, cid in enumerate(craton_faces) if plate_types.get(cid) == "oceanic"]
        cont_indices = [i for i, cid in enumerate(craton_faces) if plate_types.get(cid) == "continental"]

        ocean_depths = elevations[ocean_indices] if ocean_indices else np.array([])
        cont_heights = elevations[cont_indices] if cont_indices else np.array([])

        avg_ocean = ocean_depths.mean() if len(ocean_depths) > 0 else 0.0
        avg_cont = cont_heights.mean() if len(cont_heights) > 0 else 0.0
        trench_avg = ocean_depths[ocean_depths < avg_ocean].mean() if len(ocean_depths[ocean_depths < avg_ocean]) > 0 else 0.0
        mount_avg = cont_heights[cont_heights > avg_cont].mean() if len(cont_heights[cont_heights > avg_cont]) > 0 else 0.0

        print("[DEBUG] Elevation Summary:")
        print(f"         Lowest: {min_elev:.3f}")
        print(f"         Highest: {max_elev:.3f}")
        print(f"         Avg Ocean Depth: {avg_ocean:.3f}")
        print(f"         Avg Cont. Height: {avg_cont:.3f}")
        print(f"         Avg Ocean Trench: {trench_avg:.3f}")
        print(f"         Avg Cont. Mountain: {mount_avg:.3f}")

    return face_elevations, craton_faces, motion_vectors
