import cv2
import matplotlib.pyplot as plt
import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

def visualize(img_path, mode):
    print(img_path)
    if mode=="img":
        img = cv2.imread(img_path,  cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    elif mode=="dep":
        img = cv2.imread(img_path,  cv2.IMREAD_ANYDEPTH)
    else:
        print("Unrecongnizeble mode")
        return
    print(img)
    fig = plt.figure()
    plt.imshow(img)
    plt.colorbar()
    plt.show()


def show_disparity(img_path1, img_path2, mode):
    if mode == "img":
        imgL = cv2.imread(img_path1, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        imgR = cv2.imread(img_path2, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    elif mode == "dep":
        imgL = cv2.imread(img_path1, cv2.IMREAD_ANYDEPTH)
        imgR = cv2.imread(img_path2, cv2.IMREAD_ANYDEPTH)
    elif mode == "png":
        imgL = cv2.imread(img_path1)
        imgR = cv2.imread(img_path2)
    else:
        print("Unrecongnizeble mode")
        return
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(imgL, imgR)
    fig = plt.figure()
    plt.imshow(disparity)
    plt.colorbar()
    plt.show()