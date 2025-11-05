# Seed Data

This directory contains seed data files for initializing the game database with default content.

## Building Types

### `buildings.yaml` (or `buildings.json`)
Contains the initial building types, their tiers, and signature additions.

**Format**: YAML or JSON
- Human-readable
- Easy to edit and review
- Can be converted to SQL or loaded directly by the server

**Usage**:
- For Go server: Load via YAML/JSON parser and insert into database
- For database initialization: Convert to SQL INSERT statements
- Can be used by admin tools to populate building types

## Structure

Each building type entry should include:
- Basic properties (name, category, building_path, description)
- Geometry (footprint_polygon, door_positions)
- Construction properties (base_build_time, base_cost_data)
- Building properties (health, durability, employment, etc.)
- All 6 tiers with their properties
- Signature additions for each tier
- Supply chain associations (if any)

## Migration Strategy

1. **Design Phase**: Use `docs/building-types-reference.md` for planning
2. **Implementation**: Create structured data files here
3. **Database**: Convert to SQL migrations or use Go code to load data
4. **Admin Tools**: Can import from these files to populate database

