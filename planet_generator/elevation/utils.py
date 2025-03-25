from planet_generator import config

def get_height_amplitude():
    """
    Computes height_amplitude as a ratio of the configured planet radius.
    Returns the absolute elevation range in km.
    """
    return config.radius * config.height_amplitude_ratio


def estimate_craton_count(total_faces: int, radius: float) -> int:
    """
    Estimate number of cratons based on total mesh faces and radius.

    Args:
        total_faces (int): Number of triangle faces on the mesh.
        radius (float): Planet radius in kilometers.

    Returns:
        int: Estimated number of cratons.
    """
    # Base calculation proportional to face count and radius
    base = total_faces * config.craton_density
    scale = (radius / config.craton_reference_radius) ** config.craton_exponent
    return max(int(base * scale), config.craton_min_count)
