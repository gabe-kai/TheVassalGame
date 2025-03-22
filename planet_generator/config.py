# planet_generator/config.py

# Planet geometry
radius = 25500                  # Base radius of the planet (km). Can be any positive float.
subdivision_depth = 6           # Icosphere detail level. Integer >= 0. Higher = more triangles.

# Noise & elevation
elevation_method = "tectonic"   # Options: "perlin" or "tectonic"
# Perlin parameters
noise_scale = 0.00005           # Controls frequency of terrain noise. Lower = larger features. Suggested: 0.00001–0.001
noise_offset_x = 0.3            # Horizontal shift of noise pattern. Can be any float.
noise_offset_y = 0.0            # Vertical shift of noise pattern. Can be any float.
noise_warp = 2.0                # Adds turbulence to noise. 0 = no warp. 1–5 = mild. >10 = chaotic.
octaves = 3                     # Number of Perlin noise layers. 1–6 recommended.
persistence = 0.5               # Falloff per octave. Range: 0–1. Lower = smoother terrain.
# Tectonic parameters
craton_count = 0                # If 0 it will be a function of the planets surface area.
oceanic_craton_fraction = 0.6   # At 0.5, half of cratons will be ocean plates

apply_elevation = True
height_amplitude = 1200         # Maximum elevation displacement in km. Suggested: 200–3000

# Ocean mesh & resolution (for export and plot)
generate_ocean = False          # Toggle ocean mesh generation and export
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
