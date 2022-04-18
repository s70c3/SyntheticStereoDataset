import os
#
from src.visualize_data import visualize, show_disparity
# base = "/Users/s70c3/Projects/SyntheticStereoDataset/src/Metadata/Image"
# for i in os.listdir(base):
#     visualize(os.path.join(base, i), "img")
#     # show_disparity(os.path.join(base, i), os.path.join(base, f"{i}_R.png"), "img")


base = "/Users/s70c3/Projects/SyntheticStereoDataset/src/Metadata/img"
# for i in os.listdir(base):
#     visualize(os.path.join(base, f"{i}_L.exr"), "dep")
#     # show_disparity(os.path.join(base, f"{i}_L.exr"), os.path.join(base, f"{i}_R.exr"), "dep")

for i in range(1):
    show_disparity(os.path.join(base, f"{i}_L.png"), os.path.join(base, f"{i}_R.png"), "png")