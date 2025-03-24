# planet_generator/main.py

from planet_generator import config
from planet_generator.geometry import generate_base_icosahedron, subdivide, build_adjacency
from planet_generator.elevation import compute_face_elevation
from planet_generator.elevation.ocean import generate_ocean_sphere
from planet_generator.coloring import apply_face_coloring
from planet_generator.export import export_obj_and_mtl


def main():
    # Step 1: Build icosphere
    vertices, faces = generate_base_icosahedron()
    vertices, faces = subdivide(vertices, faces, config.subdivision_depth)
    adjacency = build_adjacency(faces)


    # Step 2: Elevation & terrain shaping
    print("[DEBUG] Starting elevation computation using method:", config.elevation_method)
    face_elevations, assigned, motion_vectors = compute_face_elevation(vertices, faces, adjacency)
    print("[DEBUG] Elevation computation complete.")

    # Step 3: Climate & elevation coloring
    face_colors = apply_face_coloring(vertices, faces, face_elevations)

    # Step 4: Optional ocean mesh
    if config.generate_ocean:
        ocean_vertices, ocean_faces = generate_ocean_sphere()
    else:
        ocean_vertices, ocean_faces = None, None

    # Step 5: Export to OBJ + MTL
    export_obj_and_mtl(vertices, faces, face_colors, ocean_vertices, ocean_faces)

if __name__ == "__main__":
    main()
