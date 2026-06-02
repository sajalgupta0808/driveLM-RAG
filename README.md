# DriveLM Multimodal RAG System for Autonomous Driving Question Answering

## Overview

This project implements a **Multimodal Retrieval-Augmented Generation (RAG) pipeline** for autonomous driving question answering using the **DriveLM** and **NuScenes-mini** datasets.

The system retrieves relevant driving context from structured driving data and generates natural language answers using an open-source Large Language Model (LLM). The project also includes dataset analysis, evaluation, visualization, and a lightweight fine-tuning pipeline using LoRA.

---

# Dataset

## DriveLM

DriveLM provides:

* Driving-related questions
* Reasoning chains
* Ground-truth answers
* References to driving scenes

## NuScenes-mini

NuScenes-mini provides:

* Multi-camera images
* Ego vehicle poses
* Scene metadata
* Sample annotations
* Temporal driving information

---

# Part 1: Data Analysis & Preparation

## Dataset Statistics

### DriveLM

| Metric        | Value |
| ------------- | ----- |
| Total Samples | 790   |

### Question Type Distribution

| Question Type | Count |
| ------------- | ----- |
| What          | 501   |
| Are           | 113   |
| Is            | 88    |
| Other         | 88    |

### Object Category Distribution

| Category        | Count |
| --------------- | ----- |
| Vehicle         | 2373  |
| Traffic Element | 779   |

### Object Status Distribution

| Status     | Count |
| ---------- | ----- |
| Moving     | 2218  |
| Stationary | 155   |

---

## Key Observations

### Dataset Bias

The dataset is heavily biased toward:

* Vehicle-centric questions
* Dynamic driving scenarios
* Moving object reasoning

Moving objects appear significantly more frequently than stationary objects.

### Implications

This bias influences retrieval quality and may improve performance on motion-related questions while reducing performance on rare or stationary-object questions.

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

Observation:

The dataset spans multiple driving sessions and contains rich temporal information useful for autonomous driving analysis.

---

## Ego Vehicle Position Analysis

| Metric               | Value   |
| -------------------- | ------- |
| Minimum X Coordinate | 309.17  |
| Maximum X Coordinate | 1935.51 |
| Minimum Y Coordinate | 658.64  |
| Maximum Y Coordinate | 2667.09 |

Observation:

The ego vehicle traverses a large spatial region across multiple driving environments.

---

## Scene Distribution

The NuScenes-mini split contains 10 scenes:

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

---

## Trajectory Analysis

Total Ego Vehicle Positions:

31,206

Observation:

The dataset contains sufficient trajectory information for future motion-aware retrieval and driving-state reasoning.

---

## Generated Visualizations

The following visualizations are generated:

* question_distribution.png
* object_distribution.png
* ego_trajectory.png

---

# Part 2: RAG Pipeline

## Architecture

```text
User Question
      │
      ▼
MiniLM Embeddings
      │
      ▼
FAISS Retrieval
      │
      ▼
Retrieved Driving Context
      │
      ├──────────────┐
      ▼              ▼
 TinyLlama       SigLIP
      │              │
      ▼              ▼
Generated      Image-Question
 Answer         Similarity Score
```

---

## Model Selection

### Embedding Model

Model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Reasoning:

* Lightweight
* Fast inference
* Strong semantic retrieval performance
* Suitable for CPU-based execution

---

### Language Model

Model:

TinyLlama/TinyLlama-1.1B-Chat-v1.0

Reasoning:

* Lightweight and open-source
* Runs locally on CPU/MPS devices
* Suitable for retrieval-augmented generation
* Fast inference for autonomous driving QA

### Vision-Language Model

Model:

google/siglip-base-patch16-224

Reasoning:

* State-of-the-art image-text alignment model
* Strong visual grounding capabilities
* Lightweight enough for local execution
* Used to measure image-question semantic relevance
* Improves multimodal retrieval validation

## Final Models Used

### Embedding Model

sentence-transformers/all-MiniLM-L6-v2

### Language Model

TinyLlama/TinyLlama-1.1B-Chat-v1.0

### Vision-Language Model

google/siglip-base-patch16-224

### Vector Database

FAISS
## Retrieval Layer

The retrieval pipeline performs:

