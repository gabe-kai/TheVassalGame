# Building Types Reference

This document contains the initial building types and their metadata for the game. This is a design reference document. For implementation, see seed data files in `server/data/seed/`.

## Table of Contents

### Resource Extraction & Processing
- [Timberworks](#timberworks-path) - Wood harvesting and lumber processing
- [Stoneworks](#stoneworks-path) - Stone extraction and processing
- [Farmland](#farmland-path) - Food production through cultivation
- [Spirit Garden](#spirit-garden-path) - Spirit herb cultivation
- [Waterworks](#waterworks-path) - Water collection and purification
- [Ironworks](#ironworks-path) - Iron ore and rare metal extraction
- [Qi Condenser Spire](#qi-condenser-spire-path) - Qi condensation into mana crystals
- [Condensation Pavilion](#condensation-pavilion-path) - Water vapor capture and purification

### Production & Manufacturing
- [Carpenter's Workshop](#carpenters-workshop-path) - Wooden tools and furniture
- [Stonecutting Yard](#stonecutting-yard-path) - Stone shaping and processing
- [Spirit Masonry Forge](#spirit-masonry-forge-path) - Spirit-infused stone blocks
- [Granary & Millhouse](#granary--millhouse-path) - Food processing and storage
- [Spiritual Kitchen](#spiritual-kitchen-path) - Spirit-infused meals
- [Drying Pavilion](#drying-pavilion-path) - Herb processing and refinement
- [Alchemists Hall](#alchemists-hall-path) - Potion and elixir crafting
- [Spiritwood Atelier](#spiritwood-atelier-path) - Spirit timber and specialized materials
- [Smithy](#smithy-path) - Weapons and armor crafting
- [Crystal Refinery](#crystal-refinery-path) - Crystal processing and refinement
- [Alloy Foundry](#alloy-foundry-path) - Metal smelting and alloy production
- [Spirit Lode](#spirit-lode-path) - Essence processing and refinement

### Defense & Fortifications
- [Fortified Wall](#fortified-wall-path) - Perimeter protection
- [Sentinel Tower](#sentinel-tower-path) - Observation and defensive support
- [Ward Bastion](#ward-bastion-path) - Protective barrier wards
- [Beastbane](#beastbane-path) - Anti-beast defensive systems
- [Rune Formation](#rune-formation-path) - Defensive formations

### Housing & Living
- [Personal Housing](#personal-housing-path) - Individual residences
- [Shared Housing](#shared-housing-path) - Communal residential spaces

### Civic & Administration
- [Sect Hall](#sect-hall-path) - Primary civic building
- [Sect Archive](#sect-archive-path) - Knowledge preservation and research
- [Discipline Hall](#discipline-hall-path) - Law enforcement and order
- [Meditation Hall](#meditation-hall-path) - Cultivation spaces

### Commerce & Culture
- [Artisan Guild Hall](#artisan-guild-hall-path) - Crafter coordination and prestige goods
- [Feast Hall](#feast-hall-path) - Communal dining and celebrations
- [Crystal Exchange Pavilion](#crystal-exchange-pavilion-path) - Crystal trading and resource exchange
- [Amphitheater](#amphitheater-path) - Entertainment and festival spaces
- [Diplomatic Embassy](#diplomatic-embassy-path) - Inter-sect relations

### Military & Adventuring
- [Adventurer's Guild Hall](#adventurers-guild-hall-path) - Mission coordination and beast trading
- [Training Grounds](#training-grounds-path) - Combat training and skill development
- [Inn](#inn-path) - Hospitality and recovery services

### Infrastructure & Logistics
- [Supply Depot](#supply-depot-path) - Storage and logistics management
- [Transit Network](#transit-network-path) - Transportation infrastructure
- [Teleport Gate](#teleport-gate-path) - Teleportation infrastructure

### Medical & Health
- [Spirit Apothecary](#spirit-apothecary-path) - Healing and medical services

## Building Categories

### Resource Extraction & Processing
Buildings in the Resource Extraction & Processing category extract and refine raw materials from the environment.

#### Timberworks Path
The Timberworks processes wood and lumber from forests.

**Building Type**: Timberworks
- **Category**: `resource`
- **Building Path**: `timberworks`
- **Description**: Wood harvesting and lumber processing facilities

**Tiers**:
1. **Woodcutter's Lodge** (Tier 1)
   - Daily Output: +10 Lumber
   - Signature Addition: Log Rack (+25% storage)
   - Unlocks: Basic Construction recipes

2. **Logging Camp** (Tier 2)
   - Daily Output: +25 Lumber; +10% hauling efficiency
   - Signature Addition: Supply Hut (+10% hauling)
   - Unlocks: Stoneworks projects

3. **Sawmill** (Tier 3)
   - Daily Output: +50 Lumber; +5 Refined Lumber
   - Signature Addition: Blade Attunement (+10% refined output)
   - Enables: Refined lumber usage

4. **Spiritwood Mill** (Tier 4)
   - Daily Output: +80 Lumber; +8 Refined Lumber
   - Signature Addition: Saw Array (+10% qi-conductive wood)
   - Bonus: +5% qi synergy near nodes

5. **Living Timberyard** (Tier 5)
   - Daily Output: +120 Lumber; +15 Refined Lumber
   - Signature Addition: Growth Basin (+5% regrowth)
   - Bonus: +10% efficiency to adjacent workshops

6. **Verdant Arboretum** (Tier 6)
   - Daily Output: +200 Lumber; +25 Refined Lumber; +3 Spirit Planks
   - Signature Addition: Heartwood Core (passive Spirit Planks)
   - Bonus: Boosts prosperity aura

#### Farmland Path
The Farmland produces food through cultivation and farming.

**Building Type**: Farmland
- **Category**: `resource`
- **Building Path**: `farmland`
- **Description**: Food production through cultivation and farming

**Tiers**:
1. **Forager's Camp** (Tier 1)
   - Daily Output: +10 Food/day
   - Signature Addition: Drying Rack (slows spoilage)

2. **Cultivation Fields** (Tier 2)
   - Daily Output: +25 Food/day
   - Signature Addition: Irrigation Ditch (+10% yield)

3. **Irrigated Terraces** (Tier 3)
   - Daily Output: +45 Food/day
   - Signature Addition: Stone Drainage (prevents rain-induced crop loss)

4. **Qi-Blessed Fields** (Tier 4)
   - Daily Output: +70 Food/day
   - Signature Addition: Fertility Array (+15% food yield)

5. **Spirit Farmstead** (Tier 5)
   - Daily Output: +95 Food/day; produces Fertilizer resource
   - Signature Addition: Beast Pen (fertilizer production)

6. **Eternal Harvest Fields** (Tier 6)
   - Daily Output: +130 Food/day; +5% settlement food efficiency; +5% morale
   - Signature Addition: Harvest Spirit Idol (+5% morale & food efficiency)

#### Spirit Garden Path
The Spirit Garden cultivates spirit herbs for alchemical and medicinal use.

**Building Type**: Spirit Garden
- **Category**: `resource`
- **Building Path**: `spirit_garden`
- **Description**: Cultivates spirit herbs for alchemical and medicinal use

**Tiers**:
1. **Herb Patch** (Tier 1)
   - Daily Output: +8 Raw Herbs/day
   - Signature Addition: Water Trough (+10% yield)

2. **Cultivation Beds** (Tier 2)
   - Daily Output: +18 Raw Herbs/day
   - Signature Addition: Glass Frames (+10% growth rate)

3. **Herbal Conservatory** (Tier 3)
   - Daily Output: +30 Raw Herbs/day; +5 Refined Herbs/day
   - Signature Addition: Drip Array (automatic irrigation)

4. **Spirit Grove** (Tier 4)
   - Daily Output: +45 Raw Herbs/day; rare herb chance
   - Signature Addition: Tree Markers (growth cycle tracking)

5. **Alchemical Grove** (Tier 5)
   - Daily Output: +55 Raw Herbs/day; +10% potency
   - Signature Addition: Essence Basin (+10% potency)

6. **Celestial Herbarium** (Tier 6)
   - Daily Output: +70 Raw Herbs/day; +10 Refined Herbs/day; +5% global qi efficiency
   - Signature Addition: Spirit Flower Core (+5% qi efficiency globally)

#### Stoneworks Path
The Stoneworks extracts and processes stone from quarries.

**Building Type**: Stoneworks
- **Category**: `resource`
- **Building Path**: `stoneworks`
- **Description**: Stone extraction and processing facilities

**Tiers**:
1. **Stone Pit** (Tier 1)
   - Daily Output: +15 Stone Blocks/day
   - Signature Addition: Tool Shed (maintained tools, +10% output)

2. **Quarry Yard** (Tier 2)
   - Daily Output: +35 Stone Blocks/day
   - Signature Addition: Winch Tower (doubles hauling distance)

3. **Mason's Guild** (Tier 3)
   - Daily Output: +55 Cut Stone/day; waste reduced
   - Signature Addition: Chisel Rack (+10% precision, less waste)

4. **Spirit Quarry** (Tier 4)
   - Daily Output: +75 Stone Blocks/day; +5 Spirit Stone Fragments/day
   - Signature Addition: Runic Picks (spirit fragment collection)

5. **Elemental Quarry** (Tier 5)
   - Daily Output: +95 Stone Blocks/day; +10 Attuned Stone/day
   - Signature Addition: Stabilizing Pillars (+10% formation defense nearby)

6. **Celestial Masonry Hall** (Tier 6)
   - Daily Output: +130 Stone Blocks/day; +15 Attuned Stone/day; +2 Monolith Cores/day
   - Signature Addition: Stone Heart Core (+5% settlement defense aura)

#### Waterworks Path
The Waterworks provides water collection, storage, and purification for the settlement.

**Building Type**: Waterworks
- **Category**: `resource`
- **Building Path**: `waterworks`
- **Description**: Provides water collection, storage, and purification for the settlement

**Tiers**:
1. **Wellshaper Camp** (Tier 1)
   - Daily Output: +10 Water Tokens/day
   - Signature Addition: Bucket Winch (faster draw)

2. **Aquifer Station** (Tier 2)
   - Daily Output: +25 Water Tokens/day
   - Signature Addition: Pump House (+10% yield)

3. **Reservoir Works** (Tier 3)
   - Daily Output: +40 Water Tokens/day; Water Reserve buffer
   - Signature Addition: Settling Basin (reduces contamination)

4. **Qi Condenser Hub** (Tier 4)
   - Daily Output: +60 Water Tokens/day; +5 Purified Water/day
   - Signature Addition: Condenser Spire (+10% purified output)

5. **Spirit Reservoir** (Tier 5)
   - Daily Output: +80 Water Tokens/day; +10 Purified Water/day; +3 Spirit Dew/day
   - Signature Addition: Flow Harmonizer (+5% morale near water)

6. **Celestial Aqueduct** (Tier 6)
   - Daily Output: +110 Water Tokens/day; +20 Purified Water/day; +5 Spirit Dew/day
   - Signature Addition: Cloud Well (+5% global agriculture efficiency)

#### Ironworks Path
The Ironworks extracts iron ore and rare metals from the earth.

**Building Type**: Ironworks
- **Category**: `resource`
- **Building Path**: `ironworks`
- **Description**: Extracts iron ore and rare metals from the earth

**Tiers**:
1. **Prospector's Pit** (Tier 1)
   - Daily Output: +10 Iron Ore/day
   - Signature Addition: Survey Stakes (+5% discovery chance)

2. **Tunnel Mine** (Tier 2)
   - Daily Output: +25 Iron Ore/day
   - Signature Addition: Winch Lift (+15% hauling efficiency)

3. **Deep Shaft** (Tier 3)
   - Daily Output: +40 Iron Ore/day; +5 Rare Ore/day
   - Signature Addition: Ore Sorting Chute (reduces waste)

4. **Spirit Vein Mine** (Tier 4)
   - Daily Output: +50 Iron Ore/day; +8 Rare Ore/day; +2 Essence Pebbles/day
   - Signature Addition: Spirit Drill Head (+10% rare ore)

5. **Elemental Excavation** (Tier 5)
   - Daily Output: +65 Iron Ore/day; +12 Rare Ore/day; +4 Essence Pebbles/day
   - Signature Addition: Elemental Dampeners (+10% safety, reduces accidents)

6. **Celestial Deepworks** (Tier 6)
   - Daily Output: +90 Iron Ore/day; +15 Rare Ore/day; +6 Essence Pebbles/day
   - Signature Addition: Deepcore Beacon (+5% global construction durability)

#### Qi Condenser Spire Path
The Qi Condenser Spire channels and condenses ambient qi into mana crystals.

**Building Type**: Qi Condenser Spire
- **Category**: `resource`
- **Building Path**: `qi_condenser_spire`
- **Description**: Channels and condenses ambient qi into mana crystals

**Tiers**:
1. **Condenser Pillar** (Tier 1)
   - Output: Ambient qi draw +5%
   - Signature Addition: Flow Ring (+5% ambient qi draw)

2. **Spire** (Tier 2)
   - Output: Conversion efficiency +10%
   - Signature Addition: Alignment Circle (+10% efficiency)

3. **Spirit Spire** (Tier 3)
   - Output: +1 Mana Crystal/day (low-grade)
   - Signature Addition: Qi Funnel Array (+1 crystal/day)

4. **Resonant Spire** (Tier 4)
   - Output: +2 Mana Crystals/day
   - Signature Addition: Attunement Node (+2 crystals/day)

5. **Celestial Spire** (Tier 5)
   - Output: +3 Mana Crystals/day; qi efficiency +5%
   - Signature Addition: Radiant Core (+3 crystals/day, +5% qi efficiency)

6. **Tower of Heaven's Pulse** (Tier 6)
   - Output: Crystal purity +10%; cultivation +5% settlement-wide
   - Signature Addition: Pulse Heart (+10% purity, +5% cultivation)

#### Condensation Pavilion Path
The Condensation Pavilion captures and purifies water through condensation processes.

**Building Type**: Condensation Pavilion
- **Category**: `resource`
- **Building Path**: `condensation_pavilion`
- **Description**: Captures and purifies water through condensation processes

**Tiers**:
1. **Condensation Shed** (Tier 1)
   - Daily Output: +5 Purified Water/day
   - Signature Addition: Vapor Screens (+10% purification)

2. **Mist Pavilion** (Tier 2)
   - Daily Output: +10 Purified Water/day; +2 Distilled Water/day
   - Signature Addition: Wind Funnels (+15% efficiency)

3. **Steam Tower** (Tier 3)
   - Daily Output: +15 Purified Water/day; +5 Distilled Water/day
   - Signature Addition: Steam Coils (+10% speed)

4. **Spirit Condenser** (Tier 4)
   - Daily Output: +20 Purified Water/day; +5 Spirit Dew/day
   - Signature Addition: Essence Linens (+10% spirit dew yield)

5. **Harmonized Cascade** (Tier 5)
   - Daily Output: +25 Purified Water/day; +8 Spirit Dew/day
   - Signature Addition: Resonance Pools (+10% alchemy potency using water modifiers)

6. **Celestial Condenser Hall** (Tier 6)
   - Daily Output: +35 Purified Water/day; +12 Spirit Dew/day; +3 Mist Crystals/day
   - Signature Addition: Aqua Nexus (+5% settlement qi stability)

### Production & Manufacturing
Buildings in the Production category focus on crafting and manufacturing.

#### Carpenter's Workshop Path
The Carpenter's Workshop crafts tools, furniture, and structural components from wood.

**Building Type**: Carpenter's Workshop
- **Category**: `production`
- **Building Path**: "carpenters_workshop"
- **Description**: Crafts wooden tools, furniture, and structural components

**Tiers**:
1. **Carpenter's Hut** (Tier 1)
   - Output: Wooden Tools (basic)
   - Signature Addition: Workbench (enables wooden tool crafting)

2. **Joiner's Hall** (Tier 2)
   - Output: Wooden Tools + Decorative Furniture (minor morale boost)
   - Signature Addition: Pattern Table (decor furniture recipes)

3. **Woodwright's Guild** (Tier 3)
   - Output: Structural Components (construction speed +5%)
   - Signature Addition: Tool Locker (+10% carpentry efficiency)

4. **Artisan Carpentry Hall** (Tier 4)
   - Output: Spirit Reinforced Components (durability +10%)
   - Signature Addition: Spirit Inlays (auto-applies durability bonus)

5. **Grand Workshop** (Tier 5)
   - Output: Prefabricated Frames (construction speed +10%)
   - Signature Addition: Framing Rig (speeds construction +10%)

6. **Master Carpenter's Pavilion** (Tier 6)
   - Output: Living Designs (buildings gain passive qi resonance)
   - Signature Addition: Living Designs blueprint library (settlement-wide resonance buff)

#### Stonecutting Yard Path
The Stonecutting Yard shapes and processes stone into construction materials.

**Building Type**: Stonecutting Yard
- **Category**: `production`
- **Building Path**: `stonecutting_yard`
- **Description**: Shapes and processes stone into construction materials

**Tiers**:
1. **Cutter's Shed** (Tier 1)
   - Output: Produces Cut Stone panels
   - Signature Addition: Block Table (carved stone panels)

2. **Cutting Yard** (Tier 2)
   - Output: +20% Cut Stone output
   - Signature Addition: Sand Pit (+10% fine-cut efficiency)

3. **Mason's Atelier** (Tier 3)
   - Output: Decorative Stone Components; +5% aesthetics
   - Signature Addition: Pattern Library (decorative architecture unlocks)

4. **Spirit Sawhouse** (Tier 4)
   - Output: +15% processed stone; Attuned Stone shaping
   - Signature Addition: Precision Array (+15% construction speed when using attuned materials)

5. **Harmonized Yard** (Tier 5)
   - Output: Waste reduced; +10% durability for stone structures
   - Signature Addition: Sound Chamber (reduces breakage/waste)

6. **Echoing Atelier** (Tier 6)
   - Output: Processed output +25%; applies +10% yield buff to nearby quarries
   - Signature Addition: Harmonic Forge (nearby quarries +10% yield)

#### Spirit Masonry Forge Path
The Spirit Masonry Forge creates spirit-infused stone blocks and defensive components.

**Building Type**: Spirit Masonry Forge
- **Category**: `production`
- **Building Path**: `spirit_masonry_forge`
- **Description**: Creates spirit-infused stone blocks and defensive components

**Tiers**:
1. **Mason's Forge** (Tier 1)
   - Output: Reinforced Spirit Blocks
   - Signature Addition: Kiln Core (boosts fusion stability)

2. **Spirit Forge** (Tier 2)
   - Output: +10% energy efficiency; Spirit Block production
   - Signature Addition: Mana Reservoir (+10% energy efficiency)

3. **Elemental Forge** (Tier 3)
   - Output: +10% refined block output; Elemental Spirit Blocks
   - Signature Addition: Anvil Array (+10% refined block output)

4. **Celestial Forge** (Tier 4)
   - Output: Spirit Array Plates unlocked; talisman components
   - Signature Addition: Rune-Smith's Bench (defensive talisman crafting)

5. **Formation Forge** (Tier 5)
   - Output: Formation-grade Stone; +15% formation power
   - Signature Addition: Glyph Press (+15% formation power)

6. **Core Forge of the Earth** (Tier 6)
   - Output: Earthen Heart Nodes (global +5% structure durability)
   - Signature Addition: Earthen Heart Node (global durability buff)

### Defense & Fortifications
Buildings in the Defense & Fortifications category focus on protective formations, defensive arrays, and settlement security.

#### Rune Formation Path
The Rune Formation facility crafts runes, talismans, and defensive formations for settlement protection.

**Building Type**: Rune Formation
- **Category**: `defense`
- **Building Path**: `rune_formation`
- **Description**: Crafts runes, talismans, and defensive formations for settlement protection

**Tiers**:
1. **Rune Carver's Bench** (Tier 1)
   - Output: Basic formation templates
   - Signature Addition: Template Scrolls (standard low-tier formations)

2. **Glyph Studio** (Tier 2)
   - Output: Warding Lanterns (minor base defense aura)
   - Signature Addition: Warding Lanterns craftable (settlement defense +2%)

3. **Formation Foundry** (Tier 3)
   - Output: Formation Cores / Anchors unlocked
   - Signature Addition: Pattern Loom (custom formation layouts)

4. **Spirit Foundry** (Tier 4)
   - Output: +10% success on advanced arrays
   - Signature Addition: Attunement Basin (+10% array success)

5. **Nexus Foundry** (Tier 5)
   - Output: Networked formations; Ley diagnostics
   - Signature Addition: Leyline Compass (detects qi faults)

6. **Earth-Sky Foundry** (Tier 6)
   - Output: Grand Seal Pedestal (+10% defense & qi stability settlement-wide)
   - Signature Addition: Grand Seal Pedestal (settlement aura)

#### Granary & Millhouse Path
The Granary & Millhouse stores and processes food for the settlement.

**Building Type**: Granary & Millhouse
- **Category**: `production`
- **Building Path**: `granary_millhouse`
- **Description**: Stores and processes food for the settlement

**Tiers**:
1. **Granary** (Tier 1)
   - Output: Increases food storage capacity
   - Signature Addition: Rat-Ward Charm (prevents decay)

2. **Millhouse** (Tier 2)
   - Output: Processed Food output +10/day
   - Signature Addition: Grinding Stone (+10% milling efficiency)

3. **Steam Mill** (Tier 3)
   - Output: Processed Food output +25/day
   - Signature Addition: Dust Trap (reduces loss/spoilage)

4. **Spirit Granary** (Tier 4)
   - Output: Food stores last +25% longer
   - Signature Addition: Preservation Rune (spoilage immunity)

5. **Harmonized Mill** (Tier 5)
   - Output: Processed Food output +45/day
   - Signature Addition: Flow Wheel (+10% processed food output)

6. **Celestial Storehouse** (Tier 6)
   - Output: Global +5% morale; -5% food upkeep
   - Signature Addition: Abundance Beacon (settlement aura)

#### Spiritual Kitchen Path
The Spiritual Kitchen prepares meals that provide cultivation benefits and morale boosts.

**Building Type**: Spiritual Kitchen
- **Category**: `production`
- **Building Path**: `spiritual_kitchen`
- **Description**: Prepares meals that provide cultivation benefits and morale boosts

**Tiers**:
1. **Cookfire** (Tier 1)
   - Output: +5 Food/day; morale +2 local radius
   - Signature Addition: Iron Pot (morale bonus)

2. **Communal Kitchen** (Tier 2)
   - Output: +10 Food/day; +5% disciple recovery
   - Signature Addition: Meal Table (recovery rate boost)

3. **Spirit Kitchen** (Tier 3)
   - Output: Spirit Infused Meals (+5% cultivation buff)
   - Signature Addition: Essence Spice Rack (cultivation buff recipes)

4. **Celestial Kitchen** (Tier 4)
   - Output: Meal potency +15%; elemental meal variants
   - Signature Addition: Flavor Array (+15% meal potency)

5. **Feast Pavilion** (Tier 5)
   - Output: Unlocks morale festivals; +10% morale during festivals
   - Signature Addition: Ceremonial Table (festival events)

6. **Divine Kitchen** (Tier 6)
   - Output: +5% global qi & stamina recovery
   - Signature Addition: Golden Cauldron (global recovery aura)

#### Drying Pavilion Path
The Drying Pavilion processes raw herbs into refined herbs and powders.

**Building Type**: Drying Pavilion
- **Category**: `production`
- **Building Path**: `drying_pavilion`
- **Description**: Processes raw herbs into refined herbs and powders

**Tiers**:
1. **Drying Rack** (Tier 1)
   - Output: +5 Refined Herbs/day; slows spoilage
   - Signature Addition: Herb Hooks (+10% preservation time)

2. **Shade Pavilion** (Tier 2)
   - Output: +10 Refined Herbs/day; faster drying
   - Signature Addition: Fan Array (+15% drying speed)

3. **Heated Pavilion** (Tier 3)
   - Output: +15 Refined Herbs/day; +5% quality
   - Signature Addition: Heat Plates (+10% quality)

4. **Spirit Pavilion** (Tier 4)
   - Output: +20 Refined Herbs/day; potency retained
   - Signature Addition: Rune Cloths (+10% potency retention)

5. **Refinement Pavilion** (Tier 5)
   - Output: +25 Refined Herbs/day; produces Herb Powder
   - Signature Addition: Powder Grinder (Herb Powder unlock)

6. **Celestial Pavilion** (Tier 6)
   - Output: +35 Refined Herbs/day; +10% yield to all herb buildings
   - Signature Addition: Preservation Sigil (+10% yield to all herb buildings)

#### Alchemists Hall Path
The Alchemists Hall crafts potions, elixirs, and pills for cultivation and healing.

**Building Type**: Alchemists Hall
- **Category**: `production`
- **Building Path**: `alchemists_hall`
- **Description**: Crafts potions, elixirs, and pills for cultivation and healing

**Tiers**:
1. **Brew Hut** (Tier 1)
   - Output: Basic Tonics; failure chance reduced
   - Signature Addition: Cooling Rack (reduces failure chance)

2. **Mixing Hall** (Tier 2)
   - Output: Potion queueing; higher throughput
   - Signature Addition: Recipe Board (potion queueing interface)

3. **Spirit Hall** (Tier 3)
   - Output: +10% elixir potency
   - Signature Addition: Essence Jar (+10% potency)

4. **Advanced Alchemy Hall** (Tier 4)
   - Output: +10% yield per batch
   - Signature Addition: Catalyst Shelf (+10% yield)

5. **Grand Alchemist's Hall** (Tier 5)
   - Output: Unlocks unique pill crafting
   - Signature Addition: Pill Mold Bench (unique pill types)

6. **Celestial Crucible** (Tier 6)
   - Output: +5% global qi cultivation speed; superior pills
   - Signature Addition: Golden Crucible (+5% qi cultivation speed globally)

#### Spirit Apothecary Path
The Spirit Apothecary provides healing services and medical care for the settlement.

**Building Type**: Spirit Apothecary
- **Category**: `production`
- **Building Path**: `spirit_apothecary`
- **Description**: Provides healing services and medical care for the settlement

**Tiers**:
1. **Healer's Hut** (Tier 1)
   - Output: Basic healing tasks available
   - Signature Addition: Salve Shelf (enables healing tasks)

2. **Medicine Shop** (Tier 2)
   - Output: +10% recovery speed (local)
   - Signature Addition: Treatment Bed (+10% recovery speed)

3. **Spirit Apothecary** (Tier 3)
   - Output: Healing success rate +10%
   - Signature Addition: Spirit Basin (+10% success rate)

4. **Grand Apothecary** (Tier 4)
   - Output: Unlocks rare elixir crafting
   - Signature Addition: Testing Chamber (rare elixirs)

5. **Alchemical Institute** (Tier 5)
   - Output: +10% global herb efficiency
   - Signature Addition: Archive Vault (+10% global herb efficiency)

6. **Celestial Apothecary** (Tier 6)
   - Output: +5% health and morale settlement-wide
   - Signature Addition: Sanctum Sigil (+5% health & morale globally)

### Military & Adventuring
Buildings in the Military & Adventuring category focus on combat, training, equipment, and adventurer services.

#### Adventurer's Guild Hall Path
The Adventurer's Guild Hall coordinates hunting missions, beast part trading, and adventurer services.

**Building Type**: Adventurer's Guild Hall
- **Category**: `commercial` (or `military` - can be configured)
- **Building Path**: `adventurers_guild_hall`
- **Description**: Coordinates hunting missions, beast part trading, and adventurer services

**Tiers**:
1. **Guild Office** (Tier 1)
   - Output: Unlocks simple hunt contracts
   - Signature Addition: Quest Board (dispatch small hunts)

2. **Hall of Trials** (Tier 2)
   - Output: Training scenario bonuses; morale +5% for active hunters
   - Signature Addition: Challenge Arena (pre-mission training buffs)

3. **Adventurer's Guild Hall** (Tier 3)
   - Output: Purchases Beast Parts/Cores; unlocks bounty missions
   - Signature Addition: Bounty Counter (Hunt mission queue)

4. **Hall of Valor** (Tier 4)
   - Output: High-tier mission success +10%; loyalty gain for hunters
   - Signature Addition: Veteran Registry (mission success boost)

5. **Spirit Hunter's Hall** (Tier 5)
   - Output: Mission time -10%; reveals rare beast encounters
   - Signature Addition: Tracking Mirror (mission time reduction)

6. **Hall of Ten Thousand Hunts** (Tier 6)
   - Output: Beast Core Exchange unlocked; converts cores → sect resources
   - Signature Addition: Beast Core Exchange (core conversion & trade)

#### Smithy Path
The Smithy crafts weapons, armor, and equipment for adventurers and combat.

**Building Type**: Smithy
- **Category**: `production`
- **Building Path**: `smithy`
- **Description**: Crafts weapons, armor, and equipment for adventurers and combat

**Tiers**:
1. **Village Forge** (Tier 1)
   - Output: Basic gear maintenance; +5% mission success
   - Signature Addition: Sharpening Wheel (+5% mission success)

2. **Smithy** (Tier 2)
   - Output: Gear durability +10%
   - Signature Addition: Temper Pit (+10% durability)

3. **Spirit Forge** (Tier 3)
   - Output: Unlocks qi-infused weapons
   - Signature Addition: Rune Anvil (qi-infused weapon recipes)

4. **Armorer's Hall** (Tier 4)
   - Output: Gear crafting speed +15%; mission defense buffs
   - Signature Addition: Forge Crew (crafting speed +15%)

5. **Elemental Forge** (Tier 5)
   - Output: Mission damage +10%; elemental gear
   - Signature Addition: Essence Crucible (+10% mission damage)

6. **Heavenly Forge** (Tier 6)
   - Output: Chance to craft relics; mission success boost +5%
   - Signature Addition: Artifact Mold (relic crafting chance)

#### Inn Path
The Inn provides hospitality, rest, and recovery services for adventurers and travelers.

**Building Type**: Inn
- **Category**: `commercial`
- **Building Path**: `inn`
- **Description**: Provides hospitality, rest, and recovery services for adventurers and travelers

**Tiers**:
1. **Roadside Inn** (Tier 1)
   - Output: Morale +5% for returning adventurers
   - Signature Addition: Meal Counter (+5% morale)

2. **Travelers' Inn** (Tier 2)
   - Output: Stamina recovery +10%
   - Signature Addition: Bathhouse (stamina recovery boost)

3. **Phoenix Inn** (Tier 3)
   - Output: Adventurer loyalty +10%
   - Signature Addition: Story Hearth (loyalty boost)

4. **Hero's Rest** (Tier 4)
   - Output: Renown gain +10%
   - Signature Addition: Hall of Deeds (renown bonus)

5. **Spirit Haven** (Tier 5)
   - Output: Cultivation recovery +10%
   - Signature Addition: Dream Array (+10% cultivation recovery)

6. **Heavenly Phoenix Pavilion** (Tier 6)
   - Output: Visiting guests bring trade & renown; +5% morale
   - Signature Addition: Pilgrim Shrine (trade & renown events)

#### Training Grounds Path
The Training Grounds provides combat training and skill development for disciples and adventurers.

**Building Type**: Training Grounds
- **Category**: `civic` (or `military` - can be configured)
- **Building Path**: `training_grounds`
- **Description**: Provides combat training and skill development for disciples and adventurers

**Tiers**:
1. **Sparring Yard** (Tier 1)
   - Output: Disciple XP gain +5%
   - Signature Addition: Instructor Post (XP boost)

2. **Combat Ring** (Tier 2)
   - Output: Skill improvement rate +10%
   - Signature Addition: Scoring Drum (+10% skill gain)

3. **Martial Grounds** (Tier 3)
   - Output: Unlocks ranged training; ranged mission bonuses
   - Signature Addition: Projectile Range (ranged drills)

4. **Spirit Arena** (Tier 4)
   - Output: Pre-battle experience buff; success +5%
   - Signature Addition: Beast Mirage Array (mission preview)

5. **War Pavilion** (Tier 5)
   - Output: Multi-party mission success +10%
   - Signature Addition: Formation Drill Square (multi-party buffs)

6. **Heavenly Dojo** (Tier 6)
   - Output: Global combat XP gain +10%; mission success +5%
   - Signature Addition: Battle Meditation Garden (global combat XP buff)

### Infrastructure & Logistics
Buildings in the Infrastructure & Logistics category provide essential utilities, services, and logistics management for the settlement.

#### Waterworks Path
The Waterworks provides water collection, storage, and purification for the settlement.

**Building Type**: Waterworks
- **Category**: `resource`
- **Building Path**: `waterworks`
- **Description**: Provides water collection, storage, and purification for the settlement

**Tiers**:
1. **Wellshaper Camp** (Tier 1)
   - Daily Output: +10 Water Tokens/day
   - Signature Addition: Bucket Winch (faster draw)

2. **Aquifer Station** (Tier 2)
   - Daily Output: +25 Water Tokens/day
   - Signature Addition: Pump House (+10% yield)

3. **Reservoir Works** (Tier 3)
   - Daily Output: +40 Water Tokens/day; Water Reserve buffer
   - Signature Addition: Settling Basin (reduces contamination)

4. **Qi Condenser Hub** (Tier 4)
   - Daily Output: +60 Water Tokens/day; +5 Purified Water/day
   - Signature Addition: Condenser Spire (+10% purified output)

5. **Spirit Reservoir** (Tier 5)
   - Daily Output: +80 Water Tokens/day; +10 Purified Water/day; +3 Spirit Dew/day
   - Signature Addition: Flow Harmonizer (+5% morale near water)

6. **Celestial Aqueduct** (Tier 6)
   - Daily Output: +110 Water Tokens/day; +20 Purified Water/day; +5 Spirit Dew/day
   - Signature Addition: Cloud Well (+5% global agriculture efficiency)

#### Crystal Refinery Path
The Crystal Refinery processes and refines qi crystals for various uses.

**Building Type**: Crystal Refinery
- **Category**: `production`
- **Building Path**: `crystal_refinery`
- **Description**: Processes and refines qi crystals for various uses

**Tiers**:
1. **Refining Table** (Tier 1)
   - Output: Crystal purity +5%
   - Signature Addition: Qi Funnel (+5% purity)

2. **Crystal Kiln** (Tier 2)
   - Output: Prevents crystal loss during refinement
   - Signature Addition: Cooling Array (loss prevention)

3. **Spirit Refinery** (Tier 3)
   - Output: Refinement speed +10%
   - Signature Addition: Harmonic Core (+10% speed)

4. **Elemental Refinery** (Tier 4)
   - Output: Produces Elemental Mana Crystals
   - Signature Addition: Essence Separator (elemental yields)

5. **Luminous Refinery** (Tier 5)
   - Output: Nearby qi flow boosted +5%
   - Signature Addition: Light Basin (local qi boost)

6. **Celestial Refinery** (Tier 6)
   - Output: Global qi efficiency +5%
   - Signature Addition: Crystal Lattice Core (global qi efficiency)

#### Meditation Hall Path
The Meditation Hall provides cultivation spaces for qi recovery and crystal formation.

**Building Type**: Meditation Hall
- **Category**: `civic`
- **Building Path**: `meditation_hall`
- **Description**: Provides cultivation spaces for qi recovery and crystal formation

**Tiers**:
1. **Meditation Room** (Tier 1)
   - Output: Qi recovery +5%
   - Signature Addition: Incense Burner (+5% qi recovery)

2. **Cultivation Hall** (Tier 2)
   - Output: Focus gain +10%
   - Signature Addition: Sound Dampening Runes (+10% focus)

3. **Spirit Chamber** (Tier 3)
   - Output: Cultivation rate +10%
   - Signature Addition: Qi Mirror (+10% cultivation rate)

4. **Resonance Hall** (Tier 4)
   - Output: Small chance of spontaneous crystal formation
   - Signature Addition: Harmonic Pool (crystal chance unlock)

5. **Chamber of Still Waters** (Tier 5)
   - Output: Occasional automatic crystal condensation
   - Signature Addition: Still Pool (automatic crystal spawn)

6. **Hall of Enlightened Silence** (Tier 6)
   - Output: Global mana crystal formation chance +5%
   - Signature Addition: Silent Heart Core (global +5% crystal chance)

#### Crystal Exchange Pavilion Path
The Crystal Exchange Pavilion facilitates crystal trading and resource exchange.

**Building Type**: Crystal Exchange Pavilion
- **Category**: `commercial`
- **Building Path**: `crystal_exchange_pavilion`
- **Description**: Facilitates crystal trading and resource exchange

**Tiers**:
1. **Trader's Kiosk** (Tier 1)
   - Output: Unlocks crystal exchange interface
   - Signature Addition: Ledger Board (tracks exchange rates)

2. **Merchant Pavilion** (Tier 2)
   - Output: Trade efficiency +10%
   - Signature Addition: Vault Room (+10% trade efficiency)

3. **Spirit Bazaar** (Tier 3)
   - Output: Merchant income +10%
   - Signature Addition: Bartering Rings (+10% income)

4. **Crystal Exchange Pavilion** (Tier 4)
   - Output: Transaction throughput +15%
   - Signature Addition: Market Array (+15% throughput)

5. **Grand Exchange** (Tier 5)
   - Output: Crystal loss reduced on conversion
   - Signature Addition: Coin of Harmony (conversion loss reduction)

6. **Heavenly Market Hall** (Tier 6)
   - Output: Global prosperity +5%; auto-balances resources
   - Signature Addition: Trade Nexus (resource balancing, +5% prosperity)

#### Qi Condenser Spire Path
The Qi Condenser Spire channels and condenses ambient qi into mana crystals.

**Building Type**: Qi Condenser Spire
- **Category**: `resource`
- **Building Path**: `qi_condenser_spire`
- **Description**: Channels and condenses ambient qi into mana crystals

**Tiers**:
1. **Condenser Pillar** (Tier 1)
   - Output: Ambient qi draw +5%
   - Signature Addition: Flow Ring (+5% ambient qi draw)

2. **Spire** (Tier 2)
   - Output: Conversion efficiency +10%
   - Signature Addition: Alignment Circle (+10% efficiency)

3. **Spirit Spire** (Tier 3)
   - Output: +1 Mana Crystal/day (low-grade)
   - Signature Addition: Qi Funnel Array (+1 crystal/day)

4. **Resonant Spire** (Tier 4)
   - Output: +2 Mana Crystals/day
   - Signature Addition: Attunement Node (+2 crystals/day)

5. **Celestial Spire** (Tier 5)
   - Output: +3 Mana Crystals/day; qi efficiency +5%
   - Signature Addition: Radiant Core (+3 crystals/day, +5% qi efficiency)

6. **Tower of Heaven's Pulse** (Tier 6)
   - Output: Crystal purity +10%; cultivation +5% settlement-wide
   - Signature Addition: Pulse Heart (+10% purity, +5% cultivation)

#### Condensation Pavilion Path
The Condensation Pavilion captures and purifies water through condensation processes.

**Building Type**: Condensation Pavilion
- **Category**: `resource`
- **Building Path**: `condensation_pavilion`
- **Description**: Captures and purifies water through condensation processes

**Tiers**:
1. **Condensation Shed** (Tier 1)
   - Daily Output: +5 Purified Water/day
   - Signature Addition: Vapor Screens (+10% purification)

2. **Mist Pavilion** (Tier 2)
   - Daily Output: +10 Purified Water/day; +2 Distilled Water/day
   - Signature Addition: Wind Funnels (+15% efficiency)

3. **Steam Tower** (Tier 3)
   - Daily Output: +15 Purified Water/day; +5 Distilled Water/day
   - Signature Addition: Steam Coils (+10% speed)

4. **Spirit Condenser** (Tier 4)
   - Daily Output: +20 Purified Water/day; +5 Spirit Dew/day
   - Signature Addition: Essence Linens (+10% spirit dew yield)

5. **Harmonized Cascade** (Tier 5)
   - Daily Output: +25 Purified Water/day; +8 Spirit Dew/day
   - Signature Addition: Resonance Pools (+10% alchemy potency using water modifiers)

6. **Celestial Condenser Hall** (Tier 6)
   - Daily Output: +35 Purified Water/day; +12 Spirit Dew/day; +3 Mist Crystals/day
   - Signature Addition: Aqua Nexus (+5% settlement qi stability)

### Housing & Living
Buildings in the Housing & Living category provide residential spaces and quality of life improvements.

#### Personal Housing Path
The Personal Housing provides individual residences for cultivators with cultivation benefits.

**Building Type**: Personal Housing
- **Category**: `civic`
- **Building Path**: `personal_housing`
- **Description**: Provides individual residences for cultivators with cultivation benefits

**Tiers**:
1. **Cultivator's Hut** (Tier 1)
   - Output: Qi recovery +5% (occupant)
   - Signature Addition: Meditation Corner (qi recovery boost)

2. **Wooden Cottage** (Tier 2)
   - Output: Prevents qi dissipation at night
   - Signature Addition: Spirit Lamp (nighttime qi stability)

3. **Stone Residence** (Tier 3)
   - Output: Ambient qi density +10% (local)
   - Signature Addition: Qi Vent (ambient qi +10%)

4. **Inner Courtyard House** (Tier 4)
   - Output: Morale +5%; cultivation rate +5%
   - Signature Addition: Tranquility Pool (morale & cultivation buff)

5. **Spirit Dwelling** (Tier 5)
   - Output: Element-specific cultivation bonus (+10%)
   - Signature Addition: Attunement Array (elemental bonus)

6. **Immortal Pavilion** (Tier 6)
   - Output: Generates 1 mana crystal weekly; global morale +1%
   - Signature Addition: Bound Spirit Core (auto crystal, morale)

#### Shared Housing Path
The Shared Housing provides communal residential spaces for disciples and workers.

**Building Type**: Shared Housing
- **Category**: `civic`
- **Building Path**: `shared_housing`
- **Description**: Provides communal residential spaces for disciples and workers

**Tiers**:
1. **Wooden Barracks** (Tier 1)
   - Output: Reduces morale penalties by 5%
   - Signature Addition: Meal Drum (morale penalty reduction)

2. **Stone Dormitory** (Tier 2)
   - Output: Stamina recovery +5%
   - Signature Addition: Training Corner (stamina buff)

3. **Disciples' Hall** (Tier 3)
   - Output: Cultivation speed +5% (shared)
   - Signature Addition: Qi Ventilation Array (cultivation buff)

4. **Spirit Residence Hall** (Tier 4)
   - Output: Morale +10%; unity buff
   - Signature Addition: Communion Shrine (morale & unity)

5. **Sect Compound** (Tier 5)
   - Output: Disciple loyalty +10%; fatigue reduction
   - Signature Addition: Harmony Courtyard (loyalty, fatigue)

6. **Grand Cloister** (Tier 6)
   - Output: Global cultivation efficiency +5%
   - Signature Addition: Sect Heart Formation (+5% cultivation globally)

### Defense & Fortifications
Buildings in the Defense & Fortifications category provide defensive structures and protective systems.

#### Fortified Wall Path
The Fortified Wall provides defensive perimeter protection for the settlement.

**Building Type**: Fortified Wall
- **Category**: `defense`
- **Building Path**: `fortified_wall`
- **Description**: Provides defensive perimeter protection for the settlement

**Tiers**:
1. **Palisade Line** (Tier 1)
   - Output: Settlement defense +10%
   - Signature Addition: Gatehouse Watch (reduces infiltration)

2. **Timber Rampart** (Tier 2)
   - Output: Defense +20%; resilience to minor tides
   - Signature Addition: Reinforced Gate (improves gate hp)

3. **Stone Rampart** (Tier 3)
   - Output: Defense +35%; unlocks tower emplacements
   - Signature Addition: Battlement Walk (enables siege weapons)

4. **Spirit Rampart** (Tier 4)
   - Output: Defense +50%; beast damage reduced
   - Signature Addition: Spirit Channel (qi redistribution)

5. **Elemental Bulwark** (Tier 5)
   - Output: Defense +65%; elemental retaliation
   - Signature Addition: Elemental Bastions (+10% elemental counter)

6. **Celestial Bastion** (Tier 6)
   - Output: Defense +80%; global defense +5%
   - Signature Addition: Celestial Shield Dome (settlement defense +5%)

#### Sentinel Tower Path
The Sentinel Tower provides observation and defensive support through elevated positions.

**Building Type**: Sentinel Tower
- **Category**: `defense`
- **Building Path**: `sentinel_tower`
- **Description**: Provides observation and defensive support through elevated positions

**Tiers**:
1. **Watchpost** (Tier 1)
   - Output: Detection range +10%
   - Signature Addition: Signal Brazier (faster alerts)

2. **Ballista Tower** (Tier 2)
   - Output: Ranged defense support; mission defense +5%
   - Signature Addition: Ballista Battery (anti-beast bolts)

3. **Spirit Beacon** (Tier 3)
   - Output: Detection +20%; nearby morale +5%
   - Signature Addition: Beacon Resonator (reveals stealth threats)

4. **Arcane Tower** (Tier 4)
   - Output: Mission success +5%; reduces ambush chance
   - Signature Addition: Divination Lens (pre-battle intel)

5. **Skywatch Tower** (Tier 5)
   - Output: Detection +35%; ranged drills buff
   - Signature Addition: Sky Beacon (global alert speed +10%)

6. **Heaven's Eye** (Tier 6)
   - Output: Global detection +50%; instantaneous alerts
   - Signature Addition: Heaven's Eye Array (auto-alert network)

#### Ward Bastion Path
The Ward Bastion provides protective barrier wards and defensive formations.

**Building Type**: Ward Bastion
- **Category**: `defense`
- **Building Path**: `ward_bastion`
- **Description**: Provides protective barrier wards and defensive formations

**Tiers**:
1. **Ward Stone** (Tier 1)
   - Output: Barrier strength +10%
   - Signature Addition: Ward Glyphs (basic scripting)

2. **Ward Nexus** (Tier 2)
   - Output: Barrier +20%; reduces spell damage
   - Signature Addition: Anchor Sigils (stabilize network)

3. **Spirit Bastion** (Tier 3)
   - Output: Barrier +35%; gradual structure healing
   - Signature Addition: Spirit Grail (heals structures slowly)

4. **Elemental Ward Bastion** (Tier 4)
   - Output: Barrier +50%; adaptive resistance
   - Signature Addition: Elemental Screen (+10% resist per element)

5. **Grand Ward Matrix** (Tier 5)
   - Output: Barrier +65%; reduces siege fatigue
   - Signature Addition: Matrix Beacon (network integrity monitor)

6. **Celestial Ward Citadel** (Tier 6)
   - Output: Barrier +80%; global qi stability +5%
   - Signature Addition: Celestial Ward Core (+5% qi stability)

#### Beastbane Path
The Beastbane provides anti-beast defensive systems and trap fields.

**Building Type**: Beastbane
- **Category**: `defense`
- **Building Path**: `beastbane`
- **Description**: Provides anti-beast defensive systems and trap fields

**Tiers**:
1. **Spike Trench** (Tier 1)
   - Output: Beast tide damage -10%
   - Signature Addition: Pitfall Nets (trap deployment)

2. **Beast Trap Field** (Tier 2)
   - Output: Capture chance +5%; damage -15%
   - Signature Addition: Net Launcher (capture beasts)

3. **Spirit Lure Grounds** (Tier 3)
   - Output: Damage -25%; extra loot chance
   - Signature Addition: Lure Totems (bonus part drop chance)

4. **Essence Sprayer Field** (Tier 4)
   - Output: Beast offense reduced; mission prep buff
   - Signature Addition: Essence Sprayers (debuff beasts)

5. **Elemental Kill-Zone** (Tier 5)
   - Output: Damage -40%; elemental penetration
   - Signature Addition: Elemental Trap Nodes (+10% elemental damage)

6. **Celestial Beastbreak Array** (Tier 6)
   - Output: Damage -55%; increased retreat chance
   - Signature Addition: Beastbreak Core (forces beast retreat)

### Civic & Administration
Buildings in the Civic & Administration category provide governance, knowledge, and administrative functions.

#### Sect Archive Path
The Sect Archive preserves knowledge, records, and enables research capabilities.

**Building Type**: Sect Archive
- **Category**: `civic`
- **Building Path**: `sect_archive`
- **Description**: Preserves knowledge, records, and enables research capabilities

**Tiers**:
1. **Scriptorium** (Tier 1)
   - Output: Unlocks mission history log
   - Signature Addition: Record Table (mission summaries)

2. **Archive Hall** (Tier 2)
   - Output: Research speed +5%
   - Signature Addition: Index Catalog (research projects)

3. **Spirit Archive** (Tier 3)
   - Output: Knowledge retention +10%; unlocks lore missions
   - Signature Addition: Spirit Codex (lore mission templates)

4. **Grand Archive** (Tier 4)
   - Output: Beast mission rewards +10%
   - Signature Addition: Core Ledger (beast core tracking)

5. **Imperial Archive Annex** (Tier 5)
   - Output: Research speed +15%; unlocks imperial edicts
   - Signature Addition: Imperial Link Sigil (edict system)

6. **Hall of Eternal Records** (Tier 6)
   - Output: Global knowledge retention +5%; unlocks legacy quests
   - Signature Addition: Legacy Vault (legacy quest chains)

#### Diplomatic Embassy Path
The Diplomatic Embassy facilitates inter-sect relations and diplomatic activities.

**Building Type**: Diplomatic Embassy
- **Category**: `commercial`
- **Building Path**: `diplomatic_embassy`
- **Description**: Facilitates inter-sect relations and diplomatic activities

**Tiers**:
1. **Envoy Office** (Tier 1)
   - Output: Unlocks envoy correspondence
   - Signature Addition: Envoy Desk (basic negotiations)

2. **Embassy Hall** (Tier 2)
   - Output: Trade missions +5%; morale +3%
   - Signature Addition: Diplomatic Salon (trade buff)

3. **Spirit Embassy** (Tier 3)
   - Output: Diplomatic success +10%; unlocks treaties
   - Signature Addition: Harmony Chamber (treaty creation)

4. **Grand Embassy** (Tier 4)
   - Output: Diplomacy rate +15%; loyalty +5%
   - Signature Addition: Summit Forum (multi-faction mediation)

5. **Imperial Liaison Court** (Tier 5)
   - Output: Access to imperial missions; renown +10%
   - Signature Addition: Imperial Liaison Office (imperial quests)

6. **Heavenly Concord Pavilion** (Tier 6)
   - Output: Settlement diplomacy +5%; global prosperity +5%
   - Signature Addition: Concord Oath Sigil (global diplomacy buff)

#### Discipline Hall Path
The Discipline Hall maintains order and law enforcement within the sect.

**Building Type**: Discipline Hall
- **Category**: `civic`
- **Building Path**: `discipline_hall`
- **Description**: Maintains order and law enforcement within the sect

**Tiers**:
1. **Discipline Office** (Tier 1)
   - Output: Reduces loyalty loss by 5%
   - Signature Addition: Sanction Ledger (conflict tracking)

2. **Tribunal Hall** (Tier 2)
   - Output: Loyalty +5%; upkeep from penalties down
   - Signature Addition: Tribunal Bench (reduces conflict upkeep)

3. **Spirit Court** (Tier 3)
   - Output: Conflict resolution success +10%
   - Signature Addition: Spirit Judge Totem (fairness aura)

4. **Inner Law Pavilion** (Tier 4)
   - Output: Renown +5%; reduces mission failure penalties
   - Signature Addition: Oath Archive (mission penalty reduction)

5. **Guardian Hall** (Tier 5)
   - Output: Loyalty +10%; unlocks guardian mission support
   - Signature Addition: Guardian Dispatch (guardian missions)

6. **Celestial Court** (Tier 6)
   - Output: Global loyalty +5%; morale +5%
   - Signature Addition: Celestial Verdict Sigil (global loyalty buff)

#### Amphitheater Path
The Amphitheater provides entertainment and festival spaces for morale and cultural events.

**Building Type**: Amphitheater
- **Category**: `commercial`
- **Building Path**: `amphitheater`
- **Description**: Provides entertainment and festival spaces for morale and cultural events

**Tiers**:
1. **Festival Stage** (Tier 1)
   - Output: Festival duration +10%
   - Signature Addition: Banner Stage (event extension)

2. **Amphitheater** (Tier 2)
   - Output: Morale +5%; event capacity +25%
   - Signature Addition: Resonant Shell (audience morale)

3. **Spirit Pavilion Stage** (Tier 3)
   - Output: Morale +10%; unlocks performance quests
   - Signature Addition: Illusion Array (performance buff)

4. **Festival Court** (Tier 4)
   - Output: Festival rewards +10%; trade buff
   - Signature Addition: Festival Market (event trade bonus)

5. **Grand Celebration Grounds** (Tier 5)
   - Output: Morale +15%; loyalty during festivals +10%
   - Signature Addition: Ritual Stage (loyalty buff)

6. **Celestial Festival Plaza** (Tier 6)
   - Output: Global morale +5%; festival cooldown -20%
   - Signature Addition: Celestial Canopy (festival cd reduction)

#### Supply Depot Path
The Supply Depot provides storage and logistics management for the settlement.

**Building Type**: Supply Depot
- **Category**: `production`
- **Building Path**: `supply_depot`
- **Description**: Provides storage and logistics management for the settlement

**Tiers**:
1. **Storehouse** (Tier 1)
   - Output: Storage capacity +10%
   - Signature Addition: Inventory Ledger (stock tracking)

2. **Supply Depot** (Tier 2)
   - Output: Storage +20%; logistics efficiency +5%
   - Signature Addition: Loading Crane (faster loading)

3. **Logistics Hub** (Tier 3)
   - Output: Logistics +10%; reduces transport fatigue
   - Signature Addition: Route Planner (transport optimization)

4. **Spirit Warehouse** (Tier 4)
   - Output: Storage +30%; perishables loss -25%
   - Signature Addition: Qi Cooling Array (loss prevention)

5. **Grand Depot** (Tier 5)
   - Output: Logistics +15%; mission supply prep faster
   - Signature Addition: Flow Rail (supply prep speed)

6. **Celestial Logistics Center** (Tier 6)
   - Output: Global logistics +5%; auto-redistributes surplus
   - Signature Addition: Celestial Dispatch Core (auto distribution)

### Transportation & Infrastructure
Buildings in the Transportation & Infrastructure category provide movement, travel, and connectivity systems.

#### Transit Network Path
The Transit Network provides transportation infrastructure and movement speed improvements.

**Building Type**: Transit Network
- **Category**: `production`
- **Building Path**: `transit_network`
- **Description**: Provides transportation infrastructure and movement speed improvements

**Tiers**:
1. **Caravan Waystation** (Tier 1)
   - Output: Travel speed +5%
   - Signature Addition: Stable Bay (caravan upkeep)

2. **Roadway Hub** (Tier 2)
   - Output: Movement speed +10%
   - Signature Addition: Paved Routes (movement speed)

3. **Spirit Gate** (Tier 3)
   - Output: Instant transport between key nodes
   - Signature Addition: Gate Sigils (teleport points)

4. **Arts of Flight Platform** (Tier 4)
   - Output: Expedition travel time -10%
   - Signature Addition: Sky Launch Platform (flight missions)

5. **Grand Transit Hall** (Tier 5)
   - Output: Travel speed +15%; trade missions faster
   - Signature Addition: Transit Array (mission travel reduction)

6. **Heavenly Transit Nexus** (Tier 6)
   - Output: Global travel speed +20%; mission prep faster
   - Signature Addition: Nexus Core (global travel buff)

#### Teleport Gate Path
The Teleport Gate provides teleportation infrastructure for rapid travel and connectivity.

**Building Type**: Teleport Gate
- **Category**: `production`
- **Building Path**: `teleport_gate`
- **Description**: Provides teleportation infrastructure for rapid travel and connectivity

**Tiers**:
1. **Way Gate** (Tier 1)
   - Output: Unlocks emergency teleports
   - Signature Addition: Way Sigil (short-range teleport)

2. **Portal Chamber** (Tier 2)
   - Output: Mission travel time -15%
   - Signature Addition: Portal Anchor (stable connections)

3. **Spirit Gatehouse** (Tier 3)
   - Output: Teleport upkeep -10%; security +10%
   - Signature Addition: Ward Lock (secure gating)

4. **Intersect Gatehall** (Tier 4)
   - Output: Trade missions speed +10%; diplomacy buff
   - Signature Addition: Trade Gate (market access)

5. **Celestial Gate** (Tier 5)
   - Output: Travel time -30%; unlocks celestial missions
   - Signature Addition: Celestial Key (imperial route)

6. **Gate of Ten Thousand Paths** (Tier 6)
   - Output: Global travel cooldown -20%; crisis response speed +15%
   - Signature Addition: Path Nexus (multiversal network)

### Resource Extraction & Processing
Buildings in the Resource Extraction & Processing category extract and refine raw materials.

#### Ironworks Path
The Ironworks extracts iron ore and rare metals from the earth.

**Building Type**: Ironworks
- **Category**: `resource`
- **Building Path**: `ironworks`
- **Description**: Extracts iron ore and rare metals from the earth

**Tiers**:
1. **Prospector's Pit** (Tier 1)
   - Daily Output: +10 Iron Ore/day
   - Signature Addition: Survey Stakes (+5% discovery chance)

2. **Tunnel Mine** (Tier 2)
   - Daily Output: +25 Iron Ore/day
   - Signature Addition: Winch Lift (+15% hauling efficiency)

3. **Deep Shaft** (Tier 3)
   - Daily Output: +40 Iron Ore/day; +5 Rare Ore/day
   - Signature Addition: Ore Sorting Chute (reduces waste)

4. **Spirit Vein Mine** (Tier 4)
   - Daily Output: +50 Iron Ore/day; +8 Rare Ore/day; +2 Essence Pebbles/day
   - Signature Addition: Spirit Drill Head (+10% rare ore)

5. **Elemental Excavation** (Tier 5)
   - Daily Output: +65 Iron Ore/day; +12 Rare Ore/day; +4 Essence Pebbles/day
   - Signature Addition: Elemental Dampeners (+10% safety, reduces accidents)

6. **Celestial Deepworks** (Tier 6)
   - Daily Output: +90 Iron Ore/day; +15 Rare Ore/day; +6 Essence Pebbles/day
   - Signature Addition: Deepcore Beacon (+5% global construction durability)

#### Alloy Foundry Path
The Alloy Foundry smelts and forges metals into ingots and alloys.

**Building Type**: Alloy Foundry
- **Category**: `production`
- **Building Path**: `alloy_foundry`
- **Description**: Smelts and forges metals into ingots and alloys

**Tiers**:
1. **Smelter Shed** (Tier 1)
   - Daily Output: +10 Iron Ingots/day
   - Signature Addition: Bellows Stand (+10% output)

2. **Foundry Hall** (Tier 2)
   - Daily Output: +20 Iron Ingots/day; +5 Steel Ingots/day
   - Signature Addition: Mold Rack (faster casting)

3. **Spirit Smelter** (Tier 3)
   - Daily Output: +25 Steel Ingots/day; +3 Spirit Alloys/day
   - Signature Addition: Essence Crucible (+10% spirit alloy yield)

4. **Harmonized Forge** (Tier 4)
   - Daily Output: +30 Steel Ingots/day; +6 Spirit Alloys/day
   - Signature Addition: Resonant Anvil (+10% tool/component durability)

5. **Grand Alloy Works** (Tier 5)
   - Daily Output: +35 Steel Ingots/day; +10 Spirit Alloys/day; unlocks Arc Alloy recipes
   - Signature Addition: Elemental Flux Chamber (+15% special alloy yield)

6. **Celestial Forgeworks** (Tier 6)
   - Daily Output: +40 Steel Ingots/day; +15 Spirit Alloys/day; +2 Celestial Alloy/day
   - Signature Addition: Forge Nexus (+5% settlement formation power)

#### Spirit Lode Path
The Spirit Lode processes and refines essence from ores and materials.

**Building Type**: Spirit Lode
- **Category**: `production`
- **Building Path**: `spirit_lode`
- **Description**: Processes and refines essence from ores and materials

**Tiers**:
1. **Essence Sifter** (Tier 1)
   - Daily Output: +3 Essence Pebbles/day
   - Signature Addition: Pebble Screens (+10% yield)

2. **Spirit Separator** (Tier 2)
   - Daily Output: +6 Essence Pebbles/day; +1 Essence Shard/day
   - Signature Addition: Resonant Drum (+10% separation efficiency)

3. **Essence Refiner** (Tier 3)
   - Daily Output: +3 Essence Stones/day
   - Signature Addition: Purification Basin (+10% purity)

4. **Spirit Matrix** (Tier 4)
   - Daily Output: +5 Essence Stones/day; +1 Spirit Core/day
   - Signature Addition: Matrix Node (unlocks spirit catalyst recipes)

5. **Elemental Synthesis Lab** (Tier 5)
   - Daily Output: +6 Essence Stones/day; +2 Elemental Catalysts/day
   - Signature Addition: Catalyst Array (+15% alchemy/formation success)

6. **Celestial Essence Vault** (Tier 6)
   - Daily Output: +8 Essence Stones/day; +3 Celestial Cores/day
   - Signature Addition: Harmonic Vault (+5% global qi prosperity)

#### Spiritwood Atelier Path
The Spiritwood Atelier infuses wood with qi to create spirit timber and specialized materials.

**Building Type**: Spiritwood Atelier
- **Category**: `production`
- **Building Path**: `spiritwood_atelier`
- **Description**: Infuses wood with qi to create spirit timber and specialized materials

**Tiers**:
1. **Spiritwood Forge** (Tier 1)
   - Output: Spirit Timber (small batches)
   - Signature Addition: Conduit Stones (+10% infusion rate)

2. **Infusion Chamber** (Tier 2)
   - Output: Increased Spirit Timber yield
   - Signature Addition: Qi Reservoir (ambient qi storage for efficiency)

3. **Spirit Timber Workshop** (Tier 3)
   - Output: Spirit Timber + Rune-etched Timber
   - Signature Addition: Inscription Bench (engraves minor runes)

4. **Elemental Atelier** (Tier 4)
   - Output: Elemental Spirit Timber variants
   - Signature Addition: Essence Collector (chance for rare timber types)

5. **Resonant Atelier** (Tier 5)
   - Output: +15% output; generates Resonant Timber
   - Signature Addition: Resonance Frame (+15% output, faster skill gain)

6. **Spiritwood Conservatory** (Tier 6)
   - Output: Spirit Timber, Resonant Timber, +5% qi efficiency aura
   - Signature Addition: Heart Resonance Array (nearby buildings +5% qi efficiency)

### Commerce & Culture
Buildings in the Commerce & Culture category focus on social cohesion, prestige, commerce, and cultural development.

#### Artisan Guild Hall Path
The Artisan Guild Hall coordinates crafters, creates prestige goods, and facilitates trade.

**Building Type**: Artisan Guild Hall
- **Category**: `commercial` (or `culture` - can be configured)
- **Building Path**: `artisan_guild_hall`
- **Description**: Coordinates crafters, creates prestige goods, and facilitates trade

**Tiers**:
1. **Artisan's Corner** (Tier 1)
   - Output: Prestige Goods (minor); +2 morale radius
   - Signature Addition: Showroom (aesthetics +2; unlocks décor placement)

2. **Craft Hall** (Tier 2)
   - Output: Enables Crafting Commissions (missions)
   - Signature Addition: Guild Charter (mission board interface)

3. **Artisan Guild Hall** (Tier 3)
   - Output: Trade refined lumber/furniture for currency/prestige
   - Signature Addition: Marketplace Annex (trade orders unlocked)

4. **Guild of Spirit Artisans** (Tier 4)
   - Output: Prestige Goods gain qi attunements; morale +5 zone
   - Signature Addition: Inspiration Fountain (morale & creativity buff)

5. **Master Artisan Assembly** (Tier 5)
   - Output: Converts surplus refined goods → Prestige Seals
   - Signature Addition: Exhibition Hall (prestige conversion & showcases)

6. **Verdant Artisan Court** (Tier 6)
   - Output: Living Art (+10% settlement morale, +5% qi generation)
   - Signature Addition: Living Art installations (apply settlement-wide buffs)

#### Feast Hall Path
The Feast Hall provides communal dining and celebration spaces that boost morale and loyalty.

**Building Type**: Feast Hall
- **Category**: `commercial` (or `culture` - can be configured)
- **Building Path**: `feast_hall`
- **Description**: Provides communal dining and celebration spaces that boost morale and loyalty

**Tiers**:
1. **Dining Hall** (Tier 1)
   - Output: Morale +5% (local radius)
   - Signature Addition: Wall Lanterns (+5% morale)

2. **Banquet Hall** (Tier 2)
   - Output: Morale +8%; buffs nearby housing
   - Signature Addition: Music Corner (housing morale bonus)

3. **Celebration Hall** (Tier 3)
   - Output: Loyalty gain +10% for disciples
   - Signature Addition: Honor Plaques (loyalty progression boost)

4. **Spirit Feast Hall** (Tier 4)
   - Output: Disciple recovery +10%; morale +10%
   - Signature Addition: Communion Bowl (+10% recovery rate)

5. **Grand Pavilion of Feasts** (Tier 5)
   - Output: Settlement productivity +5%; morale +12%
   - Signature Addition: Banner Arrays (+5% productivity)

6. **Hall of Abundance** (Tier 6)
   - Output: Periodic global morale surge; +3% qi prosperity
   - Signature Addition: Harvest Festival Rite (scheduled global morale event)

## Notes

- Each building path will have its own 6-tier upgrade system
- Signature additions are unique to each tier
- Buildings in the same category can form districts when clustered together
- Buildings can belong to supply chains for proximity bonuses

## Future Additions

Additional building paths and categories will be added as the game design evolves. This document will be updated to reflect new building types.

