---
sidebar_position: 1
title: Actuator Technologies
---

# Actuator Technologies

An actuator converts energy into motion. For a robot, the choice of actuator type determines almost everything else: how strong it is, how safe it is near humans, how efficiently it uses energy, and how precisely it can be controlled. This chapter surveys the major actuator technologies used in modern robots, from traditional hydraulics to the cutting-edge quasi-direct drive motors that power the latest humanoids.

---

## The Actuator Design Space

Robot actuators must balance competing requirements:

| Requirement | Importance |
|-------------|-----------|
| Torque/force density | High — robots need to carry loads |
| Speed | High — tasks require human-like movement speed |
| Backdrivability | High — safety near humans requires compliance |
| Energy efficiency | High — battery-powered robots need long runtimes |
| Precision | High — manipulation requires sub-millimetre accuracy |
| Cost | High — commercial robots must be affordable |

No actuator excels at all of these simultaneously. Understanding the trade-offs is the first step to intelligent robot design.

---

## Electric Actuators

### DC Motors

A DC motor converts electrical current to rotational torque via the Lorentz force on current-carrying conductors in a magnetic field. Torque is proportional to current: `τ = Kₜ·I`.

**Brushed DC motors**: simple, cheap, but brushes wear out. Suitable for low-cost, non-critical applications.

**Brushless DC (BLDC) motors**: commutation is electronic; no wear, higher efficiency (85–95%), higher power density. Standard in modern robots.

### Servo Motors

A servo motor is a BLDC + encoder + gearbox + motor driver, packaged together. Servos are the workhorse of robot joints because they combine high torque (from the gearbox) with precise position control (from the encoder).

**Common gearbox types**:
- **Spur / planetary gear**: efficient, but backlash degrades position accuracy
- **Harmonic drive**: zero backlash, very high reduction (50:1–160:1) in compact package; expensive; not backdrivable
- **Cycloidal drive**: high reduction, compact, somewhat backdrivable; used in HEBI modules

**Key metric — gear ratio**: A 100:1 reduction amplifies torque by 100× but reduces speed by 100× and inertia by 10,000×. High gear ratios make joints stiffer and less backdrivable — a force applied to the output barely moves the motor shaft.

---

## Hydraulic Actuators

Hydraulic actuators use pressurised fluid (typically oil) to generate force. Pascal's Law: pressure applied to a fluid transmits equally in all directions. A cylinder with a large piston area produces very large force from moderate pressure.

**Advantages**:
- Extremely high force density (5–10× electric for the same weight)
- Natural compliance from oil compressibility
- Tolerates brief overloads without damage

**Disadvantages**:
- Complex plumbing; risk of leaks
- Hydraulic pump is loud and heavy
- Lower efficiency than electric (60–80%)
- Fluid must be kept clean and at correct temperature

**Humanoid use**: original Boston Dynamics Atlas (2013–2023) used hydraulics precisely because its acrobatic tasks required force densities that contemporary electric motors could not match. The 2024 Atlas replaced hydraulics with electric QDD actuators, indicating electric technology has caught up.

---

## Pneumatic Actuators

Pneumatic actuators use compressed air to generate force or movement. McKibben muscles (braided pneumatic actuators) contract when pressurised — like human muscles.

**Advantages**:
- Inherently compliant (air is compressible)
- Very safe for human contact — soft robots can be squeezed without damage
- Lightweight

**Disadvantages**:
- Low force density compared to hydraulics and electric
- Requires compressed air supply (pump or tank)
- Difficult to control precisely (spongy response)

**Robotics use**: soft grippers for food handling (delicate produce); wearable rehabilitation devices; research into compliant manipulation.

---

## Cable-Driven and Tendon Actuators

Motors are located proximal (at the body) and transmit force to distal joints (fingers, feet) via cables or tendons.

**Advantages**:
- Moves motor mass away from distal joints → reduced inertia at fingers/toes → faster, more agile motion
- Natural compliance from cable elasticity

**Shadow Dexterous Hand**: 24 DOF, fully actuated by air muscles via tendons. Demonstrates human-like dexterity in research settings.

**Disadvantages**:
- Cable routing is complex; maintenance intensive
- Friction and elasticity complicate precision control

---

## Quasi-Direct Drive (QDD) — The Modern Standard

**Quasi-Direct Drive (QDD)** uses a low gear ratio (1:1 to 9:1), high-torque electric motor. The result:

| Property | High Gear Ratio | QDD (Low Ratio) |
|----------|----------------|-----------------|
| Torque at output | High | Moderate |
| Backdrivability | None/low | **High** |
| Impact robustness | Poor (gears break) | **Good** |
| Force transparency | Low | **High** |
| Speed | Low | High |

**MIT Cheetah, Mini Cheetah**: pioneered QDD for legged robots. Key result: MIT Cheetah backflips and runs at 3 m/s using QDD joints — feats impossible with high-gear-ratio motors.

**Boston Dynamics Atlas (2024)**, **Tesla Optimus**: both use QDD or custom electric actuators. QDD is now the standard for high-performance humanoids.

**Why backdrivability matters for humanoids**:
- Safe human contact: if someone pushes the robot, the joints yield rather than breaking or injuring
- Force estimation: back-calculate contact forces from motor current without dedicated F/T sensors
- Energy recovery: during downhill walking, backdrivable motors can regenerate energy

---

## Series Elastic Actuators (SEA)

A **Series Elastic Actuator** places a compliant spring element in series between the motor/gearbox and the output link.

**Invented at MIT (Jerry Pratt, 1995)**; used in Agility Robotics' Digit, Boston Dynamics' earlier robots.

**Advantages**:
- Spring deflection is measurable → accurate force control without external F/T sensor
- Spring absorbs shocks → protects gearbox from impact damage
- Natural compliance → safe human interaction

**Disadvantage**: Adds compliance (springiness) that makes precise position control harder. Trade-off between force control quality and position control bandwidth.

---

## Actuator Comparison Summary

| Type | Force Density | Backdrivable | Compliance | Cost | Example |
|------|-------------|-------------|------------|------|---------|
| BLDC + harmonic drive | High | No | Low | Medium | HEBI, Dynamixel |
| Hydraulic | Very High | Moderate | Moderate | High | Atlas Gen 1 |
| Pneumatic (McKibben) | Low | Yes | Very High | Low | Soft grippers |
| QDD (low gear) | Medium | **Yes** | Low-medium | Medium–High | MIT Cheetah, Atlas 2024 |
| SEA | Medium | Yes | **High** | Medium–High | Agility Digit |
| Cable-driven | Medium | Moderate | Moderate | Medium | Shadow Hand |

---

## Summary

- Electric actuators dominate modern robots due to cleanliness, efficiency, and controllability.
- **QDD** is the current standard for high-performance legged robots and humanoids — backdrivability is non-negotiable for safe human interaction.
- **SEA** provides superior force control at the cost of position bandwidth — ideal for arms that interact with humans.
- Hydraulics remain relevant only for extreme force density requirements; the gap is closing fast.
- **Compliance** — whether from SEA springs, QDD backdrivability, or pneumatic softness — is a first-class safety feature, not an afterthought.

> **Key Takeaway**: The actuator defines the robot's "character" — its strength, its grace, its safety. Choose it as carefully as you choose the AI algorithm.
