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
  "planet_id": 1
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
    "lumber": 500,
    "stone_blocks": 300,
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

### Game Data Documentation (Buildings, Resources, Species)

The public documentation system automatically syncs with game database tables for buildings, resources, and species. Each entity automatically gets a documentation article that can be viewed and edited.

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

**Warning:** Cannot delete if any NPCs of this species exist in the game world.

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

#### POST /avatars/{avatar_id}/expand-territory

Expand territory by claiming a neighboring 1-2km territory (partial ownership of 1m tiles).

**Request:**
```json
{
  "territory_id": 5,  // Neighboring 1-2km territory to claim
  "owned_percentage": 0.5  // Percentage of 1m tiles to assign (0.0 to 1.0)
}
```

**Response:**
```json
{
  "success": true,
  "territory": {
    "id": 5,
    "name": "Eastern Hills",
    "claimed_by_avatar_id": 22222,
    "partial_ownership": true
  },
  "tiles_assigned": 1250,  // Number of 1m tiles assigned to player
  "total_tiles": 2500,  // Total 1m tiles in the 1-2km territory
  "owned_percentage": 0.5,
  "message": "Territory expanded. 50% of tiles assigned to your territory."
}
```

**Status Codes:**
- `200 OK`: Territory expansion successful
- `400 Bad Request`: Invalid input, territory not adjacent, or insufficient resources
- `404 Not Found`: Avatar or territory not found
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Avatar doesn't belong to user

**Note:**
- This endpoint allows players to expand their control area by claiming neighboring 1-2km territories
- Player gets a percentage of the 1m tiles from the neighboring territory
- Remaining tiles can be assigned to other players or remain unclaimed
- Allows flexible territory expansion and strategic control

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

