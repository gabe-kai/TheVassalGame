# TheVassalGame - Technical Architecture

## System Overview

TheVassalGame uses a distributed architecture with clear separation between server simulation, client rendering, and web services. The system is designed for horizontal scalability and continuous operation.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
├─────────────────────────┬───────────────────────────────────────┤
│   Web Client (Low LOD)  │   Native Client (High LOD) [Future]  │
│   React + Three.js      │   Unity/Unreal/Native                 │
│   WebSocket Client      │   Custom Protocol Client              │
└─────────────────────────┴───────────────────────────────────────┘
                              │
                              │ WebSocket / Custom Protocol
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      Game Server Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Auth Service │  │ Game Server  │  │ World Server │         │
│  │              │  │ (Simulation) │  │  (Shard 1)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                     │            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ World Server │  │ World Server │  │ Matchmaking  │         │
│  │  (Shard 2)   │  │  (Shard N)   │  │   Service    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              ┌─────▼─────┐      ┌─────▼─────┐
              │ PostgreSQL │      │   Redis   │
              │  (Persist) │      │  (Cache)  │
              └────────────┘      └───────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Website Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  Next.js Frontend + API Backend                                 │
│  - User Management                                              │
│  - Subscription Management                                      │
│  - Avatar Management                                            │
│  - Documentation                                                │
│  - Admin Panel                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Game Server Architecture

### Core Components

#### 1. Simulation Engine

**Responsibilities:**
- Continuous game loop execution
- Entity Component System (ECS) management
- Tick-based updates (configurable, default 30 TPS)
- Time management and synchronization

**Design:**
```
SimulationEngine
├── GameLoop (30-60 TPS)
├── ECS System
│   ├── Entity Manager
│   ├── Component Store
│   └── System Scheduler
├── Time Manager
│   ├── Game Time
│   ├── Tick Counter
│   └── Delta Time
└── Event System
    ├── Event Queue
    └── Event Handlers
```

**Key Features:**
- Fixed timestep for deterministic simulation
- Variable timestep support for interpolation
- Pause/resume capability
- Time dilation for debugging

#### 2. World Management System

**Responsibilities:**
- Chunk loading and unloading
- Spatial partitioning
- Terrain generation and modification
- World persistence

**Design:**
```
WorldManager
├── ChunkManager
│   ├── Chunk Loader
│   ├── Chunk Unloader
│   ├── Chunk Cache (LRU)
│   └── Chunk Serializer
├── SpatialIndex
│   ├── Quadtree (2D)
│   └── Chunk Grid
├── TerrainSystem
│   ├── Heightmap Generator
│   ├── Resource Node Placement
│   └── Terrain Modification
└── Persistence Layer
    ├── Chunk Save Queue
    └── Periodic Full Save
```

**Chunk System:**
- **Chunk Size**: 1km × 1km (1000m × 1000m)
- **Coordinate System**: 64-bit integers (millimeter precision)
- **Active Radius**: ~5km around each player
- **Chunk States**: Unloaded, Loading, Active, Dirty, Saving

**Spatial Indexing:**
- Quadtree for 2D spatial queries
- Chunk-based grid for fast chunk lookup
- Hierarchical pathfinding support

#### 2.5. Map Generation System

**Responsibilities:**
- Generate entire planet geography using icosahedron subdivision
- Create multiple LOD levels from planet-scale to 1-meter resolution
- Export map data in standardized format for server and clients
- Support progressive detail loading via zoomable tiles

**Design:**
```
MapGenerator
├── IcosahedronGenerator
│   ├── Base Icosahedron (20 triangles)
│   ├── Subdivision Algorithm
│   │   ├── Recursive Subdivision
│   │   ├── LOD Level Management
│   │   └── Triangle Indexing
│   └── Spherical Mapping
│       ├── 3D to 2D Projection
│       └── Coordinate Transformation
├── TerrainGenerator
│   ├── Heightmap Generation (per LOD level)
│   ├── Biome Assignment
│   ├── Resource Node Placement
│   └── Feature Generation (rivers, mountains, etc.)
├── TileSystem
│   ├── Tile Manager
│   │   ├── Tile Generation (on-demand)
│   │   ├── Tile Caching
│   │   └── Tile Indexing
│   └── LOD Selector
│       ├── Zoom Level → LOD Mapping
│       └── Detail Threshold Calculator
└── ExportSystem
    ├── Format Handlers
    │   ├── Binary Format (server/client)
    │   ├── JSON Format (metadata)
    │   └── Image Format (preview)
    └── Compression
        ├── Heightmap Compression
        └── Tile Data Compression
```

