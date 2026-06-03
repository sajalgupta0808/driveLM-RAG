from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from app.utils.parser import parse_drivelm
from app.retrieval.vector_search import search
from app.models.rag_pipeline import generate_answer


# --------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------
# LOAD VALIDATION SAMPLES
# --------------------------------

samples = parse_drivelm(
    "data/drivelm/train.json"
)


# --------------------------------
# EVALUATION METRICS
# --------------------------------

exact_match_count = 0

semantic_scores = []

total_samples = 5


# --------------------------------
# RUN EVALUATION
# --------------------------------

print("\nRUNNING EVALUATION...\n")


for i in range(total_samples):

    sample = samples[i]

    question = sample["question"]

    ground_truth = sample["answer"]


    # -----------------------------
    # RETRIEVE CONTEXT
    # -----------------------------

    retrieved_docs = search(question)


    # -----------------------------
    # GENERATE ANSWER
    # -----------------------------

    prediction = generate_answer(
        question
    )


    # -----------------------------
    # EXACT MATCH
    # -----------------------------

    if prediction.lower().strip() == ground_truth.lower().strip():

        exact_match_count += 1


    # -----------------------------
    # SEMANTIC SIMILARITY
    # -----------------------------

    gt_embedding = embedding_model.encode(
        [ground_truth]
    )

    pred_embedding = embedding_model.encode(
        [prediction]
    )

    similarity = cosine_similarity(
        gt_embedding,
        pred_embedding
    )[0][0]

    semantic_scores.append(similarity)


    # -----------------------------
    # PRINT RESULTS
    # -----------------------------

    print("\n--------------------------------")

    print(f"\nQUESTION:\n{question}")

    print(f"\nGROUND TRUTH:\n{ground_truth}")

    print(f"\nPREDICTION:\n{prediction}")

    print(f"\nSEMANTIC SIMILARITY:\n{similarity:.4f}")


# --------------------------------
# FINAL METRICS
# --------------------------------

exact_match_accuracy = (
    exact_match_count / total_samples
) * 100


average_semantic_similarity = np.mean(
    semantic_scores
)


print("\n================================")

print(
    f"\nEXACT MATCH ACCURACY: "
    f"{exact_match_accuracy:.2f}%"
)

print(
    f"\nAVERAGE SEMANTIC SIMILARITY: "
    f"{average_semantic_similarity:.4f}"
)

print("\nEVALUATION COMPLETE.\n")