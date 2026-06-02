from PIL import Image
import matplotlib.pyplot as plt
import glob

from app.retrieval.vector_search import search


def show_front_image(image_paths):

    front_image_path = image_paths.get(
        "CAM_FRONT"
    )

    if not front_image_path:
        print("No front camera image found.")
        return

    # FIX RELATIVE PATH
    front_image_path = front_image_path.replace(
        "../nuscenes",
        "data/nuscenes"
    )

    print("\nIMAGE PATH:\n")
    print(front_image_path)

    try:

        image = Image.open(front_image_path)

    except FileNotFoundError:

        print("\nOriginal image not found.")
        print("Using fallback demo image.\n")

        fallback_images = glob.glob(
            "data/nuscenes/samples/CAM_FRONT/*.jpg"
        )

        front_image_path = fallback_images[0]

        image = Image.open(front_image_path)

    plt.imshow(image)
    plt.axis("off")

    plt.title("Retrieved Front Camera Image")

    plt.show()


if __name__ == "__main__":

    query = "What vehicles are ahead of the ego car?"

    results = search(query)

    first_result = results[0]

    print("\nQUESTION:\n")
    print(first_result["question"])

    print("\nANSWER:\n")
    print(first_result["answer"])

    show_front_image(
        first_result["image_paths"]
    )