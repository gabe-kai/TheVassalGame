# Combat Mechanics

## Table of Contents
- [Overview](#overview)
- [Combat Stat Calculations](#combat-stat-calculations)
- [Damage Formulas](#damage-formulas)
- [Defense and Armor](#defense-and-armor)
- [Techniques System](#techniques-system)
- [Qi Usage in Combat](#qi-usage-in-combat)
- [Weapons and Equipment](#weapons-and-equipment)
- [Ego Score and Behavior](#ego-score-and-behavior)
- [Combat Accuracy and Hit Chance](#combat-accuracy-and-hit-chance)
- [Critical Hits and Evasion](#critical-hits-and-evasion)
- [Status Effects](#status-effects)
- [Combat Types](#combat-types)
- [Combat AI Behavior](#combat-ai-behavior)
- [Combat Ranges](#combat-ranges)
- [Database Schema Updates](#database-schema-updates)

## Overview

Combat in TheVassalGame follows a standard top-down RPG system where individual units engage in tactical combat based on their stats, skills, techniques, and equipment. The system emphasizes the difference between mortals and cultivators, with cultivators using Qi to enhance their combat effectiveness and execute powerful techniques.

**Key Principles:**
- **Stat-Based Combat**: All combat effectiveness derives from character stats (body, mind, spirit, and expanded stats)
- **Skill Modifiers**: Skills directly influence combat effectiveness (Combat, Archery, Qi Manipulation, etc.)
- **Technique System**: Units learn and execute combat techniques that consume Qi or stamina
- **Qi Enhancement**: Cultivators use Qi to enhance their bodies and weapons during combat
- **Equipment Matters**: Weapons and armor provide significant combat bonuses
- **Ego System**: All units have an ego score that affects behavior, especially cultivators who may act independently

---

## Combat Stat Calculations

### Base Combat Stats

All units calculate combat effectiveness from their character sheet stats:

**Physical Combat Stats:**
- **Attack Power**: `strength + (body / 2) + weapon_attack_bonus`
- **Defense**: `endurance + (body / 2) + armor_defense_bonus`
- **Speed**: `speed + agility` (affects action order and dodge)
- **Health**: `max_health` (derived from `vitality + body`)
- **Stamina Capacity**: `50 + (endurance × 2) + (vitality × 2)` (mortals), `Base + (cultivation_level × 5)` (cultivators)
- **Stamina Regeneration**: `1 + (endurance / 10)` per second (out of combat), `0.5 + (endurance / 20)` per second (in combat)

**Mental Combat Stats:**
- **Technique Accuracy**: `intellect + perception + (mind / 2)`
- **Resistance**: `willpower + (mind / 2)` (resistance to mental effects)
- **Focus**: `focus + (mind / 2)` (reduces technique failure chance)

**Spiritual Combat Stats (Cultivators Only):**
- **Qi Power**: `spirit_power + (spirit / 2)` (affects Qi-based techniques)
- **Qi Efficiency**: `resonance + clarity` (reduces Qi cost of techniques)
- **Attunement Bonus**: `attunement` (bonus to techniques matching primary attunement)

### Skill Modifiers

Skills directly modify combat stats:

- **Combat Skill**: +1% to attack power per skill level (max +50%)
- **Archery Skill**: +1% to ranged attack accuracy per skill level (max +50%)
- **Defense Skill**: +1% to defense per skill level (max +50%)
- **Qi Manipulation**: +1% to Qi technique power per skill level (max +50%)
- **Stealth Skill**: +1% to evasion per skill level (max +50%)

**Formula Example:**
```
Final Attack Power = Base Attack Power × (1 + (Combat_Skill_Level / 100))
```

### Cultivation Level Bonuses

Cultivators gain combat bonuses based on cultivation tier:

- **Tier 1-4**: +5% to all combat stats per tier
- **Tier 5-9**: +10% to all combat stats per tier
- **Tier 10-14**: +15% to all combat stats per tier
- **Tier 15-19**: +20% to all combat stats per tier
- **Tier 20+**: +25% to all combat stats per tier

**Formula:**
```
Cultivation Bonus = Base Stat × (1 + (Cultivation_Tier × Tier_Bonus_Percent))
```

---

## Damage Formulas

### Physical Damage

**Base Physical Damage:**
```
Physical Damage = Attack Power × (1 + Weapon_Damage_Multiplier) × Technique_Multiplier
```

**Defense Reduction:**
```
Final Damage = Physical Damage × (1 - (Defense / (Defense + 100)))
```

**Example:**
- Attack Power: 50
- Weapon Multiplier: 1.5 (150% damage weapon)
- Defense: 30
- Calculation: `50 × 1.5 × (1 - (30 / (30 + 100))) = 75 × 0.77 = 57.75 damage`

### Qi-Based Damage (Cultivators)

**Base Qi Damage:**
```
Qi Damage = (Qi_Power × Technique_Power) + (Qi_Spent × Qi_Efficiency)
```

**Qi Resistance:**
```
Final Qi Damage = Qi Damage × (1 - (Target_Resistance / (Target_Resistance + 100)))
```

**Resistance Calculation:**
- Mortals: `Resistance = willpower + (mind / 2)`
- Cultivators: `Resistance = willpower + clarity + (mind / 2) + (spirit / 2)`

### Hybrid Damage

Some techniques combine physical and Qi damage:
```
Hybrid Damage = (Physical Damage × Physical_Ratio) + (Qi Damage × Qi_Ratio)
```

---

## Defense and Armor

### Armor Types

**Light Armor:**
- Defense Bonus: +5 to +15
- Speed Penalty: -0% to -5%
- Qi Restriction: None

**Medium Armor:**
- Defense Bonus: +15 to +30
- Speed Penalty: -5% to -10%
- Qi Restriction: -5% Qi efficiency

**Heavy Armor:**
- Defense Bonus: +30 to +50
- Speed Penalty: -10% to -20%
- Qi Restriction: -15% Qi efficiency (cultivators prefer lighter armor)

### Defense Calculation

**Total Defense:**
```
Total Defense = Base Defense + Armor Defense + Skill Defense Bonus + Qi Enhancement
```

**Defense Effectiveness:**
- Defense reduces damage by a diminishing returns formula
- Higher defense provides less relative protection as it increases
- Formula: `Damage Reduction = Defense / (Defense + 100)`

**Example:**
- 10 Defense: 9.1% damage reduction
- 50 Defense: 33.3% damage reduction
- 100 Defense: 50% damage reduction
- 200 Defense: 66.7% damage reduction

---

## Techniques System

### Technique Categories

**Physical Techniques:**
- Require stamina (mortals) or minimal Qi (cultivators)
- Examples: Power Strike, Sweep, Shield Bash, Piercing Thrust

**Qi Techniques (Cultivators Only):**
- Require Qi to execute
- Examples: Qi Blast, Elemental Strike, Qi Shield, Healing Wave

**Hybrid Techniques:**
- Combine physical and Qi power
- Examples: Qi-Enhanced Strike, Elemental Weapon, Body Reinforcement

### Technique Learning

**Technique Sources:**
- **Skill Progression**: Units learn techniques as they level up skills
- **Cultivation Tiers**: Cultivators unlock techniques at specific tiers
- **Training**: Units can learn techniques from trainers or manuals
- **Combat Experience**: Rare techniques may unlock during combat

**Technique Tiers:**
- **Basic Techniques**: Available at skill level 1-5
- **Intermediate Techniques**: Available at skill level 6-15
- **Advanced Techniques**: Available at skill level 16-25
- **Master Techniques**: Available at skill level 26+ or specific cultivation tiers

### Technique Properties

Each technique has:
- **Name**: Technique identifier
- **Type**: Physical, Qi, or Hybrid
- **Cost**: Stamina or Qi required
- **Damage Multiplier**: Multiplier to base attack power
- **Range**: Melee, short-range, medium-range, long-range
- **Cooldown**: Time before technique can be used again
- **Special Effects**: Status effects, area of effect, etc.

**Example Technique:**
```
Power Strike (Physical)
- Cost: 20 Stamina
- Damage Multiplier: 1.5x
- Range: Melee
- Cooldown: 3 seconds
- Special: Stuns target on critical hit
```

---

## Qi Usage in Combat

### Body Enhancement (Cultivators)

Cultivators can channel Qi to enhance their combat capabilities:

**Qi Body Reinforcement:**
- **Cost**: 5 Qi per second
- **Effect**: +20% to all physical stats while active
- **Duration**: While Qi is being channeled
- **Limit**: Cannot exceed Qi pool capacity

**Qi Speed Enhancement:**
- **Cost**: 3 Qi per second
- **Effect**: +30% to speed and agility
- **Duration**: While Qi is being channeled

**Qi Defense Enhancement:**
- **Cost**: 4 Qi per second
- **Effect**: +25% to defense
- **Duration**: While Qi is being channeled

### Weapon Enhancement

Cultivators can enhance weapons with Qi:

**Qi Weapon Infusion:**
- **Cost**: 10 Qi (one-time for combat)
- **Effect**: Weapon deals +50% Qi damage on top of physical damage
- **Duration**: Until combat ends or weapon is dropped

**Elemental Weapon:**
- **Cost**: 15 Qi + attunement matching
- **Effect**: Weapon gains elemental properties matching primary attunement
- **Special**: +25% damage bonus against weak elements

### Technique Execution

Qi techniques require Qi to execute:
- **Basic Qi Techniques**: 10-30 Qi
- **Intermediate Qi Techniques**: 30-60 Qi
- **Advanced Qi Techniques**: 60-100 Qi
- **Master Qi Techniques**: 100-200+ Qi

**Qi Efficiency:**
- Higher `resonance` and `clarity` stats reduce Qi costs
- Formula: `Actual Qi Cost = Base Qi Cost × (1 - (Qi_Efficiency / 200))`
- Minimum: 50% of base cost (cannot reduce below this)

---

## Weapons and Equipment

### Weapon Types

**Melee Weapons:**
- **Swords**: Balanced damage and speed (+10-20 attack, +5% speed)
- **Axes**: High damage, slow speed (+15-25 attack, -10% speed)
- **Staffs**: Medium damage, Qi bonus (+8-15 attack, +10% Qi efficiency)
- **Spears**: Long reach, balanced (+10-18 attack, +10% range)

**Ranged Weapons:**
- **Bows**: High accuracy, medium damage (+8-15 attack, +20% accuracy)
- **Crossbows**: High damage, slow reload (+12-20 attack, -15% reload speed)
- **Qi Projectors**: Qi-based ranged (cultivators only, +15-25 Qi damage)

### Weapon Properties

**Weapon Stats:**
- **Attack Bonus**: Direct addition to attack power
- **Damage Multiplier**: Multiplier to base damage
- **Speed Modifier**: Percentage change to attack speed
- **Range**: Maximum attack distance
- **Special Properties**: Critical hit chance, elemental damage, etc.

**Weapon Quality Tiers:**
- **Crude**: +5-10 attack, basic properties
- **Standard**: +10-15 attack, standard properties
- **Fine**: +15-20 attack, +5% critical chance
- **Masterwork**: +20-25 attack, +10% critical chance, special properties
- **Cultivator-Grade**: +25-35 attack, +15% critical chance, Qi enhancement compatible

### Equipment Slots

Each unit can equip:
- **Weapon**: One primary weapon (melee or ranged)
- **Armor**: One armor piece (light, medium, or heavy)
- **Accessory 1**: Ring, amulet, or talisman
- **Accessory 2**: Second ring, amulet, or talisman
- **Qi Focus** (Cultivators Only): Special item that enhances Qi techniques

**Equipment Bonuses:**
- Accessories provide small bonuses (+1-5 to specific stats)
- Qi Focus items provide Qi efficiency bonuses (+5-15% Qi efficiency)

---

## Ego Score and Behavior

### Ego Score System

All units have an **ego score** (0-100) that affects their behavior:

**Ego Score Calculation:**
```
Base Ego = charisma + (willpower / 2)
Cultivator Bonus = +10 per cultivation tier (Tier 1-4), +15 per tier (Tier 5+)
Final Ego = Base Ego + Cultivator Bonus + Personality Traits
```

**Ego Ranges:**
- **0-20**: Humble, obedient, follows orders
- **21-40**: Cooperative, follows orders with minor independence
- **41-60**: Balanced, follows orders but may suggest alternatives
- **61-80**: Proud, may question orders, seeks recognition
- **81-100**: Arrogant, frequently acts independently, seeks glory

### Cultivator Glory-Seeking Behavior

Cultivators have a natural tendency to seek glory rather than following commands:

**Glory-Seeking Triggers:**
- **High Ego Score**: Ego > 60 increases glory-seeking behavior
- **Cultivation Tier**: Higher tiers increase glory-seeking (Tier 10+: +20% chance)
- **Combat Opportunities**: Seeing enemy units or combat nearby
- **Heroic Moments**: Opportunities to save allies, defeat powerful enemies

**Independence Behavior:**
- **Leave Post**: Cultivator may abandon assigned position to engage in combat
- **Charge Ahead**: Cultivator may ignore defensive orders to attack
- **Heroic Actions**: Cultivator may attempt risky but impressive actions
- **Disobedience**: Cultivator may refuse orders that conflict with their ego

**Ego-Based Actions:**
- **Ego 60-80**: 10-20% chance to act independently per combat round
- **Ego 81-100**: 30-50% chance to act independently per combat round
- **Cultivation Tier 10+**: +15% to independence chance

**Command Resistance:**
```
Order Acceptance Chance = 100% - (Ego / 2) - (Cultivation_Tier × 2)
```

**Example:**
- Ego 70, Tier 5: `100% - 35% - 10% = 55% chance to follow orders`

### Managing Cultivator Ego

**Ways to Reduce Independence:**
- **Respect**: Acknowledging cultivator's achievements (+5 to order acceptance)
- **Autonomy**: Allowing cultivator to choose targets (+10 to order acceptance)
- **Glory Opportunities**: Assigning cultivator to prestigious positions (+15 to order acceptance)
- **Personal Relationship**: High relationship with player (+10 to order acceptance)

**Consequences of High Ego:**
- Cultivators may achieve impressive victories independently
- Cultivators may take unnecessary risks
- Cultivators may abandon defensive positions
- Cultivators may challenge player authority

---

## Combat Accuracy and Hit Chance

### Accuracy Calculation

**Base Accuracy:**
```
Base Accuracy = 75% + (Perception / 2) + (Agility / 4) + Skill_Bonus
```

**Skill Bonuses:**
- Combat Skill: +1% per level
- Archery Skill: +2% per level (ranged attacks only)
- Technique Mastery: +5% per technique tier

**Target Evasion:**
```
Evasion = (Agility / 2) + (Speed / 4) + Skill_Bonus + Equipment_Bonus
```

**Final Hit Chance:**
```
Hit Chance = Base Accuracy - (Target Evasion / 2)
Minimum: 10% (always a chance to hit)
Maximum: 95% (always a chance to miss)
```

### Range Modifiers

**Range Penalties:**
- **Melee**: No penalty
- **Short Range** (5-15m): -5% accuracy
- **Medium Range** (15-30m): -15% accuracy
- **Long Range** (30-50m): -30% accuracy
- **Extreme Range** (50m+): -50% accuracy

---

## Critical Hits and Evasion

### Critical Hit System

**Critical Hit Chance:**
```
Base Critical Chance = 5% + (Agility / 10) + (Charisma / 20) + (Spirit / 40) + Equipment_Bonus
```

**Note:** Luck is derived from `charisma + (spirit / 2)` rather than being a separate stat.

**Critical Hit Damage:**
```
Critical Damage = Base Damage × 2.0 + (Critical_Modifier / 100)
```

**Critical Modifiers:**
- Weapons: +0% to +15% critical chance
- Techniques: Some techniques have higher critical chance
- Skills: Critical Hit skill increases critical chance and damage

**Critical Hit Effects:**
- **Physical Critical**: Double damage, may cause stun
- **Qi Critical**: Double damage, may cause elemental effects
- **Technique Critical**: Technique special effects guaranteed

### Evasion System

**Dodge Chance:**
```
Dodge Chance = (Agility / 2) + (Speed / 4) + Skill_Bonus - Attacker_Accuracy_Bonus
Maximum: 50% (cannot dodge more than half of attacks)
```

**Evasion Types:**
- **Dodge**: Complete avoidance of attack (no damage)
- **Partial Dodge**: Reduce damage by 50%
- **Qi Dodge** (Cultivators): Uses Qi to enhance dodge chance (+10-20%)

**Evasion Modifiers:**
- Stealth Skill: +1% evasion per skill level
- Terrain: Cover provides +10-20% evasion
- Technique: Some techniques provide temporary evasion bonuses

---

## Status Effects

### Physical Status Effects

**Stun:**
- **Duration**: 1-3 seconds
- **Effect**: Cannot act, -50% evasion
- **Source**: Critical hits, specific techniques

**Bleed:**
- **Duration**: 5-10 seconds
- **Effect**: Damage over time (2-5 damage per second)
- **Source**: Slashing weapons, specific techniques

**Slow:**
- **Duration**: 3-5 seconds
- **Effect**: -30% speed and agility
- **Source**: Frost techniques, terrain effects

### Mental Status Effects

**Confusion:**
- **Duration**: 3-5 seconds
- **Effect**: Random actions, reduced accuracy
- **Source**: Mental techniques, specific Qi abilities

**Fear:**
- **Duration**: 5-10 seconds
- **Effect**: Reduced attack power, may flee
- **Source**: Intimidation techniques, high-tier cultivators

### Elemental Status Effects (Cultivators)

**Burn:**
- **Duration**: 5-8 seconds
- **Effect**: Fire damage over time (3-8 damage per second)
- **Source**: Fire Qi techniques

**Freeze:**
- **Duration**: 3-5 seconds
- **Effect**: Immobilized, -50% speed
- **Source**: Water/Ice Qi techniques

**Poison:**
- **Duration**: 10-15 seconds
- **Effect**: Damage over time (2-4 damage per second), reduced healing
- **Source**: Poison Qi techniques, venomous weapons

**Shock:**
- **Duration**: 2-3 seconds
- **Effect**: Stun, reduced Qi efficiency
- **Source**: Lightning Qi techniques

### Status Effect Resistance

**Resistance Calculation:**
```
Status Resistance = Willpower + (Mind / 2) + Equipment_Bonus
```

**Resistance Check:**
```
Status Applied = Base Status Chance × (1 - (Resistance / 200))
```

---

## Combat Types

### Player vs NPC Combat

**Mechanics:**
- Player controls avatar directly
- NPCs use AI behavior
- Standard combat formulas apply
- Player can use techniques manually

**Special Considerations:**
- Player has tactical advantage (human intelligence)
- NPCs follow behavior patterns
- Cultivator NPCs may act independently based on ego

### NPC vs NPC Combat

**Mechanics:**
- Both units use AI behavior
- Combat resolves automatically
- Ego affects both units' behavior
- Techniques used based on AI decisions

**Special Considerations:**
- Cultivator NPCs may seek glory, abandoning defensive positions
- High ego NPCs may challenge each other
- NPCs may form temporary alliances

### Building Defense/Attack

**Building Defense:**
- Buildings have health and durability
- Buildings can be attacked by units
- Building defense: `max_health + (durability / 2)`
- Buildings may have defensive structures (towers, walls)

**Building Attack:**
- Some buildings can attack (towers, defensive structures)
- Building attack power: Based on building tier and type
- Building range: Determined by building type
- Buildings use automated targeting

**Siege Mechanics:**
- Units can attack buildings
- Buildings have high health but low mobility
- Siege weapons provide bonus damage to buildings
- Buildings can be destroyed (reduced to 0 health)

### Territory Defense

**Territory Defense:**
- Defending units gain +10% to all combat stats
- Defending units know terrain (cover bonuses)
- Defending units can use defensive structures

**Invasion Mechanics:**
- Attacking units have -5% to combat stats (terrain unfamiliarity)
- Attacking units may face traps or defensive formations
- Territory owner can assign defenders to key positions

---

## Combat AI Behavior

### Basic Combat AI

**Combat States:**
1. **Idle**: No combat, normal behavior
2. **Alert**: Enemy detected, preparing for combat
3. **Engaging**: Moving to attack range
4. **Attacking**: Using attacks and techniques
5. **Defending**: Blocking, dodging, using defensive techniques
6. **Retreating**: Health low, fleeing combat
7. **Chasing**: Pursuing fleeing enemy

**Target Selection:**
- **Priority 1**: Attacking units (defend self)
- **Priority 2**: Weakest enemies (opportunity)
- **Priority 3**: Closest enemies (efficiency)
- **Priority 4**: High-value targets (cultivators, leaders)

**Ego-Based Target Selection:**
- High ego units prefer challenging targets (strong enemies, cultivators)
- High ego units may ignore weak targets to engage stronger ones
- High ego units may seek to defeat enemy leaders

### Cultivator Combat AI

**Cultivator Behavior:**
- **Ego 60-80**: May seek impressive targets, may abandon position for glory
- **Ego 81-100**: Frequently seeks challenging combat, may ignore orders
- **Cultivation Tier 10+**: Prefers to fight other cultivators

**Glory-Seeking Actions:**
- Charge into enemy formations
- Challenge enemy cultivators
- Attempt to defeat multiple enemies alone
- Abandon defensive positions to engage in combat

**Technique Usage:**
- Cultivators prefer Qi techniques over physical techniques
- Cultivators use body enhancement when possible
- Cultivators save powerful techniques for important moments (unless ego is very high)

### Combat Decision Tree

**Combat Decision Priority:**
1. **Health Check**: If health < 30%, consider retreating (unless ego is very high)
2. **Ego Check**: If ego > 80, consider glory-seeking actions
3. **Target Selection**: Choose target based on priority and ego
4. **Technique Selection**: Choose technique based on available resources and situation
5. **Positioning**: Move to optimal position (unless ego overrides)

---

## Combat Ranges

### Range Categories

**Melee Range (0-2m):**
- Swords, axes, staffs, spears
- No accuracy penalty
- Can be blocked by shields or weapons

**Short Range (2-10m):**
- Spears, some techniques
- -5% accuracy penalty
- Still within melee weapon reach

**Medium Range (10-30m):**
- Bows, crossbows, Qi projectors
- -15% accuracy penalty
- Requires ranged weapons or techniques

**Long Range (30-50m):**
- Advanced bows, Qi projectors
- -30% accuracy penalty
- Requires specialized equipment

**Extreme Range (50m+):**
- Master techniques, siege weapons
- -50% accuracy penalty
- Rare and powerful

### Range Modifiers

**Cover:**
- Partial cover: +10% evasion
- Full cover: +30% evasion, blocks line of sight

**Terrain:**
- Elevation advantage: +5% accuracy
- Difficult terrain: -10% speed, affects positioning

---

## Database Schema Updates

### Database Schema

All combat-related database tables and fields are defined in `docs/database-schema.md`:

**New Tables:**
- `techniques` - Combat techniques that units can learn
- `unit_techniques` - Tracks which techniques units have learned
- `weapons` - Weapon items that can be equipped
- `armor` - Armor items that can be equipped
- `accessories` - Accessory items (rings, amulets, talismans, Qi focus)

**Updated Tables:**
- `avatars` - Added combat fields: `ego_score`, equipment fields, combat state
- `npcs` - Added combat fields: `ego_score`, equipment fields, combat state
- `buildings` - Added combat capabilities: `can_attack`, `attack_power`, `attack_range`, `defense_bonus`

See `docs/database-schema.md` for complete table definitions and field descriptions.

---

## Summary

The combat system provides:
- **Stat-based combat** with clear formulas for damage, defense, and accuracy
- **Technique system** allowing units to learn and execute powerful abilities
- **Qi integration** for cultivators to enhance combat effectiveness
- **Equipment system** with weapons, armor, and accessories
- **Ego system** affecting unit behavior, especially cultivators who may act independently
- **Comprehensive AI** for NPC combat behavior
- **Status effects** for tactical depth
- **Multiple combat types** supporting various gameplay scenarios

The system emphasizes the difference between mortals and cultivators while maintaining balance and coherence across all combat interactions.

---

**Last Updated:** 2025-11-05

