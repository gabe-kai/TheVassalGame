# Documentation Gaps Analysis

**Date:** 2025-11-05  
**Purpose:** Comprehensive analysis of documentation gaps and consistency issues  
**Status:** Active review and prioritization

## Summary

This document catalogs documentation gaps, API endpoint gaps, database schema inconsistencies, and missing mechanics that need to be addressed before or during implementation. Systems are categorized by priority based on their importance to core gameplay and implementation timeline.

**Completed Core Systems:**
- ✅ Qi/Mana Generation & Refinement (`docs/qi-mana-mechanics.md`)
- ✅ Cultivation System & Tribulations (`docs/cultivation-mechanics.md`)
- ✅ Production Rate Calculations (`docs/production-mechanics.md`)
- ✅ Victory Conditions & Planetary Core (`docs/workflows.md` - Victory Conditions section)
- ✅ Combat System (`docs/combat-mechanics.md`)
- ✅ Territory Expansion Mechanics (`docs/territory-expansion-mechanics.md`)
- ✅ Database Schema (`docs/database-schema.md`)
- ✅ API Specification (`docs/api-specification.md`)
- ✅ Building Types, Resources, Skills, Species, Techniques References

---

## CRITICAL ISSUES - API & Database Consistency

These issues must be fixed before implementation begins.

### 1. **Territory Expansion API Endpoints** ✅ COMPLETED

**Current State:**
- ✅ Territory expansion mechanics documented in `docs/territory-expansion-mechanics.md`
- ✅ Database schema updated with territory expansion fields
- ✅ API endpoints updated and expanded

**Completed:**
- ✅ **Territory Purchase:**
  - `POST /avatars/{avatar_id}/purchase-territory` - Purchase new territory (with mana crystal cost)
  - `GET /avatars/{avatar_id}/territories` - List all owned territories
  - `GET /territories/{territory_id}` - Get territory details

- ✅ **Beast Tide Defense:**
  - `GET /territories/{territory_id}/beast-tides` - Get beast tide status and upcoming tides
  - `GET /territories/{territory_id}/beast-tides/{tide_id}` - Get specific beast tide details
  - `POST /territories/{territory_id}/beast-tides/{tide_id}/defend` - Report defense outcome

- ✅ **Patrol Management:**
  - `GET /territories/{territory_id}/patrols` - List all patrols for territory
  - `POST /territories/{territory_id}/patrols` - Create new patrol route
  - `PUT /territories/{territory_id}/patrols/{patrol_id}` - Update patrol route
  - `DELETE /territories/{territory_id}/patrols/{patrol_id}` - Delete patrol
  - `POST /territories/{territory_id}/patrols/{patrol_id}/assign-unit` - Assign unit to patrol

- ✅ **Beast Incursions:**
  - `GET /territories/{territory_id}/incursions` - List active/past incursions
  - `GET /territories/{territory_id}/incursions/{incursion_id}` - Get incursion details

- ✅ **Contested Territories:**
  - `GET /territories/{territory_id}/contest` - Get contest status
  - `POST /territories/{territory_id}/contest/claim` - Claim contested territory
  - `GET /territories/{territory_id}/contest/control` - Get current control status

- ✅ **Territory Loyalty:**
  - `GET /territories/{territory_id}/loyalty` - Get loyalty status and decay rate
  - `GET /territories/{territory_id}/presence` - Check faction character presence

**Documentation:**
- ✅ `docs/api-specification.md` - Updated with all territory expansion endpoints

**Priority:** ✅ **COMPLETED**

---

## HIGH PRIORITY - Core Gameplay Systems

These systems are essential for basic gameplay and should be documented before implementation begins.

### 2. **NPC AI & Behavior System** ✅ COMPLETED

**Current State:**
- ✅ NPC AI & Behavior system fully documented in `docs/npc-ai-behavior.md`
- ✅ NPC relationships and events system documented (`docs/workflows.md`)
- ✅ Personality traits system defined (derived from events)
- ✅ NPC types defined (workers, guards, traders, citizens)
- ✅ NPC character sheet stats defined
- ✅ NPC database schema complete

