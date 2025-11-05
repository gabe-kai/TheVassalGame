# Game Server

The game server handles all simulation logic, world management, NPCs, economy, and player interactions.

## Technology Stack

- **Language**: Go (primary) or Rust (alternative)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Networking**: WebSocket or custom binary protocol

## Architecture

See `/docs/architecture.md` for detailed architecture documentation.

## Development

### Prerequisites

- Go 1.21+ or Rust 1.70+
- PostgreSQL 16+ (recommended; 14+ minimum)
- Redis 7+

### Setup

```bash
# Install dependencies
go mod download  # or: cargo build

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
# TODO: Add migration commands

# Start the server
go run cmd/gameserver/main.go  # or: cargo run
```

## Project Structure

```
/server
├── cmd/
│   └── gameserver/        # Main application entry point
├── internal/
│   ├── simulation/        # Simulation engine
│   ├── world/            # World management
│   ├── player/           # Player management
│   ├── npc/              # NPC system
│   ├── economy/           # Economy system
│   └── building/          # Building system
├── pkg/
│   ├── ecs/              # Entity Component System
│   ├── networking/       # Networking layer
│   └── database/         # Database layer
└── config/               # Configuration files
```

