import os

import cv2
import numpy as np

from generate_data import render
from  npy2pfm import save_pfm
from tqdm import  tqdm
from random import choice
models_dir = "/Users/s70c3/Projects/SyntheticStereoDataset/data/scaled_models"
models = os.listdir(models_dir)

bg_dir = "/Users/s70c3/Projects/SyntheticStereoDataset/data/bgs"
bgs = os.listdir(bg_dir)
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

result = "./Metadata"


for i in tqdm(range(10)):
    try:
        f1 = os.path.join(models_dir, choice(models))
        f2 = os.path.join(models_dir, choice(models))
        bg = os.path.join(bg_dir, choice(bgs))
        render([f1, f2], bg)
        # convert images
        os.renames(os.path.join(result, "Image", "Image0001_L.exr"), os.path.join(result, "Image", f"{i}_L.exr"))
        img = cv2.imread( os.path.join(result, "Image", f"{i}_L.exr"), cv2.IMREAD_ANYDEPTH|cv2.IMREAD_ANYCOLOR)*255
        cv2.imwrite(os.path.join(result, "img", f"{i}_L.png"), img)
        os.renames(os.path.join(result, "Image", "Image0001_R.exr"), os.path.join(result, "Image", f"{i}_R.exr"))
        img = cv2.imread(os.path.join(result, "Image", f"{i}_R.exr"),  cv2.IMREAD_ANYDEPTH|cv2.IMREAD_ANYCOLOR)*255
        cv2.imwrite(os.path.join(result, "img", f"{i}_R.png"), img)
        os.renames(os.path.join(result, "Depth", "Image0001_L.exr"), os.path.join(result, "Depth", f"{i}_L.exr"))
        save_pfm(os.path.join(result, "pfm", f"{i}_L.pfm"), os.path.join(result, "Depth", f"{i}_L.exr"))
        os.renames(os.path.join(result, "Depth", "Image0001_R.exr"), os.path.join(result, "Depth", f"{i}_R.exr"))
        save_pfm(os.path.join(result, "pfm", f"{i}_R.pfm"), os.path.join(result, "Depth", f"{i}_R.exr"))
    except (ImportError, AttributeError):
        print("unsuccessful")
