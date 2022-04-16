import os
from generate_data import render
import tqdm
from random import choice
models_dir = "/Users/s70c3/Projects/SyntheticStereoDataset/data/scaled_models"
models = os.listdir(models_dir)

bg_dir = "/Users/s70c3/Projects/SyntheticStereoDataset/data/bgs"
bgs = os.listdir(bg_dir)

for i in range(1):
    f1 = os.path.join(models_dir, choice(models))
    f2 = os.path.join(models_dir, choice(models))
    bg = os.path.join(models_dir, choice(bgs))
    render([f1, f2], bg)