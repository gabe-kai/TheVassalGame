# Qi and Mana Mechanics

## Table of Contents
- [Overview](#overview)
- [Ambient Qi System](#ambient-qi-system)
- [Cultivator Qi System](#cultivator-qi-system)
- [Building Qi System](#building-qi-system)
- [Mana Crystal System](#mana-crystal-system)
- [Qi Flow and Modifiers](#qi-flow-and-modifiers)

## Overview

The Qi and Mana system is the core spiritual energy mechanic of TheVassalGame. Qi flows through the world, is absorbed by cultivators and buildings, and can be refined into mana crystals for powering devices and formations.

**Key Concepts:**
- **Ambient Qi**: The base level of spiritual energy in a territory
- **Qi Sources**: Mana veins and mana pools that generate ambient qi
- **Qi Absorption**: Cultivators and buildings absorb qi from the environment
- **Qi Attunement**: Qi can be stored in its natural state or attuned to specific elements/concepts
- **Mana Crystals**: Refined qi that can power devices, refill qi pools, and activate formations

---

## Ambient Qi System

### Territory Ambient Qi Level

Each territory has an **ambient qi level** that represents the spiritual energy density in that area. This level affects:
- Cultivator qi absorption rates
- Building qi generation efficiency
- Mana crystal refinement success rates
- Formation effectiveness

### Ambient Qi Calculation

Ambient qi is calculated at **two levels**: territory-wide base and location-specific.

**Territory-Wide Base Ambient Qi:**
```
base_ambient_qi = qi_source_output + territory_modifiers

territory_ambient_qi = base_ambient_qi + building_qi_modifiers + cultivator_qi_modifiers - territory_drain
```

**Location-Specific Ambient Qi:**
The ambient qi level at a specific location (for buildings and cultivators) is affected by proximity to qi sources:

```
local_ambient_qi = territory_ambient_qi * proximity_modifier

where:
proximity_modifier = 1.0 + (qi_source_proximity_bonus * distance_factor)

distance_factor = 1.0 - (distance_to_qi_source / max_qi_source_range)
- distance_to_qi_source = meters from building/cultivator to nearest qi source
- max_qi_source_range = 500 meters (qi source influence radius)
- distance_factor ranges from 1.0 (at qi source) to 0.0 (500m+ away)
```

**Qi Source Proximity Bonus:**
- **Mana Vein**: proximity_bonus = 0.5 (50% bonus when at source, decreases with distance)
- **Mana Pool**: proximity_bonus = 1.0 (100% bonus when at source, decreases with distance)

**Example:**
- Territory base ambient qi: 200
- Building located 100 meters from a mana vein
- Distance factor = 1.0 - (100 / 500) = 0.8
- Proximity modifier = 1.0 + (0.5 * 0.8) = 1.4
- Local ambient qi = 200 * 1.4 = 280

**Components:**

1. **Qi Source Output** (`qi_source_output`):
   - **Mana Vein**: Base output = 50-100 qi units/day (varies by vein quality)
   - **Mana Pool**: Base output = 200-500 qi units/day (varies by pool size)
   - Qi sources continuously generate qi into the ambient environment

2. **Territory Modifiers** (`territory_modifiers`):
   - Natural terrain features can enhance or reduce qi:
     - Rivers/Lakes: +5% to +15% (depending on size)
     - Forests: +5% to +20% (depending on density)
     - Deserts: -10% to -20% (qi dissipates quickly)
     - Caves/Underground: +15% to +25% (qi concentrates)
   - **Note**: Elevation does not affect qi - qi is independent of terrain height

3. **Building Qi Modifiers** (`building_qi_modifiers`):
   - Buildings can either **enrich** or **drain** ambient qi:
     - **Qi Enriching Buildings**: Add to ambient qi (e.g., Meditation Halls, Qi Condenser Spires)
     - **Qi Draining Buildings**: Consume ambient qi (e.g., Production buildings, Active formations)
   - Net modifier = sum of all building effects in territory

4. **Cultivator Qi Modifiers** (`cultivator_qi_modifiers`):
   - Cultivators actively cultivating absorb qi from ambient environment
   - Each cultivating NPC/player reduces ambient qi by their absorption rate
   - Net modifier = sum of all cultivator absorption rates

5. **Territory Drain** (`territory_drain`):
   - Some territories naturally drain qi (e.g., corrupted areas, dead zones)
   - Player actions can create drains (e.g., over-exploitation, improper formations)

### Ambient Qi Minimum/Maximum

- **Minimum Ambient Qi**: 0 (no spiritual energy, cultivators cannot cultivate)
- **Maximum Ambient Qi**: 1000 (saturated territory, diminishing returns)
- **Optimal Range**: 100-500 (best for cultivation and building efficiency)

### Ambient Qi Updates

Ambient qi levels are recalculated:
- **Every server tick** (every 1-2 seconds) for active territories
- **When buildings are constructed/demolished** (immediate effect)
- **When cultivators start/stop cultivating** (immediate effect)
- **When qi sources are discovered/exploited** (immediate effect)

---

## Cultivator Qi System

### Qi Absorption

Cultivators (NPCs and players with `mortal_class = 'cultivator'`) can absorb qi from the ambient environment.

**Absorption Rate Formula:**
```
absorption_rate = base_absorption * (1 + spirit_power_modifier) * local_ambient_qi_modifier

where:
- base_absorption = 10 + (cultivation_level * 5)  [qi units per hour]
- spirit_power_modifier = spirit_power / 100  [percentage bonus]
- local_ambient_qi_modifier = 0.5 + (local_ambient_qi / 1000) * 0.5  [0.5x to 1.0x multiplier based on local qi]
  - Uses local ambient qi at cultivator's position (affected by proximity to qi source)
  - At 0 local qi: 0.5x multiplier (50% of base rate)
  - At 1000 local qi: 1.0x multiplier (100% of base rate)
```

**Position Matters:**
- Cultivators closer to qi sources have higher local ambient qi
- Higher local ambient qi = faster absorption rate
- Cultivators should position themselves near qi sources for optimal cultivation

**Absorption Conditions:**
- Cultivator must be in a territory with ambient qi > 0
- Cultivator must be in "cultivating" state (meditating, practicing, etc.)
- Higher ambient qi = faster absorption
- Absorption is reduced if cultivator is working, fighting, or otherwise occupied

### Qi Attunement

When cultivators absorb qi, it is **attuned to their personal attunement** (based on their species, ethnicity, and cultivation path).

**Attunement Types:**
- **Fire Attunement**: From Fire Qi, useful for smithing, alchemy
- **Water Attunement**: From Water Qi, useful for healing, purification
- **Earth Attunement**: From Earth Qi, useful for construction, fortification
- **Wind/Air Attunement**: From Wind Qi, useful for speed, movement
- **Metal Attunement**: From Metal Qi, useful for crafting, weapons
- **Wood Attunement**: From Wood Qi, useful for growth, healing
- **Shadow Attunement**: From Shadow Qi, useful for stealth, illusions
- **Light Attunement**: From Light Qi, useful for purification, protection
- **Harmony Attunement**: Balanced attunement, versatile
- **Chaos Attunement**: Unstable attunement, powerful but risky

**Qi Storage:**
- Absorbed qi is stored in the cultivator's `qi_pool` (current qi) and `qi_capacity` (maximum qi)
- Qi pool increases over time as cultivator absorbs qi
- Qi capacity increases through cultivation breakthroughs

### Qi Usage

Cultivators can spend their stored qi for various purposes:

#### 1. Mana Crystal Refinement

Cultivators can refine their stored qi into mana crystals.

**Refinement Process:**
```
crystal_qi_input = cultivator.qi_pool * refinement_percentage
crystal_output = crystal_qi_input * refinement_efficiency

where:
- refinement_percentage = 0.1 to 1.0 (how much of qi pool to use)
- refinement_efficiency = 0.5 + (cultivation_level * 0.05) + (focus * 0.01) + (clarity * 0.01)
  [Base 50% efficiency, +5% per cultivation level, +1% per focus/clarity point]
- Maximum refinement_efficiency = 0.95 (95% efficiency at high levels)
```

**Example:**
- Cultivator has 1000 qi in pool
- Uses 50% (500 qi) for refinement
- Has cultivation level 5, focus 20, clarity 15
- Efficiency = 0.5 + (5 * 0.05) + (20 * 0.01) + (15 * 0.01) = 0.5 + 0.25 + 0.2 + 0.15 = 1.1 (capped at 0.95)
- Crystal output = 500 * 0.95 = 475 qi worth of mana crystals

**Crystal Quality:**
- **Low-Grade Crystal**: 10-100 qi worth
- **Mid-Grade Crystal**: 100-500 qi worth
- **High-Grade Crystal**: 500-1000 qi worth
- **Perfect Crystal**: 1000+ qi worth (rare, requires perfect conditions)

#### 2. Qi Pool Refill (External)

Cultivators can consume mana crystals to refill their qi pool:
- 1 qi unit in crystal = 1 qi unit in pool (1:1 conversion)
- Cannot exceed `qi_capacity`
- Can be done during combat or when qi pool is low

#### 3. Skill Activation

Cultivators can spend qi to activate skills:
- Each skill has a qi cost
- Higher qi investment = more powerful effect
- Skills consume qi from pool

#### 4. Formation Activation

Cultivators can power formations with their qi:
- Formations require qi to activate
- Can use stored qi or mana crystals
- Higher qi input = stronger formation effects

### Cultivation Breakthroughs

Cultivators can "break through" to higher cultivation levels:
- Requires accumulated qi pool (e.g., qi_pool >= qi_capacity * 1.5)
- Requires ambient qi above threshold (e.g., ambient_qi >= 200)
- Requires successful breakthrough attempt (based on willpower, spirit_power, clarity)
- On success: qi_capacity increases, stats may improve, new abilities unlocked

---

## Building Qi System

Buildings interact with ambient qi in three ways:

### 1. Qi Absorption and Storage (Unattuned)

Some buildings absorb qi from the ambient environment and store it in its natural state.

**Building Types:**
- **Qi Condenser Spire**: Absorbs ambient qi, stores unattuned
- **Qi Storage Vault**: Stores large amounts of unattuned qi
- **Qi Collector Arrays**: Networks of small collectors that gather ambient qi

**Absorption Rate:**
```
building_absorption = base_absorption * (1 + tier_modifier) * local_ambient_qi_modifier

where:
- base_absorption = building_type.base_qi_absorption  [qi units per hour]
- tier_modifier = building_tier * 0.1  [each tier adds 10%]
- local_ambient_qi_modifier = 0.5 + (local_ambient_qi / 1000) * 0.5  [0.5x to 1.0x multiplier based on local qi]
  - Uses local ambient qi at building's position (affected by proximity to qi source)
  - At 0 local qi: 0.5x multiplier (50% of base rate)
  - At 1000 local qi: 1.0x multiplier (100% of base rate)
```

**Position Matters:**
- Buildings closer to qi sources have higher local ambient qi
- Higher local ambient qi = faster absorption and refinement rates
- Strategic building placement near qi sources maximizes efficiency

**Storage Capacity:**
- Each building has a `qi_storage_capacity`
- Stored qi can be extracted by players or used by the building
- Storage is limited by building tier and type

### 2. Qi Attunement and Storage

Some buildings absorb qi and attune it to specific elements before storing.

**Building Types:**
- **Attunement Chambers**: Absorb qi and attune to specific elements
- **Elemental Forges**: Attune qi to fire/earth/metal for crafting
- **Harmony Halls**: Attune qi to harmony for versatile use

**Attunement Process:**
- Building absorbs ambient qi (same formula as unattuned)
- Building applies attunement process (based on building type)
- Attuned qi is stored separately from unattuned qi
- Attunement has a small efficiency loss (5-10%)

### 3. Qi Refinement into Crystals

Some buildings can refine stored qi (attuned or unattuned) into mana crystals.

**Building Types:**
- **Crystal Refinery**: Refines unattuned qi into crystals
- **Attuned Crystal Forge**: Refines attuned qi into specialized crystals
- **Sect Hall** (Tier 2+): Can refine qi into crystals

**Refinement Process:**
```
building_refinement_efficiency = base_efficiency * (1 + worker_skill_modifier + building_tier_modifier) * local_ambient_qi_modifier

crystal_output = qi_input * building_refinement_efficiency

where:
- base_efficiency = 0.6  [60% base efficiency]
- worker_skill_modifier = (average_crystal_refining_skill / 100) * 0.2  [up to 20% bonus]
- building_tier_modifier = building_tier * 0.05  [each tier adds 5%]
- local_ambient_qi_modifier = 0.7 + (local_ambient_qi / 1000) * 0.3  [0.7x to 1.0x multiplier]
  - Uses local ambient qi at building's position (affected by proximity to qi source)
  - At 0 local qi: 0.7x multiplier (70% efficiency)
  - At 1000 local qi: 1.0x multiplier (100% efficiency)
```

**Refinement Requirements:**
- Building must have stored qi (attuned or unattuned)
- Building may require workers with Crystal Refining skill
- Building may require additional resources (essence stones, etc.)

### Building Qi Effects on Ambient Qi

Buildings can either **enrich** or **drain** the ambient qi in a territory:

**Enriching Buildings:**
- **Meditation Halls**: +5 to +30 qi/day (depending on tier)
- **Qi Condenser Spires**: +10 to +50 qi/day (depending on tier)
- **Spirit Gardens**: +3 to +15 qi/day (depending on tier)
- **Harmony Arrays**: +2 to +10 qi/day (depending on tier)

**Draining Buildings:**
- **Production Buildings**: -2 to -20 qi/day (depending on tier and production intensity)
- **Active Formations**: -5 to -50 qi/day (depending on formation type and power)
- **Over-exploitation**: Excessive resource extraction can create permanent drains

**Net Effect:**
```
territory_qi_enrichment = sum(enriching_buildings) - sum(draining_buildings)
```

---

## Mana Crystal System

### Crystal Types

Mana crystals are refined qi that can power devices and formations.

**Crystal Grades:**
1. **Low-Grade Mana Crystal**
   - Qi Content: 10-100 qi units
   - Purity: 50-70%
   - Uses: Basic devices, simple formations, low-tier crafting

2. **Mid-Grade Mana Crystal**
   - Qi Content: 100-500 qi units
   - Purity: 70-85%
   - Uses: Intermediate devices, standard formations, mid-tier crafting

3. **High-Grade Mana Crystal**
   - Qi Content: 500-1000 qi units
   - Purity: 85-95%
   - Uses: Advanced devices, complex formations, high-tier crafting

4. **Perfect Mana Crystal**
   - Qi Content: 1000+ qi units
   - Purity: 95-100%
   - Uses: Master devices, legendary formations, ultimate crafting

**Attuned Crystals:**
- Crystals refined from attuned qi retain their attunement
- Attuned crystals are more effective for specific uses (e.g., Fire Crystal for smithing)
- Attuned crystals can be used for general purposes but at reduced efficiency

### Crystal Uses

#### 1. Power Devices

Mana crystals can power small devices:
- **Portable Tools**: Mining tools, gathering tools, crafting devices
- **Formation Cores**: Crystals inserted into formation arrays to power them
- **Transportation**: Crystals power vehicles, teleportation arrays
- **Communication**: Crystals power long-distance communication devices

**Device Power Consumption:**
- Each device has a `power_consumption` rate (qi units per hour)
- Crystals inserted into devices gradually deplete
- Depleted crystals become inert (can be recharged or discarded)

#### 2. Power Runes

Mana crystals can activate runes and inscriptions:
- **Defensive Runes**: Crystals power defensive barriers and shields
- **Offensive Runes**: Crystals power attack formations and traps
- **Utility Runes**: Crystals power utility formations (teleportation, storage, etc.)

**Rune Power Requirements:**
- Each rune type has a `power_requirement` (qi units to activate)
- Higher-grade crystals = more powerful rune effects
- Attuned crystals = specialized rune effects

#### 3. Refill Cultivator Qi Pools

Cultivators can consume mana crystals to refill their qi pool:
- 1 qi unit in crystal = 1 qi unit in pool (1:1 conversion)
- Can be consumed instantly or gradually
- Cannot exceed `qi_capacity`
- Useful during combat or when qi pool is low

#### 4. Crafting Material

Mana crystals can be used as crafting materials:
- **Enchanting**: Crystals enhance item properties
- **Alchemy**: Crystals are ingredients in potions and elixirs
- **Construction**: Crystals are embedded in buildings for qi effects

#### 5. Trade Currency

Mana crystals can be used as trade currency:
- Standardized value based on qi content and purity
- High-grade crystals are valuable trade goods
- Can be exchanged for resources, services, or other crystals

---

## Qi Flow and Modifiers

### Qi Flow Visualization

```
Qi Sources (Veins/Pools)
    ↓
Ambient Qi Level (Territory)
    ↓
    ├─→ Cultivators (Absorb & Attune)
    │       ↓
    │   Qi Pool (Stored, Attuned)
    │       ↓
    │   Mana Crystals (Refined)
    │
    └─→ Buildings (Absorb & Store)
            ↓
        Stored Qi (Unattuned/Attuned)
            ↓
        Mana Crystals (Refined)
```

### Modifier Stacking Rules

1. **Percentage Modifiers**: Stack multiplicatively
   - Example: 10% bonus + 20% bonus = 1.1 * 1.2 = 1.32 (32% total bonus)

2. **Flat Modifiers**: Stack additively
   - Example: +10 qi + 20 qi = +30 qi total

3. **Maximum Limits**: Some modifiers have caps
   - Absorption rate: Maximum 200% of base (3x multiplier)
   - Refinement efficiency: Maximum 95%

### Territory Qi Enrichment vs Drain

**Enrichment:**
- Buildings that add to ambient qi
- Cultivators cultivating efficiently (without over-draining)
- Proper qi management and formation placement

**Drain:**
- Excessive production building operation
- Over-exploitation of resources
- Improper formation placement
- Too many cultivators in a small area

**Balance:**
- Territories should aim for net enrichment (more qi added than consumed)
- Net enrichment contributes to planetary core leveling (see Victory Conditions)

---

## Database Schema Updates

### New Fields Needed

**`planets` table:**
- `core_level INTEGER DEFAULT 1` - Planetary core level (1-7)
- `core_value REAL DEFAULT 0.0` - Cumulative qi enrichment value (for leveling)

**`territories` table:**
- `ambient_qi_level REAL DEFAULT 0.0` - Current ambient qi in territory
- `base_qi_output REAL DEFAULT 0.0` - Base qi from qi source
- `qi_enrichment_rate REAL DEFAULT 0.0` - Net qi enrichment per day

**`buildings` table:**
- `qi_storage_capacity REAL DEFAULT 0.0` - Maximum qi storage
- `stored_qi_unattuned REAL DEFAULT 0.0` - Current unattuned qi
- `stored_qi_attuned JSONB` - Attuned qi by type: `{"fire": 100, "water": 50}`
- `qi_absorption_rate REAL DEFAULT 0.0` - Qi absorption per hour
- `qi_enrichment_per_day REAL DEFAULT 0.0` - Qi added to ambient per day

**`avatars` and `npcs` tables:**
- `cultivation_level INTEGER DEFAULT 0` - Current cultivation level
- `cultivation_experience REAL DEFAULT 0.0` - Progress toward next level

---

## Notes

- Ambient qi has **two levels**: territory-wide base and location-specific (affected by proximity to qi sources)
- **Position matters**: Buildings and cultivators closer to qi sources have higher local ambient qi
- Qi sources (veins/pools) are **permanent features** of territories (cannot be depleted)
- **Elevation does not affect qi** - qi is independent of terrain height
- Buildings can **enrich or drain** ambient qi, affecting the entire territory
- Cultivators **compete for ambient qi** - too many cultivators in one area reduces efficiency for all
- Mana crystals are **portable power sources** that enable advanced gameplay mechanics
- Qi attunement allows for **specialization** - different attunements excel at different tasks
- Planetary core tracks cumulative qi enrichment across all territories

---

**Last Updated:** 2025-11-05

