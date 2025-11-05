# Resource Node Mechanics

## Table of Contents
- [Overview](#overview)
- [Node Types](#node-types)
- [Node Spawning](#node-spawning)
- [Node Properties](#node-properties)
- [Gathering Mechanics](#gathering-mechanics)
- [Visual Indicators](#visual-indicators)
- [Depletion & Respawn](#depletion--respawn)
- [Random Events](#random-events)
- [Node Discovery](#node-discovery)
- [Skill Requirements](#skill-requirements)

## Overview

Resource nodes are natural deposits of materials scattered throughout the world that players can gather directly. Each node type has unique properties, depletion mechanics, visual indicators, and respawn behaviors. Nodes provide an alternative to building-based resource generation, allowing players to gather resources directly from the environment.

**Key Principles:**
- **Visual Feedback**: Some nodes show depletion visually (lumber), others don't (stone, iron)
- **Skill-Based**: Gathering efficiency depends on NPC/player skills
- **Event-Driven**: Random world events can affect node yields and availability
- **Sustainable**: Most nodes respawn, ensuring long-term resource availability
- **Territory-Based**: Nodes spawn within territories during generation

---

## Node Types

### 1. Lumber Nodes (Trees)

**Description:** Forested areas with harvestable trees that provide lumber.

**Properties:**
- **Resource Type**: Lumber
- **Visual Depletion**: ✅ **YES** - Trees disappear as node is depleted
- **Skill Required**: Forestry, Woodcutting
- **Tools**: Axes, saws (optional, provides bonus)
- **Gathering Rate**: Base 10-20 lumber/hour (depends on node size)
- **Node Sizes**: Small (100-200 lumber), Medium (300-500 lumber), Large (600-1000 lumber)

**Visual Indicators:**
- **Full Node**: Dense forest with many trees
- **75% Remaining**: Some clearings visible, trees thinning
- **50% Remaining**: Significant clearings, sparse tree coverage
- **25% Remaining**: Mostly clearings, few trees remaining
- **Depleted**: Bare ground, stumps, no trees
- **Respawned**: Young saplings appearing, gradually growing

**Special Mechanics:**
- Trees can be harvested individually (visual feedback per tree)
- Larger trees provide more lumber
- Node appearance directly reflects remaining resources

---

### 2. Stone Quarries

**Description:** Rock outcroppings and stone deposits that provide stone blocks.

**Properties:**
- **Resource Type**: Stone Blocks
- **Visual Depletion**: ❌ **NO** - Appearance doesn't change
- **Skill Required**: Mining, Quarrying
- **Tools**: Pickaxes, drills (optional, provides bonus)
- **Gathering Rate**: Base 15-30 stone blocks/hour (depends on node quality)
- **Node Sizes**: Small (200-400 blocks), Medium (500-800 blocks), Large (900-1500 blocks)

**Visual Indicators:**
- **Always**: Same visual appearance regardless of remaining resources
- **No Visual Feedback**: Players must check node status to see remaining amount
- **Depleted State**: Node appears the same but is non-interactive

**Special Mechanics:**
- No visual indication makes resource management strategic
- Players must track usage manually or check node status
- High-quality quarries (rare) provide bonus yield

---

### 3. Iron Mines (Ore Veins)

**Description:** Underground iron ore deposits accessible via surface nodes.

**Properties:**
- **Resource Type**: Iron Ore
- **Visual Depletion**: ❌ **NO** - Appearance doesn't change
- **Skill Required**: Mining, Metallurgy
- **Tools**: Pickaxes, drills, ore extractors (optional, provides bonus)
- **Gathering Rate**: Base 8-18 iron ore/hour (depends on node quality)
- **Node Sizes**: Small (150-300 ore), Medium (400-700 ore), Large (800-1200 ore)

**Visual Indicators:**
- **Always**: Same visual appearance (ore vein entrance/outcrop)
- **No Visual Feedback**: Appearance unchanged regardless of remaining resources
- **Depleted State**: Node appears the same but is non-interactive

**Special Mechanics:**
- Underground resources not visible from surface
- Requires mining skill to identify rich veins
- High-quality veins (rare) provide bonus yield and faster gathering

---

### 4. Food Sources (Farmable Land)

**Description:** Fertile areas suitable for farming that provide food.

**Properties:**
- **Resource Type**: Food
- **Visual Depletion**: ⚠️ **PARTIAL** - Crop quality visible, but not quantity
- **Skill Required**: Farming, Agriculture
- **Tools**: Farming tools (optional, provides bonus)
- **Gathering Rate**: **Varies** - Depends heavily on farmer skill and random events
- **Node Sizes**: Small (100-200 food), Medium (250-400 food), Large (500-800 food)

**Gathering Rate Formula:**
```
base_yield = node_size × season_modifier × soil_quality
farmer_skill_modifier = 0.5 + (farmer_skill_level / 100)  // 0.5 to 1.5
event_modifier = 1.0 + (random_event_bonus - random_event_penalty)  // 0.5 to 2.0

gathering_rate = base_yield × farmer_skill_modifier × event_modifier
```

**Visual Indicators:**
- **Healthy**: Lush, green crops, well-maintained fields
- **Poor Quality**: Wilted crops, poor soil, weeds visible
- **Event-Affected**: Visual changes based on events (drought = brown, flood = muddy)

**Special Mechanics:**
- **Skill-Dependent**: Farmer skill directly affects yield (low skill = poor yield, high skill = excellent yield)
- **Random Events**: Weather, pests, fertility events affect yield significantly
- **Seasonal**: Some crops have seasonal modifiers
- **Soil Quality**: Nodes have inherent soil quality (poor, normal, fertile, rich)

**Random Events Affecting Food:**
- **Drought**: -50% yield, visual: brown, dry fields
- **Flood**: -30% yield, visual: muddy, waterlogged fields
- **Pest Infestation**: -40% yield, visual: damaged crops
- **Fertile Rain**: +30% yield, visual: vibrant, healthy crops
- **Early Frost**: -60% yield, visual: frost-damaged crops
- **Perfect Weather**: +20% yield, visual: ideal growing conditions

---

### 5. Herb Patches

**Description:** Natural herb-growing areas that provide medicinal and alchemical herbs.

**Properties:**
- **Resource Type**: Various herbs (Healing Herbs, Spirit Herbs, etc.)
- **Visual Depletion**: ✅ **YES** - Herbs become sparse as node depletes
- **Skill Required**: Herbalism, Botany
- **Tools**: Gathering baskets, scythes (optional, provides bonus)
- **Gathering Rate**: Base 5-15 herbs/hour (depends on herb rarity)
- **Node Sizes**: Small (50-100 herbs), Medium (150-250 herbs), Large (300-500 herbs)

**Visual Indicators:**
- **Full Node**: Dense herb growth, vibrant colors
- **50% Remaining**: Sparse patches, visible ground
- **Depleted**: Bare ground, few scattered herbs
- **Respawned**: Young herbs sprouting

**Special Mechanics:**
- Rare herbs spawn in specific biomes
- Some herbs only spawn near qi sources
- Herbs can be over-harvested (permanent depletion if harvested too aggressively)

---

### 6. Qi Source Nodes

**Description:** Natural qi pools, veins, and ley lines that provide ambient qi enhancement.

**Properties:**
- **Resource Type**: Ambient Qi (not directly gathered, but enhances nearby activities)
- **Visual Depletion**: ❌ **NO** - Qi sources don't deplete
- **Skill Required**: Qi Sensing (to identify), Cultivation (to benefit)
- **Tools**: None (qi sources are passive)
- **Effect**: Provides ambient qi bonus to nearby buildings and cultivators
- **Types**: Qi Veins (small), Qi Pools (medium), Ley Lines (large)

**Visual Indicators:**
- **Always**: Glowing, ethereal appearance, visible qi aura
- **Strength**: Visual intensity indicates qi potency
- **No Depletion**: Appearance unchanged over time

**Special Mechanics:**
- Qi sources don't deplete (infinite ambient qi)
- Strength affects ambient qi calculation (see `docs/qi-mana-mechanics.md`)
- Can be enhanced by cultivation techniques
- Buildings near qi sources gain efficiency bonuses

---

### 7. Water Sources

**Description:** Rivers, lakes, and springs that provide water.

**Properties:**
- **Resource Type**: Water
- **Visual Depletion**: ❌ **NO** - Water sources are infinite
- **Skill Required**: None (basic), Water Gathering (for efficiency)
- **Tools**: Buckets, water wheels (optional, provides bonus)
- **Gathering Rate**: Base 20-50 water/hour (depends on source size)
- **Node Sizes**: Infinite (water sources don't deplete)

**Visual Indicators:**
- **Always**: Same appearance (flowing water, lake, spring)
- **No Depletion**: Water sources are renewable

**Special Mechanics:**
- Water sources never deplete (infinite)
- Some sources have quality levels (fresh, brackish, mineral)
- Can be polluted by events (temporary usability loss)

---

## Node Spawning

### Territory Generation

**Initial Spawning:**
- Resource nodes spawn during territory generation
- Node placement is biome-based and terrain-based
- Distribution follows natural patterns (forests have trees, mountains have stone/ore)

**Spawning Rules:**
- **Biome-Based**: Each biome has preferred node types
  - Forests: Lumber nodes, herb patches
  - Mountains: Stone quarries, iron mines
  - Plains: Food sources, herb patches
  - Rivers/Lakes: Water sources
- **Density**: 5-15 nodes per 1km² territory (varies by biome)
- **Distribution**: Random placement within appropriate terrain
- **Quality Distribution**: 70% normal, 20% high quality, 10% low quality

### Node Quality Tiers

**Low Quality:**
- -30% yield
- Slower gathering rate
- Smaller node size

**Normal Quality:**
- Standard yield
- Standard gathering rate
- Standard node size

**High Quality:**
- +30% yield
- Faster gathering rate
- Larger node size

**Rare Quality:**
- +50% yield
- +20% gathering rate
- +40% node size
- Special properties (e.g., rare herbs, spirit-infused stone)

---

## Node Properties

### Base Properties

Each node has the following properties:

**Resource Type:**
- Determines what resource is gathered
- Affects gathering skill requirements

**Amount:**
- Current remaining resources
- Starts at `max_amount` when spawned
- Decreases as resources are gathered

**Max Amount:**
- Initial resource capacity
- Determines node size category
- Affected by quality tier

**Respawn Time:**
- Time in seconds until node respawns after depletion
- `NULL` for non-respawning nodes (rare, permanent depletion)
- Varies by node type and quality

**Quality Tier:**
- Affects yield, gathering rate, and node size
- Low, Normal, High, Rare

**Location:**
- World coordinates (world_x, world_y)
- Territory and region association
- Chunk coordinates for spatial queries

---

## Gathering Mechanics

### Gathering Process

**Step 1: Node Selection**
- Player/NPC approaches resource node
- Node must be within interaction range (5 meters)
- Node must have resources remaining (`amount > 0`)

**Step 2: Gathering Initiation**
- Player/NPC initiates gathering action
- Server validates:
  - Node is accessible
  - Node has resources remaining
  - Gatherer has required skill level
  - Gatherer has tools (if required)

**Step 3: Gathering Rate Calculation**

**Base Gathering Rate:**
```
base_rate = node_type_base_rate × quality_modifier

Where:
- node_type_base_rate: Base rate for node type (lumber: 15/hour, stone: 20/hour, etc.)
- quality_modifier: Low: 0.7, Normal: 1.0, High: 1.3, Rare: 1.5
```

**Skill Modifier:**
```
skill_modifier = 0.5 + (skill_level / 100) × 1.0

Where:
- skill_level: Gatherer's relevant skill level (0-100)
- Minimum: 0.5 (50% efficiency at skill 0)
- Maximum: 1.5 (150% efficiency at skill 100)
```

**Tool Modifier:**
```
tool_modifier = 1.0 + (tool_quality × 0.2)

Where:
- tool_quality: 0 (no tool) to 5 (masterwork tool)
- No tool: 1.0
- Basic tool: 1.2
- Advanced tool: 1.4
- Masterwork tool: 2.0
```

**Final Gathering Rate:**
```
final_rate = base_rate × skill_modifier × tool_modifier × event_modifier

Where:
- event_modifier: Random event effects (default: 1.0)
```

**Step 4: Resource Extraction**
- Server calculates resources gathered over time interval
- Deducts resources from node (`amount -= resources_gathered`)
- Adds resources to gatherer's inventory
- Updates node `last_harvested_at` timestamp

**Step 5: Depletion Check**
- If `amount <= 0`:
  - Mark node as depleted
  - Start respawn timer (if applicable)
  - Update visual appearance (for visual nodes)
  - Broadcast depletion to nearby players

---

## Visual Indicators

### Visual Depletion (Lumber, Herbs)

**Lumber Nodes:**
- Trees disappear as node is depleted
- Visual density directly correlates to remaining resources
- Players can estimate remaining resources by tree count
- Depleted state: Bare ground, stumps

**Herb Patches:**
- Herbs become sparse as node depletes
- Visual density correlates to remaining resources
- Depleted state: Bare ground, scattered herbs

### No Visual Depletion (Stone, Iron)

**Stone Quarries:**
- Appearance unchanged regardless of remaining resources
- Players must check node status to see remaining amount
- Strategic resource management required

**Iron Mines:**
- Appearance unchanged regardless of remaining resources
- Underground resources not visible from surface
- Requires checking node status or mining skill to estimate

### Partial Visual (Food)

**Food Sources:**
- Crop quality visible (healthy vs. poor)
- Quantity not directly visible (but can be estimated from crop density)
- Visual changes based on random events (drought, flood, etc.)
- Soil quality affects visual appearance

---

## Depletion & Respawn

### Depletion Mechanics

**Standard Depletion:**
- Resources are deducted as they are gathered
- Node becomes non-interactive when `amount = 0`
- Depletion triggers respawn timer (if applicable)

**Over-Harvesting (Herbs Only):**
- If herbs are harvested too aggressively (depleted multiple times rapidly)
- Node may permanently deplete (rare, 5% chance per rapid depletion)
- Permanent depletion: Node never respawns

### Respawn Mechanics

**Standard Respawn:**
- Most nodes respawn after depletion
- Respawn time varies by node type:
  - **Lumber**: 7-14 days (real-time)
  - **Stone**: 10-20 days
  - **Iron**: 12-24 days
  - **Herbs**: 3-7 days
  - **Food**: 1-3 days (if farmable, instant if natural)

**Respawn Conditions:**
- Time-based: Node respawns after `respawn_time` seconds
- Same location: Node respawns at same coordinates
- Quality preservation: Node respawns at same quality tier (90% chance) or one tier lower (10% chance)
- Amount reset: Node respawns with `max_amount` resources

**Non-Respawning Nodes:**
- Rare nodes (5% of all nodes) never respawn
- Once depleted, permanently removed
- High yield encourages careful resource management

**Respawn Calculation:**
```
respawn_time = base_respawn_time × quality_modifier × territory_modifier

Where:
- base_respawn_time: Node type base (lumber: 7 days, stone: 10 days, etc.)
- quality_modifier: Low: 0.8, Normal: 1.0, High: 1.2, Rare: 1.5
- territory_modifier: Based on territory qi level (higher qi = faster respawn)
```

---

## Random Events

### Event Types

**Weather Events:**
- **Drought**: Affects food sources (-50% yield, visual: brown fields)
- **Flood**: Affects food sources (-30% yield, visual: muddy fields)
- **Fertile Rain**: Affects food sources (+30% yield, visual: vibrant crops)
- **Early Frost**: Affects food sources (-60% yield, visual: frost damage)

**Natural Events:**
- **Pest Infestation**: Affects food sources (-40% yield, visual: damaged crops)
- **Soil Enrichment**: Affects food sources (+20% yield, visual: rich soil)
- **Mineral Discovery**: Temporarily increases stone/iron node yield (+50% for 1 day)
- **Tree Blight**: Reduces lumber node yield (-30% for 3 days)

**Cultivation Events:**
- **Qi Surge**: Temporarily increases all node yields (+10% for 6 hours)
- **Qi Drain**: Temporarily decreases all node yields (-15% for 6 hours)
- **Spirit Infusion**: Rarely transforms normal node to spirit-infused node (permanent +20% yield)

### Event Frequency

**Common Events (Daily):**
- Weather events: 20% chance per day per territory
- Natural events: 10% chance per day per territory

**Rare Events (Weekly):**
- Cultivation events: 5% chance per week per territory
- Mineral discovery: 2% chance per week per territory

**Event Duration:**
- Most events last 1-3 days
- Some events are permanent (spirit infusion, permanent depletion)

### Event Impact on Food

Food sources are most affected by random events:

**Positive Events:**
- Fertile Rain: +30% yield
- Perfect Weather: +20% yield
- Soil Enrichment: +20% yield
- Qi Surge: +10% yield

**Negative Events:**
- Drought: -50% yield
- Early Frost: -60% yield
- Pest Infestation: -40% yield
- Flood: -30% yield
- Qi Drain: -15% yield

**Combined Effects:**
- Multiple events can stack (e.g., drought + pest = -90% yield)
- Farmer skill helps mitigate negative events:
  - High skill farmers: -50% penalty → -30% penalty
  - Low skill farmers: -50% penalty → -70% penalty

---

## Node Discovery

### Discovery Mechanics

**Automatic Discovery:**
- Nodes within player's territory are automatically discovered
- Nodes are visible on map when player enters territory

**Exploration Discovery:**
- Nodes outside player's territory require exploration
- Player must be within 50 meters to discover node
- Nodes appear on map after discovery

**Skill-Based Discovery:**
- High skill in relevant gathering skill increases discovery range:
  - Skill 0-25: 25 meters
  - Skill 26-50: 35 meters
  - Skill 51-75: 50 meters
  - Skill 76-100: 75 meters

**Hidden Nodes:**
- Rare nodes (10% of all nodes) are hidden
- Require specific skills or exploration to discover
- Hidden nodes often have higher quality or rare resources

### Discovery Indicators

**Visual Indicators:**
- Discovered nodes: Visible on map, interactable
- Undiscovered nodes: Not visible on map
- Hidden nodes: May show subtle visual hints (glowing, unusual terrain)

**Map Display:**
- Nodes show as icons on map
- Icon indicates node type and status
- Depleted nodes show as grayed-out icons
- High-quality nodes show with special icon border

---

## Skill Requirements

### Required Skills

**Lumber Nodes:**
- **Primary**: Forestry, Woodcutting
- **Minimum Skill**: Level 1 (can gather at 50% efficiency)
- **Optimal Skill**: Level 50+ (100%+ efficiency)

**Stone Quarries:**
- **Primary**: Mining, Quarrying
- **Minimum Skill**: Level 1 (can gather at 50% efficiency)
- **Optimal Skill**: Level 50+ (100%+ efficiency)

**Iron Mines:**
- **Primary**: Mining, Metallurgy
- **Minimum Skill**: Level 1 (can gather at 50% efficiency)
- **Optimal Skill**: Level 50+ (100%+ efficiency)

**Food Sources:**
- **Primary**: Farming, Agriculture
- **Minimum Skill**: Level 1 (can gather at 50% efficiency)
- **Optimal Skill**: Level 50+ (100%+ efficiency)
- **Special**: Skill directly affects yield (not just efficiency)

**Herb Patches:**
- **Primary**: Herbalism, Botany
- **Minimum Skill**: Level 1 (can gather at 50% efficiency)
- **Optimal Skill**: Level 50+ (100%+ efficiency)

### Skill Effects

**Gathering Efficiency:**
- Skill level affects gathering rate (see Gathering Mechanics)
- Higher skill = faster gathering = more resources per hour

**Yield Quality (Food Only):**
- Higher farming skill = better yield quality
- High skill farmers can extract more food from same node
- Skill affects random event mitigation

**Discovery Range:**
- Higher skill = increased discovery range
- Helps find hidden nodes and rare resources

**Tool Usage:**
- Higher skill = better tool utilization
- Advanced tools require higher skill to use effectively

---

## Database Schema

### Resource Nodes Table

The `resource_nodes` table (defined in `docs/database-schema.md`) stores:

- `id`: Unique node identifier
- `resource_type_id`: References resource type
- `world_x`, `world_y`: World coordinates
- `amount`: Current remaining resources
- `max_amount`: Initial resource capacity
- `respawn_time`: Seconds to respawn (NULL if non-respawning)
- `last_harvested_at`: Timestamp of last harvest
- `region_id`, `chunk_x`, `chunk_y`: Spatial organization

### Additional Fields Needed

**Consider Adding:**
- `quality_tier`: Low, Normal, High, Rare
- `is_hidden`: Boolean (hidden nodes)
- `discovered_by_avatar_ids`: Array of avatar IDs who discovered this node
- `permanent_depletion`: Boolean (permanently depleted nodes)
- `event_modifiers`: JSONB (active random event effects)

---

## Summary

Resource nodes provide a natural resource gathering system with:

- **Visual Feedback**: Lumber and herbs show depletion, stone and iron don't
- **Skill-Based**: Gathering efficiency depends on NPC/player skills
- **Event-Driven**: Random events significantly affect food yields
- **Sustainable**: Most nodes respawn, ensuring long-term availability
- **Strategic**: No visual depletion for stone/iron requires resource management

**Key Mechanics:**
- Lumber nodes: Visual depletion as trees are harvested
- Stone/Iron nodes: No visual indication, strategic management required
- Food sources: Skill-dependent yield, heavily affected by random events
- Most nodes respawn after depletion
- Quality tiers affect yield and gathering rate
- Random events create dynamic gameplay

---

**Last Updated:** 2025-01-XX