**Completed:**
- ✅ **NPC Decision-Making:**
  - Weighted priority system based on needs, personality, relationships, skills
  - Job selection algorithm with skill matching and personality fit
  - Pathfinding and destination selection
  - Relationship-based decision modifiers
  - Personality trait influence on all decisions

- ✅ **NPC State Machine:**
  - 10 core states defined (Idle, Working, Moving, Fighting, Resting, Socializing, Eating, Training, Patrolling, Seeking)
  - State transition logic with priority system
  - Personality influence on state transitions
  - Emergency state handling

- ✅ **NPC Behavior Trees:**
  - Behavior trees for Workers, Guards, Traders, Citizens
  - Emergency response behaviors
  - Need-driven behavior selection
  - Personality-driven behavior variations

- ✅ **NPC Job System:**
  - Auto-assignment algorithm with skill matching
  - Manual assignment support
  - Job satisfaction calculation (pay, skills, coworkers, location, advancement)
  - Job change triggers and decision-making
  - NPC job application system

- ✅ **NPC Social System:**
  - Relationship formation (proximity, events, compatibility)
  - Relationship maintenance (interactions, gifts, conflicts)
  - Relationship types (Friendship, Acquaintance, Rivalry, Enmity)
  - Personality trait influence on social interactions

- ✅ **NPC Needs & Wants:**
  - Core needs defined (Hunger, Rest/Stamina, Social, Safety, Work Satisfaction, Autonomy)
  - Need priority calculation with personality modifiers
  - Need-driven behavior selection

- ✅ **Event Response System:**
  - Event detection and importance calculation
  - Personality-based response selection
  - Event response priority system

- ✅ **NPC Learning & Adaptation:**
  - Skill progression formulas
  - Preference learning (jobs, locations, social)
  - Adaptation to territory and relationship changes
  - Personality evolution over time

- ✅ **Emergency Response:**
  - Emergency detection and classification
  - Response types (Combat, Building Defense, Territory Defense, Evacuation)
  - Priority system with personality influence

- ✅ **Player Interaction:**
  - Player order system with acceptance algorithm
  - Player request system
  - NPC conversation system
  - Order resistance based on ego, loyalty, personality

**Documentation:**
- ✅ `docs/npc-ai-behavior.md` - Complete NPC AI & Behavior system documentation

**Priority:** ✅ **COMPLETED**

---

## MEDIUM PRIORITY - Important Systems

These systems are important but can be refined during implementation.

### 3. **Resource Node Mechanics** 🟡 MEDIUM PRIORITY

**Current State:**
- ✅ Resource gathering workflow exists in `docs/workflows.md`
- ✅ Resource nodes mentioned in territory generation
- ✅ Node depletion/respawn mentioned
- ✅ Resource types defined in `docs/resources-reference.md`
- ✅ `resource_nodes` table exists in database schema

**Missing Details:**
- **Node Spawning:**
  - How are resource nodes placed during territory generation?
  - What types of nodes exist? (Trees, ore veins, herb patches, qi sources, etc.)
  - How many nodes per territory? (Density, distribution)
  - Are nodes randomly placed or strategic? (Biome-based, terrain-based)
  - Do nodes have quality/richness levels?

- **Node Depletion & Respawn:**
  - How fast do nodes deplete? (Based on gathering rate, node size)
  - What's the respawn rate? (Time-based, condition-based)
  - Do nodes respawn in the same location?
  - Do nodes respawn at the same quality/richness?
  - Can nodes be permanently depleted?
  - Are there respawn conditions? (Time, qi level, cultivation)

- **Node Types & Properties:**
  - What resource nodes exist? (Complete list)
  - What are their properties? (Yield, respawn time, quality tiers)
  - How do players discover nodes? (Exploration, scouting, skills)
  - Can nodes be improved? (Cultivation, enrichment, cultivation level)
  - Do nodes have special requirements? (Tools, skills, cultivation level)

- **Node Interaction:**
  - How do NPCs gather from nodes?
  - How do players gather from nodes?
  - Can nodes be claimed/owned?
  - Can nodes be contested between players?