**Icosahedron Approach:**
- **Base Geometry**: Regular icosahedron (20 equilateral triangles)
- **Subdivision**: Recursive subdivision of triangles (4:1 ratio per level)
- **LOD Levels**: Each subdivision level = one LOD level
- **Coordinate Mapping**: Map icosahedron triangles to world coordinates
- **Spherical Projection**: Convert 3D icosahedron to 2D tiles for rendering

**LOD System:**
- **Level 0**: Planet-scale (entire planet, very low detail)
- **Level 1-N**: Intermediate levels (regional detail)
- **Level Max**: 1-meter resolution (highest detail)
- **Tile Size**: Varies by LOD level (larger tiles at low LOD, smaller at high LOD)
- **Progressive Loading**: Load higher detail tiles as player zooms in

**Tile Structure:**
- Each tile contains:
  - Heightmap data (compressed)
  - Biome/terrain type data
  - Resource node positions
  - Metadata (bounds, LOD level, parent tile reference)
- Tiles are organized in a quadtree structure
- Tiles can be generated on-demand or pre-generated

**Export Format:**
- **Binary Format**: Efficient for server/client (MessagePack or custom binary)
- **JSON Metadata**: Human-readable metadata and configuration
- **Image Format**: Optional preview images for debugging/visualization
- **Compression**: Use appropriate compression (LZ4, gzip) for storage

**Coordinate System Integration:**
- Map generator outputs coordinates in the same 64-bit integer system
- Icosahedron triangles map to world regions
- Tile coordinates map to chunk coordinates
- Seamless integration with existing chunk system

**Usage:**
- **Pre-Generation**: Generate entire planet at low detail, then generate detailed tiles on-demand
- **On-Demand Generation**: Generate tiles as needed when players explore new areas
- **Hybrid Approach**: Pre-generate common areas, generate others on-demand

#### 3. Player Management

**Responsibilities:**
- Player session lifecycle
- Input processing and validation
- Authority and anti-cheat
- Interest management for updates

**Design:**
```
PlayerManager
├── SessionManager
│   ├── Session Creation
│   ├── Session Cleanup
│   └── Session Authentication
├── InputProcessor
│   ├── Input Validation
│   ├── Command Queue
│   └── Rate Limiting
├── AuthoritySystem
│   ├── Ownership Validation
│   ├── Action Validation
│   └── Cheat Detection
└── InterestManager
    ├── Visibility Calculation
    ├── Update Prioritization
    └── Delta Compression
```

**Session Lifecycle:**
1. Authentication (JWT validation)
2. World selection / shard assignment
3. Player entity creation / loading
4. Chunk streaming
5. Active gameplay
6. Disconnect / logout
7. Session cleanup

**Interest Management:**
- Only send updates for visible/relevant entities
- Prioritize updates by distance and importance
- Use area-of-interest (AOI) calculations
- Implement delta compression for state updates

#### 4. NPC System

**Responsibilities:**
- NPC entity lifecycle
- AI behavior execution
- Job queue management
- Pathfinding coordination

**Design:**
```
NPCSystem
├── NPCManager
│   ├── NPC Spawning
│   ├── NPC Despawning
│   └── NPC State Management
├── AISystem
│   ├── Behavior Trees
│   ├── State Machines
│   └── Decision Making
├── JobSystem
│   ├── Job Queue (per NPC)
│   ├── Job Assignment
│   └── Job Execution
└── PathfindingSystem
    ├── Hierarchical A*
    ├── Path Cache
    └── Path Smoothing
```

**NPC Types:**
- **Workers**: Resource gathering, building construction
- **Guards**: Defense, patrol
- **Traders**: Transport, market operations
- **Citizens**: Background simulation, city services

**Optimization Strategies:**
- **Sleep Mode**: NPCs far from players are "sleeping"
- **Batch Processing**: Process NPCs in batches per chunk
- **LOD AI**: Simplified AI for distant NPCs
- **Spatial Partitioning**: Only process NPCs in active chunks

#### 5. Economy System

**Responsibilities:**
- Resource management
- Trade system
- Market dynamics
- Production chains

**Design:**
```
EconomySystem
├── ResourceManager
│   ├── Resource Nodes
│   ├── Resource Storage
│   └── Resource Consumption
├── TradeSystem
│   ├── Trade Offers
│   ├── Trade Matching
│   └── Trade Execution
├── MarketSystem
│   ├── Price Calculation
│   ├── Market Orders
│   └── Market History
└── ProductionSystem
    ├── Building Production
    ├── Production Chains
    └── Resource Conversion
```

**Resource Types:**
- **Raw Materials**: Wood, Stone, Iron, Gold, etc.
- **Processed Goods**: Tools, Weapons, Food, etc.
- **Energy**: Power generation and consumption

