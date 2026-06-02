# DriveLM Dataset Analysis

## Overview

This project analyzes the DriveLM and NuScenes-mini datasets to understand the characteristics of autonomous driving question-answering data and to support the development of a multimodal Retrieval-Augmented Generation (RAG) system.

The analysis focuses on:

* Question distributions
* Object category frequencies
* Object status analysis
* NuScenes metadata exploration
* Ego vehicle trajectory analysis
* Dataset biases and limitations

---

# Dataset Structure

## DriveLM

DriveLM provides:

* Question-answer pairs
* Reasoning chains
* Scene descriptions
* Object references
* Image references

## NuScenes-mini

NuScenes-mini provides:

* Multi-camera driving images
* Ego vehicle poses
* Scene metadata
* Temporal information
* Sensor data references

---

# Parsing and Structuring

A custom parser was implemented to:

* Parse DriveLM JSON files
* Extract question-answer pairs
* Associate scene descriptions
* Link object metadata
* Link image paths
* Create a structured representation for retrieval

Each parsed sample contains:

* Question
* Answer
* Scene description
* Image paths
* Object metadata

---

# DriveLM Dataset Analysis

## Dataset Statistics

| Metric        | Value |
| ------------- | ----- |
| Total Samples | 790   |

---

## Question Type Distribution

| Question Type | Count |
| ------------- | ----- |
| What          | 501   |
| Are           | 113   |
| Is            | 88    |
| Other         | 88    |

### Observation

The majority of questions focus on scene understanding, object identification, and driving-context reasoning.

Examples:

* What vehicles are ahead?
* Is the traffic light green?
* What objects are to the left?

---

## Object Category Distribution

| Category        | Count |
| --------------- | ----- |
| Vehicle         | 2373  |
| Traffic Element | 779   |

### Observation

Vehicle-related reasoning dominates the dataset, indicating a strong emphasis on traffic participant understanding.

---

## Object Status Distribution

| Status     | Count |
| ---------- | ----- |
| Moving     | 2218  |
| Stationary | 155   |

### Observation

Moving objects are significantly more common than stationary objects, reflecting the dynamic nature of autonomous driving environments.

---

# Patterns and Observations

## Observed Patterns

* Vehicle-related questions dominate the dataset.
* Most questions focus on objects relative to the ego vehicle.
* Traffic-light and road-object reasoning frequently appear.
* Dynamic traffic scenarios are more common than static scenes.

## Potential Biases

* Rare-event scenarios are underrepresented.
* Stationary-object reasoning appears less frequently.
* Pedestrian-heavy scenes are less common than vehicle-heavy scenes.
* Urban driving environments dominate the dataset.

---

# NuScenes Metadata Analysis

## Dataset Statistics

| Metric                    | Value  |
| ------------------------- | ------ |
| Total Samples             | 404    |
| Total Sample Data Records | 31,206 |
| Total Ego Poses           | 31,206 |
| Total Scenes              | 10     |

---

## Timestamp Analysis

| Metric             | Value            |
| ------------------ | ---------------- |
| Earliest Timestamp | 1532402927604844 |
| Latest Timestamp   | 1542801007452232 |

### Observation

The dataset spans multiple driving sessions and contains rich temporal information useful for autonomous driving analysis.

---

## Ego Vehicle Position Analysis

| Metric               | Value   |
| -------------------- | ------- |
| Minimum X Coordinate | 309.17  |
| Maximum X Coordinate | 1935.51 |
| Minimum Y Coordinate | 658.64  |
| Maximum Y Coordinate | 2667.09 |

### Observation

The ego vehicle traverses a large spatial region across multiple driving environments.

---

## Scene Distribution

The NuScenes-mini split contains the following driving scenes:

* scene-0061
* scene-0103
* scene-0553
* scene-0655
* scene-0757
* scene-0796
* scene-0916
* scene-1077
* scene-1094
* scene-1100

### Observation

The dataset covers multiple urban driving environments and traffic situations suitable for autonomous driving question-answering tasks.

---

## Trajectory Analysis

| Metric                      | Value  |
| --------------------------- | ------ |
| Total Ego Vehicle Positions | 31,206 |

### Observation

The large number of ego poses provides continuous vehicle trajectory information that can be leveraged for future motion reasoning, velocity estimation, and driving-state retrieval.

---

# Generated Visualizations

The following visualizations were generated:

* question_distribution.png
* object_distribution.png
* ego_trajectory.png

These visualizations provide insight into:

* Question distribution
* Object frequency
* Driving-scene composition
* Ego vehicle movement patterns

---

# Challenges Encountered

* Parsing nested DriveLM JSON structures
* Mapping DriveLM image references to NuScenes-mini
* Handling missing image paths due to dataset mismatch
* CPU-intensive embedding generation
* Docker environment setup and dependency management

---

# Key Findings

1. Vehicle-centric reasoning dominates the dataset.
2. Moving objects significantly outnumber stationary objects.
3. The dataset contains rich spatial and temporal metadata.
4. Multiple urban driving scenarios are represented.
5. DriveLM and NuScenes-mini do not fully overlap, requiring fallback image handling.
6. Future retrieval systems can leverage ego-state, trajectory, and timestamp metadata for improved reasoning.

---

# Conclusion

The analysis provides a comprehensive understanding of the DriveLM and NuScenes-mini datasets, including question distributions, object frequencies, scene characteristics, temporal coverage, and ego vehicle trajectories. These insights were used to guide the design and implementation of the multimodal RAG pipeline for autonomous driving question answering.
