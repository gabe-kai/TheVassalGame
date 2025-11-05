# TheVassalGame - Database Schema

## Overview

The database uses PostgreSQL for persistent storage. The schema is designed for scalability, with support for sharding by world region. Redis is used for hot data caching and real-time state.

## Schema Design Principles

- **Normalization**: Third normal form where appropriate
- **Denormalization**: Strategic denormalization for performance
- **Indexing**: Comprehensive indexing for common queries
- **Partitioning**: Support for table partitioning by region
- **Soft Deletes**: Use `deleted_at` timestamps instead of hard deletes
- **Audit Trail**: Track creation and modification times

## Core Tables

### Users & Authentication

#### `users`
Stores user account information.

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Player', -- 'Admin', 'StoryTeller', 'Player', 'Observer'
    email_verified BOOLEAN DEFAULT FALSE,
    account_approved BOOLEAN DEFAULT FALSE, -- Account access requires email_verified OR account_approved
    approved_by BIGINT REFERENCES users(id), -- Admin who approved (if admin approval was used)
    approved_at TIMESTAMP WITH TIME ZONE,
    selected_planet_id BIGINT REFERENCES planets(id), -- Planet selected during onboarding (NULL if not yet selected)
    onboarding_completed BOOLEAN DEFAULT FALSE, -- True after completing: verification, subscription, lore, planet selection
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_users_email (email),
    INDEX idx_users_username (username),
    INDEX idx_users_role (role),
    INDEX idx_users_account_approved (account_approved),
    INDEX idx_users_selected_planet_id (selected_planet_id),
    INDEX idx_users_onboarding_completed (onboarding_completed),
    INDEX idx_users_deleted_at (deleted_at),
    CHECK (role IN ('Admin', 'StoryTeller', 'Player', 'Observer'))
);
```

**Account Access Rules:**
- Users can access their account if either `email_verified = TRUE` OR `account_approved = TRUE`
- Default role is 'Player'
- Admin role should be set manually for the default admin user
- StoryTeller and Observer roles are special roles for game management

**Default Admin User:**
Upon database initialization, a default Admin user should be created with:
- Username: `admin` (or configurable)
- Email: configurable during setup
- Role: `Admin`
- `account_approved = TRUE` (bypasses email verification requirement)
- This user can manage the game server, client, and approve other users

**User Roles:**
- **Admin**: Full access to game server, client management, user approval, system configuration
- **StoryTeller**: Can manage world events, NPCs, and story elements (game master role)
- **Player**: Standard player role (default)
- **Observer**: Read-only access for spectating/monitoring (cannot interact with game)

#### `email_verification_tokens`
Email verification tokens for account activation.

```sql
CREATE TABLE email_verification_tokens (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_email_verification_tokens_user_id (user_id),
    INDEX idx_email_verification_tokens_token (token),
    INDEX idx_email_verification_tokens_expires_at (expires_at)
);
```

**Note:** Tokens expire after 24 hours (configurable). Once used, the token cannot be reused.

#### `user_sessions`
Active user sessions for authentication.

```sql
CREATE TABLE user_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_user_sessions_user_id (user_id),
    INDEX idx_user_sessions_token_hash (token_hash),
    INDEX idx_user_sessions_expires_at (expires_at)
);
```

#### `subscriptions`
User subscription information.

```sql
CREATE TABLE subscriptions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    tier VARCHAR(50) NOT NULL, -- 'initiate' (free), 'novice', 'master'
    status VARCHAR(50) NOT NULL, -- 'active', 'cancelled', 'expired'
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE, -- NULL for 'initiate' tier (free, no expiration)
    cancelled_at TIMESTAMP WITH TIME ZONE,
    payment_provider VARCHAR(50), -- 'stripe', 'paypal', etc. (NULL for 'initiate' tier)
    payment_provider_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_subscriptions_user_id (user_id),
    INDEX idx_subscriptions_status (status),
    INDEX idx_subscriptions_tier (tier),
    INDEX idx_subscriptions_expires_at (expires_at),
    CHECK (tier IN ('initiate', 'novice', 'master'))
);
```

**Subscription Tiers:**
- **Initiate**: Free tier, no payment required, no expiration
- **Novice**: Paid subscription tier
- **Master**: Premium paid subscription tier

### Game World

#### `planets`
Defines planets in the game universe. Planets are subdivided icospheres with tiles subdivided down to playable chunks (1-2m edge faces).

```sql
CREATE TABLE planets (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    doc_section_slug VARCHAR(255) UNIQUE, -- Slug for documentation section (e.g., 'planet-aurora')
    size_x BIGINT NOT NULL, -- Planet size in world units (width)
    size_y BIGINT NOT NULL, -- Planet size in world units (height)
    
    -- Icosahedron Generation Parameters
    icosahedron_subdivisions INTEGER NOT NULL DEFAULT 8, -- Number of subdivision levels (tiles subdivided to 1-2m faces)
    max_lod_level INTEGER NOT NULL DEFAULT 15, -- Maximum LOD level (1-meter resolution)
    
    -- Geography Presets
    geography_preset VARCHAR(50) NOT NULL DEFAULT 'few_large_continents', -- 'pangaea', 'few_large_continents', 'many_small_continents', 'archipelago', 'custom'
    
    -- Terrain Generation Parameters
    sea_level REAL NOT NULL DEFAULT 0.0, -- Sea level (-1.0 to 1.0, controls land-sea ratio)
    mountain_peak_height REAL NOT NULL DEFAULT 1.0, -- Maximum mountain height multiplier (0.0 to 2.0)
    ocean_trench_depth REAL NOT NULL DEFAULT 1.0, -- Maximum ocean depth multiplier (0.0 to 2.0)
    terrain_roughness REAL NOT NULL DEFAULT 0.5, -- How hilly/flat the terrain is (0.0 = flat, 1.0 = very hilly)
    
    -- Generation Metadata
    generator_seed BIGINT, -- Random seed for generation (NULL = random)
    generated_at TIMESTAMP WITH TIME ZONE, -- When planet was generated
    generated_by BIGINT REFERENCES users(id), -- Admin/StoryTeller who generated it
    
    -- Status
    active BOOLEAN DEFAULT TRUE, -- Whether planet is available for selection
    generation_status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'generating', 'completed', 'failed'
    generation_progress REAL DEFAULT 0.0, -- Generation progress (0.0 to 1.0)
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_planets_active (active),
    INDEX idx_planets_generation_status (generation_status),
    INDEX idx_planets_doc_section_slug (doc_section_slug),
    CHECK (geography_preset IN ('pangaea', 'few_large_continents', 'many_small_continents', 'archipelago', 'custom')),
    CHECK (generation_status IN ('pending', 'generating', 'completed', 'failed')),
    CHECK (sea_level >= -1.0 AND sea_level <= 1.0),
    CHECK (mountain_peak_height >= 0.0 AND mountain_peak_height <= 2.0),
    CHECK (ocean_trench_depth >= 0.0 AND ocean_trench_depth <= 2.0),
    CHECK (terrain_roughness >= 0.0 AND terrain_roughness <= 1.0)
);
```

**Geography Presets:**
- **pangaea**: Single large continent
- **few_large_continents**: 2-4 large continents
- **many_small_continents**: Many small continents scattered
- **archipelago**: Many small islands
- **custom**: Custom generation parameters

**Generation Parameters:**
- **sea_level**: Controls land-sea ratio (-1.0 = mostly land, 1.0 = mostly ocean)
- **mountain_peak_height**: Multiplier for maximum mountain height
- **ocean_trench_depth**: Multiplier for maximum ocean depth
- **terrain_roughness**: Controls how hilly (1.0) or flat (0.0) the terrain is

**Note:** 
- Each planet automatically gets a documentation section (slug based on planet name)
- Planets use icosahedron subdivision with tiles subdivided down to playable chunks (1-2m edge faces)
- Initially one planet will be designed during development. System supports multiple planets for future expansion.

#### `territories`
Defines territories within planets. Territories are 1-2km edge tiles that players claim. Once claimed, territories are subdivided into 1m edge tiles for gameplay.

```sql
CREATE TABLE territories (
    id BIGSERIAL PRIMARY KEY,
    planet_id BIGINT NOT NULL REFERENCES planets(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    min_x BIGINT NOT NULL, -- Territory boundaries within planet (1-2km tile boundaries)
    min_y BIGINT NOT NULL,
    max_x BIGINT NOT NULL,
    max_y BIGINT NOT NULL,
    
    -- Territory Type and Generation
    territory_type VARCHAR(50) NOT NULL DEFAULT 'potential', -- 'potential' (1-2km, detailed), 'starting_tile' (1-2km, pre-selected), 'player_claimed' (claimed by player)
    generation_level INTEGER NOT NULL, -- LOD level: all territories are 1-2km edge tiles
    detailed_features JSONB, -- Detailed terrain features at 1-2km level: {"mountains": [...], "rivers": [...], "lakes": [...], "forests": [...], "deserts": [...], "plains": [...]}
    subdivided BOOLEAN DEFAULT FALSE, -- Whether this 1-2km territory has been subdivided into 1m gameplay tiles
    
    -- Terrain Characteristics
    terrain_type VARCHAR(50), -- 'plains', 'forest', 'desert', 'mountain', 'coastal', etc.
    biome_type VARCHAR(50), -- Overall biome classification
    starting_resources JSONB, -- Initial resources for avatars starting here: {"wood": 100, "stone": 50, "qi_crystal": 10}
    
    -- Qi Source (Mana Generation)
    qi_source_type VARCHAR(50) NOT NULL, -- 'qi_vein' or 'qi_well'
    qi_source_x BIGINT, -- X coordinate of qi source within territory (1m tile coordinates)
    qi_source_y BIGINT, -- Y coordinate of qi source within territory (1m tile coordinates)
    qi_source_world_x BIGINT, -- Absolute world X coordinate of qi source
    qi_source_world_y BIGINT, -- Absolute world Y coordinate of qi source
    qi_source_potency REAL DEFAULT 1.0, -- Qi source potency (affects mana generation rate)
    
    -- Player Assignment
    territory_preference VARCHAR(50), -- 'busy' (with other players), 'isolated' (no nearby players), NULL (not yet selected)
    nearby_player_count INTEGER DEFAULT 0, -- Number of active players within territory radius
    discourage_new_players BOOLEAN DEFAULT FALSE, -- If true, discourage (but not restrict) new players from starting nearby
    difficulty VARCHAR(50) DEFAULT 'normal', -- 'easy', 'normal', 'hard', 'expert' (expert = near established isolated player)
    
    -- Status
    available BOOLEAN DEFAULT TRUE, -- Whether territory is available for selection
    claimed_by_avatar_id BIGINT REFERENCES avatars(id), -- Avatar that claimed this territory (NULL if not claimed)
    claimed_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_territories_planet_id (planet_id),
    INDEX idx_territories_territory_type (territory_type),
    INDEX idx_territories_available (available),
    INDEX idx_territories_territory_preference (territory_preference),
    INDEX idx_territories_nearby_player_count (nearby_player_count),
    INDEX idx_territories_claimed_by_avatar_id (claimed_by_avatar_id),
    INDEX idx_territories_subdivided (subdivided),
    INDEX idx_territories_qi_source_type (qi_source_type),
    INDEX idx_territories_coords (min_x, min_y, max_x, max_y),
    CHECK (territory_type IN ('potential', 'starting_tile', 'player_claimed')),
    CHECK (territory_preference IN ('busy', 'isolated') OR territory_preference IS NULL),
    CHECK (qi_source_type IN ('qi_vein', 'qi_well'))
);
```

**Qi Sources:**
- Each territory has either a **qi vein** or **qi well**
- Qi veins: Smaller, more common qi sources
- Qi wells: Larger, more powerful qi sources (rarer)
- Qi sources are the foundation for mana generation and refinement
- Avatar starts near the qi source (within ~50-100m) with starting resources
- Qi source coordinates are stored in territory record

**Territory Generation Process:**
1. **Potential Territories (1-2km)**: After planet generation, system selects 1 tile in each major landmass and ocean
   - These tiles are subdivided down to 1-2km edge lengths
   - Detailed features generated: mountains, hills, plains, rivers, lakes, forests, deserts, etc.
   - **Qi source placement**: System places a qi vein or qi well in each potential territory
   - These become "potential territories" (`territory_type = 'potential'`)

2. **Starting Tiles (1-2km)**: From each potential territory, system picks 8 subdivided tiles (1-2km edge faces)
   - These are marked as `territory_type = 'starting_tile'`
   - **Qi source assignment**: Each starting tile inherits or gets assigned a qi vein or qi well
   - Qi source coordinates are determined (within the 1-2km territory boundaries)
   - Detailed features are NOT generated until a player selects them (on-demand generation)
   - These are the territories (1-2km tiles) offered to players during territory selection

3. **Player Claimed**: When a player selects a starting tile (1-2km territory):
   - Detailed features are generated at 1-2km level
   - **Qi source finalized**: Qi source location is finalized at 1m resolution
   - Territory is subdivided into 1m edge tiles for gameplay
   - Player gets all 1m tiles within their claimed 1-2km territory
   - **Avatar starting location**: Avatar is placed near the qi source (within ~50-100m)
   - **Starting resources**: Avatar receives starting resources for building near the qi source
   - Territory becomes `territory_type = 'player_claimed'` and `subdivided = TRUE`

**Gameplay Map (1m Tiles):**
- Once a 1-2km territory is claimed, it is subdivided into 1m edge tiles
- These 1m tiles are the actual gameplay map
- Player controls all 1m tiles within their claimed 1-2km territory
- Allows good elevation changes and flexible expansion
- Stored in `territory_tiles` table (see below)

**Territory Expansion:**
- Players can buy/claim neighboring 1-2km territories
- When a neighboring territory is claimed, player gets some percentage of the 1m subtiles from that territory
- Allows players to expand their control area gradually

**Territory Selection:**
- **Busy Territories**: Players choosing "busy" are placed on territories with other busy-choice players nearby
- **Isolated Territories**: Players choosing "isolated" are placed on territories without nearby players
  - System sets `discourage_new_players = TRUE` to discourage (not restrict) new players from starting nearby
- **When Map Gets Busy**: System can offer new players territories near established isolated players (more difficult experience)
  - These territories have `difficulty = 'expert'` and `nearby_player_count > 0`

#### `territory_tiles`
Defines the 1m edge tiles that make up a claimed territory's gameplay map. Each 1-2km territory is subdivided into many 1m tiles.

```sql
CREATE TABLE territory_tiles (
    id BIGSERIAL PRIMARY KEY,
    territory_id BIGINT NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    owner_avatar_id BIGINT REFERENCES avatars(id), -- Avatar that owns this 1m tile (can be NULL if unclaimed portion of territory)
    tile_x BIGINT NOT NULL, -- 1m tile coordinates within territory
    tile_y BIGINT NOT NULL,
    world_x BIGINT NOT NULL, -- Absolute world coordinates
    world_y BIGINT NOT NULL,
    elevation REAL, -- Elevation at this 1m tile
    terrain_feature VARCHAR(50), -- Specific feature: 'mountain_peak', 'river', 'lake', 'forest', 'desert', 'plains', etc.
    resource_nodes JSONB, -- Resource nodes on this tile: {"wood": 5, "stone": 2}
    owned_percentage REAL DEFAULT 1.0, -- Percentage of tile owned (1.0 = fully owned, 0.5 = partially owned from neighboring territory expansion)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(territory_id, tile_x, tile_y),
    INDEX idx_territory_tiles_territory_id (territory_id),
    INDEX idx_territory_tiles_owner_avatar_id (owner_avatar_id),
    INDEX idx_territory_tiles_world_coords (world_x, world_y),
    CHECK (owned_percentage > 0.0 AND owned_percentage <= 1.0)
);
```

**Note:** 
- When a 1-2km territory is claimed, all 1m tiles within it are created with `owner_avatar_id` set to the claiming player
- When a player expands to a neighboring 1-2km territory, only a percentage of those 1m tiles are assigned to the player
- This allows flexible territory expansion and shared control of neighboring territories

#### `world_regions`
Defines world regions/shards for partitioning. Regions exist within planets/territories.

```sql
CREATE TABLE world_regions (
    id BIGSERIAL PRIMARY KEY,
    planet_id BIGINT REFERENCES planets(id), -- Which planet this region belongs to
    territory_id BIGINT REFERENCES territories(id), -- Which territory this region belongs to (optional)
    name VARCHAR(100) NOT NULL,
    min_x BIGINT NOT NULL,
    min_y BIGINT NOT NULL,
    max_x BIGINT NOT NULL,
    max_y BIGINT NOT NULL,
    shard_id INTEGER, -- Which shard server handles this region
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_world_regions_planet_id (planet_id),
    INDEX idx_world_regions_territory_id (territory_id),
    INDEX idx_world_regions_shard_id (shard_id),
    INDEX idx_world_regions_coords (min_x, min_y, max_x, max_y)
);
```

#### `world_chunks`
Stores persistent chunk data.

```sql
CREATE TABLE world_chunks (
    id BIGSERIAL PRIMARY KEY,
    chunk_x BIGINT NOT NULL,
    chunk_y BIGINT NOT NULL,
    region_id BIGINT REFERENCES world_regions(id),
    terrain_data BYTEA, -- Compressed terrain heightmap/type data
    version INTEGER DEFAULT 1, -- For optimistic locking
    last_modified TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(chunk_x, chunk_y),
    INDEX idx_world_chunks_coords (chunk_x, chunk_y),
    INDEX idx_world_chunks_region_id (region_id),
    INDEX idx_world_chunks_last_modified (last_modified)
);

-- Partition by region_id for scalability
-- CREATE TABLE world_chunks_region_1 PARTITION OF world_chunks
--   FOR VALUES WITH (region_id = 1);
```

#### `avatars`
Player characters/avatars. Each avatar is linked to a planet and territory.

```sql
CREATE TABLE avatars (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    planet_id BIGINT NOT NULL REFERENCES planets(id), -- Planet this avatar is on
    territory_id BIGINT REFERENCES territories(id), -- Territory this avatar manages
    name VARCHAR(100) NOT NULL,
    world_x BIGINT NOT NULL,
    world_y BIGINT NOT NULL,
    facing_angle REAL DEFAULT 0, -- Rotation in radians
    level INTEGER DEFAULT 1,
    experience BIGINT DEFAULT 0,
    health INTEGER NOT NULL,
    max_health INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending' (not yet placed), 'active' (in world)
    region_id BIGINT REFERENCES world_regions(id),
    chunk_x BIGINT NOT NULL,
    chunk_y BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_played_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_avatars_user_id (user_id),
    INDEX idx_avatars_planet_id (planet_id),
    INDEX idx_avatars_territory_id (territory_id),
    INDEX idx_avatars_coords (world_x, world_y),
    INDEX idx_avatars_region_id (region_id),
    INDEX idx_avatars_chunk (chunk_x, chunk_y),
    INDEX idx_avatars_status (status)
);
```

**Note:** Avatar status:
- `pending`: Avatar created but not yet placed in world (territory not selected)
- `active`: Avatar is active in the game world

### Buildings

#### `buildings`
All building structures in the world.

```sql
CREATE TABLE buildings (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT REFERENCES avatars(id), -- NULL for neutral/public buildings
    building_type_id INTEGER NOT NULL REFERENCES building_types(id),
    world_x BIGINT NOT NULL, -- Building center X coordinate
    world_y BIGINT NOT NULL, -- Building center Y coordinate
    rotation REAL DEFAULT 0, -- Rotation in radians
    
    -- Health & Durability
    health INTEGER NOT NULL, -- Current health (damage from combat/events)
    max_health INTEGER NOT NULL, -- Maximum health (from building_type)
    durability INTEGER NOT NULL, -- Current durability (structural integrity, degrades over time)
    max_durability INTEGER NOT NULL, -- Maximum durability (from building_type)
    
    -- Construction State
    construction_progress REAL DEFAULT 1.0, -- 0.0 to 1.0 (1.0 = fully constructed)
    construction_started_at TIMESTAMP WITH TIME ZONE,
    construction_completed_at TIMESTAMP WITH TIME ZONE,
    constructed_by_avatar_id BIGINT REFERENCES avatars(id), -- Avatar who constructed this building
    actual_build_time INTEGER, -- Actual build time used (after skill bonuses)
    actual_cost_data JSONB, -- Actual resources spent (after skill bonuses)
    
    -- Relocation State
    is_relocating BOOLEAN DEFAULT FALSE, -- Whether building is currently being relocated
    relocation_progress REAL DEFAULT 0.0, -- 0.0 to 1.0 (relocation progress)
    relocation_started_at TIMESTAMP WITH TIME ZONE,
    original_location_x BIGINT, -- Original location before relocation started
    original_location_y BIGINT,
    target_location_x BIGINT, -- Target location for relocation
    target_location_y BIGINT,
    
    -- Maintenance State
    last_maintenance_at TIMESTAMP WITH TIME ZONE, -- Last successful maintenance
    next_maintenance_due_at TIMESTAMP WITH TIME ZONE, -- When next maintenance is due
    maintenance_overdue BOOLEAN DEFAULT FALSE, -- Whether maintenance is overdue
    durability_loss_accumulated REAL DEFAULT 0.0, -- Accumulated durability loss from missed maintenance
    
    -- Functionality State
    is_functional BOOLEAN DEFAULT TRUE, -- Whether building is functional (false if durability too low, no workers, etc.)
    functional_reason TEXT, -- Reason why building is non-functional (if applicable)
    
    -- District & Proximity
    district_id BIGINT REFERENCES districts(id), -- District this building belongs to (NULL if not in district)
    district_bonus_applied BOOLEAN DEFAULT FALSE, -- Whether district bonus is currently applied
    proximity_bonuses JSONB, -- Active proximity bonuses: {"supply_chain": 1.15, "category": 1.1} (multipliers)
    
    -- Tier & Upgrade State
    current_tier INTEGER DEFAULT 1, -- Current tier level (1-6)
    tier_upgrade_progress REAL DEFAULT 0.0, -- 0.0 to 1.0 (upgrade progress)
    tier_upgrade_started_at TIMESTAMP WITH TIME ZONE,
    signature_addition_id INTEGER REFERENCES building_signature_additions(id), -- Signature addition built (NULL if none)
    signature_addition_progress REAL DEFAULT 0.0, -- 0.0 to 1.0 (signature addition construction progress)
    signature_addition_started_at TIMESTAMP WITH TIME ZONE,
    
    -- Spatial Data
    region_id BIGINT REFERENCES world_regions(id),
    chunk_x BIGINT NOT NULL,
    chunk_y BIGINT NOT NULL,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    destroyed_at TIMESTAMP WITH TIME ZONE,
    demolished_at TIMESTAMP WITH TIME ZONE, -- When building was demolished (vs destroyed)
    
    INDEX idx_buildings_owner_id (owner_id),
    INDEX idx_buildings_coords (world_x, world_y),
    INDEX idx_buildings_region_id (region_id),
    INDEX idx_buildings_chunk (chunk_x, chunk_y),
    INDEX idx_buildings_type (building_type_id),
    INDEX idx_buildings_construction_progress (construction_progress),
    INDEX idx_buildings_is_functional (is_functional),
    INDEX idx_buildings_next_maintenance_due_at (next_maintenance_due_at),
    INDEX idx_buildings_current_tier (current_tier),
    INDEX idx_buildings_signature_addition_id (signature_addition_id),
    INDEX idx_buildings_district_id (district_id),
    INDEX idx_buildings_coords_for_district (world_x, world_y, region_id)
);
```

**Health vs Durability:**
- `health`: Damage from combat, events, disasters. Can be repaired.
- `durability`: Structural integrity. Degrades over time if maintenance is missed. Cannot be directly repaired (only maintained).

**Construction:**
- Tracks actual build time and costs (after skill bonuses applied)
- Records who constructed the building
- Construction progress tracks building phase

**Relocation:**
- Tracks relocation state and progress
- Stores original and target locations during relocation

**Maintenance:**
- Tracks maintenance schedule and overdue status
- Accumulates durability loss from missed maintenance cycles

**Functionality:**
- Building may be non-functional if:
  - Durability too low
  - Required workers not assigned
  - Other building-specific conditions

**Tier System:**
- Buildings start at tier 1 when first constructed
- Can be upgraded through tiers 2-6
- Each tier upgrade requires resources and time
- Current tier determines building benefits (housing, qi output, unlocks)
- Signature additions can be built separately for each tier

#### `building_types`
Defines available building types. Automatically synced to public documentation system.

```sql
CREATE TABLE building_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) UNIQUE, -- URL-friendly identifier for documentation (auto-generated from name)
    category VARCHAR(50) NOT NULL, -- 'civic', 'resource', 'production', 'defense', 'infrastructure', 'research', 'commercial'
    building_path VARCHAR(100), -- Path within category (e.g., 'sect_hall', 'archive', 'constabulary' for 'civic')
    description TEXT, -- Description shown in documentation
    detailed_description TEXT, -- Extended lore/mechanics description
    
    -- Building Geometry
    footprint_polygon JSONB NOT NULL, -- Polygonal footprint: {"vertices": [{"x": 0, "y": 0}, {"x": 5, "y": 0}, ...]}
    door_positions JSONB, -- Door locations: [{"x": 2.5, "y": 0, "facing": 0}, ...] (relative to building center)
    
    -- Construction Properties
    base_build_time INTEGER NOT NULL, -- Base construction time in seconds (before skill bonuses)
    base_cost_data JSONB NOT NULL, -- Base resource costs: {"wood": 100, "stone": 50} (before skill bonuses)
    construction_skill VARCHAR(50) DEFAULT 'Construction', -- Skill that provides bonuses (default: 'Construction')
    skill_time_bonus_per_level REAL DEFAULT 0.02, -- 2% time reduction per skill level (0.02 = 2%)
    skill_cost_bonus_per_level REAL DEFAULT 0.01, -- 1% cost reduction per skill level (0.01 = 1%)
    max_skill_bonus REAL DEFAULT 0.5, -- Maximum 50% bonus from skills
    
    -- Building Properties
    max_health INTEGER NOT NULL, -- Maximum health
    max_durability INTEGER NOT NULL, -- Maximum durability (separate from health, degrades over time)
    base_durability INTEGER NOT NULL, -- Starting durability
    
    -- Employment & Workers
    max_employment_slots INTEGER DEFAULT 0, -- Maximum number of workers this building can employ
    required_workers INTEGER DEFAULT 0, -- Minimum workers required for building to function (0 = no requirement)
    employment_skill VARCHAR(50), -- Skill that workers develop while employed (e.g., 'Cultivation', 'Crafting')
    
    -- Passive Resource Generation
    passive_resources JSONB, -- Passive resource generation per day: {"mana_crystal": 10, "food": 50}
    passive_resources_requires_workers BOOLEAN DEFAULT FALSE, -- Whether passive resources require workers
    
    -- Building Functionality
    relocatable BOOLEAN DEFAULT FALSE, -- Whether building can be moved after construction
    relocation_cost_multiplier REAL DEFAULT 0.5, -- Cost multiplier for relocation (0.5 = 50% of build cost)
    relocation_time_multiplier REAL DEFAULT 0.3, -- Time multiplier for relocation (0.3 = 30% of build time)
    relocation_requires_workers BOOLEAN DEFAULT TRUE, -- Whether relocation requires workers
    
    -- Supply Chain & Proximity
    supply_chain_id INTEGER REFERENCES supply_chains(id), -- Supply chain this building belongs to (NULL if none)
    proximity_bonus_range REAL DEFAULT 50.0, -- Range in meters for proximity bonuses (default 50m)
    proximity_bonus_type VARCHAR(50), -- Type of proximity bonus: 'supply_chain', 'category', 'both'
    
    -- Demolition
    demolition_resource_return REAL DEFAULT 0.25, -- Percentage of resources returned on demolition (0.25 = 25%)
    
    -- Maintenance
    maintenance_required BOOLEAN DEFAULT TRUE, -- Whether building requires maintenance
    maintenance_resources JSONB, -- Resources required per maintenance cycle: {"wood": 10, "stone": 5}
    maintenance_interval_hours INTEGER DEFAULT 24, -- Hours between maintenance cycles
    durability_loss_per_cycle REAL DEFAULT 1.0, -- Durability lost per maintenance cycle if not maintained
    max_durability_loss REAL DEFAULT 0.5, -- Maximum durability loss before building becomes non-functional (0.5 = 50%)
    
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'archived' (archived = hidden from selection but still in game)
    archived_at TIMESTAMP WITH TIME ZONE,
    archived_by BIGINT REFERENCES users(id),
    created_by BIGINT REFERENCES users(id), -- Admin/StoryTeller who created it
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_by BIGINT REFERENCES users(id),
    
    INDEX idx_building_types_category (category),
    INDEX idx_building_types_building_path (building_path),
    INDEX idx_building_types_category_path (category, building_path),
    INDEX idx_building_types_status (status),
    INDEX idx_building_types_slug (slug),
    INDEX idx_building_types_relocatable (relocatable),
    CHECK (status IN ('active', 'archived')),
    CHECK (category IN ('civic', 'resource', 'production', 'defense', 'infrastructure', 'research', 'commercial')),
    CHECK (max_skill_bonus >= 0.0 AND max_skill_bonus <= 1.0),
    CHECK (demolition_resource_return >= 0.0 AND demolition_resource_return <= 1.0),
    CHECK (durability_loss_per_cycle >= 0.0),
    CHECK (max_durability_loss >= 0.0 AND max_durability_loss <= 1.0)
);
```

**Building Geometry:**
- `footprint_polygon`: Defines the building's polygonal footprint as an array of vertices
- `door_positions`: Defines entry/exit points for units (relative to building center, includes facing direction)

**Construction Mechanics:**
- Base build time and costs can be reduced by construction skills
- Skill bonuses: time reduction and cost reduction per skill level
- Maximum skill bonus cap prevents unlimited bonuses

**Durability System:**
- `durability`: Separate from health, represents structural integrity
- Degrades over time if maintenance is not performed
- Buildings become non-functional if durability drops too low

**Employment System:**
- Buildings can employ workers (cultivators, etc.)
- Workers develop skills while employed
- Some buildings require workers to function at all

**Passive Resources:**
- Buildings can generate resources passively (mana crystals, food, etc.)
- Can optionally require workers to generate passive resources

**Relocation:**
- Relocatable buildings can be moved after construction
- Requires resources, time, and workers to deconstruct/reconstruct
- Cost and time are multipliers of original build cost/time

**Demolition:**
- Returns a percentage of original build resources

**Maintenance:**
- Buildings require periodic maintenance
- Failure to maintain causes durability loss
- Buildings become non-functional if durability drops too low

**Documentation Integration:**
- Each building type automatically gets a documentation article (slug: `building-{slug}`)
- Documentation is auto-generated from database fields
- StoryTellers/Admins can edit the documentation article to add lore/details
- When building type is archived, documentation is hidden but not deleted

**Note:** Building types are managed by Admins and StoryTellers. Changes automatically sync to the public documentation system.

#### `building_tiers`
Defines the 6 tiers/levels for each building type. Each tier has unique costs, benefits, and unlocks.

```sql
CREATE TABLE building_tiers (
    id SERIAL PRIMARY KEY,
    building_type_id INTEGER NOT NULL REFERENCES building_types(id) ON DELETE CASCADE,
    tier_level INTEGER NOT NULL, -- 1-6 (tier level)
    name VARCHAR(100) NOT NULL, -- Tier name (e.g., "Founder's Shelter", "Gathering Hall")
    description TEXT, -- Description of this tier
    
    -- Upgrade Costs (to reach this tier from previous tier)
    upgrade_cost_data JSONB NOT NULL, -- Resource costs to upgrade to this tier: {"wood": 200, "stone": 100, "qi_crystal": 50}
    upgrade_time INTEGER NOT NULL, -- Time in seconds to complete upgrade (before skill bonuses)
    
    -- Benefits & Properties
    housing_capacity INTEGER DEFAULT 0, -- Housing slots provided (e.g., 12, 20, 35)
    qi_output_description VARCHAR(255), -- Description of qi output (e.g., "Ambient absorption", "Low-Grade Crystals")
    qi_output_rate REAL DEFAULT 0.0, -- Actual qi/mana generation rate per day
    qi_output_resource_type_id INTEGER REFERENCES resource_types(id), -- Type of qi resource generated
    
    -- Unlocks (JSONB array of building types or features unlocked)
    unlocks JSONB, -- Features unlocked: ["basic_housing", "fields", "dorms", "training", "gardens", ...]
    
    -- Tier-Specific Properties
    max_health_modifier REAL DEFAULT 1.0, -- Health multiplier for this tier (1.0 = no change)
    max_durability_modifier REAL DEFAULT 1.0, -- Durability multiplier for this tier
    employment_slots_modifier INTEGER DEFAULT 0, -- Additional employment slots (can be negative)
    passive_resources_modifier JSONB, -- Modifier to passive resources: {"mana_crystal": 1.5} (multiplier)
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(building_type_id, tier_level),
    INDEX idx_building_tiers_building_type_id (building_type_id),
    INDEX idx_building_tiers_tier_level (tier_level),
    CHECK (tier_level >= 1 AND tier_level <= 6)
);
```

**Tier System:**
- Each building type has 6 tiers (levels 1-6)
- Tier 1 is the base building when first constructed
- Each tier upgrade requires resources and time
- Each tier provides new benefits: housing, qi output, unlocks
- Tier properties modify base building properties (health, durability, employment, etc.)

**Unlocks:**
- Each tier unlocks new building types or features
- Unlocks are stored as JSONB array of identifiers
- Unlocks can be checked to determine what player can build

#### `building_signature_additions`
Defines signature additions that can be built for each tier. Each tier has one signature addition.

```sql
CREATE TABLE building_signature_additions (
    id SERIAL PRIMARY KEY,
    building_tier_id INTEGER NOT NULL REFERENCES building_tiers(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL, -- Signature addition name (e.g., "Meditation Platform", "Qi Conduit Array")
    description TEXT, -- Description of the signature addition
    
    -- Construction Properties
    cost_data JSONB NOT NULL, -- Resource costs to build: {"wood": 50, "stone": 25, "qi_crystal": 10}
    build_time INTEGER NOT NULL, -- Time in seconds to build (before skill bonuses)
    
    -- Additional Space Required
    additional_footprint_polygon JSONB, -- Additional footprint polygon: {"vertices": [{"x": 0, "y": 0}, ...]}
    attachment_point JSONB, -- Where it attaches to building: {"x": 2.5, "y": 0, "side": "north"}
    
    -- Benefits
    benefits JSONB NOT NULL, -- Benefits provided: {"qi_output_bonus": 1.5, "housing_bonus": 5, "unlocks": ["advanced_meditation"]}
    qi_output_bonus REAL DEFAULT 0.0, -- Additional qi output rate per day
    housing_bonus INTEGER DEFAULT 0, -- Additional housing capacity
    unlocks JSONB, -- Additional unlocks provided by this signature addition
    
    -- Visual/Gameplay
    visual_model VARCHAR(255), -- Model/visual identifier for the addition
    special_effects JSONB, -- Special effects or animations: {"particles": "qi_flow", "aura": "cultivation"}
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_building_signature_additions_building_tier_id (building_tier_id)
);
```

**Signature Additions:**
- Each tier has exactly one signature addition
- Signature additions are optional (player can choose to build or not)
- Require additional resources and space
- Provide additional benefits beyond the tier itself
- Can unlock additional features or provide bonuses

**Note:** Signature additions are built separately from tier upgrades. A player can:
1. Upgrade building to tier 2
2. Then build the tier 2 signature addition (separate construction)
3. Or skip the signature addition and upgrade to tier 3

#### `building_employment`
Tracks workers assigned to buildings.

```sql
CREATE TABLE building_employment (
    id BIGSERIAL PRIMARY KEY,
    building_id BIGINT NOT NULL REFERENCES buildings(id) ON DELETE CASCADE,
    npc_id BIGINT NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    skill_level_when_assigned INTEGER, -- Skill level when first assigned (for tracking improvement)
    last_skill_check_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(building_id, npc_id),
    INDEX idx_building_employment_building_id (building_id),
    INDEX idx_building_employment_npc_id (npc_id)
);
```

**Note:** Workers assigned to buildings will develop skills over time. The system tracks skill levels to show improvement.

#### `building_production`
Tracks production queues and output for buildings.

```sql
CREATE TABLE building_production (
    id BIGSERIAL PRIMARY KEY,
    building_id BIGINT NOT NULL REFERENCES buildings(id) ON DELETE CASCADE,
    item_type VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    progress REAL DEFAULT 0.0, -- 0.0 to 1.0
    queued_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_building_production_building_id (building_id),
    INDEX idx_building_production_completed_at (completed_at)
);
```

#### `building_passive_resources`
Tracks passive resource generation for buildings (daily generation).

```sql
CREATE TABLE building_passive_resources (
    id BIGSERIAL PRIMARY KEY,
    building_id BIGINT NOT NULL REFERENCES buildings(id) ON DELETE CASCADE,
    resource_type_id INTEGER NOT NULL REFERENCES resource_types(id),
    rate_per_day REAL NOT NULL, -- Resources generated per day
    last_generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    accumulated REAL DEFAULT 0.0, -- Accumulated resources waiting to be collected
    
    UNIQUE(building_id, resource_type_id),
    INDEX idx_building_passive_resources_building_id (building_id),
    INDEX idx_building_passive_resources_resource_type_id (resource_type_id)
);
```

**Note:** Passive resources accumulate over time. Players must collect them from the building.

#### `districts`
Defines districts formed when buildings of the same category cluster together.

```sql
CREATE TABLE districts (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT REFERENCES avatars(id), -- Owner of the district (usually owner of majority buildings)
    category VARCHAR(50) NOT NULL, -- Category of buildings in this district: 'civic', 'resource', 'production', etc.
    name VARCHAR(100), -- Optional district name (auto-generated if NULL)
    
    -- District Boundaries
    center_x BIGINT NOT NULL, -- Center X coordinate of district
    center_y BIGINT NOT NULL, -- Center Y coordinate of district
    radius REAL NOT NULL, -- Radius of district in meters
    boundary_polygon JSONB, -- Polygonal boundary of district: {"vertices": [{"x": 0, "y": 0}, ...]}
    
    -- District Formation
    building_count INTEGER NOT NULL DEFAULT 0, -- Number of buildings in district
    min_buildings_required INTEGER NOT NULL DEFAULT 3, -- Minimum buildings required to form district
    formation_threshold REAL DEFAULT 50.0, -- Maximum distance between buildings to form district (meters)
    
    -- District Benefits
    district_bonus_type VARCHAR(50) DEFAULT 'efficiency', -- Type of bonus: 'efficiency', 'production', 'cost_reduction', 'qi_output'
    district_bonus_value REAL DEFAULT 0.1, -- Bonus value (0.1 = 10% bonus)
    bonus_scales_with_buildings BOOLEAN DEFAULT TRUE, -- Whether bonus increases with more buildings
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE, -- Whether district is active (false if below min_buildings_required)
    formed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    dissolved_at TIMESTAMP WITH TIME ZONE,
    
    -- Spatial Data
    region_id BIGINT REFERENCES world_regions(id),
    chunk_x BIGINT NOT NULL,
    chunk_y BIGINT NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_districts_owner_id (owner_id),
    INDEX idx_districts_category (category),
    INDEX idx_districts_coords (center_x, center_y),
    INDEX idx_districts_region_id (region_id),
    INDEX idx_districts_chunk (chunk_x, chunk_y),
    INDEX idx_districts_is_active (is_active)
);
```

**District Formation:**
- Districts form automatically when buildings of the same category cluster together
- Minimum buildings required (default: 3)
- Buildings must be within formation threshold distance (default: 50m)
- District boundaries are calculated from building positions
- District dissolves if building count drops below minimum

**District Benefits:**
- Buildings in districts receive bonuses
- Bonus type and value are configurable per category
- Bonus can scale with number of buildings in district
- Benefits apply automatically to all buildings in district

#### `supply_chains`
Defines supply chains - groups of buildings that work together in production/resource chains.

```sql
CREATE TABLE supply_chains (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE, -- Supply chain name (e.g., "Wood Processing", "Mana Refinement")
    description TEXT, -- Description of the supply chain
    
    -- Supply Chain Properties
    chain_type VARCHAR(50) NOT NULL, -- 'linear' (A->B->C), 'hub' (A->B, A->C), 'network' (complex)
    proximity_bonus_range REAL DEFAULT 50.0, -- Range in meters for proximity bonuses
    proximity_bonus_per_link REAL DEFAULT 0.05, -- Bonus per linked building in range (0.05 = 5%)
    max_proximity_bonus REAL DEFAULT 0.25, -- Maximum proximity bonus (0.25 = 25%)
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_supply_chains_name (name)
);
```

**Supply Chains:**
- Groups buildings that work together in production chains
- Buildings in supply chains get proximity bonuses when near other chain buildings
- Bonus increases with number of linked buildings in range
- Maximum bonus cap prevents unlimited bonuses

#### `supply_chain_links`
Defines relationships between buildings in a supply chain.

```sql
CREATE TABLE supply_chain_links (
    id SERIAL PRIMARY KEY,
    supply_chain_id INTEGER NOT NULL REFERENCES supply_chains(id) ON DELETE CASCADE,
    source_building_type_id INTEGER NOT NULL REFERENCES building_types(id),
    target_building_type_id INTEGER NOT NULL REFERENCES building_types(id),
    link_type VARCHAR(50) DEFAULT 'produces', -- 'produces', 'consumes', 'transforms', 'enhances'
    link_description TEXT, -- Description of the relationship
    
    -- Link Properties
    proximity_bonus REAL DEFAULT 0.1, -- Bonus when source and target are in proximity (0.1 = 10%)
    max_distance REAL DEFAULT 100.0, -- Maximum distance for bonus (meters)
    bidirectional BOOLEAN DEFAULT FALSE, -- Whether bonus applies in both directions
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(supply_chain_id, source_building_type_id, target_building_type_id),
    INDEX idx_supply_chain_links_supply_chain_id (supply_chain_id),
    INDEX idx_supply_chain_links_source (source_building_type_id),
    INDEX idx_supply_chain_links_target (target_building_type_id)
);
```

**Supply Chain Links:**
- Defines relationships between building types in a supply chain
- Links can be directional or bidirectional
- Proximity bonuses apply when linked buildings are near each other
- Different link types (produces, consumes, transforms, enhances) can have different bonuses

**Note:** Supply chains are managed by Admins and StoryTellers. Buildings can belong to multiple supply chains through their building_type configuration.

### Resources

#### `resource_types`
Defines resource types in the game. Automatically synced to public documentation system.

```sql
CREATE TABLE resource_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) UNIQUE, -- URL-friendly identifier for documentation (auto-generated from name)
    category VARCHAR(50) NOT NULL, -- 'raw_material', 'processed_material', 'refined_product', 'specialized', 'crafted', 'commerce'
    description TEXT, -- Description shown in documentation
    detailed_description TEXT, -- Extended lore/mechanics description
    icon VARCHAR(255), -- Icon identifier/path
    rarity VARCHAR(50) DEFAULT 'common', -- 'common', 'uncommon', 'rare', 'epic', 'legendary'
    gathering_method VARCHAR(50), -- 'mining', 'harvesting', 'extraction', 'refinement', 'generation', 'crafting', 'trade', 'hunting', 'processing', 'smelting', 'condensation'
    base_value INTEGER DEFAULT 1, -- Base trade value
    stack_size INTEGER DEFAULT 1000, -- Maximum stack size in inventory
    
    -- Production Chain Information
    production_chain VARCHAR(50), -- Which production chain: 'wood', 'stone', 'metal', 'essence', 'qi', 'food', 'herb', 'water', 'crafting', 'commerce', 'beast'
    production_tier INTEGER DEFAULT 1, -- Tier in production chain: 1=raw, 2=processed, 3=refined, 4=specialized, 5=ultimate
    created_from JSONB, -- Array of resource slugs that create this resource: ["lumber", "refined_lumber", "qi_crystal"]
    
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'archived' (archived = hidden from selection but still in game)
    archived_at TIMESTAMP WITH TIME ZONE,
    archived_by BIGINT REFERENCES users(id),
    created_by BIGINT REFERENCES users(id), -- Admin/StoryTeller who created it
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_by BIGINT REFERENCES users(id),
    
    INDEX idx_resource_types_category (category),
    INDEX idx_resource_types_rarity (rarity),
    INDEX idx_resource_types_status (status),
    INDEX idx_resource_types_slug (slug),
    INDEX idx_resource_types_production_chain (production_chain),
    INDEX idx_resource_types_production_tier (production_tier),
    CHECK (status IN ('active', 'archived')),
    CHECK (rarity IN ('common', 'uncommon', 'rare', 'epic', 'legendary')),
    CHECK (category IN ('raw_material', 'processed_material', 'refined_product', 'specialized', 'crafted', 'commerce')),
    CHECK (production_tier >= 1 AND production_tier <= 5)
);
```

**Documentation Integration:**
- Each resource type automatically gets a documentation article (slug: `resource-{slug}`)
- Documentation is auto-generated from database fields
- StoryTellers/Admins can edit the documentation article to add lore/details
- When resource type is archived, documentation is hidden but not deleted

**Note:** Resource types are managed by Admins and StoryTellers. Changes automatically sync to the public documentation system.

#### `resource_nodes`
Resource gathering nodes in the world. References `resource_types`.

```sql
CREATE TABLE resource_nodes (
    id BIGSERIAL PRIMARY KEY,
    resource_type_id INTEGER NOT NULL REFERENCES resource_types(id), -- References resource_types table
    world_x BIGINT NOT NULL,
    world_y BIGINT NOT NULL,
    amount INTEGER NOT NULL, -- Remaining resource amount
    max_amount INTEGER NOT NULL,
    respawn_time INTEGER, -- Seconds to respawn (NULL if non-respawning)
    last_harvested_at TIMESTAMP WITH TIME ZONE,
    region_id BIGINT REFERENCES world_regions(id),
    chunk_x BIGINT NOT NULL,
    chunk_y BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_resource_nodes_resource_type_id (resource_type_id),
    INDEX idx_resource_nodes_coords (world_x, world_y),
    INDEX idx_resource_nodes_region_id (region_id),
    INDEX idx_resource_nodes_chunk (chunk_x, chunk_y)
);
```

#### `inventories`
Player and building inventories.

```sql
CREATE TABLE inventories (
    id BIGSERIAL PRIMARY KEY,
    owner_type VARCHAR(50) NOT NULL, -- 'avatar', 'building'
    owner_id BIGINT NOT NULL,
    resources JSONB NOT NULL, -- {"wood": 100, "stone": 50, ...}
    max_capacity INTEGER,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(owner_type, owner_id),
    INDEX idx_inventories_owner (owner_type, owner_id)
);
```

### NPCs

#### `npcs`
Persistent NPC entities.

```sql
CREATE TABLE npcs (
    id BIGSERIAL PRIMARY KEY,
    npc_type_id INTEGER NOT NULL REFERENCES npc_types(id), -- References npc_types table
    owner_id BIGINT REFERENCES avatars(id), -- NULL for neutral NPCs
    world_x BIGINT NOT NULL,
    world_y BIGINT NOT NULL,
    facing_angle REAL DEFAULT 0,
    health INTEGER NOT NULL,
    max_health INTEGER NOT NULL,
    state VARCHAR(50) DEFAULT 'idle', -- 'idle', 'working', 'moving', 'fighting'
    current_job_id BIGINT, -- References jobs table
    region_id BIGINT REFERENCES world_regions(id),
    chunk_x BIGINT NOT NULL,
    chunk_y BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_npcs_owner_id (owner_id),
    INDEX idx_npcs_coords (world_x, world_y),
    INDEX idx_npcs_region_id (region_id),
    INDEX idx_npcs_chunk (chunk_x, chunk_y),
    INDEX idx_npcs_state (state)
);
```

#### `species`
Defines species in the game world (uplifted species, native fauna, etc.). Automatically synced to public documentation system.

```sql
CREATE TABLE species (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) UNIQUE, -- URL-friendly identifier for documentation (auto-generated from name)
    category VARCHAR(50) NOT NULL, -- 'uplifted', 'native_fauna', 'native_flora', 'engineered', 'other'
    description TEXT, -- Description shown in documentation
    detailed_description TEXT, -- Extended lore/biology description
    sapient BOOLEAN DEFAULT FALSE, -- Whether species is sapient (uplifted species = TRUE)
    size_category VARCHAR(50), -- 'microscopic', 'tiny', 'small', 'medium', 'large', 'huge', 'gigantic'
    habitat VARCHAR(100), -- Preferred habitat/biome
    diet VARCHAR(50), -- 'herbivore', 'carnivore', 'omnivore', 'photosynthetic', 'other'
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'archived' (archived = hidden from selection but still in game)
    archived_at TIMESTAMP WITH TIME ZONE,
    archived_by BIGINT REFERENCES users(id),
    created_by BIGINT REFERENCES users(id), -- Admin/StoryTeller who created it
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_by BIGINT REFERENCES users(id),
    
    INDEX idx_species_category (category),
    INDEX idx_species_sapient (sapient),
    INDEX idx_species_status (status),
    INDEX idx_species_slug (slug),
    CHECK (status IN ('active', 'archived'))
);
```

**Documentation Integration:**
- Each species automatically gets a documentation article (slug: `species-{slug}`)
- Documentation is auto-generated from database fields
- StoryTellers/Admins can edit the documentation article to add lore/details
- When species is archived, documentation is hidden but not deleted

**Note:** Species are managed by Admins and StoryTellers. Changes automatically sync to the public documentation system.

#### `npc_types`
Defines NPC types and their properties. NPCs are instances of species.

```sql
CREATE TABLE npc_types (
    id SERIAL PRIMARY KEY,
    species_id INTEGER REFERENCES species(id), -- Species this NPC type belongs to (NULL if generic)
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL, -- 'worker', 'guard', 'trader', 'citizen'
    health INTEGER NOT NULL,
    speed REAL NOT NULL, -- Movement speed
    abilities JSONB, -- NPC abilities/config
    cost_data JSONB, -- Cost to spawn this NPC
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### `jobs`
Job queue for NPCs.

```sql
CREATE TABLE jobs (
    id BIGSERIAL PRIMARY KEY,
    npc_id BIGINT REFERENCES npcs(id),
    job_type VARCHAR(50) NOT NULL, -- 'gather', 'build', 'move', 'attack', etc.
    target_type VARCHAR(50), -- Type of target (entity, building, location)
    target_id BIGINT, -- ID of target entity/building
    target_x BIGINT, -- Target location if applicable
    target_y BIGINT,
    priority INTEGER DEFAULT 5, -- 1-10, higher is more important
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'assigned', 'in_progress', 'completed', 'failed'
    data JSONB, -- Additional job data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_jobs_npc_id (npc_id),
    INDEX idx_jobs_status (status),
    INDEX idx_jobs_priority (priority DESC)
);
```

### Economy & Trade

#### `trades`
Active trade offers.

```sql
CREATE TABLE trades (
    id BIGSERIAL PRIMARY KEY,
    seller_id BIGINT NOT NULL REFERENCES avatars(id),
    item_type VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_unit BIGINT NOT NULL, -- Price in base currency
    total_price BIGINT NOT NULL, -- Calculated: quantity * price_per_unit
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'pending', 'completed', 'cancelled'
    buyer_id BIGINT REFERENCES avatars(id),
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_trades_seller_id (seller_id),
    INDEX idx_trades_buyer_id (buyer_id),
    INDEX idx_trades_status (status),
    INDEX idx_trades_item_type (item_type),
    INDEX idx_trades_expires_at (expires_at)
);
```

#### `trade_history`
Historical trade records.

```sql
CREATE TABLE trade_history (
    id BIGSERIAL PRIMARY KEY,
    trade_id BIGINT REFERENCES trades(id),
    seller_id BIGINT NOT NULL REFERENCES avatars(id),
    buyer_id BIGINT NOT NULL REFERENCES avatars(id),
    item_type VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_unit BIGINT NOT NULL,
    total_price BIGINT NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_trade_history_seller_id (seller_id),
    INDEX idx_trade_history_buyer_id (buyer_id),
    INDEX idx_trade_history_item_type (item_type),
    INDEX idx_trade_history_completed_at (completed_at)
);
```

#### `market_prices`
Market price history for price tracking.

```sql
CREATE TABLE market_prices (
    id BIGSERIAL PRIMARY KEY,
    item_type VARCHAR(100) NOT NULL,
    region_id BIGINT REFERENCES world_regions(id),
    average_price BIGINT NOT NULL,
    min_price BIGINT NOT NULL,
    max_price BIGINT NOT NULL,
    volume INTEGER NOT NULL, -- Number of trades
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_market_prices_item_type (item_type),
    INDEX idx_market_prices_region_id (region_id),
    INDEX idx_market_prices_recorded_at (recorded_at)
);
```

### Social & Communication

#### `guilds`
Player guilds/clans.

```sql
CREATE TABLE guilds (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    tag VARCHAR(10) NOT NULL UNIQUE, -- Short guild tag
    description TEXT,
    leader_id BIGINT NOT NULL REFERENCES avatars(id),
    member_count INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_guilds_leader_id (leader_id)
);
```

#### `guild_members`
Guild membership.

```sql
CREATE TABLE guild_members (
    id BIGSERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL REFERENCES guilds(id),
    avatar_id BIGINT NOT NULL REFERENCES avatars(id),
    role VARCHAR(50) DEFAULT 'member', -- 'leader', 'officer', 'member'
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(guild_id, avatar_id),
    INDEX idx_guild_members_guild_id (guild_id),
    INDEX idx_guild_members_avatar_id (avatar_id)
);
```

#### `chat_messages`
Chat message history.

```sql
CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    sender_id BIGINT REFERENCES avatars(id),
    channel VARCHAR(50) NOT NULL, -- 'global', 'local', 'guild', 'whisper'
    recipient_id BIGINT REFERENCES avatars(id), -- For whispers
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_chat_messages_sender_id (sender_id),
    INDEX idx_chat_messages_channel (channel),
    INDEX idx_chat_messages_created_at (created_at DESC)
);
```

### Admin & System

#### `admin_users`
Admin user accounts and permissions. Note: User roles are stored in `users.role`, but this table provides additional admin-specific permissions.

```sql
CREATE TABLE admin_users (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    permissions JSONB, -- Specific permissions beyond role (e.g., {"can_manage_users": true, "can_edit_world": true})
    notes TEXT, -- Admin notes about this user
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_admin_users_user_id (user_id),
    UNIQUE(user_id)
);
```

**Note:** User roles (Admin, StoryTeller, Player, Observer) are stored in the `users.role` field. This table is for additional admin-specific permissions and metadata.

#### `game_config`
Game configuration values.

```sql
CREATE TABLE game_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    updated_by BIGINT REFERENCES admin_users(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_game_config_key (key)
);
```

#### `audit_log`
System audit log for admin actions.

```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    admin_user_id BIGINT REFERENCES admin_users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id BIGINT,
    details JSONB,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_audit_log_admin_user_id (admin_user_id),
    INDEX idx_audit_log_created_at (created_at DESC),
    INDEX idx_audit_log_action (action)
);
```

### Documentation System

#### `doc_articles`
Documentation articles (game lore, user guides, etc.). Uses markdown formatting.

```sql
CREATE TABLE doc_articles (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL, -- URL-friendly identifier
    content TEXT NOT NULL, -- Markdown content
    content_html TEXT, -- Rendered HTML (cached for performance)
    category VARCHAR(100), -- 'lore', 'guide', 'reference', etc.
    author_id BIGINT NOT NULL REFERENCES users(id), -- User who created/owns the article
    status VARCHAR(50) NOT NULL DEFAULT 'published', -- 'draft', 'published', 'archived'
    archived_at TIMESTAMP WITH TIME ZONE, -- When archived (soft delete)
    archived_by BIGINT REFERENCES users(id), -- Who archived it
    view_count INTEGER DEFAULT 0, -- View counter
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_edited_by BIGINT REFERENCES users(id), -- Last user to edit
    
    INDEX idx_doc_articles_slug (slug),
    INDEX idx_doc_articles_category (category),
    INDEX idx_doc_articles_status (status),
    INDEX idx_doc_articles_author_id (author_id),
    INDEX idx_doc_articles_created_at (created_at DESC),
    CHECK (status IN ('draft', 'published', 'archived'))
);
```

**Permissions:**
- **Viewers/Players**: Read published articles, comment
- **StoryTellers/Admins**: Write, edit, archive, read, comment
- **Admins**: Additionally can delete (hard delete, not just archive)

#### `doc_comments`
Comments on documentation articles.

```sql
CREATE TABLE doc_comments (
    id BIGSERIAL PRIMARY KEY,
    article_id BIGINT NOT NULL REFERENCES doc_articles(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id),
    parent_comment_id BIGINT REFERENCES doc_comments(id), -- For threaded comments/replies
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE, -- Soft delete
    
    INDEX idx_doc_comments_article_id (article_id),
    INDEX idx_doc_comments_user_id (user_id),
    INDEX idx_doc_comments_parent_comment_id (parent_comment_id),
    INDEX idx_doc_comments_created_at (created_at DESC)
);
```

**Permissions:**
- All registered users (Viewers/Players/StoryTellers/Admins) can comment on published articles
- Users can edit their own comments
- StoryTellers and Admins can moderate comments

#### `doc_edit_requests`
User requests to edit documentation articles.

```sql
CREATE TABLE doc_edit_requests (
    id BIGSERIAL PRIMARY KEY,
    article_id BIGINT NOT NULL REFERENCES doc_articles(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id), -- User requesting the edit
    requested_content TEXT NOT NULL, -- Proposed markdown content
    notes TEXT, -- User's explanation of why they want this edit
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    reviewed_by BIGINT REFERENCES users(id), -- StoryTeller/Admin who reviewed
    reviewed_at TIMESTAMP WITH TIME ZONE,
    review_notes TEXT, -- Reviewer's notes
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_doc_edit_requests_article_id (article_id),
    INDEX idx_doc_edit_requests_user_id (user_id),
    INDEX idx_doc_edit_requests_status (status),
    INDEX idx_doc_edit_requests_created_at (created_at DESC),
    CHECK (status IN ('pending', 'approved', 'rejected'))
);
```

**Permissions:**
- All registered users can request edits to published articles
- StoryTellers and Admins can approve/reject edit requests

## Indexes & Performance

### Composite Indexes

```sql
-- Common query patterns
CREATE INDEX idx_avatars_region_chunk ON avatars(region_id, chunk_x, chunk_y);
CREATE INDEX idx_buildings_region_chunk ON buildings(region_id, chunk_x, chunk_y);
CREATE INDEX idx_npcs_region_chunk ON npcs(region_id, chunk_x, chunk_y);
CREATE INDEX idx_resource_nodes_region_chunk ON resource_nodes(region_id, chunk_x, chunk_y);
```

### Partial Indexes

```sql
-- Only index active/visible entities
CREATE INDEX idx_buildings_active ON buildings(region_id, chunk_x, chunk_y) 
  WHERE destroyed_at IS NULL;
CREATE INDEX idx_trades_open ON trades(item_type, price_per_unit) 
  WHERE status = 'open' AND expires_at > NOW();
```

## Data Partitioning Strategy

### Horizontal Partitioning

Partition large tables by `region_id` to distribute load:

```sql
-- Example: Partition buildings table by region
CREATE TABLE buildings (
    -- ... columns ...
) PARTITION BY HASH (region_id);

CREATE TABLE buildings_region_0 PARTITION OF buildings
  FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE buildings_region_1 PARTITION OF buildings
  FOR VALUES WITH (modulus 4, remainder 1);
CREATE TABLE buildings_region_2 PARTITION OF buildings
  FOR VALUES WITH (modulus 4, remainder 2);
CREATE TABLE buildings_region_3 PARTITION OF buildings
  FOR VALUES WITH (modulus 4, remainder 3);
```

## Caching Strategy (Redis)

### Cache Keys

```
# Chunk data
chunk:{chunk_x}:{chunk_y} -> Serialized chunk data (TTL: 5 minutes)

# Player session
session:{session_id} -> Session data (TTL: 24 hours)

# Player state
player:{avatar_id}:state -> Current player state (TTL: 1 hour)

# Hot NPC data
npcs:chunk:{chunk_x}:{chunk_y} -> NPC list for chunk (TTL: 1 minute)

# Market prices
market:{item_type}:{region_id} -> Current market price (TTL: 5 minutes)

# Rate limiting
ratelimit:{user_id}:{action} -> Request count (TTL: 1 minute)
```

### Pub/Sub Channels

```
# World updates
world:chunk:{chunk_x}:{chunk_y}:update -> Chunk update notifications

# Player events
player:{avatar_id}:event -> Player-specific events

# Trade updates
trade:{trade_id}:update -> Trade status updates

# Chat
chat:{channel} -> Chat messages
```

## Migration Strategy

### Version Control

Use a migration tool (e.g., golang-migrate, diesel) to manage schema changes:

```
/migrations
  ├── 0001_initial_schema.up.sql
  ├── 0001_initial_schema.down.sql
  ├── 0002_add_trade_history.up.sql
  └── 0002_add_trade_history.down.sql
```

### Backup Strategy

- **Full Backups**: Daily full database backups
- **Incremental Backups**: Hourly incremental backups
- **Point-in-Time Recovery**: Transaction log backups
- **Retention**: 30 days for full backups, 7 days for incremental

## Data Retention

### Archival Strategy

- **Chat Messages**: Archive messages older than 90 days
- **Trade History**: Keep indefinitely (valuable for analytics)
- **Audit Log**: Keep indefinitely (compliance)
- **Player Sessions**: Delete expired sessions after 30 days

### Soft Deletes

Use `deleted_at` timestamps for soft deletes, allowing data recovery and audit trails.

