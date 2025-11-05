# Web Client

Low-detail web client for TheVassalGame. Runs in the browser using WebGL (Three.js) or Canvas (Phaser).

## Technology Stack

- **Framework**: React + TypeScript
- **Rendering**: Three.js or Babylon.js (WebGL) or Phaser (2D Canvas)
- **State Management**: Redux or Zustand
- **Build Tool**: Vite or Next.js
- **Networking**: WebSocket client

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Setup

```bash
# Install dependencies
npm install  # or: yarn install

# Start development server
npm run dev  # or: yarn dev

# Build for production
npm run build  # or: yarn build
```

## Project Structure

```
/client-web
├── src/
│   ├── core/              # Core game engine
│   ├── systems/           # Game systems (LOD, rendering, etc.)
│   ├── ui/                # UI components
│   └── state/             # State management
├── public/                # Static assets
└── config/                # Configuration files
```

## Features

- Multiple LOD levels for performance
- Chunk-based world loading
- Sprite-based rendering for distant objects
- Progressive loading as player moves

