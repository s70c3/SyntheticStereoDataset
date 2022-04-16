import cv2
import matplotlib.pyplot as plt
import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

img_path = "/Users/s70c3/Projects/SyntheticStereoDataset/Metadata/Depth/Image0001_L.exr"
# img = cv2.imread(img_path,  cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
img = cv2.imread(img_path,  cv2.IMREAD_ANYDEPTH)
# with open("test.pfm", "wb") as f:
#     save_pfm(f, img)
# img = load_pfm("test.pfm")[0]
fig = plt.figure()
plt.imshow(img)
plt.colorbar()
plt.show()

#
img_path = "/Users/s70c3/Projects/SyntheticStereoDataset/Metadata/Image/Image0001_L.exr"
img = cv2.imread(img_path,  cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
# img = cv2.imread(img_path,  cv2.IMREAD_ANYDEPTH)
# with open("test.pfm", "wb") as f:
#     save_pfm(f, img)
# img = load_pfm("test.pfm")[0]
fig = plt.figure()
plt.imshow(img)
plt.colorbar()
plt.show()
#
#
img_path = "/Users/s70c3/Projects/SyntheticStereoDataset/Metadata_L.exr"
img = cv2.imread(img_path,  cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
# img = cv2.imread(img_path,  cv2.IMREAD_ANYDEPTH)
# with open("test.pfm", "wb") as f:
#     save_pfm(f, img)
# img = load_pfm("test.pfm")[0]
fig = plt.figure()
plt.imshow(img)
plt.colorbar()
plt.show()