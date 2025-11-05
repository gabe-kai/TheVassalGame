# Infrastructure

Infrastructure configuration files for deployment, containerization, and orchestration.

## Contents

This directory contains:

- **Docker**: Dockerfile and docker-compose.yml files
- **Kubernetes**: K8s manifests for production deployment
- **Monitoring**: Prometheus, Grafana configurations
- **CI/CD**: GitHub Actions, GitLab CI, or similar pipeline configs

## Technology Stack

- **Containerization**: Docker
- **Orchestration**: Kubernetes (production) or Docker Compose (development)
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK stack or Loki
- **CDN**: CloudFlare or AWS CloudFront

## Development Setup

### Docker Compose

A `docker-compose.yml` file is provided for local development with PostgreSQL, Redis, and optional management tools (pgAdmin, Redis Commander).

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

**Services included:**
- **PostgreSQL 16** on port 5433 (external, to avoid conflicts with local PostgreSQL on 5432)
- **Redis 7** on port 6379
- **pgAdmin** on port 5050 (optional, for database management)
- **Redis Commander** on port 8082 (optional, for Redis management)

**Default credentials** (for development only):
- Database: `vassalgame_user` / `vassalgame_dev_password`
- pgAdmin: `admin@vassalgame.local` / `admin`

**Note:** Change default passwords in production!

## Production Deployment

### Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check status
kubectl get pods
kubectl get services
```

## Monitoring

Access monitoring dashboards:
- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090

## Services

- Game Server
- Website (Frontend + API)
- PostgreSQL Database
- Redis Cache
- Monitoring Stack

