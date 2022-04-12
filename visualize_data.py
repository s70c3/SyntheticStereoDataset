import cv2
import matplotlib.pyplot as plt
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
from matplotlib.patches import Rectangle
img_path = "/Users/s70c3/Projects/SyntheticStereoDataset/Metadata/Depth/Image0001.exr"
# img = cv2.imread(img_path,  cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
img = cv2.imread(img_path,  cv2.IMREAD_ANYDEPTH)
fig = plt.figure()
plt.imshow(img)
plt.colorbar()
plt.show()