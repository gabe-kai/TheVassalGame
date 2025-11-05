# NPC AI & Behavior System

## Table of Contents
- [Overview](#overview)
- [NPC State Machine](#npc-state-machine)
- [NPC Decision-Making](#npc-decision-making)
- [NPC Needs & Wants](#npc-needs--wants)
- [Job Assignment System](#job-assignment-system)
- [NPC Behavior Trees](#npc-behavior-trees)
- [Social Interaction System](#social-interaction-system)
- [Event Response System](#event-response-system)
- [NPC Learning & Adaptation](#npc-learning--adaptation)
- [Emergency Response](#emergency-response)
- [Player Interaction](#player-interaction)

## Overview

NPCs (Non-Player Characters) are the lifeblood of TheVassalGame's city simulation. They work in buildings, form relationships, respond to events, and make autonomous decisions based on their personality, needs, and circumstances. NPCs are persistent entities with evolving personalities, skills, and relationships that create a living, breathing world.

**Key Principles:**
- **Autonomous Decision-Making**: NPCs make their own choices based on needs, personality, and circumstances
- **Personality-Driven**: Personality traits derived from events influence all NPC behavior
- **Relationship-Based**: Relationships with other NPCs and buildings affect behavior and decisions
- **Need-Driven**: NPCs prioritize actions based on their current needs (hunger, rest, social, work satisfaction)
- **Skill-Based**: NPC skills determine job eligibility and performance
- **Evolving**: NPCs learn, adapt, and change over time based on experiences

---

## NPC State Machine

### Core States

NPCs transition between states based on their current situation, needs, and assigned tasks:

**1. Idle**
- **Description**: NPC has no active task and is free to choose actions
- **Entry Conditions**: 
  - No assigned job
  - Job completed
  - Shift ended
  - Task completed
- **Exit Conditions**:
  - Assigned a job
  - Needs trigger (hunger, rest, social)
  - Random event occurs
  - Player order received
- **Behavior**: NPC evaluates needs and decides next action

**2. Working**
- **Description**: NPC is actively performing job duties at assigned building
- **Entry Conditions**:
  - Assigned to building
  - Shift started
  - Job task available
- **Exit Conditions**:
  - Shift ended
  - Job completed
  - Building destroyed/damaged
  - Need threshold reached (hunger, rest)
  - Emergency occurs
- **Behavior**: 
  - Perform job tasks (production, services, etc.)
  - Gain skill experience
  - Interact with coworkers
  - Generate relationship events

**3. Moving**
- **Description**: NPC is traveling to a destination
- **Entry Conditions**:
  - Destination selected (building, location, NPC)
  - Pathfinding initiated
- **Exit Conditions**:
  - Destination reached
  - Path blocked/interrupted
  - Emergency occurs
  - Need threshold reached (critical hunger, health)
- **Behavior**:
  - Follow pathfinding route
  - Avoid obstacles
  - Respond to nearby events
  - May interact with NPCs along path

**4. Fighting**
- **Description**: NPC is engaged in combat
- **Entry Conditions**:
  - Enemy detected (beast, hostile NPC, player)
  - Territory attacked
  - Building attacked
  - Combat initiated
- **Exit Conditions**:
  - Enemy defeated
  - Enemy fled
  - NPC defeated/fled
  - Combat resolved
- **Behavior**:
  - Engage in combat (see Combat AI in `docs/combat-mechanics.md`)
  - Use techniques and equipment
  - May seek glory (high ego cultivators)
  - May flee if health low (low ego or cautious personality)

**5. Resting**
- **Description**: NPC is resting to recover stamina/health
- **Entry Conditions**:
  - Stamina below threshold (30%)
  - Health below threshold (50%)
  - Shift ended (workers)
  - Forced rest by player
- **Exit Conditions**:
  - Stamina/health recovered
  - Rest time expired
  - Emergency occurs
  - Player order received
- **Behavior**:
  - Regenerate stamina/health
  - May visit rest areas (homes, inns, meditation halls)
  - May socialize while resting

**6. Socializing**
- **Description**: NPC is engaging in social interactions
- **Entry Conditions**:
  - Social need threshold reached
  - Friend/rival nearby
  - Social event triggered
  - Building visit (tavern, feast hall, etc.)
- **Exit Conditions**:
  - Social need satisfied
  - Friend/rival leaves
  - Time limit reached
  - Work/emergency interrupts
- **Behavior**:
  - Interact with nearby NPCs
  - Visit social buildings
  - Build/maintain relationships
  - Generate relationship events

**7. Eating**
- **Description**: NPC is consuming food to satisfy hunger
- **Entry Conditions**:
  - Hunger below threshold (40%)
  - Meal time (if scheduled)
  - Food available
- **Exit Conditions**:
  - Hunger satisfied
  - Food consumed
  - Emergency occurs
- **Behavior**:
  - Travel to food source (kitchen, market, feast hall)
  - Consume food
  - May socialize while eating
  - Restore hunger value

**8. Training**
- **Description**: NPC is practicing skills or cultivation
- **Entry Conditions**:
  - Assigned to training
  - Skill improvement needed
  - Cultivation practice (cultivators)
  - Player order
- **Exit Conditions**:
  - Training session completed
  - Skill/Cultivation goal reached
  - Need threshold reached
  - Emergency occurs
- **Behavior**:
  - Practice at training grounds
  - Gain skill experience
  - Cultivators practice cultivation
  - May interact with other trainees

**9. Patrolling**
- **Description**: NPC is assigned to territory patrol
- **Entry Conditions**:
  - Assigned to patrol route
  - Patrol active
- **Exit Conditions**:
  - Patrol completed
  - Patrol interrupted (combat, emergency)
  - Patrol assignment removed
- **Behavior**:
  - Follow patrol route
  - Detect and engage beast incursions
  - Report findings
  - Defend territory perimeter

**10. Seeking**
- **Description**: NPC is searching for something (job, resource, location, NPC)
- **Entry Conditions**:
  - Job search initiated
  - Resource search needed
  - Location search (exploration)
  - NPC search (friend, rival)
- **Exit Conditions**:
  - Target found
  - Search abandoned (time limit, need threshold)
  - Alternative found
- **Behavior**:
  - Explore territory
  - Check available buildings/jobs
  - Query information from other NPCs
  - Make decisions based on findings

### State Transition Logic

**Priority System:**
1. **Emergency States** (highest priority): Fighting, Emergency Response
2. **Critical Needs**: Health/Stamina restoration (if critical)
3. **Assigned Tasks**: Working, Patrolling, Training (if assigned)
4. **Scheduled Activities**: Eating (meal times), Resting (shift end)
5. **Social Needs**: Socializing (if threshold reached)
6. **Idle Activities**: Seeking, Exploring, Idle

**State Transition Formula:**
```
If Emergency: Transition to Fighting/Emergency
Else If Critical Need: Transition to Resting/Eating
Else If Assigned Task: Transition to Working/Patrolling/Training
Else If Scheduled Activity: Transition to Eating/Resting
Else If Social Need: Transition to Socializing
Else: Transition to Idle/Seeking
```

**Personality Influence:**
- **Cautious NPCs**: May prioritize safety over assigned tasks
- **Ambitious NPCs**: May prioritize work/training over social needs
- **Friendly NPCs**: May prioritize socializing over other needs
- **Lazy NPCs**: May extend resting/eating states longer

---

## NPC Decision-Making

### Decision Framework

NPCs make decisions using a weighted priority system that considers:
1. **Current Needs** (hunger, rest, social, safety)
2. **Personality Traits** (cautious, ambitious, friendly, etc.)
3. **Relationships** (friends, rivals, loyalty to player)
4. **Skills & Abilities** (job eligibility, combat effectiveness)
5. **Current State** (working, idle, fighting, etc.)
6. **Available Opportunities** (jobs, resources, events)
7. **Ego Score** (especially for cultivators - glory-seeking behavior)

### Decision Algorithm

**Step 1: Evaluate Needs**
```
For each need (hunger, rest, social, safety, work_satisfaction):
  Calculate need_urgency = (need_threshold - current_need) / need_threshold
  If need_urgency > 0.5: Add to priority_queue
```

**Step 2: Apply Personality Modifiers**
```
For each need in priority_queue:
  Apply personality_modifier:
    - Cautious: +20% to safety needs
    - Ambitious: +20% to work needs
    - Friendly: +20% to social needs
    - Lazy: -20% to work needs, +20% to rest needs
```

**Step 3: Evaluate Opportunities**
```
For each available opportunity (job, event, interaction):
  Calculate opportunity_score = base_score × personality_fit × skill_match × relationship_bonus
  Add to opportunity_queue
```

**Step 4: Select Action**
```
If highest_priority_need.urgency > 0.8:
  Select action to satisfy need
Else If highest_opportunity_score > threshold:
  Select opportunity action
Else:
  Select idle/default action
```

### Job Selection Decision

When an NPC needs to choose or change jobs:

**Job Evaluation Formula:**
```
job_score = base_pay_score + skill_match_score + location_score + 
            coworker_relationship_score + personality_fit_score + 
            advancement_opportunity_score

Where:
- base_pay_score = job_pay / max_pay (0.0 to 1.0)
- skill_match_score = (NPC_skill_level / required_skill_level) × 0.3
- location_score = (1 - distance_to_job / max_distance) × 0.2
- coworker_relationship_score = average_relationship_with_coworkers × 0.2
- personality_fit_score = personality_match_with_job_type × 0.2
- advancement_opportunity_score = (promotion_possibility / max_promotion) × 0.1
```

**Personality Influence:**
- **Ambitious NPCs**: Weight advancement_opportunity_score higher (+50%)
- **Friendly NPCs**: Weight coworker_relationship_score higher (+50%)
- **Lazy NPCs**: Weight base_pay_score higher, skill_match lower
- **Cautious NPCs**: Prefer familiar jobs (bonus for current job type)

**Job Change Triggers:**
- Current job satisfaction < 40%
- Better opportunity found (job_score > current_job_score + 20%)
- Relationship with coworkers < -30 (rivalry)
- Building destroyed or job eliminated
- Player order/assignment

---

## NPC Needs & Wants

### Core Needs System

NPCs have several core needs that drive behavior:

**1. Hunger (0-100%)**
- **Base Decay**: 1% per 10 minutes (active), 0.5% per 10 minutes (resting)
- **Critical Threshold**: 20% (NPC prioritizes eating)
- **Satisfaction**: +50% per meal consumed
- **Sources**: Kitchens, markets, feast halls, food items
- **Behavior**: NPCs seek food when hunger < 40%

**2. Rest/Stamina (0-100%)**
- **Base Decay**: Varies by activity (working: 2%/min, fighting: 5%/min, idle: 0.5%/min)
- **Critical Threshold**: 20% (NPC must rest)
- **Recovery**: 5% per minute resting, 10% per minute sleeping
- **Sources**: Homes, inns, meditation halls
- **Behavior**: NPCs rest when stamina < 30% or shift ends

**3. Social (0-100%)**
- **Base Decay**: 0.5% per hour (varies by personality: introverts decay slower)
- **Critical Threshold**: 30% (NPC seeks social interaction)
- **Satisfaction**: +10-30% per social interaction (depends on relationship quality)
- **Sources**: Friends, coworkers, social buildings (taverns, feast halls)
- **Behavior**: NPCs socialize when social < 40% (friendly NPCs: < 60%)

**4. Safety (0-100%)**
- **Current Level**: Based on territory security, building safety, combat threats
- **Critical Threshold**: 30% (NPC feels unsafe)
- **Influences**: 
  - Territory loyalty (high loyalty = safer)
  - Beast incursions (active = unsafe)
  - Combat nearby (very unsafe)
  - Building defenses (safer)
- **Behavior**: NPCs may flee or seek shelter when safety < 40%

**5. Work Satisfaction (0-100%)**
- **Current Level**: Based on job quality, pay, coworkers, advancement
- **Critical Threshold**: 40% (NPC considers job change)
- **Influences**:
  - Job pay vs. market rate
  - Skill-job match (better match = higher satisfaction)
  - Coworker relationships (positive = higher satisfaction)
  - Advancement opportunities
  - Building conditions (well-maintained = higher satisfaction)
- **Behavior**: NPCs may seek new jobs when satisfaction < 40%

**6. Autonomy (0-100%)**
- **Current Level**: Based on player control, orders, restrictions
- **Critical Threshold**: 30% (NPC resists orders)
- **Influences**:
  - Number of player orders
  - Ego score (high ego = needs more autonomy)
  - Cultivation level (cultivators need more autonomy)
  - Personality (ambitious NPCs need autonomy)
- **Behavior**: High ego/cultivator NPCs may ignore orders if autonomy < 30%

### Need Priority Calculation

**Urgency Formula:**
```
need_urgency = (need_threshold - current_need) / need_threshold

If need_urgency > 0:
  priority = need_urgency × personality_weight × base_priority
Else:
  priority = 0
```

**Base Priorities:**
- Hunger: 1.0 (critical for survival)
- Rest/Stamina: 0.9 (critical for function)
- Safety: 0.8 (critical for survival)
- Social: 0.5 (important for well-being)
- Work Satisfaction: 0.4 (important for productivity)
- Autonomy: 0.3 (important for cultivators/high ego)

**Personality Weights:**
- **Friendly NPCs**: Social +50%, Hunger -20%
- **Ambitious NPCs**: Work Satisfaction +50%, Social -30%
- **Cautious NPCs**: Safety +50%, Autonomy -20%
- **Lazy NPCs**: Rest +50%, Work Satisfaction -50%

---

## Job Assignment System

### Auto-Assignment Algorithm

**Step 1: Identify Available Jobs**
```
For each building in territory:
  If building needs workers:
    Calculate workers_needed = building.employment_slots - current_workers
    For each slot:
      Identify required_skills
      Add to available_jobs_queue
```

**Step 2: Match NPCs to Jobs**
```
For each idle NPC:
  For each available_job:
    Calculate job_match_score = skill_match + location_score + personality_fit
    If job_match_score > threshold:
      Add (NPC, job) to candidate_matches
```

**Step 3: Resolve Conflicts**
```
Sort candidate_matches by job_match_score (descending)
For each match:
  If NPC not yet assigned AND job not yet filled:
    Assign NPC to job
    Remove from candidate_matches
```

**Step 4: Handle Unfilled Jobs**
```
For each unfilled job:
  If building.auto_recruit = true:
    Create job posting (NPCs can apply)
  Else:
    Wait for manual assignment
```

### Manual Assignment

**Player Assignment:**
- Player can manually assign NPCs to buildings
- Player can override auto-assignment
- Player can reassign NPCs
- Player can remove NPCs from jobs

**NPC Application:**
- NPCs can apply for posted jobs
- NPCs compare job to current job
- NPCs switch if new job is significantly better (+20% score)
- NPCs consider relationship with coworkers at new job

### Job Satisfaction Calculation

**Satisfaction Formula:**
```
base_satisfaction = 50

pay_satisfaction = (job_pay / market_rate_pay) × 30
skill_satisfaction = (NPC_skill_level / required_skill_level) × 20
coworker_satisfaction = average_relationship_with_coworkers × 20
location_satisfaction = (1 - distance_to_job / max_acceptable_distance) × 10
advancement_satisfaction = promotion_possibility × 10
building_condition_satisfaction = building_health_percentage × 10

total_satisfaction = base_satisfaction + pay_satisfaction + skill_satisfaction + 
                    coworker_satisfaction + location_satisfaction + 
                    advancement_satisfaction + building_condition_satisfaction

Final satisfaction = min(100, max(0, total_satisfaction))
```

**Satisfaction Thresholds:**
- **90-100%**: Excellent (NPC very happy, unlikely to leave)
- **70-89%**: Good (NPC content, occasional job search)
- **50-69%**: Acceptable (NPC neutral, may search for better)
- **30-49%**: Poor (NPC dissatisfied, actively searching)
- **0-29%**: Critical (NPC very unhappy, will leave soon)

---

## NPC Behavior Trees

### Worker Behavior Tree

**Root Node: State Check**
- **Idle**: → Evaluate Needs → Select Action
- **Working**: → Perform Job Tasks → Check Needs → Continue/Exit
- **Moving**: → Follow Path → Check Obstacles → Continue/Recalculate
- **Fighting**: → Combat AI (see `docs/combat-mechanics.md`)
- **Resting**: → Rest → Check Recovery → Continue/Exit

**Idle Node: Evaluate Needs**
- **Hunger < 40%**: → Find Food → Move to Food Source → Eat
- **Stamina < 30%**: → Find Rest Area → Move to Rest Area → Rest
- **Social < 40%**: → Find Social Opportunity → Socialize
- **Work Satisfaction < 40%**: → Search for Jobs → Evaluate Opportunities → Apply/Switch
- **No Critical Needs**: → Idle Actions (wander, explore, socialize)

**Working Node: Perform Job Tasks**
- **Check Building Status**: Destroyed? → Exit Job
- **Check Shift**: Shift ended? → Exit Job
- **Check Stamina**: Stamina < 20%? → Request Break → Rest
- **Perform Task**: Execute job function → Gain XP → Check for Events
- **Interact with Coworkers**: Chance to socialize → Update Relationships

### Guard Behavior Tree

**Root Node: State Check**
- **Patrolling**: → Follow Patrol Route → Check for Threats → Engage/Continue
- **Fighting**: → Combat AI
- **Idle**: → Return to Guard Post → Wait for Orders
- **Resting**: → Rest → Return to Duty

**Patrolling Node: Check for Threats**
- **Beast Detected**: → Engage Beast → Combat → Report
- **Hostile NPC Detected**: → Alert → Engage/Report
- **Player Order**: → Follow Order → Return to Patrol
- **No Threats**: → Continue Patrol → Check Route Progress

### Trader Behavior Tree

**Root Node: State Check**
- **Trading**: → Execute Trade → Update Inventory → Check Prices
- **Traveling**: → Follow Trade Route → Check Safety → Continue/Flee
- **Idle**: → Evaluate Market → Plan Routes → Execute Trades
- **Resting**: → Rest → Continue Trading

**Trading Node: Execute Trade**
- **Check Market Prices**: Compare prices → Find Best Deals
- **Check Inventory**: What to sell? What to buy?
- **Negotiate**: Interact with other traders/NPCs
- **Execute Trade**: Complete transaction → Update relationships
- **Plan Next Trade**: Evaluate opportunities → Select destination

### Citizen Behavior Tree

**Root Node: State Check**
- **Idle**: → Evaluate Needs → Select Activity
- **Socializing**: → Interact with NPCs → Build Relationships
- **Visiting Building**: → Travel to Building → Interact → Leave
- **Resting**: → Rest at Home → Socialize with Family
- **Working**: → Part-time work (if needed)

**Idle Node: Select Activity**
- **Social Need**: → Visit Social Buildings → Meet Friends
- **Hunger**: → Find Food → Eat
- **Entertainment**: → Visit Entertainment Buildings
- **Exploration**: → Explore Territory → Discover Locations
- **Random Event**: → Respond to Event → Update Relationships

---

## Social Interaction System

### Relationship Formation

**Proximity-Based:**
- NPCs near each other (within 50m) for extended periods form relationships
- Working together increases relationship formation rate
- Living near each other (same district) increases relationship formation

**Event-Based:**
- Shared experiences create relationships
- Helping each other increases relationship
- Competing for same job decreases relationship
- Random events involving multiple NPCs create relationships

**Compatibility-Based:**
- Personality compatibility affects relationship formation speed
- Similar personalities (both friendly) = faster relationship
- Opposing personalities (friendly vs. antisocial) = slower relationship
- Skills/interests compatibility affects relationship quality

**Relationship Formation Formula:**
```
relationship_formation_rate = base_rate × proximity_multiplier × 
                              event_multiplier × compatibility_multiplier

Where:
- base_rate = 0.1 per hour (when in proximity)
- proximity_multiplier = 1.0 (same building) to 0.1 (50m away)
- event_multiplier = 1.0 (no events) to 5.0 (major shared event)
- compatibility_multiplier = 0.5 (opposing) to 2.0 (compatible)
```

### Relationship Maintenance

**Regular Interactions:**
- NPCs maintain relationships through regular contact
- Relationships decay if no interaction for extended period (1 point per week)
- Social interactions increase relationship (+1 to +5 per interaction)
- Working together maintains relationships

**Gifts & Favors:**
- NPCs can give gifts to improve relationships (+5 to +15)
- Helping NPCs in need improves relationships (+10 to +20)
- Sharing resources improves relationships (+5 to +10)

**Conflict Resolution:**
- Disagreements decrease relationships (-5 to -15)
- Conflicts can be resolved through negotiation (+5 to +10)
- Unresolved conflicts lead to rivalries (relationship < -30)

### Relationship Types

**Friendship (30-100):**
- NPCs help each other
- NPCs seek each other out for socializing
- NPCs share information and resources
- NPCs may form groups/teams

**Acquaintance (0-29):**
- Neutral relationship
- Basic interactions
- No strong feelings

**Rivalry (-30 to -1):**
- NPCs compete for resources/jobs
- NPCs may avoid each other
- NPCs may sabotage each other
- Conflicts may escalate

**Enmity (-100 to -31):**
- Strong negative relationship
- NPCs actively work against each other
- NPCs may attack each other (if circumstances allow)
- Very difficult to repair

---

## Event Response System

### Event Detection

NPCs detect and respond to events in their environment:

**Event Types:**
- **Personal Events**: Directly affect the NPC (job offer, injury, discovery)
- **Social Events**: Involve other NPCs (friend in trouble, celebration, conflict)
- **Territory Events**: Affect territory (beast incursion, building completion, disaster)
- **Random Events**: Unexpected occurrences (found item, chance encounter, opportunity)

**Event Detection Range:**
- **Personal**: Always detected (affects NPC directly)
- **Social**: Detected if relationship > 20 (friend/rival)
- **Territory**: Detected if NPC in territory (within 500m)
- **Random**: Detected based on proximity and personality (friendly NPCs detect more social events)

### Event Response Algorithm

**Step 1: Evaluate Event Importance**
```
event_importance = base_importance × relationship_modifier × 
                   personality_modifier × proximity_modifier

Where:
- base_importance = event_severity (minor: 1, major: 5, life-changing: 10)
- relationship_modifier = 1.0 (stranger) to 3.0 (close friend/rival)
- personality_modifier = personality trait relevance (cautious NPCs respond to danger events)
- proximity_modifier = 1.0 (nearby) to 0.1 (far away)
```

**Step 2: Determine Response**
```
If event_importance > 7.0:
  Interrupt current activity → Respond to event
Else If event_importance > 4.0:
  Add to priority queue → Respond when available
Else:
  Note event → May respond later
```

**Step 3: Execute Response**
```
For personal events:
  - Direct response (accept job, treat injury, use item)
For social events:
  - Travel to NPC → Interact → Update relationship
For territory events:
  - Assess situation → Take action (defend, help, flee)
For random events:
  - Evaluate opportunity → Take action or ignore
```

### Personality-Based Responses

**Cautious NPCs:**
- Avoid dangerous events
- Prefer safe responses
- May flee from threats
- Slow to respond to opportunities

**Ambitious NPCs:**
- Seek opportunity events
- Take risks for advancement
- Compete for resources/jobs
- Quick to respond to opportunities

**Friendly NPCs:**
- Prioritize social events
- Help friends in need
- Seek social interactions
- Respond to relationship events

**Lazy NPCs:**
- Ignore low-importance events
- Prefer rest over action
- Slow to respond
- May miss opportunities

---

## NPC Learning & Adaptation

### Skill Progression

**Experience Gain:**
- NPCs gain skill experience by performing related tasks
- Working at buildings increases building-related skills
- Training increases skills faster
- Combat increases combat-related skills

**Skill Level Formula:**
```
skill_experience_gain = base_xp × task_difficulty × skill_match × 
                        building_efficiency × qi_modifier

Where:
- base_xp = 1-10 per task (depends on skill)
- task_difficulty = 0.5 (easy) to 2.0 (challenging)
- skill_match = current_skill_level / required_skill_level (max 1.5)
- building_efficiency = building_tier × building_condition
- qi_modifier = 1.0 (mortals) to 1.5 (cultivators with qi enhancement)
```

**Skill Cap:**
- **Mortals**: Skills cap at level 50
- **Cultivators**: Skills can exceed 50 (up to 100+)

### Preference Learning

**Job Preferences:**
- NPCs develop preferences for job types they've worked
- Success at a job increases preference (+0.1 per successful shift)
- Failure decreases preference (-0.05 per failed task)
- Personality affects preference development

**Location Preferences:**
- NPCs prefer familiar locations
- Positive experiences increase location preference
- Negative experiences decrease location preference
- NPCs may avoid locations with negative memories

**Social Preferences:**
- NPCs prefer spending time with friends
- NPCs avoid rivals/enemies
- NPCs may develop favorite buildings (taverns, training grounds)
- NPCs may avoid buildings with negative associations

### Adaptation to Circumstances

**Territory Changes:**
- NPCs adapt to new buildings
- NPCs adjust to territory expansion
- NPCs respond to territory threats (beast incursions)
- NPCs may relocate if territory becomes unsafe

**Relationship Changes:**
- NPCs adjust behavior based on relationship changes
- New friendships open new opportunities
- Rivalries create conflicts
- NPCs may change jobs to avoid rivals

**Personality Evolution:**
- Major events cause personality shifts
- Consistent patterns reinforce traits
- NPCs become more cautious after trauma
- NPCs become more ambitious after success

---

## Emergency Response

### Emergency Detection

NPCs detect emergencies through:
- **Combat**: Immediate detection if in combat
- **Proximity**: Detect emergencies within 100m
- **Alerts**: Territory-wide alerts (beast incursions, attacks)
- **Building Damage**: Detect if building is attacked/destroyed

### Emergency Response Types

**1. Combat Response**
- **Guards**: Engage enemies immediately
- **Workers**: May flee or hide (depends on personality)
- **Cultivators**: May seek glory (high ego) or assist (high loyalty)
- **Civilians**: Typically flee to safety

**2. Building Defense**
- **Workers**: May defend building if loyalty high
- **Guards**: Defend assigned buildings
- **Cultivators**: May defend if building is important
- **Civilians**: Typically evacuate

**3. Territory Defense**
- **Guards**: Patrol and defend territory
- **Cultivators**: May join defense (especially high ego)
- **Workers**: May assist if loyalty high
- **Civilians**: Typically seek shelter

**4. Evacuation**
- **Civilians**: Evacuate to safe areas
- **Workers**: May evacuate if building unsafe
- **Guards**: Last to evacuate (protect others)
- **Cultivators**: May stay to fight (high ego)

### Emergency Response Priority

**Priority Order:**
1. **Self-Preservation**: Health/safety critical
2. **Protect Allies**: Friends, family, coworkers
3. **Defend Territory**: High loyalty NPCs
4. **Follow Orders**: Player orders (if loyalty high)
5. **Seek Glory**: High ego cultivators

**Personality Influence:**
- **Cautious NPCs**: Prioritize self-preservation
- **Loyal NPCs**: Prioritize territory/player
- **High Ego NPCs**: May prioritize glory over safety
- **Friendly NPCs**: Prioritize protecting friends

---

## Player Interaction

### Player Orders

**Order Types:**
- **Job Assignment**: Assign NPC to building/job
- **Movement**: Order NPC to location
- **Combat**: Order NPC to attack/defend
- **Training**: Order NPC to train skill
- **Patrol**: Assign NPC to patrol route

**Order Acceptance:**
```
order_acceptance = base_loyalty + relationship_modifier + 
                   ego_modifier + personality_modifier + 
                   order_reasonableness

Where:
- base_loyalty = relationship with player (0-100)
- relationship_modifier = (relationship - 50) / 50 (scaled)
- ego_modifier = -(ego_score - 50) / 50 (high ego = less accepting)
- personality_modifier = personality trait (cautious NPCs reject dangerous orders)
- order_reasonableness = 1.0 (reasonable) to 0.0 (unreasonable/dangerous)

If order_acceptance > 0.5:
  NPC accepts order
Else:
  NPC may refuse or ignore order
```

**Order Resistance:**
- High ego NPCs may refuse orders
- Cultivators may refuse orders (seek autonomy)
- Low loyalty NPCs may ignore orders
- Unreasonable orders may be refused
- NPCs may delay execution (passive resistance)

### Player Requests

**Request Types:**
- **Information**: Ask NPC about territory, events, other NPCs
- **Assistance**: Request help with task
- **Trade**: Request trade or resource sharing
- **Social**: Invite NPC to event or building

**Request Response:**
```
request_response = relationship_modifier + personality_modifier + 
                   request_type_modifier + availability_modifier

Where:
- relationship_modifier = relationship / 100
- personality_modifier = personality trait (friendly NPCs accept social requests)
- request_type_modifier = 1.0 (easy) to 0.5 (difficult)
- availability_modifier = 1.0 (available) to 0.0 (busy)

If request_response > 0.6:
  NPC accepts request
Else:
  NPC may refuse or negotiate
```

### NPC Conversations

NPCs can engage in conversations with players:
- **Greetings**: Based on relationship and personality
- **Information Sharing**: NPCs share information about territory, events, other NPCs
- **Requests**: NPCs may request help, resources, or favors
- **Complaints**: NPCs may complain about jobs, relationships, or conditions
- **Suggestions**: NPCs may suggest improvements or opportunities

**Conversation Topics:**
- Current job and satisfaction
- Relationships with other NPCs
- Recent events
- Territory conditions
- Requests for help
- Suggestions for improvements

---

## Summary

The NPC AI & Behavior System creates autonomous, personality-driven NPCs that:
- Make decisions based on needs, personality, and relationships
- Transition between states based on circumstances
- Form and maintain relationships with other NPCs
- Respond to events and adapt to circumstances
- Learn and evolve over time
- Interact with players in meaningful ways

This system ensures NPCs feel alive and create emergent gameplay through their interactions, decisions, and relationships.

---

**Last Updated:** 2025-11-05

