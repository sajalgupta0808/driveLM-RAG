import os
import matplotlib.pyplot as plt
from collections import Counter

from app.utils.parser import parse_drivelm


# --------------------------------
# LOAD DATA
# --------------------------------

samples = parse_drivelm(
    "data/drivelm/train.json"
)

print(f"\nTOTAL SAMPLES: {len(samples)}")


# --------------------------------
# QUESTION TYPE ANALYSIS
# --------------------------------

question_types = []

for sample in samples:

    question = sample["question"].lower()

    if "what" in question:
        question_types.append("What")

    elif "is" in question:
        question_types.append("Is")

    elif "are" in question:
        question_types.append("Are")

    elif "how" in question:
        question_types.append("How")

    else:
        question_types.append("Other")


question_counter = Counter(question_types)

print("\nQUESTION TYPE DISTRIBUTION:\n")

for key, value in question_counter.items():

    print(f"{key}: {value}")


# --------------------------------
# CREATE OUTPUT FOLDER
# --------------------------------

os.makedirs(
    "outputs",
    exist_ok=True
)


# --------------------------------
# QUESTION DISTRIBUTION PLOT
# --------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    question_counter.keys(),
    question_counter.values()
)

plt.title(
    "Question Type Distribution"
)

plt.xlabel(
    "Question Type"
)

plt.ylabel(
    "Count"
)

plt.savefig(
    "outputs/question_distribution.png"
)

print(
    "\nSaved question_distribution.png"
)


# --------------------------------
# OBJECT CATEGORY ANALYSIS
# --------------------------------

object_categories = []

for sample in samples:

    for obj_id, obj_data in sample["objects"].items():

        category = obj_data.get(
            "Category",
            "Unknown"
        )

        object_categories.append(
            category
        )


object_counter = Counter(
    object_categories
)

print("\nOBJECT CATEGORY DISTRIBUTION:\n")

for key, value in object_counter.items():

    print(f"{key}: {value}")


# --------------------------------
# OBJECT CATEGORY PLOT
# --------------------------------

plt.figure(figsize=(10, 5))

plt.bar(
    object_counter.keys(),
    object_counter.values()
)

plt.title(
    "Object Category Distribution"
)

plt.xlabel(
    "Object Category"
)

plt.ylabel(
    "Count"
)

plt.xticks(rotation=20)

plt.savefig(
    "outputs/object_distribution.png"
)

print(
    "\nSaved object_distribution.png"
)


# --------------------------------
# STATUS ANALYSIS
# --------------------------------

status_counter = Counter()

for sample in samples:

    for obj_id, obj_data in sample["objects"].items():

        status = obj_data.get(
            "Status",
            "Unknown"
        )

        if status is not None:

            status_counter[status] += 1


print("\nOBJECT STATUS DISTRIBUTION:\n")

for key, value in status_counter.items():

    print(f"{key}: {value}")


# --------------------------------
# STATUS DISTRIBUTION PLOT
# --------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    status_counter.keys(),
    status_counter.values()
)

plt.title(
    "Object Status Distribution"
)

plt.xlabel(
    "Status"
)

plt.ylabel(
    "Count"
)

plt.savefig(
    "outputs/status_distribution.png"
)

print(
    "\nSaved status_distribution.png"
)