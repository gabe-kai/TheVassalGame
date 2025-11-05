# TheVassalGame - Project Entry Point

> **START HERE**: This file contains the essential project context, file structure, and design principles. Read this first when starting a new conversation or onboarding to the project.

## Project Overview

TheVassalGame is a persistent-world 4x RTS game inspired by Warcraft and Command & Conquer, with city simulation and tower defense elements.

### Background Story

The planet has been slow-terraformed for millions of years inside a time-dilation field and is now ready for colonization. The biosphere, flora, and fauna have all been engineered by Imperial Cultivators, and one of the native species has been uplifted to sapience.

Players create an Avatar who is a promising example of the uplifted species, competing to become the magistrate of a territory on the new planet. The player who develops the best territory and generates and refines the most mana will become the ruler of the planet once the contest ends. The refined mana will be used to upgrade the planet's core multiple times and to power a dimensional portal that will bring in the colonists.

**Note:** Detailed lore and world-building will be documented in the public documentation system (lore articles). This summary provides the essential context for game design and development.

### Core Characteristics

- **Game Type**: Top-down 4x RTS with city simulator and tower defense elements
- **World Scale**: Up to 4x Earth's surface area (massive persistent world)
- **Simulation**: Continuous server-side simulation (runs 24/7, even without players)
- **Core Gameplay**: Resource management and building, with background social interaction and trade
- **NPC System**: Entity-based with tens of thousands of light NPCs
- **Player Scale**: Hundreds to thousands of concurrent players
- **Client Types**: Web client (low detail) now, native client (high detail) later

### Architecture Principles

1. **Complete Separation**: Server and client are completely separate
2. **Server Authority**: All game logic runs on the server (client is rendering only)
3. **Continuous Operation**: Server runs continuously, simulating even when no players are connected
4. **Multiple Detail Levels**: Clients can run at different detail levels (web = low, native = high)
5. **Horizontal Scalability**: System designed to scale horizontally across multiple servers

## Technology Stack

### Game Server
- **Primary**: Go (excellent concurrency for thousands of NPCs)
- **Alternative**: Rust (maximum performance)
- **Database**: PostgreSQL (persistent data)
- **Cache**: Redis (real-time state, pub/sub)
- **Networking**: WebSocket or custom binary protocol

### Web Client (Low Detail)
- **Framework**: React + TypeScript
- **Rendering**: Three.js or Babylon.js (WebGL) or Phaser (2D Canvas)
- **State Management**: Redux or Zustand
- **Build Tool**: Vite or Next.js
- **Networking**: WebSocket client

### Native Client (Future - High Detail)
- **Options**: Unity, Unreal Engine, or Native (Rust/C++)

### Website
- **Frontend**: Next.js (React) + TypeScript
- **Backend API**: Node.js/Express or Go
- **Database**: PostgreSQL (shared with game server)
- **Authentication**: JWT tokens + OAuth2
- **Payment**: Stripe
- **Documentation System**: Markdown-based viewer for game lore and user documentation
  - Users can read and comment on articles
  - Users can request edits to articles
  - StoryTellers and Admins can write, edit, archive articles
  - Admins can delete articles

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes (production) or Docker Compose (development)
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK stack or Loki

## Project File Structure

