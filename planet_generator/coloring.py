# planet_generator/coloring.py

import numpy as np
from planet_generator import config
from .elevation.utils import get_height_amplitude


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
    height_amplitude = get_height_amplitude()

    lowland_max = sea_level + height_amplitude * config.plains_zone_threshold
    plains_max = sea_level + height_amplitude * config.foothills_zone_threshold
    foothill_max = sea_level + height_amplitude * config.mountain_zone_threshold
    mountain_max = sea_level + height_amplitude * config.mountain_peak_threshold
    trench_min = sea_level - height_amplitude * config.trench_zone_threshold

    face_colors = []

    for i, tri in enumerate(faces):
        center = np.mean([vertices[idx] for idx in tri], axis=0)
        latitude = get_latitude(center)
        elevation = face_elevations[i]

        if elevation < trench_min:
            # Ocean trench: black to dark blue
            norm = abs(elevation - min_elev) / abs(trench_min - min_elev)
            base_color = np.array([0.0, 0.0, 0.1 + 0.2 * norm])

        elif elevation < sea_level:
            # Regular ocean depth: dark blue to medium blue
            norm = abs(elevation - trench_min) / abs(sea_level - trench_min)
            base_color = np.array([0.0, 0.1 * norm, 0.3 + 0.4 * norm])

        elif elevation <= lowland_max:
            # Lowlands: sandy brown to swampy yellow-green
            norm = (elevation - sea_level) / (lowland_max - sea_level)
            base_color = np.array([0.4, 0.3, 0.15]) * (1 - norm) + np.array([0.6, 0.75, 0.2]) * norm

        elif elevation <= plains_max:
            # Plains: light green to dark pine green
            norm = (elevation - lowland_max) / (plains_max - lowland_max)
            base_color = np.array([0.5, 0.75, 0.3]) * (1 - norm) + np.array([0.1, 0.4, 0.1]) * norm

        elif elevation <= foothill_max:
            # Foothills: earthy-brown to gray-brown
            norm = (elevation - plains_max) / (foothill_max - plains_max)
            base_color = np.array([0.5, 0.4, 0.2]) * (1 - norm) + np.array([0.45, 0.4, 0.35]) * norm

        elif elevation <= mountain_max:
            # Mountains: gray-brown to light gray
            norm = (elevation - foothill_max) / (mountain_max - foothill_max)
            base_color = np.array([0.45, 0.4, 0.35]) * (1 - norm) + np.array([0.85, 0.85, 0.85]) * norm

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
