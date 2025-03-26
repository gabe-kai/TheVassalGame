# Project Status

`/Status.md`

Purpose: A complete explanation of the project and its status for onboarding new ChatGPT conversations when the old one becomes too big and slow.

## Aggregated Daily Summary of GIT Commits
- `2025.03.21:` _Initial build of the icosphere generator and icosphere calculator. And first pass at debugging output._
- `2025.03.22:` _Refactored elevation.py into elevation library. Switched from perlin-noise continents to tectonic-method continents._
- `2025.03.23:` _Updated craton elevation generation. Updated feature elevations to scale off planet size. Added docstrings._
- `2025.03.24:` _Refactored tectonic.py into 5 tectonic\_{function}.py files. Added voronoi craton growth method._
- `2025.03.25:` _Added elevation zones & calibrated elevations. Switched craton slope from outward to inward. Added this status file._

---

## In-Progress

I've been attempting to calibrate values to get my landmasses to consistently generate in the right quantities at the right elevations.

- The average continental landmass is a bit too high while the average mountain range is too low.
- The continents edges are too straight and need more variation.
- Continents still have too many mountains ringing them, without enough gradual slopes into the ocean.

---

## TODOs

### 🌍 Elevation & Terrain Shaping
- [ ] Introduce post-boundary landscape noise for minor variation.
- [ ] Implement a falloff from mountain/trench extremes toward interior terrain.
- [ ] Explore plate-thickness and erosion-style variation.
- [ ] Add support for elevation 'masks' for scripted/hand-tuned worlds.

### 🧭 Craton Growth Improvements
- [ ] Improve edge detection for lowland coastal plains.
- [ ] Tune Voronoi distortion parameters for more organic coastline shapes.
- [ ] Experiment with region merging or small-plate smoothing.

### ⚙️ Performance & Refactoring
- [ ] Extract reusable utility functions across tectonic modules.
- [ ] Cache or accelerate geodesic distance calculations.
- [ ] Split long debug blocks into structured logging with optional verbosity levels.

### 🎨 Visualization & Output
- [ ] Improve elevation-based coloring blending at zone edges.
- [ ] Add optional overlays for tectonic plate boundaries and motion vectors.
- [ ] Export normal and elevation maps

### 🧪 Testing & Calibration
- [ ] Add sample test harness for debugging individual components.
- [ ] Document best `config.py` values for planets of different sizes.
- [ ] Add CLI flags or UI sliders for key generation parameters (in a future GUI).

---

## File & Folder Structure
```
# 📁 TheVassalGame
│
├── Documentation/                                - Notes, design docs, and visualizations (optional or planned).
│
├── planet_generator/
│   ├── __init__.py                                - Marks this folder as a Python package.
│   ├── coloring.py                                - Applies face coloring based on face elevations.
│   ├── config.py                                  - User controllable variables.
│   ├── export.py                                  - Handles exporting mesh and material data to OBJ/MTL files.
│   ├── geometry.py                                - Builds and subdivides the icosphere, adjacency, and face centers.
│   ├── icosphere_calculator.py                    - Standalone tool for basic icosphere calculations.
│   ├── main.py                                    - Main entry point: orchestrates geometry, elevation, and export.
│   ├── plot.py                                    - MatPlotLib icosphere displayer (old)
│   │
│   ├── elevation/
│   │   ├── __init__.py                            - Marks this folder as a Python subpackage.
│   │   ├── ocean.py                               - Optional or planned ocean-specific terrain shaping.
│   │   ├── perlin.py                              - Elevation generator using Perlin noise (alternative to tectonics).
│   │   ├── tectonic.py                            - Elevation orchestrator using tectonic-based systems.
│   │   ├── tectonic_boundary_interactions.py      - Handles elevation changes from plate collisions/divergence.
│   │   ├── tectonic_craton_growth.py              - Expands craton seeds via BFS or Voronoi distortion.
│   │   ├── tectonic_craton_seeding.py             - Seeds cratons and assigns tectonic types (continental/oceanic).
│   │   ├── tectonic_craton_sloping.py             - Slopes elevation inward (or outward) across cratons.
│   │   ├── utils.py                               - Shared elevation helpers (e.g. get_height_amplitude).
│   │
│   └── export/
│       ├── planet.obj                             - Exported 3D model mesh of the generated planet.
│       ├── planet.mtl                             - Associated material/texture references for the OBJ.
│
└── STATUS.md                                      - Human-readable project status, file map, and development notes.
```

