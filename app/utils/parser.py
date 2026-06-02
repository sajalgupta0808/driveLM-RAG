import json
import shutil
import tempfile


def parse_drivelm(path):

    # --------------------------------
    # COPY JSON TO LOCAL TEMP STORAGE
    # (avoids Docker mounted-volume deadlock)
    # --------------------------------

    temp_dir = tempfile.mkdtemp()

    temp_json_path = f"{temp_dir}/train.json"

    shutil.copy(path, temp_json_path)

    # --------------------------------
    # LOAD JSON
    # --------------------------------

    with open(temp_json_path, "r") as f:

        data = json.load(f)

    parsed_samples = []

    # --------------------------------
    # PARSE SCENES
    # --------------------------------

    for scene_id, scene_data in data.items():

        scene_description = scene_data.get(
            "scene_description",
            ""
        )

        key_frames = scene_data.get(
            "key_frames",
            {}
        )

        # --------------------------------
        # PARSE FRAMES
        # --------------------------------

        for frame_token, frame_data in key_frames.items():

            qas = frame_data.get(
                "QA",
                {}
            )

            image_paths = frame_data.get(
                "image_paths",
                {}
            )

            objects = frame_data.get(
                "key_object_infos",
                {}
            )

            # --------------------------------
            # PARSE QA TYPES
            # --------------------------------

            for qa_type in qas:

                for qa in qas[qa_type]:

                    parsed_samples.append({

                        "scene_id": scene_id,

                        "frame_token": frame_token,

                        "question": qa.get("Q", ""),

                        "answer": qa.get("A", ""),

                        "scene_description": scene_description,

                        "image_paths": image_paths,

                        "objects": objects

                    })

    return parsed_samples


# --------------------------------
# TEST RUN
# --------------------------------

if __name__ == "__main__":

    samples = parse_drivelm(
        "data/drivelm/train.json"
    )

    print("\nTOTAL QA SAMPLES:\n")
    print(len(samples))

    print("\nFIRST SAMPLE:\n")
    print(samples[0])