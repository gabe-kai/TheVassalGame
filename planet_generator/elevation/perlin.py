# planet_generator/elevation/perlin.py

import numpy as np
from noise import pnoise3
from planet_generator import config


def compute_perlin_elevation(vertices, faces):
    """
    Applies fractal noise-based elevation to each face and modifies vertices in-place.
    Returns:
        - face_elevations: list of elevation values per face
    """
    face_elevations = []

    for tri in faces:
        amplitude = 1.0
        frequency = config.noise_scale
        noise_value = 0

        for _ in range(config.octaves):
            noise_value += amplitude * pnoise3(
                vertices[tri[0]][0] * frequency + config.noise_offset_x,
                vertices[tri[1]][1] * frequency + config.noise_offset_y,
                vertices[tri[2]][2] * frequency
            )
            frequency *= 2
            amplitude *= config.persistence

        # Stretch noise range from ~[-0.5, 0.5] → [-1, 1]
        avg_noise = (noise_value / config.octaves) * 2
        elevation = avg_noise * config.height_amplitude
        face_elevations.append(elevation)

        if config.apply_elevation:
            for idx in tri:
                direction = vertices[idx] / np.linalg.norm(vertices[idx])
                vertices[idx] = direction * (config.radius + elevation)

    if config.debug_mode:
        min_elev = min(face_elevations)
        max_elev = max(face_elevations)
        print(f"[DEBUG] Elevation range: min = {min_elev:.2f} km, max = {max_elev:.2f} km")

    return face_elevations
