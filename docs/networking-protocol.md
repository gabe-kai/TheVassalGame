# TheVassalGame - Networking Protocol Specification

## Overview

The networking protocol defines how clients and servers communicate. It supports both WebSocket (for web clients) and a custom binary protocol (for native clients). All messages are serialized using MessagePack for efficiency.

## Protocol Stack

```
┌─────────────────────────────────────┐
│      Application Layer               │
│  (Game Protocol Messages)           │
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│      Serialization Layer            │
│  (MessagePack / Protobuf)           │
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│      Compression Layer              │
│  (Delta Compression / Snapshot)    │
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│      Transport Layer                │
│  (WebSocket / Custom Binary)        │
└─────────────────────────────────────┘
              │
┌─────────────────────────────────────┐
│      Network Layer                  │
│  (TCP/IP with TLS)                  │
└─────────────────────────────────────┘
```

## Message Format

### Message Structure

All messages follow this structure:

```
┌─────────────────┬──────────────────┬─────────────────┐
│ Message Type    │ Sequence Number  │ Payload         │
│ (2 bytes)       │ (4 bytes)        │ (variable)      │
└─────────────────┴──────────────────┴─────────────────┘
```

**Fields:**
- **Message Type**: 2-byte unsigned integer identifying message type
- **Sequence Number**: 4-byte unsigned integer for ordering and acknowledgment
- **Payload**: MessagePack-encoded message data

### Message Types

#### Client → Server Messages

| Type ID | Message Name | Description |
|---------|-------------|-------------|
| 0x0001 | `PlayerMove` | Player movement input |
| 0x0002 | `PlayerStop` | Player stop movement |
| 0x0003 | `PlaceBuilding` | Request to place building |
| 0x0004 | `CancelBuilding` | Cancel building placement |
| 0x0005 | `SelectEntity` | Select entity/NPC |
| 0x0006 | `CommandEntity` | Command entity/NPC |
| 0x0007 | `CancelCommand` | Cancel entity command |
| 0x0008 | `TradeOffer` | Create trade offer |
| 0x0009 | `AcceptTrade` | Accept trade offer |
| 0x000A | `CancelTrade` | Cancel trade offer |
| 0x000B | `ChatMessage` | Send chat message |
| 0x000C | `RequestChunk` | Request chunk data |
| 0x000D | `Ping` | Keep-alive ping |
| 0x000E | `AuthRequest` | Authentication request |
| 0x000F | `InventoryAction` | Inventory action (move, use, etc.) |
| 0x0010 | `BuildingAction` | Building action (upgrade, cancel production, etc.) |

#### Server → Client Messages

| Type ID | Message Name | Description |
|---------|-------------|-------------|
| 0x1001 | `WorldUpdate` | Chunk data update |
| 0x1002 | `EntityUpdate` | Entity state update |
| 0x1003 | `EntitySpawn` | New entity spawned |
| 0x1004 | `EntityDespawn` | Entity removed |
| 0x1005 | `BuildingUpdate` | Building state update |
| 0x1006 | `ResourceUpdate` | Resource node update |
| 0x1007 | `TradeUpdate` | Trade status update |
| 0x1008 | `ChatMessage` | Chat message broadcast |
| 0x1009 | `PlayerState` | Player state update |
| 0x100A | `InventoryState` | Inventory state update |
| 0x100B | `Error` | Error message |
| 0x100C | `Pong` | Keep-alive response |
| 0x100D | `AuthResponse` | Authentication response |
| 0x100E | `ChunkData` | Chunk data response |
| 0x100F | `ServerInfo` | Server information |

## Message Definitions

### Client → Server Messages

#### PlayerMove (0x0001)

Player movement input.

```json
{
  "direction_x": 0.0,  // Float: -1.0 to 1.0
  "direction_y": 0.0,  // Float: -1.0 to 1.0
  "timestamp": 1234567890  // Integer: Unix timestamp in milliseconds
}
```

**Validation:**
- `direction_x` and `direction_y` must be between -1.0 and 1.0
- Magnitude must be <= 1.0 (normalized)
- Rate limit: Max 30 messages per second

#### PlayerStop (0x0002)

Stop player movement.

```json
{
  "timestamp": 1234567890
}
```

#### PlaceBuilding (0x0003)

Request to place a building.

```json
{
  "building_type_id": 1,     // Integer: Building type ID
  "world_x": 12345,          // Integer: World X coordinate
  "world_y": 67890,          // Integer: World Y coordinate
  "rotation": 0.0            // Float: Rotation in radians
}
```