**Recommended Documentation:**
- Add section to `docs/workflows.md`: "Resource Node Mechanics" or create `docs/resource-nodes.md`:
  - Complete node types and properties
  - Spawning algorithms
  - Depletion and respawn mechanics
  - Node discovery system
  - Node interaction mechanics

**Priority:** 🟡 **MEDIUM** - Important but can be refined during implementation

---

### 4. **Building Placement Rules** 🟡 MEDIUM PRIORITY

**Current State:**
- ✅ Building placement workflow exists in `docs/workflows.md`
- ✅ Building `footprint_polygon` defined in database schema
- ✅ Basic placement validation mentioned
- ✅ Building types and tiers documented
- ✅ Qi source influence mechanics documented in `docs/qi-mana-mechanics.md`

**Missing Details:**
- **Placement Constraints:**
  - Minimum distance between buildings? (Fire safety, aesthetics, gameplay)
  - Proximity to qi source requirements? (Some buildings require qi sources)
  - Terrain requirements? (Flat ground, elevation limits, water proximity)
  - Can buildings overlap? (Footprint validation)
  - Distance from territory boundaries? (Buffer zones)
  - Can buildings be placed on water? (Floating structures, piers)

- **Qi Source Influence:**
  - How does distance from qi source affect building effectiveness?
  - Are some buildings required to be near qi sources? (Which ones?)
  - What's the qi source radius/area of effect? (Linear, exponential decay?)
  - How does proximity affect qi absorption rates? (Formula from `docs/qi-mana-mechanics.md` exists, but placement rules need detail)
  - Can buildings be too close to qi sources? (Overload, instability)

- **Building Placement Validation:**
  - What makes a placement valid/invalid? (Complete validation rules)
  - What are the error messages? (User-friendly feedback)
  - Can players preview placement before confirming? (Ghost preview, validation indicators)
  - Can buildings be rotated? (Rotation constraints, footprint changes)
  - Are there elevation restrictions? (Slope limits, foundation requirements)

- **Building Placement Costs:**
  - Are there placement costs beyond construction costs? (Terrain modification, clearing)
  - Can terrain be modified for building placement? (Flattening, elevation changes)
  - What are the costs of terrain modification?

**Recommended Documentation:**
- Expand "Building Placement Workflow" in `docs/workflows.md`:
  - Complete placement rules and constraints
  - Qi source influence mechanics (detailed)
  - Placement validation rules
  - Terrain modification mechanics
  - Error handling and user feedback

**Priority:** 🟡 **MEDIUM** - Important for gameplay but can be refined during implementation

---

### 5. **Trade & Economy Mechanics** 🟡 MEDIUM PRIORITY

**Current State:**
- ✅ Trade workflow exists in `docs/workflows.md` (high-level)
- ✅ Market system mentioned in architecture
- ✅ Trade tables exist in database schema (`trades`, `trade_history`, `market_prices`)
- ✅ Basic trade flow described (offer → discovery → acceptance)

**Missing Details:**
- **Pricing Mechanics:**
  - How are prices determined? (Base values, supply/demand, market dynamics)
  - Supply and demand calculations? (How do they affect prices?)
  - Market price fluctuations? (Volatility, trends, events)
  - Regional price differences? (Distance, scarcity, local supply/demand)
  - How do NPCs price goods? (Markup, profit margins, negotiation)

- **NPC Traders:**
  - How do NPCs participate in trade? (Merchants, caravans, markets)
  - Do NPCs have their own trade offers? (Selling, buying, bartering)
  - How do NPCs price goods? (Intelligence, market awareness, profit goals)
  - How do NPCs react to market conditions? (Price adjustments, stock management)
  - Can NPCs form trade routes?

- **Trade Routes:**
  - How do trade routes work? (Established paths, distance, safety)
  - What's the cost of transporting goods? (Time, resources, risk)
  - How does distance affect trade? (Transport costs, time delays)
  - Can trade routes be attacked/raided?
  - Can players establish trade routes?

