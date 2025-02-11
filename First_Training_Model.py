from fastai.vision.all import *
import os
from pathlib import Path


import wandb

run = wandb.init()
artifact = run.use_artifact(
    "arcslaboratory/wandering-random-2K+/07-26_wandering_10Trials_randomized:v0",
    type="dataset",
)
artifact_dir = artifact.download()


image_dir = os.path.join(artifact_dir, "data")

# Use the `get_image_files` function to get image files from the image_dir
files = get_image_files(image_dir)


def label_func(f):
    direction = f.split("/")[-1].split(".")[0].split("_")[-1]

    if direction[0] == "+":
        return "left"
    elif direction[0] == "-":
        return "right"
    else:
        return "forward"


dls = ImageDataLoaders.from_name_func(
    image_dir, files, label_func, item_tfms=Resize(224)
)


dls.show_batch()


learn = vision_learner(dls, resnet34, metrics=error_rate)
num_epochs = 5
learn.fine_tune(epochs=num_epochs)


learn.predict(files[0])


learn.show_results()
