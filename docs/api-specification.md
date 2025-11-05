# TheVassalGame - API Specification

## Overview

The API specification defines the REST API endpoints for the website and web services. This API handles user management, authentication, subscription management, avatar management, documentation, and admin functions.

## Base URL

```
Production: https://api.vassalgame.com/v1
Development: http://localhost:8080/api/v1
```

## Authentication

Most endpoints require authentication using JWT tokens.

### Authentication Header

```
Authorization: Bearer <jwt_token>
```

### Token Format

JWT tokens are issued after successful authentication and contain:
- User ID
- Email
- Role (Admin, StoryTeller, Player, Observer)
- Permissions
- Expiration time

## API Endpoints

### Authentication

#### POST /auth/register

Register a new user account. Account access requires either email verification OR admin approval.

**Request:**
```json
{
  "email": "user@example.com",
  "username": "player1",
  "password": "secure_password_123"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": 12345,
  "message": "Registration successful. Please verify your email or wait for admin approval.",
  "requires_verification": true,
  "verification_method": "email"  // or "admin_approval" if email verification is disabled
}
```

**Status Codes:**
- `201 Created`: Registration successful
- `400 Bad Request`: Invalid input or user already exists
- `422 Unprocessable Entity`: Validation errors

**Note:** Users cannot access their account until either:
- Email is verified (`email_verified = true`), OR
- Account is approved by an Admin (`account_approved = true`)

#### POST /auth/login

Authenticate user and receive JWT token. User must have either verified email or admin approval.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "user": {
    "id": 12345,
    "email": "user@example.com",
    "username": "player1",
    "role": "Player",
    "email_verified": true,
    "account_approved": false
  }
}
```

**Response (Account Not Verified/Approved):**
```json
{
  "success": false,
  "error": {
    "code": "ACCOUNT_NOT_VERIFIED",
    "message": "Account requires email verification or admin approval to access.",
    "requires_verification": true,
    "requires_approval": false
  }
}
```

**Status Codes:**
- `200 OK`: Login successful
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account not verified or approved
- `400 Bad Request`: Invalid input

#### POST /auth/refresh

Refresh JWT token.

**Request:**
```json
{
  "token": "expired_token_here"
}
```

**Response:**
```json
{
  "success": true,
  "token": "new_jwt_token_here",
  "expires_in": 3600
}
```

**Status Codes:**
- `200 OK`: Token refreshed
- `401 Unauthorized`: Invalid or expired token

#### POST /auth/logout

Logout user (invalidate token).

**Request:** (Headers only)

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Status Codes:**
- `200 OK`: Logout successful

#### POST /auth/verify-email

Verify email address. Once verified, user can access their account.

**Request:**
```json
{
  "token": "verification_token_from_email"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email verified successfully. You can now access your account.",
  "user": {
    "id": 12345,
    "email_verified": true,
    "account_approved": false
  }
}
```

**Status Codes:**
- `200 OK`: Email verified
- `400 Bad Request`: Invalid or expired token

#### POST /auth/approve-account

Approve a user account (Admin only). Alternative to email verification.

**Request:**
```json
{
  "user_id": 12345,
  "reason": "Manual approval for trusted user"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Account approved successfully",
  "user": {
    "id": 12345,
    "account_approved": true,
    "approved_by": 1,
    "approved_at": "2024-01-15T12:00:00Z"
  }
}
```

**Status Codes:**
- `200 OK`: Account approved
- `400 Bad Request`: Invalid user ID or user already approved
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin
- `404 Not Found`: User not found

### Users

#### GET /users/me

Get current user information.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "id": 12345,
  "email": "user@example.com",
  "username": "player1",
  "role": "Player",
  "email_verified": true,
  "account_approved": false,
  "created_at": "2024-01-01T00:00:00Z",
  "subscription": {
    "tier": "novice",
    "status": "active",
    "expires_at": "2024-12-31T23:59:59Z"
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### PUT /users/me

Update current user information.

**Request:**
```json
{
  "username": "new_username",
  "email": "new_email@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 12345,
    "email": "new_email@example.com",
    "username": "new_username"
  }
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `409 Conflict`: Username/email already taken

#### POST /users/me/change-password

Change user password.