**Validation:**
- Player must have required resources
- Location must be valid (not blocked, within range)
- Building type must be valid
- Rate limit: Max 1 message per 100ms

#### CancelBuilding (0x0004)

Cancel building placement.

```json
{
  "building_id": 12345  // Integer: Building ID to cancel
}
```

#### SelectEntity (0x0005)

Select an entity or NPC.

```json
{
  "entity_id": 12345,        // Integer: Entity ID
  "entity_type": "npc"       // String: "npc", "building", "resource"
}
```

#### CommandEntity (0x0006)

Command an entity/NPC.

```json
{
  "entity_id": 12345,        // Integer: Entity ID
  "command_type": "move",    // String: "move", "gather", "build", "attack"
  "target_x": 12345,         // Integer: Target X coordinate (optional)
  "target_y": 67890,         // Integer: Target Y coordinate (optional)
  "target_id": 67890,        // Integer: Target entity ID (optional)
  "data": {}                  // Object: Additional command data
}
```

**Command Types:**
- `move`: Move to location
- `gather`: Gather from resource node
- `build`: Build structure
- `attack`: Attack target
- `stop`: Stop current action

#### TradeOffer (0x0008)

Create a trade offer.

```json
{
  "item_type": "wood",        // String: Item type
  "quantity": 100,            // Integer: Quantity
  "price_per_unit": 10,       // Integer: Price per unit
  "expires_in": 3600          // Integer: Expiration time in seconds
}
```

**Validation:**
- Player must have required quantity
- Price must be positive
- Rate limit: Max 10 offers per minute

#### AcceptTrade (0x0009)

Accept a trade offer.

```json
{
  "trade_id": 12345           // Integer: Trade ID
}
```

**Validation:**
- Player must have required funds
- Trade must be open and not expired

#### ChatMessage (0x000B)

Send a chat message.

```json
{
  "channel": "global",        // String: "global", "local", "guild", "whisper"
  "message": "Hello!",        // String: Message text
  "recipient_id": 67890       // Integer: Recipient ID (for whispers)
}
```

**Validation:**
- Message length: 1-500 characters
- Rate limit: Max 10 messages per 10 seconds
- Content filtering (profanity, spam)

#### RequestChunk (0x000C)

Request chunk data.

```json
{
  "chunk_x": 123,             // Integer: Chunk X coordinate
  "chunk_y": 456             // Integer: Chunk Y coordinate
}
```

#### Ping (0x000D)

Keep-alive ping.

```json
{
  "timestamp": 1234567890    // Integer: Client timestamp
}
```

#### AuthRequest (0x000E)

Authentication request.

```json
{
  "token": "jwt_token_here"  // String: JWT authentication token
}
```

### Server → Client Messages

#### WorldUpdate (0x1001)

Chunk data update (delta compression).

```json
{
  "chunk_x": 123,             // Integer: Chunk X coordinate
  "chunk_y": 456,             // Integer: Chunk Y coordinate
  "version": 5,                // Integer: Chunk version
  "entities": [                // Array: Entity updates
    {
      "id": 12345,
      "type": "npc",
      "x": 123.45,
      "y": 678.90,
      "state": "moving"
    }
  ],
  "buildings": [               // Array: Building updates
    {
      "id": 67890,
      "type": 1,
      "x": 123.45,
      "y": 678.90,
      "health": 100,
      "construction_progress": 0.5
    }
  ],
  "resources": [               // Array: Resource node updates
    {
      "id": 11111,
      "type": "wood",
      "x": 123.45,
      "y": 678.90,
      "amount": 50
    }
  ]
}
```

#### EntityUpdate (0x1002)

Entity state update.

```json
{
  "entity_id": 12345,         // Integer: Entity ID
  "entity_type": "npc",       // String: Entity type
  "x": 123.45,                // Float: X coordinate
  "y": 678.90,                // Float: Y coordinate
  "facing_angle": 1.57,       // Float: Facing angle in radians
  "health": 100,              // Integer: Current health
  "state": "working",         // String: Current state
  "velocity_x": 0.5,          // Float: Velocity X (optional)
  "velocity_y": 0.3           // Float: Velocity Y (optional)
}
```

#### EntitySpawn (0x1003)

New entity spawned.

