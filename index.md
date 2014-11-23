---
title: This is my title
layout: default
---

## Abstract

Puerta del Mar is a marine ecosystem simulation environment engine. The project is started as a collaborative effort during **Interactivos?14 workshop** at MediaLab Prado in Madrid. Theme for this 16th edition of the event is "Rethinking collective behaviour and action" and it's reflected in our work: ecosystem by itself is already a collaborative environment as well we are working on implementing various scenarios and tools in ecosystem to show difference between collaborative/collective action and individual/selfish.

## Strategy

Technically and strategically we are building a universal engine, which will be relatively easy to adopt to use as a core in different simulations, ecosystems and visualisations from very abstract to quite realistic, just to mention few ideas: planetarium/cosmos visualisation, microbiological sim - immune system visualisation??, historical war battles - realtime tweakable visualisations, timeline based visualisations like evolution of language/alphabet or may be bananas agricultural selection? Igor is concerned: marine ecosystem is a good universal example to start with coding. It will give different examples, which could be adopted later for building up variations mentioned before. 

## Practice

The first practical application of the engine will be in Andrey's MA dissertation project - an explorative immersive art installation exploring the borders of virtual reality and real world from a point of view of a fish. Not only this work between collaborators might adopt the engine in the future: Marta is working on Collective behaviour at PolaviejaLab,  Ismael had as a final MA work 2D ecosystem named "Info-Alive" and Regina had a number of publications in marine biology. 

## Description

Current version (development continues) of Puerta del Mar Ecosystem Engine is a representation of a very basic marine ecosystem written in Python and visualised in Processing.py. It's consist of few species including Plankton - creatures growing and reproducing from solar power, basically plants; Herbivores -  species eating only Plankton; two kinds of Carnivores - species eating both Herbivores and other kind of Carnivores but not Plankton. This is a first approximation but in future we looking for developing an algorithm of species development capable to generate new species without the need to categorise them previously. Environment includes a Sun giving a power for Plankton and changing a Temperature of a Water. There is a Day/Night cycle, according to it water temperature is changing and all species migrating. The migration is happening due to binding to Niches - each of the ecosystem habitants have it's own Comfort Temperature and so depth or Niche. Each individual have parameters like: Mass, Energy, Max energy tolerated, Health, Health loss rate, Regeneration rate, Absorption rate, Hardness, Internal clock, Size etc. The interaction and actions includes: Wondering - basically no action, just moving somewhere; Deciding; Attacking; Escaping; Eating; Looking for partner for reproduction; Reproducing. Also there is clusters of genes of a phenotype: Mass, Energy, Energy Loss rate, Health, Regeneration rate, Speed, Acceleration, SightRange, Feeding Power, Comfortable Temperature (range), Socialisation. The last one is more abstract gene and, for example it might affect the decision between cooperation or selfish action. In general cooperation is very common in real life, as well as in our engine: species can form gangs to feed, attack or defend. In next versions will be implemented SuperSpecies - a big number of species might unite to form a one big and powerful individual. As an alternative there could be scenario when a fish gang start a tornado around enemy or around prey to attack or protect itself. Such a behaviours will be possible with implementing hormones and advanced instincts. Now there is a basic usage of instincts - Eat, Escape, Reproduce. 

# Tech Documentation (now and next)

## Elements and Organisms


### Plankton
Plankton is storing energy to reproduce, regenerate and move (slowly). The cost of mithosis is rather small. If energy is going below zero it starts loosing health. When energy is full the plankton starts to increase its mass. As soon as mass reaches 2, the plankton divides. Absortion rate could be directly related to the size,

<u>DNA</u>mass, energy, energy loss rate, health, regeneration rate, absorbtion rate, hardness.

<u>Properties</u>

*   Mass
*   Energy
*   Regeneration rate
*   Absobrtion rate
*   Hardness
*   Max energy tolerated
*   Internal clock

<u>Methods</u>

