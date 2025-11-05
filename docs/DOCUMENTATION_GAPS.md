# Documentation Gaps Analysis

**Date:** 2025-01-21  
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
- ✅ NPC AI & Behavior System (`docs/npc-ai-behavior.md`)
- ✅ Resource Node Mechanics (`docs/resource-node-mechanics.md`)
- ✅ Building Placement Mechanics (`docs/building-placement-mechanics.md`)
- ✅ Database Schema (`docs/database-schema.md`)
- ✅ API Specification (`docs/api-specification.md`)
- ✅ Building Types, Resources, Skills, Species, Techniques References

---

## COMPLETED SYSTEMS

All critical and high-priority systems have been fully documented. These systems are ready for implementation.

### 1. **Territory Expansion API Endpoints** ✅ COMPLETED

**Status:** Fully documented with complete API endpoints and database schema.

**Documentation:**
- ✅ `docs/territory-expansion-mechanics.md` - Complete territory expansion mechanics
- ✅ `docs/api-specification.md` - All territory expansion endpoints
- ✅ `docs/database-schema.md` - Territory expansion tables and fields

**API Endpoints:**
- ✅ Territory Purchase: `POST /avatars/{avatar_id}/purchase-territory`, `GET /avatars/{avatar_id}/territories`, `GET /territories/{territory_id}`
- ✅ Beast Tide Defense: `GET /territories/{territory_id}/beast-tides`, `GET /territories/{territory_id}/beast-tides/{tide_id}`, `POST /territories/{territory_id}/beast-tides/{tide_id}/defend`
- ✅ Patrol Management: `GET /territories/{territory_id}/patrols`, `POST /territories/{territory_id}/patrols`, `PUT /territories/{territory_id}/patrols/{patrol_id}`, `DELETE /territories/{territory_id}/patrols/{patrol_id}`, `POST /territories/{territory_id}/patrols/{patrol_id}/assign-unit`
- ✅ Beast Incursions: `GET /territories/{territory_id}/incursions`, `GET /territories/{territory_id}/incursions/{incursion_id}`
- ✅ Contested Territories: `GET /territories/{territory_id}/contest`, `POST /territories/{territory_id}/contest/claim`, `GET /territories/{territory_id}/contest/control`
- ✅ Territory Loyalty: `GET /territories/{territory_id}/loyalty`, `GET /territories/{territory_id}/presence`

---

### 2. **NPC AI & Behavior System** ✅ COMPLETED

**Status:** Fully documented with comprehensive behavior system, decision-making, and social mechanics.

**Documentation:**
- ✅ `docs/npc-ai-behavior.md` - Complete NPC AI & Behavior system documentation
- ✅ `docs/workflows.md` - NPC relationships and events system
- ✅ `docs/database-schema.md` - NPC tables with all states and relationships
- ✅ `docs/api-specification.md` - NPC management endpoints

**Key Features:**
- ✅ 10-state state machine (Idle, Working, Moving, Fighting, Resting, Socializing, Eating, Training, Patrolling, Seeking)
- ✅ Weighted priority decision-making system
- ✅ Needs & wants system (Hunger, Rest/Stamina, Social, Safety, Work Satisfaction, Autonomy)
- ✅ Job assignment system (auto and manual)
- ✅ Relationship system (NPC-to-NPC, NPC-to-Building)
- ✅ Event journal and personality trait derivation
- ✅ Behavior trees for Workers, Guards, Traders, Citizens
- ✅ Emergency response system
- ✅ Player interaction system

---

### 3. **Resource Node Mechanics** ✅ COMPLETED

**Status:** Fully documented with complete gathering, depletion, and respawn mechanics.

**Documentation:**
- ✅ `docs/resource-node-mechanics.md` - Complete resource node mechanics documentation
- ✅ `docs/workflows.md` - Resource gathering workflow
- ✅ `docs/database-schema.md` - `resource_nodes` table
- ✅ `docs/resources-reference.md` - Resource types reference

