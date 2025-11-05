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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_users_email (email),
    INDEX idx_users_username (username),
    INDEX idx_users_role (role),
    INDEX idx_users_account_approved (account_approved),
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

#### `world_regions`
Defines world regions/shards for partitioning.

```sql
CREATE TABLE world_regions (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    min_x BIGINT NOT NULL,
    min_y BIGINT NOT NULL,
    max_x BIGINT NOT NULL,
    max_y BIGINT NOT NULL,
    shard_id INTEGER, -- Which shard server handles this region
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
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
Player characters/avatars.

```sql
CREATE TABLE avatars (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    world_x BIGINT NOT NULL,
    world_y BIGINT NOT NULL,
    facing_angle REAL DEFAULT 0, -- Rotation in radians
    level INTEGER DEFAULT 1,
    experience BIGINT DEFAULT 0,
    health INTEGER NOT NULL,
    max_health INTEGER NOT NULL,
    region_id BIGINT REFERENCES world_regions(id),
    chunk_x BIGINT NOT NULL,
    chunk_y BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_played_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_avatars_user_id (user_id),
    INDEX idx_avatars_coords (world_x, world_y),
    INDEX idx_avatars_region_id (region_id),
    INDEX idx_avatars_chunk (chunk_x, chunk_y)
);
```

### Buildings

#### `buildings`
All building structures in the world.

```sql
CREATE TABLE buildings (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT REFERENCES avatars(id), -- NULL for neutral/public buildings
    building_type_id INTEGER NOT NULL, -- References building_types table
    world_x BIGINT NOT NULL,
    world_y BIGINT NOT NULL,
    rotation REAL DEFAULT 0,
    health INTEGER NOT NULL,
    max_health INTEGER NOT NULL,
    construction_progress REAL DEFAULT 1.0, -- 0.0 to 1.0
    region_id BIGINT REFERENCES world_regions(id),
    chunk_x BIGINT NOT NULL,
    chunk_y BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    destroyed_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_buildings_owner_id (owner_id),
    INDEX idx_buildings_coords (world_x, world_y),
    INDEX idx_buildings_region_id (region_id),
    INDEX idx_buildings_chunk (chunk_x, chunk_y),
    INDEX idx_buildings_type (building_type_id)
);
```

#### `building_types`
Defines available building types.

```sql
CREATE TABLE building_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL, -- 'resource', 'production', 'defense', 'infrastructure'
    description TEXT,
    size_x INTEGER NOT NULL, -- Width in world units
    size_y INTEGER NOT NULL, -- Height in world units
    build_time INTEGER NOT NULL, -- Seconds to build
    health INTEGER NOT NULL,
    cost_data JSONB, -- Resource costs: {"wood": 100, "stone": 50}
    production_data JSONB, -- Production info if applicable
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### `building_production`
Tracks production queues and output for buildings.

```sql
CREATE TABLE building_production (
    id BIGSERIAL PRIMARY KEY,
    building_id BIGINT NOT NULL REFERENCES buildings(id),
    item_type VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    progress REAL DEFAULT 0.0, -- 0.0 to 1.0
    queued_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    INDEX idx_building_production_building_id (building_id),
    INDEX idx_building_production_completed_at (completed_at)
);
```

### Resources

#### `resource_nodes`
Resource gathering nodes in the world.

```sql
CREATE TABLE resource_nodes (
    id BIGSERIAL PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL, -- 'wood', 'stone', 'iron', 'gold', etc.
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
    
    INDEX idx_resource_nodes_type (resource_type),
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
    npc_type VARCHAR(100) NOT NULL,
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

#### `npc_types`
Defines NPC types and their properties.

```sql
CREATE TABLE npc_types (
    id SERIAL PRIMARY KEY,
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

