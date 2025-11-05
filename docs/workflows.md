# TheVassalGame - Workflows and Game Flows

## Table of Contents
- [Overview](#overview)
- [User Registration and Authentication Flow](#user-registration-and-authentication-flow)
- [New Player Workflow](#new-player-workflow)
- [Planet Management Workflow](#planet-management-workflow)
- [Territory Generation Details](#territory-generation-details)
- [Territory Expansion Flow](#territory-expansion-flow)
- [Game Data Management Workflow](#game-data-management-workflow)
- [Building Placement Workflow](#building-placement-workflow)
- [Building Management Flow](#building-management-flow)
  - [Building Maintenance](#building-maintenance)
  - [Worker Assignment](#worker-assignment)
  - [Passive Resource Generation](#passive-resource-generation)
  - [Building Relocation](#building-relocation)
  - [Building Demolition](#building-demolition)
  - [Building Functionality Check](#building-functionality-check)
  - [Building Tier Upgrades](#building-tier-upgrades)
  - [Signature Addition Construction](#signature-addition-construction)
  - [Tier and Signature Addition Management](#tier-and-signature-addition-management)
- [District Formation](#district-formation)
- [Supply Chain Proximity Bonuses](#supply-chain-proximity-bonuses)
- [NPC Relationships and Events](#npc-relationships-and-events)
  - [NPC Relationship System](#npc-relationship-system)
  - [NPC Event Journal](#npc-event-journal)
  - [Personality Trait Derivation](#personality-trait-derivation)
  - [Random Events](#random-events)

## Overview

This document describes the user-facing workflows and system flows for TheVassalGame. It covers how users interact with the system, how components work together, and the step-by-step processes for key features.

## User Registration and Authentication Flow

### Registration Workflow

1. **User Registration**
   - User visits website registration page
   - User enters: email, username, password
   - System validates input (email format, username uniqueness, password strength)
   - System creates user account with status:
     - `email_verified = FALSE`
     - `account_approved = FALSE`
     - `role = 'Player'` (default)
     - Account status: **"Pending Verification"**
   - User is redirected to "Pending Verification" page

2. **Pending Verification State**
   - User sees pending verification page with:
     - Message explaining verification is required
     - Information about verification email sent
     - Option to resend verification email
     - Note about alternative: Admin approval
   - User cannot access any other part of the site while in pending state
   - User can log out but cannot log back in until verified/approved

3. **Email Verification Process**
   - System sends verification email containing:
     - **Verification Link**: Clickable link that verifies email when clicked
     - **Verification URL**: Plain text URL that user can copy/paste if they don't want to click links
     - Both links contain unique verification token
     - Token expires after 24 hours (configurable)
   - User clicks link OR pastes URL in browser
   - System validates token:
     - If valid: Sets `email_verified = TRUE`, removes "Pending Verification" state
     - If expired: Shows error, offers to resend verification email
     - If invalid: Shows error
   - **Alternative: Admin Approval**
     - Admin can approve user account, setting `account_approved = TRUE`
     - This bypasses email verification requirement
     - Approved users are removed from "Pending Verification" state

4. **Subscription Selection (Required)**
   - Once user is verified/approved, they are **forced** to subscription selection page
   - User cannot proceed to other parts of the site until subscription is selected
   - User sees subscription tiers:
     - **Initiate**: Free tier (no payment, no expiration)
     - **Novice**: Paid subscription tier
     - **Master**: Premium paid subscription tier
   - User selects subscription tier
   - System creates subscription record in database
   - For paid tiers: User completes payment process (Stripe)
   - User is redirected to next step after subscription selection

5. **Emperor's Offer Letter (Lore)**
   - After subscription selection, user is shown "Emperor's Offer Letter"
   - This is a documentation article from the public documentation system
   - Article slug: `emperor-offer-letter` (or similar, configurable)
   - User views the lore article (markdown rendered)
   - User must acknowledge/continue to proceed (prevents skipping)
   - This introduces the game world and story context:
     - The planet has been terraformed for millions of years in a time-dilation field
     - Players are uplifted members of a native species competing to become magistrates
     - The competition: develop territories, generate and refine mana
     - The prize: become ruler of the planet
     - The purpose: upgrade planet's core and power dimensional portal for colonists

6. **Planet Selection**
   - User is shown planet selection page
   - Initially: **One planet available** (designed during development)
   - System designed to support multiple planets in future
   - User selects planet
   - System stores planet selection in user profile
   - User proceeds to avatar creation

7. **First Login (After Initial Setup)**
   - After completing registration, verification, subscription, and planet selection:
   - User can log in normally with email/password
   - System checks: `email_verified = TRUE` OR `account_approved = TRUE`
   - System checks: User has active subscription
   - If all checks pass: Generate JWT token, grant access
   - User is taken to their dashboard/home page

8. **Session Management**
   - JWT token issued with user ID, role, permissions, subscription tier
   - Token stored in secure HTTP-only cookie or localStorage (client decision)
   - Token expiry: 1 hour (configurable)
   - Refresh token mechanism for extended sessions

## New Player Workflow

### First-Time Player Experience

1. **Prerequisites**
   - User has completed:
     - Registration
     - Email verification OR admin approval
     - Subscription selection
     - Viewed Emperor's Offer Letter (lore)
     - Selected planet

2. **Avatar Creation**
   - User navigates to avatar creation page (on selected planet)
   - User selects:
     - Avatar name (unique, may be planet-specific)
     - Starting faction/race (if applicable)
     - Appearance customization (if implemented)
   - System creates avatar in database:
     - Links avatar to user account
     - Links avatar to selected planet
     - Sets avatar status to 'pending' (not yet placed in world)
   - User proceeds to territory selection

3. **Territory Selection**
   - User is shown territory selection interface for their selected planet
   - User first chooses territory preference:
     - **Busy Territory**: Start near other players (social gameplay)
     - **Isolated Territory**: Start away from other players (solitary gameplay)
   - System displays available territories (1-2km tiles) based on preference:
     - **Busy Choice**: Shows territories with nearby busy-choice players
     - **Isolated Choice**: Shows territories without nearby players
     - System may also offer territories near established isolated players (difficult experience) if map is busy
   - System displays territory information:
     - Territory location on map (1-2km tile boundaries)
     - Terrain type (from parent potential territory)
     - **Qi source type**: qi vein or qi well
     - **Qi source potency**: Indicates mana generation potential
     - Nearby features (mountains, rivers, forests, etc.)
     - Difficulty level
     - Starting resources (if available)
   - User selects a territory (1-2km tile) for their avatar
   - System validates:
     - Territory is available (not already claimed)
     - Territory is on the selected planet
     - Territory matches user's preference (busy/isolated)
   - System assigns territory to avatar:
     - **Generates detailed features** for the selected territory at 1-2km level:
       - Mountains, hills, plains
       - Rivers, lakes
       - Forests, deserts
       - Resource nodes
       - **Qi source placement**: Finalizes qi vein or qi well location at precise 1m coordinates
       - All terrain features at 1-2km resolution
     - **Subdivides territory into 1m gameplay tiles**:
       - Creates all 1m edge tiles within the 1-2km territory
       - Generates elevation and terrain features for each 1m tile
       - Assigns all 1m tiles to the player's avatar
       - Sets `subdivided = TRUE` on territory
     - **Places avatar near qi source**:
       - Avatar starting location set within ~50-100m of the qi source
       - Starting location is safe and buildable (not on water, not on steep terrain)
       - Avatar spawns facing the qi source
     - **Provides starting resources**:
       - Avatar receives starting resource package for building
       - Resources include: basic materials (wood, stone), qi crystals, and initial supplies
       - Resources are sufficient to begin construction near the qi source
     - Links avatar to territory (`claimed_by_avatar_id`)
     - Updates territory to `territory_type = 'player_claimed'`
     - Sets territory preference (`busy` or `isolated`)
     - Updates nearby player counts for adjacent territories
     - Initializes starting resources based on territory
     - Sets territory ownership/permissions
     - Sets avatar status to 'active'
   - **Isolation Handling**:
     - If user chose "isolated": System sets `discourage_new_players = TRUE` for this territory
     - System discourages (but does not restrict) other new players from starting nearby
     - Adjacent territories may show warnings about nearby established players
   - System stores territory selection in database

4. **Tutorial/Onboarding** (Optional, Phase 2+)
   - After territory selection, user may be shown tutorial
   - System presents tutorial quests
   - Guides player through basic mechanics
   - Introduces core systems (building, resource gathering, etc.)
   - Tutorial may be territory-specific or planet-specific

5. **Game Entry**
   - Client connects to game server via WebSocket
   - Client sends authentication token
   - Server validates token and loads avatar data
   - Server loads:
     - Avatar's planet
     - Avatar's territory
     - World chunks within territory
   - Server determines appropriate shard for avatar (based on planet/territory)
   - Server sends initial world state to client:
     - Territory information
     - **Qi source location and type** (qi vein or qi well)
     - Nearby resources
     - Starting location (near qi source)
     - Starting resources in inventory
   - Client renders world and avatar
   - Player enters game at their territory
   - Player spawns near the qi source with starting resources
   - Player sees their 1-2km territory subdivided into 1m gameplay tiles
   - Player can begin building near the qi source to generate and refine mana

## Territory Expansion Flow

### Buying Neighboring Territories

1. **Territory Expansion Initiation**
   - Player wants to expand their territory
   - Player opens territory management interface
   - System displays neighboring 1-2km territories that are available or partially available
   - Player selects a neighboring territory to claim/expand into

2. **Territory Purchase/Claim**
   - Player initiates purchase/claim of neighboring territory
   - System validates:
     - Territory is adjacent to player's current territory
     - Territory is available (not fully claimed by another player)
     - Player has sufficient resources/permissions
   - Player completes purchase/claim

3. **Partial Territory Assignment**
   - System assigns a percentage of the neighboring territory's 1m tiles to the player
   - Not all 1m tiles from the neighboring territory are assigned
   - Player gets some percentage (e.g., 30-70%) of the 1m subtiles
   - Remaining percentage can be assigned to other players or remain unclaimed
   - System creates `territory_tiles` records with `owner_avatar_id` and `owned_percentage`
   - Player's control area expands gradually

4. **Gameplay Impact**
   - Player can now build and operate on the newly acquired 1m tiles
   - Player's territory extends across multiple 1-2km territory tiles
   - Territory boundaries become more complex (not just one 1-2km square)
   - Allows flexible expansion and strategic territory control

### Planet System Notes

- **Initial Planet**: One planet designed during development
- **Future Expansion**: System designed to support multiple planets
- **Planet-Specific Features**: Each planet may have:
  - Unique terrain/biomes
  - Unique resources
  - Unique factions/races
  - Unique gameplay mechanics
- **Avatar-Planet Relationship**: Avatars are linked to specific planets
- **Multi-Planet Support**: Users may be able to create avatars on different planets (future feature)

## In-Game Quest Flow

### Quest System Workflow

1. **Quest Availability**
   - Server checks quest triggers:
     - Location-based (player enters area)
     - Event-based (specific action performed)
     - Time-based (scheduled quests)
     - NPC interaction (NPC offers quest)
   - System determines available quests for player
   - Quest data sent to client via WebSocket

2. **Quest Acceptance**
   - Player views available quests in UI
   - Player selects quest to accept
   - Client sends quest acceptance request to server
   - Server validates:
     - Quest is available to player
     - Player meets requirements (level, previous quests, etc.)
   - Server adds quest to player's active quest list
   - Server updates quest status to 'active'
   - Server sends confirmation to client

3. **Quest Progress Tracking**
   - Server monitors quest objectives:
     - Kill X enemies
     - Collect X resources
     - Build X buildings
     - Reach X location
     - Interact with X NPC
   - As objectives are completed:
     - Server updates quest progress
     - Server sends progress updates to client
     - Client updates quest UI

4. **Quest Completion**
   - All quest objectives completed
   - Server detects completion
   - Server awards rewards:
     - Experience points
     - Resources
     - Items
     - Currency
     - Unlock new content
   - Server updates player state
   - Server marks quest as 'completed'
   - Server sends completion notification to client
   - Client displays reward notification

5. **Quest Chain Progression**
   - Completed quest may unlock:
     - New quests in chain
     - New quest givers
     - New areas
     - New abilities/features
   - Server updates available quests
   - Client receives quest updates

## Building and Construction Flow

### Building Placement Workflow

1. **Building Selection**
   - Player opens building menu
   - Client displays available buildings based on:
     - Player's unlocked buildings
     - Available resources
     - Current location restrictions
   - System displays for each building:
     - Base resource costs (before skill bonuses)
     - Base build time (before skill bonuses)
     - Estimated costs/time (with player's construction skill bonuses applied)
     - Building footprint (polygonal shape)
   - Player selects building type

2. **Placement Mode**
   - Client enters placement mode
   - Player sees building preview (ghost building) with polygonal footprint
   - Client validates placement in real-time:
     - Terrain suitability (footprint polygon fits)
     - No overlap with other buildings (footprint collision)
     - Distance from other buildings (if required)
     - Resource requirements
     - Door positions are accessible
   - Preview shows green (valid) or red (invalid)
   - Player can rotate building (if allowed)

3. **Placement Request**
   - Player confirms placement
   - Client sends placement request to server:
     - Building type
     - Position (X, Y coordinates - building center)
     - Rotation (if applicable)
   - Server validates:
     - Player has required resources (after skill bonuses calculated)
     - Location is valid (footprint polygon fits, no collisions)
     - Building is allowed at this location
     - Player has permission (land ownership, etc.)
     - Door positions are accessible

4. **Construction Calculation**
   - Server calculates construction skill bonuses:
     - Gets player's construction skill level
     - Calculates time reduction: `base_time * (1 - min(skill_level * time_bonus_per_level, max_skill_bonus))`
     - Calculates cost reduction: `base_cost * (1 - min(skill_level * cost_bonus_per_level, max_skill_bonus))`
   - Server determines actual build time and costs

5. **Building Creation**
   - Server deducts actual resources from player (after skill bonuses)
   - Server creates building entity in database:
     - Sets construction progress to 0.0
     - Records actual build time and costs
     - Records who constructed it
     - Sets initial durability from building type
     - Sets next maintenance due date
   - Server assigns building to world chunk
   - Server broadcasts building creation to nearby players
   - Server sends confirmation to placing player with:
     - Actual build time
     - Actual costs paid
   - Client renders new building in construction state

6. **Construction Progress**
   - Server tracks construction progress over time
   - Construction progress increases based on actual build time
   - If workers are assigned: Construction speed may be increased
   - Server sends periodic updates to client
   - Client displays construction progress bar
   - Building appears partially constructed (visual state)
   - When construction_progress reaches 1.0:
     - Building becomes functional
     - Sets `construction_completed_at` timestamp
     - If passive resources: Starts generating resources
     - If required workers: Checks if workers are assigned

7. **Post-Construction**
   - Building is now functional (if requirements met)
   - If building has passive resources: Starts accumulating
   - If building requires workers: Checks worker count
   - Maintenance schedule begins
   - Building starts durability degradation timer

## Building Management Flow

### Building Maintenance

1. **Maintenance Cycle**
   - Server checks buildings for maintenance needs periodically
   - For each building:
     - Checks if `next_maintenance_due_at` has passed
     - If overdue:
       - Sets `maintenance_overdue = TRUE`
       - Accumulates durability loss: `durability_loss_accumulated += durability_loss_per_cycle`
       - Applies durability loss: `durability -= durability_loss_accumulated`
       - If durability drops below threshold: Building becomes non-functional
   - Server sends maintenance warnings to building owner

2. **Performing Maintenance**
   - Player selects building
   - Player clicks "Perform Maintenance"
   - System checks:
     - Maintenance resources required
     - Player has required resources
     - Maintenance is due (or overdue)
   - Player confirms maintenance
   - Server deducts maintenance resources
   - Server updates building:
     - Sets `last_maintenance_at = NOW()`
     - Sets `next_maintenance_due_at = NOW() + maintenance_interval_hours`
     - Resets `maintenance_overdue = FALSE`
     - Resets `durability_loss_accumulated = 0.0`
     - Restores durability (if degraded, up to max)
   - Building continues functioning normally

3. **Durability Degradation**
   - If maintenance is missed:
     - Durability degrades each maintenance cycle
     - Degradation accumulates over time
     - If durability drops below `max_durability * (1 - max_durability_loss)`:
       - Building becomes non-functional
       - `is_functional = FALSE`
       - `functional_reason = 'Durability too low'`
   - Building cannot function until durability is restored via maintenance

### Worker Assignment

1. **Assign Worker to Building**
   - Player selects building
   - Player opens building management interface
   - System shows:
     - Current workers assigned
     - Available employment slots
     - Required workers (if any)
     - Skills workers will develop
   - Player selects available NPC to assign
   - System validates:
     - NPC is available (not assigned elsewhere)
     - Building has available employment slots
     - NPC is owner's (or neutral)
   - Server creates `building_employment` record:
     - Records NPC's current skill level in employment skill
     - Sets assignment timestamp
   - NPC moves to building and enters through door
   - NPC begins working at building

2. **Worker Skill Development**
   - While NPC is assigned to building:
     - Server periodically checks skill development
     - NPC gains experience in `employment_skill`
     - Skill level increases over time
     - System tracks improvement from assignment start
   - Higher skill levels improve building efficiency (if applicable)
   - Player can see skill improvement in building interface

3. **Remove Worker from Building**
   - Player selects building
   - Player opens worker management
   - Player selects worker to remove
   - Server removes `building_employment` record
   - NPC exits building through door
   - NPC becomes available for other assignments
   - If building requires workers: Checks if minimum requirement is still met

4. **Required Workers Check**
   - If building has `required_workers > 0`:
     - System checks number of assigned workers
     - If `assigned_workers < required_workers`:
       - Building becomes non-functional
       - `is_functional = FALSE`
       - `functional_reason = 'Insufficient workers'`
     - If `assigned_workers >= required_workers`:
       - Building becomes functional (if other conditions met)
       - `is_functional = TRUE`

### Passive Resource Generation

1. **Resource Accumulation**
   - Server processes passive resources periodically (daily)
   - For each building with passive resources:
     - Checks if building is functional
     - If `passive_resources_requires_workers = TRUE`:
       - Checks if required workers are assigned
     - Calculates time since last generation
     - Calculates resources generated: `rate_per_day * (time_days)`
     - Adds to `accumulated` in `building_passive_resources`
     - Updates `last_generated_at`

2. **Collecting Passive Resources**
   - Player selects building
   - Player sees accumulated resources in building interface
   - Player clicks "Collect Resources"
   - Server transfers accumulated resources to player inventory
   - Server resets `accumulated = 0.0`
   - Resources are now available to player

### Building Relocation

1. **Initiate Relocation**
   - Player selects building
   - Player checks if building is relocatable
   - If relocatable:
     - Player opens relocation interface
     - System shows:
       - Relocation cost (percentage of build cost)
       - Relocation time (percentage of build time)
       - Worker requirement (if applicable)
     - Player selects new location
     - Client validates new location (footprint polygon, no collisions)
     - Player confirms relocation

2. **Relocation Process**
   - Server validates:
     - Building is relocatable
     - Player has relocation resources
     - New location is valid
     - Workers available (if required)
   - Server deducts relocation resources
   - Server sets building to relocation state:
     - `is_relocating = TRUE`
     - `relocation_progress = 0.0`
     - Stores original location
     - Sets target location
     - Sets `relocation_started_at`
   - Building becomes non-functional during relocation
   - Workers begin deconstruction (if required)

3. **Relocation Progress**
   - Server tracks relocation progress over time
   - Relocation progress increases based on relocation time
   - If workers required: Progress increases faster
   - Building appears partially deconstructed
   - When `relocation_progress >= 0.5`:
     - Building disappears from original location
     - Building appears at new location (still under construction)
   - When `relocation_progress >= 1.0`:
     - Relocation complete
     - Building is fully reconstructed at new location
     - Building becomes functional again
     - Server updates:
       - `world_x`, `world_y` to new location
       - `is_relocating = FALSE`
       - `relocation_progress = 0.0`
       - Clears relocation state

### Building Demolition

1. **Demolish Building**
   - Player selects building
   - Player opens building management
   - Player clicks "Demolish Building"
   - System shows:
     - Resources that will be returned (percentage of build cost)
     - Warning about permanent removal
   - Player confirms demolition

2. **Demolition Process**
   - Server processes demolition:
     - Calculates resource return: `actual_cost_data * demolition_resource_return`
     - Returns resources to player inventory
     - Removes all workers from building
     - Removes building from world
     - Sets `demolished_at` timestamp
     - Deletes building record (or marks as demolished)
   - Building disappears from world
   - Resources are added to player inventory

### Building Functionality Check

1. **Functionality Status**
   - Building may be non-functional due to:
     - Durability too low (`durability < max_durability * (1 - max_durability_loss)`)
     - Required workers not assigned (`required_workers > assigned_workers`)
     - Building-specific conditions
   - System checks functionality periodically:
     - Checks durability threshold
     - Checks worker requirements
     - Updates `is_functional` flag
     - Sets `functional_reason` if non-functional
   - Non-functional buildings:
     - Do not generate passive resources
     - Do not process production queues
     - May still be maintained/repaired
   - Building becomes functional again when conditions are met

### Building Tier Upgrades

1. **View Available Upgrades**
   - Player selects building
   - System displays:
     - Current tier (1-6)
     - Next tier available (if not at max tier)
     - Upgrade costs and time
     - Benefits of next tier (housing, qi output, unlocks)
     - Signature addition available for current tier (if not built)
   - Player can see all 6 tiers and their benefits

2. **Initiate Tier Upgrade**
   - Player selects building
   - Player clicks "Upgrade to Tier {N}"
   - System validates:
     - Building is at tier N-1
     - Player has required resources
     - Building is functional (not under construction/relocation)
   - Player confirms upgrade
   - Server calculates upgrade costs (after skill bonuses if applicable)
   - Server deducts resources
   - Server initiates upgrade:
     - Sets `tier_upgrade_progress = 0.0`
     - Sets `tier_upgrade_started_at = NOW()`
     - Building becomes non-functional during upgrade
     - Building appears under construction

3. **Upgrade Progress**
   - Server tracks upgrade progress over time
   - Upgrade progress increases based on upgrade time
   - If workers assigned: Upgrade speed may be increased
   - Server sends periodic updates to client
   - Client displays upgrade progress bar
   - Building appears partially upgraded (visual state)
   - When `tier_upgrade_progress >= 1.0`:
     - Upgrade complete
     - Building tier increases: `current_tier = N`
     - Building benefits update:
       - Housing capacity increases
       - Qi output rate increases
       - Unlocks become available
       - Health/durability modifiers apply
       - Employment slots update
     - Building becomes functional again
     - Signature addition for new tier becomes available

4. **Post-Upgrade**
   - Building now has new tier benefits
   - New features/building types unlocked
   - Player can now:
     - Build signature addition for new tier
     - Upgrade to next tier (if available)
     - Use new housing capacity
     - Benefit from increased qi output

### Signature Addition Construction

1. **View Signature Addition**
   - Player selects building
   - System displays signature addition for current tier:
     - Name and description
     - Construction costs
     - Build time
     - Additional space required
     - Benefits provided
     - Whether already built
   - Player can see preview of where it attaches to building

2. **Build Signature Addition**
   - Player selects building
   - Player clicks "Build Signature Addition"
   - System validates:
     - Building has signature addition available for current tier
     - Signature addition not already built
     - Player has required resources
     - Additional footprint space is available (no collisions)
     - Building is functional
   - Player confirms construction
   - Server calculates construction costs (after skill bonuses)
   - Server deducts resources
   - Server initiates signature addition construction:
     - Sets `signature_addition_id` to the signature addition
     - Sets `signature_addition_progress = 0.0`
     - Sets `signature_addition_started_at = NOW()`
     - Building remains functional during construction

3. **Signature Addition Progress**
   - Server tracks construction progress over time
   - Progress increases based on build time
   - If workers assigned: Construction speed may be increased
   - Server sends periodic updates to client
   - Client displays construction progress
   - Signature addition appears partially constructed
   - When `signature_addition_progress >= 1.0`:
     - Construction complete
     - Signature addition benefits apply:
       - Qi output bonus
       - Housing bonus
       - Additional unlocks
       - Special effects/visuals
     - Building footprint includes signature addition

4. **Signature Addition Benefits**
   - Benefits are active once construction completes
   - Benefits persist until building is demolished or signature addition is removed (if allowed)
   - Benefits stack with tier benefits
   - Visual effects and special features become active

### Tier and Signature Addition Management

1. **Current Tier Benefits**
   - Building benefits are calculated from:
     - Base building type properties
     - Current tier modifiers
     - Signature addition bonuses (if built)
   - System calculates:
     - Total housing capacity = `tier_housing + signature_housing_bonus`
     - Total qi output = `tier_qi_output * (1 + signature_qi_bonus)`
     - Total unlocks = `tier_unlocks + signature_unlocks`
   - Benefits update automatically when tier changes or signature addition is built

2. **Upgrade Path Planning**
   - Player can view full upgrade path:
     - All 6 tiers and their costs
     - All signature additions and their costs
     - Total resources needed for full upgrade path
   - Helps player plan resource allocation

3. **Tier-Specific Maintenance**
   - Higher tiers may require more maintenance resources
   - Maintenance costs scale with tier
   - Signature additions may add maintenance requirements

### District Formation

1. **Automatic District Detection**
   - Server periodically scans for building clusters
   - For each building category:
     - System finds buildings of the same category
     - Calculates distances between buildings
     - Groups buildings within formation threshold (default: 50m)
     - Checks if group meets minimum building requirement (default: 3)

2. **District Formation**
   - When conditions are met:
     - System calculates district center (average of building positions)
     - System calculates district radius (to encompass all buildings)
     - System creates district boundary polygon
     - System creates district record
     - System assigns all qualifying buildings to district
     - System applies district bonuses to all buildings
   - District name is auto-generated (e.g., "Civic District", "Resource District") or can be customized

3. **District Benefits Application**
   - Buildings in district receive district bonuses:
     - Bonus type depends on category (efficiency, production, cost reduction, qi output)
     - Bonus value is base value + scaling (if enabled) based on building count
     - Benefits apply automatically:
       - Production efficiency increases
       - Resource generation increases
       - Maintenance costs reduced
       - Qi output increases
   - System updates building records:
     - Sets `district_id`
     - Sets `district_bonus_applied = TRUE`
     - Updates `proximity_bonuses` with district bonus

4. **District Maintenance**
   - System periodically checks district validity:
     - Verifies building count still meets minimum
     - Checks if buildings are still within district boundaries
     - Updates district boundaries if buildings added/removed
   - If building count drops below minimum:
     - District becomes inactive (`is_active = FALSE`)
     - District bonuses are removed from buildings
     - District is marked for dissolution
   - If buildings are removed too far:
     - District boundaries are recalculated
     - District may be split into multiple districts
     - Or district may be dissolved if below minimum

5. **District Dissolution**
   - When district dissolves:
     - System removes district bonuses from all buildings
     - Sets `district_id = NULL` on all buildings
     - Sets `district_bonus_applied = FALSE`
     - Marks district as dissolved (`dissolved_at = NOW()`)
     - Buildings remain but lose district benefits

### Supply Chain Proximity Bonuses

1. **Supply Chain Detection**
   - When building is constructed:
     - System checks if building type belongs to a supply chain
     - System scans for other buildings in the same supply chain within proximity range
     - System calculates proximity bonuses based on linked buildings

2. **Proximity Bonus Calculation**
   - For each building in supply chain:
     - System finds all linked buildings within proximity range
     - For each linked building found:
       - Calculates distance
       - Applies link-specific proximity bonus
       - Accumulates bonuses
   - System applies total proximity bonus (capped at maximum)
   - Bonus types:
     - Production efficiency
     - Resource generation
     - Cost reduction
     - Quality improvement

3. **Dynamic Proximity Updates**
   - System periodically recalculates proximity bonuses:
     - When new buildings are constructed nearby
     - When buildings are demolished
     - When buildings are relocated
   - System updates building `proximity_bonuses` JSONB field
   - Bonuses apply automatically to building operations

4. **Supply Chain Link Types**
   - **Produces**: Source building produces resources for target building
     - Bonus when target is near source
   - **Consumes**: Target building consumes resources from source
     - Bonus when target is near source
   - **Transforms**: Source building transforms resources for target
     - Bonus applies in both directions
   - **Enhances**: Source building enhances target building's operations
     - Bonus applies to target building

5. **Combined Bonuses**
   - Buildings can receive multiple bonuses:
     - District bonus (from category clustering)
     - Supply chain proximity bonus (from linked buildings)
     - Bonuses stack multiplicatively or additively (configurable)
   - System calculates total effective bonus:
     - `total_efficiency = base * (1 + district_bonus) * (1 + proximity_bonus)`
   - Maximum bonus cap prevents unlimited stacking

## Resource Management Flow

### Resource Gathering Workflow

1. **Resource Node Discovery**
   - Player explores world
   - Server loads resource nodes in visible chunks
   - Client renders resource nodes on map
   - Player approaches resource node

2. **Resource Gathering Initiation**
   - Player selects resource node
   - Player initiates gathering action
   - Client sends gather request to server
   - Server validates:
     - Node is accessible
     - Node has resources remaining
     - Player has gathering capability (tools, workers, etc.)

3. **Resource Extraction**
   - Server processes gathering:
     - Calculates gathering rate (based on tools, workers, skills)
     - Deducts resources from node
     - Adds resources to player inventory/storage
   - Server sends resource updates to client
   - Client updates UI with new resource counts

4. **Resource Node Depletion**
   - Node resources reach zero
   - Server marks node as depleted
   - Server schedules node respawn (if applicable)
   - Server broadcasts node depletion to nearby players
   - Client updates node visualization (depleted state)

### Resource Production Flow

1. **Production Building Operation**
   - Player places production building
   - Player configures production:
     - Select recipe/product
     - Set production queue
     - Allocate resources for production
   - Client sends production configuration to server

2. **Production Processing**
   - Server processes production:
     - Validates required resources available
     - Deducts input resources
     - Tracks production time
     - Produces output resources
   - Server sends production updates to client
   - Client displays production progress

3. **Resource Collection**
   - Production completes
   - Output resources added to building storage
   - Player collects resources
   - Resources transferred to player inventory/storage
   - Server updates player and building state

## Trading Flow

### Trade System Workflow

1. **Trade Offer Creation**
   - Player opens trade interface
   - Player selects items/resources to offer
   - Player specifies desired items/resources
   - Player sets trade terms (ratio, quantity, etc.)
   - Client sends trade creation request to server
   - Server validates:
     - Player has offered items/resources
     - Trade terms are valid
   - Server creates trade offer in database
   - Server broadcasts trade offer (if public)

2. **Trade Discovery**
   - Players can browse available trades:
     - Global market
     - Local market (region-based)
     - Player-to-player trades
   - Server filters trades based on:
     - Player location
     - Player preferences
     - Trade relevance
   - Client displays available trades

3. **Trade Acceptance**
   - Player selects trade to accept
   - Client sends trade acceptance to server
   - Server validates:
     - Trade still available
     - Both parties have required items/resources
     - Trade hasn't expired
   - Server executes trade:
     - Transfers items from both parties
     - Deducts trade fees (if applicable)
     - Updates trade status to 'completed'
   - Server notifies both parties
   - Client updates both players' inventories

## Combat Flow

### Combat System Workflow

1. **Combat Initiation**
   - Player selects target (enemy unit, building, NPC)
   - Player initiates attack action
   - Client sends attack request to server
   - Server validates:
     - Target is valid
     - Target is in range
     - Player has attack capability

2. **Combat Resolution**
   - Server calculates combat:
     - Attack damage (weapon, stats, bonuses)
     - Defense (armor, stats, bonuses)
     - Hit chance
     - Critical hit chance
   - Server applies damage
   - Server updates target health
   - Server broadcasts combat event to nearby players
   - Client displays combat animations/effects

3. **Combat Outcome**
   - Target health reaches zero:
     - Server marks target as defeated
     - Server awards experience/resources to attacker
     - Server removes target from world (if applicable)
     - Server broadcasts defeat to nearby players
   - Combat continues until one side is defeated or retreats

## Player Disconnection Flow

### Graceful Disconnection

1. **Client Disconnection Detection**
   - Client loses connection to server
   - Server detects connection loss
   - Server enters "graceful disconnect" mode

2. **State Preservation**
   - Server saves player state:
     - Current position
     - Inventory
     - Active quests
     - Building ownership
     - Resources
   - Server persists state to database
   - Server marks player as "offline"

3. **Reconnection**
   - Player reconnects
   - Client sends authentication token
   - Server validates token
   - Server loads saved player state
   - Server restores player to previous position/state
   - Server sends world state update to client
   - Player continues from where they left off

## Admin Workflow

### Admin Actions Flow

1. **Admin Authentication**
   - Admin logs in with admin credentials
   - Server validates admin role
   - Server issues admin JWT token with admin permissions

2. **Admin Panel Access**
   - Admin accesses admin panel on website
   - Admin panel loads available admin actions
   - Actions include:
     - User management (approve, ban, role changes)
     - **Planet Management** (create, modify planets)
     - **Game Data Management** (buildings, resources, species - create, edit, archive, delete)
     - World configuration
     - NPC management
     - Event management
     - System monitoring

## Planet Management Workflow

### Planet Creation (Admin/StoryTeller)

1. **Access Planet Management**
   - Admin or StoryTeller accesses Planet Management interface
   - Interface shows list of existing planets
   - User clicks "Create New Planet" button

2. **Planet Configuration**
   - User enters basic information:
     - Planet name (unique)
     - Planet description
   - System automatically creates documentation section slug (e.g., `planet-aurora`)
   - User selects geography preset:
     - Pangaea (single large continent)
     - Few Large Continents (2-4 large continents)
     - Many Small Continents (many small continents)
     - Archipelago (many small islands)
     - Custom (manual parameter configuration)
   - User adjusts terrain parameters:
     - **Sea Level**: Slider (-1.0 to 1.0) - controls land-sea ratio
     - **Mountain Peak Height**: Slider (0.0 to 2.0) - multiplier for mountain heights
     - **Ocean Trench Depth**: Slider (0.0 to 2.0) - multiplier for ocean depths
     - **Terrain Roughness**: Slider (0.0 to 1.0) - how hilly/flat terrain is
   - User sets generation parameters:
     - Icosahedron subdivisions (default: 8, subdivided to 1-2m edge faces)
     - Maximum LOD level (default: 15, for 1-meter resolution)
     - Optional: Random seed for generation

3. **Planet Generation**
   - User clicks "Generate Planet" button
   - System validates parameters
   - System creates planet record in database with status 'pending'
   - System creates documentation section for planet (slug: `planet-{name-slug}`)
   - System queues planet generation job:
     - Status set to 'generating'
     - Progress tracking begins
   - Generation process:
     - **Phase 1: Outer Subdivision**
       - Creates icosahedron base (20 triangles)
       - Subdivides icosahedron based on subdivision level
       - Generates terrain using selected preset and parameters
       - Applies sea level, mountain heights, ocean depths, terrain roughness
       - Generates heightmaps, biomes at planet scale
     - **Phase 2: Potential Territory Seeding**
       - System identifies major landmasses and oceans
       - Selects 1 tile in each major landmass and ocean
       - Subdivides these tiles down to 1-2km edge lengths
       - Generates detailed features for each potential territory:
         - Mountains, hills, plains
         - Rivers, lakes
         - Forests, deserts
         - Other terrain features
       - Creates potential territory records (`territory_type = 'potential'`)
     - **Phase 3: Starting Tile Selection**
       - From each potential territory (1-2km tile), system picks 8 subdivided tiles
       - These tiles are 1-2km edge tiles (territories, not the 1m gameplay tiles)
       - Creates starting tile records (`territory_type = 'starting_tile'`)
       - **Note**: Detailed features for starting tiles are NOT generated yet (on-demand)
       - These are the territories that will be offered to players
     - Saves planet data to database
     - Updates generation status to 'completed'
   - User can monitor generation progress in real-time
   - On completion: Planet becomes available for selection

4. **Planet Documentation**
   - System automatically creates documentation section for planet
   - Documentation section includes:
     - Planet name and description
     - Generation parameters
     - Geography preset used
     - Planet statistics (size, land-sea ratio, etc.)
   - StoryTellers/Admins can edit planet documentation
   - Documentation is accessible to all users (public documentation system)

### Planet Modification (Admin/StoryTeller)

1. **Select Planet**
   - Admin/StoryTeller selects planet from management interface
   - System loads planet details and current configuration

2. **Modify Planet Settings**
   - User can modify:
     - Planet name (if no avatars exist on planet)
     - Planet description
     - Active status (enable/disable for selection)
     - Documentation content
   - **Note**: Generation parameters cannot be modified after generation (would require regeneration)
   - **Regeneration**: Admin can trigger planet regeneration:
     - WARNING: This will regenerate all terrain data
     - May affect existing avatars/buildings (requires confirmation)
     - New generation uses same or updated parameters

3. **Save Changes**
   - User saves modifications
   - System validates changes
   - System updates planet record
   - System updates documentation section if needed
   - Changes are reflected immediately

## Game Data Management Workflow

### Building Types Management (Admin/StoryTeller)

1. **Access Building Management**
   - Admin or StoryTeller accesses Building Management interface
   - Interface shows list of all building types
   - Filters available: category, status (active/archived)

2. **Create Building Type**
   - User clicks "Create New Building" button
   - User enters building information:
     - Name, category, description
     - Size, build time, health
     - Resource costs (JSONB)
     - Production/mana generation data
   - System validates input
   - System creates building type record
   - **System automatically creates documentation article**:
     - Slug: `building-{name-slug}` (auto-generated)
     - Title: "Building: {name}"
     - Category: "reference"
     - Initial content: Auto-generated from database fields
   - Building type becomes available in game and documentation

3. **Edit Building Type**
   - User selects building type to edit
   - User can modify:
     - Description, detailed description
     - Building properties (size, costs, etc.)
     - Status (active/archived)
   - **Documentation sync**: Changes to description fields automatically update documentation article
   - User can also edit documentation article directly for lore/details
   - Changes are saved and synced

4. **Archive Building Type**
   - User archives building type
   - Building type status set to 'archived'
   - **Documentation**: Article is hidden from public view but not deleted
   - Existing buildings of this type continue to function
   - Building type hidden from selection in game

5. **Delete Building Type** (Admin only)
   - Admin can permanently delete building type
   - System validates: No buildings of this type exist in game
   - If valid: Deletes building type and documentation article
   - If invalid: Returns error, cannot delete

### Resource Types Management (Admin/StoryTeller)

1. **Access Resource Management**
   - Admin or StoryTeller accesses Resource Management interface
   - Interface shows list of all resource types
   - Filters available: category, rarity, status

2. **Create Resource Type**
   - User clicks "Create New Resource" button
   - User enters resource information:
     - Name, category, description
     - Rarity, gathering method
     - Base value, stack size
   - System validates input
   - System creates resource type record
   - **System automatically creates documentation article**:
     - Slug: `resource-{name-slug}` (auto-generated)
     - Title: "Resource: {name}"
     - Category: "reference"
     - Initial content: Auto-generated from database fields
   - Resource type becomes available in game and documentation

3. **Edit Resource Type**
   - User selects resource type to edit
   - User can modify:
     - Description, detailed description
     - Resource properties (value, rarity, etc.)
     - Status (active/archived)
   - **Documentation sync**: Changes automatically update documentation article
   - User can also edit documentation article directly for lore/details

4. **Archive Resource Type**
   - User archives resource type
   - Resource type status set to 'archived'
   - **Documentation**: Article is hidden from public view but not deleted
   - Existing resource nodes of this type continue to exist
   - Resource type hidden from selection in game

5. **Delete Resource Type** (Admin only)
   - Admin can permanently delete resource type
   - System validates: No resource nodes or items of this type exist
   - If valid: Deletes resource type and documentation article
   - If invalid: Returns error, cannot delete

### Species Management (Admin/StoryTeller)

1. **Access Species Management**
   - Admin or StoryTeller accesses Species Management interface
   - Interface shows list of all species
   - Filters available: category, sapient status, status

2. **Create Species**
   - User clicks "Create New Species" button
   - User enters species information:
     - Name, category, description
     - Sapient status, size category
     - Habitat, diet
   - System validates input
   - System creates species record
   - **System automatically creates documentation article**:
     - Slug: `species-{name-slug}` (auto-generated)
     - Title: "Species: {name}"
     - Category: "lore"
     - Initial content: Auto-generated from database fields
   - Species becomes available in game and documentation

3. **Edit Species**
   - User selects species to edit
   - User can modify:
     - Description, detailed description (lore/biology)
     - Species properties (habitat, diet, etc.)
     - Status (active/archived)
   - **Documentation sync**: Changes automatically update documentation article
   - User can also edit documentation article directly for extended lore

4. **Archive Species**
   - User archives species
   - Species status set to 'archived'
   - **Documentation**: Article is hidden from public view but not deleted
   - Existing NPCs of this species continue to exist
   - Species hidden from selection in game

5. **Delete Species** (Admin only)
   - Admin can permanently delete species
   - System validates: No NPCs of this species exist
   - If valid: Deletes species and documentation article
   - If invalid: Returns error, cannot delete

### Documentation Auto-Sync

1. **Automatic Documentation Creation**
   - When a building/resource/species is created:
     - System generates documentation article slug from name
     - System creates article with auto-generated content
     - Article category: "reference" (buildings/resources) or "lore" (species)
     - Article is linked to the database entity

2. **Automatic Documentation Updates**
   - When building/resource/species fields are updated:
     - System updates corresponding documentation article
     - Description fields sync to article content
     - Technical fields (costs, stats) are included in article

3. **Manual Documentation Editing**
   - StoryTellers/Admins can edit documentation articles directly
   - Manual edits override auto-generated content
   - System preserves manual edits when syncing
   - Allows adding lore, details, examples beyond database fields

4. **Documentation Visibility**
   - Active entities: Documentation visible to all users
   - Archived entities: Documentation hidden from public view
   - StoryTellers/Admins can view archived documentation

### Planet Selection by Players

1. **View Available Planets**
   - Player sees list of active planets during onboarding
   - Each planet shows:
     - Planet name
     - Description
     - Link to planet documentation
   - Player can view planet documentation before selecting

2. **Planet Documentation Access**
   - Player clicks planet documentation link
   - Documentation page loads from public documentation system
   - Shows planet lore, geography, features, etc.
   - Player can read and comment on planet documentation

3. **Planet Selection**
   - Player selects planet
   - System stores selection in user profile
   - Player proceeds to avatar creation on selected planet

### Territory Generation Details

1. **Potential Territory Generation** (During Planet Generation)
   - System identifies major landmasses and oceans from planet-scale generation
   - For each major landmass/ocean:
     - Selects 1 representative tile
     - Subdivides tile down to 1-2km edge lengths
     - Generates detailed terrain features:
       - Mountain ranges and peaks
       - Hills and valleys
       - Plains and plateaus
       - River systems
       - Lakes and water bodies
       - Forest areas
       - Desert regions
       - Other biome-specific features
   - These potential territories serve as starting areas

2. **Starting Territory Selection** (During Planet Generation)
   - From each potential territory (1-2km tile):
     - System selects 8 subdivided tiles (1-2km edge tiles)
     - These are the territories offered to players
     - Territories are NOT detailed yet (on-demand generation)
   - Starting territories inherit terrain characteristics from parent potential territory

3. **On-Demand Detail Generation and Subdivision** (When Player Selects)
   - When player selects a territory (1-2km tile):
     - **Step 1: Generate 1-2km Level Features**
       - System generates detailed features at 1-2km resolution
       - Creates terrain features:
         - Mountain ranges and peaks
         - River systems and paths
         - Lake boundaries
         - Forest areas and boundaries
         - Desert regions
         - Resource node placement
     - **Step 2: Finalize Qi Source**
       - System finalizes qi source location at precise 1m coordinates
       - Qi source type (qi vein or qi well) is already determined
       - Qi source coordinates stored in territory record
     - **Step 3: Subdivide into 1m Gameplay Tiles**
       - System subdivides the 1-2km territory into 1m edge tiles
       - For each 1m tile:
         - Generates precise elevation
         - Assigns specific terrain features (mountain peak, river, lake, forest, desert, plains)
         - Places resource nodes
         - Marks tile containing qi source (if applicable)
         - Assigns tile to player's avatar (`owner_avatar_id`)
       - Creates all `territory_tiles` records for the 1m tiles
     - **Step 4: Place Avatar and Starting Resources**
       - System places avatar starting location near qi source (~50-100m away)
       - Starting location is validated: safe, buildable terrain
       - Avatar receives starting resources package for building
       - Player now controls all 1m tiles within their 1-2km territory
     - This ensures detailed generation and subdivision only happens when needed

### Admin Action Execution

1. **Admin Action Execution**
   - Admin selects action
   - Admin provides action parameters
   - Client sends action request to server
   - Server validates:
     - Admin has permission for action
     - Action parameters are valid
   - Server executes action
   - Server logs action to audit log
   - Server sends confirmation to admin
   - Admin panel updates to reflect changes

## System Integration Flows

### Website ↔ Game Server Integration

1. **Account Linking**
   - User account exists on website
   - User creates avatar on website
   - Avatar linked to user account
   - Avatar data stored in shared database
   - Game server accesses avatar data from database

2. **Subscription Integration**
   - User subscribes on website
   - Website updates subscription in database
   - Game server queries subscription status
   - Game server applies subscription benefits to player
   - Subscription features unlocked in-game

3. **Documentation Integration**
   - StoryTellers create lore articles on website
   - Articles stored in documentation database
   - Website displays articles to users
   - Game client can optionally fetch lore articles
   - In-game events reference documentation articles

## NPC Relationships and Events

### NPC Relationship System

NPCs form relationships with each other and with buildings through interactions. These relationships affect behavior, decision-making, and reactions to events.

#### 1. **Initial Relationship Creation**
   - When NPCs first interact, a relationship record is created
   - Initial relationship values start at 0.0 (neutral)
   - Relationship type is determined by context:
     - Work colleagues: `colleague`
     - Social interactions: `friend` or `neutral`
     - Building visits: `patron` or `frequent_visitor`
   - First interaction timestamp recorded
   - Interaction count initialized to 1

#### 2. **Relationship Updates During Interactions**
   - Each interaction between NPCs can modify relationship values
   - Positive interactions (helping, sharing, working together) increase relationship value
   - Negative interactions (conflict, competition, harm) decrease relationship value
   - Relationship history entry created for each change
   - Trust and familiarity increase with repeated positive interactions
   - Trust decreases with negative interactions
   - Familiarity increases with any interaction (positive or negative)

#### 3. **Relationship Value Calculation**
   - Relationship value: -100.0 (hostile) to +100.0 (very friendly)
   - Trust level: 0.0 to 1.0 (how much NPC trusts target)
   - Familiarity: 0.0 to 1.0 (how well NPC knows target)
   - Values decay slowly over time if no interactions occur
   - Strong relationships (high value) decay more slowly than weak ones

#### 4. **Building Relationships**
   - NPCs form relationships with buildings they visit frequently
   - Working at a building creates `employee` relationship
   - Visiting a building regularly creates `patron` or `frequent_visitor` relationship
   - Building relationships affect NPC preferences:
     - NPCs prefer to visit buildings they have positive relationships with
     - NPCs avoid buildings with negative relationships
     - High relationship with building increases NPC satisfaction

#### 5. **Relationship Impact on Behavior**
   - NPCs prefer to interact with NPCs they have positive relationships with
   - NPCs avoid or react negatively to NPCs with negative relationships
   - High trust levels make NPCs more likely to:
     - Share information
     - Help in conflicts
     - Form alliances
     - Accept advice
   - Low trust levels make NPCs:
     - Suspicious
     - Unlikely to help
     - More likely to conflict

### NPC Event Journal

NPCs maintain a journal of significant events in their lives. Events affect relationships, personality, and future behavior.

#### 1. **Event Creation**
   - Events are created automatically by the simulation system
   - Events can be triggered by:
     - NPC interactions (social, work, conflict)
     - Work activities (job started, completed, promotion)
     - Random events (discovery, accident, opportunity)
     - Player actions (building construction, territory changes)
     - System events (festivals, celebrations, disasters)
   - Each event has:
     - Type (interaction, work, social, random, etc.)
     - Severity (minor, normal, significant, major, life_changing)
     - Title and description
     - Location (building, territory, world coordinates)
     - Related NPCs and buildings
     - Relationship impacts
     - Personality impacts

#### 2. **Event Severity and Impact**
   - **Minor Events**: Routine daily activities, minor conversations
     - Small relationship adjustments (0-2 points)
     - Minimal personality impact
   - **Normal Events**: Regular work, standard interactions
     - Moderate relationship adjustments (2-5 points)
     - Small personality adjustments
   - **Significant Events**: Major achievements, friendships formed
     - Larger relationship adjustments (5-15 points)
     - Notable personality adjustments
   - **Major Events**: Promotions, major conflicts, relationship milestones
     - Large relationship adjustments (15-30 points)
     - Significant personality adjustments
   - **Life-Changing Events**: Death of friend, major discovery, career change
     - Massive relationship adjustments (30-50+ points)
     - Major personality shifts

#### 3. **Event Relationship Impacts**
   - Events automatically update relationship values
   - Relationship impacts are stored in event's `relationship_impacts` JSONB
   - Example: "Helped NPC during conflict" → +10 relationship value
   - Example: "Competed for same job" → -5 relationship value
   - Relationship history records track all changes
   - Multiple NPCs can be affected by the same event

#### 4. **Event Personality Impacts**
   - Events slowly adjust personality traits over time
   - Personality impacts are stored in event's `personality_impact` JSONB
   - Example: "Helped friend in need" → `{"friendly": 0.02, "loyal": 0.01}`
   - Example: "Was betrayed" → `{"trusting": -0.03, "cautious": 0.02}`
   - Personality traits are recalculated periodically from event history
   - Major events have larger personality impacts than minor events

#### 5. **Event Journal Queries**
   - NPCs can query their event history
   - Events can be filtered by:
     - Type
     - Severity
     - Time range
     - Importance
     - Related NPCs or buildings
   - Most important/recent events are prioritized in queries
   - Events are never deleted (act as permanent journal)

### Personality Trait Derivation

Personality traits are derived from an NPC's event history and relationships. Traits influence behavior and reactions.

#### 1. **Personality Trait Calculation**
   - Traits are calculated periodically (daily or weekly)
   - Calculation analyzes:
     - Recent events (last 30-90 days weighted more heavily)
     - Relationship history patterns
     - Event frequency and types
     - Major life events
   - Traits are stored as JSONB: `{"friendly": 0.7, "cautious": 0.4, "ambitious": 0.6}`
   - Trait values range from 0.0 to 1.0
   - Traits are normalized to prevent extreme values

#### 2. **Common Personality Traits**
   - **Social Traits**: friendly, introverted, charismatic, antisocial
   - **Behavioral Traits**: cautious, reckless, patient, impulsive
   - **Work Traits**: ambitious, lazy, diligent, perfectionist
   - **Emotional Traits**: optimistic, pessimistic, resilient, fragile
   - **Trust Traits**: trusting, suspicious, loyal, treacherous

#### 3. **Personality Impact on Behavior**
   - High `friendly` trait: NPCs more likely to initiate social interactions
   - High `cautious` trait: NPCs avoid risky situations, prefer familiar locations
   - High `ambitious` trait: NPCs seek promotions, take on challenging work
   - High `trusting` trait: NPCs form relationships quickly, believe others
   - Low `trusting` trait: NPCs are suspicious, slow to form relationships
   - Personality traits affect:
     - Job preferences
     - Building visit frequency
     - Social interaction frequency
     - Reaction to events
     - Decision-making

#### 4. **Personality Evolution**
   - Personality traits evolve slowly over time
   - Major events cause significant shifts
   - Consistent patterns in events reinforce traits
   - Traits can change completely over NPC's lifetime
   - Recent events have more weight than old events

### Random Events

Random events provide variety and unpredictability to NPC lives, creating opportunities for relationship changes and personality development.

#### 1. **Random Event Generation**
   - Random events are generated periodically (daily or weekly per NPC)
   - Event probability is affected by:
     - NPC's current location
     - NPC's relationships
     - NPC's personality traits
     - Building types nearby
     - Time of day/season
   - Events are marked with `is_random_event = TRUE`

#### 2. **Random Event Types**
   - **Discovery Events**: Found valuable item, discovered new location, learned something new
   - **Opportunity Events**: Job offer, chance encounter, invitation to event
   - **Accident Events**: Minor injury, lost item, mishap
   - **Social Events**: Unexpected meeting, chance conversation, shared experience
   - **Work Events**: Unexpected work opportunity, workplace incident, recognition

#### 3. **Random Event Impact**
   - Random events create relationship changes
   - Events involving multiple NPCs affect all participants
   - Events can trigger personality adjustments
   - Events create memorable moments in NPC's journal
   - Events can lead to new relationships or deepen existing ones

#### 4. **Player Influence on Random Events**
   - Player actions can affect random event probability
   - Building certain structures increases event types (e.g., tavern increases social events)
   - Territory development affects event frequency
   - Player can trigger specific events through StoryTeller interface

---

**Note**: These workflows are subject to change during development. This document should be updated as workflows evolve and new features are added.

