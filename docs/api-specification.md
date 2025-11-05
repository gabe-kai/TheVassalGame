# TheVassalGame - API Specification

## Table of Contents
- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
  - [Authentication Header](#authentication-header)
  - [Token Format](#token-format)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication-1)
  - [Users](#users)
  - [Avatars](#avatars)
  - [Subscriptions](#subscriptions)
  - [Trades](#trades)
  - [Market](#market)
  - [Documentation](#documentation)
  - [Admin](#admin)
  - [Planet Management](#planet-management)
  - [Game Data Documentation (Buildings, Resources, Species)](#game-data-documentation-buildings-resources-species)
  - [Skills Management](#skills-management)
  - [Building Skill Mappings](#building-skill-mappings)
  - [Building Management](#building-management)
  - [Building Tier Upgrades](#building-tier-upgrades)
  - [Districts & Supply Chains](#districts--supply-chains)
  - [Territory Selection](#territory-selection)
  - [Territory Management](#territory-management)
  - [NPC Management](#npc-management)
  - [NPC Relationships and Events](#npc-relationships-and-events)
  - [Cultivation Actions](#cultivation-actions)
  - [Combat & Equipment](#combat--equipment)
- [Error Responses](#error-responses)
- [Rate Limiting](#rate-limiting)
- [Pagination](#pagination)
- [Webhooks](#webhooks)
- [Versioning](#versioning)

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
  "planet_id": 1,
  "ethnicity_id": 123,   // optional
  "mortal_class": "mortal"  // "mortal" | "cultivator" (default: mortal)
}
```

**Response:**
```json
{
  "success": true,
  "avatar": {
    "id": 22222,
    "name": "MyNewCharacter",
    "planet_id": 1,
    "level": 1,
    "mortal_class": "mortal",
    "body": 10,
    "mind": 10,
    "spirit": 10,
    "qi_pool": 0.0,
    "qi_capacity": 5.0,
    "status": "pending",
    "territory_id": null
  }
}
```

**Status Codes:**
- `201 Created`: Avatar created (status: 'pending', territory not yet selected)
- `400 Bad Request`: Invalid input or name taken
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Subscription tier doesn't allow more avatars

**Note:** Avatar is created in 'pending' status. Territory must be selected before avatar becomes 'active'.

#### GET /avatars/{avatar_id}

Get avatar details.

**Request:** (Headers: Authorization)

**Response (Mortal):**
```json
{
  "id": 11111,
  "name": "MyCharacter",
  "level": 15,
  "experience": 50000,
  "mortal_class": "mortal",
  "body": 12,
  "mind": 11,
  "spirit": 10,
  "qi_pool": 2.0,
  "qi_capacity": 5.0,
  "stamina_pool": 100.0,
  "stamina_capacity": 100.0,
  "world_x": 12345,
  "world_y": 67890,
  "region_id": 1,
  "health": 100,
  "max_health": 100,
  "inventory": {
    "lumber": 500,
    "stone_blocks": 300,
    "iron": 100
  },
  "created_at": "2024-01-01T00:00:00Z",
  "last_played_at": "2024-01-15T10:30:00Z"
}
```

**Response (Cultivator):**
```json
{
  "id": 11111,
  "name": "MyCharacter",
  "level": 15,
  "experience": 50000,
  "mortal_class": "cultivator",
  "body": 25,
  "mind": 22,
  "spirit": 28,
  "strength": 24,
  "endurance": 26,
  "agility": 22,
  "speed": 20,
  "vitality": 25,
  "intellect": 21,
  "perception": 26,
  "willpower": 28,
  "charisma": 18,
  "focus": 24,
  "spirit_power": 28,
  "resonance": 24,
  "clarity": 26,
  "attunement": 22,
  "qi_pool": 240.0,
  "qi_capacity": 320.0,
  "stamina_pool": 180.0,
  "stamina_capacity": 180.0,
  "cultivation_level": 3,
  "cultivation_experience": 0.65,
  "primary_attunement": "Fire",
  "cultivation_concept": "The Phoenix's Rebirth - Strength through destruction and renewal",
  "last_tribulation_at": "2024-01-10T14:30:00Z",
  "tribulation_count": 2,
  "tribulation_failures": 0,
  "world_x": 12345,
  "world_y": 67890,
  "region_id": 1,
  "health": 250,
  "max_health": 250,
  "inventory": {
    "lumber": 500,
    "stone_blocks": 300,
    "iron": 100,
    "mana_crystal_low": 5,
    "mana_crystal_mid": 2
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

#### Character Stats Schema

Mortal (default):
```json
{
  "mortal_class": "mortal",
  "body": 10,
  "mind": 10,
  "spirit": 10,
  "qi_pool": 0.0,
  "qi_capacity": 5.0,
  "stamina_pool": 100.0,
  "stamina_capacity": 100.0
}
```

Cultivator (expanded):
```json
{
  "mortal_class": "cultivator",
  "body": 12,
  "mind": 11,
  "spirit": 14,
  "strength": 12,
  "endurance": 13,
  "agility": 11,
  "speed": 10,
  "vitality": 12,
  "intellect": 11,
  "perception": 13,
  "willpower": 14,
  "charisma": 9,
  "focus": 12,
  "spirit_power": 14,
  "resonance": 12,
  "clarity": 13,
  "attunement": 11,
  "qi_pool": 24.0,
  "qi_capacity": 60.0,
  "stamina_pool": 150.0,
  "stamina_capacity": 150.0,
  "cultivation_level": 3,
  "cultivation_experience": 0.65,
  "primary_attunement": "Fire",
  "cultivation_concept": "The Phoenix's Rebirth - Strength through destruction and renewal",
  "last_tribulation_at": "2024-01-10T14:30:00Z",
  "tribulation_count": 2,
  "tribulation_failures": 0
}
```

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
      "item_type": "lumber",
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
      "item_type": "lumber",
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
  "item_type": "lumber",
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
    "item_type": "lumber",
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
      "item_type": "lumber",
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
      "item_type": "lumber",
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

### Documentation

#### GET /docs/articles

List all published documentation articles.

**Query Parameters:**
- `category`: Filter by category (optional)
- `limit`: Number of results (default: 50, max: 100)
- `offset`: Pagination offset (default: 0)
- `search`: Search in title and content (optional)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "The History of the Realm",
      "slug": "history-of-the-realm",
      "category": "lore",
      "author": {
        "id": 5,
        "username": "storyteller1"
      },
      "view_count": 1234,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-20T15:30:00Z"
    }
  ],
  "pagination": {
    "total": 50,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated (for accessing draft articles)

**Permissions:**
- Public: Can view published articles
- Authenticated: Can view published articles
- StoryTellers/Admins: Can view all articles including drafts

#### GET /docs/articles/{slug}

Get a single documentation article by slug.

**Response:**
```json
{
  "id": 1,
  "title": "The History of the Realm",
  "slug": "history-of-the-realm",
  "content": "# The History of the Realm\n\n...",
  "content_html": "<h1>The History of the Realm</h1>\n...",
  "category": "lore",
  "author": {
    "id": 5,
    "username": "storyteller1"
  },
  "status": "published",
  "view_count": 1235,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T15:30:00Z",
  "last_edited_by": {
    "id": 5,
    "username": "storyteller1"
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Article not found or not accessible
- `401 Unauthorized`: Not authenticated (for draft articles)

**Permissions:**
- Public: Can view published articles
- StoryTellers/Admins: Can view all articles including drafts

#### POST /docs/articles

Create a new documentation article.

**Request:**
```json
{
  "title": "New Article Title",
  "slug": "new-article-slug",
  "content": "# Markdown Content\n\n...",
  "category": "guide",
  "status": "draft"  // or "published"
}
```

**Response:**
```json
{
  "id": 10,
  "title": "New Article Title",
  "slug": "new-article-slug",
  "content": "# Markdown Content\n\n...",
  "category": "guide",
  "status": "draft",
  "author": {
    "id": 5,
    "username": "storyteller1"
  },
  "created_at": "2024-01-21T12:00:00Z",
  "updated_at": "2024-01-21T12:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Article created successfully
- `400 Bad Request`: Invalid input
- `409 Conflict`: Slug already exists
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not StoryTeller or Admin

**Permissions:**
- StoryTellers and Admins only

#### PUT /docs/articles/{id}

Update an existing documentation article.

**Request:**
```json
{
  "title": "Updated Title",
  "content": "# Updated Content\n\n...",
  "category": "lore",
  "status": "published"
}
```

**Response:**
```json
{
  "id": 10,
  "title": "Updated Title",
  "slug": "new-article-slug",
  "content": "# Updated Content\n\n...",
  "category": "lore",
  "status": "published",
  "updated_at": "2024-01-21T13:00:00Z",
  "last_edited_by": {
    "id": 5,
    "username": "storyteller1"
  }
}
```

**Status Codes:**
- `200 OK`: Article updated successfully
- `404 Not Found`: Article not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not StoryTeller or Admin

**Permissions:**
- StoryTellers and Admins only

#### POST /docs/articles/{id}/archive

Archive a documentation article (soft delete).

**Response:**
```json
{
  "id": 10,
  "status": "archived",
  "archived_at": "2024-01-21T14:00:00Z",
  "archived_by": {
    "id": 5,
    "username": "storyteller1"
  }
}
```

**Status Codes:**
- `200 OK`: Article archived successfully
- `404 Not Found`: Article not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not StoryTeller or Admin

**Permissions:**
- StoryTellers and Admins only

#### DELETE /docs/articles/{id}

Permanently delete a documentation article (hard delete).

**Response:**
```json
{
  "success": true,
  "message": "Article deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Article deleted successfully
- `404 Not Found`: Article not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin

**Permissions:**
- Admins only

#### GET /docs/articles/{id}/comments

Get comments for an article.

**Query Parameters:**
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "article_id": 10,
      "user": {
        "id": 3,
        "username": "player1"
      },
      "content": "Great article!",
      "parent_comment_id": null,
      "created_at": "2024-01-21T15:00:00Z",
      "updated_at": "2024-01-21T15:00:00Z"
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Article not found

**Permissions:**
- Public: Can view comments on published articles
- Authenticated: Can view comments on published articles

#### POST /docs/articles/{id}/comments

Create a comment on an article.

**Request:**
```json
{
  "content": "This is a great article!",
  "parent_comment_id": null  // Optional: for replying to a comment
}
```

**Response:**
```json
{
  "id": 2,
  "article_id": 10,
  "user": {
    "id": 3,
    "username": "player1"
  },
  "content": "This is a great article!",
  "parent_comment_id": null,
  "created_at": "2024-01-21T16:00:00Z",
  "updated_at": "2024-01-21T16:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Comment created successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Cannot comment (article not published or user doesn't have access)
- `404 Not Found`: Article not found

**Permissions:**
- All registered users (Viewers/Players/StoryTellers/Admins) can comment on published articles

#### PUT /docs/comments/{id}

Update own comment.

**Request:**
```json
{
  "content": "Updated comment text"
}
```

**Response:**
```json
{
  "id": 2,
  "content": "Updated comment text",
  "updated_at": "2024-01-21T17:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Comment updated successfully
- `404 Not Found`: Comment not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not the comment owner

**Permissions:**
- Users can edit their own comments

#### DELETE /docs/comments/{id}

Delete own comment (soft delete).

**Response:**
```json
{
  "success": true,
  "message": "Comment deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Comment deleted successfully
- `404 Not Found`: Comment not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not the comment owner or admin

**Permissions:**
- Users can delete their own comments
- StoryTellers and Admins can delete any comment

#### POST /docs/articles/{id}/edit-requests

Request an edit to an article.

**Request:**
```json
{
  "requested_content": "# Updated Markdown Content\n\n...",
  "notes": "I think this section needs more detail about..."
}
```

**Response:**
```json
{
  "id": 1,
  "article_id": 10,
  "user": {
    "id": 3,
    "username": "player1"
  },
  "requested_content": "# Updated Markdown Content\n\n...",
  "notes": "I think this section needs more detail about...",
  "status": "pending",
  "created_at": "2024-01-21T18:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Edit request created successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Article not found

**Permissions:**
- All registered users can request edits to published articles

#### GET /docs/edit-requests

List edit requests (for StoryTellers/Admins to review).

**Query Parameters:**
- `status`: Filter by status ('pending', 'approved', 'rejected') - optional
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "article": {
        "id": 10,
        "title": "Article Title",
        "slug": "article-slug"
      },
      "user": {
        "id": 3,
        "username": "player1"
      },
      "notes": "I think this section needs more detail...",
      "status": "pending",
      "created_at": "2024-01-21T18:00:00Z"
    }
  ],
  "pagination": {
    "total": 5,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not StoryTeller or Admin

**Permissions:**
- StoryTellers and Admins only

#### PUT /docs/edit-requests/{id}/review

Approve or reject an edit request.

**Request:**
```json
{
  "status": "approved",  // or "rejected"
  "review_notes": "Good suggestion, merging this change."
}
```

**Response:**
```json
{
  "id": 1,
  "status": "approved",
  "reviewed_by": {
    "id": 5,
    "username": "storyteller1"
  },
  "reviewed_at": "2024-01-21T19:00:00Z",
  "review_notes": "Good suggestion, merging this change."
}
```

**Status Codes:**
- `200 OK`: Review completed successfully
- `400 Bad Request`: Invalid status
- `404 Not Found`: Edit request not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not StoryTeller or Admin

**Permissions:**
- StoryTellers and Admins only

**Note:** When an edit request is approved, the article should be automatically updated with the requested content, and the `last_edited_by` field should be set to the original requester's user ID.

### Planet Management

#### GET /planets

List all planets (public endpoint).

**Query Parameters:**
- `active_only`: Filter to active planets only (default: true for non-authenticated, false for StoryTellers/Admins)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Aurora",
      "description": "A lush planet with diverse biomes",
      "doc_section_slug": "planet-aurora",
      "geography_preset": "few_large_continents",
      "active": true,
      "generation_status": "completed",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success

**Permissions:**
- Public: Can view active planets
- StoryTellers/Admins: Can view all planets (including inactive)

#### GET /planets/{id}

Get planet details.

**Response:**
```json
{
  "id": 1,
  "name": "Aurora",
  "description": "A lush planet with diverse biomes",
  "doc_section_slug": "planet-aurora",
  "geography_preset": "few_large_continents",
  "sea_level": 0.0,
  "mountain_peak_height": 1.0,
  "ocean_trench_depth": 1.0,
  "terrain_roughness": 0.5,
  "icosahedron_subdivisions": 8,
  "max_lod_level": 15,
  "active": true,
  "generation_status": "completed",
  "generation_progress": 1.0,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Planet not found

**Permissions:**
- Public: Can view active planet details
- StoryTellers/Admins: Can view all planet details

#### POST /admin/planets

Create a new planet (Admin/StoryTeller only).

**Request:**
```json
{
  "name": "New Planet",
  "description": "A new planet to explore",
  "geography_preset": "few_large_continents",
  "sea_level": 0.0,
  "mountain_peak_height": 1.0,
  "ocean_trench_depth": 1.0,
  "terrain_roughness": 0.5,
  "icosahedron_subdivisions": 8,
  "max_lod_level": 15,
  "generator_seed": null
}
```

**Response:**
```json
{
  "id": 2,
  "name": "New Planet",
  "description": "A new planet to explore",
  "doc_section_slug": "planet-new-planet",
  "geography_preset": "few_large_continents",
  "generation_status": "pending",
  "generation_progress": 0.0,
  "created_at": "2024-01-21T12:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Planet created, generation queued
- `400 Bad Request`: Invalid input
- `409 Conflict`: Planet name already exists
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

**Note:** Planet generation is queued asynchronously. Use GET /admin/planets/{id}/status to check generation progress.

#### PUT /admin/planets/{id}

Update planet settings (Admin/StoryTeller only).

**Request:**
```json
{
  "name": "Updated Planet Name",
  "description": "Updated description",
  "active": true
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Updated Planet Name",
  "description": "Updated description",
  "active": true,
  "updated_at": "2024-01-21T13:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `400 Bad Request`: Invalid input (e.g., cannot change name if avatars exist)
- `404 Not Found`: Planet not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

**Note:** Generation parameters cannot be modified after generation. Use POST /admin/planets/{id}/regenerate to regenerate planet.

#### GET /admin/planets/{id}/status

Get planet generation status and progress (Admin/StoryTeller only).

**Response:**
```json
{
  "id": 2,
  "generation_status": "generating",
  "generation_progress": 0.65,
  "estimated_completion": "2024-01-21T14:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Planet not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### POST /admin/planets/{id}/regenerate

Regenerate planet with new or updated parameters (Admin only).

**Request:**
```json
{
  "geography_preset": "archipelago",
  "sea_level": 0.3,
  "mountain_peak_height": 1.2,
  "ocean_trench_depth": 1.1,
  "terrain_roughness": 0.7,
  "confirm": true
}
```

**Response:**
```json
{
  "id": 2,
  "generation_status": "pending",
  "message": "Planet regeneration queued. Warning: This will regenerate all terrain data."
}
```

**Status Codes:**
- `200 OK`: Regeneration queued
- `400 Bad Request`: Invalid input or confirmation not provided
- `404 Not Found`: Planet not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin

**Permissions:**
- Admins only

**Warning:** Regeneration will recreate all terrain data. Existing avatars/buildings may be affected.

#### GET /planets/{id}/documentation

Get planet documentation section (public endpoint).

**Response:**
```json
{
  "planet_id": 1,
  "doc_section": {
    "slug": "planet-aurora",
    "title": "Planet: Aurora",
    "content": "# Planet Aurora\n\n...",
    "category": "lore"
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Planet or documentation not found

**Permissions:**
- Public access

**Note:** Each planet automatically has a documentation section created. StoryTellers/Admins can edit this documentation.

### Game Data Documentation (Buildings, Resources, Species, Skills)

The public documentation system automatically syncs with game database tables for buildings, resources, species, and skills. Each entity automatically gets a documentation article that can be viewed and edited.

#### GET /docs/buildings

List all building types (public endpoint, auto-synced from database).

**Query Parameters:**
- `category`: Filter by category ('civic', 'resource', 'production', 'defense', 'infrastructure', 'commercial', 'research') - optional
- `building_path`: Filter by building path within category - optional
- `status`: Filter by status ('active', 'archived') - default: 'active' for public, 'all' for StoryTellers/Admins
- `limit`: Number of results (default: 50, max: 100)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Sect Hall",
      "slug": "sect-hall",
      "category": "civic",
      "building_path": "sect_hall",
      "description": "The central administrative and social hub for territory governance",
      "base_build_time": 300,
      "max_health": 1000,
      "max_durability": 1000,
      "base_cost_data": {
        "lumber": 100,
        "stone_blocks": 50,
        "qi_crystal": 10
      },
      "max_employment_slots": 5,
      "relocatable": false,
      "status": "active"
    }
  ],
  "pagination": {
    "total": 25,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Status Codes:**
- `200 OK`: Success

**Permissions:**
- Public: Can view active buildings
- StoryTellers/Admins: Can view all buildings including archived

#### GET /docs/buildings/{slug}

Get building type details and documentation (public endpoint).

**Response:**
```json
{
  "id": 1,
  "name": "Qi Refinery",
  "slug": "qi-refinery",
  "category": "production",
  "description": "Refines raw qi into mana",
  "detailed_description": "A specialized building that processes raw qi energy...",
  "size_x": 5,
  "size_y": 5,
  "build_time": 300,
  "health": 1000,
  "cost_data": {
        "lumber": 100,
    "stone_blocks": 50,
    "qi_crystal": 10
  },
  "production_data": {
    "output": "mana",
    "rate": 5.0
  },
  "mana_generation": 5.0,
  "status": "active",
  "skills": {
    "required": ["construction"],
    "recommended": ["logistics"],
    "employment": ["administration"]
  },
  "doc_article": {
    "slug": "building-qi-refinery",
    "title": "Building: Qi Refinery",
    "content": "# Qi Refinery\n\n...",
    "content_html": "<h1>Qi Refinery</h1>\n...",
    "category": "reference"
  },
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T15:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Building type not found

**Permissions:**
- Public: Can view active building types
- StoryTellers/Admins: Can view all building types including archived

#### POST /admin/buildings

Create a new building type (Admin/StoryTeller only).

**Request:**
```json
{
  "name": "Sect Hall",
  "category": "civic",
  "building_path": "sect_hall",
  "description": "The central administrative and social hub for territory governance",
  "detailed_description": "The Sect Hall serves as the heart of your territory...",
  "footprint_polygon": {
    "vertices": [
      {"x": -3, "y": -3},
      {"x": 3, "y": -3},
      {"x": 3, "y": 3},
      {"x": -3, "y": 3}
    ]
  },
  "door_positions": [
    {"x": 0, "y": -3, "facing": 3.14159}
  ],
  "base_build_time": 300,
  "base_cost_data": {
    "lumber": 100,
    "stone_blocks": 50,
    "qi_crystal": 10
  },
  "max_health": 1000,
  "max_durability": 1000,
  "base_durability": 1000,
  "max_employment_slots": 5,
  "required_workers": 0,
  "employment_skill": "Administration",
  "passive_resources": null,
  "relocatable": false,
  "maintenance_required": true
}
```

**Response:**
```json
{
  "id": 10,
  "name": "Sect Hall",
  "slug": "sect-hall",
  "category": "civic",
  "building_path": "sect_hall",
  "status": "active",
  "doc_article": {
    "slug": "building-sect-hall",
    "title": "Building: Sect Hall"
  },
  "created_at": "2024-01-21T16:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Building type created, documentation article auto-generated
- `400 Bad Request`: Invalid input
- `409 Conflict`: Name or slug already exists
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

**Note:** Creating a building type automatically creates a documentation article. The article slug is auto-generated from the building name.

#### PUT /admin/buildings/{id}

Update building type (Admin/StoryTeller only).

**Request:**
```json
{
  "description": "Updated description",
  "detailed_description": "Extended lore description...",
  "base_cost_data": {
    "lumber": 120,
    "stone_blocks": 60
  },
  "max_employment_slots": 6
}
```

**Response:**
```json
{
  "id": 10,
  "name": "Mana Tower",
  "description": "Updated description",
  "updated_at": "2024-01-21T17:00:00Z",
  "updated_by": {
    "id": 5,
    "username": "storyteller1"
  }
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `404 Not Found`: Building type not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

**Note:** Updates automatically sync to the documentation article. StoryTellers/Admins can also edit the documentation article directly for lore/details.

#### POST /admin/buildings/{id}/archive

Archive a building type (Admin/StoryTeller only).

**Response:**
```json
{
  "id": 10,
  "status": "archived",
  "archived_at": "2024-01-21T18:00:00Z",
  "archived_by": {
    "id": 5,
    "username": "storyteller1"
  }
}
```

**Status Codes:**
- `200 OK`: Building type archived
- `404 Not Found`: Building type not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

**Note:** Archived building types are hidden from public documentation but remain in the game. Existing buildings of this type continue to function.

#### DELETE /admin/buildings/{id}

Permanently delete a building type (Admin only).

**Response:**
```json
{
  "success": true,
  "message": "Building type deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Building type deleted
- `404 Not Found`: Building type not found
- `400 Bad Request`: Cannot delete if buildings of this type exist
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin

**Permissions:**
- Admins only

**Warning:** Cannot delete if any buildings of this type exist in the game world.

#### GET /docs/resources

List all resource types (public endpoint, auto-synced from database).

**Query Parameters:**
- `category`: Filter by category ('raw_material', 'processed_material', 'refined_product', 'specialized', 'crafted', 'commerce') - optional
- `rarity`: Filter by rarity ('common', 'uncommon', 'rare', 'epic', 'legendary') - optional
- `production_chain`: Filter by production chain ('wood', 'stone', 'metal', 'essence', 'qi', 'food', 'herb', 'water', 'crafting', 'commerce', 'beast') - optional
- `production_tier`: Filter by production tier (1-5) - optional
- `status`: Filter by status ('active', 'archived') - default: 'active' for public, 'all' for StoryTellers/Admins
- `limit`: Number of results (default: 50, max: 100)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Lumber",
      "slug": "lumber",
      "category": "raw_material",
      "description": "Basic wood harvested from forests",
      "rarity": "common",
      "gathering_method": "harvesting",
      "base_value": 1,
      "stack_size": 1000,
      "production_chain": "wood",
      "production_tier": 1,
      "created_from": null,
      "status": "active"
    }
  ],
  "pagination": {
    "total": 30,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Status Codes:**
- `200 OK`: Success

**Permissions:**
- Public: Can view active resources
- StoryTellers/Admins: Can view all resources including archived

#### GET /docs/resources/{slug}

Get resource type details and documentation (public endpoint).

**Response:**
```json
{
  "id": 1,
  "name": "Refined Lumber",
  "slug": "refined-lumber",
  "category": "processed_material",
  "description": "Processed and refined wood",
  "detailed_description": "Refined lumber is created by processing raw lumber...",
  "rarity": "common",
  "gathering_method": "processing",
  "base_value": 3,
  "stack_size": 500,
  "production_chain": "wood",
  "production_tier": 2,
  "created_from": ["lumber"],
  "status": "active",
  "doc_article": {
    "slug": "resource-refined-lumber",
    "title": "Resource: Refined Lumber",
    "content": "# Refined Lumber\n\n...",
    "category": "reference"
  },
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T15:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Resource type not found

**Permissions:**
- Public: Can view active resource types
- StoryTellers/Admins: Can view all resource types including archived

#### POST /admin/resources

Create a new resource type (Admin/StoryTeller only).

**Request:**
```json
{
  "name": "Spirit Timber",
  "category": "refined_product",
  "description": "Qi-infused wood with spiritual properties",
  "detailed_description": "Spirit timber is created by infusing wood with qi...",
  "rarity": "uncommon",
  "gathering_method": "crafting",
  "base_value": 20,
  "stack_size": 100,
  "production_chain": "wood",
  "production_tier": 3,
  "created_from": ["lumber", "refined_lumber", "qi_crystal"]
}
```

**Response:**
```json
{
  "id": 15,
  "name": "Spirit Timber",
  "slug": "spirit-timber",
  "category": "refined_product",
  "production_chain": "wood",
  "production_tier": 3,
  "created_from": ["lumber", "refined_lumber", "qi_crystal"],
  "status": "active",
  "doc_article": {
    "slug": "resource-spirit-timber",
    "title": "Resource: Spirit Timber"
  },
  "created_at": "2024-01-21T16:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Resource type created, documentation article auto-generated
- `400 Bad Request`: Invalid input
- `409 Conflict`: Name or slug already exists
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### PUT /admin/resources/{id}

Update resource type (Admin/StoryTeller only).

**Request:**
```json
{
  "description": "Updated description",
  "detailed_description": "Extended lore description...",
  "base_value": 120,
  "production_tier": 3,
  "created_from": ["lumber", "refined_lumber", "qi_crystal"]
}
```

**Response:**
```json
{
  "id": 15,
  "name": "Mana Essence",
  "description": "Updated description",
  "updated_at": "2024-01-21T17:00:00Z",
  "updated_by": {
    "id": 5,
    "username": "storyteller1"
  }
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `404 Not Found`: Resource type not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### POST /admin/resources/{id}/archive

Archive a resource type (Admin/StoryTeller only).

**Response:**
```json
{
  "id": 15,
  "status": "archived",
  "archived_at": "2024-01-21T18:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Resource type archived
- `404 Not Found`: Resource type not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### DELETE /admin/resources/{id}

Permanently delete a resource type (Admin only).

**Response:**
```json
{
  "success": true,
  "message": "Resource type deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Resource type deleted
- `404 Not Found`: Resource type not found
- `400 Bad Request`: Cannot delete if resource nodes or items of this type exist
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin

**Permissions:**
- Admins only

#### GET /docs/species

List all species (public endpoint, auto-synced from database).

**Query Parameters:**
- `category`: Filter by category ('uplifted', 'native_fauna', 'native_flora', 'engineered', 'other') - optional
- `sapient`: Filter by sapient status (true/false) - optional
- `status`: Filter by status ('active', 'archived') - default: 'active' for public, 'all' for StoryTellers/Admins
- `limit`: Number of results (default: 50, max: 100)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Uplifted Terran",
      "slug": "uplifted-terran",
      "category": "uplifted",
      "description": "The native species uplifted to sapience",
      "sapient": true,
      "size_category": "medium",
      "status": "active"
    }
  ],
  "pagination": {
    "total": 20,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Status Codes:**
- `200 OK`: Success

**Permissions:**
- Public: Can view active species
- StoryTellers/Admins: Can view all species including archived

#### GET /docs/species/{slug}

Get species details and documentation (public endpoint).

**Response:**
```json
{
  "id": 1,
  "name": "Uplifted Terran",
  "slug": "uplifted-terran",
  "category": "uplifted",
  "description": "The native species uplifted to sapience",
  "detailed_description": "Originally a native species of the planet...",
  "sapient": true,
  "size_category": "medium",
  "habitat": "temperate",
  "diet": "omnivore",
  "status": "active",
  "ethnicities": [
    {
      "id": 101,
      "name": "Falcon",
      "slug": "avian-falcon",
      "description": "Swift, sharp-eyed, and disciplined",
      "qi_themes": ["wind", "precision", "speed"],
      "stat_modifiers": {"perception": 2, "speed": 2, "willpower": -1},
      "status": "active"
    }
  ],
  "doc_article": {
    "slug": "species-uplifted-terran",
    "title": "Species: Uplifted Terran",
    "content": "# Uplifted Terran\n\n...",
    "category": "lore"
  },
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T15:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Species not found

**Permissions:**
- Public: Can view active species
- StoryTellers/Admins: Can view all species including archived

#### POST /admin/species

Create a new species (Admin/StoryTeller only).

**Request:**
```json
{
  "name": "Forest Guardian",
  "category": "native_fauna",
  "description": "A large native predator",
  "sapient": false,
  "size_category": "large",
  "habitat": "forest",
  "diet": "carnivore"
}
```

**Response:**
```json
{
  "id": 10,
  "name": "Forest Guardian",
  "slug": "forest-guardian",
  "category": "native_fauna",
  "status": "active",
  "doc_article": {
    "slug": "species-forest-guardian",
    "title": "Species: Forest Guardian"
  },
  "created_at": "2024-01-21T16:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Species created, documentation article auto-generated
- `400 Bad Request`: Invalid input
- `409 Conflict`: Name or slug already exists
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### PUT /admin/species/{id}

Update species (Admin/StoryTeller only).

**Request:**
```json
{
  "description": "Updated description",
  "detailed_description": "Extended lore/biology description...",
  "habitat": "forest,mountain"
}
```

**Response:**
```json
{
  "id": 10,
  "name": "Forest Guardian",
  "description": "Updated description",
  "updated_at": "2024-01-21T17:00:00Z",
  "updated_by": {
    "id": 5,
    "username": "storyteller1"
  }
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `404 Not Found`: Species not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### POST /admin/species/{id}/archive

Archive a species (Admin/StoryTeller only).

**Response:**
```json
{
  "id": 10,
  "status": "archived",
  "archived_at": "2024-01-21T18:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Species archived
- `404 Not Found`: Species not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### DELETE /admin/species/{id}

Permanently delete a species (Admin only).

**Response:**
```json
{
  "success": true,
  "message": "Species deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Species deleted
- `404 Not Found`: Species not found
- `400 Bad Request`: Cannot delete if NPCs of this species exist
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin

**Permissions:**
- Admins only

#### POST /admin/species-ethnicities

Create a new species ethnicity (Admin/StoryTeller only).

**Request:**
```json
{
  "species_id": 1,
  "name": "Falcon",
  "slug": "avian-falcon",
  "description": "Swift, sharp-eyed, and disciplined",
  "qi_themes": ["wind", "precision", "speed"],
  "stat_modifiers": {"perception": 2, "speed": 2, "willpower": -1}
}
```

**Response:**
```json
{
  "id": 101,
  "species_id": 1,
  "name": "Falcon",
  "slug": "avian-falcon",
  "status": "active",
  "created_at": "2024-01-21T16:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Ethnicity created
- `400 Bad Request`: Invalid input
- `409 Conflict`: Name/slug already exists for species
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

#### PUT /admin/species-ethnicities/{id}

Update a species ethnicity (Admin/StoryTeller only).

**Request:**
```json
{
  "description": "Updated description",
  "qi_themes": ["wind", "precision", "focused_strikes"],
  "stat_modifiers": {"perception": 2, "speed": 1, "willpower": 1}
}
```

**Response:**
```json
{
  "id": 101,
  "name": "Falcon",
  "updated_at": "2024-01-21T17:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `404 Not Found`: Ethnicity not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

#### POST /admin/species-ethnicities/{id}/archive

Archive a species ethnicity (Admin/StoryTeller only).

**Response:**
```json
{
  "id": 101,
  "status": "archived",
  "archived_at": "2024-01-21T18:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Ethnicity archived
- `404 Not Found`: Ethnicity not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

#### DELETE /admin/species-ethnicities/{id}

Permanently delete a species ethnicity (Admin only).

**Response:**
```json
{
  "success": true,
  "message": "Species ethnicity deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Ethnicity deleted
- `404 Not Found`: Ethnicity not found
- `400 Bad Request`: Cannot delete if referenced by avatars/NPCs
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin

**Warning:** Cannot delete if any NPCs of this species exist in the game world.

### Skills Management

#### GET /docs/skills

List all skills (public endpoint).

**Query Parameters:**
- `category`: Filter by category ('core', 'gathering', 'processing', 'arcane', 'civic', 'combat') - optional
- `status`: Filter by status ('active', 'archived') - default: 'active' for public, 'all' for StoryTellers/Admins
- `limit`: Number of results (default: 50, max: 100)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Construction",
      "slug": "construction",
      "category": "core",
      "description": "Ability to build and construct structures",
      "primary_attributes": {"strength": 0.5, "focus": 0.5},
      "derived_influences": {
        "build_time_multiplier": -0.01,
        "cost_reduction": 0.005
      },
      "status": "active"
    }
  ],
  "pagination": {
    "total": 28,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Status Codes:**
- `200 OK`: Success

**Permissions:**
- Public: Can view active skills
- StoryTellers/Admins: Can view all skills including archived

#### GET /docs/skills/{slug}

Get skill details and documentation (public endpoint).

**Response:**
```json
{
  "id": 1,
  "name": "Construction",
  "slug": "construction",
  "category": "core",
  "description": "Ability to build and construct structures",
  "detailed_description": "Construction skill affects build time and resource costs...",
  "primary_attributes": {
    "strength": 0.5,
    "focus": 0.5
  },
  "derived_influences": {
    "build_time_multiplier": -0.01,
    "cost_reduction": 0.005
  },
  "status": "active",
  "doc_article": {
    "slug": "skill-construction",
    "title": "Skill: Construction",
    "content": "# Construction\n\n...",
    "category": "reference"
  },
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T15:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Skill not found

**Permissions:**
- Public: Can view active skills
- StoryTellers/Admins: Can view all skills including archived

#### POST /admin/skills

Create a new skill (Admin/StoryTeller only).

**Request:**
```json
{
  "name": "Advanced Alchemy",
  "category": "arcane",
  "description": "Advanced alchemical techniques",
  "primary_attributes": {"intellect": 0.6, "focus": 0.4},
  "derived_influences": {
    "potion_potency": 0.02,
    "yield_bonus": 0.01
  }
}
```

**Response:**
```json
{
  "id": 30,
  "name": "Advanced Alchemy",
  "slug": "advanced-alchemy",
  "category": "arcane",
  "status": "active",
  "doc_article": {
    "slug": "skill-advanced-alchemy",
    "title": "Skill: Advanced Alchemy"
  },
  "created_at": "2024-01-21T16:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Skill created, documentation article auto-generated
- `400 Bad Request`: Invalid input
- `409 Conflict`: Name or slug already exists
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### PUT /admin/skills/{id}

Update skill (Admin/StoryTeller only).

**Request:**
```json
{
  "description": "Updated description",
  "primary_attributes": {"intellect": 0.7, "focus": 0.3},
  "derived_influences": {
    "potion_potency": 0.025,
    "yield_bonus": 0.015
  }
}
```

**Response:**
```json
{
  "id": 30,
  "name": "Advanced Alchemy",
  "updated_at": "2024-01-21T17:00:00Z",
  "updated_by": {
    "id": 5,
    "username": "storyteller1"
  }
}
```

**Status Codes:**
- `200 OK`: Updated successfully
- `404 Not Found`: Skill not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### POST /admin/skills/{id}/archive

Archive a skill (Admin/StoryTeller only).

**Response:**
```json
{
  "id": 30,
  "status": "archived",
  "archived_at": "2024-01-21T18:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Skill archived
- `404 Not Found`: Skill not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### DELETE /admin/skills/{id}

Permanently delete a skill (Admin only).

**Response:**
```json
{
  "success": true,
  "message": "Skill deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Skill deleted
- `404 Not Found`: Skill not found
- `400 Bad Request`: Cannot delete if referenced by building skill mappings
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin

**Warning:** Cannot delete if any building types or tiers reference this skill.

### Building Skill Mappings

#### GET /admin/buildings/{id}/skills

Get all skills mapped to a building type (Admin/StoryTeller only).

**Response:**
```json
{
  "building_type": {
    "id": 5,
    "name": "Sect Hall",
    "slug": "sect-hall"
  },
  "skills": {
    "required": [
      {
        "id": 1,
        "skill_id": 20,
        "skill": {
          "id": 20,
          "name": "Administration",
          "slug": "administration",
          "category": "civic"
        },
        "relation": "required",
        "notes": "Required for basic operations"
      }
    ],
    "recommended": [
      {
        "id": 2,
        "skill_id": 15,
        "skill": {
          "id": 15,
          "name": "Logistics",
          "slug": "logistics",
          "category": "civic"
        },
        "relation": "recommended",
        "notes": null
      }
    ],
    "employment": [
      {
        "id": 3,
        "skill_id": 20,
        "skill": {
          "id": 20,
          "name": "Administration",
          "slug": "administration",
          "category": "civic"
        },
        "relation": "employment",
        "notes": "Workers develop this skill while employed"
      }
    ]
  },
  "tier_overrides": {
    "1": [],
    "2": [],
    "3": [
      {
        "id": 10,
        "building_tier_id": 25,
        "skill_id": 15,
        "skill": {
          "id": 15,
          "name": "Logistics",
          "slug": "logistics"
        },
        "relation": "required",
        "notes": "Tier 3 requires Logistics in addition to Administration"
      }
    ],
    "4": [],
    "5": [],
    "6": []
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Building type not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

**Note:** Response includes both building type level skills (applies to all tiers) and tier-specific overrides (from `building_tier_skills` table).

#### POST /admin/buildings/{id}/skills

Add or update skill mappings for a building type (Admin/StoryTeller only).

**Request:**
```json
{
  "skill_id": 20,
  "relation": "employment",
  "notes": "Workers develop Administration skill",
  "tier_specific": false
}
```

**Response:**
```json
{
  "success": true,
  "mapping": {
    "id": 3,
    "building_type_id": 5,
    "skill_id": 20,
    "relation": "employment",
    "notes": "Workers develop Administration skill"
  },
  "message": "Skill mapping added at building type level"
}
```

**Status Codes:**
- `201 Created`: Mapping created (if new)
- `200 OK`: Mapping updated (if existing)
- `400 Bad Request`: Invalid input
- `404 Not Found`: Building type or skill not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

#### POST /admin/buildings/{id}/tiers/{tier_level}/skills

Add or update tier-specific skill mapping (Admin/StoryTeller only).

**Request:**
```json
{
  "skill_id": 15,
  "relation": "required",
  "notes": "Tier 3 requires Logistics in addition to base skills"
}
```

**Response:**
```json
{
  "success": true,
  "mapping": {
    "id": 10,
    "building_tier_id": 25,
    "skill_id": 15,
    "relation": "required",
    "notes": "Tier 3 requires Logistics in addition to base skills"
  },
  "message": "Tier-specific skill mapping added"
}
```

**Status Codes:**
- `201 Created`: Mapping created (if new)
- `200 OK`: Mapping updated (if existing)
- `400 Bad Request`: Invalid input or tier level out of range (1-6)
- `404 Not Found`: Building type, tier, or skill not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

**Note:** Tier-specific mappings override building type level mappings for the same skill+relation.

#### DELETE /admin/buildings/{id}/skills/{skill_id}

Remove a skill mapping from a building type (Admin/StoryTeller only).

**Query Parameters:**
- `relation`: Filter by relation type ('required', 'recommended', 'employment') - optional, if not provided removes all relations
- `tier_level`: If provided, removes tier-specific mapping instead of building type level (1-6) - optional

**Response:**
```json
{
  "success": true,
  "message": "Skill mapping removed successfully"
}
```

**Status Codes:**
- `200 OK`: Mapping removed successfully
- `404 Not Found`: Building type, skill, or mapping not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

**Permissions:**
- Admins and StoryTellers only

### Building Management

#### POST /game/buildings

Place a new building (Game Server API - WebSocket or REST).

**Request:**
```json
{
  "building_type_id": 5,
  "world_x": 12345,
  "world_y": 67890,
  "rotation": 0.0
}
```

**Response:**
```json
{
  "success": true,
  "building": {
    "id": 100,
    "building_type_id": 5,
    "world_x": 12345,
    "world_y": 67890,
    "rotation": 0.0,
    "construction_progress": 0.0,
    "actual_build_time": 180,
    "actual_cost_data": {
      "lumber": 90,
      "stone_blocks": 45
    },
    "durability": 1000,
    "max_durability": 1000,
    "next_maintenance_due_at": "2024-01-22T12:00:00Z"
  },
  "message": "Building placement initiated. Construction in progress."
}
```

**Status Codes:**
- `201 Created`: Building placed successfully
- `400 Bad Request`: Invalid input or insufficient resources
- `403 Forbidden`: Location not available or permission denied
- `401 Unauthorized`: Not authenticated

**Note:** This endpoint calculates skill bonuses and applies them to build time and costs.

#### GET /game/buildings/{id}

Get building details.

**Response:**
```json
{
  "id": 100,
  "building_type": {
    "id": 5,
    "name": "Sect Hall",
    "slug": "sect-hall",
    "footprint_polygon": {
      "vertices": [
        {"x": -2.5, "y": -2.5},
        {"x": 2.5, "y": -2.5},
        {"x": 2.5, "y": 2.5},
        {"x": -2.5, "y": 2.5}
      ]
    },
    "door_positions": [
      {"x": 0, "y": -2.5, "facing": 3.14159}
    ]
  },
  "world_x": 12345,
  "world_y": 67890,
  "rotation": 0.0,
  "health": 1000,
  "max_health": 1000,
  "durability": 950,
  "max_durability": 1000,
  "construction_progress": 1.0,
  "is_functional": true,
  "is_relocating": false,
  "current_tier": 2,
  "tier_upgrade_progress": 0.0,
  "current_tier_info": {
    "tier_level": 2,
    "name": "Gathering Hall",
    "housing_capacity": 20,
    "qi_output_description": "Low-Grade Crystals",
    "qi_output_rate": 15.0,
    "unlocks": ["dorms", "training", "gardens"]
  },
  "signature_addition": {
    "id": 2,
    "name": "Qi Conduit Array",
    "is_built": true,
    "construction_progress": 1.0,
    "benefits": {
      "qi_output_bonus": 5.0,
      "housing_bonus": 3
    }
  },
  "total_housing_capacity": 23,
  "total_qi_output_rate": 20.0,
  "last_maintenance_at": "2024-01-21T12:00:00Z",
  "next_maintenance_due_at": "2024-01-22T12:00:00Z",
  "maintenance_overdue": false,
  "workers": [
    {
      "npc_id": 50,
      "npc_name": "Cultivator Alpha",
      "skill_level": 5,
      "skill_level_when_assigned": 3,
      "assigned_at": "2024-01-20T10:00:00Z"
    }
  ],
  "passive_resources": [
    {
      "resource_type": "mana_crystal",
      "rate_per_day": 20.0,
      "accumulated": 15.5,
      "last_generated_at": "2024-01-21T06:00:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Building not found

#### POST /game/buildings/{id}/maintenance

Perform maintenance on a building.

**Request:**
```json
{}
```

**Response:**
```json
{
  "success": true,
  "building": {
    "id": 100,
    "durability": 1000,
    "last_maintenance_at": "2024-01-21T15:00:00Z",
    "next_maintenance_due_at": "2024-01-22T15:00:00Z",
    "maintenance_overdue": false,
    "durability_loss_accumulated": 0.0
  },
  "resources_deducted": {
    "lumber": 10,
    "stone_blocks": 5
  }
}
```

**Status Codes:**
- `200 OK`: Maintenance performed successfully
- `400 Bad Request`: Insufficient resources or maintenance not due
- `404 Not Found`: Building not found

#### POST /game/buildings/{id}/assign-worker

Assign a worker (NPC) to a building.

**Request:**
```json
{
  "npc_id": 50
}
```

**Response:**
```json
{
  "success": true,
  "building": {
    "id": 100,
    "workers_count": 1
  },
  "worker": {
    "npc_id": 50,
    "assigned_at": "2024-01-21T15:00:00Z",
    "skill_level": 3
  }
}
```

**Status Codes:**
- `200 OK`: Worker assigned successfully
- `400 Bad Request`: No available slots or NPC not available
- `404 Not Found`: Building or NPC not found

#### DELETE /game/buildings/{id}/workers/{npc_id}

Remove a worker from a building.

**Response:**
```json
{
  "success": true,
  "message": "Worker removed from building"
}
```

**Status Codes:**
- `200 OK`: Worker removed successfully
- `404 Not Found`: Building or worker assignment not found

#### POST /game/buildings/{id}/collect-resources

Collect accumulated passive resources from a building.

**Response:**
```json
{
  "success": true,
  "resources_collected": {
    "mana_crystal": 15.5,
    "food": 25.0
  },
  "building": {
    "id": 100,
    "passive_resources": [
      {
        "resource_type": "mana_crystal",
        "accumulated": 0.0
      }
    ]
  }
}
```

**Status Codes:**
- `200 OK`: Resources collected successfully
- `404 Not Found`: Building not found

#### POST /game/buildings/{id}/relocate

Relocate a building to a new location.

**Request:**
```json
{
  "target_x": 13000,
  "target_y": 68000,
  "rotation": 0.0
}
```

**Response:**
```json
{
  "success": true,
  "building": {
    "id": 100,
    "is_relocating": true,
    "relocation_progress": 0.0,
    "original_location_x": 12345,
    "original_location_y": 67890,
    "target_location_x": 13000,
    "target_location_y": 68000,
    "relocation_started_at": "2024-01-21T15:00:00Z"
  },
  "relocation_cost": {
    "lumber": 45,
    "stone_blocks": 22.5
  },
  "estimated_relocation_time": 54
}
```

**Status Codes:**
- `200 OK`: Relocation initiated
- `400 Bad Request`: Building not relocatable or insufficient resources
- `404 Not Found`: Building not found

#### POST /game/buildings/{id}/demolish

Demolish a building and receive resource refund.

**Response:**
```json
{
  "success": true,
  "resources_returned": {
    "lumber": 22.5,
    "stone_blocks": 11.25
  },
  "message": "Building demolished successfully"
}
```

**Status Codes:**
- `200 OK`: Building demolished successfully
- `404 Not Found`: Building not found

### Building Tier Upgrades

#### GET /game/buildings/{id}/tiers

Get all tiers and upgrade information for a building.

**Response:**
```json
{
  "building": {
    "id": 100,
    "current_tier": 2,
    "tier_upgrade_progress": 0.0
  },
  "tiers": [
    {
      "tier_level": 1,
      "name": "Founder's Shelter",
      "housing_capacity": 12,
      "qi_output_description": "Ambient absorption",
      "qi_output_rate": 5.0,
      "upgrade_cost_data": null,
      "upgrade_time": null,
      "unlocks": ["basic_housing", "fields"],
      "signature_addition": {
        "id": 1,
        "name": "Meditation Platform",
        "cost_data": {"lumber": 50, "stone_blocks": 25},
        "build_time": 120,
        "benefits": {
          "qi_output_bonus": 2.0,
          "unlocks": ["advanced_meditation"]
        }
      }
    },
    {
      "tier_level": 2,
      "name": "Gathering Hall",
      "housing_capacity": 20,
      "qi_output_description": "Low-Grade Crystals",
      "qi_output_rate": 15.0,
      "upgrade_cost_data": {"lumber": 200, "stone_blocks": 100, "qi_crystal": 50},
      "upgrade_time": 600,
      "unlocks": ["dorms", "training", "gardens"],
      "signature_addition": {
        "id": 2,
        "name": "Qi Conduit Array",
        "cost_data": {"lumber": 100, "stone_blocks": 50, "qi_crystal": 25},
        "build_time": 300,
        "benefits": {
          "qi_output_bonus": 5.0,
          "housing_bonus": 3
        }
      },
      "is_current_tier": true
    },
    {
      "tier_level": 3,
      "name": "Inner Hall",
      "housing_capacity": 35,
      "qi_output_description": "Mid-Grade Crystals",
      "qi_output_rate": 30.0,
      "upgrade_cost_data": {"lumber": 400, "stone_blocks": 200, "qi_crystal": 100},
      "upgrade_time": 1200,
      "unlocks": ["stone_houses", "terraces", "quarries"],
      "signature_addition": {
        "id": 3,
        "name": "Refinement Chamber",
        "cost_data": {"lumber": 200, "stone_blocks": 100, "qi_crystal": 50},
        "build_time": 600,
        "benefits": {
          "qi_output_bonus": 10.0,
          "unlocks": ["refinement"]
        }
      },
      "is_available": true
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Building not found

#### POST /game/buildings/{id}/upgrade-tier

Upgrade building to next tier.

**Request:**
```json
{
  "target_tier": 3
}
```

**Response:**
```json
{
  "success": true,
  "building": {
    "id": 100,
    "current_tier": 2,
    "tier_upgrade_progress": 0.0,
    "tier_upgrade_started_at": "2024-01-21T16:00:00Z"
  },
  "upgrade": {
    "target_tier": 3,
    "upgrade_cost_data": {
      "lumber": 400,
      "stone_blocks": 200,
      "qi_crystal": 100
    },
    "actual_upgrade_time": 1080,
    "estimated_completion": "2024-01-21T16:18:00Z"
  },
  "message": "Tier upgrade initiated. Building will be non-functional during upgrade."
}
```

**Status Codes:**
- `200 OK`: Upgrade initiated
- `400 Bad Request`: Invalid tier or insufficient resources
- `404 Not Found`: Building not found

**Note:** Upgrade time is calculated after skill bonuses. Building becomes non-functional during upgrade.

#### GET /game/buildings/{id}/signature-additions

Get signature addition information for building's current tier.

**Response:**
```json
{
  "current_tier": 2,
  "signature_addition": {
    "id": 2,
    "name": "Qi Conduit Array",
    "description": "An array of qi conduits that enhances qi flow",
    "cost_data": {
      "lumber": 100,
      "stone_blocks": 50,
      "qi_crystal": 25
    },
    "build_time": 300,
    "additional_footprint_polygon": {
      "vertices": [
        {"x": -1, "y": -1},
        {"x": 1, "y": -1},
        {"x": 1, "y": 1},
        {"x": -1, "y": 1}
      ]
    },
    "attachment_point": {
      "x": 0,
      "y": -2.5,
      "side": "north"
    },
    "benefits": {
      "qi_output_bonus": 5.0,
      "housing_bonus": 3,
      "unlocks": []
    },
    "is_built": false,
    "construction_progress": 0.0
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Building not found

#### POST /game/buildings/{id}/build-signature-addition

Build the signature addition for the building's current tier.

**Request:**
```json
{
  "rotation": 0.0
}
```

**Response:**
```json
{
  "success": true,
  "building": {
    "id": 100,
    "signature_addition_id": 2,
    "signature_addition_progress": 0.0,
    "signature_addition_started_at": "2024-01-21T16:00:00Z"
  },
  "construction": {
    "cost_data": {
      "lumber": 100,
      "stone_blocks": 50,
      "qi_crystal": 25
    },
    "actual_build_time": 270,
    "estimated_completion": "2024-01-21T16:04:30Z"
  },
  "message": "Signature addition construction initiated."
}
```

**Status Codes:**
- `200 OK`: Construction initiated
- `400 Bad Request`: Signature addition already built or insufficient resources
- `404 Not Found`: Building not found

**Note:** Building remains functional during signature addition construction. Benefits apply when construction completes.

### Districts & Supply Chains

#### GET /game/districts

Get all districts for a territory or area.

**Query Parameters:**
- `territory_id`: Filter by territory - optional
- `category`: Filter by category - optional
- `owner_id`: Filter by owner - optional
- `center_x`, `center_y`, `radius`: Get districts within radius of point - optional

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "category": "civic",
      "name": "Civic District",
      "center_x": 12345,
      "center_y": 67890,
      "radius": 75.5,
      "building_count": 5,
      "min_buildings_required": 3,
      "district_bonus_type": "efficiency",
      "district_bonus_value": 0.15,
      "is_active": true,
      "buildings": [
        {
          "id": 100,
          "building_type": "Sect Hall",
          "world_x": 12300,
          "world_y": 67850
        },
        {
          "id": 101,
          "building_type": "Archive",
          "world_x": 12350,
          "world_y": 67900
        }
      ]
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success

#### GET /game/districts/{id}

Get district details.

**Response:**
```json
{
  "id": 1,
  "owner_id": 10,
  "category": "civic",
  "name": "Civic District",
  "center_x": 12345,
  "center_y": 67890,
  "radius": 75.5,
  "boundary_polygon": {
    "vertices": [
      {"x": 12270, "y": 67815},
      {"x": 12420, "y": 67815},
      {"x": 12420, "y": 67965},
      {"x": 12270, "y": 67965}
    ]
  },
  "building_count": 5,
  "min_buildings_required": 3,
  "formation_threshold": 50.0,
  "district_bonus_type": "efficiency",
  "district_bonus_value": 0.15,
  "bonus_scales_with_buildings": true,
  "is_active": true,
  "formed_at": "2024-01-20T10:00:00Z",
  "buildings": [
    {
      "id": 100,
      "building_type": {
        "id": 5,
        "name": "Sect Hall",
        "category": "civic",
        "building_path": "sect_hall"
      },
      "world_x": 12300,
      "world_y": 67850,
      "district_bonus_applied": true
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: District not found

#### GET /game/buildings/{id}/supply-chain

Get supply chain information for a building.

**Response:**
```json
{
  "building": {
    "id": 100,
    "building_type": {
      "id": 5,
      "name": "Wood Mill",
      "supply_chain_id": 2
    }
  },
  "supply_chain": {
    "id": 2,
    "name": "Wood Processing",
    "description": "Processing chain for wood resources",
    "chain_type": "linear",
    "proximity_bonus_range": 50.0,
    "proximity_bonus_per_link": 0.05,
    "max_proximity_bonus": 0.25
  },
  "linked_buildings": [
    {
      "building_type": {
        "id": 3,
        "name": "Lumber Camp"
      },
      "link_type": "produces",
      "proximity_bonus": 0.1,
      "max_distance": 100.0
    },
    {
      "building_type": {
        "id": 7,
        "name": "Carpentry Workshop"
      },
      "link_type": "consumes",
      "proximity_bonus": 0.15,
      "max_distance": 100.0
    }
  ],
  "nearby_supply_chain_buildings": [
    {
      "building_id": 95,
      "building_type": "Lumber Camp",
      "distance": 35.5,
      "link_bonus_applied": 0.1
    },
    {
      "building_id": 102,
      "building_type": "Carpentry Workshop",
      "distance": 42.3,
      "link_bonus_applied": 0.15
    }
  ],
  "total_proximity_bonus": 0.25,
  "proximity_bonuses": {
    "supply_chain": 0.25,
    "district": 0.15
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Building not found

#### POST /game/districts/{id}/rename

Rename a district (owner only).

**Request:**
```json
{
  "name": "Grand Civic Center"
}
```

**Response:**
```json
{
  "success": true,
  "district": {
    "id": 1,
    "name": "Grand Civic Center",
    "updated_at": "2024-01-21T16:00:00Z"
  }
}
```

**Status Codes:**
- `200 OK`: District renamed
- `403 Forbidden`: Not district owner
- `404 Not Found`: District not found

### Territory Selection

#### GET /planets/{planet_id}/territories

Get available territories for a planet (for territory selection).

**Query Parameters:**
- `preference`: Filter by preference ('busy' or 'isolated') - optional
- `available_only`: Filter to available territories only (default: true)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Northern Plains",
      "description": "A fertile plain with access to rivers",
      "territory_type": "starting_tile",
      "terrain_type": "plains",
      "biome_type": "temperate",
      "qi_source_type": "qi_vein",
      "qi_source_potency": 1.0,
      "territory_preference": "busy",
      "nearby_player_count": 3,
      "difficulty": "normal",
      "starting_resources": {
        "lumber": 100,
        "stone_blocks": 50,
        "qi_crystal": 10
      },
      "available": true
    },
    {
      "id": 2,
      "name": "Mountain Valley",
      "description": "A secluded valley in the mountains",
      "territory_type": "starting_tile",
      "terrain_type": "mountain",
      "biome_type": "alpine",
      "qi_source_type": "qi_well",
      "qi_source_potency": 1.5,
      "territory_preference": "isolated",
      "nearby_player_count": 0,
      "discourage_new_players": false,
      "difficulty": "normal",
      "starting_resources": {
        "lumber": 50,
        "stone_blocks": 150,
        "qi_crystal": 15
      },
      "available": true
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Planet not found

**Permissions:**
- Authenticated users only (for territory selection)

#### POST /avatars/{avatar_id}/select-territory

Select a territory for an avatar (completes avatar setup).

**Request:**
```json
{
  "territory_id": 1,
  "preference": "busy"
}
```

**Response:**
```json
{
  "success": true,
  "avatar": {
    "id": 22222,
    "name": "MyNewCharacter",
    "planet_id": 1,
    "territory_id": 1,
    "status": "active",
    "world_x": 12345,
    "world_y": 67890
  },
  "territory": {
    "id": 1,
    "name": "Northern Plains",
    "territory_type": "player_claimed",
    "qi_source_type": "qi_vein",
    "qi_source_world_x": 12300,
    "qi_source_world_y": 67850,
    "claimed_at": "2024-01-21T15:00:00Z"
  },
  "starting_resources": {
        "lumber": 100,
    "stone_blocks": 50,
    "qi_crystal": 10
  },
  "message": "Territory selected. Avatar placed near qi source with starting resources."
}
```

**Status Codes:**
- `200 OK`: Territory selected, avatar activated
- `400 Bad Request`: Invalid input or territory not available
- `404 Not Found`: Avatar or territory not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user or territory preference mismatch

**Note:**
- This endpoint triggers:
  1. Detailed feature generation for the selected territory at 1-2km level
  2. Subdivision of the 1-2km territory into 1m gameplay tiles
  3. Assignment of all 1m tiles within the territory to the player
- Avatar status changes from 'pending' to 'active'
- Territory is marked as claimed (`territory_type = 'player_claimed'`, `subdivided = TRUE`) and linked to avatar

**Territory Structure:**
- Territories are 1-2km edge tiles
- Once claimed, territory is subdivided into 1m edge tiles for gameplay
- Player controls all 1m tiles within their claimed 1-2km territory

**Territory Preference Logic:**
- If `preference = "busy"`: System validates territory has nearby players or is marked for busy players
- If `preference = "isolated"`: System validates territory has no nearby players or is marked for isolated players
- System may offer territories near established isolated players (difficult experience) if map is busy

#### POST /avatars/{avatar_id}/purchase-territory

Purchase a new territory (adjacent or non-contiguous). Requires mana crystals and triggers beast tide defense.

**Request:**
```json
{
  "territory_id": 5,  // 1-2km territory to purchase
  "confirm_cost": true  // Client must confirm they understand the cost is non-refundable
}
```

**Response:**
```json
{
  "success": true,
  "territory": {
    "id": 5,
    "name": "Eastern Hills",
    "claim_status": "claimed",
    "loyalty": 50.0,
    "beast_tide_count": 5,
    "beast_tide_completed": 0,
    "next_beast_tide_at": "2024-01-15T11:00:00Z",
    "purchase_cost_mana_crystals": 115,
    "purchase_cost_territory_number": 2
  },
  "mana_crystals_deducted": 115,
  "message": "Territory purchased. Beast tide defense begins in 1 hour. You must successfully defend all beast tides to secure the territory."
}
```

**Status Codes:**
- `200 OK`: Territory purchase successful
- `400 Bad Request`: Invalid input, insufficient mana crystals, territory not available, or outside effective control distance
- `404 Not Found`: Avatar or territory not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `409 Conflict`: Territory is already claimed or contested

**Note:**
- Cost is calculated based on number of owned territories (1.15 ^ (owned_territories - 1) × 100)
- Distance and terrain modifiers apply for non-contiguous territories
- Cost is non-refundable even if territory is lost
- Beast tide defense phase begins immediately after purchase
- Territory must be successfully defended through all beast tides to become secured

#### GET /avatars/{avatar_id}/territories

Get all territories owned by an avatar.

**Query Parameters:**
- `status`: Filter by claim status ('claimed', 'secured', 'feral', 'contested') - optional
- `include_stats`: Include detailed stats (loyalty, beast tides, etc.) - default: false

**Response:**
```json
{
  "territories": [
    {
      "id": 1,
      "name": "Starting Territory",
      "claim_status": "secured",
      "loyalty": 85.0,
      "is_contiguous": true,
      "distance_from_nearest_owned_km": 0.0,
      "terrain_type": "plains",
      "qi_source_type": "qi_vein",
      "qi_source_potency": 1.0
    },
    {
      "id": 5,
      "name": "Eastern Hills",
      "claim_status": "claimed",
      "loyalty": 50.0,
      "beast_tide_count": 5,
      "beast_tide_completed": 2,
      "next_beast_tide_at": "2024-01-15T14:30:00Z",
      "is_contiguous": true,
      "distance_from_nearest_owned_km": 2.5
    }
  ],
  "total_territories": 2,
  "total_secured": 1,
  "total_claimed": 1
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar not found

#### GET /territories/{territory_id}

Get detailed information about a territory.

**Response:**
```json
{
  "id": 5,
  "name": "Eastern Hills",
  "planet_id": 1,
  "terrain_type": "mountain",
  "biome_type": "alpine",
  "qi_source_type": "qi_vein",
  "qi_source_potency": 1.2,
  "claimed_by_avatar_id": 22222,
  "claim_status": "claimed",
  "loyalty": 50.0,
  "last_faction_presence_at": "2024-01-15T10:00:00Z",
  "loyalty_decay_rate": 1.0,
  "beast_tide_count": 5,
  "beast_tide_completed": 2,
  "beast_tide_failures": 0,
  "beast_tide_continuous": false,
  "next_beast_tide_at": "2024-01-15T14:30:00Z",
  "contested_by_avatar_ids": [],
  "controlling_avatar_id": null,
  "purchase_cost_mana_crystals": 115,
  "distance_from_nearest_owned_km": 2.5,
  "is_contiguous": true,
  "min_x": 1000,
  "min_y": 2000,
  "max_x": 3000,
  "max_y": 4000
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory not found

### Territory Management

#### GET /territories/{territory_id}/beast-tides

Get beast tide status and upcoming tides for a territory.

**Response:**
```json
{
  "territory_id": 5,
  "beast_tide_count": 5,
  "beast_tide_completed": 2,
  "beast_tide_failures": 0,
  "beast_tide_continuous": false,
  "next_beast_tide_at": "2024-01-15T14:30:00Z",
  "upcoming_tides": [
    {
      "tide_number": 3,
      "scheduled_at": "2024-01-15T14:30:00Z",
      "estimated_groups": 5,
      "tide_type": "medium"
    },
    {
      "tide_number": 4,
      "scheduled_at": "2024-01-15T17:00:00Z",
      "estimated_groups": 6,
      "tide_type": "medium"
    }
  ],
  "completed_tides": [
    {
      "tide_number": 1,
      "completed_at": "2024-01-15T10:00:00Z",
      "beast_groups_spawned": 4,
      "beast_groups_defeated": 4,
      "buildings_damaged": 0,
      "defense_successful": true
    },
    {
      "tide_number": 2,
      "completed_at": "2024-01-15T12:30:00Z",
      "beast_groups_spawned": 5,
      "beast_groups_defeated": 5,
      "buildings_damaged": 1,
      "defense_successful": true
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory not found
- `403 Forbidden`: Territory doesn't belong to user's avatar

#### GET /territories/{territory_id}/beast-tides/{tide_id}

Get detailed information about a specific beast tide.

**Response:**
```json
{
  "tide_id": 123,
  "territory_id": 5,
  "tide_number": 3,
  "status": "scheduled",
  "scheduled_at": "2024-01-15T14:30:00Z",
  "started_at": null,
  "completed_at": null,
  "beast_groups_spawned": null,
  "beast_groups_defeated": null,
  "beast_group_details": null,
  "buildings_damaged": null,
  "defense_successful": null
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory or tide not found

#### POST /territories/{territory_id}/beast-tides/{tide_id}/defend

Report the outcome of a beast tide defense (called by game server after tide completion).

**Request:**
```json
{
  "beast_groups_defeated": 5,
  "buildings_damaged": 0,
  "defense_successful": true
}
```

**Response:**
```json
{
  "success": true,
  "tide": {
    "tide_id": 123,
    "status": "completed",
    "defense_successful": true,
    "completed_at": "2024-01-15T15:00:00Z"
  },
  "territory": {
    "loyalty": 60.0,
    "beast_tide_completed": 3,
    "beast_tide_failures": 0
  },
  "message": "Beast tide successfully defended. Territory loyalty increased."
}
```

**Status Codes:**
- `200 OK`: Defense outcome recorded
- `400 Bad Request`: Invalid input
- `404 Not Found`: Territory or tide not found
- `409 Conflict`: Tide already completed

**Note:** This endpoint is primarily called by the game server. Client may call it to report defense outcomes if needed.

#### GET /territories/{territory_id}/patrols

Get all patrols for a territory.

**Query Parameters:**
- `status`: Filter by patrol status ('active', 'paused', 'completed', 'interrupted') - optional

**Response:**
```json
{
  "territory_id": 5,
  "patrols": [
    {
      "id": 10,
      "patrol_route": [
        {"x": 1500, "y": 2500},
        {"x": 2000, "y": 2500},
        {"x": 2000, "y": 3000},
        {"x": 1500, "y": 3000}
      ],
      "assigned_unit_type": "npc",
      "assigned_unit_id": 100,
      "assigned_unit_name": "Guard NPC",
      "patrol_status": "active",
      "last_patrol_at": "2024-01-15T12:00:00Z",
      "incursions_encountered": 3,
      "incursions_defeated": 3
    }
  ],
  "total_patrols": 1,
  "active_patrols": 1
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory not found
- `403 Forbidden`: Territory doesn't belong to user's avatar

#### POST /territories/{territory_id}/patrols

Create a new patrol route for a territory.

**Request:**
```json
{
  "patrol_route": [
    {"x": 1500, "y": 2500},
    {"x": 2000, "y": 2500},
    {"x": 2000, "y": 3000},
    {"x": 1500, "y": 3000}
  ],
  "assigned_unit_type": "npc",
  "assigned_unit_id": 100
}
```

**Response:**
```json
{
  "success": true,
  "patrol": {
    "id": 11,
    "territory_id": 5,
    "patrol_route": [
      {"x": 1500, "y": 2500},
      {"x": 2000, "y": 2500},
      {"x": 2000, "y": 3000},
      {"x": 1500, "y": 3000}
    ],
    "assigned_unit_type": "npc",
    "assigned_unit_id": 100,
    "patrol_status": "active",
    "created_at": "2024-01-15T13:00:00Z"
  }
}
```

**Status Codes:**
- `201 Created`: Patrol created successfully
- `400 Bad Request`: Invalid route (too few waypoints, invalid coordinates, etc.)
- `404 Not Found`: Territory or unit not found
- `403 Forbidden`: Territory or unit doesn't belong to user's avatar
- `409 Conflict`: Unit already assigned to another patrol

#### PUT /territories/{territory_id}/patrols/{patrol_id}

Update a patrol route.

**Request:**
```json
{
  "patrol_route": [
    {"x": 1600, "y": 2600},
    {"x": 2100, "y": 2600},
    {"x": 2100, "y": 3100},
    {"x": 1600, "y": 3100}
  ],
  "patrol_status": "paused"
}
```

**Response:**
```json
{
  "success": true,
  "patrol": {
    "id": 11,
    "patrol_route": [
      {"x": 1600, "y": 2600},
      {"x": 2100, "y": 2600},
      {"x": 2100, "y": 3100},
      {"x": 1600, "y": 3100}
    ],
    "patrol_status": "paused",
    "updated_at": "2024-01-15T13:30:00Z"
  }
}
```

**Status Codes:**
- `200 OK`: Patrol updated successfully
- `400 Bad Request`: Invalid input
- `404 Not Found`: Territory or patrol not found
- `403 Forbidden`: Territory doesn't belong to user's avatar

#### DELETE /territories/{territory_id}/patrols/{patrol_id}

Delete a patrol route.

**Response:**
```json
{
  "success": true,
  "message": "Patrol deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Patrol deleted successfully
- `404 Not Found`: Territory or patrol not found
- `403 Forbidden`: Territory doesn't belong to user's avatar

#### POST /territories/{territory_id}/patrols/{patrol_id}/assign-unit

Assign or reassign a unit to a patrol.

**Request:**
```json
{
  "assigned_unit_type": "npc",
  "assigned_unit_id": 101
}
```

**Response:**
```json
{
  "success": true,
  "patrol": {
    "id": 11,
    "assigned_unit_type": "npc",
    "assigned_unit_id": 101,
    "assigned_unit_name": "Guard NPC 2",
    "updated_at": "2024-01-15T14:00:00Z"
  }
}
```

**Status Codes:**
- `200 OK`: Unit assigned successfully
- `400 Bad Request`: Invalid unit type or ID
- `404 Not Found`: Territory, patrol, or unit not found
- `403 Forbidden`: Territory or unit doesn't belong to user's avatar
- `409 Conflict`: Unit already assigned to another patrol

#### GET /territories/{territory_id}/incursions

Get beast incursions for a territory.

**Query Parameters:**
- `status`: Filter by status ('active', 'defeated', 'entered_territory', 'expired') - optional
- `incursion_type`: Filter by type ('tide', 'regular', 'large') - optional
- `limit`: Number of results (default: 50, max: 100)

**Response:**
```json
{
  "territory_id": 5,
  "incursions": [
    {
      "id": 50,
      "incursion_type": "regular",
      "spawn_x": 1800,
      "spawn_y": 2800,
      "beast_group_count": 3,
      "beast_group_data": [
        {"type": "wolf", "count": 5, "level": 3},
        {"type": "bear", "count": 2, "level": 4},
        {"type": "eagle", "count": 3, "level": 2}
      ],
      "status": "defeated",
      "detected_by_patrol_id": 10,
      "defeated_at": "2024-01-15T12:15:00Z",
      "created_at": "2024-01-15T12:10:00Z"
    }
  ],
  "total_incursions": 15,
  "active_incursions": 0,
  "defeated_incursions": 12,
  "entered_territory_incursions": 3
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory not found
- `403 Forbidden`: Territory doesn't belong to user's avatar

#### GET /territories/{territory_id}/incursions/{incursion_id}

Get detailed information about a specific beast incursion.

**Response:**
```json
{
  "id": 50,
  "territory_id": 5,
  "incursion_type": "regular",
  "spawn_x": 1800,
  "spawn_y": 2800,
  "beast_group_count": 3,
  "beast_group_data": [
    {"type": "wolf", "count": 5, "level": 3, "health": 100},
    {"type": "bear", "count": 2, "level": 4, "health": 200},
    {"type": "eagle", "count": 3, "level": 2, "health": 80}
  ],
  "status": "defeated",
  "detected_by_patrol_id": 10,
  "defeated_at": "2024-01-15T12:15:00Z",
  "entered_territory_at": null,
  "created_at": "2024-01-15T12:10:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory or incursion not found

#### GET /territories/{territory_id}/contest

Get contest status for a contested territory.

**Response:**
```json
{
  "territory_id": 5,
  "claim_status": "contested",
  "contested_by_avatar_ids": [22222, 33333],
  "contested_since": "2024-01-15T10:00:00Z",
  "controlling_avatar_id": 22222,
  "control_started_at": "2024-01-15T11:30:00Z",
  "control_duration_hours": 1.5,
  "beast_tide_continuous": true,
  "beast_tide_continuous_until": null,
  "contests": [
    {
      "id": 1,
      "contesting_avatar_id": 22222,
      "contest_started_at": "2024-01-15T10:00:00Z",
      "contest_status": "active",
      "control_duration_hours": 1.5
    },
    {
      "id": 2,
      "contesting_avatar_id": 33333,
      "contest_started_at": "2024-01-15T10:05:00Z",
      "contest_status": "active",
      "control_duration_hours": 0.0
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory not found
- `409 Conflict`: Territory is not contested

#### POST /territories/{territory_id}/contest/claim

Claim a contested territory (join the contest).

**Request:**
```json
{
  "confirm_danger": true  // Must confirm understanding of continuous beast tide
}
```

**Response:**
```json
{
  "success": true,
  "territory": {
    "claim_status": "contested",
    "contested_by_avatar_ids": [22222, 33333, 44444],
    "beast_tide_continuous": true
  },
  "message": "Territory contestation joined. Continuous beast tide is active."
}
```

**Status Codes:**
- `200 OK`: Contestation joined successfully
- `400 Bad Request`: Invalid input or territory not available for contestation
- `404 Not Found`: Territory not found
- `403 Forbidden`: Cannot claim own territory
- `409 Conflict`: Already contesting this territory

#### GET /territories/{territory_id}/contest/control

Get current control status for a contested territory.

**Response:**
```json
{
  "territory_id": 5,
  "controlling_avatar_id": 22222,
  "control_started_at": "2024-01-15T11:30:00Z",
  "control_duration_hours": 1.5,
  "hours_required_for_securing": 6.0,
  "hours_remaining": 4.5,
  "opposing_units_present": false,
  "opposing_buildings_present": false,
  "can_secure": false
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory not found
- `409 Conflict`: Territory is not contested

#### GET /territories/{territory_id}/loyalty

Get territory loyalty status and decay information.

**Response:**
```json
{
  "territory_id": 5,
  "loyalty": 75.0,
  "last_faction_presence_at": "2024-01-15T13:00:00Z",
  "loyalty_decay_rate": 1.0,
  "hours_since_presence": 0.5,
  "loyalty_state": "secure",
  "estimated_time_to_feral": null,
  "estimated_time_to_lost": null,
  "faction_characters_present": [
    {
      "unit_type": "avatar",
      "unit_id": 22222,
      "name": "Player Avatar"
    },
    {
      "unit_type": "npc",
      "unit_id": 100,
      "name": "Guard NPC"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory not found
- `403 Forbidden`: Territory doesn't belong to user's avatar

#### GET /territories/{territory_id}/presence

Check faction character presence in a territory.

**Response:**
```json
{
  "territory_id": 5,
  "has_faction_presence": true,
  "last_faction_presence_at": "2024-01-15T13:00:00Z",
  "presence_check_interval_minutes": 5,
  "faction_characters": [
    {
      "unit_type": "avatar",
      "unit_id": 22222,
      "name": "Player Avatar",
      "world_x": 2000,
      "world_y": 3000,
      "distance_from_territory_center": 500
    },
    {
      "unit_type": "npc",
      "unit_id": 100,
      "name": "Guard NPC",
      "world_x": 1800,
      "world_y": 2800,
      "distance_from_territory_center": 300
    }
  ],
  "total_faction_characters": 2
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Territory not found

### NPC Management

#### GET /game/npcs

List NPCs with optional filters.

**Query Parameters:**
- `owner_id`: Filter by avatar owner - optional
- `state`: Filter by NPC state ('idle', 'working', 'moving', 'fighting', 'resting', 'socializing', 'eating', 'training', 'patrolling', 'seeking') - optional
- `npc_type_id`: Filter by NPC type - optional
- `territory_id`: Filter by territory - optional
- `mortal_class`: Filter by mortal class ('mortal', 'cultivator') - optional
- `in_combat`: Filter by combat status (true/false) - optional
- `limit`: Number of results (default: 50, max: 100) - optional
- `offset`: Pagination offset - optional

**Response:**
```json
{
  "npcs": [
    {
      "id": 100,
      "name": "Worker NPC",
      "npc_type": "worker",
      "owner_id": 22222,
      "state": "working",
      "world_x": 2000,
      "world_y": 3000,
      "health": 100,
      "max_health": 100,
      "stamina_pool": 75.0,
      "stamina_capacity": 100.0,
      "mortal_class": "mortal",
      "current_job_id": 50,
      "current_job_building_id": 100,
      "in_combat": false,
      "cultivation_level": 0
    }
  ],
  "pagination": {
    "total": 45,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### GET /game/npcs/{npc_id}

Get detailed information about an NPC.

**Response:**
```json
{
  "id": 100,
  "name": "Worker NPC",
  "npc_type_id": 1,
  "npc_type": "worker",
  "ethnicity_id": 5,
  "ethnicity": "Bison Faun",
  "owner_id": 22222,
  "world_x": 2000,
  "world_y": 3000,
  "facing_angle": 45.0,
  "health": 100,
  "max_health": 100,
  "stamina_pool": 75.0,
  "stamina_capacity": 100.0,
  "state": "working",
  "mortal_class": "mortal",
  "body": 12,
  "mind": 10,
  "spirit": 8,
  "qi_pool": 0.0,
  "qi_capacity": 0.0,
  "cultivation_level": 0,
  "skills": {
    "construction": 5,
    "mining": 3
  },
  "personality_traits": {
    "friendly": 0.7,
    "cautious": 0.4,
    "ambitious": 0.6
  },
  "ego_score": 15,
  "current_job_id": 50,
  "current_job": {
    "id": 50,
    "building_id": 100,
    "building_name": "Sect Hall",
    "job_type": "construction",
    "status": "in_progress"
  },
  "in_combat": false,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-21T15:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: NPC not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: NPC doesn't belong to user's avatar

#### GET /game/npcs/{npc_id}/state

Get NPC current state and status information.

**Response:**
```json
{
  "npc_id": 100,
  "state": "working",
  "state_description": "NPC is actively performing job duties at assigned building",
  "current_job_id": 50,
  "current_location": {
    "world_x": 2000,
    "world_y": 3000,
    "building_id": 100,
    "building_name": "Sect Hall"
  },
  "health_status": {
    "health": 100,
    "max_health": 100,
    "health_percentage": 100.0
  },
  "stamina_status": {
    "stamina_pool": 75.0,
    "stamina_capacity": 100.0,
    "stamina_percentage": 75.0
  },
  "in_combat": false,
  "last_state_change_at": "2024-01-21T09:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: NPC not found
- `401 Unauthorized`: Not authenticated

#### GET /game/npcs/{npc_id}/needs

Get NPC current needs (calculated dynamically).

**Response:**
```json
{
  "npc_id": 100,
  "needs": {
    "hunger": {
      "current": 65.0,
      "threshold": 40.0,
      "critical_threshold": 20.0,
      "urgency": 0.0,
      "status": "satisfied"
    },
    "rest": {
      "current": 75.0,
      "threshold": 30.0,
      "critical_threshold": 20.0,
      "urgency": 0.0,
      "status": "satisfied"
    },
    "social": {
      "current": 45.0,
      "threshold": 40.0,
      "critical_threshold": 30.0,
      "urgency": 0.125,
      "status": "low"
    },
    "safety": {
      "current": 85.0,
      "threshold": 40.0,
      "critical_threshold": 30.0,
      "urgency": 0.0,
      "status": "secure"
    },
    "work_satisfaction": {
      "current": 72.0,
      "threshold": 40.0,
      "critical_threshold": 30.0,
      "urgency": 0.0,
      "status": "good"
    },
    "autonomy": {
      "current": 90.0,
      "threshold": 30.0,
      "critical_threshold": 20.0,
      "urgency": 0.0,
      "status": "high"
    }
  },
  "priority_need": "social",
  "calculated_at": "2024-01-21T15:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: NPC not found
- `401 Unauthorized`: Not authenticated

**Note:** Needs are calculated dynamically based on current state, events, relationships, and territory conditions. Values are not stored in the database.

#### GET /game/npcs/{npc_id}/job

Get current job information for an NPC.

**Response:**
```json
{
  "npc_id": 100,
  "current_job": {
    "id": 50,
    "job_type": "construction",
    "building_id": 100,
    "building_name": "Sect Hall",
    "building_type": "sect_hall",
    "status": "in_progress",
    "assigned_at": "2024-01-20T09:00:00Z",
    "started_at": "2024-01-20T09:05:00Z",
    "job_satisfaction": 72.0,
    "required_skills": {
      "construction": 3
    },
    "npc_skill_levels": {
      "construction": 5
    },
    "coworkers": [
      {
        "npc_id": 101,
        "name": "Coworker NPC",
        "relationship_value": 45.0
      }
    ]
  },
  "has_job": true
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: NPC not found
- `401 Unauthorized`: Not authenticated

#### PUT /game/npcs/{npc_id}/job

Assign or reassign an NPC to a job.

**Request:**
```json
{
  "building_id": 100,
  "force_assignment": false  // If true, overrides NPC's job preferences
}
```

**Response:**
```json
{
  "success": true,
  "npc_id": 100,
  "job": {
    "id": 51,
    "building_id": 100,
    "building_name": "Sect Hall",
    "job_type": "construction",
    "assigned_at": "2024-01-21T15:30:00Z",
    "status": "assigned"
  },
  "message": "NPC assigned to job successfully"
}
```

**Status Codes:**
- `200 OK`: Job assigned successfully
- `400 Bad Request`: Building doesn't need workers, NPC not available, or insufficient slots
- `404 Not Found`: NPC or building not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: NPC or building doesn't belong to user's avatar
- `409 Conflict`: NPC already assigned to this building or cannot accept assignment (low autonomy, high ego)

**Note:** High ego or cultivator NPCs may reject assignments if autonomy is low. Use `force_assignment` carefully.

#### DELETE /game/npcs/{npc_id}/job

Remove NPC from current job.

**Response:**
```json
{
  "success": true,
  "npc_id": 100,
  "message": "NPC removed from job successfully"
}
```

**Status Codes:**
- `200 OK`: Job removed successfully
- `404 Not Found`: NPC not found or not assigned to a job
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: NPC doesn't belong to user's avatar

### NPC Relationships and Events

#### GET /game/npcs/{npc_id}/relationships

Get all relationships for an NPC (Game Server API).

**Query Parameters:**
- `target_type`: Filter by target type ('npc', 'building') - optional
- `relationship_type`: Filter by relationship type - optional
- `min_value`: Minimum relationship value - optional
- `max_value`: Maximum relationship value - optional

**Response:**
```json
{
  "npc": {
    "id": 100,
    "name": "Worker NPC",
    "personality_traits": {
      "friendly": 0.7,
      "cautious": 0.4,
      "ambitious": 0.6
    }
  },
  "relationships": [
    {
      "id": 1,
      "target_type": "npc",
      "target_id": 101,
      "target_name": "Friend NPC",
      "relationship_type": "friend",
      "relationship_value": 65.5,
      "trust_level": 0.8,
      "familiarity": 0.9,
      "first_interaction_at": "2024-01-10T10:00:00Z",
      "last_interaction_at": "2024-01-20T15:30:00Z",
      "interaction_count": 45,
      "notes": "Work colleagues who became close friends"
    },
    {
      "id": 2,
      "target_type": "building",
      "target_id": 50,
      "target_name": "Sect Hall",
      "relationship_type": "employee",
      "relationship_value": 40.0,
      "trust_level": 0.6,
      "familiarity": 0.7,
      "first_interaction_at": "2024-01-05T08:00:00Z",
      "last_interaction_at": "2024-01-21T09:00:00Z",
      "interaction_count": 120,
      "notes": "Works here daily"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: NPC not found
- `401 Unauthorized`: Not authenticated

#### GET /game/npcs/{npc_id}/events

Get event journal for an NPC (Game Server API).

**Query Parameters:**
- `event_type`: Filter by event type - optional
- `severity`: Filter by severity - optional
- `min_importance`: Minimum importance (0.0-1.0) - optional
- `since`: Events since timestamp - optional
- `limit`: Number of results (default: 50, max: 200) - optional
- `offset`: Pagination offset - optional

**Response:**
```json
{
  "npc": {
    "id": 100,
    "name": "Worker NPC"
  },
  "events": [
    {
      "id": 500,
      "event_type": "achievement",
      "severity": "major",
      "title": "Promoted to Master Craftsman",
      "description": "After years of dedicated work, NPC was promoted to Master Craftsman at the Sect Hall.",
      "location_type": "building",
      "location_id": 50,
      "related_npc_ids": [101, 102],
      "related_building_id": 50,
      "relationship_impacts": {
        "101": {"change": 10.0, "reason": "Celebrated promotion together"},
        "102": {"change": -5.0, "reason": "Competed for same promotion"}
      },
      "personality_impact": {
        "ambitious": 0.05,
        "confident": 0.03
      },
      "is_random_event": false,
      "triggered_by": "work",
      "importance": 0.8,
      "occurred_at": "2024-01-20T14:00:00Z"
    }
  ],
  "pagination": {
    "total": 156,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: NPC not found
- `401 Unauthorized`: Not authenticated

#### POST /admin/npcs/{npc_id}/events

Create a manual event for an NPC (Admin/StoryTeller only).

**Request:**
```json
{
  "event_type": "social",
  "severity": "significant",
  "title": "Participated in Festival",
  "description": "NPC attended the Spring Festival.",
  "location_type": "building",
  "location_id": 50,
  "related_npc_ids": [101, 102],
  "relationship_impacts": {
    "101": {"change": 5.0, "reason": "Shared experience"}
  },
  "personality_impact": {
    "friendly": 0.02
  },
  "importance": 0.6
}
```

**Response:**
```json
{
  "success": true,
  "event": {
    "id": 502,
    "npc_id": 100,
    "title": "Participated in Festival",
    "occurred_at": "2024-01-21T18:00:00Z"
  },
  "relationships_updated": 2,
  "personality_updated": true
}
```

**Status Codes:**
- `201 Created`: Event created, relationships updated
- `400 Bad Request`: Invalid input
- `404 Not Found`: NPC not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller

#### GET /avatars/{avatar_id}/territory-tiles

Get all 1m gameplay tiles owned by an avatar's territory.

**Query Parameters:**
- `territory_id`: Filter by specific 1-2km territory (optional)
- `limit`: Number of results (default: 1000, max: 10000)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": 12345,
      "territory_id": 1,
      "tile_x": 10,
      "tile_y": 20,
      "world_x": 123450,
      "world_y": 678900,
      "elevation": 125.5,
      "terrain_feature": "plains",
      "resource_nodes": {
        "lumber": 5
      },
      "owned_percentage": 1.0
    }
  ],
  "pagination": {
    "total": 5000,
    "limit": 1000,
    "offset": 0,
    "has_more": true
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Avatar not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user

**Permissions:**
- Users can only view tiles for their own avatars

### Cultivation Actions

#### GET /avatars/{avatar_id}/cultivation

Get cultivation details for an avatar.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "avatar_id": 11111,
  "cultivation_level": 3,
  "cultivation_experience": 0.65,
  "qi_pool": 240.0,
  "qi_capacity": 320.0,
  "qi_required_for_next_tier": 640.0,
  "primary_attunement": "Fire",
  "cultivation_concept": "The Phoenix's Rebirth - Strength through destruction and renewal",
  "last_tribulation_at": "2024-01-10T14:30:00Z",
  "tribulation_count": 2,
  "tribulation_failures": 0,
  "next_tier": 4,
  "next_tier_name": "Qi Novice",
  "next_tribulation_type": "Internal Refinement",
  "can_attempt_breakthrough": false,
  "breakthrough_requirements": {
    "qi_capacity_met": false,
    "qi_required": 640.0,
    "current_capacity": 320.0,
    "cultivation_experience_met": true
  },
  "tier_info": {
    "tier": 3,
    "name": "Spiritual Awakening",
    "grouping": "Mortal Foundation (Tiers 1-4)",
    "abilities": [
      "Perceives ley-lines and Qi nodes",
      "Senses and communicates with spirits"
    ]
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar not found

#### POST /avatars/{avatar_id}/cultivation/attempt-breakthrough

Attempt to breakthrough to the next cultivation tier. This triggers Qi compression and may trigger a tribulation.

**Request:**
```json
{
  "confirm": true
}
```

**Response (Success - No Tribulation):**
```json
{
  "success": true,
  "message": "Breakthrough successful. Tier increased without tribulation.",
  "avatar": {
    "cultivation_level": 4,
    "cultivation_experience": 0.0,
    "qi_capacity": 640.0,
    "qi_pool": 240.0
  }
}
```

**Response (Success - Tribulation Triggered):**
```json
{
  "success": true,
  "message": "Breakthrough initiated. Tribulation triggered.",
  "tribulation": {
    "id": 12345,
    "tier": 4,
    "type": "Internal Refinement",
    "theme": "Test of Willpower & Endurance",
    "status": "active",
    "started_at": "2024-01-15T10:30:00Z",
    "estimated_duration": "2-4 hours",
    "challenges": [
      "Sensory deprivation",
      "Hallucinations",
      "Qi poisoning resistance"
    ]
  },
  "avatar": {
    "cultivation_level": 4,
    "cultivation_experience": 0.0,
    "qi_capacity": 640.0,
    "qi_pool": 240.0
  }
}
```

**Response (Failure - Requirements Not Met):**
```json
{
  "success": false,
  "error": {
    "code": "BREAKTHROUGH_REQUIREMENTS_NOT_MET",
    "message": "Cannot attempt breakthrough. Qi capacity must be doubled.",
    "requirements": {
      "qi_capacity_met": false,
      "qi_required": 640.0,
      "current_capacity": 320.0
    }
  }
}
```

**Status Codes:**
- `200 OK`: Breakthrough attempted (may trigger tribulation)
- `400 Bad Request`: Requirements not met or invalid request
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar not found

**Note:**
- Breakthrough requires `qi_capacity` to be doubled from previous tier
- Breakthrough may trigger a tribulation based on tier range
- Tribulations are personalized tests of mind, body, and spirit
- Failure consequences vary by tribulation severity

#### GET /avatars/{avatar_id}/cultivation/tribulation/{tribulation_id}

Get details of an active tribulation.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "tribulation": {
    "id": 12345,
    "avatar_id": 11111,
    "tier": 4,
    "type": "Internal Refinement",
    "theme": "Test of Willpower & Endurance",
    "status": "active",
    "started_at": "2024-01-15T10:30:00Z",
    "completed_at": null,
    "estimated_duration": "2-4 hours",
    "challenges": [
      "Sensory deprivation",
      "Hallucinations",
      "Qi poisoning resistance"
    ],
    "principles": {
      "balance": "Greater power demands equivalent price",
      "karma": "Past actions shape challenges",
      "attunement": "Reflects primary Qi attunement"
    },
    "failure_consequences": [
      "Weakened Qi Sensitivity",
      "Core Instability",
      "Shattered Meridians",
      "Cultivation Deviation",
      "Death"
    ]
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar or tribulation not found

#### POST /admin/avatars/{avatar_id}/cultivation/trigger-tribulation

Manually trigger a tribulation for an avatar (Admin/StoryTeller only).

**Request:**
```json
{
  "tier": 5,
  "type": "Elemental Trial",
  "reason": "Story event - testing character's resolve"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tribulation triggered successfully",
  "tribulation": {
    "id": 12346,
    "avatar_id": 11111,
    "tier": 5,
    "type": "Elemental Trial",
    "theme": "Faces own Qi as force of nature",
    "status": "active",
    "started_at": "2024-01-15T11:00:00Z"
  }
}
```

**Status Codes:**
- `200 OK`: Tribulation triggered
- `400 Bad Request`: Invalid input or avatar not ready
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not Admin or StoryTeller
- `404 Not Found`: Avatar not found

**Permissions:**
- Admins and StoryTellers only

#### GET /game/npcs/{npc_id}/cultivation

Get cultivation details for an NPC.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "npc_id": 100,
  "cultivation_level": 2,
  "cultivation_experience": 0.35,
  "qi_pool": 120.0,
  "qi_capacity": 160.0,
  "qi_required_for_next_tier": 320.0,
  "primary_attunement": "Water",
  "cultivation_concept": null,
  "last_tribulation_at": null,
  "tribulation_count": 0,
  "tribulation_failures": 0,
  "next_tier": 3,
  "next_tier_name": "Spiritual Awakening",
  "can_attempt_breakthrough": false,
  "tier_info": {
    "tier": 2,
    "name": "Qi Channeler",
    "grouping": "Mortal Foundation (Tiers 1-4)"
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: NPC not found

**Note:** NPCs may attempt breakthroughs automatically based on AI behavior, or manually via admin/storyteller actions.

### Combat & Equipment

#### GET /avatars/{avatar_id}/techniques

Get all techniques learned by an avatar.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "techniques": [
    {
      "id": 1,
      "technique_id": 5,
      "name": "Power Strike",
      "category": "physical",
      "tier": "basic",
      "mastery_level": 3,
      "experience": 125.5,
      "learned_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar not found

#### GET /game/npcs/{npc_id}/techniques

Get all techniques learned by an NPC.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "techniques": [
    {
      "id": 2,
      "technique_id": 8,
      "name": "Qi Blast",
      "category": "qi",
      "tier": "intermediate",
      "mastery_level": 5,
      "experience": 450.0,
      "learned_at": "2024-01-05T14:30:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: NPC not found

#### GET /avatars/{avatar_id}/equipment

Get equipped equipment for an avatar.

**Request:** (Headers: Authorization)

**Response:**
```json
{
  "weapon": {
    "id": 10,
    "name": "Iron Sword",
    "weapon_type": "sword",
    "quality_tier": "standard",
    "attack_bonus": 12,
    "damage_multiplier": 1.0
  },
  "armor": {
    "id": 5,
    "name": "Leather Armor",
    "armor_type": "light",
    "defense_bonus": 8,
    "speed_penalty": 0.0
  },
  "accessories": [
    {
      "id": 3,
      "name": "Strength Ring",
      "accessory_type": "ring",
      "stat_bonuses": {"strength": 2}
    }
  ],
  "qi_focus": null
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar not found

#### PUT /avatars/{avatar_id}/equipment

Equip or unequip items for an avatar.

**Request:**
```json
{
  "weapon_id": 10,
  "armor_id": 5,
  "accessory_1_id": 3,
  "accessory_2_id": null,
  "qi_focus_id": null
}
```

**Response:**
```json
{
  "success": true,
  "equipment": {
    "weapon_id": 10,
    "armor_id": 5,
    "accessory_1_id": 3,
    "accessory_2_id": null,
    "qi_focus_id": null
  }
}
```

**Status Codes:**
- `200 OK`: Equipment updated successfully
- `400 Bad Request`: Invalid equipment IDs or unit cannot equip item
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user
- `404 Not Found`: Avatar or equipment not found

#### GET /game/techniques

Get list of available techniques (for learning/selection).

**Query Parameters:**
- `category`: Filter by category ('physical', 'qi', 'hybrid') - optional
- `tier`: Filter by tier ('basic', 'intermediate', 'advanced', 'master') - optional
- `requires_cultivation_tier`: Filter by minimum cultivation tier - optional
- `required_skill_id`: Filter by required skill - optional

**Response:**
```json
{
  "data": [
    {
      "id": 5,
      "name": "Power Strike",
      "slug": "power-strike",
      "description": "A powerful physical strike that deals increased damage",
      "category": "physical",
      "tier": "basic",
      "cost_type": "stamina",
      "cost_amount": 20,
      "damage_multiplier": 1.5,
      "range_type": "melee",
      "range_distance": 2,
      "cooldown_seconds": 3,
      "requires_cultivation_tier": 0,
      "required_skill_id": 1,
      "required_skill_level": 1
    }
  ],
  "pagination": {
    "total": 50,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### GET /game/weapons

Get list of available weapons.

**Query Parameters:**
- `weapon_type`: Filter by weapon type - optional
- `quality_tier`: Filter by quality tier - optional
- `qi_enhanceable`: Filter by Qi enhanceable status - optional

**Response:**
```json
{
  "data": [
    {
      "id": 10,
      "name": "Iron Sword",
      "weapon_type": "sword",
      "quality_tier": "standard",
      "attack_bonus": 12,
      "damage_multiplier": 1.0,
      "speed_modifier": 1.0,
      "range_meters": 2,
      "critical_chance_bonus": 0.0,
      "qi_enhanceable": true
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### GET /game/armor

Get list of available armor.

**Query Parameters:**
- `armor_type`: Filter by armor type ('light', 'medium', 'heavy') - optional

**Response:**
```json
{
  "data": [
    {
      "id": 5,
      "name": "Leather Armor",
      "armor_type": "light",
      "defense_bonus": 8,
      "speed_penalty": 0.0,
      "qi_efficiency_penalty": 0.0
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

#### GET /game/accessories

Get list of available accessories.

**Query Parameters:**
- `accessory_type`: Filter by accessory type ('ring', 'amulet', 'talisman', 'qi_focus') - optional

**Response:**
```json
{
  "data": [
    {
      "id": 3,
      "name": "Strength Ring",
      "accessory_type": "ring",
      "stat_bonuses": {"strength": 2}
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

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

