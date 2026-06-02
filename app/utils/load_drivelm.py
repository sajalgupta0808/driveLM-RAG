import json


def load_drivelm(path):

    with open(path, "r") as f:
        data = json.load(f)

    first_scene_key = list(data.keys())[0]

    first_scene = data[first_scene_key]

    print("\nSCENE DESCRIPTION:\n")
    print(first_scene["scene_description"])

    key_frames = first_scene["key_frames"]

    first_frame_key = list(key_frames.keys())[0]

    print("\nFIRST FRAME TOKEN:\n")
    print(first_frame_key)

    first_frame = key_frames[first_frame_key]

    print("\nFRAME KEYS:\n")
    print(first_frame.keys())

    print("\nFIRST FRAME FULL DATA:\n")
    print(json.dumps(first_frame, indent=2))


if __name__ == "__main__":

    load_drivelm("data/drivelm/train.json")