---

## 🌍 Terrain Generation Control Summary

This table summarizes the main variables used in the tectonic boundary interaction phase and how they influence terrain shaping. These controls help tune elevation extremes and averages for land, ocean, and fault zones.

| **Target Feature**            | **Primary Variables**                           | **Effect / Description**                                                                |
|-------------------------------|-------------------------------------------------|-----------------------------------------------------------------------------------------|
| **Max mountain height**       | `cont_cont_converge`, `cont_ocean_converge_*`   | Controls tallest peaks at continental collisions and coastal ranges                     |
| **Avg mountain height**       | same as above + reduce randomness (`variation`) | Tones down average ridge elevation while still allowing tall peaks                      |
| **Avg land elevation**        | `compute_base_elevations()` (continental base)  | Sets overall starting elevation of continents before sloping or boundary shaping        |
| **Avg ocean depth**           | `compute_base_elevations()` (oceanic base)      | Sets base ocean level before trenches or mid-ocean ridges are applied                   |
| **Ocean trench depth**        | `cont_ocean_converge_ocean_side`                | Elevation drop for subducting oceanic plate at continental edges                        |
| **Mid-ocean ridges**          | `ocean_ocean_diverge`                           | Adds shallow ridges between diverging oceanic plates                                    |
| **Continental rifts**         | `cont_cont_diverge`                             | Lowers elevation between diverging continental plates                                   |
| **Coastal rifts**             | `cont_ocean_diverge`                            | Drop-off near coastal split zones (weaker than true trenches)                           |
| **Ocean-ocean collision**     | `ocean_ocean_converge_ratio`                    | Gentle elevation boost for oceanic convergence zones, scaled by current ocean depth     |
| **Fracture noise**            | `transform_variation`                           | Adds randomized elevation variation at transform boundaries (e.g. jagged coastlines)    |
| **Terrain steepness falloff** | Not directly here (consider smoothing)          | Can apply smoothing or falloff elsewhere for broader/milder terrain transitions         |

---

### 🔧 Tips for Fine-Tuning

- Use **base elevation** controls to globally lift/lower entire landmasses or seafloors.
- Use **converging/diverging multipliers** to localize shaping near tectonic edges.
- Keep **transform variation** subtle unless creating very broken or rugged terrain.
- Normalize only if needed, or tune so that terrain fits desired amplitude without post-scaling.

---

### Active Configuration Snapshot
- elevation_method: "tectonic"
- craton_growth_method: "voronoi"
- height_amplitude_ratio: 0.01
- oceanic_craton_fraction: 0.6
- radius: 25500
- subdivision_depth: 5

---

## Planet Creation Workflow

### 🧭 Program Flow Overview (main.py)

This program generates a 3D planet mesh with tectonic elevation, terrain coloring, and optional ocean rendering. The major steps are outlined below.

---

### 🌐 1. Build Icosphere Mesh
```python
vertices, faces = generate_base_icosahedron()
vertices, faces = subdivide(vertices, faces, config.subdivision_depth)
adjacency = build_adjacency(faces)
face_centers = compute_face_centers(faces, vertices)
```
- **generate_base_icosahedron()**: Starts with a simple icosahedron (20 triangle faces).
- **subdivide()**: Recursively subdivides each triangle face to increase mesh resolution.
- **build_adjacency()**: Constructs a map of neighboring faces for each face (needed for plate growth and boundary detection).
- **compute_face_centers()**: Calculates the center point (unit vector) of each triangle, used for slope gradients, motion vectors, and map coloring.

---

### 🏔️ 2. Elevation & Terrain Shaping
```python
face_elevations, assigned, motion_vectors = select_elevation_method(vertices, faces, face_centers, adjacency)
```
- Dispatches to the method specified in `config.elevation_method` ("tectonic" or "perlin").
- In the **tectonic** method:
  - Seeds tectonic cratons with types (continental/oceanic).
  - Grows cratons using BFS or Voronoi distortion.
  - Assigns motion vectors per plate.
  - Computes elevation change from tectonic boundary interactions.
  - Applies smoothing and craton sloping.
  - Normalizes final elevations relative to sea_level and height_amplitude.

