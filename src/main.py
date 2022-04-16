import os
from generate_data import render
import tqdm
from random import choice
models_dir = "/Users/s70c3/Projects/SyntheticStereoDataset/data/scaled_models"
models = os.listdir(models_dir)

bg_dir = "/Users/ s70c3/Projects/SyntheticStereoDataset/data/bgs"
bgs = os.listdir(bg_dir)

result = "./Metadata"
for i in range(3):
    f1 = os.path.join(models_dir, choice(models))
    f2 = os.path.join(models_dir, choice(models))
    bg = os.path.join(bg_dir, choice(bgs))
    render([f1, f2], bg)
    os.renames(os.path.join(result, "Image", "Image0001_L.png"), os.path.join(result, "Image", f"{i}_L.png"))
    os.renames(os.path.join(result, "Image", "Image0001_R.png"), os.path.join(result, "Image", f"{i}_R.png"))
    os.renames(os.path.join(result, "Depth", "Image0001_L.png"), os.path.join(result, "Depth", f"{i}_L.png"))
    os.renames(os.path.join(result, "Depth", "Image0001_R.png"), os.path.join(result, "Depth", f"{i}_R.png"))