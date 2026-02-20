---
sidebar_position: 3
title: Control Theory for Robots
---

# Control Theory for Robots

A robot that knows where to go but cannot reliably get there is useless. **Control theory** is the discipline that makes robots actually do what they're asked — accurately, smoothly, and robustly in the face of disturbances. This chapter progresses from the humble PID controller (which powers most industrial robots) through model-predictive control (which enables constraint-aware planning) to reinforcement learning (which is transforming legged locomotion).

---

## PID Control: The Foundation

**PID** (Proportional-Integral-Derivative) is the workhorse of industrial control. It is simple, tunable without a model, and surprisingly effective. An estimated 90% of industrial control loops use some form of PID.

### Intuition via Analogy: Cruise Control

Imagine driving a car with cruise control set to 100 km/h:
- **Proportional (P)**: the harder you're away from 100, the harder you press the accelerator. Large error → large correction.
- **Integral (I)**: if you've been consistently below 100 for a while (e.g., headwind), gradually add more throttle until the steady error disappears.
- **Derivative (D)**: if you're approaching 100 quickly, ease off before you overshoot. Anticipates the future based on the rate of change.

### The PID Equation

```
u(t) = Kₚ·e(t) + Kᵢ·∫e(τ)dτ + Kd·(de/dt)
```

In discrete time (for a computer running at frequency f = 1/Δt):

```python
class PIDController:
    def __init__(self, Kp, Ki, Kd, dt):
        self.Kp, self.Ki, self.Kd, self.dt = Kp, Ki, Kd, dt
        self.integral = 0.0
        self.prev_error = 0.0

    def step(self, setpoint, measurement):
        error = setpoint - measurement
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        self.prev_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative
```

### PID Tuning: Ziegler-Nichols

1. Set Kᵢ = Kd = 0. Increase Kₚ until the output oscillates steadily → record Kc (critical gain) and Tc (oscillation period).
2. Set: Kₚ = 0.6·Kc, Kᵢ = 2Kₚ/Tc, Kd = KₚTc/8

Modern practice uses autotuning software (MATLAB, Python control library).

### PID Limitations

- **Assumes linear system**: robot dynamics are highly nonlinear; PID must be re-tuned at different operating points
- **No constraint handling**: PID cannot respect joint limits, torque limits, or collision avoidance
- **No predictive ability**: reacts to errors after they occur; cannot anticipate upcoming terrain changes

---

## Model-Predictive Control (MPC)

**MPC** solves an online optimisation problem at each timestep, planning ahead over a finite horizon:

```
Minimise:  Σₖ [ ||xₖ − x*ₖ||²_Q + ||uₖ||²_R ]  (tracking + control effort)

Subject to:
  xₖ₊₁ = f(xₖ, uₖ)        (dynamics model)
  xmin ≤ xₖ ≤ xmax         (state constraints: joint limits)
  umin ≤ uₖ ≤ umax         (input constraints: torque limits)
  g(xₖ, uₖ) ≤ 0           (collision avoidance, etc.)
```

Only the first control input u₀ is applied; at the next timestep, the horizon shifts and the problem is re-solved. This **receding horizon** approach provides feedback robustness.

### Why MPC for Legged Robots?

1. **Constraint handling**: joint torque limits, ground contact constraints (friction cone), and impact timing can all be encoded explicitly
2. **Multi-step prediction**: a quadruped approaching a step can plan its footsteps several strides ahead
3. **Natural integration of physics**: the robot's dynamics model is built into the optimisation

**Convex MPC for legged locomotion** (Di Carlo et al., 2018): linearise the contact model and dynamics; solve a quadratic program (QP) at 40 Hz. Used in MIT Cheetah and many subsequent systems.

---

## Whole-Body Control (WBC)

A humanoid robot performing a reaching task while standing must:
- Maintain balance (highest priority)
- Track a desired centre-of-mass height
- Move the hand to the target
- Keep the head looking forward

These tasks conflict (moving the arm shifts the centre of mass). **Whole-Body Control** (Sentis & Khatib, 2005) resolves conflicts through a **task hierarchy** using null-space projection.

### Prioritised Null-Space Projection

For each task i (ordered by priority), compute the joint velocity that achieves task i while living in the null space of all higher-priority tasks:

```
q̇* = q̇*_i-1 + N_i · (J_i†_bar · (ẋ*_i - J_i · q̇*_i-1))
```

where `N_i` is the null-space projector of all tasks 1…i−1, and `J_i†_bar` is a dynamically consistent pseudoinverse.

This ensures that tasks are fulfilled in strict priority order — balance is never sacrificed for arm tracking.

### QP-Based WBC

Modern WBC formulates the control problem as a **Quadratic Program** (QP) — solved in ~1 ms using efficient solvers (OSQP, qpOASES). This allows contact constraints, torque limits, and task objectives to be handled in a unified, principled framework.

---

## Reinforcement Learning for Locomotion

While MPC and WBC require explicit models, **Reinforcement Learning (RL)** learns control policies directly from interaction.

### MDP Formulation

| Component | Robot Locomotion Definition |
|-----------|----------------------------|
| State s | Joint positions, velocities, IMU data (orientation, angular velocity), foot contact flags |
| Action a | Joint position targets or torques (n-dimensional) |
| Reward r | +forward velocity − energy penalty − fall penalty − joint limit violation |
| Episode end | Robot falls; time limit reached |

### PPO (Proximal Policy Optimisation)

PPO is the dominant RL algorithm for locomotion:
1. Collect rollouts in simulation using current policy π
2. Compute advantages (how much better than baseline was each action)
3. Update policy: maximise surrogate objective with a clipping constraint that prevents large policy updates

**Training**: 10,000+ parallel simulation environments; 1–5 days on a GPU cluster; produces a neural network (typically 2–3 layer MLP) that directly maps state → action.

### Sim-to-Real Transfer

Policies trained in simulation often fail in the real world due to the **reality gap**. Standard mitigations:

**Domain Randomisation**:
```
On each episode reset:
  mass += uniform(-30%, +30%)
  motor_strength += uniform(-20%, +20%)
  friction_coeff += uniform(-40%, +40%)
  joint_damping += uniform(-50%, +50%)
  sensor_noise = add Gaussian noise to observations
```

**Actuator Delay Modelling**: add simulated communication and actuation delay to match real hardware.

**Real-world fine-tuning**: brief fine-tuning on the real robot using safe, conservative exploration.

### State-of-the-Art Results

| System | Achievement | Method |
|--------|-------------|--------|
| ETH ANYmal | Parkour over obstacles, stairs, gaps | Deep RL + sim-to-real |
| Berkeley Humanoid | Dynamic locomotion from RL | PPO + domain randomisation |
| Unitree H1 | 3.3 m/s running (humanoid speed record) | RL locomotion |
| MIT Cheetah 3 | Blind stair climbing | MPC + perception |

---

## Summary

- **PID**: Simple, tunable, works for linear systems. Foundation of industrial robotics.
- **MPC**: Handles constraints and plans ahead. Essential for contact-rich locomotion.
- **WBC**: Manages conflicting tasks in a priority hierarchy. Required for whole-body humanoid motion.
- **RL**: Learns from interaction; handles complex contact dynamics automatically; requires sim-to-real for deployment.
- Modern high-performance robots combine these: RL-trained locomotion + MPC stepping + WBC for arm use.

> **Key Takeaway**: PID to move a joint. MPC to walk on terrain. WBC to use your arms while walking. RL to learn all of this without writing the equations.
