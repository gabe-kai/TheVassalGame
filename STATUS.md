# Project Status

`#/Status.md`

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
└── Status.md                                      - Human-readable project status, file map, and development notes.
```