**Request:**
```json
{
  "current_password": "old_password",
  "new_password": "new_secure_password"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

**Status Codes:**
- `200 OK`: Password changed
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Current password incorrect

### Avatars

#### GET /avatars

Get all avatars for current user.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "avatars": [
    {
      "id": 11111,
      "name": "MyCharacter",
      "level": 15,
      "world_x": 12345,
      "world_y": 67890,
      "region_id": 1,
      "last_played_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### POST /avatars

Create a new avatar.

**Request:**
```json
{
  "name": "MyNewCharacter",
  "starting_region": 1
}
```

**Response:**
```json
{
  "success": true,
  "avatar": {
    "id": 22222,
    "name": "MyNewCharacter",
    "level": 1,
    "world_x": 0,
    "world_y": 0,
    "region_id": 1
  }
}
```

**Status Codes:**
- `201 Created`: Avatar created
- `400 Bad Request`: Invalid input or name taken
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Subscription tier doesn't allow more avatars

#### GET /avatars/{avatar_id}

Get avatar details.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "id": 11111,
  "name": "MyCharacter",
  "level": 15,
  "experience": 50000,
  "world_x": 12345,
  "world_y": 67890,
  "region_id": 1,
  "health": 100,
  "max_health": 100,
  "inventory": {
    "wood": 500,
    "stone": 300,
    "iron": 100
  },
  "created_at": "2024-01-01T00:00:00Z",
  "last_played_at": "2024-01-15T10:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar not found

#### PUT /avatars/{avatar_id}

Update avatar (limited fields).

**Request:**
```json
{
  "name": "NewCharacterName"
}
```

**Response:**
```json
{
  "success": true,
  "avatar": {
    "id": 11111,
    "name": "NewCharacterName",
    ...
  }
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar not found

#### DELETE /avatars/{avatar_id}

Delete avatar.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "success": true,
  "message": "Avatar deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Deleted successfully
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar not found

### Subscriptions

#### GET /subscriptions

Get current user's subscription.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "subscription": {
    "id": 999,
    "tier": "novice",
    "status": "active",
    "started_at": "2024-01-01T00:00:00Z",
    "expires_at": "2024-12-31T23:59:59Z",
    "payment_provider": "stripe",
    "features": {
      "max_avatars": 3,
      "priority_support": false,
      "exclusive_content": false
    }
  }
}
```

**Subscription Tiers:**
- **initiate**: Free tier, no payment, no expiration, basic features
- **novice**: Paid tier, enhanced features
- **master**: Premium tier, maximum features

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### POST /subscriptions

Create or update subscription.

**Request:**
```json
{
  "tier": "novice",
  "payment_method_id": "pm_1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "subscription": {
    "id": 999,
    "tier": "novice",
    "status": "active",
    ...
  }
}
```

**Status Codes:**
- `200 OK`: Subscription created/updated
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `402 Payment Required`: Payment failed

#### DELETE /subscriptions

Cancel subscription.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "success": true,
  "message": "Subscription cancelled. Active until 2024-12-31."
}
```

**Status Codes:**
- `200 OK`: Cancelled successfully
- `401 Unauthorized`: Not authenticated

### Trades

#### GET /trades

Get available trades.

