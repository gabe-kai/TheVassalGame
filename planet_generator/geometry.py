# planet_generator/geometry.py

import numpy as np
from planet_generator import config

def generate_base_icosahedron():
    """Returns the initial icosahedron vertices and faces, scaled to config.radius."""
    golden_ratio = (1 + np.sqrt(5)) / 2

    vertices = np.array([
        [-1, golden_ratio, 0], [1, golden_ratio, 0],
        [-1, -golden_ratio, 0], [1, -golden_ratio, 0],
        [0, -1, golden_ratio], [0, 1, golden_ratio],
        [0, -1, -golden_ratio], [0, 1, -golden_ratio],
        [golden_ratio, 0, -1], [golden_ratio, 0, 1],
        [-golden_ratio, 0, -1], [-golden_ratio, 0, 1],
    ])

    # Normalize to unit sphere and scale to planet radius
    vertices /= np.linalg.norm(vertices[0])
    vertices *= config.radius

    faces = np.array([
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ])

    return vertices, faces


def subdivide(vertices, faces, depth):
    """Performs recursive subdivision of triangle faces."""
    midpoint_cache = {}
    vertices = list(vertices)

    def get_midpoint(v1, v2):
        key = tuple(sorted((v1, v2)))
        if key not in midpoint_cache:
            midpoint = (vertices[v1] + vertices[v2]) / 2
            midpoint /= np.linalg.norm(midpoint)
            midpoint *= config.radius
            midpoint_cache[key] = len(vertices)
            vertices.append(midpoint)
        return midpoint_cache[key]

    for _ in range(depth):
        new_faces = []
        for tri in faces:
            a = get_midpoint(tri[0], tri[1])
            b = get_midpoint(tri[1], tri[2])
            c = get_midpoint(tri[2], tri[0])
            new_faces.extend([
                [tri[0], a, c], [tri[1], b, a],
                [tri[2], c, b], [a, b, c]
            ])
        faces = np.array(new_faces)

    return np.array(vertices), faces


def build_adjacency(faces):
    """
    Builds an adjacency map for each face index based on shared vertices.
    Returns a dictionary: {face_index: set(neighbor_indices)}
    """
    adjacency = {i: set() for i in range(len(faces))}
    vertex_to_faces = {}
    for i, tri in enumerate(faces):
        for v in tri:
            vertex_to_faces.setdefault(v, set()).add(i)
    for i, tri in enumerate(faces):
        neighbors = set()
        for v in tri:
            neighbors.update(vertex_to_faces[v])
        neighbors.discard(i)
        adjacency[i] = neighbors
    return adjacency