```
TheVassalGame/
│
├── PROJECT.md                    # ← THIS FILE: Entry point for project context
├── README.md                      # Quick start and overview
├── .gitignore                     # Git ignore patterns (env files, dependencies, etc.)
│
├── docs/                          # Design and technical documentation
│   ├── design-document.md         # Main design document: overview, tech stack, phases
│   ├── architecture.md            # Detailed technical architecture (server, client, networking)
│   ├── workflows.md               # Game flows and component workflows (registration, gameplay, quests)
│   ├── database-schema.md         # Complete PostgreSQL database schema
│   ├── networking-protocol.md     # Client-server communication protocol specification
│   ├── api-specification.md       # Website REST API endpoints
│   ├── building-types-reference.md # Building types reference and design documentation
│   ├── resources-reference.md     # Resource types and production chains reference
│   ├── skills-reference.md        # Skills system reference and design documentation
│   ├── techniques-reference.md    # Combat techniques reference and design documentation
│   ├── species-reference.md       # Playable species and ethnicities reference
│   ├── qi-mana-mechanics.md       # Qi and mana generation, refinement, and cultivation mechanics
│   ├── cultivation-mechanics.md   # Cultivation tiers, tribulations, and progression system
│   ├── production-mechanics.md    # Production rate calculations and modifiers
│   ├── combat-mechanics.md        # Combat system, techniques, weapons, ego, and AI behavior
│   ├── territory-expansion-mechanics.md # Territory expansion, beast tides, loyalty, contested claims
│   ├── npc-ai-behavior.md         # NPC AI, decision-making, behavior trees, and social systems
│   ├── resource-node-mechanics.md # Resource node types, gathering, depletion, respawn mechanics
│   ├── building-placement-mechanics.md # Building placement, footprints, doors, roads, relocation
│   └── DOCUMENTATION_GAPS.md      # Analysis of documentation gaps and missing systems
│
├── server/                        # Game server code (Go)
│   ├── README.md                 # Server setup and development guide
│   ├── go.mod                     # Go module definition (module: github.com/gabe-kai/vassalgame/server)
│   ├── .env                       # Server environment variables (gitignored)
│   │
│   ├── data/                      # Data files and seed data
│   │   └── seed/                  # Seed data for initial game content
│   │       ├── README.md         # Seed data structure and usage guide
│   │       ├── buildings.yaml    # Building types seed data
│   │       ├── resources.yaml    # Resource types seed data
│   │       ├── skills.yaml        # Skills system seed data
│   │       ├── techniques.yaml    # Combat techniques seed data
│   │       ├── species.yaml       # Species and ethnicities seed data
│   │       └── building_skills.yaml # Building-to-skill mappings seed data
│   │
│   ├── [Planned] cmd/             # Application entry points
│   │   └── gameserver/           # Main game server executable
│   ├── [Planned] internal/        # Internal packages (not imported by other projects)
│   │   ├── simulation/           # Simulation engine
│   │   ├── world/                # World management
│   │   ├── player/               # Player management
│   │   ├── npc/                  # NPC system
│   │   ├── economy/              # Economy system
│   │   └── building/             # Building system
│   ├── [Planned] pkg/            # Public packages (can be imported by other projects)
│   │   ├── ecs/                  # Entity Component System
│   │   ├── networking/           # Networking layer
│   │   └── database/             # Database layer
│   └── [Planned] config/          # Configuration files
│
├── client-web/                    # Web client (low detail)
│   ├── README.md                 # Web client setup and development guide
│   │
│   ├── [Planned] src/
│   │   ├── core/                 # Core game engine
│   │   ├── systems/              # Game systems (LOD, rendering, etc.)
│   │   ├── ui/                   # UI components
│   │   └── state/                # State management
│   ├── [Planned] public/         # Static assets
│   └── [Planned] config/         # Configuration files
│
├── client-native/                 # Native client (future - high detail)
│   └── README.md                 # Placeholder for future native client
│
├── map-generator/                  # Map generation tool (standalone or server-integrated)
│   ├── README.md                 # Map generator setup and usage
│   │
│   ├── [Planned] generator/       # Core generation logic
│   ├── [Planned] export/          # Export format handlers
│   └── [Planned] ui/             # Optional UI for map generation
│
├── website/                       # Website (user management, docs, admin)
│   ├── README.md                 # Website setup and development guide
│   ├── .env.local                 # Website environment variables (gitignored)
│   │
│   ├── [Planned] app/            # Next.js app directory (if using App Router)
│   ├── [Planned] pages/          # Next.js pages (if using Pages Router)
│   ├── [Planned] components/     # React components
│   │   └── documentation/        # Documentation system components (viewer, editor, comments)
│   ├── [Planned] lib/            # Utility functions
│   │   └── markdown/             # Markdown parsing and rendering utilities
│   ├── [Planned] api/            # API routes
│   │   └── docs/                 # Documentation API endpoints
│   ├── [Planned] docs/           # Static documentation content (if any)
│   └── [Planned] public/         # Static assets
│
├── infrastructure/                # Infrastructure and deployment
│   ├── README.md                 # Infrastructure setup guide
│   ├── docker-compose.yml        # Docker Compose configuration (PostgreSQL 16, Redis 7, pgAdmin, Redis Commander)
│   ├── init-db/                  # Database initialization scripts (mounted to PostgreSQL container)
│   │
│   ├── [Planned] docker/         # Dockerfiles
│   ├── [Planned] k8s/            # Kubernetes manifests
│   ├── [Planned] monitoring/     # Prometheus, Grafana configs
│   └── [Planned] ci-cd/          # CI/CD pipeline configs
│
└── [Root] .env                    # Root environment variables (gitignored, for shared config)
```

