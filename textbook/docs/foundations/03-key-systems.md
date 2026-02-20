---
sidebar_position: 3
title: Key Humanoid Systems
---

# Key Humanoid Systems

A new generation of humanoid robots has emerged since 2020, transitioning from research prototypes to commercially-targeted platforms. This chapter surveys the most significant systems, their design choices, and the principles governing their safe deployment.

---

## Why Survey Specific Robots?

Every humanoid robot represents a set of **engineering trade-offs** made concrete. Reading about degrees of freedom and actuator types in the abstract is less instructive than seeing how real teams resolved real constraints. Each system below embodies a different philosophy about what matters most.

---

## Platform Comparison

| Platform | Organisation | DOF | Weight | Actuator Type | Primary Use | Status (2024) |
|----------|-------------|-----|--------|---------------|-------------|----------------|
| Atlas (electric) | Boston Dynamics | 28 | 89 kg | Electric, custom QDD | Research / demonstration | Active R&D |
| Spot | Boston Dynamics | 12 (legs) | 32 kg | Electric BLDC | Inspection, security | Commercial |
| Optimus Gen 2 | Tesla | 28 | 57 kg | Linear electric | Factory automation | Limited pilot |
| Figure 01 | Figure AI | 44 | 70 kg | Electric | Industrial logistics | Pilot at BMW |
| Digit | Agility Robotics | 21 | 65 kg | Electric SEA | Warehouse logistics | Commercial |
| TALOS | PAL Robotics | 32 | 95 kg | Electric, harmonic drive | Research | Commercial R&D |

---

## Boston Dynamics Atlas

Atlas is the most technically capable humanoid robot publicly demonstrated as of 2024. Originally hydraulic (2013), Boston Dynamics redesigned Atlas with an all-electric drivetrain in 2024.

**Key innovations**:
- **Custom QDD actuators**: Low gear ratio, high torque density, backdrivable. Enables dynamic manipulation — Atlas can pick up a heavy tool bag and throw it to a worker on an upper level.
- **Whole-body control**: Atlas plans movements that simultaneously use legs, torso, and arms, solving a single optimisation problem rather than separate modules.
- **360° mobility**: Unlike most humanoids, Atlas can move through unusual postures — squatting, crawling, rotating its torso beyond human range.

**Demonstrated tasks** (2024): Pick up a tool bag (5 kg), rotate and toss it upward to a human worker; walk across a construction site; recover from being pushed.

---

## Tesla Optimus Gen 2

Optimus is designed with a fundamentally different priority from Atlas: **cost and manufacturability** at scale.

**Key design choices**:
- **28 DOF with linear actuators**: Simpler manufacturing than custom rotary joints; easier to replace in a factory setting.
- **Hands**: 11 DOF per hand, 22 N·m torque, tactile sensing on fingertips. Capable of handling eggs without breaking them (demonstrated 2023).
- **Training approach**: Imitation learning from human demonstrations (operators wear motion-capture suits; robot imitates their movements). Significantly reduces the need for hand-engineered control policies.
- **Vertical integration**: Tesla manufactures the battery, motors, and compute chip (FSD chip adapted for robotics) in-house.

**Target use case**: Replace humans in repetitive, ergonomically harmful factory tasks — lifting, sorting, carrying. Tesla's Fremont factory is the initial deployment site.

---

## Agility Robotics Digit

Digit is the first humanoid robot in commercial volume production (partnership with Amazon, 2023).

**Design philosophy**: Digit is explicitly designed for **one task category** — moving totes (plastic storage bins) in warehouse environments. This focus enables significant simplification:
- 21 DOF vs 28–44 for research humanoids
- No neck, no facial features, minimal sensors beyond what's needed for navigation and manipulation
- Series Elastic Actuators: spring-in-series enables safe force control without expensive torque sensors

**Deployment**: Amazon pilots in fulfillment centers; robot lifts totes from conveyor to rack and back. Human workers handle exception cases.

---

## Figure 01

Figure AI's Figure 01 is a well-funded startup's attempt to build a general-purpose humanoid from the ground up with a focus on commercial viability.

**Notable**: BMW partnership for manufacturing tasks (2024). Figure demonstrated a robot making a coffee using an espresso machine — a manipulation task requiring precise grasping, pouring, and lid placement.

**AI approach**: OpenAI partnership to use large vision-language-action models for task understanding and planning.

---

## Safety Principles

As humanoids move from research labs to factories and homes, safety standards become critical.

### ISO 10218-1/2 (Industrial Robot Safety)
- Defines speed and force limits for robots operating near humans
- Requires risk assessments for every collaborative workspace
- Mandates emergency stop mechanisms with sub-100 ms response time

### ISO/TS 15066 (Collaborative Robots)
Adds specific limits for **power and force limiting** (PFL) mode:
- Maximum contact force: 140 N (transient), 70 N (quasi-static) for most body regions
- Maximum speed: varies by robot mass and contact location

### What Makes a Humanoid "Ready"?

A deployment-ready humanoid must demonstrate:
1. **Reliable locomotion** over the deployment environment (flat floors, ramps, thresholds)
2. **Manipulation success rate** >95% on target tasks under normal conditions
3. **Graceful failure**: when the robot cannot complete a task, it stops safely and requests human assistance rather than damaging itself or the environment
4. **Safe human interaction**: compliant behaviour when contacted; immediate response to emergency stop

---

## Summary

- Humanoid robots span a wide design space: from Atlas's acrobatic capability to Digit's focused warehouse utility.
- Key differentiators: **DOF count, actuator type, training methodology, and target use case**.
- Safety standards (ISO 10218, ISO/TS 15066) provide the regulatory framework for deployment near humans.
- The commercial race is on: Figure, Tesla, and Agility are deploying — not just demonstrating.

> **Key Takeaway**: The "best" humanoid depends entirely on the use case. A robot that can do a backflip is not necessarily the right choice for a warehouse.
