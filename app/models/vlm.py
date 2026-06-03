from PIL import Image

import torch

from transformers import (
    AutoProcessor,
    AutoModel
)

print(
    "\nLoading SigLIP...\n"
)

processor = AutoProcessor.from_pretrained(
    "google/siglip-base-patch16-224"
)

model = AutoModel.from_pretrained(
    "google/siglip-base-patch16-224"
)

print(
    "\nSigLIP Loaded.\n"
)


def image_text_similarity(
    image_path,
    text
):

    image = Image.open(
        image_path
    ).convert("RGB")

    inputs = processor(
        text=[text],
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():

        outputs = model(
            **inputs
        )

    score = outputs.logits_per_image[
        0
    ][0].item()

    return score