# TheVassalGame

A persistent-world 4x RTS game inspired by Warcraft and Command & Conquer, with city simulation and tower defense elements.

## Project Overview

TheVassalGame features:
- **Massive World**: Up to 4x Earth's surface area
- **Continuous Simulation**: Server runs 24/7, even without players
- **Multiple Clients**: Web client (low detail) and future native client (high detail)
- **Persistent World**: Everything persists and evolves continuously
- **Entity-Based Simulation**: Tens of thousands of light NPCs

## Project Structure

```
/docs              # Design and technical documentation
/server            # Game server (Go or Rust)
/client-web        # Web client (React + TypeScript + Three.js)
/client-native     # Native client (Future - Unity/Unreal/Native)
/website           # Website (Next.js)
/infrastructure    # Docker, Kubernetes, monitoring configs
```

## Documentation

**Start Here**: [PROJECT.md](PROJECT.md) - Entry point with project context, design principles, and quick reference.

**Technical Documentation** (in `/docs` folder):

- **[Design Document](docs/design-document.md)**: Detailed project overview, tech stack recommendations, and high-level design
- **[Architecture](docs/architecture.md)**: Detailed technical architecture (server, client, networking)
- **[Database Schema](docs/database-schema.md)**: Complete PostgreSQL database schema
- **[Networking Protocol](docs/networking-protocol.md)**: Client-server communication protocol specification
- **[API Specification](docs/api-specification.md)**: Website REST API endpoints

## Quick Start

**For complete setup instructions, see [SETUP.md](SETUP.md)**

### Quick Setup Steps

1. **Install Prerequisites**:
   - PostgreSQL 16+ (recommended), Redis 7+, Node.js 18+, Go 1.21+
   - Or use Docker Compose for services (see infrastructure/docker-compose.yml)

2. **Start Services** (using Docker Compose):
   ```bash
   cd infrastructure
   docker-compose up -d
   ```

3. **Set up Database**:
   ```bash
   # Create database and user (see SETUP.md for details)
   psql -U postgres -c "CREATE DATABASE vassalgame;"
   ```

4. **Configure Environment**:
   ```bash
   # Copy example env files and configure
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Start Development**:
   - Follow component-specific setup in [SETUP.md](SETUP.md)

## Technology Stack

Quick overview (see [Design Document](docs/design-document.md) for detailed tech stack):

- **Server**: Go (primary) or Rust (alternative), PostgreSQL 16+, Redis 7+
- **Web Client**: React + TypeScript, Three.js/Babylon.js, WebSocket
- **Website**: Next.js, Node.js/Go backend, PostgreSQL, JWT auth
- **Infrastructure**: Docker, Kubernetes/Docker Compose, Prometheus, Grafana

## Development Phases

See [Design Document - Development Phases](docs/design-document.md#development-phases) for detailed phase breakdown.

**Current Phase**: Phase 1 - Foundation

## Contributing

This is a planning document. Implementation will begin in Phase 1. For project context and design principles, see [PROJECT.md](PROJECT.md).

## License

[To be determined]

