# planet_generator/elevation/tectonic_craton_seeding.py

from planet_generator import config


def seed_cratons_with_types(total_faces, count, rng):
    """
    Seeds cratons on random faces and assigns each one a tectonic type.

    This replaces the separate steps of seeding cratons and assigning plate types.
    Each seed is chosen randomly and assigned as 'continental' or 'oceanic'
    based on the configured oceanic_craton_fraction.

    Args:
        total_faces (int): Number of mesh faces on the planet.
        count (int): Number of cratons to seed.
        rng (np.random.Generator): Random number generator.

    Returns:
        tuple:
            - List[int]: Craton seed face indices.
            - Dict[int, str]: Mapping from seed index to 'continental' or 'oceanic'.
    """
    if config.debug_mode:
        print("[DEBUG] Seeding cratons and assigning plate types...")

    oceanic = 0
    continental = 0

    craton_seeds = rng.choice(total_faces, size=count, replace=False)
    plate_types = {}

    for seed in craton_seeds:
        if rng.random() < config.oceanic_craton_fraction:
            plate_types[seed] = "oceanic"
            if config.debug_mode:
                oceanic += 1
        else:
            plate_types[seed] = "continental"
            if config.debug_mode:
                continental += 1

    if config.debug_mode:
        print(f"[DEBUG] Plate types assigned: {continental} continental, {oceanic} oceanic")

    return craton_seeds.tolist(), plate_types