- **Market Dynamics:**
  - How does the market evolve? (Player actions, NPC actions, events)
  - Are there market events? (Scarcity, abundance, disruptions)
  - How do market crashes/booms work?
  - Can players influence markets? (Market manipulation, cornering markets)

**Recommended Documentation:**
- Expand "Trading Flow" in `docs/workflows.md` or create `docs/economy-mechanics.md`:
  - Complete pricing mechanics and formulas
  - Market dynamics and supply/demand
  - NPC trader behavior
  - Trade route mechanics
  - Market events and player influence

**Priority:** 🟡 **MEDIUM** - Important for economy but can be refined during implementation

---

## LOW PRIORITY - Advanced Features

These systems are end-game or advanced features that can be documented later.

### 6. **Formation/Array Mechanics** 🟢 LOW PRIORITY

**Current State:**
- Buildings reference "formations" and "arrays" (mentioned in lore/descriptions)
- Resources include "Formation-grade Stone" (in `docs/resources-reference.md`)
- Inscription skill mentioned (in `docs/skills-reference.md`)
- No mechanics defined

**Missing Details:**
- **What are Formations?**
  - What do formations do? (Defensive, offensive, utility, qi manipulation)
  - How are they created? (Inscription skill, resources, placement)
  - What resources are required? (Formation-grade materials, qi crystals, etc.)
  - How do formations affect gameplay? (Building protection, territory defense, qi manipulation)
  - Can formations be upgraded? (Tiers, complexity)

- **Formation Types:**
  - What types of formations exist? (Defensive arrays, offensive arrays, qi gathering, protection, etc.)
  - What are their effects? (Damage reduction, attack bonuses, qi absorption, etc.)
  - How do formations interact with buildings? (Placement, activation, maintenance)
  - Can formations be combined? (Array networks, compound formations)

- **Array Mechanics:**
  - What are arrays? (Larger formations, multi-building systems)
  - How do arrays differ from formations? (Scale, complexity, effects)
  - How are arrays constructed? (Multiple formations, coordination)
  - What are array networks? (Interconnected formations)

**Recommended Documentation:**
- Create `docs/formation-mechanics.md` with:
  - Formation types and effects
  - Construction requirements
  - Array mechanics
  - Formation networks

**Priority:** 🟢 **LOW** - Advanced feature, can be documented later

---

### 7. **Planet Core Upgrade Mechanics** 🟢 LOW PRIORITY

**Current State:**
- ✅ Victory conditions section in `docs/workflows.md` describes planetary core system
- ✅ Planetary core levels defined (1-7, with level 5+ unlocking dimensional portal)
- ✅ Qi enrichment contribution mechanics documented
- ✅ Core leveling thresholds mentioned
- ✅ Database schema has `core_property` and `core_value` fields

**Missing Details:**
- **Core Properties:**
  - What are `core_property` and `core_value`? (Not documented)
  - What properties can cores have? (Different types, specializations)
  - How do core properties affect gameplay?
  - How are core properties determined? (Random, planet-specific, player choice)

- **Core Upgrade Process:**
  - Detailed upgrade stages beyond levels 1-7? (Sub-levels, milestones)
  - What are the exact costs per upgrade? (Qi enrichment thresholds - partially documented)
  - What are the benefits of upgrading? (Detailed effects per level - partially documented)
  - Are there upgrade prerequisites? (Beyond qi enrichment)
  - Can upgrades be triggered manually? (Admin, player actions)

**Recommended Documentation:**
- Expand "Victory Conditions and Planetary Core System" in `docs/workflows.md`:
  - Core properties and specializations
  - Detailed upgrade stages and costs
  - Core effects on gameplay

**Priority:** 🟢 **LOW** - End-game feature, basic mechanics documented

---

### 8. **Dimensional Portal Mechanics** 🟢 LOW PRIORITY

