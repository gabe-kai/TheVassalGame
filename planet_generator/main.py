# planet_generator/main.py

from planet_generator import config
from planet_generator.geometry import generate_base_icosahedron, subdivide
from planet_generator.elevation import compute_face_elevation
from planet_generator.elevation.ocean import generate_ocean_sphere
from planet_generator.coloring import apply_face_coloring
from planet_generator.export import export_obj_and_mtl
# from planet_generator.plot import draw_planet

import numpy as np

def generate_qi_pools(vertices, faces):
    """Returns Qi Pool vertex coordinates, randomly selected from all vertices."""
    total_faces = len(faces)
    num_qi_pools = int(total_faces * config.qi_pool_percentage)

    vertex_indices = np.arange(len(vertices))
    np.random.seed(config.qi_pool_seed)
    np.random.shuffle(vertex_indices)
    qi_indices = vertex_indices[:num_qi_pools]
    return vertices[qi_indices]

def main():
    # Step 1: Build icosphere
    vertices, faces = generate_base_icosahedron()
    vertices, faces = subdivide(vertices, faces, config.subdivision_depth)

    # Step 2: Elevation & terrain shaping
    print("[DEBUG] Starting elevation computation using method:", config.elevation_method)
    face_elevations, assigned, motion_vectors = compute_face_elevation(vertices, faces)
    print("[DEBUG] Elevation computation complete.")

    # Step 3: Climate & elevation coloring
    face_colors = apply_face_coloring(vertices, faces, face_elevations)

    # Step 4: Qi Pools (optional)
    qi_coords = generate_qi_pools(vertices, faces)

    # Step 5: Optional ocean mesh
    if config.generate_ocean:
        ocean_vertices, ocean_faces = generate_ocean_sphere()
    else:
        ocean_vertices, ocean_faces = None, None

    # Step 6: Preview planet
    # draw_planet(vertices, faces, face_colors, qi_pool_coords=qi_coords)

    # Step 7: Export to OBJ + MTL
    export_obj_and_mtl(vertices, faces, face_colors, ocean_vertices, ocean_faces)

if __name__ == "__main__":
    main()