```json
{
  "entity_id": 12345,         // Integer: Entity ID
  "entity_type": "npc",       // String: Entity type
  "npc_type": "worker",       // String: NPC type (if applicable)
  "x": 123.45,                // Float: X coordinate
  "y": 678.90,                // Float: Y coordinate
  "facing_angle": 0.0,        // Float: Facing angle
  "owner_id": 99999,          // Integer: Owner ID (if applicable)
  "properties": {}             // Object: Additional properties
}
```

#### EntityDespawn (0x1004)

Entity removed.

```json
{
  "entity_id": 12345          // Integer: Entity ID
}
```

#### BuildingUpdate (0x1005)

Building state update.

```json
{
  "building_id": 12345,       // Integer: Building ID
  "building_type_id": 1,      // Integer: Building type ID
  "x": 123.45,                // Float: X coordinate
  "y": 678.90,                // Float: Y coordinate
  "rotation": 0.0,             // Float: Rotation
  "health": 100,               // Integer: Current health
  "max_health": 100,           // Integer: Maximum health
  "construction_progress": 1.0, // Float: Construction progress (0.0-1.0)
  "owner_id": 99999,          // Integer: Owner ID
  "production": {              // Object: Production info (optional)
    "current_item": "tools",
    "progress": 0.5,
    "queue_size": 3
  }
}
```

#### ResourceUpdate (0x1006)

Resource node update.

```json
{
  "resource_id": 12345,       // Integer: Resource node ID
  "resource_type": "wood",    // String: Resource type
  "x": 123.45,                // Float: X coordinate
  "y": 678.90,                // Float: Y coordinate
  "amount": 50,                // Integer: Remaining amount
  "max_amount": 100           // Integer: Maximum amount
}
```

#### TradeUpdate (0x1007)

Trade status update.

```json
{
  "trade_id": 12345,          // Integer: Trade ID
  "status": "completed",      // String: "open", "pending", "completed", "cancelled"
  "seller_id": 11111,         // Integer: Seller ID
  "buyer_id": 22222,          // Integer: Buyer ID (if applicable)
  "item_type": "wood",        // String: Item type
  "quantity": 100,             // Integer: Quantity
  "price_per_unit": 10        // Integer: Price per unit
}
```

#### ChatMessage (0x1008)

Chat message broadcast.

```json
{
  "sender_id": 12345,         // Integer: Sender avatar ID
  "sender_name": "Player1",   // String: Sender name
  "channel": "global",        // String: Channel name
  "message": "Hello!",        // String: Message text
  "timestamp": 1234567890     // Integer: Timestamp
}
```

#### PlayerState (0x1009)

Player state update.

```json
{
  "avatar_id": 12345,         // Integer: Avatar ID
  "x": 123.45,                // Float: X coordinate
  "y": 678.90,                // Float: Y coordinate
  "facing_angle": 1.57,       // Float: Facing angle
  "health": 100,               // Integer: Current health
  "max_health": 100,           // Integer: Maximum health
  "level": 5,                  // Integer: Level
  "experience": 5000           // Integer: Experience points
}
```

#### Error (0x100B)

Error message.

```json
{
  "code": "INVALID_LOCATION", // String: Error code
  "message": "Cannot place building here", // String: Error message
  "request_id": 12345          // Integer: Sequence number of failed request
}
```

**Error Codes:**
- `INVALID_LOCATION`: Invalid location for action
- `INSUFFICIENT_RESOURCES`: Not enough resources
- `INVALID_ENTITY`: Entity not found or invalid
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `AUTHENTICATION_FAILED`: Authentication failed
- `PERMISSION_DENIED`: Insufficient permissions
- `TRADE_EXPIRED`: Trade offer expired
- `SERVER_ERROR`: Internal server error

#### Pong (0x100C)

Keep-alive response.

```json
{
  "timestamp": 1234567890,    // Integer: Server timestamp
  "client_timestamp": 1234567890 // Integer: Original client timestamp
}
```

#### AuthResponse (0x100D)

Authentication response.

```json
{
  "success": true,            // Boolean: Authentication success
  "avatar_id": 12345,         // Integer: Avatar ID (if successful)
  "world_info": {             // Object: World information
    "region_id": 1,
    "spawn_x": 123.45,
    "spawn_y": 678.90
  },
  "error": "Invalid token"    // String: Error message (if failed)
}
```

#### ChunkData (0x100E)

Chunk data response.