---

### 🎨 3. Terrain Coloring
```python
face_colors = apply_face_coloring(vertices, faces, face_elevations)
```
- Applies elevation-based color shading to faces.
- Optionally blends in features like longitude, terrain zones, or plate overlays.

---

### 🌊 4. Optional Ocean Mesh
```python
if config.generate_ocean:
    ocean_vertices, ocean_faces = generate_ocean_sphere()
```
- Generates a slightly larger duplicate UVSphere to serve as a stylized ocean shell.
- This mesh renders as water in 3D modeling software and helps visualize sea level.

---

### 💾 5. Export to OBJ/MTL
```python
export_obj_and_mtl(vertices, faces, face_colors, ocean_vertices, ocean_faces)
```
- Saves the mesh and colors to `.obj` and `.mtl` files.
- Compatible with Blender, Unity, or other 3D tools for inspection and rendering.

---

### 🧪 Debug Output
If `config.debug_mode = True`, debug output includes:
- Craton seeding stats
- Plate type counts
- Growth completion and unassigned face checks
- Elevation range and classification thresholds
- Motion vectors and boundary interactions

---

### 📂 Output Files
| File                  | Description                           |
|-----------------------|---------------------------------------|
| `export/planet.obj`   | 3D model of the generated terrain     |
| `export/planet.mtl`   | Color and material references         |


## Methodology Choices

### Icosphere Over UVSphere
We chose an **icosphere** for our planet mesh rather than a UV sphere due to its more uniform triangle distribution. UV spheres distort heavily at the poles, which led to poor craton distribution and irregular shapes in tectonic plate assignments. Icospheres provide consistent geometry for procedural face-based simulations.

### Custom Craton-Based Tectonic Method Over Perlin Noise
While Perlin noise is fast and visually appealing, it lacks geological plausibility for simulating large landmasses or tectonic interactions. We implemented a **custom tectonic system** that builds elevation through:
- Craton seeding (continental/oceanic plate origins)
- Plate spreading using BFS or Voronoi
- Boundary interaction rules
- Craton edge-inward sloping

This results in more realistic continental shelves, ocean trenches, rift valleys, and mountainous regions.

### Voronoi Craton Growth Over BFS
The original BFS-based craton growth suffered from uneven fill, especially when using fewer cratons (e.g. large supercontinents). We replaced it with a **Voronoi-partitioned growth** system, using geodesic distances and optional distortion noise to:
- Ensure consistent global coverage
- Allow variable plate sizes via weight multipliers
- Add organic, non-circular continent outlines

### Precomputed Face Centers and Adjacency
To reduce redundant calculations and improve modularity, we precompute and reuse:
- `face_centers`: unit vectors for triangle centroids, used for slopes and distances
- `adjacency`: face neighbor relationships, essential for boundary logic and BFS

### Elevation Tuning via Plate Interactions
Rather than relying solely on noise or masks, we control terrain features through **boundary rules**. Each plate boundary type (converge/diverge/transform) triggers elevation offsets, with separate controls for oceanic/continental sides. This allows detailed tuning of features like:
- Coastal cliffs
- Mid-ocean ridges
- Mountain arcs
- Subduction trenches

### Post-Processing with Normalization
In later stages, we normalize the elevation output to match the configured `height_amplitude`, preserving sea level and re-scaling terrain while retaining relative differences.

---

### Abandoned or Replaced Approaches
| Rejected Method          | Replaced With                   | Reason                                                        |
|--------------------------|---------------------------------|---------------------------------------------------------------|
| UV Sphere                | Icosphere                       | Severe pole distortion; uneven face sizes                     |
| Perlin-only elevation    | Craton-based tectonics          | Hard to constrain into natural-looking continents             |
| BFS-only craton fill     | Voronoi growth w/ distortion    | BFS made donut shapes, especially with low seed counts        |
| Runtime face center calc | Precomputed face centers        | Reduced redundancy and simplified slope/distance calculations |
