# TheVassalGame - Project Entry Point

> **START HERE**: This file contains the essential project context, file structure, and design principles. Read this first when starting a new conversation or onboarding to the project.

## Project Overview

TheVassalGame is a persistent-world 4x RTS game inspired by Warcraft and Command & Conquer, with city simulation and tower defense elements.

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
│
├── docs/                          # Design and technical documentation
│   ├── design-document.md         # Main design document: overview, tech stack, phases
│   ├── architecture.md            # Detailed technical architecture (server, client, networking)
│   ├── database-schema.md         # Complete PostgreSQL database schema
│   ├── networking-protocol.md     # Client-server communication protocol specification
│   └── api-specification.md       # Website REST API endpoints
│
├── server/                        # Game server code
│   ├── README.md                 # Server setup and development guide
│   ├── cmd/                      # Application entry points
│   │   └── gameserver/           # Main game server executable
│   ├── internal/                 # Internal packages (not imported by other projects)
│   │   ├── simulation/           # Simulation engine
│   │   ├── world/                # World management
│   │   ├── player/               # Player management
│   │   ├── npc/                  # NPC system
│   │   ├── economy/              # Economy system
│   │   └── building/             # Building system
│   ├── pkg/                      # Public packages (can be imported by other projects)
│   │   ├── ecs/                  # Entity Component System
│   │   ├── networking/           # Networking layer
│   │   └── database/             # Database layer
│   └── config/                   # Configuration files
│
├── client-web/                    # Web client (low detail)
│   ├── README.md                 # Web client setup and development guide
│   ├── src/
│   │   ├── core/                 # Core game engine
│   │   ├── systems/              # Game systems (LOD, rendering, etc.)
│   │   ├── ui/                   # UI components
│   │   └── state/                # State management
│   ├── public/                   # Static assets
│   └── config/                   # Configuration files
│
├── client-native/                 # Native client (future - high detail)
│   └── README.md                 # Placeholder for future native client
│
├── map-generator/                  # Map generation tool (standalone or server-integrated)
│   ├── README.md                 # Map generator setup and usage
│   ├── generator/                # Core generation logic
│   ├── export/                   # Export format handlers
│   └── ui/                       # Optional UI for map generation
│
├── website/                       # Website (user management, docs, admin)
│   ├── README.md                 # Website setup and development guide
│   ├── app/                      # Next.js app directory (if using App Router)
│   ├── pages/                    # Next.js pages (if using Pages Router)
│   ├── components/               # React components
│   ├── lib/                      # Utility functions
│   ├── api/                      # API routes
│   ├── docs/                     # Documentation content
│   └── public/                   # Static assets
│
└── infrastructure/                # Infrastructure and deployment
    ├── README.md                 # Infrastructure setup guide
    ├── docker/                   # Dockerfiles and docker-compose.yml
    ├── k8s/                      # Kubernetes manifests
    ├── monitoring/               # Prometheus, Grafana configs
    └── ci-cd/                    # CI/CD pipeline configs
```

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
- **Tile System**: Zoomable map tiles that increase detail as needed
- **Export Format**: Standardized format for server and client consumption
- **Generation Tool**: Standalone application or integrated into server
- **Coordinate System**: Maps to existing 64-bit integer world coordinate system

## Development Phases

### Phase 1: Foundation (Current)
- Basic server architecture
- Simple web client (low detail)
- World chunking system
- Basic player movement
- Minimal NPC system

### Phase 2: Core Gameplay
- Building system
- Resource management
- Basic NPC behaviors
- Trade system foundation

### Phase 3: Polish & Scale
- Performance optimization
- Advanced NPC behaviors
- Social features
- Website integration

### Phase 4: High-End Client
- Native client development
- Advanced graphics
- Enhanced features

## Important Notes

### When Starting Development
1. Always check this file (PROJECT.md) for context
2. Review relevant docs/ files for detailed specifications
3. Follow the design principles above
4. Maintain server authority - no client-side game logic
5. Keep performance in mind (tens of thousands of NPCs)

### When Adding Features
- Consider scalability (will this work with 1000+ players?)
- Think about spatial partitioning (does it fit chunk system?)
- Maintain separation of concerns
- Validate all inputs on server
- Use interest management for updates

### Code Organization
- Server: Keep simulation logic separate from networking
- Client: Keep rendering separate from game state
- Website: Keep API separate from frontend
- Use clear package/module boundaries

### Code Quality Requirements
- **Testing**: Write tests for all new code
  - No function or method should be committed without tests
  - Test edge cases and error conditions
  - Maintain or improve test coverage
- **Documentation**: Document all code
  - Functions and methods: purpose, parameters, returns, side effects
  - Complex logic: explain the algorithm or approach
  - Types/interfaces: describe their purpose and usage
- **Pre-Commit**: Run checks before every commit
  - Execute test suite: `npm test`, `go test`, etc.
  - Run linters: ensure code style compliance
  - Check formatting: ensure consistent code style
  - Verify compilation: ensure code builds successfully
  - **DO NOT skip these checks** - they catch issues early

## Quick Reference

### Documentation Files
- **PROJECT.md** (this file): Entry point, context, principles
- **docs/design-document.md**: Overall design and tech stack
- **docs/architecture.md**: Detailed technical architecture
- **docs/database-schema.md**: Database schema and tables
- **docs/networking-protocol.md**: Communication protocol
- **docs/api-specification.md**: Website API endpoints

### Key Decisions
- **Server Language**: Go (primary), Rust (alternative)
- **Client Framework**: React + TypeScript for web
- **Database**: PostgreSQL 16+ (recommended) for persistence, Redis for cache
- **World Scale**: Up to 4x Earth size
- **Chunk Size**: 1km²
- **Tick Rate**: 30-60 TPS
- **NPC Scale**: Tens of thousands per shard

### Common Patterns
- **ECS**: Entity Component System for NPCs
- **Chunking**: 1km² chunks for world management
- **Spatial Indexing**: Quadtree for 2D queries
- **Delta Compression**: Only send changed fields
- **Interest Management**: AOI-based updates
- **Icosahedron Planet**: Spherical planet using subdivided icosahedron
- **LOD System**: Progressive detail levels from planet-scale to 1-meter resolution

---

**Last Updated**: 2024-01-15
**Current Phase**: Phase 1 - Foundation

