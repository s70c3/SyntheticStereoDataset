from tqdm import tqdm
import cv2

from src.npy2pfm import write_pfm
from visualize_data import *
from calibration import camera_calibration

base = "./Metadata/img"
result_dir = "./Metadata/disp"
disp_dir = "./Metadata/pfm"
# stereo = cv2.StereoBM_create(numDisparities=80, blockSize=5)
matrix, K = camera_calibration()

dist = 1
win_size = 2
min_disp = 16
num_disp = 64  # Needs to be divisible by 16


# stereo = cv2.StereoSGBM_create(minDisparity= min_disp,
#  numDisparities = num_disp,
#  blockSize = 5,
#  uniquenessRatio = 5,
#  speckleWindowSize = 5,
#  speckleRange = 5,
#  disp12MaxDiff = 1,
#  P1 = 8*3*win_size**2,#8*3*win_size**2,
#  P2 =32*3*win_size**2) #32*3*win_size**2)
#
# Function that Downsamples image x number (reduce_factor) of times.
def downsample_image(image, reduce_factor):
    for i in range(0, reduce_factor):
        # Check if image is color or grayscale
        if len(image.shape) > 2:
            row, col = image.shape[:2]
        else:
            row, col = image.shape

        image = cv2.pyrDown(image, dstsize=(col // 2, row // 2))
    return image


def preprocessing(frame):
    bgr = frame

    #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     h, s, v = cv2.split(hsv)

    #     v = cv2.equalizeHist(v)

    #     hsv = cv2.merge([h, s, v])
    #     bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.undistort(gray, K, 1, None, matrix)
    gray = cv2.GaussianBlur(gray, (25, 25), 0)
    # gray = downsample_image(gray, 2)
    return gray


stereo = cv2.StereoBM_create(numDisparities=64, blockSize=5)
for i in tqdm(range(1000)):
    try:
        imgL = cv2.imread(os.path.join(base, "left", f"{i}.png"))

        imgL = preprocessing(imgL)

        imgR = cv2.imread(os.path.join(base, "right", f"{i}.png"))
        imgR = preprocessing(imgR)


        disparity = stereo.compute(imgL, imgR)
        cv2.imwrite(os.path.join(result_dir, f"{i}.png"), disparity)
        write_pfm(disparity, os.path.join(disp_dir, f"{i}.pfm"))
    except Exception as e:
        print("Something went wrong:", e)