**Note**: Files marked `[Planned]` are directories that will be created during Phase 1 implementation. Files marked `[Root]` are at the project root level. `.env` files are gitignored and exist for local development.

## Design Principles

### 1. Server Authority
- **All game logic runs on the server**
- Client is rendering and input only
- Server validates all actions
- No client-side game state calculations

### 2. Continuous Simulation
- Server runs game loop continuously (30-60 TPS)
- World evolves even without players
- NPCs operate independently
- Economy and systems run in background

### 3. Spatial Partitioning
- World divided into chunks (1km² each)
- Only active chunks fully simulated
- Efficient spatial indexing (quadtree)
- Chunk-based loading and persistence

### 4. Interest Management
- Only send updates for visible/relevant entities
- Prioritize updates by distance and importance
- Area-of-interest (AOI) calculations
- Delta compression for state updates

### 5. Scalability
- Horizontal scaling via sharding
- World divided into regions (shards)
- Each shard handles ~100-500 players
- Database sharding by region

### 6. Performance
- Lightweight NPCs (minimal state)
- Batch processing for NPCs
- Sleep mode for distant NPCs
- LOD system for rendering

### 7. Security
- Server-authoritative game state
- Input validation and sanitization
- Rate limiting on actions
- TLS/SSL for all connections

### 8. Separation of Concerns
- **Server**: Simulation logic only
- **Client**: Rendering and input only
- **Website**: Account management, subscriptions, docs, admin
- No business logic in client

### 9. User Roles & Access Control
- **User Roles**: Admin, StoryTeller, Player, Observer
  - **Admin**: Full access to game server, client management, user approval, system configuration
  - **StoryTeller**: Can manage world events, NPCs, and story elements (game master role)
  - **Player**: Standard player role (default)
  - **Observer**: Read-only access for spectating/monitoring (cannot interact with game)
- **Account Access**: Users require either email verification OR admin approval to access their account
- **Default Admin**: A default Admin user is created during database initialization

### 10. Subscription Tiers
- **Initiate**: Free tier, no payment required, no expiration, basic features
- **Novice**: Paid subscription tier, enhanced features
- **Master**: Premium paid subscription tier, maximum features

### 11. Code Quality Standards
- **Comprehensive Testing**: Write tests for all functions and methods
  - Unit tests for individual functions
  - Integration tests for system interactions
  - Test coverage should be maintained
- **Documentation**: All functions and methods must have comprehensive comments
  - Explain purpose, parameters, return values, and side effects
  - Document complex algorithms and business logic
  - Include examples where helpful
- **Pre-Commit Checks**: Always run pre-commit checks before committing or pushing
  - Run tests to ensure nothing is broken
  - Run linters and formatters
  - Check for type errors and compilation issues
  - Verify code follows project standards

## Key Systems

### World System
- Chunked world (1km² chunks)
- Coordinate system: 64-bit integers (millimeter precision)
- Active simulation radius: ~5km around players
- Terrain generation and modification

### NPC System
- Lightweight entities with minimal state
- Behavior trees or state machines
- Job queues for tasks
- Hierarchical pathfinding
- Sleep mode for distant NPCs

### Economy System
- Resource management
- Trade system with market dynamics
- Production chains
- Background processing

### Building System
- Building placement and construction
- Production queues
- Resource consumption
- Building upgrades

