# planet_generator/elevation/ocean.py

import numpy as np
from planet_generator import config


def generate_ocean_sphere(res_u=None, res_v=None):
    """
    Generates a UV sphere mesh for the ocean layer at config.radius.
    Returns:
        - ocean_vertices: np.ndarray of shape (N, 3)
        - ocean_faces: list of [i1, i2, i3] triangle indices
    """
    if res_u is None:
        res_u = config.ocean_u_resolution
    if res_v is None:
        res_v = config.ocean_v_resolution

    u, v = np.mgrid[0:2 * np.pi:res_u * 1j, 0:np.pi:res_v * 1j]
    r = config.radius

    x = r * np.cos(u) * np.sin(v)
    y = r * np.sin(u) * np.sin(v)
    z = r * np.cos(v)

    ocean_vertices = np.stack((x, y, z), axis=-1).reshape(-1, 3)
    ocean_faces = []

    for i in range(res_u - 1):
        for j in range(res_v - 1):
            a = i * res_v + j
            b = a + 1
            c = (i + 1) * res_v + j
            d = c + 1
            ocean_faces.append([a, b, d])
            ocean_faces.append([a, d, c])

    return np.array(ocean_vertices), ocean_faces
