# Development Environment Setup

This guide will help you set up your development environment for TheVassalGame.

## Prerequisites

Before starting, ensure you have the following installed:

### Required

- **Git** - Version control
- **PostgreSQL 16+** - Database (recommended; 14+ minimum)
- **Redis 7+** - Cache and pub/sub
- **Node.js 18+** - For web client and website
- **Go 1.21+** - For game server (primary)
- **Docker & Docker Compose** - For local services (optional but recommended)

### Optional

- **Rust 1.70+** - Alternative server language
- **Postman/Insomnia** - API testing
- **VS Code / Your preferred IDE** - Code editor

## Initial Project Setup

If this is a new project (no git repository yet):

```bash
# 1. Navigate to project directory
cd TheVassalGame

# 2. Initialize Git repository
git init

# 3. Create initial commit
git add .
git commit -m "Initial commit: Project setup and documentation"

# 4. (Optional) Connect to remote repository
# Create a repository on GitHub/GitLab/etc., then:
# git remote add origin <your-repository-url>
# git branch -M main
# git push -u origin main
```

## Quick Setup (Using Docker)

The fastest way to get started is using Docker Compose for local services:

```bash
# 1. Start PostgreSQL and Redis using Docker Compose
cd infrastructure
docker-compose up -d

# 2. Set up database
# (See Database Setup section below)

# 3. Set up environment variables
# Create .env file from example (see Environment Configuration section)

# 4. Start development
# Follow component-specific setup below
```

## Manual Setup

### 1. Install PostgreSQL

**Windows:**
```powershell
# Download from https://www.postgresql.org/download/windows/
# Or use chocolatey:
choco install postgresql16
```

**macOS:**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql-16 postgresql-contrib
sudo systemctl start postgresql
```

**Verify installation:**
```bash
psql --version
```

### 2. Install Redis

**Windows:**
```powershell
# Download from https://github.com/microsoftarchive/redis/releases
# Or use WSL2 with Redis
# Or use Docker: docker run -d -p 6379:6379 redis:7
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

**Verify installation:**
```bash
redis-cli ping
# Should return: PONG
```

### 3. Install Node.js

**All platforms:**
- Download from https://nodejs.org/ (LTS version 18+)
- Or use nvm: `nvm install 18 && nvm use 18`

**Verify installation:**
```bash
node --version  # Should be 18.x or higher
npm --version
```

### 4. Install Go

**Windows:**
- Download from https://go.dev/dl/
- Or use chocolatey: `choco install golang`

**macOS:**
```bash
brew install go
```

**Linux:**
```bash
sudo apt update
sudo apt install golang-go
```

**Verify installation:**
```bash
go version  # Should be 1.21 or higher
```

## Database Setup

### 1. Create Database and User

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE vassalgame;
CREATE USER vassalgame_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE vassalgame TO vassalgame_user;
\q
```

### 2. Run Migrations

```bash
# Navigate to server directory
cd server

# Run migrations (once migration system is set up)
# go run cmd/migrate/main.go up
# Or use golang-migrate:
# migrate -path ./migrations -database "postgres://vassalgame_user:password@localhost/vassalgame?sslmode=disable" up
```

### 3. Create Default Admin User

```bash
# Connect to database
psql -U vassalgame_user -d vassalgame

# Insert default admin user (password should be hashed in production)
# This will be handled by the server initialization code
```

## Environment Configuration

### Root `.env.example`

Create a `.env` file in the project root:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vassalgame
DB_USER=vassalgame_user
DB_PASSWORD=your_secure_password
DB_SSLMODE=disable

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Server
SERVER_PORT=8080
GAME_SERVER_PORT=8081
JWT_SECRET=your_jwt_secret_key_change_in_production
JWT_EXPIRY=3600

# Website
WEBSITE_URL=http://localhost:3000
API_URL=http://localhost:8080/api/v1

# Development
ENVIRONMENT=development
DEBUG=true
```

### Server `.env.example`