### Map Generation System
- **Planet Representation**: Icosahedron-based spherical planet (subdivided for detail)
- **LOD System**: Multiple detail levels from planet-scale (low detail) to 1-meter resolution
- **Tile System**: Zoomable map tiles that increase detail as needed (tiles subdivided to 1-2m edge faces)
- **Planet Management**: Admin/StoryTeller interface for creating and modifying planets
- **Geography Presets**: Pangaea, few large continents, many small continents, archipelago, custom
- **Terrain Controls**: Sea level (land-sea ratio), mountain heights, ocean depths, terrain roughness
- **Documentation Integration**: Each planet automatically gets a public documentation section
- **Export Format**: Standardized format for server and client consumption
- **Generation Tool**: Standalone application or integrated into server
- **Coordinate System**: Maps to existing 64-bit integer world coordinate system

## Development Phases

See `docs/design-document.md` for detailed phase breakdown. Current focus: **Phase 1 - Foundation**.

## Development Guidelines

### When Starting Development
1. Review this file (PROJECT.md) for essential context
2. Check relevant `docs/` files for detailed specifications
3. Follow all design principles above
4. **Remember**: Docker PostgreSQL uses port 5433 (see Quick Reference below)

### Maintaining Project File Structure
**Important**: Keep the "Project File Structure" section in this file up to date. Update it:
- When files are created or deleted
- When files are significantly altered (structure changes)
- **During each pre-commit check** (before committing code)

This ensures the file structure remains accurate for future development sessions and onboarding.

### When Adding Features
- Consider scalability (1000+ players)
- Think about spatial partitioning (chunk system)
- Maintain server authority (no client-side game logic)
- Validate all inputs on server
- Use interest management for updates

## Quick Reference

### Documentation Files
- **PROJECT.md** (this file): Entry point, context, principles
- **docs/design-document.md**: Overall design and tech stack
- **docs/architecture.md**: Detailed technical architecture
- **docs/workflows.md**: Game flows and component workflows (registration, gameplay, quests, etc.)
- **docs/database-schema.md**: Database schema and tables
- **docs/networking-protocol.md**: Communication protocol
- **docs/api-specification.md**: Website API endpoints
- **docs/building-types-reference.md**: Building types reference and design documentation
- **docs/resources-reference.md**: Resource types and production chains reference
- **docs/skills-reference.md**: Skills system reference and design documentation
- **docs/techniques-reference.md**: Combat techniques reference and design documentation
- **docs/species-reference.md**: Playable species and ethnicities reference
- **docs/qi-mana-mechanics.md**: Qi and mana generation, refinement, and cultivation mechanics
- **docs/cultivation-mechanics.md**: Cultivation tiers, tribulations, and progression system
- **docs/production-mechanics.md**: Production rate calculations and modifiers
- **docs/combat-mechanics.md**: Combat system, techniques, weapons, ego, and AI behavior
- **docs/territory-expansion-mechanics.md**: Territory expansion, beast tides, loyalty, contested claims
- **docs/npc-ai-behavior.md**: NPC AI, decision-making, behavior trees, and social systems
- **docs/resource-node-mechanics.md**: Resource node types, gathering, depletion, respawn mechanics
- **docs/building-placement-mechanics.md**: Building placement, footprints, doors, roads, relocation
- **docs/DOCUMENTATION_GAPS.md**: Analysis of documentation gaps and missing systems

### Key Decisions
- **Server Language**: Go (primary), Rust (alternative)
- **Client Framework**: React + TypeScript for web
- **Database**: PostgreSQL 16+ (recommended) for persistence, Redis for cache
- **World Scale**: Up to 4x Earth size
- **Chunk Size**: 1km²
- **Tick Rate**: 30-60 TPS
- **NPC Scale**: Tens of thousands per shard

### Development Environment
- **Docker PostgreSQL**: Port 5433 (external) - avoids conflicts with local PostgreSQL on 5432
- **Docker Redis**: Port 6379 (standard)
- **Database**: `localhost:5433`, user: `vassalgame_user`, password: `vassalgame_dev_password`
- **All `.env` files use `DB_PORT=5433`** for Docker PostgreSQL

### Common Patterns
- **ECS**: Entity Component System for NPCs
- **Chunking**: 1km² chunks for world management
- **Spatial Indexing**: Quadtree for 2D queries
- **Delta Compression**: Only send changed fields
- **Interest Management**: AOI-based updates
- **Icosahedron Planet**: Spherical planet using subdivided icosahedron
- **LOD System**: Progressive detail levels from planet-scale to 1-meter resolution

---

**Current Phase**: Phase 1 - Foundation

