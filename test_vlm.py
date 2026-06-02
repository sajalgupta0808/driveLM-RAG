import glob

from app.models.vlm import image_text_similarity

image_path = glob.glob(
    "data/nuscenes/samples/CAM_FRONT/*.jpg"
)[0]

queries = [

    "What vehicles are ahead of the ego car?",

    "Is there a pedestrian crossing the road?",

    "A cat sitting on a sofa.",

    "Traffic scene with multiple vehicles."

]

for query in queries:

    score = image_text_similarity(
        image_path,
        query
    )

    print(
        f"\n{query}"
    )

    print(
        f"Score: {score:.2f}"
    )