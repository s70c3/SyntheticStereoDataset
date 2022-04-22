
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
stereo = cv2.StereoBM_create(numDisparities=32, blockSize=15)
for i in tqdm(range(1)):
    try:
        models = []
        for _ in range(randint(2,4)):
            models.append(os.path.join(models_dir, choice(models_files)))
        print(models)
        bg = os.path.join(bg_dir, choice(bgs))
        render(models, bg)
        #convert images
        #LEFT
        os.renames(os.path.join(result, "Image", "Image0001_L.png"), os.path.join(result, "img/left", f"{i}.png"))
        # RIGHT
        os.renames(os.path.join(result, "Image", "Image0001_R.png"), os.path.join(result, "img/right", f"{i}.png"))

        #DEPTH
        #LEFT
        os.renames(os.path.join(result, "Depth", "Image0001_L.exr"), os.path.join(result, "Depth", f"{i}_L.exr"))
        imgL = cv2.imread(os.path.join(result, "Depth", f"{i}_L.exr"))
        cv2.imwrite(os.path.join(result, "dep/left", f"{i}.png"), imgL*16)
        # RIGHT
        os.renames(os.path.join(result, "Depth", "Image0001_R.exr"), os.path.join(result, "Depth", f"{i}_R.exr"))
        imgR = cv2.imread(os.path.join(result, "Depth", f"{i}_R.exr"))
        cv2.imwrite(os.path.join(result, "dep/right", f"{i}.png"), imgR*16)
        # DISP
        imgL = cv2.imread(os.path.join(result, "Depth", f"{i}_L.exr"), cv2.IMREAD_ANYDEPTH)

        writePFM(os.path.join(result,'pfm', f"{i}.pfm"), imgL)
        img, _= readPFM(os.path.join(result, 'pfm', f"{i}.pfm"))
        cv2.imshow('image', img)
        cv2.waitKey(0)

    # closing all open windows
        cv2.destroyAllWindows()
    except (ImportError, AttributeError):
        print("unsuccessful")
