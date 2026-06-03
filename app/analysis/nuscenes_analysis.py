import json
import os
import matplotlib.pyplot as plt

from collections import Counter


NUSCENES_PATH = "data/nuscenes/v1.0-mini"


def load_json(filename):

    path = os.path.join(
        NUSCENES_PATH,
        filename
    )

    with open(path, "r") as f:

        return json.load(f)


def analyze_nuscenes():

    print("\nLOADING NUSCENES METADATA...\n")

    samples = load_json(
        "sample.json"
    )

    sample_data = load_json(
        "sample_data.json"
    )

    ego_pose = load_json(
        "ego_pose.json"
    )

    scenes = load_json(
        "scene.json"
    )

    # -----------------------------
    # BASIC COUNTS
    # -----------------------------

    print(
        f"Total Samples: "
        f"{len(samples)}"
    )

    print(
        f"Total Sample Data: "
        f"{len(sample_data)}"
    )

    print(
        f"Total Ego Poses: "
        f"{len(ego_pose)}"
    )

    print(
        f"Total Scenes: "
        f"{len(scenes)}"
    )

    # -----------------------------
    # TIMESTAMP ANALYSIS
    # -----------------------------

    timestamps = [

        pose["timestamp"]

        for pose in ego_pose

    ]

    print(
        "\nTIMESTAMP ANALYSIS"
    )

    print(
        f"Earliest Timestamp: "
        f"{min(timestamps)}"
    )

    print(
        f"Latest Timestamp: "
        f"{max(timestamps)}"
    )

    # -----------------------------
    # EGO LOCATIONS
    # -----------------------------

    x_values = []
    y_values = []

    for pose in ego_pose:

        translation = pose[
            "translation"
        ]

        x_values.append(
            translation[0]
        )

        y_values.append(
            translation[1]
        )

    print(
        "\nEGO VEHICLE POSITION"
    )

    print(
        f"Min X: {min(x_values):.2f}"
    )

    print(
        f"Max X: {max(x_values):.2f}"
    )

    print(
        f"Min Y: {min(y_values):.2f}"
    )

    print(
        f"Max Y: {max(y_values):.2f}"
    )

    # -----------------------------
    # TRAJECTORY VISUALIZATION
    # -----------------------------

    plt.figure(
        figsize=(8, 6)
    )

    plt.scatter(
        x_values,
        y_values,
        s=2
    )

    plt.title(
        "Ego Vehicle Trajectory Distribution"
    )

    plt.xlabel(
        "X Coordinate"
    )

    plt.ylabel(
        "Y Coordinate"
    )

    plt.grid(True)

    plt.savefig(
        "ego_trajectory.png"
    )

    print(
        "\nSaved ego_trajectory.png"
    )

    # -----------------------------
    # SCENE ANALYSIS
    # -----------------------------

    scene_names = [

        scene["name"]

        for scene in scenes

    ]

    print(
        "\nSCENE DISTRIBUTION"
    )

    for scene in scene_names[:10]:

        print(scene)

    # -----------------------------
    # TRAJECTORY LENGTH
    # -----------------------------

    trajectory_points = len(
        ego_pose
    )

    print(
        "\nTRAJECTORY ANALYSIS"
    )

    print(
        f"Total Ego Positions: "
        f"{trajectory_points}"
    )


if __name__ == "__main__":

    analyze_nuscenes()