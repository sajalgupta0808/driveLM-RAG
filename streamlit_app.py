import glob
import os
import streamlit as st

from PIL import Image

from app.retrieval.vector_search import search
from app.models.rag_pipeline import generate_answer
from app.models.vlm import image_text_similarity


# --------------------------------
# PAGE TITLE
# --------------------------------

st.set_page_config(
    page_title="DriveLM Multimodal RAG Demo",
    layout="wide"
)

st.title("🚗 DriveLM Multimodal RAG Demo")

st.markdown(
    """
    Retrieval-Augmented Generation for Autonomous Driving.

    Pipeline:
    - DriveLM Retrieval
    - FAISS Semantic Search
    - SigLIP Vision-Language Alignment
    - TinyLlama Answer Generation
    """
)

# --------------------------------
# USER INPUT
# --------------------------------

question = st.text_input(
    "Ask a driving question:",
    "What vehicles are ahead of the ego car?"
)

# --------------------------------
# RUN PIPELINE
# --------------------------------

if st.button("Generate Answer"):

    # --------------------------------
    # RETRIEVAL
    # --------------------------------

    results = search(
        question,
        top_k=5
    )

    first_result = results[0]

    image_paths = first_result.get(
        "image_paths",
        {}
    )

    camera_views = [

        "CAM_FRONT",
        "CAM_FRONT_LEFT",
        "CAM_FRONT_RIGHT",
        "CAM_BACK",
        "CAM_BACK_LEFT",
        "CAM_BACK_RIGHT"

    ]

    # --------------------------------
    # FIND FIRST VALID IMAGE
    # --------------------------------

    selected_image_path = None

    for cam in camera_views:

        image_path = image_paths.get(
            cam
        )

        if not image_path:
            continue

        corrected_path = image_path.replace(
            "../nuscenes",
            "data/nuscenes"
        )

        if os.path.isfile(
            corrected_path
        ):

            selected_image_path = (
                corrected_path
            )
            print("\nSelected Image:")
            print(corrected_path)
            break

    # --------------------------------
    # SIGLIP SIMILARITY
    # --------------------------------

    similarity_score = None

    if selected_image_path:

        try:

            similarity_score = (
                image_text_similarity(
                    selected_image_path,
                    question
                )
            )
            print("\nSIGLIP SCORE:")
            print(similarity_score)

        except Exception as e:

            st.error(
                f"SigLIP Error: {e}"
            )

    # --------------------------------
    # GENERATE ANSWER
    # --------------------------------

    answer = generate_answer(
        question
    )

    # --------------------------------
    # GENERATED ANSWER
    # --------------------------------

    st.subheader(
        "Generated Answer"
    )

    st.write(
        answer
    )

    # --------------------------------
    # SIGLIP OUTPUT
    # --------------------------------

    if similarity_score is not None:

        st.subheader(
            "SigLIP Vision-Language Alignment"
        )

        st.metric(
            "Image ↔ Question Similarity",
            f"{similarity_score:.2f}"
        )

        if similarity_score > 10:

            st.success(
                "Strong visual relevance detected."
            )

        elif similarity_score > 0:

            st.info(
                "Moderate visual relevance detected."
            )

        else:

            st.warning(
                "Low visual relevance detected."
            )

    # --------------------------------
    # RETRIEVED CONTEXTS
    # --------------------------------

    st.subheader(
        "Retrieved Contexts"
    )

    for i, result in enumerate(
        results
    ):

        with st.expander(
            f"Context {i+1}",
            expanded=(i == 0)
        ):

            st.write(
                "**Question:**"
            )

            st.write(
                result["question"]
            )

            st.write(
                "**Answer:**"
            )

            st.write(
                result["answer"]
            )

    # --------------------------------
    # CAMERA IMAGES
    # --------------------------------

    st.subheader(
        "Retrieved Camera Views"
    )

    cols = st.columns(3)

    valid_images = 0

    for idx, cam in enumerate(
        camera_views
    ):

        image_path = image_paths.get(
            cam
        )

        if not image_path:
            continue

        corrected_path = image_path.replace(
            "../nuscenes",
            "data/nuscenes"
        )

        file_exists = os.path.isfile(
            corrected_path
        )

        if file_exists:

            image = Image.open(
                corrected_path
            )

            valid_images += 1

        else:

            fallback_images = glob.glob(
                "data/nuscenes/samples/CAM_FRONT/*.jpg"
            )

            if len(fallback_images) == 0:
                continue

            image = Image.open(
                fallback_images[0]
            )

        with cols[idx % 3]:

            st.image(
                image,
                caption=cam,
                use_container_width=True
            )

    # --------------------------------
    # IMAGE SUMMARY
    # --------------------------------

    st.info(
        f"Displayed {valid_images} real camera images."
    )

    if valid_images == 0:

        st.warning(
            "No matching NuScenes-mini images were found. "
            "Fallback images are being displayed."
        )