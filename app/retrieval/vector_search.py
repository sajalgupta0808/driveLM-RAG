import os
import torch
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from app.utils.parser import parse_drivelm
from app.retrieval.build_documents import build_documents


# --------------------------------
# PERFORMANCE SETTINGS
# --------------------------------

os.environ["TOKENIZERS_PARALLELISM"] = "false"

torch.set_num_threads(2)


# --------------------------------
# GLOBAL VARIABLES
# --------------------------------

model = None
index = None
documents = None


# --------------------------------
# INITIALIZE VECTOR DATABASE
# --------------------------------

def initialize_vector_db():

    global model
    global index
    global documents

    # Avoid rebuilding every time
    if model is not None:
        return

    print("\nLoading embedding model...\n")

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("\nParsing DriveLM dataset...\n")

    samples = parse_drivelm(
        "data/drivelm/train.json"
    )

    # OPTIONAL:
    # Reduce dataset for faster testing

    samples = samples[:100]

    print(f"\nLoaded {len(samples)} samples\n")

    documents = build_documents(samples)

    document_texts = [
        doc["text"]
        for doc in documents
    ]

    print("\nCreating embeddings...\n")

    embeddings = model.encode(
        document_texts,
        show_progress_bar=True
    )

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    print("\nFAISS index created.\n")


# --------------------------------
# SEARCH FUNCTION
# --------------------------------

def search(query, top_k=5):

    initialize_vector_db()

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        results.append(
            documents[idx]
        )

    return results


# --------------------------------
# TEST RUN
# --------------------------------

if __name__ == "__main__":

    query = "What vehicles are ahead of the ego car?"

    results = search(query)

    print("\nQUERY:\n")
    print(query)

    print("\nTOP RESULTS:\n")

    for i, result in enumerate(results):

        print(f"\nRESULT {i+1}\n")

        print("QUESTION:")
        print(result["question"])

        print("\nANSWER:")
        print(result["answer"])

        print("\n-------------------")