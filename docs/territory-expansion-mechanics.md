# Territory Expansion Mechanics

## Table of Contents
- [Overview](#overview)
- [Territory Purchase System](#territory-purchase-system)
- [Beast Tide Defense](#beast-tide-defense)
- [Loyalty and Feral System](#loyalty-and-feral-system)
- [Contested Territories](#contested-territories)
- [Beast Incursions and Patrol](#beast-incursions-and-patrol)
- [Distance and Claim Limits](#distance-and-claim-limits)
- [Non-Contiguous Territories](#non-contiguous-territories)
- [Database Schema Updates](#database-schema-updates)

## Overview

Territory expansion is a core progression mechanic that allows players to claim new 1-2km territories beyond their starting territory. Expansion requires mana crystals, successful defense against beast tides, and ongoing maintenance through patrols and presence. Territories can become contested between players, and unmaintained territories will go feral and return to beast control.

**Key Principles:**
- **Expansion Costs**: Mana crystal cost that increases with each purchase
- **Claim-and-Hold**: Must successfully defend territory through beast tides to keep it
- **Local Presence**: Faction characters must be present to maintain loyalty
- **No Size Limit**: No cap on total territory size, but distance limited by ability to hold claims
- **Contested Claims**: Multiple players can claim the same territory, leading to conflict
- **Constant Threats**: Beast incursions force active patrol and defense

---

## Territory Purchase System

### Purchase Requirements

**Cost Formula:**
```
Base Cost = 100 mana_crystal_low
Cost Multiplier = 1.15 ^ (number_of_owned_territories - 1)
Total Cost = Base Cost × Cost Multiplier
```

**Example Costs:**
- First territory expansion (2nd territory): 100 × 1.15^1 = 115 mana crystals
- Second expansion (3rd territory): 100 × 1.15^2 = 132 mana crystals
- Third expansion (4th territory): 100 × 1.15^3 = 152 mana crystals
- Tenth expansion (11th territory): 100 × 1.15^10 = 405 mana crystals

**Additional Costs:**
- **Distance Penalty**: +5% cost per 10km distance from nearest owned territory (for non-contiguous)
- **Terrain Modifier**: 
  - Hills/Mountains: +20% cost (strategic value)
  - Plains: Base cost
  - Coastal: +10% cost
  - Forest: +5% cost

**Final Cost:**
```
Final Cost = Base Cost × Cost Multiplier × (1 + Distance_Penalty) × (1 + Terrain_Modifier)
```

### Purchase Process

1. **Player Initiates Purchase**
   - Player selects available 1-2km territory (adjacent or non-contiguous)
   - System calculates cost based on owned territories and distance
   - Player must have sufficient mana crystals in inventory

2. **Payment**
   - Mana crystals deducted from player's inventory
   - Cost is non-refundable (even if territory is lost)

3. **Territory Claim**
   - Territory status changes to `claimed` (but not yet `secured`)
   - Territory loyalty starts at 50% (newly claimed)
   - Beast tide defense phase begins

4. **Beast Tide Defense** (see below)
   - Player must successfully defend through beast tides
   - If defense fails, territory is lost (no refund)

5. **Securing Territory**
   - After successful beast tide defense, territory becomes `secured`
   - Territory loyalty increases to 75%
   - Player gains full control of territory

---

## Beast Tide Defense

### Beast Tide Triggers

After purchasing a territory, the player must defend against a series of beast tides:

**Beast Tide Count:**
```
Base Beast Tides = 2 + floor(territory_size_km² / 2)
Improvement Rate Modifier = improvement_rate × 0.5
Total Beast Tides = Base Beast Tides + floor(Improvement Rate Modifier)
```

**Improvement Rate:**
- Measured by buildings constructed per day in the territory
- Higher improvement rate = more beast tides (beasts are drawn to development)

**Example:**
- 1km² territory, low improvement (1 building/day): 2 + 0 = 2 beast tides
- 2km² territory, medium improvement (5 buildings/day): 2 + 1 + 2 = 5 beast tides
- 1km² territory, high improvement (10 buildings/day): 2 + 0 + 5 = 7 beast tides

### Beast Tide Mechanics

**Beast Tide Timing (Normal Purchase):**
- First beast tide: 1 hour after purchase
- Subsequent tides: 2-4 hours apart (randomized)
- All tides must be completed within 24 hours of purchase

**Beast Tide Timing (Contested Territory):**
- Continuous beast tide begins immediately when territory becomes contested
- New waves spawn every 30-60 minutes (randomized)
- Beast tide continues until contestation is resolved
- Final wave spawns 1 hour after control is secured

**Beast Tide Strength:**
- Each tide spawns 3-8 beast groups (depending on territory size)
- Beast groups appear at random points along territory perimeter
- Beast groups move toward territory center or nearest buildings
- Beast groups are level-appropriate for the player's cultivation level

**Beast Tide Types (Normal Purchase):**
- **Small Tide**: 3-5 groups, weak beasts (common)
- **Medium Tide**: 5-7 groups, moderate beasts (common)
- **Large Tide**: 7-10 groups, strong beasts (rare, 10% chance)

**Beast Tide Types (Contested Territory):**
- **Continuous Wave**: 5-10 groups per wave, beasts are level +2 to player's cultivation level
- Wave size increases with number of contesting players (+1-2 groups per additional player)
- All waves are "Large Tide" equivalent in strength
- No variation in difficulty (always challenging)

**Defense Requirements:**
- Player must defeat or repel all beast groups in each tide
- If any building is destroyed, defense is considered "failed" for that tide
- If 3+ consecutive tides fail, territory is lost
- If all tides succeed, territory becomes secured

**Defense Failure:**
- Territory loyalty drops by 20% per failed tide
- If loyalty reaches 0%, territory is lost
- Lost territory returns to `unclaimed` status
- No refund of mana crystals

---

## Loyalty and Feral System

### Loyalty Mechanics

**Loyalty Range:** 0-100%

**Loyalty States:**
- **100%**: Fully loyal, maximum benefits
- **75-99%**: Secure, normal operation
- **50-74%**: Unstable, reduced benefits
- **25-49%**: Rebellious, frequent issues
- **1-24%**: Feral, returning to beast control
- **0%**: Lost, returns to unclaimed

### Loyalty Decay

**Presence Requirement:**
- Territory requires at least one faction character (avatar or NPC) present
- Presence is checked every 5 minutes
- If no faction character present, loyalty decays

**Loyalty Decay Rate:**
```
Base Decay = 1% per hour
Distance Modifier = distance_from_nearest_owned_territory_km / 10 (max 5x)
Loyalty Decay = Base Decay × (1 + Distance_Modifier)
```

**Example:**
- Territory 5km away: 1% × 1.5 = 1.5% per hour
- Territory 20km away: 1% × 3.0 = 3% per hour
- Territory 50km+ away: 1% × 6.0 = 6% per hour (capped)

**Loyalty Recovery:**
- Faction character present: +2% per hour (up to 100%)
- Buildings constructed: +5% per building
- Successful beast tide defense: +10%
- Successful patrol: +1% per patrol

### Feral Territory

**Becoming Feral:**
- When loyalty drops below 25%, territory enters "feral" state
- Feral territories spawn hostile beasts
- Buildings in feral territories stop functioning
- NPCs may flee or become hostile

**Recovering Feral Territory:**
- Requires faction character presence
- Must clear all hostile beasts
- Must restore loyalty to 50%+ to exit feral state
- Recovery takes 2-4 hours of active presence

**Losing Territory:**
- If loyalty reaches 0%, territory is lost
- Territory returns to `unclaimed` status
- All buildings become neutral/abandoned
- Territory can be claimed by any player (including original owner)

---

## Contested Territories

### Contested Territory Mechanics

**Contestation:**
- Multiple players can claim the same 1-2km territory
- Both players can place units and buildings
- Both players can attempt to secure the territory
- Territory remains contested until one player secures control
- **Contested territories spawn continuous beast tides** - making them extremely dangerous

**Contestation Triggers:**
- Player A claims territory
- Player B (neighboring sect) claims same territory within 24 hours
- Territory enters "contested" state
- Continuous beast tide begins immediately

### Continuous Beast Tide in Contested Territories

**Beast Tide Mechanics:**
- When territory becomes contested (2+ players), a **continuous beast tide begins**
- Beast tide spawns new waves every 30-60 minutes (randomized)
- Each wave spawns 5-10 beast groups at territory perimeter
- Beast groups are stronger than normal (level +2 to player's cultivation level)
- Beast tide continues until contestation is resolved

**Beast Tide Intensity:**
- Base wave size: 5-8 beast groups
- Additional modifier: +1-2 groups per contesting player beyond the first
- Example: 2 players = 5-8 groups, 3 players = 6-10 groups, 4 players = 7-12 groups
- Beast groups prioritize attacking buildings and units of all players
- Beast groups may also attack each other, but primarily target player structures

**Beast Tide Effects:**
- All players in contested territory face constant beast attacks
- Buildings are constantly at risk
- Units must defend against both beasts and opposing players
- Makes contested territories extremely dangerous and resource-intensive
- Forces players to either cooperate temporarily or rapidly resolve the conflict

**Beast Tide End:**
- Beast tide ends when contestation is resolved (one player secures control)
- After securing control, player must survive final beast wave
- Final wave spawns 1 hour after control is secured
- After final wave is defeated, territory becomes fully secured

### Contested Territory Rules

**Unit Placement:**
- Both players can place units in contested territory
- Units can attack each other
- Buildings can be attacked by opposing player's units
- Buildings can be attacked by beast tide groups
- No restrictions on building placement (but can be destroyed by beasts or players)

**Interference:**
- Players can sabotage each other's buildings
- Players can attack each other's units
- Players can disrupt each other's beast tide defenses
- Players can interfere with each other's patrols
- Players can use beast attacks to their advantage (lure beasts toward opponent)

**Securing Control:**
- Player must push opposing player's units out of territory
- Player must maintain control for 6 hours **while surviving continuous beast tide**
- Control means: no opposing player units present, all opposing buildings destroyed or abandoned
- During control period, player must successfully defend against beast tide waves
- If player fails to defend against beast tide during control period, control resets
- After 6 hours of control + successful beast tide defense, territory becomes secured for controlling player
- Opposing player's claim is invalidated

**Contestation Resolution:**
- If contestation lasts 72 hours without resolution, territory becomes "neutral"
- Neutral territory returns to unclaimed status
- Both players lose their claim (no refund)
- Beast tide ends when territory becomes neutral
- Territory can be claimed again by any player

**Strategic Considerations:**
- Contested territories are extremely dangerous due to continuous beast tides
- Players must balance fighting opponents and defending against beasts
- Temporary cooperation may be necessary to survive beast tides
- Early resolution of conflict is crucial (longer conflict = more resources lost)
- Players may choose to abandon contested territory rather than fight in dangerous conditions

---

## Beast Incursions and Patrol

### Constant Beast Incursions

**Incursion Mechanics:**
- Beasts constantly attempt to enter territory from perimeter
- Incursion rate: 1-3 incursion attempts per hour (randomized)
- Incursion size: 1-3 beast groups per attempt
- Incursions spawn at random points along territory perimeter

**Beast Group Behavior:**
- Beast groups move toward territory center
- Beast groups attack buildings and units
- Beast groups avoid areas with active patrols
- Beast groups are attracted to qi sources and cultivation areas

### Patrol System

**Patrol Requirements:**
- Players must maintain patrols to defend territory perimeter
- Patrols reduce incursion success rate
- Patrols provide early warning of incursions
- Patrols increase territory loyalty (+1% per successful patrol)

**Patrol Mechanics:**
- Player assigns units (NPCs or avatar) to patrol routes
- Patrol routes cover territory perimeter
- Patrols detect and engage beast incursions
- Successful patrols: Defeat or repel all beast groups
- Failed patrols: Beast groups enter territory

**Patrol Effectiveness:**
- **No Patrol**: 100% incursion success rate
- **Light Patrol** (1-2 units): 50% incursion success rate
- **Medium Patrol** (3-5 units): 25% incursion success rate
- **Heavy Patrol** (6+ units): 10% incursion success rate

**Patrol Routes:**
- Player defines patrol routes along territory perimeter
- Routes can be customized (waypoints, coverage areas)
- Units assigned to routes will patrol automatically
- Patrols can be interrupted by combat or other tasks

**Patrol Rewards:**
- Successful patrols: +1% loyalty, +experience for patrolling units
- Failed patrols: -2% loyalty, potential damage to buildings

---

## Distance and Claim Limits

### No Size Limit

**Territory Size:**
- No maximum limit on total territory size
- Players can own unlimited territories
- Distance is the limiting factor (ability to hold claims)

### Distance Limits

**Effective Control Distance:**
- Maximum distance from nearest owned territory: 50km (base)
- Distance limit increases with cultivation level: +5km per cultivation tier
- Distance limit increases with buildings: +1km per 10 buildings in territory
- Distance limit increases with NPCs: +0.5km per NPC assigned to territory

**Distance Calculation:**
```
Max Distance = 50 + (cultivation_level × 5) + (buildings / 10) + (npcs × 0.5)
```

**Distance Penalties:**
- Territories beyond effective control distance:
  - Loyalty decay increases exponentially
  - Patrol effectiveness decreases
  - Beast incursion rate increases
  - Building efficiency decreases

**Practical Limit:**
- Most players can effectively control territories within 100-150km
- High-tier cultivators (Tier 20+) can control territories 200km+
- Territories beyond effective control are difficult to maintain

---

## Non-Contiguous Territories

### Non-Contiguous Purchase

**Mechanics:**
- Players can purchase territories that are not adjacent to existing territories
- Useful for strategic positions (hills, defensive structures)
- Non-contiguous territories have higher maintenance costs

**Cost Modifier:**
- Distance penalty: +5% per 10km from nearest owned territory
- Non-contiguous penalty: +50% base cost
- Total: Base cost × 1.5 × (1 + distance_penalty)

**Benefits:**
- Strategic positioning (hills for defensive structures)
- Resource access (ore deposits, qi sources)
- Forward bases for expansion
- Distraction for opponents

**Drawbacks:**
- Higher loyalty decay (distance penalty)
- More difficult to patrol (isolated)
- Higher maintenance costs
- More vulnerable to attacks

**Maintenance:**
- Non-contiguous territories require more active management
- Higher loyalty decay rates
- May require dedicated NPCs for patrol
- May need defensive structures to maintain

---

## Territory Benefits

### Expansion Benefits

**Resource Access:**
- More resource nodes
- Additional qi sources (veins or wells)
- Strategic terrain features

**Building Space:**
- More area for buildings
- Better terrain for specific building types
- Room for district formation

**Strategic Value:**
- Defensive positions (hills, chokepoints)
- Resource control (ore deposits, qi sources)
- Expansion routes
- Territory control (blocking opponents)

**Qi Enrichment:**
- More territory = more potential for qi enrichment
- Additional qi sources increase enrichment capacity
- Larger territories allow for more enriching buildings

### Diminishing Returns

**Management Complexity:**
- More territories = more management overhead
- Each territory requires patrols and presence
- Loyalty management becomes more difficult
- Building maintenance increases

**Cost Scaling:**
- Each territory purchase is more expensive
- Maintenance costs increase
- Patrol requirements increase

**Practical Limits:**
- Most players effectively manage 5-10 territories
- High-tier cultivators can manage 15-20 territories
- Beyond that, territories become difficult to maintain

---

## Database Schema Updates

### Updates to `territories` Table

Add the following fields:
```sql
-- Territory Ownership
claimed_by_avatar_id BIGINT REFERENCES avatars(id), -- Player who claimed this territory
claimed_at TIMESTAMP WITH TIME ZONE, -- When territory was claimed
secured_at TIMESTAMP WITH TIME ZONE, -- When territory was secured (after beast tides)
claim_status VARCHAR(50) DEFAULT 'unclaimed', -- 'unclaimed', 'claimed', 'contested', 'secured', 'feral', 'lost'

-- Territory Loyalty
loyalty REAL DEFAULT 0.0, -- 0.0 to 100.0, territory loyalty percentage
last_faction_presence_at TIMESTAMP WITH TIME ZONE, -- Last time a faction character was present
loyalty_decay_rate REAL DEFAULT 1.0, -- Loyalty decay per hour (affected by distance)

-- Beast Tide Defense
beast_tide_count INTEGER DEFAULT 0, -- Number of beast tides required
beast_tide_completed INTEGER DEFAULT 0, -- Number of beast tides completed
beast_tide_failures INTEGER DEFAULT 0, -- Number of failed beast tides
next_beast_tide_at TIMESTAMP WITH TIME ZONE, -- When next beast tide occurs

-- Contested Territory
contested_by_avatar_ids BIGINT[], -- Array of avatar IDs contesting this territory
contested_since TIMESTAMP WITH TIME ZONE, -- When contestation began
controlling_avatar_id BIGINT REFERENCES avatars(id), -- Current controlling player
control_started_at TIMESTAMP WITH TIME ZONE, -- When current control began

-- Territory Purchase
purchase_cost_mana_crystals INTEGER, -- Mana crystals spent to purchase
purchase_cost_territory_number INTEGER, -- Which territory number this was (for cost scaling)

-- Distance and Limits
distance_from_nearest_owned_km REAL, -- Distance from nearest owned territory
is_contiguous BOOLEAN DEFAULT TRUE, -- Whether territory is contiguous with owned territories
```

### New Table: `territory_patrols`

```sql
CREATE TABLE territory_patrols (
    id BIGSERIAL PRIMARY KEY,
    territory_id BIGINT NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    patrol_route JSONB NOT NULL, -- Route waypoints: [{"x": 100, "y": 200}, ...]
    assigned_unit_type VARCHAR(20) NOT NULL, -- 'avatar', 'npc'
    assigned_unit_id BIGINT NOT NULL, -- Unit ID
    patrol_status VARCHAR(50) DEFAULT 'active', -- 'active', 'paused', 'completed', 'interrupted'
    last_patrol_at TIMESTAMP WITH TIME ZONE, -- Last successful patrol completion
    incursions_encountered INTEGER DEFAULT 0, -- Number of incursions encountered
    incursions_defeated INTEGER DEFAULT 0, -- Number of incursions successfully defeated
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_territory_patrols_territory_id (territory_id),
    INDEX idx_territory_patrols_unit (assigned_unit_type, assigned_unit_id),
    INDEX idx_territory_patrols_status (patrol_status)
);
```

### New Table: `beast_incursions`

```sql
CREATE TABLE beast_incursions (
    id BIGSERIAL PRIMARY KEY,
    territory_id BIGINT NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    incursion_type VARCHAR(50) NOT NULL, -- 'tide', 'regular', 'large'
    spawn_x BIGINT NOT NULL, -- Spawn location X
    spawn_y BIGINT NOT NULL, -- Spawn location Y
    beast_group_count INTEGER NOT NULL, -- Number of beast groups
    beast_group_data JSONB NOT NULL, -- Beast group details: [{"type": "wolf", "count": 5, "level": 3}, ...]
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'defeated', 'entered_territory', 'expired'
    detected_by_patrol_id BIGINT REFERENCES territory_patrols(id), -- Which patrol detected it
    defeated_at TIMESTAMP WITH TIME ZONE, -- When incursion was defeated
    entered_territory_at TIMESTAMP WITH TIME ZONE, -- When beasts entered territory (if not defeated)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_beast_incursions_territory_id (territory_id),
    INDEX idx_beast_incursions_status (status),
    INDEX idx_beast_incursions_created_at (created_at)
);
```

### New Table: `territory_contests`

```sql
CREATE TABLE territory_contests (
    id BIGSERIAL PRIMARY KEY,
    territory_id BIGINT NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    contesting_avatar_id BIGINT NOT NULL REFERENCES avatars(id),
    contest_started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    contest_status VARCHAR(50) DEFAULT 'active', -- 'active', 'resolved', 'neutralized'
    resolved_at TIMESTAMP WITH TIME ZONE, -- When contest was resolved
    winner_avatar_id BIGINT REFERENCES avatars(id), -- Winner (if resolved)
    control_duration_hours REAL DEFAULT 0.0, -- Hours of continuous control by current controller
    
    UNIQUE(territory_id, contesting_avatar_id),
    INDEX idx_territory_contests_territory_id (territory_id),
    INDEX idx_territory_contests_avatar_id (contesting_avatar_id),
    INDEX idx_territory_contests_status (contest_status)
);
```

---

## Summary

The territory expansion system provides:
- **Progressive Costs**: Each expansion is more expensive (mana crystal cost scaling)
- **Risk and Reward**: Must defend through beast tides to secure territory
- **Active Maintenance**: Constant patrols and presence required to maintain loyalty
- **Strategic Depth**: Non-contiguous territories, contested claims, distance management
- **No Artificial Limits**: No size cap, but practical limits based on ability to maintain
- **Constant Threats**: Beast incursions force active defense and engagement

The system emphasizes active gameplay and strategic decision-making, requiring players to balance expansion with maintenance capabilities.

---

**Last Updated:** 2025-11-05

