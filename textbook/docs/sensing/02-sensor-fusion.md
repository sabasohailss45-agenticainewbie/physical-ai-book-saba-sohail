---
sidebar_position: 2
title: Sensor Fusion & SLAM
---

# Sensor Fusion & SLAM

No single sensor is perfect. Cameras lose tracking in the dark; LiDAR struggles in heavy rain; IMUs drift without correction. **Sensor fusion** is the discipline of combining multiple imperfect measurements to produce a better estimate of the robot's state and its environment than any single sensor could provide.

At its most ambitious, sensor fusion enables **SLAM** — Simultaneous Localisation And Mapping — where the robot builds a map of an unknown environment while simultaneously figuring out where it is within that map.

---

## Why Fusion?

Consider a humanoid walking through a corridor:
- **IMU** tells it approximately how far it has moved and how it is oriented — but drifts after a few seconds
- **Camera** provides rich texture and can detect landmarks — but fails in darkness or motion blur
- **LiDAR** gives precise geometry — but has no colour and is blind to transparent surfaces

Each sensor answers a different part of the state estimation problem. Fusion answers all of them together.

---

## The Kalman Filter: A Framework for Uncertainty

The **Kalman Filter** (Rudolf Kálmán, 1960) is the canonical framework for fusing noisy measurements. It models the robot's state as a **Gaussian belief** — a mean estimate plus a covariance matrix representing uncertainty.

### Two Steps

**Predict (Motion Update)**:
Use the robot's motion model (e.g., from IMU) to propagate the state forward:
- Mean: `x̂ = F·x̂ + B·u`
- Covariance: `P = F·P·Fᵀ + Q`

Where F is the state transition matrix, B is the control matrix, u is the control input, and Q is the process noise covariance.

**Update (Measurement Update)**:
When a sensor measurement z arrives:
1. Compute the Kalman gain: `K = P·Hᵀ·(H·P·Hᵀ + R)⁻¹`
2. Update mean: `x̂ = x̂ + K·(z − H·x̂)`
3. Update covariance: `P = (I − K·H)·P`

Where H maps the state to the measurement space, and R is the measurement noise covariance.

**Intuition**: High Kalman gain (K ≈ 1) means "trust the measurement more". Low gain means "trust the prediction more". The filter automatically adjusts based on the relative uncertainty of prediction vs. measurement.

---

## Extended Kalman Filter (EKF)

The standard Kalman Filter assumes **linear** motion and measurement models. Real robots are nonlinear — rotating and translating simultaneously produces nonlinear kinematics.

The **Extended Kalman Filter (EKF)** handles nonlinearity by linearising around the current estimate using the **Jacobian matrix**:
- `F` is replaced by `∂f/∂x` (Jacobian of the motion model)
- `H` is replaced by `∂h/∂x` (Jacobian of the measurement model)

This linearisation is an approximation — it breaks down for highly nonlinear systems or when uncertainty is large.

---

## Particle Filter

When the probability distribution over states is **non-Gaussian** (e.g., a robot that is genuinely uncertain which of three corridors it is in), the Kalman Filter fails.

The **particle filter** represents the state distribution as a set of N weighted particles `(x_i, w_i)`. Each particle is a hypothesis about the current state.

**Algorithm** (simplified):
```
For each particle i:
  1. Propagate: x_i_new = motion_model(x_i, u) + noise
  2. Weight: w_i = p(z | x_i_new)  // how well does measurement z match particle state?
3. Normalise weights
4. Resample: draw N particles from distribution defined by weights
```

Particles cluster around high-probability states. The particle filter naturally handles multimodal distributions and non-Gaussian noise.

**Cost**: O(N) per step — more accurate requires more particles, which is computationally expensive.

---

## SLAM: Simultaneous Localisation and Mapping

A robot entering an unknown building faces the "chicken-and-egg" problem:
- To localise, you need a map
- To build a map, you need to know your location

SLAM solves both problems simultaneously. The state vector includes both the robot pose and the positions of all detected landmarks.

### EKF-SLAM

**State vector**: `[robot pose | landmark₁ position | landmark₂ position | ... | landmarkₙ position]`

As the robot moves and detects landmarks, the covariance matrix grows. **Critical property**: once two landmarks are jointly observed, their joint uncertainty **decreases** even if neither is individually certain. This is the power of SLAM.

**Limitation**: state vector grows quadratically with number of landmarks; covariance update is O(n²). Expensive for large maps.

### Particle-SLAM (FastSLAM)

Decomposes the SLAM problem: each particle represents a robot trajectory hypothesis, and each particle maintains its own independent landmark map. This enables efficient O(N log M) updates.

### Visual-Inertial Odometry (VIO)

Modern humanoids and drones typically use **VIO**: tight fusion of camera and IMU.

- **IMU**: fast (400–1000 Hz), measures acceleration and rotation, drifts over time
- **Camera**: slower (30–60 Hz), provides absolute geometric constraints, fails during fast motion

**Tight coupling** — processing both in a single estimator — outperforms loose coupling (running separately and combining outputs). Systems like **VINS-Mono** (HKUST) and **ORB-SLAM3** implement state-of-the-art VIO.

---

## Applications

| Application | Fusion Strategy | Why |
|-------------|----------------|-----|
| Robot vacuum (Roomba i7+) | Particle filter SLAM (camera) | Low cost; indoor use |
| Autonomous vehicle (Waymo) | LiDAR SLAM + EKF (GPS + IMU) | High accuracy; outdoor |
| Humanoid indoor navigation | VIO (camera + IMU) | Compact; no GPS |
| Mars rover (Perseverance) | Stereo visual odometry + IMU | No GPS on Mars |
| Drone race | VIO + EKF | Low weight; agile motion |

---

## Summary

- **Sensor fusion** combines multiple noisy measurements to produce better state estimates.
- The **Kalman Filter** is the foundation: predict with motion model, update with measurements.
- **EKF** extends this to nonlinear systems via Jacobian linearisation.
- **Particle filters** handle non-Gaussian, multimodal distributions.
- **SLAM** solves localisation and mapping jointly — the cornerstone of autonomous robot navigation.
- **VIO** (camera + IMU fusion) is the preferred approach for indoor humanoid and drone navigation.

> **Key Takeaway**: A robot without sensor fusion is always flying blind. With fusion, it can navigate a building it has never seen before.
