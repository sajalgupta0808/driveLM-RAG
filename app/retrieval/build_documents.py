from app.utils.parser import parse_drivelm


def build_documents(samples):

    documents = []

    for sample in samples:

        object_descriptions = []

        for obj_id, obj_data in sample["objects"].items():

            category = obj_data.get(
                "Category",
                "Unknown"
            )

            status = obj_data.get(
                "Status",
                "Unknown"
            )

            visual_description = obj_data.get(
                "Visual_description",
                ""
            )

            object_descriptions.append(
                f"{category} | {status} | {visual_description}"
            )

        object_text = " ".join(
            object_descriptions
        )

        document_text = f"""
        Scene Description:
        {sample["scene_description"]}

        Question:
        {sample["question"]}

        Objects:
        {object_text}

        ANSWER:

        {sample["answer"]}
        """

        documents.append({

            "text": document_text,

            "question": sample["question"],

            "answer": sample["answer"],

            "image_paths": sample["image_paths"]

        })

    return documents


# --------------------------------
# TEST RUN
# --------------------------------

if __name__ == "__main__":

    from app.utils.parser import parse_drivelm

    samples = parse_drivelm(
        "data/drivelm/train.json"
    )

    documents = build_documents(samples)

    print("\nTOTAL DOCUMENTS:\n")

    print(len(documents))

    print("\nFIRST DOCUMENT:\n")

    print(documents[0]["text"])

if __name__ == "__main__":

    samples = parse_drivelm(
        "data/drivelm/train.json"
    )

    docs = build_documents(samples)

    print("\nTOTAL DOCUMENTS:")
    print(len(docs))

    print("\nFIRST DOCUMENT:\n")

    print(docs[0]["text"])

    print("\nANSWER:\n")

    print(docs[0]["answer"])