**Query Parameters:**
- `item_type`: Filter by item type
- `region_id`: Filter by region
- `min_price`: Minimum price
- `max_price`: Maximum price
- `limit`: Results per page (default: 50)
- `offset`: Pagination offset

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "trades": [
    {
      "id": 12345,
      "seller_id": 11111,
      "seller_name": "Player1",
      "item_type": "wood",
      "quantity": 100,
      "price_per_unit": 10,
      "total_price": 1000,
      "expires_at": "2024-01-16T12:00:00Z"
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### GET /trades/my

Get current user's trades.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "trades": [
    {
      "id": 12345,
      "item_type": "wood",
      "quantity": 100,
      "price_per_unit": 10,
      "status": "open",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### POST /trades

Create a trade offer.

**Request:**
```json
{
  "avatar_id": 11111,
  "item_type": "wood",
  "quantity": 100,
  "price_per_unit": 10,
  "expires_in": 3600
}
```

**Response:**
```json
{
  "success": true,
  "trade": {
    "id": 12345,
    "item_type": "wood",
    "quantity": 100,
    "price_per_unit": 10,
    "status": "open",
    "expires_at": "2024-01-16T12:00:00Z"
  }
}
```

**Status Codes:**
- `201 Created`: Trade created
- `400 Bad Request`: Invalid input or insufficient resources
- `401 Unauthorized`: Not authenticated

#### POST /trades/{trade_id}/accept

Accept a trade offer.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "success": true,
  "message": "Trade completed successfully"
}
```

**Status Codes:**
- `200 OK`: Trade completed
- `400 Bad Request`: Insufficient funds or trade expired
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Trade not found

### Market

#### GET /market/prices

Get current market prices.

**Query Parameters:**
- `item_type`: Filter by item type
- `region_id`: Filter by region
- `time_range`: Time range for history (e.g., "24h", "7d", "30d")

**Request:** (Headers: Authorization, optional)

**Response:**
```json
{
  "prices": [
    {
      "item_type": "wood",
      "region_id": 1,
      "average_price": 10,
      "min_price": 8,
      "max_price": 12,
      "volume_24h": 5000,
      "trend": "up"  // "up", "down", "stable"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success

#### GET /market/history

Get market price history.

**Query Parameters:**
- `item_type`: Filter by item type
- `region_id`: Filter by region
- `start_date`: Start date (ISO 8601)
- `end_date`: End date (ISO 8601)

**Request:** (Headers: Authorization, optional)

**Response:**
```json
{
  "history": [
    {
      "date": "2024-01-15T00:00:00Z",
      "item_type": "wood",
      "average_price": 10,
      "volume": 1000
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success

### Documentation

#### GET /docs

Get documentation index.

**Response:**
```json
{
  "sections": [
    {
      "id": "getting-started",
      "title": "Getting Started",
      "articles": [
        {
          "id": "installation",
          "title": "Installation Guide",
          "url": "/docs/getting-started/installation"
        }
      ]
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success

#### GET /docs/{section}/{article}

Get documentation article.

**Response:**
```json
{
  "title": "Installation Guide",
  "content": "# Installation Guide\n\n...",
  "last_updated": "2024-01-01T00:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Article not found

### Admin

All admin endpoints require admin authentication.

#### GET /admin/users

Get user list (admin only).

**Query Parameters:**
- `search`: Search by email/username
- `status`: Filter by status
- `limit`: Results per page
- `offset`: Pagination offset

**Request:** (Headers: Authorization - Admin)

**Response:**
```json
{
  "users": [
    {
      "id": 12345,
      "email": "user@example.com",
      "username": "player1",
      "created_at": "2024-01-01T00:00:00Z",
      "subscription": {
        "tier": "novice",
        "status": "active"
      }
    }
  ],
  "total": 1000,
  "limit": 50,
  "offset": 0
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin

#### GET /admin/stats

Get server statistics (admin only).

**Request:** (Headers: Authorization - Admin)

**Response:**
```json
{
  "players": {
    "total": 10000,
    "online": 500,
    "active_24h": 2000
  },
  "world": {
    "total_chunks": 1000000,
    "active_chunks": 5000,
    "total_buildings": 50000
  },
  "economy": {
    "total_trades_24h": 10000,
    "total_volume_24h": 1000000
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin

#### PUT /admin/config

Update game configuration (admin only).

**Request:**
```json
{
  "key": "resource_respawn_rate",
  "value": 1.5
}
```

**Response:**
```json
{
  "success": true,
  "config": {
    "key": "resource_respawn_rate",
    "value": 1.5,
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin

#### POST /admin/actions/{action}

Perform admin action (admin only).

**Actions:**
- `approve_user`: Approve a user account (alternative to email verification)
- `update_user_role`: Update a user's role (Admin, StoryTeller, Player, Observer)
- `ban_user`: Ban a user
- `unban_user`: Unban a user
- `reset_avatar`: Reset an avatar
- `grant_resources`: Grant resources to avatar

**Request:**
```json
{
  "target_id": 12345,
  "reason": "Violation of terms",
  "duration": 86400  // seconds (optional, for bans)
}
```

**Response:**
```json
{
  "success": true,
  "message": "Action performed successfully"
}
```

**Status Codes:**
- `200 OK`: Action performed
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin

## Error Responses

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}  // Optional additional details
  }
}
```

### Common Error Codes

- `INVALID_REQUEST`: Invalid request format
- `UNAUTHORIZED`: Authentication required
- `FORBIDDEN`: Insufficient permissions
- `ACCOUNT_NOT_VERIFIED`: Account requires email verification or admin approval
- `NOT_FOUND`: Resource not found
- `CONFLICT`: Resource conflict (e.g., duplicate)
- `VALIDATION_ERROR`: Input validation failed
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `SERVER_ERROR`: Internal server error

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **General endpoints**: 100 requests per minute per user
- **Admin endpoints**: 200 requests per minute per admin

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642234560
```

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `limit`: Number of results per page (default: 50, max: 100)
- `offset`: Number of results to skip (default: 0)

**Response includes:**
```json
{
  "data": [...],
  "pagination": {
    "total": 1000,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

## Webhooks

Webhooks can be configured for subscription events:

### Subscription Events

- `subscription.created`
- `subscription.updated`
- `subscription.cancelled`
- `subscription.expired`

### Webhook Payload

```json
{
  "event": "subscription.updated",
  "timestamp": "2024-01-15T12:00:00Z",
  "data": {
    "user_id": 12345,
    "subscription": {...}
  }
}
```

## Versioning

API versioning is done via URL path:

- Current version: `/api/v1`
- Future versions: `/api/v2`, etc.

Version changes are backward compatible when possible. Breaking changes increment the major version.

