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
os.makedirs(os.path.join("Metadata"), exist_ok=True)
os.makedirs(os.path.join(result, "img"), exist_ok=True)
os.makedirs(os.path.join(result, "img/left"), exist_ok=True)
os.makedirs(os.path.join(result, "img/right"), exist_ok=True)
os.makedirs(os.path.join(result, "img_scaled"), exist_ok=True)
os.makedirs(os.path.join(result, "img_scaled/left"), exist_ok=True)
os.makedirs(os.path.join(result, "img_scaled/right"), exist_ok=True)
os.makedirs(os.path.join(result, "pfm"), exist_ok=True)
os.makedirs(os.path.join(result, "pfm_scaled"), exist_ok=True)
os.makedirs(os.path.join(result, "dep"), exist_ok=True)
os.makedirs(os.path.join(result, "dep/left"), exist_ok=True)
os.makedirs(os.path.join(result, "dep/right"), exist_ok=True)
os.makedirs(os.path.join(result, "disp"), exist_ok=True)

from npy2pfm import writePFM, readPFM

from calibration import get_alphas
print(get_alphas())

for i in tqdm(range(1001, 1011)):
    try:
        models = []
        for _ in range(randint(3,8)):
            models.append(os.path.join(models_dir, choice(models_files)))
        print(models)
        bg = os.path.join(bg_dir, choice(bgs))
        render(models, bg)
        # convert images
        # LEFT
        os.renames(os.path.join(result, "Image", "Image0001_L.png"), os.path.join(result, "img/left", f"{i}.png"))
        # RIGHT
        os.renames(os.path.join(result, "Image", "Image0001_R.png"), os.path.join(result, "img/right", f"{i}.png"))

        #DEPTH
        #LEFT
        os.renames(os.path.join(result, "Depth", "Image0001_L.exr"), os.path.join(result, "Depth", f"{i}_L.exr"))
        imgL = cv2.imread(os.path.join(result, "Depth", f"{i}_L.exr"))
        cv2.imwrite(os.path.join(result, "dep/left", f"{i}.png"), imgL)
        # RIGHT
        os.renames(os.path.join(result, "Depth", "Image0001_R.exr"), os.path.join(result, "Depth", f"{i}_R.exr"))
        imgR = cv2.imread(os.path.join(result, "Depth", f"{i}_R.exr"))
        cv2.imwrite(os.path.join(result, "dep/right", f"  {i}.png"), imgR)
        # DISP
        imgL = cv2.imread(os.path.join(result, "Depth", f"{i}_L.exr"))

        imgL = 1/(cv2.imread(os.path.join(result, "Depth", f"{i}_L.exr"), cv2.IMREAD_ANYDEPTH)/0.065/50*0.000375)
        # imgL = np.clip(imgL, 0.0, 30.0)
        writePFM(os.path.join(result,'pfm', f"{i}.pfm"), imgL)

    # closing all open windows
        cv2.destroyAllWindows()
    except (ImportError, AttributeError):
        pass
        # print("unsuccessful")
