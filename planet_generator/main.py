# planet_generator/main.py

from planet_generator import config
from planet_generator.geometry import generate_base_icosahedron, subdivide, build_adjacency, compute_face_centers
from planet_generator.elevation import select_elevation_method
from planet_generator.elevation.ocean import generate_ocean_sphere
from planet_generator.coloring import apply_face_coloring
from planet_generator.export import export_obj_and_mtl


def main():
    # Step 1: Build icosphere
    print("[DEBUG] Generating an icosphere.")
    vertices, faces = generate_base_icosahedron()                           # Start with an icosahedron
    vertices, faces = subdivide(vertices, faces, config.subdivision_depth)  # Subdivide it
    adjacency = build_adjacency(faces)                                      # Build an adjacency map
    face_centers = compute_face_centers(faces, vertices)                    # Calculate the face_canters for later use

    # Step 2: Elevation & terrain shaping
    print("[DEBUG] Starting elevation computation using method:", config.elevation_method)
    # Accepts the elevation-related parameters and passes them on to the elevation method chosen in config.py
    face_elevations, assigned, motion_vectors = select_elevation_method(vertices, faces, face_centers, adjacency)
    print("[DEBUG] Elevation computation complete.")

    # Step 3: Climate & elevation coloring
    # Colors the faces according to elevation, longitude, and overlay options from config.py
    face_colors = apply_face_coloring(vertices, faces, face_elevations)

    # Step 4: Optional ocean mesh
    # Generate a separate ocean mesh for 3d modeling software.
    if config.generate_ocean:
        ocean_vertices, ocean_faces = generate_ocean_sphere()
    else:
        ocean_vertices, ocean_faces = None, None

    # Step 5: Export to OBJ + MTL
    export_obj_and_mtl(vertices, faces, face_colors, ocean_vertices, ocean_faces)

if __name__ == "__main__":
    main()
