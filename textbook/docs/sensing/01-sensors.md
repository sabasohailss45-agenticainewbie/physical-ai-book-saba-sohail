---
sidebar_position: 1
title: Sensor Modalities for Robotics
---

# Sensor Modalities for Robotics

A robot without sensors is blind, deaf, and numb. Sensors are the interface between the robot's computational brain and the physical world. Choosing the right sensor — or combination of sensors — is one of the most consequential design decisions in Physical AI.

This chapter surveys the major sensor modalities used in modern robots, from the cameras that give humanoids their "eyes" to the tactile arrays that let them feel a grape without crushing it.

---

## Overview of Sensor Modalities

| Modality | Measurement | Range | Cost | Key Challenge |
|----------|-------------|-------|------|---------------|
| RGB Camera | Colour + intensity (2D) | 0.1 m – ∞ | Low | No depth; lighting sensitivity |
| Depth Camera | Per-pixel depth (2.5D) | 0.2 – 10 m | Low–medium | Outdoor sunlight noise |
| LiDAR | 3D point cloud | 0.1 – 200 m | Medium–high | No colour; rain/dust degradation |
| IMU | Linear acceleration + angular velocity | N/A | Very low | Integration drift |
| Force/Torque Sensor | 6-axis wrench | N/A | High | Noise; bandwidth |
| Tactile Array | Contact distribution | Contact only | High | Fragility; wiring |

---

## RGB Cameras

A standard RGB camera captures a 2D image: width × height pixels, each with R, G, B colour channels. Modern robotics cameras offer:

- **Resolution**: 720p to 4K. More pixels ≠ better robot performance; latency and processing cost scale with resolution.
- **Frame rate**: 30–120 fps. High frame rates reduce motion blur for fast-moving robots.
- **Field of view**: Typically 60–120°. Wide-angle lenses increase situational awareness but distort distances.
- **Shutter type**:
  - *Rolling shutter*: rows exposed sequentially; causes "jello effect" during vibration. Common in consumer cameras.
  - *Global shutter*: all pixels exposed simultaneously; essential for fast robot motion. More expensive.

**Robotics use**: object detection and recognition, visual odometry, manipulation target localisation, person tracking.

**Key limitation**: RGB cameras provide no depth information. A 2D image cannot directly tell you how far away an object is — this must be inferred by stereo correspondence, motion parallax, or a separate depth sensor.

---

## Depth Cameras

Depth cameras add a third dimension — a per-pixel distance estimate — to the 2D image.

### Technologies

**Structured light** (e.g., Intel RealSense D415, original Microsoft Kinect):
- Projects a known infrared pattern onto the scene
- Observes the distortion of the pattern to infer depth
- Range: 0.2–10 m; accuracy: ±2% at 2 m
- Weakness: fails in bright sunlight (infrared noise)

**Stereo** (e.g., ZED Camera, RealSense D435):
- Two RGB cameras at a known baseline; compute disparity to get depth
- Works outdoors; longer range than structured light
- Weakness: fails on textureless surfaces (no features to match)

**Time-of-Flight (ToF)** (e.g., Microsoft Azure Kinect, Sony DepthSense):
- Emits modulated infrared light; measures round-trip time to infer distance
- Very fast per-pixel depth (~60 fps); compact
- Weakness: multipath interference; flying pixel artefacts at edges

---

## LiDAR

LiDAR (Light Detection And Ranging) fires laser pulses and measures return time to build a precise 3D point cloud of the environment.

### Types

**Spinning LiDAR** (e.g., Velodyne VLP-16, HDL-64E):
- Rotates a set of laser/detector pairs (16–128 channels) at 10–20 Hz
- Generates a full 360° 3D point cloud ~10 times per second
- Range: 100–200 m; accuracy: ±2 cm
- Used in: autonomous vehicles (Waymo, Cruise), robot navigation

**Solid-state LiDAR** (e.g., Ouster OS1, Livox Mid-360):
- No rotating parts; uses MEMS or OPA steering
- More compact, lower cost, higher reliability
- Used in: indoor robots, drones, next-gen autonomous vehicles

### LiDAR vs Camera

| Property | LiDAR | Camera |
|----------|-------|--------|
| 3D geometry | Direct, precise | Inferred |
| Colour/texture | None | Rich |
| Performance in dark | Excellent | Poor |
| Performance in fog/rain | Degraded | Degraded |
| Cost | $500–$10,000 | $10–$500 |
| Data rate | ~1 M points/sec | ~30 MB/frame |

---

## Inertial Measurement Units (IMUs)

An IMU combines a 3-axis accelerometer (measures specific force) and a 3-axis gyroscope (measures angular velocity) in a single chip. Most modern IMUs also include a 3-axis magnetometer (compass).

**Use in robots**:
- Bipedal balance: IMU measures trunk tilt; controller corrects to stay upright
- Visual-Inertial Odometry (VIO): fuse IMU with camera to estimate robot pose
- Vibration detection: detect foot contact impacts; estimate ground contact timing

**Key challenge — drift**: Integrating gyroscope data once gives orientation (angle); integrating accelerometer data twice gives position. Each integration step accumulates noise. A cheap MEMS IMU drifts several degrees/minute without correction from another sensor.

---

## Force/Torque Sensors

A 6-axis Force/Torque (F/T) sensor measures the full wrench vector: Fx, Fy, Fz, Mx, My, Mz at a single point. Typically mounted at a robot's wrist or ankle.

**Applications**:
- **Compliant manipulation**: detect when a peg is misaligned during insertion; use force feedback to guide it in
- **Grasp quality**: verify a grip is secure before moving
- **Bipedal balance**: foot F/T sensors tell the controller exactly what force the ground is exerting

**Joint torque sensing**: Modern humanoids (Agility Digit, MIT Cheetah) embed torque sensors in each joint. This enables full dynamic state estimation without external sensors.

---

## Tactile Arrays

Tactile sensors measure distributed contact — like an artificial skin.

**BioTac** (SynTouch): A fluid-filled rubber fingertip with 24 electrodes measuring pressure distribution, vibration (texture), and temperature. Used in research manipulation.

**GelSight** (MIT): A camera behind a transparent elastomer. When the elastomer deforms on contact, the camera images the deformation and a neural network reconstructs the 3D contact geometry. Extremely fine detail (~0.1 mm resolution).

**Applications**:
- Detecting slip: when a grasped object starts to slip, the tactile signal changes before the object falls — triggering a grip-tightening reflex
- Texture identification: distinguish silk from sandpaper by contact feel
- Insertion tasks: guide a USB plug into a port without visual feedback

---

## Sensor Selection in Practice: Humanoid Hands

A humanoid hand illustrates the trade-off between sensor capability and cost/complexity:

| Scenario | Sensors Used |
|----------|-------------|
| Picking a water bottle | Wrist F/T + fingertip pressure |
| Threading a needle | High-res GelSight + fine motor control |
| Identifying objects by touch | BioTac + learned classifier |
| Navigation in a warehouse | LiDAR + IMU |
| Face-to-face interaction | RGB cameras + depth cameras |

---

## Summary

- Each sensor modality has distinct strengths, weaknesses, and cost profiles.
- **No single sensor is sufficient** for a general-purpose humanoid — sensor fusion is mandatory.
- Camera + depth for manipulation; LiDAR + IMU for navigation; F/T + tactile for dexterous handling.
- Design principle: match sensor capability to the task's real requirements, not to the most impressive spec sheet.

> **Key Takeaway**: The best sensor for a robot is the cheapest one that can reliably provide the information the controller actually needs.