*   _(Instant)_ Metabolism
*   _(Instant)_ Photosynthesis: Transform sunlight into energy
*   Reproduce: creates another plancton with the same DNA
*   EATEN (?)
*   EVALUATE (?) (learning)
*   Further implementation
*   Search for sunlight function - IF in the last movement was more sunlight than now, (store the sunlight value of the last position and compare it to the current one) then go in that direction again, IF NOT, continue to move randomly
*   Implement move function (slow random movement)
*   Limit the photosynthesis to +-90% of sunlight. That is, IF sunlight power is below 90%, then you can't do photosynthesis.

### Herbivores

Herbivores eat plankton to get energy. They lay eggs to reproduce. They are _R strategas_ (see below). If energy is going below zero it starts loosing health. They will tend to scape from the Carnivors, their natural predators. When they are in danger, their _comfort zone_ reduces in order to be more close to each other.

<u>DNA</u>mass, energy, energy loss rate, health, regeneration rate, speed, acceleration, sightRange, sight angle, feeding power (teeth sharpness?), comfortable temperature (range), socialisation (or confort zone radius)
<u>Properties</u>

*   Max energy tolerated
*   Critical age of reproduction [mix, max]  -- [Maturity, Ageing]
*   Determined by Maturity (min) and Aging (max) 
*   Critical energy of reproduction
*   Reproduction energy rate cost 
*   Range of energy being hungry  
*   Rate of genes compatibility for successful reproduction
*   Fitness
*   Cruise speed
*   Maximum speed

<u>Methods</u>

*   Metabolism
*   Detect
*   Wander
*   Flock
*   Eat
*   Escape
*   Reproduce
*   Die
*   Evaluate

### Carnivores I and II

Carnivores eat Herbivores and other Carnivores to get energy. They give birth to few number of offspring (usually 1). They are _K strategies_ (see below). If energy is going below zero it starts loosing health. 

<u>DNA</u>mass, energy, energy loss rate, health, regeneration rate, speed, acceleration, sightRange, sight angle, comfortable temperature range

<u>Properties</u>

*   Max energy tolerated
*   Critical age of reproduction
*   Critical energy of reproduction
*   Reproduction energy rate cost
*   Initial and final time of predation
*   Rate of genes compatibility for successful reproduction
*   Max energy tolerated
*   Fitness 
*   Metabolism
*   Energy waste

<u>Methods</u>

*   Metabolism
*   Detect
*   Wander
*   Flock
*   Eat
*   Escape
*   Reproduce
*   Die
*   Evaluate
*   Attack

## DNA

*   Each gene is determined by a string of 8 letters length [AABBCCDD]. 
*   A and B define the maximum value and C and D the minimum (max / 8, min / 8)
*   A function counts the amount of times each letter appears in the string
*   A function divides the numerical value assigned to each letter between 8, then multiply the result by the amount of times each letter appears in the string
*   After that, sum all the results to get the final value (fenotype) of the creature

### EXAMPLE

This DNA string determines, for instance, the SIZE of the species  [AABCDCBA]

*   The max. value of SIZE is 20
*   The min. value of SIZE is 5
*   So, A and B = 20

A function divides this values between 8 (size of the string). So, we get the relative value of each letter of the string 

*   (max value) 20 / 8 = 2,5                 -- so each A and B of the string will be 2,5
*   (min value)    5 / 8 = 0,625             -- so each A and B of the string will be 0,625

We take the DNA string [AABCDCBA]

A function counts the ammount of times each letter appears in the string:

*   3A, 2B, 2C, 1D

A function multiplies the number of times each letter appears in the string by its relative value. So:

*   3A = 3 x 2,5 = 7,5
*   2B = 2 x 2,5 = 5
*   2C = 2 x 0,625 = 1,25
*   D = 1 x 0,625 = 0,625

We sum all the values...

*   7,5 + 5 + 1,25 + 0.625 = 14,375

14,375 will be the final value of the size of the creature

## Hardy-Weinberg Principle