#### 6. Building System

**Responsibilities:**
- Building placement and construction
- Building state management
- Production and consumption
- Building upgrades

**Design:**
```
BuildingSystem
├── BuildingManager
│   ├── Building Placement
│   ├── Building Construction
│   └── Building Destruction
├── BuildingTypes
│   ├── Resource Buildings
│   ├── Production Buildings
│   ├── Defense Buildings
│   └── Infrastructure Buildings
└── ProductionManager
    ├── Production Queues
    ├── Resource Consumption
    └── Output Management
```

## Client Architecture

### Web Client (Low Detail)

**Technology Stack:**
- React + TypeScript
- Three.js for 3D rendering
- Vite for build tooling
- Zustand for state management
- WebSocket for server communication

**Component Structure:**
```
WebClient
├── Core
│   ├── GameEngine
│   ├── Renderer (Three.js)
│   ├── InputHandler
│   └── NetworkClient
├── Systems
│   ├── LODSystem
│   ├── ChunkLoader
│   ├── EntityRenderer
│   └── UIManager
├── UI
│   ├── HUD
│   ├── Menus
│   ├── BuildingPlacer
│   └── ResourceDisplay
└── State
    ├── GameState
    ├── PlayerState
    └── WorldState
```

**Rendering Strategy:**
- **LOD Levels**: 4 levels based on distance
  - Level 0: Full detail (< 100m)
  - Level 1: Medium detail (100-500m)
  - Level 2: Low detail (500-2000m)
  - Level 3: Minimal detail (> 2000m)
- **Culling**: Frustum culling, occlusion culling
- **Instancing**: Use instanced rendering for similar entities
- **Batching**: Batch draw calls for performance

### High-End Client (Future)

**Technology Options:**
1. **Unity** (Recommended for cross-platform)
2. **Unreal Engine** (Maximum graphics)
3. **Native** (Rust/C++) (Best performance)

**Features:**
- Full 3D rendering with advanced lighting
- Particle systems and effects
- High-resolution textures and models
- Complex animations
- Advanced post-processing

## Networking Architecture

### Protocol Stack

```
Application Layer
├── Game Protocol (MessagePack/Protobuf)
├── Message Types
│   ├── Player Input
│   ├── World Updates
│   ├── Entity Updates
│   └── System Messages
└── Compression
    ├── Delta Compression
    └── Snapshot Compression

Transport Layer
├── WebSocket (Web Client)
└── Custom Binary Protocol (Native Client)

Network Layer
└── TCP/IP with TLS
```

### Message Types

**Client → Server:**
- `PlayerMove`: Movement input
- `PlaceBuilding`: Building placement request
- `CancelBuilding`: Cancel building placement
- `SelectEntity`: Entity selection
- `CommandEntity`: Command to entity/NPC
- `TradeOffer`: Create trade offer
- `AcceptTrade`: Accept trade offer
- `ChatMessage`: Chat message
- `Ping`: Keep-alive

**Server → Client:**
- `WorldUpdate`: Chunk data updates
- `EntityUpdate`: Entity state changes
- `EntitySpawn`: New entity spawned
- `EntityDespawn`: Entity removed
- `BuildingUpdate`: Building state changes
- `ResourceUpdate`: Resource changes
- `TradeUpdate`: Trade status updates
- `ChatMessage`: Chat message broadcast
- `Pong`: Keep-alive response
- `Error`: Error message

### Update Strategy

**Priority Levels:**
1. **Critical** (immediate): Player actions, nearby combat
2. **High** (20-30 Hz): Player position, nearby entities
3. **Medium** (5-10 Hz): Distant entities, economy updates
4. **Low** (1 Hz): Statistics, background systems

**Compression:**
- Delta compression for state updates
- Snapshot compression for full state
- MessagePack for serialization
- Optional: gzip for large messages

## Scalability Architecture

### Sharding Strategy

**World Partitioning:**
- Divide world into regions (shards)
- Each shard handles ~100-500 concurrent players
- Shards can be distributed across servers
- Players can move between shards (seamless or with loading)

**Shard Assignment:**
- Matchmaking service assigns players to shards
- Consider player location, population, load
- Support for private shards (guilds, etc.)

### Load Balancing

**Components:**
1. **Load Balancer**: Routes players to appropriate shards
2. **Shard Manager**: Tracks shard status and load
3. **Dynamic Scaling**: Add/remove shards based on load

**Database Sharding:**
- Partition by world region
- Use consistent hashing for shard assignment
- Support cross-shard queries when needed

### Caching Strategy

