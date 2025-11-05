# TheVassalGame - Design Document

## Project Overview

TheVassalGame is a persistent-world 4x RTS game inspired by Warcraft and Command & Conquer, with city simulation and tower defense elements. The game features a massive world (up to 4x Earth size), continuous server-side simulation, and supports multiple client detail levels.

### Core Gameplay

- **Primary Loop**: Resource management and building
- **Secondary Systems**: Background social interaction and trade
- **Simulation Focus**: Entity-based with tens of thousands of light NPCs
- **Scale**: Hundreds to thousands of concurrent players
- **World Size**: Up to 4x Earth's surface area

## Architecture Principles

### Separation of Concerns

- **Server**: Runs continuously, handles all game simulation logic
- **Client**: Rendering and user input only
- **Website**: Account management, subscriptions, documentation, admin tools

### Key Requirements

- Server runs independently of client connections
- Massive world with efficient spatial partitioning
- Multiple client detail levels (low-end web, high-end native)
- Horizontal scalability for server components

## Recommended Tech Stack

### Game Server

**Primary Recommendation: Go**

- Excellent concurrency for handling thousands of NPCs
- Strong performance for real-time simulation
- Good networking libraries
- Easy deployment and maintenance

**Alternative: Rust**

- Maximum performance
- Memory safety guarantees
- Excellent for systems programming
- Steeper learning curve

**Technology Choices:**

- **Language**: Go (primary) or Rust (alternative)
- **Networking**: WebSocket (gobwas/ws for Go, tokio-tungstenite for Rust) or custom binary protocol
- **Database**: PostgreSQL (persistent data, complex queries)
- **Cache/State**: Redis (real-time state, pub/sub for updates)
- **Message Queue**: Redis Streams or RabbitMQ (for async tasks)

### Client - Web (Low Detail)

**Technology Choices:**

- **Framework**: React + TypeScript
- **Rendering**: Three.js or Babylon.js (WebGL) for 3D, or Phaser (2D Canvas)
- **Networking**: WebSocket client
- **State Management**: Redux or Zustand
- **Build Tool**: Vite or Next.js

### Client - High Detail (Future)

**Technology Choices:**

- **Option 1**: Unity (C#) - Cross-platform, large ecosystem
- **Option 2**: Unreal Engine (C++) - Maximum graphics fidelity
- **Option 3**: Native (Rust/C++) - Full control, best performance

### Website

**Technology Choices:**

- **Frontend**: Next.js (React) + TypeScript
- **Backend API**: Node.js/Express or Go (shared with game server)
- **Database**: PostgreSQL (shared with game server)
- **Authentication**: JWT tokens + OAuth2
- **Payment Processing**: Stripe or similar
- **Documentation**: Markdown-based (MDX) or GitBook

### Infrastructure

- **Containerization**: Docker
- **Orchestration**: Kubernetes (for scaling) or Docker Compose (simpler)
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK stack or Loki
- **CDN**: CloudFlare or AWS CloudFront (for static assets)

## System Architecture

### Server Architecture

#### Core Components

1. **Simulation Engine**

   - Continuous tick-based simulation (e.g., 20-60 ticks/second)
   - Entity Component System (ECS) for NPCs
   - Spatial partitioning (quadtree/octree) for world queries
   - Chunk-based world loading

2. **World Management**

   - Chunked world system (chunks of 1km² or similar)
   - Only active chunks fully simulated
   - LOD for distant chunks
   - Efficient serialization for persistence

3. **Player Management**

   - Player session handling
   - Authority system (server-authoritative)
   - Input validation and anti-cheat
   - Interest management (only send relevant updates)

4. **NPC System**

   - Lightweight NPC entities
   - Behavior trees or state machines
   - Job queues (resource gathering, building, etc.)
   - Efficient pathfinding (hierarchical A*)

5. **Economy System**

   - Resource management
   - Trade system
   - Market dynamics
   - Background processing (async tasks)

#### Database Schema (High-Level)

- **Players**: User accounts, authentication
- **Avatars**: Player characters, stats, inventory
- **World Chunks**: Terrain, structures, persistent state
- **Buildings**: Structures, ownership, production
- **NPCs**: Persistent NPCs (some may be temporary)
- **Resources**: Resource nodes, inventory
- **Trades**: Active trades, market history
- **Subscriptions**: Payment info, tier management

### Client Architecture

#### Web Client (Low Detail)

- **LOD System**: Multiple detail levels based on zoom/distance
- **Sprite-based rendering** for distant objects
- **Simplified animations**
- **Culling**: Only render visible chunks
- **Progressive loading**: Load chunks as player moves

#### High-End Client (Future)

- **Full 3D rendering**
- **Advanced lighting and shadows**
- **Particle effects**
- **High-resolution textures**
- **Complex animations**

### Networking Protocol

#### Communication Pattern

- **Client → Server**: Input events (movement, building placement, etc.)
- **Server → Client**: World state updates (delta compression)
- **Interest Management**: Only send relevant updates per client
- **Compression**: Protocol buffers or MessagePack

#### Update Frequency

- **High Priority**: Player actions, nearby entities (20-30 Hz)
- **Medium Priority**: Distant entities, economy updates (5-10 Hz)
- **Low Priority**: Background systems, statistics (1 Hz)

## Key Design Decisions

### World Scale

- **Chunk Size**: 1km² chunks (balance between granularity and overhead)
- **Active Simulation**: ~5km radius around players
- **Persistence**: Save chunks on change, periodic full saves
- **Coordinate System**: 64-bit integers for world positions

### NPC Management

- **Lightweight NPCs**: Minimal state, simple AI
- **Spatial Indexing**: Use quadtree for efficient queries
- **Batch Processing**: Process NPCs in batches per chunk
- **Sleeping NPCs**: NPCs far from players in "sleep" mode

### Scalability

- **Sharding**: World divided into regions (shards)
- **Load Balancing**: Distribute players across shards
- **Horizontal Scaling**: Add game server instances as needed
- **Database Sharding**: Partition by world region

### Security

- **Server Authority**: All game logic on server
- **Input Validation**: Validate all client inputs
- **Rate Limiting**: Prevent spam/DoS
- **Encryption**: TLS for all connections

## Development Phases

### Phase 1: Foundation

- Basic server architecture
- Simple client (web, low detail)
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

## Project Structure

For detailed file structure and project organization, see [PROJECT.md](../PROJECT.md#project-file-structure).

## Next Steps

1. Review and approve tech stack
2. Create detailed architecture diagrams
3. Design database schema
4. Define networking protocol
5. Create project structure
6. Begin Phase 1 implementation

