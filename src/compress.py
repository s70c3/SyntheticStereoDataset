import cv2
import numpy as np

from generate_data import render
from tqdm import  tqdm
from random import choice, randint
from visualize_data import  *
models_dir = "/Users/s70c3/Projects/SyntheticStereoDataset/data/scaled_models"
models_files = os.listdir(models_dir)

bg_dir = "/Users/s70c3/Projects/SyntheticStereoDataset/data/bgs"
bgs = os.listdir(bg_dir)
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

result = "./Metadata"
from npy2pfm import writePFM, readPFM
width, height = 960, 540
for i in tqdm(range(0, 2)):
    try:
        imgL = cv2.imread(os.path.join(result, "img/left", f"{i}.png"))
        imgL = cv2.resize(imgL, (width, height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(result, "img_scaled/left", f"{i}.png"), imgL)
        #
        imgR = cv2.imread(os.path.join(result, "img/right", f"{i}.png"))
        imgR = cv2.resize(imgR, (width, height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(result, "img_scaled/right", f"{i}.png"), imgR)

        imgL = 100 * 1493 / (cv2.imread(os.path.join(result, "Depth", f"{i}_L.exr"),
                               cv2.IMREAD_ANYDEPTH))
        # imgL = cv2.resize(imgL, (width, height), interpolation=cv2.INTER_AREA)
        # imgL = np.clip(imgL, 0.0, 30.0)
        writePFM(os.path.join(result,'pfm_scaled', f"{i}.pfm"), imgL)

    # closing all open windows
        cv2.destroyAllWindows()
    except (ImportError,TypeError, cv2.error):
        print(i, "not found")
