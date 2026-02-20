---
sidebar_position: 2
title: Kinematics & Dynamics
---

# Kinematics & Dynamics

Before a robot can move intelligently, we must understand the mathematical relationship between its joint angles and the position of its end-effector in space. **Kinematics** describes this relationship geometrically. **Dynamics** adds the forces and torques that cause motion. Together, they form the mathematical foundation on which every robot controller is built.

---

## Kinematics: Position Without Forces

Kinematics asks: "Given a configuration (joint angles), where is each part of the robot?"

### Forward Kinematics (FK)

**Forward kinematics** computes the end-effector pose (position + orientation) from joint angles:

```
FK: joint angles θ → end-effector pose T (4×4 transformation matrix)
```

A 6-DOF serial manipulator (like a standard robot arm) has 6 joints. The end-effector pose is the product of 6 transformation matrices, one per joint:

```
T_0_6 = T_0_1 · T_1_2 · T_2_3 · T_3_4 · T_4_5 · T_5_6
```

Each `T_i_{i+1}` is a 4×4 homogeneous transformation matrix encoding rotation and translation.

### Denavit-Hartenberg (DH) Parameters

The **DH convention** provides a systematic method to define each joint's transformation using just 4 parameters:

| Parameter | Symbol | Meaning |
|-----------|--------|---------|
| Link length | a | Distance along x-axis from old z to new z |
| Link twist | α | Angle about x-axis from old z to new z |
| Joint offset | d | Distance along z-axis from old x to new x |
| Joint angle | θ | Angle about z-axis from old x to new x |

**DH transformation matrix**:
```
T_i = Rot_z(θ) · Trans_z(d) · Trans_x(a) · Rot_x(α)
```

The DH table for a 6-DOF robot arm has 6 rows, one per joint. Computing FK is then a straightforward matrix multiplication.

---

### Inverse Kinematics (IK)

**Inverse kinematics** is the reverse problem: given a desired end-effector pose, find the joint angles:

```
IK: end-effector pose T → joint angles θ
```

This is significantly harder than FK:
- **Multiple solutions**: a 6-DOF arm typically has up to 16 analytical solutions for a given target pose
- **No solution**: the target may be outside the robot's workspace
- **Singularities**: certain configurations have infinitely many solutions (at singularities) or lose directions of motion

#### Analytical IK

For robots with special geometry (e.g., three consecutive joints whose axes intersect at a point — "spherical wrist"), **closed-form** analytical solutions exist. These are fast (microseconds) and return all solutions.

#### Numerical IK

For general robots or when the target is near a singularity, use **iterative numerical methods**:

```python
# Pseudocode for Jacobian pseudoinverse IK
θ = θ_initial
for iteration in range(max_iter):
    T = forward_kinematics(θ)
    error = compute_pose_error(T_target, T)  # 6-vector: [Δx, Δy, Δz, Δroll, Δpitch, Δyaw]
    if norm(error) < tolerance:
        return θ
    J = compute_jacobian(θ)
    J_pseudo = pinv(J)  # Moore-Penrose pseudoinverse
    dθ = J_pseudo @ error * step_size
    θ = θ + dθ
```

---

## The Jacobian Matrix

The **Jacobian** J is the core tool of robot kinematics. It is a 6×n matrix (for a 6-DOF end-effector and n joints) that maps joint velocities to end-effector velocities:

```
ẋ = J(θ) · θ̇
```

Where:
- `ẋ` is the 6-vector end-effector velocity [vx, vy, vz, ωx, ωy, ωz]
- `θ̇` is the n-vector of joint velocities
- `J(θ)` depends on the current configuration

### Singularities

A **singularity** occurs when `J` loses rank — its columns become linearly dependent. At a singularity:
- Some end-effector motions become impossible (the robot "gets stuck")
- The pseudoinverse explodes → unrealistically large joint velocities

**Types of singularity**:
- **Boundary singularity**: arm fully extended or folded — at edge of workspace
- **Interior singularity**: arm aligned in a way that loses a direction of motion

**Avoiding singularities**: use damped least squares IK (replace `J⁺` with `Jᵀ(JJᵀ + λ²I)⁻¹`), which trades end-effector accuracy near singularities for bounded joint velocities.

---

## Workspace Analysis

| Workspace Type | Definition |
|----------------|-----------|
| Reachable | All positions the end-effector can reach in any orientation |
| Dexterous | All positions the end-effector can reach in **every** orientation |
| Manipulability | Measure of how far a configuration is from a singularity |

The **dexterous workspace** is always a subset of the reachable workspace. For a 6-DOF robot with a spherical wrist, the dexterous workspace is an annular region centred on the base.

---

## Dynamics: Forces Cause Motion

Kinematics ignores mass, inertia, and forces. **Dynamics** adds them:

```
M(q)·q̈ + C(q,q̇)·q̇ + G(q) = τ
```

Where:
- `q` = joint positions (n-vector)
- `q̈` = joint accelerations
- `M(q)` = mass matrix (n×n, positive definite) — inertia at each joint
- `C(q,q̇)` = Coriolis/centrifugal matrix — coupling between joint velocities
- `G(q)` = gravity vector — torque needed to hold against gravity
- `τ` = applied joint torques

### Newton-Euler Equations

For computing joint torques from a desired motion (Inverse Dynamics), the **Newton-Euler** recursive algorithm is efficient:

1. **Forward pass** (base to tip): propagate velocities and accelerations
2. **Backward pass** (tip to base): propagate forces and torques

This runs in O(n) — linear in the number of joints.

### Lagrangian Mechanics

The **Lagrangian** L = T − V (kinetic minus potential energy). The equations of motion follow from:

```
d/dt(∂L/∂q̇) − ∂L/∂q = τ
```

This yields the same equation `M·q̈ + C·q̇ + G = τ` but makes the physical structure explicit.

---

## Applications

### Pick-and-Place Robot Arm

A 6-DOF industrial arm (e.g., UR5) uses:
1. **FK** to verify the current gripper position
2. **IK** to find joint angles for the target grasp pose
3. **Inverse dynamics** to compute the torques needed to follow a smooth trajectory
4. **Jacobian** for Cartesian velocity control during approach

### Humanoid Arm Reaching

A humanoid arm reaches for an object on a table:
1. Vision detects object pose (from Chapter 3)
2. IK computes arm configuration to reach the object
3. Dynamics ensures the movement doesn't violate torque limits or destabilise the robot's balance (this requires whole-body control — Chapter 8)

---

## Summary

- **Forward kinematics**: joint angles → end-effector pose. Always has a solution; computed via DH matrix products.
- **Inverse kinematics**: end-effector pose → joint angles. May have 0, 1, or multiple solutions; singularities are the key challenge.
- **The Jacobian** maps joint velocities to end-effector velocities — the workhorse of velocity control and IK.
- **Dynamics equation**: M·q̈ + C·q̇ + G = τ — the equation that connects motion to forces.
- Newton-Euler recursion computes inverse dynamics in O(n).

> **Key Takeaway**: Kinematics tells you where the robot can go. Dynamics tells you how hard it has to work to get there.
