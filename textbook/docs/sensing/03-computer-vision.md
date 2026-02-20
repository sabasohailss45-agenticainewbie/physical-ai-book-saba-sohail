---
sidebar_position: 3
title: Computer Vision for Robotics
---

# Computer Vision for Robotics

A humanoid robot navigating a home must identify a coffee mug on a cluttered counter, estimate its exact 3D position and orientation, and grasp it without knocking over the neighbouring glass. Each step — detection, pose estimation, grasp planning — relies on computer vision. This chapter covers the core vision algorithms that power modern robotic manipulation and navigation.

---

## Object Detection

**Object detection** answers: "What objects are in this image, and where are they (bounding box)?"

### Two-Stage Detectors (Faster R-CNN)
1. **Region Proposal Network (RPN)**: scans the feature map; proposes ~2000 candidate regions
2. **Classification head**: classifies each proposal and refines its bounding box

Advantage: high accuracy. Disadvantage: slow (~7 fps on consumer GPU).

### Single-Stage Detectors (YOLO Family)
YOLO (You Only Look Once) divides the image into a grid; each cell predicts bounding boxes and class probabilities in a single forward pass.

**YOLO v8** (Ultralytics, 2023) achieves ~50 mAP on COCO at 80–160 fps on a mid-range GPU — fast enough for real-time robotics.

**DETR** (DEtection TRansformer, Facebook 2020): uses a transformer encoder-decoder with learned object queries. No anchors, no NMS post-processing. Sets new accuracy standards but slower than YOLO for the same accuracy.

### Robotics Considerations
- **Latency budget**: a robot controller running at 100 Hz has 10 ms per cycle. A 5 ms detector leaves 5 ms for everything else.
- **Domain shift**: a detector trained on ImageNet may fail on your robot's camera angle, lighting, and object set. Fine-tune on in-distribution data.
- **Embedded deployment**: models must run on edge hardware (Nvidia Jetson, Hailo-8). Use quantisation (INT8) and pruning to fit within power/memory budgets.

---

## Instance Segmentation

**Instance segmentation** extends detection: rather than a bounding box, it produces a per-pixel mask for each object instance.

**Mask R-CNN** (He et al., 2017): adds a mask prediction branch to Faster R-CNN. Each detected object gets a binary mask.

**SAM — Segment Anything Model** (Meta, 2023): a foundation model that segments any object from a point, bounding box, or text prompt. Zero-shot capability: no fine-tuning needed for new object categories.

**Robotics use**: grasping from clutter — segment the target object precisely so the robot's grasp planner knows the exact object shape, not just a bounding box approximation.

---

## 6-DOF Pose Estimation

For a robot to grasp an object, it needs not just "where is the mug" but the full 6-DOF pose: **(x, y, z, roll, pitch, yaw)** — position and orientation in 3D.

### PnP (Perspective-n-Point)
Given N known 3D points on an object and their 2D projections in an image, PnP solves for the camera-to-object transformation. Used when object geometry is known (CAD model available).

### FoundationPose (NVIDIA, 2024)
A state-of-the-art 6-DOF pose estimator that requires only a CAD model or a few reference images. Uses a rendering-and-refinement loop:
1. Generate pose hypotheses from depth + colour
2. Render synthetic views at hypothesised poses
3. Refine by maximising correspondence between rendered and real

Achieves &lt;5 mm / &lt;5° accuracy on the YCB-Video benchmark.

### Textureless Objects
Many industrial parts (metal brackets, white cups) have no texture — traditional feature matching fails. Solutions:
- **EdgePose**: matches 3D model edges to detected image edges
- **SymmetryAware**: handle rotationally symmetric objects (cylinders, bolts)
- **Depth-only**: use RANSAC plane + shape fitting on point cloud

---

## Optical Flow

**Optical flow** estimates the per-pixel 2D motion field between consecutive frames — how each pixel has moved.

**Lucas-Kanade (LK)**: assumes constant flow within small windows; computes flow at sparse feature points (Harris corners). Fast; used for visual odometry.

**Farneback**: computes dense (every pixel) flow using polynomial expansion. Slower but provides a complete motion field.

**RAFT** (2020): neural network that produces state-of-the-art dense optical flow using a recurrent lookup mechanism. Used in robot video understanding and motion segmentation.

**Robotics applications**:
- **Ego-motion estimation**: compute camera velocity from flow field
- **Moving object detection**: pixels with flow inconsistent with ego-motion belong to independently moving objects
- **Tactile flow**: apply optical flow to GelSight images to detect and quantify slip

---

## Dataset Pipelines for Robot Training

Training robust vision models requires **large, diverse, annotated datasets** — expensive to collect in the real world. Modern pipelines use synthetic data heavily.

### Photo-Realistic Simulation
**Nvidia Isaac Sim** and **Blender** render physically accurate scenes with:
- Randomised lighting (hue, intensity, position)
- Randomised object textures and poses
- Randomised camera parameters (FOV, noise, blur)

Automatic annotation: every pixel, every bounding box, every 6-DOF pose is known by construction.

### Domain Randomisation
Vary simulation parameters so widely that the real world appears as "just another variant":
- Object textures: solid colours, random images, real textures
- Lighting: point lights, area lights, HDRI environment maps
- Physics: mass, friction, restitution randomised ±50%
- Sensor noise: Gaussian noise added to RGB + depth images

### Real-to-Sim Adaptation (RealDreamer, UniSim)
Instead of randomising the simulation, reconstruct a digital twin of the real deployment environment using NeRF or Gaussian Splatting. Train on this high-fidelity replica.

### Foundation Vision Models as Backbones

Rather than training from scratch, robot vision systems increasingly use **pre-trained foundation models** as feature extractors:

| Model | Organisation | Key Strength |
|-------|-------------|-------------|
| CLIP | OpenAI (2021) | Image–text alignment; zero-shot classification |
| DINOv2 | Meta (2023) | Dense spatial features; excellent for segmentation backbones |
| SAM | Meta (2023) | Zero-shot segmentation from prompts |
| OpenVocab detectors | Various | Detect novel categories by text description |

---

## Summary

- **Object detection**: YOLO v8 for real-time; Faster R-CNN / DETR for highest accuracy.
- **Instance segmentation**: Mask R-CNN for classic; SAM for foundation-model zero-shot.
- **6-DOF pose estimation**: FoundationPose is state-of-the-art; PnP for simple known objects.
- **Optical flow**: Lucas-Kanade for sparse tracking; RAFT for dense neural flow.
- **Dataset strategy**: synthetic data + domain randomisation reduces the cost of labelled real data by 10–100×.
- Foundation models (CLIP, DINOv2) eliminate most from-scratch training for perception backbones.

> **Key Takeaway**: Modern robot vision is a combination of task-specific networks (YOLO, FoundationPose) and foundation models (CLIP, SAM) — neither alone is sufficient.
