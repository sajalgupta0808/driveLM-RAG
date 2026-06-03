from transformers import pipeline

from app.retrieval.vector_search import search


print("\nLoading LLM...\n")

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

print("\nLLM Loaded.\n")


def build_prompt(
    question,
    retrieved_docs
):

    context = ""

    for i, doc in enumerate(
        retrieved_docs
    ):

        context += f"""
Context {i+1}:
Question: {doc['question']}
Answer: {doc['answer']}
"""

    prompt = f"""
You are an AI assistant for autonomous driving.

Use the retrieved driving context below
to answer the question.

Retrieved Context:
{context}

User Question:
{question}

Final Answer:
"""

    return prompt


def generate_answer(
    question
):

    retrieved_docs = search(
        question,
        top_k=5
    )

    prompt = build_prompt(
        question,
        retrieved_docs
    )

    output = generator(
        prompt,
        max_new_tokens=100,
        do_sample=False
    )

    generated_text = output[0][
        "generated_text"
    ]

    if "Final Answer:" in generated_text:

        answer = generated_text.split(
            "Final Answer:"
        )[-1].strip()

    else:

        answer = generated_text.strip()

    return answer


if __name__ == "__main__":

    question = (
        "What vehicles are ahead "
        "of the ego car?"
    )

    answer = generate_answer(
        question
    )

    print(
        "\nFINAL GENERATED ANSWER:\n"
    )

    print(answer)