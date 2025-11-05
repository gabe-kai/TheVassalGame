# Building Placement Mechanics

## Table of Contents
- [Overview](#overview)
- [Building Footprints](#building-footprints)
- [Door Accessibility](#door-accessibility)
- [Placement Validation](#placement-validation)
- [Terrain Modification](#terrain-modification)
- [Proximity Bonuses](#proximity-bonuses)
- [Automatic Road Generation](#automatic-road-generation)
- [Building Relocation](#building-relocation)
- [Qi Source Proximity](#qi-source-proximity)
- [Placement Constraints](#placement-constraints)

## Overview

Building placement is a core mechanic that determines where structures can be constructed. Buildings have polygonal footprints, require door accessibility, benefit from proximity to supply chain buildings, and can trigger automatic road generation. Some buildings can be relocated, and terrain may need modification for placement.

**Key Principles:**
- **Polygonal Footprints**: Buildings use polygon shapes, not simple rectangles
- **Door Accessibility**: All door positions must be accessible from paths/roads
- **Proximity Bonuses**: Buildings benefit from being near supply chain partners
- **Automatic Roads**: Frequently traveled paths become roads automatically
- **Relocatable**: Some buildings can be deconstructed and relocated
- **Terrain Modification**: Land may need landscaping or supports for placement

---

## Building Footprints

### Polygon-Based Footprints

**Footprint Definition:**
- Each building has a `footprint_polygon` defined as a JSONB array of vertices
- Vertices are relative to building center (0, 0)
- Polygon must be closed (first vertex = last vertex, or system closes it)
- Polygon must be convex or simple concave (no self-intersections)

**Example Footprint:**
```json
{
  "vertices": [
    {"x": -5, "y": -3},
    {"x": 5, "y": -3},
    {"x": 5, "y": 3},
    {"x": -2, "y": 3},
    {"x": -2, "y": 1},
    {"x": -5, "y": 1},
    {"x": -5, "y": -3}
  ]
}
```

**Polygon Properties:**
- **Area**: Calculated using shoelace formula
- **Bounding Box**: Minimum rectangle that contains polygon
- **Center Point**: Building center (world_x, world_y)
- **Rotation**: Building can be rotated (affects footprint polygon)

**Rotation:**
- Buildings can be rotated around their center point
- Rotation angle in radians (0 to 2π)
- Polygon vertices are transformed by rotation matrix
- Some buildings may have rotation restrictions (e.g., must face north)

**Footprint Validation:**
- All vertices must form a valid polygon
- Polygon area must be > 0
- Polygon must not self-intersect
- Maximum polygon size: 100m × 100m (bounding box)

---

## Door Accessibility

### Door Positions

**Door Definition:**
- Each building has `door_positions` defined as JSONB array
- Door positions are relative to building center
- Each door has: `x`, `y`, `facing` (angle in radians)

**Example Door Positions:**
```json
[
  {"x": 0, "y": -3, "facing": 1.57},  // South door, facing north
  {"x": 5, "y": 0, "facing": 3.14}   // East door, facing west
]
```

**Accessibility Requirements:**
- All door positions must be accessible from paths/roads
- Accessibility check: Path exists within 3 meters of door
- Door must not be blocked by terrain, buildings, or obstacles
- Door must be reachable by units (pathfinding can reach door)

**Accessibility Validation:**
1. **Path Check**: System checks if path/road exists within 3m of door position
2. **Terrain Check**: Door position must not be on impassable terrain
3. **Obstacle Check**: No buildings, structures, or obstacles block door
4. **Pathfinding Check**: Units must be able to pathfind to door (within 10m)

**Accessibility Failure:**
- If any door is inaccessible, placement is invalid
- Error message: "Door at position (x, y) is not accessible"
- Player must adjust placement or add paths/roads first

**Door Placement Rules:**
- Doors typically placed on polygon edges
- Doors should face outward (toward accessible area)
- Large buildings may have multiple doors
- Doors can be on any side of building

---

## Placement Validation

### Validation Checks

**Step 1: Footprint Validation**
- Check if footprint polygon fits within territory boundaries
- Check if footprint overlaps with existing buildings (polygon collision)
- Check if footprint overlaps with resource nodes
- Check if footprint is on valid terrain (not water, not impassable)

**Step 2: Terrain Suitability**
- Check terrain slope (maximum 15° for most buildings)
- Check elevation (some buildings require specific elevation)
- Check terrain type (some buildings require specific terrain)
- Check if terrain modification is needed

**Step 3: Door Accessibility**
- Check all door positions are accessible
- Verify paths/roads exist near doors
- Verify no obstacles block doors

**Step 4: Resource Requirements**
- Check player has required resources (after skill bonuses)
- Check player has permission (territory ownership)
- Check building is unlocked (tier/tech requirements)

**Step 5: Proximity Requirements**
- Check qi source proximity (if building requires qi source)
- Check distance from other buildings (if building has minimum distance requirement)
- Check distance from specific building types (if building has restrictions)

**Validation Result:**
- **Valid**: Green preview, building can be placed
- **Invalid**: Red preview with error message explaining why

### Collision Detection

**Polygon Collision:**
- Use Separating Axis Theorem (SAT) for polygon collision detection
- Check building footprint against all existing building footprints
- Check building footprint against resource nodes
- Check building footprint against terrain obstacles

**Minimum Distance:**
- Some buildings require minimum distance from other buildings
- Default: 1 meter minimum (prevents overlapping)
- Some buildings: 5-10 meters (defensive structures, large buildings)

**Collision Resolution:**
- If collision detected: Placement invalid
- Error message: "Building overlaps with [existing building/resource node]"
- Player must move building to non-colliding location

---

## Terrain Modification

### Landscaping Requirements

**Terrain Analysis:**
- System analyzes terrain within footprint polygon
- Checks slope, elevation variance, terrain type
- Determines if terrain modification is needed

**Slope Requirements:**
- **Most Buildings**: Maximum 15° slope
- **Large Buildings**: Maximum 10° slope
- **Defensive Structures**: Maximum 20° slope (can be built on hills)
- **Special Buildings**: May have specific slope requirements

**Elevation Requirements:**
- **Standard Buildings**: Elevation variance ≤ 2 meters within footprint
- **Large Buildings**: Elevation variance ≤ 1 meter within footprint
- **Special Buildings**: May require specific elevation (e.g., near water)

**Terrain Modification Process:**
1. **Terrain Analysis**: System checks terrain suitability
2. **Modification Calculation**: Calculates required terrain changes
3. **Cost Calculation**: Determines landscaping cost (resources, time)
4. **Player Confirmation**: Player approves terrain modification
5. **Terrain Modification**: System flattens/elevates terrain as needed

**Landscaping Costs:**
- **Flattening**: 10% of build cost, 20% of build time
- **Elevation Changes**: 15% of build cost, 25% of build time
- **Major Terrain Modification**: 25% of build cost, 40% of build time
- **Terrain Modification Tools**: May require specific tools/workers

**Terrain Modification Limits:**
- Maximum elevation change: ±5 meters
- Maximum slope reduction: 20° to 5°
- Cannot modify terrain outside building footprint
- Cannot modify terrain that would affect other buildings

### Building Supports

**Support Requirements:**
- Some buildings require supports on steep terrain
- Supports needed if slope > 10° or elevation variance > 3 meters
- Supports provide structural stability

**Support Types:**
- **Foundation Supports**: Basic supports for elevation differences
- **Slope Supports**: Supports for buildings on slopes
- **Advanced Supports**: Complex supports for large buildings on difficult terrain

**Support Costs:**
- **Foundation Supports**: +5% build cost, +10% build time
- **Slope Supports**: +10% build cost, +15% build time
- **Advanced Supports**: +20% build cost, +25% build time

**Support Calculation:**
```
support_needed = false
if (max_slope > 10°) support_needed = true
if (elevation_variance > 3m) support_needed = true
if (terrain_type == 'swamp' || terrain_type == 'sand') support_needed = true

if (support_needed):
  support_type = determine_support_type(slope, elevation, terrain)
  support_cost = calculate_support_cost(support_type, footprint_area)
```

**Support Placement:**
- Supports placed automatically at corners and edges
- Supports visible as building foundation elements
- Supports integrated into building structure

---

## Proximity Bonuses

### Supply Chain Proximity

**Proximity Bonus System:**
- Buildings receive bonuses when placed near supply chain partners
- Bonus increases with proximity (closer = better)
- Multiple supply chain buildings stack bonuses

**Proximity Bonus Formula:**
```
proximity_bonus = sum(base_bonus × (1 - distance / max_distance))

Where:
- base_bonus = 0.05 (5% per supply chain building)
- max_distance = proximity_bonus_range (default: 50 meters)
- distance = meters to supply chain building
```

**Proximity Bonus Range:**
- Default: 50 meters
- Some buildings: 100 meters (large buildings)
- Some buildings: 25 meters (small buildings)
- Configurable per building type

**Bonus Stacking:**
- Multiple supply chain buildings in range: Bonuses stack additively
- Maximum bonus: 25% (configurable)
- Example: 3 supply chain buildings at 25m each = 15% bonus

**Proximity Bonus Types:**
- **Production Efficiency**: Increased production rate
- **Resource Generation**: Increased resource output
- **Cost Reduction**: Reduced resource costs
- **Quality Improvement**: Improved output quality

**Dynamic Proximity Updates:**
- Proximity bonuses recalculated when:
  - New buildings constructed nearby
  - Buildings demolished nearby
  - Buildings relocated
- Updates occur automatically every 5 minutes
- Player sees bonus preview when placing building

**Proximity Preview:**
- When placing building, system shows:
  - Nearby supply chain buildings
  - Proximity bonus estimate
  - Optimal placement suggestions

---

## Automatic Road Generation

### Path Tracking System

**Path Usage Tracking:**
- System tracks unit movement between buildings
- Records path segments (from building A to building B)
- Tracks frequency: How many times path is used
- Tracks time: How long path has been active

**Path Data Structure:**
```json
{
  "path_id": 123,
  "start_building_id": 100,
  "end_building_id": 200,
  "waypoints": [
    {"x": 1000, "y": 2000},
    {"x": 1200, "y": 2100},
    {"x": 1400, "y": 2200}
  ],
  "usage_count": 150,
  "last_used_at": "2024-01-21T15:30:00Z",
  "path_quality": "path"  // "none", "path", "rough_road", "road", "nice_road"
}
```

**Path Quality Levels:**
1. **None**: No visible path (0-10 uses)
2. **Path**: Visible trail in grass/terrain (11-50 uses)
3. **Rough Road**: Dirt road, visible but rough (51-150 uses)
4. **Road**: Standard road, well-traveled (151-500 uses)
5. **Nice Road**: Paved/improved road, high quality (501+ uses)

### Road Generation Process

**Step 1: Path Detection**
- System detects when units frequently travel between buildings
- Tracks path usage over time (daily/weekly)
- Identifies path segments that exceed threshold

**Step 2: Path Quality Upgrade**
- When usage threshold reached, path quality upgrades
- Upgrade is automatic (no player action required)
- Visual change: Terrain shows path/road

**Step 3: Road Benefits**
- **Path**: +5% movement speed
- **Rough Road**: +10% movement speed
- **Road**: +15% movement speed
- **Nice Road**: +20% movement speed

**Usage Thresholds:**
- **Path**: 10 uses (units traveling between buildings)
- **Rough Road**: 50 uses
- **Road**: 150 uses
- **Nice Road**: 500 uses

**Time-Based Decay:**
- Paths decay if not used for extended period
- **Path**: Decays after 7 days of no use
- **Rough Road**: Decays after 14 days of no use
- **Road**: Decays after 30 days of no use
- **Nice Road**: Decays after 90 days of no use

**Road Maintenance:**
- Roads may require maintenance (rare, high-traffic roads)
- Maintenance prevents road decay
- Maintenance cost: Minimal resources

### Road Placement Rules

**Automatic Placement:**
- Roads follow unit pathfinding routes
- Roads connect building doors to other buildings
- Roads avoid obstacles and terrain

**Road Width:**
- **Path**: 1 meter wide
- **Rough Road**: 2 meters wide
- **Road**: 3 meters wide
- **Nice Road**: 4 meters wide

**Road Merging:**
- Multiple paths to same destination merge into single road
- Merged roads use highest quality level
- Road network forms naturally from unit movement

**Road Benefits for Buildings:**
- Buildings with roads nearby have better door accessibility
- Roads improve NPC pathfinding efficiency
- Roads reduce travel time between buildings

---

## Building Relocation

### Relocatable Buildings

**Relocation Eligibility:**
- Only buildings with `relocatable = TRUE` can be relocated
- Some buildings are permanently placed (cannot relocate)
- Buildings under construction cannot be relocated

**Relocation Process:**
1. **Initiate Relocation**: Player selects building, chooses relocate option
2. **Deconstruction**: Building is deconstructed (if required)
3. **Resource Recovery**: Resources recovered (percentage of build cost)
4. **New Placement**: Player places building at new location
5. **Reconstruction**: Building reconstructed at new location

**Relocation Costs:**
- **Cost**: `relocation_cost_multiplier × build_cost` (default: 50% of build cost)
- **Time**: `relocation_time_multiplier × build_time` (default: 30% of build time)
- **Resource Recovery**: 75% of original build cost returned (if deconstructed)

**Relocation Requirements:**
- **Workers**: Relocation may require workers (if `relocation_requires_workers = TRUE`)
- **Resources**: Player must have relocation cost resources
- **Valid Location**: New location must pass all placement validation

**Relocation State:**
- Building marked as `is_relocating = TRUE` during relocation
- Building becomes non-functional during relocation
- Workers assigned to relocation (if required)
- Relocation progress tracked: 0.0 to 1.0

**Relocation Limitations:**
- Cannot relocate during construction
- Cannot relocate if building is damaged (health < 50%)
- Cannot relocate if building has active workers (must remove workers first)
- Cannot relocate if building is in combat

### Deconstruction

**Deconstruction Process:**
- Buildings can be deconstructed (demolished intentionally)
- Deconstruction returns resources: `demolition_resource_return × build_cost` (default: 25%)
- Deconstruction time: 50% of build time
- Deconstruction requires workers (if building requires workers)

**Deconstruction vs Destruction:**
- **Deconstruction**: Intentional demolition, returns resources
- **Destruction**: Combat/event damage, no resource return

**Deconstruction Requirements:**
- Building must be owner's (or player has permission)
- Building must not be in combat
- Workers must be removed (if building requires workers)

---

## Qi Source Proximity

### Qi Source Requirements

**Qi Source Dependencies:**
- Some buildings require proximity to qi sources
- Qi sources: Qi Veins, Qi Pools, Ley Lines
- Proximity affects building efficiency and qi absorption

**Qi Source Proximity Formula:**
```
local_ambient_qi = base_territory_qi × (1 + qi_source_proximity_bonus)

Where:
qi_source_proximity_bonus = qi_source_potency × (1 - distance / max_range) × 0.5

- qi_source_potency: Strength of qi source (1.0 to 3.0)
- distance: Meters to qi source
- max_range: Maximum range for qi source effect (default: 200 meters)
```

**Qi Source Proximity Bonuses:**
- **0-50m**: 100% of qi source potency
- **50-100m**: 75% of qi source potency
- **100-150m**: 50% of qi source potency
- **150-200m**: 25% of qi source potency
- **200m+**: No bonus

**Required vs Recommended:**
- **Required**: Building cannot function without qi source within range
- **Recommended**: Building benefits from qi source but can function without

**Qi Source Building Types:**
- **Qi Condensers**: Require qi source (high efficiency near source)
- **Cultivation Halls**: Require qi source (cultivators need ambient qi)
- **Spirit Buildings**: Require qi source (spirit-infused construction)

**Placement Validation:**
- If building requires qi source: Check qi source within required range
- If no qi source: Placement invalid, error message shown
- If qi source too far: Placement invalid, show distance to nearest source

---

## Placement Constraints

### Territory Constraints

**Territory Ownership:**
- Buildings can only be placed in player's owned territories
- Buildings cannot be placed in unclaimed territories
- Buildings cannot be placed in other players' territories

**Territory Boundaries:**
- Building footprint must be entirely within territory boundaries
- Building cannot span multiple territories
- Building center must be within territory

**Territory Status:**
- Buildings can be placed in `secured` territories
- Buildings cannot be placed in `contested` territories (during contest)
- Buildings can be placed in `claimed` territories (if defended)

### Terrain Constraints

**Terrain Type Restrictions:**
- **Water**: Most buildings cannot be placed on water
- **Swamp**: Some buildings require supports on swamp
- **Mountain**: Some buildings require flat terrain modification
- **Forest**: Some buildings require clearing trees first

**Terrain Type Requirements:**
- **Farmland**: Requires fertile soil (plains, river valleys)
- **Quarries**: Requires rocky terrain (mountains, hills)
- **Ports**: Requires coastal terrain (water access)
- **Mines**: Requires appropriate terrain (mountains, hills)

**Elevation Constraints:**
- **Standard Buildings**: Elevation 0-500m above sea level
- **Mountain Buildings**: Elevation 500-2000m (special buildings)
- **Valley Buildings**: Elevation 0-200m (some buildings prefer valleys)

### Building-Specific Constraints

**Minimum Distance:**
- Some buildings require minimum distance from other buildings
- **Defensive Structures**: 10 meters from other buildings
- **Large Buildings**: 5 meters from other buildings
- **Standard Buildings**: 1 meter minimum (prevents overlap)

**Maximum Distance:**
- Some buildings require maximum distance from specific types
- **Housing**: Cannot be too far from resources (max 200m from food source)
- **Production**: Cannot be too far from supply chain (max 100m recommended)

**Category Restrictions:**
- Some buildings cannot be placed near certain categories
- **Defensive Structures**: Cannot be too close to civilian buildings (safety)
- **Production Buildings**: Cannot be too close to housing (pollution)

### Resource Constraints

**Resource Requirements:**
- Player must have required resources (after skill bonuses)
- Resources checked before placement validation
- Insufficient resources: Placement invalid

**Unlock Requirements:**
- Building must be unlocked (tier/tech requirements)
- Player must have required tier/tech level
- Unlocked buildings shown in building menu

---

## Placement Workflow

### Placement Process

**Step 1: Building Selection**
- Player opens building menu
- System shows available buildings (unlocked, affordable)
- Player selects building type
- System shows building properties:
  - Footprint polygon preview
  - Door positions
  - Resource costs
  - Build time
  - Proximity bonus preview

**Step 2: Placement Mode**
- Client enters placement mode
- Player sees building preview (ghost building) with:
  - Footprint polygon outline
  - Door positions marked
  - Rotation controls (if applicable)
- Preview updates in real-time as player moves mouse

**Step 3: Real-Time Validation**
- Client validates placement as player moves building:
  - Footprint collision check
  - Terrain suitability check
  - Door accessibility check
  - Proximity bonus preview
  - Qi source proximity check (if required)
- Preview color:
  - **Green**: Valid placement
  - **Red**: Invalid placement (with error message)
  - **Yellow**: Valid but suboptimal (low proximity bonus)

**Step 4: Terrain Modification Preview**
- If terrain modification needed:
  - System shows terrain modification preview
  - Shows modification cost and time
  - Player can approve or cancel

**Step 5: Placement Confirmation**
- Player confirms placement
- Client sends placement request to server:
  - Building type
  - Position (X, Y coordinates - building center)
  - Rotation (if applicable)
  - Terrain modification approval (if needed)

**Step 6: Server Validation**
- Server validates placement:
  - Resource availability
  - Location validity
  - Permission checks
  - All validation checks

**Step 7: Construction Start**
- Server deducts resources
- Server creates building record
- Building enters construction phase
- Workers assigned (if required)
- Construction progress tracked

---

## Database Schema

### Building Placement Fields

The `buildings` table (defined in `docs/database-schema.md`) includes:

- `world_x`, `world_y`: Building center coordinates
- `rotation`: Building rotation in radians
- `footprint_polygon`: Copied from `building_types` (for collision detection)
- `door_positions`: Copied from `building_types` (for accessibility checks)

The `building_types` table includes:

- `footprint_polygon`: JSONB polygon definition
- `door_positions`: JSONB door positions
- `relocatable`: Boolean (can building be relocated)
- `relocation_cost_multiplier`: Cost multiplier for relocation
- `relocation_time_multiplier`: Time multiplier for relocation
- `proximity_bonus_range`: Range for proximity bonuses
- `proximity_bonus_type`: Type of proximity bonus

### Road System Tables

The road system tables are defined in `docs/database-schema.md`:

- **`paths`**: Automatic roads and paths generated from unit pathfinding
  - Tracks path usage, quality levels, and waypoints
  - See `docs/database-schema.md` for full schema definition

- **`terrain_modifications`**: Terrain modifications made for building placement
  - Records flattening, elevation changes, and structural supports
  - Links to buildings via `building_id`
  - See `docs/database-schema.md` for full schema definition

---

## Summary

Building placement mechanics provide a comprehensive system for:

- **Polygonal Footprints**: Buildings use complex polygon shapes, not rectangles
- **Door Accessibility**: All doors must be accessible from paths/roads
- **Proximity Bonuses**: Buildings benefit from supply chain proximity
- **Automatic Roads**: Frequently traveled paths become roads automatically
- **Relocation**: Some buildings can be deconstructed and relocated
- **Terrain Modification**: Land may need landscaping or supports for placement
- **Qi Source Proximity**: Some buildings require or benefit from qi sources

**Key Mechanics:**
- Footprint validation using polygon collision detection
- Door accessibility checks for all door positions
- Proximity bonus calculation based on supply chain buildings
- Automatic road generation from unit pathfinding
- Terrain modification for slope and elevation requirements
- Building supports for difficult terrain
- Relocation system for relocatable buildings

---

**Last Updated:** 2025-01-21

