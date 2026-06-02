# Evaluation & Failure Analysis

# Overview

The DriveLM-RAG pipeline was evaluated on a subset of validation samples from the DriveLM dataset.

The evaluation focused on:

* Retrieval quality
* Answer generation quality
* Semantic correctness
* Context relevance

The goal was to assess how effectively the system retrieves relevant driving information and generates accurate responses for autonomous driving question-answering tasks.

---

# Evaluation Metrics

## Exact Match Accuracy (EM)

Exact Match measures whether the generated answer exactly matches the ground-truth answer.

This metric is useful for:

* Factual question answering
* Short autonomous-driving responses
* Object-state questions
* Binary (Yes/No) reasoning

### Limitation

Exact Match is a strict metric and may underestimate performance when generated answers are semantically correct but phrased differently from the ground-truth answer.

---

## Semantic Similarity

Semantic Similarity was measured using SentenceTransformer embeddings and cosine similarity.

This metric evaluates:

* Semantic closeness
* Meaning preservation
* Contextual correctness

even when exact wording differs.

Semantic Similarity provides a more flexible assessment of answer quality for natural language generation tasks.

---

# Quantitative Results

| Metric                      | Score  |
| --------------------------- | ------ |
| Exact Match Accuracy        | 20.00% |
| Average Semantic Similarity | 0.7827 |

---

# Qualitative Analysis

## Strengths

The retrieval pipeline successfully retrieves semantically relevant driving scenes and contextual information.

The system performs well on:

* Object presence questions
* Vehicle state questions
* Traffic-element identification
* Basic scene understanding
* Motion-related reasoning

Examples include:

* "Are there moving vehicles nearby?"
* "What is the traffic light status?"
* "What objects are visible in the scene?"

The semantic similarity score demonstrates that generated answers are often meaningfully aligned with ground-truth responses even when exact wording differs.

---

# Failure Analysis

## Directional Retrieval Errors

One of the most common failure modes involves directional reasoning.

Questions asking about:

* Vehicles ahead
* Front-facing objects
* Forward traffic participants

sometimes retrieve contexts discussing:

* Rear vehicles
* Back-facing objects
* Objects behind the ego vehicle

### Example

Question:

"What vehicles are ahead of the ego car?"

Retrieved Context:

"There is a brown SUV to the back of the ego vehicle."

Result:

The generated answer incorrectly reasons about rear vehicles instead of front-facing vehicles.

---

## Root Cause Analysis

The primary cause of these failures is retrieval ambiguity.

Sentence embeddings capture semantic similarity effectively but do not strongly distinguish directional concepts such as:

* Ahead
* Behind
* Front
* Back
* Left
* Right

As a result, semantically similar but directionally incorrect contexts may be retrieved.

---

## Retrieval Dependency

The overall system performance is highly dependent on retrieval quality.

When relevant context is retrieved, the language model generally produces reasonable answers.

When retrieval quality degrades, answer quality decreases significantly even if the language model itself is capable of correct reasoning.

This behavior is characteristic of Retrieval-Augmented Generation systems.

---

## Dataset Overlap Limitation

DriveLM references scenes from the full NuScenes dataset, while this project uses the NuScenes-mini subset.

As a result:

* Some referenced image paths are unavailable locally.
* Certain retrieved samples cannot display the original corresponding image.
* Fallback image visualization is required in some cases.

This limitation does not affect text retrieval but reduces visual grounding fidelity.

---

## Image Reasoning Limitations

The current implementation retrieves image references and visualizes camera views but does not perform direct image reasoning through a Vision-Language Model (VLM).

Consequently:

* Fine-grained vehicle behavior understanding is limited.
* Distance estimation is unavailable.
* Action prediction remains weak.
* Complex visual reasoning is not supported.

Future versions could integrate:

* LLaVA
* CogVLM
* Qwen-VL

to enable stronger multimodal understanding.

---

# Connection to Dataset Analysis

The evaluation results align closely with observations from the dataset analysis.

Key findings from the analysis included:

* Vehicle-centric questions dominate the dataset.
* Moving objects significantly outnumber stationary objects.
* Dynamic traffic scenarios are more common than rare events.
* Directional reasoning questions appear less frequently.

These characteristics help explain why:

* Vehicle-related questions generally perform well.
* Rare or highly specific questions perform worse.
* Direction-sensitive queries remain challenging.

---

# Suggested Improvements

## Retrieval Improvements

Potential retrieval enhancements include:

* Hybrid retrieval (dense + keyword search)
* Direction-aware filtering
* Metadata-aware retrieval
* Cross-encoder reranking
* Query expansion techniques

These methods could improve retrieval precision and reduce directional retrieval errors.

---

## Model Improvements

Potential model improvements include:

* Larger instruction-tuned LLMs
* Retrieval-aware fine-tuning
* LoRA adaptation using DriveLM
* Vision-Language Model integration
* Multimodal reranking

---

## Data Improvements

Potential dataset improvements include:

* Additional directional reasoning examples
* Rare-event augmentation
* Ego-state metadata integration
* Velocity-aware retrieval features
* Trajectory-aware reasoning signals

---

# Conclusion

The evaluation demonstrates that the DriveLM-RAG pipeline successfully performs semantic retrieval and autonomous-driving question answering using lightweight local infrastructure.

The system achieves strong semantic alignment between generated and ground-truth answers while remaining computationally efficient for CPU-based execution.

The analysis also highlights important real-world RAG challenges, including retrieval ambiguity, dataset mismatch issues, and the absence of full multimodal reasoning.

Future improvements focused on retrieval precision, metadata integration, and vision-language modeling are expected to further improve performance and robustness.