```json
{
  "chunk_x": 123,             // Integer: Chunk X coordinate
  "chunk_y": 456,             // Integer: Chunk Y coordinate
  "version": 5,                // Integer: Chunk version
  "terrain": "...",            // String: Base64-encoded terrain data
  "entities": [...],           // Array: Entity data
  "buildings": [...],          // Array: Building data
  "resources": [...]           // Array: Resource node data
}
```

#### ServerInfo (0x100F)

Server information.

```json
{
  "server_name": "VassalGame Server",
  "version": "1.0.0",
  "tick_rate": 30,             // Integer: Server tick rate
  "world_size": {              // Object: World size
    "min_x": -1000000,
    "min_y": -1000000,
    "max_x": 1000000,
    "max_y": 1000000
  },
  "chunk_size": 1000,          // Integer: Chunk size in world units
  "features": ["trade", "guilds"] // Array: Enabled features
}
```

## Communication Patterns

### Connection Flow

1. **Client connects** to server via WebSocket or TCP
2. **Client sends** `AuthRequest` with JWT token
3. **Server validates** token and sends `AuthResponse`
4. **Server sends** `ServerInfo` with server details
5. **Server sends** initial `ChunkData` for player's area
6. **Normal gameplay** begins with bidirectional message exchange

### Update Frequency

**High Priority** (20-30 Hz):
- Player position and movement
- Nearby entities (< 100m)
- Active combat
- Building construction progress

**Medium Priority** (5-10 Hz):
- Distant entities (100-500m)
- Economy updates
- Resource node changes
- Trade updates

**Low Priority** (1 Hz):
- Statistics
- Background systems
- Market prices

### Interest Management

Server only sends updates for entities within the player's area of interest (AOI):

- **Default AOI**: 500m radius around player
- **Extended AOI**: 1000m for important entities (player structures, etc.)
- **Dynamic AOI**: Adjusts based on zoom level and player activity

### Delta Compression

For state updates, only send changed fields:

```json
// Full state (first update)
{
  "entity_id": 12345,
  "x": 123.45,
  "y": 678.90,
  "health": 100,
  "state": "idle"
}

// Delta update (subsequent updates)
{
  "entity_id": 12345,
  "x": 124.50  // Only changed field
}
```

### Snapshot Compression

For chunk data, use compression algorithms:

- **LZ4**: Fast compression for real-time updates
- **Gzip**: Better compression for initial chunk loads
- **Delta encoding**: Only send changes since last version

## Error Handling

### Connection Errors

- **Timeout**: If no message received for 30 seconds, send ping
- **Reconnection**: Client should automatically reconnect on disconnect
- **Backoff**: Exponential backoff for reconnection attempts

### Message Errors

- **Invalid Message**: Server responds with `Error` message
- **Sequence Mismatch**: Server may request retransmission
- **Rate Limiting**: Server may throttle or drop excess messages

## Security Considerations

### Message Validation

- Validate all input data on server
- Check bounds and types
- Sanitize string inputs
- Validate ownership and permissions

### Rate Limiting

- **Per-Player**: Limit messages per second per player
- **Per-Action**: Limit specific actions (e.g., building placement)
- **Per-Connection**: Limit total connection bandwidth

### Encryption

- **TLS/SSL**: All connections encrypted
- **Message Authentication**: Optional MAC for sensitive messages
- **Token Validation**: Validate JWT tokens on every authenticated request

## Performance Optimization

### Message Batching

Batch multiple updates into single messages when possible:

```json
{
  "type": "batch_update",
  "updates": [
    {"type": "entity_update", "data": {...}},
    {"type": "entity_update", "data": {...}},
    {"type": "building_update", "data": {...}}
  ]
}
```

### Prioritization

- **Priority Queue**: Process high-priority messages first
- **Drop Low Priority**: Drop low-priority updates if queue is full
- **Adaptive Rate**: Adjust update rate based on connection quality

### Compression

- **MessagePack**: Efficient binary serialization
- **Field Compression**: Omit default/null values
- **String Compression**: Compress long strings
- **Array Compression**: Use efficient encoding for arrays

## Testing

### Protocol Testing

- **Unit Tests**: Test message serialization/deserialization
- **Integration Tests**: Test full message exchange
- **Load Tests**: Test under high message volume
- **Latency Tests**: Measure and optimize latency

### Tools

- **Message Validator**: Validate message format
- **Protocol Analyzer**: Analyze message traffic
- **Performance Profiler**: Profile message processing

