# Map Generator

The map generation tool for TheVassalGame. Generates the entire planet geography using an icosahedron-based approach with multiple levels of detail (LOD), from planet-scale to 1-meter resolution.

## Overview

The map generator creates a spherical planet representation by:
1. Starting with a base icosahedron (20 triangles)
2. Recursively subdividing triangles to create multiple LOD levels
3. Generating terrain data (heightmaps, biomes, resources) for each LOD level
4. Organizing data into zoomable tiles
5. Exporting in formats usable by the server and clients

## Features

- **Icosahedron-Based Planet**: Spherical representation using subdivided icosahedron
- **Multiple LOD Levels**: From planet-scale (low detail) to 1-meter resolution (high detail)
- **Progressive Detail**: Tiles increase in detail as you zoom in
- **Multiple Export Formats**: Binary, JSON, and image formats
- **Coordinate Integration**: Seamlessly integrates with 64-bit integer world coordinate system

## Technology Stack

- **Language**: Go (primary) or Rust (alternative)
- **Geometry**: Icosahedron subdivision algorithm
- **Compression**: LZ4 or gzip for heightmap data
- **Format**: MessagePack or custom binary for efficient storage

## Architecture

### Icosahedron Generator

- Creates base icosahedron (20 equilateral triangles)
- Recursively subdivides triangles (4:1 ratio per level)
- Maps triangles to world coordinates
- Handles spherical projection for 3D to 2D conversion

### Terrain Generator

- Generates heightmaps at each LOD level
- Assigns biomes based on terrain characteristics
- Places resource nodes
- Generates features (rivers, mountains, etc.)

### Tile System

- Organizes terrain data into zoomable tiles
- Manages LOD selection based on zoom level
- Handles tile indexing and caching
- Supports on-demand tile generation

### Export System

- Binary format for server/client consumption
- JSON format for metadata and configuration
- Image format for preview/visualization
- Compression for efficient storage

## Usage

### Standalone Tool

```bash
# Generate entire planet at low detail
./mapgen generate --planet --lod 0 --output ./maps/planet

# Generate specific region at high detail
./mapgen generate --region x,y --lod 10 --output ./maps/region

# Export existing tiles to different format
./mapgen export --input ./maps/planet --format binary --output ./maps/exported
```

### Integrated into Server

The map generator can also be integrated into the game server for on-demand generation:

```go
// Generate tile on-demand
tile := mapgen.GenerateTile(region, lodLevel)
```

## LOD Levels

- **Level 0**: Planet-scale (entire planet, very low detail)
- **Level 1-5**: Regional detail (continents, major features)
- **Level 6-10**: Local detail (cities, landmarks)
- **Level 11+**: High detail (1-meter resolution at maximum)

## Tile Structure

Each tile contains:
- Heightmap data (compressed)
- Biome/terrain type data
- Resource node positions
- Metadata (bounds, LOD level, parent tile reference)

## Coordinate System

- Uses the same 64-bit integer coordinate system as the game
- Icosahedron triangles map to world regions
- Tile coordinates map to chunk coordinates
- Seamless integration with existing chunk system

## Export Formats

### Binary Format (Server/Client)

Efficient binary format for runtime use:
- MessagePack or custom binary encoding
- Compressed heightmap data
- Optimized for fast loading

### JSON Format (Metadata)

Human-readable format for configuration:
- Tile metadata
- Generation parameters
- Coordinate mappings

### Image Format (Preview)

Optional preview images:
- Heightmap visualization
- Biome maps
- Resource node overlays

## Development

### Prerequisites

- Go 1.21+ or Rust 1.70+
- Geometry/math libraries for icosahedron operations
- Compression libraries (LZ4, gzip)

### Project Structure

```
/map-generator
├── cmd/
│   └── mapgen/           # Main application
├── internal/
│   ├── icosahedron/      # Icosahedron generation
│   ├── terrain/          # Terrain generation
│   ├── tiles/            # Tile management
│   └── export/           # Export formats
└── config/               # Configuration files
```

## Integration with Game Server

The map generator can work in two modes:

1. **Pre-Generation**: Generate entire planet at low detail, then generate detailed tiles on-demand
2. **On-Demand**: Generate tiles as needed when players explore new areas
3. **Hybrid**: Pre-generate common areas, generate others on-demand

## Performance Considerations

- **Memory**: High-detail tiles can be large; use streaming/chunking
- **Storage**: Compress heightmap data to reduce storage requirements
- **Generation Time**: Higher LOD levels take longer to generate
- **Caching**: Cache generated tiles to avoid regeneration

## Future Enhancements

- Procedural biome generation
- Climate system integration
- Dynamic terrain modification
- Multi-threaded generation
- GPU acceleration for heightmap generation