**Current State:**
- ✅ Victory conditions section in `docs/workflows.md` describes dimensional portal
- ✅ Portal activation tied to planetary core level 5
- ✅ Portal capacity and upgrade mechanics mentioned
- ✅ Portal hosting mechanics documented (winner's city becomes capital)

**Missing Details:**
- **Portal Requirements:**
  - Exact refined mana requirements? (Beyond "enough")
  - Are there other requirements? (Building construction, resources, cultivator level)
  - How is the portal activated? (Construction process, activation ceremony)
  - Can portal activation fail? (Conditions, requirements)

- **Portal Effects:**
  - What exactly happens when the portal is activated? (Detailed mechanics)
  - Do colonists arrive? (How many, how often, what types)
  - How does this affect gameplay? (New resources, NPCs, buildings, quests)
  - What happens to the winning player? (Ruler status, benefits, responsibilities)
  - What happens to other players? (Continue playing, new objectives)

- **Portal Operations:**
  - How does the portal operate? (Daily operations, maintenance)
  - What are the portal's capabilities? (Transport capacity, range, destinations)
  - Can the portal be upgraded? (Beyond initial capacity)
  - Are there portal events? (Arrivals, departures, special transports)

**Recommended Documentation:**
- Expand "Dimensional Portal Mechanics" in `docs/workflows.md`:
  - Detailed activation requirements and process
  - Portal effects and gameplay changes
  - Portal operations and maintenance
  - Post-victory gameplay mechanics

**Priority:** 🟢 **LOW** - End-game feature, basic mechanics documented

---

## Documentation Priority Recommendations

### Phase 1 (Before Implementation - Critical):
1. ✅ **Territory Expansion API Endpoints** - ✅ COMPLETED
2. ✅ **NPC AI & Behavior System** - ✅ COMPLETED

### Phase 2 (Early Implementation - Important):
3. 🟡 **Resource Node Mechanics** - Important for resource gathering
4. 🟡 **Building Placement Rules** - Important for gameplay
5. 🟡 **Trade & Economy Mechanics** - Important for economy

### Phase 3 (Later Implementation - Advanced):
6. 🟢 **Formation/Array Mechanics** - Advanced feature
7. 🟢 **Planet Core Upgrade Mechanics** - End-game feature (basic mechanics exist)
8. 🟢 **Dimensional Portal Mechanics** - End-game feature (basic mechanics exist)

---

## Consistency Issues Found

### Database Schema vs API Specification

1. **Territory Expansion:**
   - ✅ Database schema has all required fields for territory expansion
   - ✅ API endpoint updated: `POST /avatars/{avatar_id}/purchase-territory` (replaces outdated expand-territory)
   - ✅ All API endpoints for beast tides, patrols, incursions, contested territories added

2. **Combat System:**
   - ✅ Database schema has all combat tables (techniques, weapons, armor, accessories)
   - ✅ API endpoints exist for techniques and equipment
   - ✅ All fields are properly exposed

3. **NPC System:**
   - ✅ Database schema has NPC relationships, events, personality traits, all states
   - ✅ API endpoints exist for NPC relationships, events, management, and behavior
   - ✅ All fields are properly exposed
   - ✅ NPC state field updated with all 10 states and CHECK constraint

### Documentation vs Implementation

1. **Territory Expansion Mechanics:**
   - ✅ Mechanics fully documented in `docs/territory-expansion-mechanics.md`
   - ✅ Database schema updated
   - ✅ API specification updated with all endpoints

2. **Combat System:**
   - ✅ Mechanics fully documented
   - ✅ Database schema complete
   - ✅ API endpoints complete

3. **Skills System:**
   - ✅ Skills reference complete
   - ✅ Database schema complete
   - ✅ API endpoints complete

---

## Next Steps

1. ✅ **Fix Critical API Issues**: ✅ COMPLETED - Territory expansion endpoints updated
2. ✅ **Document NPC AI**: ✅ COMPLETED - Comprehensive NPC behavior documentation created
3. ✅ **Review Consistency**: ✅ COMPLETED - All documentation aligned with database schema
4. ✅ **Update API Spec**: ✅ COMPLETED - All missing endpoints added
5. **Implementation Planning**: Use completed documentation to guide implementation
6. **Document Medium Priority Systems**: Resource Node Mechanics, Building Placement Rules, Trade & Economy Mechanics

---

**Last Updated:** 2025-11-05  
**Next Review:** After Phase 1 documentation is complete
