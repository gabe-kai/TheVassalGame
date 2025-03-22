# planet_generator/coloring.py

import numpy as np
from planet_generator import config


def get_latitude(vertex):
    """Returns the latitude in degrees of a vertex's Z position relative to the planet radius."""
    z_normalized = np.clip(vertex[2] / config.radius, -1.0, 1.0)
    return np.degrees(np.arcsin(z_normalized))


def apply_face_coloring(vertices, faces, face_elevations):
    """
    Returns a list of RGB tuples representing the color of each face based on elevation and latitude.
    Below sea level: blue-black gradient
    Above sea level: green elevation gradient
    All adjusted by polar and tropical overlays.
    """
    min_elev = min(face_elevations)
    max_elev = max(face_elevations)

    # Define elevation zones based on global amplitude and sea level
    sea_level = config.sea_level
    height_amplitude = config.height_amplitude

    grassline_max = sea_level + height_amplitude * 0.29       # upper bound of grasslands
    foothill_max = sea_level + height_amplitude * 0.42        # upper bound of foothills
    mountain_max = sea_level + height_amplitude * 0.58        # upper bound of rocky mountains

    face_colors = []

    for i, tri in enumerate(faces):
        center = np.mean([vertices[idx] for idx in tri], axis=0)
        latitude = get_latitude(center)
        elevation = face_elevations[i]

        if elevation < sea_level:
            # Ocean depth: dark blue at deepest, lighter blue near sea level
            norm = abs(elevation) / abs(min_elev) if min_elev != 0 else 0
            base_color = np.array([0.0, 0.05 + 0.2 * (1 - norm), 0.3 + 0.5 * (1 - norm)])

        elif elevation <= grassline_max:
            # Grasslands: light green to yellow-green
            norm = (elevation - sea_level) / (grassline_max - sea_level)
            base_color = np.array([0.3 * norm, 0.6 + 0.3 * norm, 0.2 * (1 - norm)])

        elif elevation <= foothill_max:
            # Foothills: yellow-green to brown-gray
            norm = (elevation - grassline_max) / (foothill_max - grassline_max)
            base_color = np.array([0.6 - 0.2 * norm, 0.8 - 0.6 * norm, 0.3 * norm])

        elif elevation <= mountain_max:
            # Mountains: brown-gray to light gray
            norm = (elevation - foothill_max) / (mountain_max - foothill_max)
            base_color = np.array([0.6, 0.6, 0.6]) * (1 - norm) + np.array([0.85, 0.85, 0.85]) * norm

        else:
            # Snow-capped peaks: light gray to white
            norm = min((elevation - mountain_max) / (height_amplitude - (mountain_max - sea_level)), 1.0)
            base_color = np.array([0.85, 0.85, 0.85]) * (1 - norm) + np.array([1, 1, 1]) * norm

        # Polar fade to white
        if config.enable_polar_overlay and abs(latitude) >= config.polar_latitude:
            fade = min(1, (abs(latitude) - config.polar_latitude) / config.polar_fade_range)
            base_color = base_color * (1 - fade) + np.array([1, 1, 1]) * fade

        # Tropical fade to orange
        elif config.enable_tropical_overlay and abs(latitude) <= config.tropical_latitude + config.tropical_fade_range:
            fade = max(0, 1 - (abs(latitude) - config.tropical_latitude) / config.tropical_fade_range)
            base_color = base_color * (1 - fade) + np.array([1, 0.85, 0.6]) * fade

        face_colors.append(tuple(np.clip(base_color, 0, 1)))

    return face_colors


def apply_ocean_coloring(vertices, faces):
    """
    Returns a list of RGB tuples for ocean faces based on latitude only.
    Base color is a very light blue, tinted polar or tropical.
    """
    face_colors = []

    for tri in faces:
        center = np.mean([vertices[idx] for idx in tri], axis=0)
        latitude = get_latitude(center)
        base_color = np.array([0.7, 0.85, 1.0])  # very light blue

        if abs(latitude) >= config.polar_latitude:
            fade = min(1, (abs(latitude) - config.polar_latitude) / config.polar_fade_range)
            base_color = base_color * (1 - fade) + np.array([1, 1, 1]) * fade

        elif abs(latitude) <= config.tropical_latitude + config.tropical_fade_range:
            fade = max(0, 1 - (abs(latitude) - config.tropical_latitude) / config.tropical_fade_range)
            base_color = base_color * (1 - fade) + np.array([1, 0.6, 0]) * fade

        face_colors.append(tuple(np.clip(base_color, 0, 1)))

    return face_colors
