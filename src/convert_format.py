import os
import shutil
def convert_format(src, trg):
    ldir = os.listdir(src)
    os.makedirs(os.path.join(trg, 'frames_cleanpass'), exist_ok=True)
    os.makedirs(os.path.join(trg, 'frames_cleanpass', 'left'), exist_ok=True)
    os.makedirs(os.path.join(trg, 'frames_cleanpass', 'right'),exist_ok=True)
    os.makedirs(os.path.join(trg, 'disparity'), exist_ok=True)
    for i, d in enumerate(ldir):
        try:
            os.rename(f"{src}/{d}/im0.png", f"{trg}/frames_cleanpass/left/{i}.png")
            os.rename(f"{src}/{d}/im1.png", f"{trg}/frames_cleanpass/right/{i}.png")
            os.rename(f"{src}/{d}/disp0.pfm", f"{trg}/disparity/{i}.pfm")
        except NotADirectoryError:
            print(d, 'do not done')
        except FileNotFoundError:
            print(d, 'no file')

convert_format('/Users/s70c3/Downloads/data', '/Users/s70c3/Projects/SyntheticStereoDataset/test_midburry_dataset' )