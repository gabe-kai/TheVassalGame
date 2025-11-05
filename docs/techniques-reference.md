# Techniques Reference

## Table of Contents
- [Overview](#overview)
- [Physical Techniques](#physical-techniques)
- [Qi Techniques](#qi-techniques)
- [Hybrid Techniques](#hybrid-techniques)

## Overview

Techniques are combat abilities that units can learn and execute during combat. Techniques are categorized by their power source (physical, qi, or hybrid) and organized into tiers (basic, intermediate, advanced, master). Mortals can learn physical techniques, while cultivators can learn all types, with higher-tier techniques requiring specific cultivation levels.

**Technique Properties:**
- **Category**: Physical (stamina-based), Qi (qi-based), or Hybrid (both)
- **Tier**: Basic, Intermediate, Advanced, or Master
- **Cost**: Stamina for mortals, Qi for cultivators, or hybrid costs
- **Damage Multiplier**: Multiplier to base attack power
- **Range**: Melee, short, medium, long, or extreme range
- **Cooldown**: Time before technique can be used again
- **Special Effects**: Status effects, area of effect, etc.

**Learning Requirements:**
- Physical techniques typically require Combat skill
- Qi techniques require cultivation tier and Qi Manipulation skill
- Hybrid techniques may require both
- Some techniques unlock at specific cultivation tiers

## Physical Techniques

### Basic Tier

#### Power Strike
- **Description**: A powerful physical strike that channels strength into a single devastating blow.
- **Category**: Physical
- **Tier**: Basic
- **Cost**: 20 Stamina
- **Damage Multiplier**: 1.5x
- **Range**: Melee (2m)
- **Cooldown**: 3 seconds
- **Special Effects**: Stuns target on critical hit
- **Required Skill**: Combat (Level 1)

#### Shield Bash
- **Description**: A defensive technique using shield or weapon to bash and stagger enemies.
- **Category**: Physical
- **Tier**: Basic
- **Cost**: 15 Stamina
- **Damage Multiplier**: 1.2x
- **Range**: Melee (2m)
- **Cooldown**: 4 seconds
- **Special Effects**: Reduces target speed by 20% for 3 seconds
- **Required Skill**: Combat (Level 1), Defense (Level 1)

#### Piercing Thrust
- **Description**: A precise thrust attack that pierces through armor.
- **Category**: Physical
- **Tier**: Basic
- **Cost**: 18 Stamina
- **Damage Multiplier**: 1.3x
- **Range**: Short (5m)
- **Cooldown**: 3 seconds
- **Special Effects**: Ignores 25% of target's defense
- **Required Skill**: Combat (Level 2)

#### Sweep
- **Description**: A wide horizontal sweep that can hit multiple enemies.
- **Category**: Physical
- **Tier**: Basic
- **Cost**: 22 Stamina
- **Damage Multiplier**: 1.2x
- **Range**: Melee (2m)
- **Cooldown**: 5 seconds
- **Special Effects**: Area of effect (120° arc, 3m radius)
- **Required Skill**: Combat (Level 3)

### Intermediate Tier

#### Whirlwind Strike
- **Description**: A spinning attack that strikes all nearby enemies.
- **Category**: Physical
- **Tier**: Intermediate
- **Cost**: 35 Stamina
- **Damage Multiplier**: 1.4x
- **Range**: Melee (3m radius)
- **Cooldown**: 8 seconds
- **Special Effects**: Full 360° area of effect, 3m radius
- **Required Skill**: Combat (Level 6)

#### Armor Breaker
- **Description**: A technique designed to shatter heavy armor and defenses.
- **Category**: Physical
- **Tier**: Intermediate
- **Cost**: 40 Stamina
- **Damage Multiplier**: 1.6x
- **Range**: Melee (2m)
- **Cooldown**: 6 seconds
- **Special Effects**: Reduces target's defense by 30% for 5 seconds
- **Required Skill**: Combat (Level 8)

## Qi Techniques

### Basic Tier (Cultivators Only)

#### Qi Blast
- **Description**: A basic ranged Qi attack that projects raw Qi energy at the target.
- **Category**: Qi
- **Tier**: Basic
- **Cost**: 25 Qi
- **Damage Multiplier**: 1.5x (Qi-based)
- **Range**: Medium (15m)
- **Cooldown**: 4 seconds
- **Special Effects**: None
- **Required Skill**: Qi Manipulation (Level 1)
- **Requires Cultivation Tier**: 1

#### Qi Shield
- **Description**: A defensive technique that creates a barrier of Qi to absorb damage.
- **Category**: Qi
- **Tier**: Basic
- **Cost**: 30 Qi
- **Damage Multiplier**: N/A (Defensive)
- **Range**: Self
- **Cooldown**: 10 seconds
- **Special Effects**: Absorbs 50 damage for 5 seconds
- **Required Skill**: Qi Manipulation (Level 2)
- **Requires Cultivation Tier**: 2

#### Healing Wave
- **Description**: Channels Qi to restore health to self or nearby allies.
- **Category**: Qi
- **Tier**: Basic
- **Cost**: 35 Qi
- **Damage Multiplier**: N/A (Healing)
- **Range**: Short (8m)
- **Cooldown**: 8 seconds
- **Special Effects**: Restores 20-40 health (based on spirit_power)
- **Required Skill**: Qi Manipulation (Level 2)
- **Requires Cultivation Tier**: 2

#### Elemental Strike (Fire)
- **Description**: A Qi attack infused with fire element, causing burning damage over time.
- **Category**: Qi
- **Tier**: Basic
- **Cost**: 30 Qi
- **Damage Multiplier**: 1.4x (Qi-based)
- **Range**: Short (10m)
- **Cooldown**: 5 seconds
- **Special Effects**: Applies Burn status (5-8 fire damage/second for 5 seconds)
- **Required Skill**: Qi Manipulation (Level 3)
- **Requires Cultivation Tier**: 3
- **Note**: Requires Fire Qi attunement

### Intermediate Tier (Cultivators Only)

#### Qi Chain
- **Description**: A Qi attack that chains between multiple enemies.
- **Category**: Qi
- **Tier**: Intermediate
- **Cost**: 45 Qi
- **Damage Multiplier**: 1.3x (Qi-based)
- **Range**: Medium (20m)
- **Cooldown**: 7 seconds
- **Special Effects**: Chains to up to 3 additional enemies within 5m of each other
- **Required Skill**: Qi Manipulation (Level 6)
- **Requires Cultivation Tier**: 5

#### Elemental Burst
- **Description**: A powerful area-of-effect elemental attack matching the cultivator's attunement.
- **Category**: Qi
- **Tier**: Intermediate
- **Cost**: 60 Qi
- **Damage Multiplier**: 1.8x (Qi-based)
- **Range**: Medium (15m radius)
- **Cooldown**: 12 seconds
- **Special Effects**: Area of effect (15m radius), elemental status effect based on attunement
- **Required Skill**: Qi Manipulation (Level 8)
- **Requires Cultivation Tier**: 7

## Hybrid Techniques

### Basic Tier (Cultivators Only)

#### Qi-Enhanced Strike
- **Description**: A physical attack enhanced with Qi, dealing both physical and Qi damage.
- **Category**: Hybrid
- **Tier**: Basic
- **Cost**: 20 Stamina + 15 Qi
- **Damage Multiplier**: 1.4x (Physical) + 0.6x (Qi)
- **Range**: Melee (2m)
- **Cooldown**: 4 seconds
- **Special Effects**: None
- **Required Skill**: Combat (Level 3), Qi Manipulation (Level 2)
- **Requires Cultivation Tier**: 3

#### Body Reinforcement
- **Description**: Temporarily enhances the body with Qi, increasing combat effectiveness.
- **Category**: Hybrid
- **Tier**: Basic
- **Cost**: 25 Qi (sustained, 5 Qi/second)
- **Damage Multiplier**: N/A (Buff)
- **Range**: Self
- **Cooldown**: 15 seconds
- **Special Effects**: +20% to all physical stats for 10 seconds
- **Required Skill**: Qi Manipulation (Level 3)
- **Requires Cultivation Tier**: 3

### Intermediate Tier (Cultivators Only)

#### Elemental Weapon
- **Description**: Infuses weapon with elemental Qi, adding elemental damage to attacks.
- **Category**: Hybrid
- **Tier**: Intermediate
- **Cost**: 40 Qi (one-time, lasts until combat ends)
- **Damage Multiplier**: N/A (Enhancement)
- **Range**: Self
- **Cooldown**: 20 seconds
- **Special Effects**: Weapon gains +50% Qi damage, +25% damage bonus against weak elements
- **Required Skill**: Qi Manipulation (Level 6)
- **Requires Cultivation Tier**: 5

#### Thunder Strike
- **Description**: A lightning-fast physical strike enhanced with Lightning Qi.
- **Category**: Hybrid
- **Tier**: Intermediate
- **Cost**: 30 Stamina + 35 Qi
- **Damage Multiplier**: 1.5x (Physical) + 0.8x (Qi)
- **Range**: Melee (2m)
- **Cooldown**: 6 seconds
- **Special Effects**: Applies Shock status (stun for 2 seconds, reduced Qi efficiency)
- **Required Skill**: Combat (Level 6), Qi Manipulation (Level 5)
- **Requires Cultivation Tier**: 6

---

**Last Updated:** 2025-11-05