**Redis Usage:**
- **Hot Data**: Active chunks, player sessions
- **Pub/Sub**: Real-time updates across shards
- **Rate Limiting**: API rate limiting
- **Session Storage**: Player session data

**Cache Invalidation:**
- TTL-based expiration
- Event-based invalidation
- Write-through cache for critical data

## Security Architecture

### Authentication & Authorization

**Flow:**
1. User authenticates via website API
2. Receives JWT token
3. Client connects to game server with JWT
4. Server validates JWT
5. Creates game session

**Authorization:**
- Role-based access control (RBAC)
- Player permissions
- Admin permissions
- Subscription-based features

### Anti-Cheat

**Strategies:**
- Server-authoritative game state
- Input validation and sanitization
- Rate limiting on actions
- Statistical anomaly detection
- Client-side obfuscation (native client)

### Network Security

- TLS/SSL for all connections
- Message authentication codes (MAC)
- Optional: End-to-end encryption for sensitive data
- DDoS protection at load balancer level

## Monitoring & Observability

### Metrics

**Key Metrics:**
- TPS (Ticks Per Second)
- Player count per shard
- Network latency
- Database query performance
- Memory usage
- CPU usage

**Tools:**
- Prometheus for metrics collection
- Grafana for visualization
- Custom dashboards for game-specific metrics

### Logging

**Log Levels:**
- ERROR: Critical errors
- WARN: Warning conditions
- INFO: General information
- DEBUG: Debug information
- TRACE: Detailed tracing

**Log Aggregation:**
- ELK stack (Elasticsearch, Logstash, Kibana)
- Or Loki + Grafana
- Structured logging (JSON format)

### Alerting

**Alert Conditions:**
- High error rate
- Low TPS
- High latency
- Server crashes
- Database connection issues

## Deployment Architecture

### Containerization

**Docker Images:**
- Game server image
- Website API image
- Website frontend image
- Database migrations

### Orchestration

**Option 1: Kubernetes** (Recommended for production
- Kubernetes for orchestration
- Auto-scaling based on load
- Service discovery
- Health checks and restart policies

**Option 2: Docker Compose** (Development/Simple deployment)
- Docker Compose for local development
- Simpler setup, easier debugging

### Infrastructure Components

**Required Services:**
- PostgreSQL database (managed or self-hosted)
- Redis cache (managed or self-hosted)
- Load balancer (nginx, HAProxy, or cloud LB)
- CDN for static assets (CloudFlare, AWS CloudFront)
- Monitoring stack (Prometheus, Grafana)

## Performance Targets

### Server Performance

- **TPS**: Maintain 30 TPS minimum (target 60 TPS)
- **Latency**: < 50ms for player actions
- **NPC Processing**: Handle 10,000+ NPCs per shard
- **Concurrent Players**: 100-500 per shard

### Client Performance

**Web Client:**
- **FPS**: 30+ FPS on mid-range hardware
- **Memory**: < 500MB RAM usage
- **Network**: < 100KB/s average bandwidth

**Native Client (Future):**
- **FPS**: 60+ FPS
- **Memory**: < 2GB RAM usage
- **Network**: < 500KB/s average bandwidth

## Development Workflow

### Code Organization

**Server:**
```
/server
├── cmd/
│   └── gameserver/
│       └── main.go
├── internal/
│   ├── simulation/
│   ├── world/
│   ├── player/
│   ├── npc/
│   ├── economy/
│   └── building/
├── pkg/
│   ├── ecs/
│   ├── networking/
│   ├── database/
│   └── mapgen/  # Shared map generation utilities (if integrated)
└── config/
```

**Map Generator:**
```
/map-generator
├── cmd/
│   └── mapgen/
│       └── main.go  # Standalone tool entry point
├── internal/
│   ├── icosahedron/
│   │   ├── generator.go
│   │   ├── subdivision.go
│   │   └── mapping.go
│   ├── terrain/
│   │   ├── heightmap.go
│   │   ├── biome.go
│   │   └── features.go
│   ├── tiles/
│   │   ├── manager.go
│   │   ├── lod.go
│   │   └── indexing.go
│   └── export/
│       ├── binary.go
│       ├── json.go
│       └── image.go
└── config/
```

**Client:**
```
/client-web
├── src/
│   ├── core/
│   ├── systems/
│   ├── ui/
│   └── state/
├── public/
└── config/
```

### Testing Strategy

- **Unit Tests**: Core game logic, systems
- **Integration Tests**: System interactions
- **Load Tests**: Performance under load
- **E2E Tests**: Full game flow

### CI/CD Pipeline

1. Code commit
2. Automated tests
3. Build Docker images
4. Deploy to staging
5. Manual approval
6. Deploy to production

