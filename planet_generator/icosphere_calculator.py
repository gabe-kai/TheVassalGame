#/planet_generator/icosphere_calculator.py
import math

# === Configuration ===
radius = 25500                                      # Radius. Earth is 6371km. Empire Standard Shell Worlds are 25500km.
subdivision_depth = 10                              # Subdivision level

# === Geometry Calculations ===
f = 20 * (4 ** subdivision_depth)                   # Number of faces (triangles)
e = 30 * (4 ** subdivision_depth)                   # Number of edges
v = 10 * (4 ** subdivision_depth) + 2               # Number of vertices (Euler's formula)

# === Surface Area and Face Area ===
surface_area = 4 * math.pi * radius ** 2            # Surface area of final sphere in km^2
average_face_area = surface_area / f                # Average face-area of individual triangles.

# === Hex/Pent Face Cluster Areas ===
hex_cluster_area = 6 * average_face_area            # Surface area of a cluster of 6 hexes around most vertices.
pent_cluster_area = 5 * average_face_area           # Surface area of a cluster of 5 hexes around the 20 icosahedron vertices.

# === Approximate Edge and Region Distances ===
avg_edge_length = math.sqrt(average_face_area)      # Assuming equilateral triangle
hex_cluster_diameter = avg_edge_length * 2.5        # Approximate tip-to-tip
pent_cluster_diameter = avg_edge_length * 2.2       # Slightly smaller region than hex clusters

# === Sphere Volume & Circumference ===
volume = (4/3) * math.pi * radius**3                # Total internal volume in km^3
circumference = 2 * math.pi * radius                # Equatorial great-circle circumference in km

# === Output ===
print("=== Icosphere Geometry Stats ===")
print(f"Radius: {radius} km")
print(f"Subdivision depth: {subdivision_depth}")
print(f"Total vertices: {v:,}")
print(f"Total edges:    {e:,}")
print(f"Total faces:    {f:,}")
print()
print("=== Surface Area ===")
print(f"Total surface area:  {surface_area:,.2f} km²")
print(f"Average face area:   {average_face_area:,.2f} km²")
print(f"Approximate edge length: {avg_edge_length:,.2f} km (assuming equilateral)")
print()
print("=== Regional Tile Clusters ===")
print(f"Hex cluster area (6 triangles):   {hex_cluster_area:,.2f} km²")
print(f"Pent cluster area (5 triangles):  {pent_cluster_area:,.2f} km²")
print(f"Hex cluster diameter:             {hex_cluster_diameter:,.2f} km")
print(f"Pent cluster diameter:            {pent_cluster_diameter:,.2f} km")
print()
print("=== Global Sphere Properties ===")
print(f"Volume:                           {volume:,.2f} km³")
print(f"Great-circle circumference:       {circumference:,.2f} km")
