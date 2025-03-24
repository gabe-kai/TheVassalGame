# planet_generator/elevation/tectonic.py

import math
import numpy as np
from collections import deque
from planet_generator import config


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
    craton_faces = grow_cratons(faces, craton_seeds, adjacency, plate_types, face_elevations)
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


# --- Helper Functions ---

def seed_cratons_with_types(total_faces, count, rng):
    """
    Seeds cratons on random faces and assigns each one a tectonic type.

    This replaces the separate steps of seeding cratons and assigning plate types.
    Each seed is chosen randomly and assigned as 'continental' or 'oceanic'
    based on the configured oceanic_craton_fraction.

    Args:
        total_faces (int): Number of mesh faces on the planet.
        count (int): Number of cratons to seed.
        rng (np.random.Generator): Random number generator.

    Returns:
        tuple:
            - List[int]: Craton seed face indices.
            - Dict[int, str]: Mapping from seed index to 'continental' or 'oceanic'.
    """
    if config.debug_mode:
        print("[DEBUG] Seeding cratons and assigning plate types...")

    oceanic = 0
    continental = 0

    craton_seeds = rng.choice(total_faces, size=count, replace=False)
    plate_types = {}

    for seed in craton_seeds:
        if rng.random() < config.oceanic_craton_fraction:
            plate_types[seed] = "oceanic"
            if config.debug_mode:
                oceanic += 1
        else:
            plate_types[seed] = "continental"
            if config.debug_mode:
                continental += 1

    if config.debug_mode:
        print(f"[DEBUG] Plate types assigned: {continental} continental, {oceanic} oceanic")

    return craton_seeds.tolist(), plate_types


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


def apply_boundary_interactions(vertices, faces, adjacency, assigned, motion_vectors, face_elevations, rng, plate_types):
    """
    Modifies elevation based on tectonic boundary interactions.

    Detects and classifies boundaries between adjacent cratons
    (converging, diverging, or transform) and applies
    corresponding elevation adjustments based on plate types.

    Args:
        vertices (np.ndarray): Vertex coordinates.
        faces (list[tuple[int]]): Triangle face definitions.
        adjacency (dict[int, list[int]]): Face adjacency map.
        assigned (list[int]): Craton ID for each face.
        motion_vectors (dict[int, np.ndarray]): 3D vector per craton.
        face_elevations (list[float]): Elevation values to modify in-place.
        rng (np.random.Generator): Random number generator.
        plate_types (dict[int, str]): Mapping of craton IDs to 'continental' or 'oceanic'.
    """
    if config.debug_mode:
        print("[DEBUG] Applying boundary interactions...")

    threshold = 0.1
    debug_count = 0
    debug_count_display_limit = 10

    # Converging lifts
    cont_cont_converge = config.height_amplitude * 0.8                  # big mountains for continental collision
    cont_ocean_converge_cont_side = config.height_amplitude             # tall coastal mountains
    cont_ocean_converge_ocean_side = -config.height_amplitude * 0.8     # trench
    ocean_ocean_converge_ratio = 0.06                                   # relative to ocean base height

    # Diverging lowers or forms ridges
    cont_cont_diverge = -config.height_amplitude * 0.2                  # continental rift
    ocean_ocean_diverge = config.height_amplitude * 0.1                 # mid-ocean ridge
    cont_ocean_diverge = -config.height_amplitude * 0.1                 # mild rift near coasts

    # Transform gets random fracturing
    transform_variation = config.height_amplitude * 0.05

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
            pos_a = np.mean(vertices[np.array(faces[face_idx])], axis=0)
            pos_b = np.mean(vertices[np.array(faces[neighbor_idx])], axis=0)
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
                variation_a = rng.normal(loc=1.0, scale=0.18)
                variation_b = rng.normal(loc=1.0, scale=0.18)
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
                    rise = config.height_amplitude * ocean_ocean_converge_ratio
                    face_elevations[face_idx] += (rise * (1 - abs(base_a) / config.height_amplitude)) * variation_a
                    face_elevations[neighbor_idx] += (rise * (1 - abs(base_b) / config.height_amplitude)) * variation_b

            elif interaction == "diverging":
                # Similar logic for plate combos
                variation_a = rng.normal(loc=1.0, scale=0.18)
                variation_b = rng.normal(loc=1.0, scale=0.18)
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
