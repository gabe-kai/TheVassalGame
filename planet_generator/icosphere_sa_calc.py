import math

# Update these variables as needed:
radius = 25500         # Radius of the sphere in km (e.g., Earth's radius is 6371)
subdivision_depth = 10 # Subdivision depth (n)

# Total surface area of the sphere.
total_area = 4 * math.pi * radius**2

# Total number of faces on the subdivided icosahedron.
num_faces = 20 * (4 ** subdivision_depth)

# Average area per face using the formula:
# A_face = (pi * R^2) / (5 * 4^n)
average_face_area = (math.pi * radius**2) / (5 * (4 ** subdivision_depth))

# Alternatively, it is the same as:
# average_face_area = total_area / num_faces

# Combined area of the 6 faces that share a vertex in a standard hex tile
hex_tile_combined_area = 6 * average_face_area

# Combined area of the 5 faces that share a vertex at one of the original 20 icosahedron vertices
special_tile_combined_area = 5 * average_face_area

print("Sphere radius: {} km".format(radius))
print("Subdivision depth: {}".format(subdivision_depth))
print("Total number of faces: {}".format(num_faces))
print("Total surface area of sphere: {:.2f} km^2".format(total_area))
print("Average face area: {:.2f} km^2".format(average_face_area))
print("Combined area of 6 faces in a hex tile: {:.2f} km^2".format(hex_tile_combined_area))
print("Combined area of 5 faces at an original vertex: {:.2f} km^2".format(special_tile_combined_area))
