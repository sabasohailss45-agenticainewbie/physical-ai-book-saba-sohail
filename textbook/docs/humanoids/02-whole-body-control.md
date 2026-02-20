---
sidebar_position: 2
title: Whole-Body Control & Loco-Manipulation
---

# Whole-Body Control & Loco-Manipulation

A humanoid robot that can walk and a humanoid robot that can manipulate objects are two very different systems. Combining both — walking while carrying a tray, opening a door while stepping through it — requires **whole-body control**: a unified framework that plans motions for all joints simultaneously, respecting physical constraints and balancing competing objectives.

---

## The Loco-Manipulation Problem

**Locomotion** (walking, running, climbing) and **manipulation** (grasping, inserting, assembling) have traditionally been separate research areas. Humanoid robots force their unification.

### Why They Couple

When a humanoid moves its arm, its **centre of mass (CoM)** shifts. This changes the ground reaction forces required to maintain balance. Ignoring this coupling causes:
- Falls during reaching for heavy objects
- Unstable postures when carrying asymmetric loads
- Failure to coordinate footsteps with arm trajectories on stairs

Loco-manipulation requires a **single planner** that simultaneously considers:
- The robot's balance
- The arm's trajectory to the target
- The ground contact forces
- The joint torque limits across all joints

---

## Contact-Rich Manipulation

Most useful manipulation tasks involve **contact**: the robot's hand contacts an object, which contacts a surface, which contacts the floor. Managing these contacts correctly is crucial.

### Unilateral Contact Constraints

Contact forces can only push, never pull (unless using suction). This is captured by:

```
fₙ ≥ 0  (normal force must be non-negative)
```

A robot's foot cannot pull the floor towards it. A gripper finger cannot pull a surface unless it has a suction cup.

### Friction Cone

For a contact not to slip, the tangential force must stay within the friction cone:

```
√(fx² + fy²) ≤ μ · fₙ
```

Where μ is the coefficient of friction and fₙ is the normal force. This is a cone in 3D force space — hence "friction cone".

Linearising the friction cone to a pyramid (4–8 faces) makes it compatible with linear/quadratic programming.

---

## Task Hierarchy and Prioritised QP

### The Task Stack

A humanoid performing a task typically has multiple simultaneous objectives. These are ordered by priority:

| Priority | Task | Why |
|----------|------|-----|
| 1 (highest) | Balance / CoM regulation | If this fails, everything fails |
| 2 | Joint limit avoidance | Prevents self-damage |
| 3 | End-effector tracking | Actual manipulation goal |
| 4 | Posture reference | Keeps robot in natural configuration |
| 5 | Gaze direction | Visual tracking of task |

### Null-Space Projection

For a set of tasks with Jacobians J₁, J₂, …, the null-space projector ensures lower-priority tasks do not interfere with higher-priority ones:

```
N₁ = I − J₁† · J₁          (null space of task 1)
N₂ = N₁ · (I − (J₂·N₁)† · (J₂·N₁))   (null space of tasks 1 and 2)
```

The combined velocity command:
```
q̇* = J₁† · ẋ₁* + N₁ · J₂† · ẋ₂* + N₂ · J₃† · ẋ₃* + ...
```

Each task is executed in the null space of all higher-priority tasks.

### QP Formulation

Modern WBC formulates all tasks and constraints as a **Quadratic Program**:

```
min_{q̈, f_contact}  Σᵢ wᵢ ||Jᵢ q̈ + J̇ᵢ q̇ − ẍᵢ*||²

Subject to:
  M(q)q̈ + h(q,q̇) = τ + Jc^T · f_contact    (equations of motion)
  fₙ ≥ 0                                      (unilateral contact)
  ||fₜ||₂ ≤ μ fₙ                              (friction cone)
  τmin ≤ τ ≤ τmax                             (torque limits)
  qmin ≤ q ≤ qmax                             (joint limits)
```

Solved at 1 kHz using efficient QP solvers (OSQP, qpOASES, ECOS).

---

## Footstep Planning and Balance

### Zero Moment Point (ZMP)

The **ZMP** (Vukobratovic & Borovac, 2004) is the point on the ground where the net ground reaction moment about horizontal axes is zero. For a dynamically stable biped:

```
ZMP must remain inside the support polygon
```

The **support polygon** is the convex hull of all contact points with the ground. During single support (one foot on ground), it is the foot outline. During double support, it is the convex hull of both feet.

### 3D Linear Inverted Pendulum Model (LIPM)

The full humanoid dynamics can be approximately reduced to a point mass (the CoM) on a massless telescoping leg — the **3D LIPM**:

```
ẍ_CoM = (g/z_CoM) · (x_CoM − x_ZMP)
```

This linear model enables **preview control**: plan CoM trajectory over multiple future steps.

### Capture Point and DCM

The **Divergent Component of Motion (DCM)** (also called "capture point") is the point where the robot must step to recover from a push without falling:

```
DCM = x_CoM + ẋ_CoM / ω₀    where ω₀ = √(g/z_CoM)
```

If the DCM exits the support polygon and you don't step, you fall. This gives a **reactive stepping criterion**: step when DCM approaches the support polygon boundary.

### Push Recovery Strategies

| Strategy | When Used |
|----------|-----------|
| Ankle strategy | Small pushes; shift CoM by ankle torque |
| Hip strategy | Medium pushes; bend at hip to shift CoM quickly |
| Stepping strategy | Large pushes; take a step to re-establish support |
| Multi-step recovery | Very large disturbances; multiple rapid steps |

---

## Case Study: Humanoid Robot Climbing Stairs While Carrying a Tray

1. **Vision** detects staircase geometry and tray position
2. **Footstep planner** selects foothold positions on each stair riser, constrained by friction and robot kinematic reachability
3. **WBC** simultaneously:
   - Tracks the CoM above the support polygon as feet lift and land
   - Maintains the tray in a horizontal orientation (torso + arm task)
   - Controls gaze toward the next stair
4. **Reactive controller** adjusts footstep timing and position when IMU detects unexpected disturbances

The key insight: arms, torso, and legs are **not controlled independently**. Every joint is part of a single optimisation that balances all objectives simultaneously.

---

## Summary

- **Loco-manipulation** requires treating locomotion and manipulation as a single coupled planning problem.
- **Contact constraints** (unilateral normal forces, friction cones) must be explicitly respected.
- **Prioritised QP** enables a task hierarchy: balance first, manipulation second, posture third.
- **ZMP and DCM** provide criteria for dynamic stability — a humanoid is stable if and only if the ZMP stays inside the support polygon.
- **Push recovery** is not a special mode — it is the same WBC framework responding to larger disturbances.

> **Key Takeaway**: Whole-body control is the reason a humanoid can wave goodbye while walking backwards without falling. It's not magic — it's a well-structured optimisation problem solved 1000 times per second.
