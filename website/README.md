# Website

The website provides user account management, subscription management, avatar management, documentation, and admin tools.

## Technology Stack

- **Frontend**: Next.js (React) + TypeScript
- **Backend API**: Node.js/Express or Go (shared with game server)
- **Database**: PostgreSQL (shared with game server)
- **Authentication**: JWT tokens + OAuth2
- **Payment Processing**: Stripe or similar
- **Documentation**: Markdown-based (MDX) or GitBook

## Development

### Prerequisites

- Node.js 18+
- PostgreSQL 16+ (recommended; 14+ minimum, shared with game server)

### Setup

```bash
# Install dependencies
npm install  # or: yarn install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev  # or: yarn dev

# Build for production
npm run build  # or: yarn build
```

## Project Structure

```
/website
├── app/                   # Next.js app directory (if using App Router)
├── pages/                 # Next.js pages (if using Pages Router)
├── components/            # React components
├── lib/                   # Utility functions
├── api/                   # API routes
├── docs/                  # Documentation content
└── public/                # Static assets
```

## Features

- User registration and authentication
- Subscription management
- Avatar creation and management
- Game documentation
- Admin panel for game management
- Market data and trade history

## API

See `/docs/api-specification.md` for the complete API documentation.