1. Dataset parsing
2. Document creation
3. Embedding generation
4. FAISS indexing
5. Semantic similarity search

Retrieved context includes:

* Questions
* Answers
* Image references
* Driving scene information

---

## Multimodal Support

The system supports:

* Text retrieval
* Camera image retrieval
* Multi-camera scene visualization
* SigLIP-based image-question alignment
* Multimodal visual grounding

Supported cameras:

* CAM_FRONT
* CAM_FRONT_LEFT
* CAM_FRONT_RIGHT
* CAM_BACK
* CAM_BACK_LEFT
* CAM_BACK_RIGHT

---

## Fine-Tuning Extension

A LoRA-based fine-tuning pipeline is included.

Features:

* DriveLM data loader
* PEFT integration
* LoRA configuration
* Instruction tuning workflow

This pipeline serves as a foundation for future task-specific adaptation.

---

# Part 3: Evaluation and Visualization

## Evaluation Metrics

### Exact Match (EM)

Measures exact correspondence between prediction and ground-truth answer.

### Semantic Similarity

Measures semantic alignment between prediction and ground truth using sentence embeddings.

---

## Evaluation Results

| Metric                      | Score  |
| --------------------------- | ------ |
| Exact Match Accuracy        | 20.00% |
| Average Semantic Similarity | 0.7827 |

---

## Streamlit Visualization Tool

The project includes a Streamlit-based interface that displays:

* User question
* Generated answer
* Top retrieved contexts
* Retrieved camera views
* SigLIP image-question similarity score
* Visual grounding information

---

# Failure Analysis

## Retrieval Mismatch

Some failures occur because semantically similar but incorrect contexts are retrieved.

---

## Dataset Overlap Limitation

DriveLM references the full NuScenes dataset, while this project uses NuScenes-mini.

As a result:

* Some image paths are unavailable locally
* Fallback image visualization is used when necessary

---

## Limited Visual Reasoning

## Limited Visual Reasoning

The current system performs lightweight multimodal grounding using SigLIP image-text similarity.

Limitations:

* Visual information is used for relevance validation rather than direct answer generation.
* Full multimodal reasoning could be achieved using larger VLMs such as LLaVA or Qwen-VL.

---

## Long-Tail Question Types

Rare question categories appear less frequently in training data and tend to produce lower retrieval quality.

---

# Future Improvements

Potential enhancements include:

* Full NuScenes integration
* Velocity-aware retrieval
* Ego-state retrieval
* Trajectory-aware reasoning
* Hybrid metadata retrieval
* Cross-modal reranking
* End-to-end multimodal RAG using LLaVA or Qwen-VL
* Image-aware answer generation
---

# Running the Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Dataset Analysis

```bash
python -m app.analysis.data_analysis
```

---

## Run NuScenes Analysis

```bash
python -m app.analysis.nuscenes_analysis
```

---

## Run Evaluation

```bash
python -m app.evaluation.evaluate
```

---

## Launch Streamlit Demo

```bash
streamlit run streamlit_app.py
```

---

# Docker

Build the Docker image:

```bash
docker build -t drivelm-rag .
```

Run the container:

```bash
docker run -p 8501:8501 drivelm-rag
```

---

# Project Structure

```text
drivelm-rag/

├── app/
│   ├── analysis/
│   ├── evaluation/
│   ├── retrieval/
│   ├── models/
│   ├── training/
│   └── utils/
│
├── data/
│
├── outputs/
│
├── DATA_ANALYSIS.md
├── README.md
├── Dockerfile
├── requirements.txt
├── streamlit_app.py
```

---

# Conclusion

This project implements a multimodal Retrieval-Augmented Generation (RAG) pipeline for autonomous driving question answering using DriveLM and NuScenes-mini.

The system combines:

* Semantic retrieval using FAISS and MiniLM
* Answer generation using TinyLlama
* Visual grounding using SigLIP
* Multi-camera scene visualization
* Dataset analysis and evaluation
* NuScenes metadata exploration
* Trajectory analysis and visualization

The implementation includes end-to-end retrieval, multimodal grounding, evaluation, Dockerized deployment, and an interactive Streamlit interface while remaining lightweight enough to run locally on consumer hardware.