**Key Features:**
- ✅ Node spawning (biome-based, 5-15 nodes per 1km² territory)
- ✅ Node types: Lumber, Stone Quarries, Iron Mines, Food Sources, Herb Patches, Qi Sources, Water Sources
- ✅ Depletion and respawn mechanics (varies by node type)
- ✅ Visual indicators (Lumber visually depletes, Stone/Iron don't, Food partial visual)
- ✅ Food source special mechanics (farmer skill affects yield, random events)
- ✅ Gathering mechanics (skill, tool, event modifiers)
- ✅ Node discovery (automatic in territories, exploration-based outside)

---

### 4. **Building Placement Mechanics** ✅ COMPLETED

**Status:** Fully documented with complete placement validation, terrain modification, and road generation.

**Documentation:**
- ✅ `docs/building-placement-mechanics.md` - Complete building placement mechanics documentation
- ✅ `docs/workflows.md` - Building placement workflow
- ✅ `docs/database-schema.md` - Building tables with `paths` and `terrain_modifications` tables
- ✅ `docs/api-specification.md` - Building placement and validation endpoints

**Key Features:**
- ✅ Polygonal footprint system (not just rectangles)
- ✅ Door accessibility validation (all doors must be accessible from paths/roads)
- ✅ Proximity bonuses for supply chain buildings (0-50m range, up to 25% bonus)
- ✅ Automatic road generation (Path → Rough Road → Road → Nice Road based on usage)
- ✅ Terrain modification system (flattening, elevation changes, structural supports)
- ✅ Building relocation system (deconstruction and reconstruction)
- ✅ Qi source proximity requirements (0-200m range, exponential decay)
- ✅ Complete placement validation (footprint, terrain, doors, resources, proximity)
- ✅ API endpoint: `POST /game/buildings/validate` for preview mode validation

**API Endpoints:**
- ✅ `POST /game/buildings` - Place building with terrain modification approval
- ✅ `POST /game/buildings/validate` - Validate placement before submitting
- ✅ `GET /game/buildings/{id}` - Get building details with terrain modifications and proximity bonuses
- ✅ `GET /game/buildings/{building_id}/paths` - Get paths/roads connected to building
- ✅ `GET /game/paths/{path_id}` - Get path details
- ✅ `GET /game/territories/{territory_id}/paths` - Get all paths in territory

---

## REMAINING DOCUMENTATION GAPS

### MEDIUM PRIORITY - Important Systems

These systems are important for gameplay but can be refined during implementation.

#### 5. **Trade & Economy Mechanics** 🟡 MEDIUM PRIORITY

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
- Create `docs/economy-mechanics.md`:
  - Complete pricing mechanics and formulas
  - Market dynamics and supply/demand
  - NPC trader behavior
  - Trade route mechanics
  - Market events and player influence

**Priority:** 🟡 **MEDIUM** - Important for economy but can be refined during implementation

---

### LOW PRIORITY - Advanced Features

These systems are end-game or advanced features that can be documented later.

#### 6. **Formation/Array Mechanics** 🟢 LOW PRIORITY

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

#### 7. **Planet Core Upgrade Mechanics** 🟢 LOW PRIORITY

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

#### 8. **Dimensional Portal Mechanics** 🟢 LOW PRIORITY

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

### Phase 1 (Before Implementation - Critical): ✅ COMPLETED
1. ✅ **Territory Expansion API Endpoints** - ✅ COMPLETED
2. ✅ **NPC AI & Behavior System** - ✅ COMPLETED

### Phase 2 (Early Implementation - Important): ✅ COMPLETED
3. ✅ **Resource Node Mechanics** - ✅ COMPLETED
4. ✅ **Building Placement Rules** - ✅ COMPLETED
5. 🟡 **Trade & Economy Mechanics** - Important for economy (can be refined during implementation)

### Phase 3 (Later Implementation - Advanced):
6. 🟢 **Formation/Array Mechanics** - Advanced feature
7. 🟢 **Planet Core Upgrade Mechanics** - End-game feature (basic mechanics exist)
8. 🟢 **Dimensional Portal Mechanics** - End-game feature (basic mechanics exist)

---

## Consistency Status

### Database Schema vs API Specification ✅ VERIFIED

All documented systems have been verified for consistency:

1. **Territory Expansion:**
   - ✅ Database schema has all required fields
   - ✅ API endpoints complete and consistent
   - ✅ All tables properly defined

2. **Combat System:**
   - ✅ Database schema has all combat tables (techniques, weapons, armor, accessories)
   - ✅ API endpoints exist for techniques and equipment
   - ✅ All fields are properly exposed

3. **NPC System:**
   - ✅ Database schema has NPC relationships, events, personality traits, all states
   - ✅ API endpoints exist for NPC relationships, events, management, and behavior
   - ✅ All fields are properly exposed
   - ✅ NPC state field updated with all 10 states and CHECK constraint

4. **Building Placement:**
   - ✅ Database schema has `paths` and `terrain_modifications` tables
   - ✅ API endpoints exist for building placement, validation, and paths
   - ✅ All fields are properly exposed

5. **Resource Nodes:**
   - ✅ Database schema has `resource_nodes` table
   - ✅ API endpoints exist for resource gathering
   - ✅ All fields are properly exposed

### Documentation vs Implementation ✅ VERIFIED

All documented mechanics have corresponding database schema and API endpoints:

1. **Territory Expansion Mechanics:**
   - ✅ Mechanics fully documented
   - ✅ Database schema complete
   - ✅ API specification complete

2. **Combat System:**
   - ✅ Mechanics fully documented
   - ✅ Database schema complete
   - ✅ API endpoints complete

3. **NPC AI & Behavior:**
   - ✅ Mechanics fully documented
   - ✅ Database schema complete
   - ✅ API endpoints complete

4. **Resource Node Mechanics:**
   - ✅ Mechanics fully documented
   - ✅ Database schema complete
   - ✅ API endpoints complete

5. **Building Placement Mechanics:**
   - ✅ Mechanics fully documented
   - ✅ Database schema complete (including paths and terrain_modifications)
   - ✅ API endpoints complete (including validation endpoint)

6. **Skills System:**
   - ✅ Skills reference complete
   - ✅ Database schema complete
   - ✅ API endpoints complete

---

## Next Steps

1. ✅ **Fix Critical API Issues**: ✅ COMPLETED
2. ✅ **Document NPC AI**: ✅ COMPLETED
3. ✅ **Review Consistency**: ✅ COMPLETED
4. ✅ **Update API Spec**: ✅ COMPLETED
5. ✅ **Document Resource Node Mechanics**: ✅ COMPLETED
6. ✅ **Document Building Placement Mechanics**: ✅ COMPLETED
7. **Implementation Planning**: Use completed documentation to guide implementation
8. **Document Trade & Economy Mechanics**: Medium priority - can be done during implementation
9. **Document Advanced Features**: Low priority - Formation/Array, Planet Core, Dimensional Portal (can be done later)

---

## Implementation Readiness

**Core Systems Documentation Status:**
- ✅ **100% Complete** - All critical and high-priority systems documented
- ✅ **Database Schema** - Complete and consistent
- ✅ **API Specification** - Complete and consistent
- ✅ **Mechanics Documentation** - Complete for all core systems

**Ready for Implementation:**
- ✅ All Phase 1 systems documented
- ✅ All Phase 2 systems documented
- ✅ Database schema finalized
- ✅ API endpoints defined
- ✅ Consistency verified

**Remaining Work:**
- 🟡 Trade & Economy Mechanics (can be refined during implementation)
- 🟢 Advanced features (Formation/Array, Planet Core details, Portal details)

---

**Last Updated:** 2025-01-21  
**Next Review:** After Trade & Economy Mechanics documentation or during implementation phase