States that [genotype frequencies](http://en.wikipedia.org/wiki/Genotype_frequencies) in a population will remain constant from generation to generation in the absence of other evolutionary influences. 

**Abstract DNA Class for living creatures (related to all current creatures):**

*   Mass
*   Energy
*   Energy loss rate
*   Health
*   Regeneration rate per second
*   Speed
*   Acceleration

## Energy-related properties

**Maturity**: Threshold that determines that an organism has reached its full development -- its able to reproduce. A **R strategy** will reach Maturity at** 5** seconds, and a **K stratega** at **20** seconds

**Aging**: Threshold that determines the age at which an organism starts to loose efficiency - its not able to reproduce anymore. And **R stratega** will begin Aging at 15 seconds, and K stratega at 80 seconds

**Energy Absortion Rate (int or float):** Determined by age --> maturity and aging. 

*   Factor de eficiencia dependiente de la edad (fe). Así, p.ej, para la alimentación la energía que se obtiene E(t+1) = fe*E(t).
*   From birth to the maturity, the organism is highly efficient: Value equals to 100% or 1
*   When reaches maturity, is normal: Value equals 80%, or 0.8
*   When it begins the aging process, starts to loose 1% of Energy Absortion Rate per second until a limit of 10%

**Full Energy Capacity: **Determined by age --> maturity and aging. 

*   From birth to the maturity, the organism begins with 1/2 of its full energy capacity, and grows over time.
*   When reaches maturity, the energy capacity reaches its full potential -- the real value determined by the genes --
*   When it begins the aging process, its max energy capacity begins to shrink over time, until a limit of 1/2

**Reproduction energy rate cost**: Amount of energy wasted in reproduction functions. Determined by the type of the species, and the sex:

*   Plankton (by mithosis): 20% of the total energy
*   R strategas: 35% of the total energy
*   K strategas: 60% of the total energy

**Max energy tolerated** - Constrain the maximum energy to the Energy value determined by DNA. (Your body cannot store more than that amount of Energy)

**Critical energy of reproduction** - Amount of energy needed to reproduce (usually 100%) - **FURTHER _-_** We will introduce a Hormone that will control the firing of reproduction function. The chances that this Hormone fires the reproduction will increase with the amount of energy of the organism. (For instance:

*   Energy at 50% - Chances of search for reproduction at 10% 
*   Energy at 100% - Chances of search for reproduction at 90% )

**Range of energy being hungry** - Threshold of energy that determines when the organism starts looking for food (for instance 45%) 

## Environmental properties

*   Sunlight/Heat - Primary energy input of the system. This define: Layers 
*   Bounding box - Defines the limits of the environment
*   Inner clock
*   Night / Day cycle - Regulates the ammount of sunlight available at each timestep.
*   (Further) Oxygen

## Behaviour Rules 

### Life Strategies:

**R** estrategas - Short lifecycle, lots of species, lots of breeding

**K** estrategas - Long lifecycle, small amount of species, small of breeding

### Altruism VS Egoism

Cooperation and Conflict - In our upcoming flocking system, we will have three rulesalignment, cohesion, and separation. Alignment and Cohesion will ask the elements to _cooperate_i.e. work together to stay together and move together. Separation, however, will ask the elements to _compete_ for space.

The radius of each of this 3 functions should be different...
*   Separation Radius Detection
*   Allignment Radius Detection
*   Cohesion Radius Detection 

### Confrontation

This function will describe the mechanism that the species use to decide between attack or escape in any given conflict.

Combat Points : [(Force x Mass) / 2] x [Experience x (Energy/10)]

## Reproduction Rules

*   <u>Plancton </u>- Mithosis: It splits in two creatures, with the same DNA with probability of mutation
*   <u>Herbívoros</u> - Sexual (R), more than 3 to 50 individuals per Successful Reproduction
*   <u>Carnívoros </u>- Sexual (K), only 1 individual per Successful Reproduction

## Energy Absortion Rates (Digestive system)

Herbivores 

*   <u>Plants </u>- The energy absortion is 100%
*   <u>Animals </u>- The energy absortion is 95% (In real life, they have no problem digesting meat. The problem is that the meat usually belongs to a stronger animal. Given cases of plants scarcity, some herbivors can eat meat -we are talking about eating corpses of other animals, not hunting them down-)

Carnivores

*   <u>Plants </u>- The energy absortion is 1% (Carnivors can eat plants, but they organism don't assimilate/digest well the nutrients)
*   <u>Animals </u>- The energy absortion is 100%

## General Rules

*   If energy reaches 0, then loose health
*   If health reaches 0, then die
*   No reproduction if the genes are not compatible enough

