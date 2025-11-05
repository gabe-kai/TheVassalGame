# Production Mechanics and Rate Calculations

## Table of Contents
- [Overview](#overview)
- [Production Rate Formula](#production-rate-formula)
- [Modifiers](#modifiers)
- [Processing Time Calculations](#processing-time-calculations)
- [Resource Collection Mechanics](#resource-collection-mechanics)
- [Examples](#examples)

## Overview

Production rates determine how fast resources are generated, processed, or consumed by buildings. Rates are calculated using base values from building tiers, modified by worker skills, building conditions, district bonuses, and other factors.

## Production Rate Formula

### Base Formula

```
final_production_rate = base_rate * skill_modifier * building_modifier * district_modifier * supply_chain_modifier * condition_modifier * qi_modifier
```

### Component Breakdown

#### 1. Base Rate (`base_rate`)

The base production rate comes from the building tier and building type.

**Source:** `building_tiers` table or `building_types` passive resource definitions

**Examples:**
- Timberworks Tier 1: 10 lumber/day
- Timberworks Tier 2: 25 lumber/day
- Timberworks Tier 3: 50 lumber/day
- Farmland Tier 1: 10 food/day
- Farmland Tier 2: 25 food/day

**Formula:**
```
base_rate = building_tier.base_production_rate
```

#### 2. Skill Modifier (`skill_modifier`)

Workers assigned to buildings improve production rates based on their skill levels.

**Calculation:**
```
skill_modifier = 1.0 + sum(worker_skill_bonus) / max(assigned_workers, 1)

where:
worker_skill_bonus = (worker_skill_level / 100) * skill_bonus_per_level

- skill_bonus_per_level = 0.01 (1% per skill level)
- Maximum skill level = 100
- Maximum skill bonus per worker = 1.0 (100% bonus)
```

**Example:**
- Building requires "Logging" skill
- Worker 1: Logging level 50 → bonus = 0.5 * 0.01 = 0.005 (0.5%)
- Worker 2: Logging level 80 → bonus = 0.8 * 0.01 = 0.008 (0.8%)
- Worker 3: Logging level 30 → bonus = 0.3 * 0.01 = 0.003 (0.3%)
- Total skill bonus = (0.005 + 0.008 + 0.003) / 3 = 0.0053 (0.53%)
- Skill modifier = 1.0 + 0.0053 = 1.0053

**Multiple Skills:**
If a building benefits from multiple skills (e.g., primary + secondary):
```
skill_modifier = 1.0 + (primary_skill_bonus * 0.7) + (secondary_skill_bonus * 0.3)
```

**Worker Count:**
- Each building has a maximum employment capacity
- More workers = more skill bonuses (averaged)
- Diminishing returns: Workers beyond optimal count provide reduced bonuses

**No Workers:**
- If no workers assigned: `skill_modifier = 1.0` (no bonus, no penalty)
- Some buildings can operate without workers (passive generation)
- Workers are optional but recommended for best rates

#### 3. Building Modifier (`building_modifier`)

Building-specific modifiers from tier upgrades and signature additions.

**Components:**
```
building_modifier = tier_bonus * signature_bonus

where:
- tier_bonus = 1.0 + (building_tier * 0.05)  [5% per tier above Tier 1]
- signature_bonus = 1.0 + sum(signature_addition_bonuses)
```

**Tier Bonus:**
- Tier 1: 1.0 (no bonus)
- Tier 2: 1.05 (5% bonus)
- Tier 3: 1.10 (10% bonus)
- Tier 4: 1.15 (15% bonus)
- Tier 5: 1.20 (20% bonus)
- Tier 6: 1.25 (25% bonus)

**Signature Additions:**
- Each signature addition can provide production bonuses
- Bonuses are additive (e.g., +5% + 3% = +8%)
- Signature bonus = 1.0 + sum of all signature addition percentages

**Example:**
- Building: Timberworks Tier 3
- Signature Addition: "Efficiency Ring" (+10% production)
- Tier bonus = 1.10
- Signature bonus = 1.10
- Building modifier = 1.10 * 1.10 = 1.21 (21% total bonus)

#### 4. District Modifier (`district_modifier`)

Buildings of the same category clustered together form districts that provide bonuses.

**Calculation:**
```
district_modifier = 1.0 + district_bonus

where:
district_bonus = (district_building_count - 1) * district_bonus_per_building

- district_bonus_per_building = 0.02 (2% per additional building)
- Minimum district size = 2 buildings
- Maximum district bonus = 0.20 (20% bonus at 11+ buildings)
```

**Example:**
- District: 5 Timberworks buildings
- District bonus = (5 - 1) * 0.02 = 0.08 (8% bonus)
- District modifier = 1.0 + 0.08 = 1.08

**District Requirements:**
- Buildings must be within 50 meters of each other
- Buildings must be of the same category (e.g., all "resource" buildings)
- Buildings must be Tier 2+ to form districts

#### 5. Supply Chain Modifier (`supply_chain_modifier`)

Buildings receive bonuses when placed near their supply chain dependencies.

**Calculation:**
```
supply_chain_modifier = 1.0 + sum(proximity_bonuses)

where:
proximity_bonus = base_bonus * (1 - distance / max_distance)

- base_bonus = 0.05 (5% per supply chain building)
- max_distance = 100 meters (bonus applies within this range)
- distance = meters to supply chain building
```

**Example:**
- Building: Smithy (requires Ironworks for iron ingots)
- Ironworks located 50 meters away
- Proximity bonus = 0.05 * (1 - 50/100) = 0.05 * 0.5 = 0.025 (2.5%)
- Supply chain modifier = 1.0 + 0.025 = 1.025

**Multiple Supply Chains:**
- Buildings can have multiple supply chain dependencies
- Each dependency provides its own proximity bonus
- Bonuses stack additively

**Supply Chain Types:**
- **Direct Supply**: Building requires output from another building (e.g., Smithy needs Ironworks)
- **Resource Proximity**: Building benefits from nearby resource nodes (e.g., Timberworks near forests)

#### 6. Condition Modifier (`condition_modifier`)

Building condition (health, durability, maintenance) affects production rates.

**Calculation:**
```
condition_modifier = (building_health / max_health) * (building_durability / max_durability) * maintenance_modifier

where:
- building_health = current health (0 to max_health)
- building_durability = current durability (0 to max_durability)
- maintenance_modifier = 1.0 if maintenance is current, 0.8 if overdue
```

**Example:**
- Building health: 800 / 1000 (80%)
- Building durability: 900 / 1000 (90%)
- Maintenance: Current (1.0)
- Condition modifier = 0.8 * 0.9 * 1.0 = 0.72 (28% penalty)

**Penalties:**
- Buildings below 50% health/durability: Additional 10% penalty
- Buildings below 25% health/durability: Additional 20% penalty
- Buildings at 0%: Cannot produce (must be repaired)

#### 7. Qi Modifier (`qi_modifier`)

Local ambient qi level at building position affects production efficiency for qi-sensitive buildings. Proximity to qi sources increases local ambient qi.

**Calculation:**
```
local_ambient_qi = territory_base_ambient_qi * proximity_modifier

qi_modifier = 1.0 + (local_ambient_qi / 500) * 0.2

where:
- territory_base_ambient_qi = base ambient qi in territory (0 to 1000)
- proximity_modifier = 1.0 + (qi_source_proximity_bonus * distance_factor)
  - distance_factor = 1.0 - (distance_to_qi_source / 500)
  - qi_source_proximity_bonus = 0.5 for mana veins, 1.0 for mana pools
  - max_qi_source_range = 500 meters
- local_ambient_qi = local qi at building position (can exceed 1000 near strong sources)
- Maximum qi bonus = 0.4 (40% bonus at 1000+ local qi)
- Minimum qi modifier = 0.8 (20% penalty at 0 local qi)
```

**Example:**
- Territory base ambient qi: 200
- Building located 100m from mana pool
- Distance factor = 1.0 - (100 / 500) = 0.8
- Proximity modifier = 1.0 + (1.0 * 0.8) = 1.8
- Local ambient qi = 200 * 1.8 = 360
- Qi modifier = 1.0 + (360 / 500) * 0.2 = 1.0 + 0.144 = 1.144 (14.4% bonus)

**Qi-Sensitive Buildings:**
- Not all buildings are affected by qi
- Buildings that produce qi-related resources (mana crystals, essence stones) are most affected
- Production buildings (smithy, timberworks) are less affected
- Buildings that consume qi are penalized at low qi levels

### Final Production Rate

**Complete Example:**

Building: Timberworks Tier 3
- Base rate: 50 lumber/day
- Workers: 3 workers, average Logging skill 60 → skill modifier = 1.06
- Tier 3 → building modifier = 1.10
- Signature addition (+10%) → building modifier = 1.10 * 1.10 = 1.21
- District: 4 buildings → district modifier = 1.06
- Supply chain: Ironworks 30m away → supply chain modifier = 1.035
- Condition: 90% health, 95% durability, maintenance current → condition modifier = 0.855
- Ambient qi: 200 → qi modifier = 1.08

Final rate = 50 * 1.06 * 1.21 * 1.06 * 1.035 * 0.855 * 1.08
           = 50 * 1.28
           = 64 lumber/day

## Processing Time Calculations

For buildings that process resources (not passive generation), processing time is calculated separately.

### Processing Time Formula

```
final_processing_time = base_processing_time * skill_modifier * building_modifier * condition_modifier
```

**Components:**
- **Base Processing Time**: From building type/recipe definition
- **Skill Modifier**: Workers with relevant skills reduce processing time
- **Building Modifier**: Tier and signature additions reduce processing time
- **Condition Modifier**: Building condition affects processing speed

**Skill Modifier for Processing:**
```
skill_modifier = 1.0 - (sum(worker_skill_bonus) / max(assigned_workers, 1))

where:
worker_skill_bonus = (worker_skill_level / 100) * time_reduction_per_level
time_reduction_per_level = 0.005 (0.5% per skill level)
```

**Example:**
- Base processing time: 100 seconds
- Worker skill level 80 → skill bonus = 0.8 * 0.005 = 0.004 (0.4% reduction)
- Skill modifier = 1.0 - 0.004 = 0.996
- Final processing time = 100 * 0.996 = 99.6 seconds

**Time Reduction Caps:**
- Maximum time reduction from skills: 50% (processing time cannot be reduced below 50% of base)
- Maximum time reduction from building modifiers: 30% (total reduction cap: 80%)

## Resource Collection Mechanics

### Passive Resource Accumulation

Buildings with passive resource generation accumulate resources over time.

**Accumulation Rate:**
```
accumulation_rate = final_production_rate / 24  [resources per hour]

accumulated_resources = accumulation_rate * time_elapsed_hours
```

**Storage Limits:**
- Each building has a `storage_capacity` (based on building type and tier)
- When storage is full, production stops
- Players must collect resources to free storage space

**Collection Process:**
1. Player interacts with building
2. Player requests resource collection
3. Server transfers accumulated resources to player inventory/storage
4. Building storage is reset to 0
5. Production resumes

### Collection Timing

**Automatic Collection:**
- Resources can be collected at any time
- No penalty for delayed collection
- Resources accumulate indefinitely (until storage full)

**Optimal Collection:**
- Collect frequently to maximize production (prevents storage overflow)
- Collect infrequently to reduce micromanagement (but risk storage overflow)

## Examples

### Example 1: Simple Passive Generation

**Building:** Farmland Tier 2
- Base rate: 25 food/day
- No workers assigned
- No district
- No supply chain
- Condition: 100% health, 100% durability, maintenance current
- Ambient qi: 150 (not qi-sensitive)

**Calculation:**
- Base rate: 25
- Skill modifier: 1.0 (no workers)
- Building modifier: 1.05 (Tier 2)
- District modifier: 1.0 (no district)
- Supply chain modifier: 1.0 (no supply chain)
- Condition modifier: 1.0 (perfect condition)
- Qi modifier: 1.0 (not qi-sensitive)

Final rate = 25 * 1.0 * 1.05 * 1.0 * 1.0 * 1.0 * 1.0 = 26.25 food/day

### Example 2: Complex Production with All Modifiers

**Building:** Qi Condenser Spire Tier 4
- Base rate: 2 mana crystals/day
- Workers: 2 workers, average Crystal Refining skill 75
- Tier 4 with signature addition (+15% production)
- District: 6 buildings
- Supply chain: Spirit Lode 40m away
- Condition: 85% health, 90% durability, maintenance current
- Ambient qi: 400 (qi-sensitive building)

**Calculation:**
- Base rate: 2
- Skill modifier: 1.0 + (0.75 * 0.01 * 2) / 2 = 1.0075
- Building modifier: 1.15 * 1.15 = 1.3225 (Tier 4 + signature)
- District modifier: 1.0 + (6-1) * 0.02 = 1.10
- Supply chain modifier: 1.0 + 0.05 * (1 - 40/100) = 1.03
- Condition modifier: 0.85 * 0.90 * 1.0 = 0.765
- Qi modifier: 1.0 + (400/500) * 0.2 = 1.16

Final rate = 2 * 1.0075 * 1.3225 * 1.10 * 1.03 * 0.765 * 1.16
           = 2 * 1.52
           = 3.04 mana crystals/day

### Example 3: Processing Time Calculation

**Building:** Alchemists Hall Tier 3
- Processing recipe: Elixir of Healing
- Base processing time: 300 seconds (5 minutes)
- Workers: 3 workers, average Alchemy skill 65
- Tier 3 with signature addition (+10% speed)
- Condition: 95% health, 100% durability, maintenance current

**Calculation:**
- Base time: 300 seconds
- Skill modifier: 1.0 - (0.65 * 0.005 * 3) / 3 = 1.0 - 0.00325 = 0.99675
- Building modifier: 1.0 - 0.10 = 0.90 (10% speed bonus = 10% time reduction)
- Condition modifier: 0.95 * 1.0 * 1.0 = 0.95

Final time = 300 * 0.99675 * 0.90 * 0.95
           = 300 * 0.852
           = 255.6 seconds (4 minutes 15 seconds)

## Modifier Stacking Rules

### Multiplicative Modifiers
- Skill, Building, District, Supply Chain, Condition, Qi modifiers stack multiplicatively
- Formula: `final_rate = base_rate * mod1 * mod2 * mod3 * ...`

### Additive Sub-Modifiers
- Within each modifier category, sub-modifiers are additive
- Example: Tier bonus + Signature bonus = (1.0 + tier_bonus) * (1.0 + signature_bonus)

### Maximum Bonuses
- **Skill Bonus**: Maximum 100% per worker (skill level 100)
- **Building Bonus**: No maximum (limited by tier and signature additions)
- **District Bonus**: Maximum 20% (11+ buildings)
- **Supply Chain Bonus**: Maximum 5% per dependency (diminishing with distance)
- **Condition Penalty**: Maximum 100% penalty (building at 0% health/durability)
- **Qi Bonus**: Maximum 40% (at 1000 ambient qi)

### Minimum Values
- **Production Rate**: Cannot go below 0 (building stops producing)
- **Processing Time**: Cannot be reduced below 50% of base time
- **Condition Modifier**: Cannot go below 0 (building destroyed)

## Notes

- Production rates are calculated **per building instance**
- Multiple buildings of the same type = multiple production streams
- Rates are calculated **server-side** every tick (every 1-2 seconds)
- Rates are **cached** and only recalculated when modifiers change
- Players see **estimated rates** in UI (actual rates may vary slightly)
- Production continues **24/7** even when players are offline
- Resources accumulate and must be collected by players

---

**Last Updated:** 2025-11-05