Create `server/.env`:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vassalgame
DB_USER=vassalgame_user
DB_PASSWORD=your_secure_password
DB_SSLMODE=disable

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Server Configuration
GAME_SERVER_PORT=8081
TICK_RATE=30
MAX_PLAYERS_PER_SHARD=500

# JWT
JWT_SECRET=your_jwt_secret_key_change_in_production
JWT_EXPIRY=3600

# Logging
LOG_LEVEL=debug
```

### Website `.env.example`

Create `website/.env.local`:

```bash
# Database
DATABASE_URL=postgresql://vassalgame_user:password@localhost:5432/vassalgame

# Next.js
NEXT_PUBLIC_API_URL=http://localhost:8080/api/v1
NEXT_PUBLIC_WEBSITE_URL=http://localhost:3000

# JWT
JWT_SECRET=your_jwt_secret_key_change_in_production

# OAuth (if using)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Stripe (if using)
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
```

## Component Setup

### Game Server

```bash
cd server

# Initialize Go module (if not already done)
go mod init github.com/yourusername/vassalgame/server

# Install dependencies
go mod download

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run tests
go test ./...

# Start development server
go run cmd/gameserver/main.go
```

### Web Client

```bash
cd client-web

# Initialize project (if not already done)
npm init -y

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev
```

### Website

```bash
cd website

# Initialize Next.js project (if not already done)
npx create-next-app@latest . --typescript --tailwind --app

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev
```

## Docker Compose Setup (Recommended)

For local development, use Docker Compose to run PostgreSQL and Redis:

```bash
cd infrastructure

# Create docker-compose.yml (see infrastructure/docker-compose.yml)
# Start services
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Verification

### 1. Check Database Connection

```bash
psql -U vassalgame_user -d vassalgame -c "SELECT version();"
```

### 2. Check Redis Connection

```bash
redis-cli ping
# Should return: PONG
```

### 3. Verify Go Installation

```bash
go version
go env
```

### 4. Verify Node.js Installation

```bash
node --version
npm --version
```

## Development Workflow

### 1. Start Services

```bash
# Terminal 1: Start PostgreSQL and Redis (if not using Docker)
# Or: docker-compose up -d

# Terminal 2: Start game server
cd server
go run cmd/gameserver/main.go

# Terminal 3: Start website
cd website
npm run dev

# Terminal 4: Start web client
cd client-web
npm run dev
```

### 2. Run Tests

```bash
# Server tests
cd server
go test ./...

# Client tests
cd client-web
npm test

# Website tests
cd website
npm test
```

### 3. Run Linters

```bash
# Server
cd server
golangci-lint run

# Client/Website
cd client-web
npm run lint

cd website
npm run lint
```

## Troubleshooting

### PostgreSQL Connection Issues

- Verify PostgreSQL is running: `psql -U postgres -c "SELECT 1;"`
- Check connection string in `.env` file
- Verify user permissions: `GRANT ALL PRIVILEGES ON DATABASE vassalgame TO vassalgame_user;`

### Redis Connection Issues

- Verify Redis is running: `redis-cli ping`
- Check Redis port (default: 6379)
- Verify firewall settings

### Port Already in Use

- Check what's using the port: `netstat -ano | findstr :8080` (Windows) or `lsof -i :8080` (macOS/Linux)
- Change port in `.env` file
- Kill the process using the port

### Go Module Issues

```bash
cd server
go mod tidy
go mod download
```

### Node.js Issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

After setup is complete:

1. Review [PROJECT.md](PROJECT.md) for project context
2. Read [docs/design-document.md](docs/design-document.md) for design details
3. Check [docs/architecture.md](docs/architecture.md) for technical architecture
4. Start with Phase 1 development (see Development Phases in design-document.md)

## Additional Resources

- [Go Documentation](https://go.dev/doc/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)
- [Node.js Documentation](https://nodejs.org/docs/)
- [Next.js Documentation](https://nextjs.org/docs)

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review component-specific README files
3. Check the documentation in `/docs`
4. Review logs for error messages

