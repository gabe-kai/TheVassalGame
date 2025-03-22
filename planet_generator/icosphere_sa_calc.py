#!/usr/bin/env python3
import math

# === Configuration ===
radius = 25500               # Radius in kilometers (try 25500 +/- 25%)
subdivision_depth = 6        # Subdivision level (e.g., 0 to 7)

# === Geometry Calculations ===
f = 20 * (4 ** subdivision_depth)               # Number of faces (triangles)
e = 30 * (4 ** subdivision_depth)               # Number of edges
v = 10 * (4 ** subdivision_depth) + 2           # Number of vertices (Euler's formula)

# === Surface Area and Face Area ===
surface_area = 4 * math.pi * radius ** 2
average_face_area = surface_area / f

# === Output ===
print("=== Icosphere Geometry Stats ===")
print(f"Radius: {radius} km")
print(f"Subdivision depth: {subdivision_depth}")
print(f"Total vertices: {v}")
print(f"Total edges:    {e}")
print(f"Total faces:    {f}")
print()
print("=== Surface Area ===")
print(f"Total surface area:  {surface_area:,.2f} km²")
print(f"Average face area:   {average_face_area:,.2f} km²")
print(f"Approximate edge length: {math.sqrt(average_face_area):,.2f} km (assuming equilateral)")
