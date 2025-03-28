# planet_generator/config.py

# Planet geometry
radius = 25500                  # Base radius of the planet (km). Can be any positive float.
subdivision_depth = 6           # Icosphere detail level. Integer >= 0. Higher = more triangles.

# Noise & elevation
apply_elevation = True
elevation_method = "tectonic"   # Options: "perlin" or "tectonic"
height_amplitude_ratio = 0.01   # Max elevation = ±5% of planet radius (Earth = 0.0017 - 0.0025)
sea_level = 0.0                 # Base elevation of sea level

# Perlin parameters
noise_scale = 0.00005           # Controls frequency of terrain noise. Lower = larger features. Suggested: 0.00001–0.001
noise_offset_x = 0.3            # Horizontal shift of noise pattern. Can be any float.
noise_offset_y = 0.0            # Vertical shift of noise pattern. Can be any float.
noise_warp = 2.0                # Adds turbulence to noise. 0 = no warp. 1–5 = mild. >10 = chaotic.
octaves = 3                     # Number of Perlin noise layers. 1–6 recommended.
persistence = 0.5               # Falloff per octave. Range: 0–1. Lower = smoother terrain.

# Tectonic parameters
craton_density = 0.0001         # Higher means more tectonic plates for a given mesh density
craton_exponent = 1.5           # Higher makes the craton count scale more strongly with planet size.
craton_reference_radius = 6371  # Earth-like baseline
craton_min_count = 7            # Keep the number odd to prevent quadrant or evenly-split halves
oceanic_craton_fraction = 0.6   # At 0.5, half of cratons will be ocean plates
craton_growth_method = "voronoi"    # Choose "bfs" or "voronoi"

# Terrain classification thresholds (as fractions of height_amplitude)
plains_zone_threshold = 0.10     # Anything above this is considered plains, anything below is lowlands
foothills_zone_threshold = 0.29  # Anything above this is considered hills
mountain_zone_threshold = 0.42   # Anything above this is considered mountainous
mountain_peak_threshold = 0.58   # Anything above this is considered mountain peaks
trench_zone_threshold = 0.40     # Anything below this is considered trench

# Ocean mesh & resolution (for export and plot)
generate_ocean = False          # Toggle ocean mesh (as a separate object) generation and export
ocean_u_resolution = 128        # Horizontal segments (longitude)
ocean_v_resolution = 64         # Vertical segments (latitude)

# Climate zones (latitude-based tints)
enable_polar_overlay = True     # Apply white polar caps
enable_tropical_overlay = False # Apply orange tropical zones
polar_latitude = 60             # Degrees from equator to start polar fade. Range: 0–90
tropical_latitude = 13.5        # Degrees from equator to start tropical tint
polar_fade_range = 10           # Degrees over which polar fade occurs
tropical_fade_range = 20        # Degrees over which tropical fade occurs

# Qi Pools
qi_pool_percentage = 0.1        # Fraction of total faces. Range: 0.0–1.0
qi_pool_seed = 42               # Random seed. Any integer.

# OBJ export settings
posterize_levels = 16           # Reduces unique colors. Use 8–64 for visual quality vs. file size
export_dir = "export"           # Folder for output files (will be created if missing)
convert_to_y_up = True          # If True, rotates geometry from Z-up to Y-up for compatibility with Object Viewer

# Rendering flags
show_edges = False              # Toggle triangle edge outlines in plot
debug_mode = True               # Enables verbose debug printouts
