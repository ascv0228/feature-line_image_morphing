# import cv2
import imageio
# import numpy as np
# import argparse
# from typing import List

def images2animation(rgb_images, filename : str, fps=11):
    # filename = 
    imageio.mimsave(filename, rgb_images, fps=fps)  # fps: 每秒帧数

    print(f"Animation saved as {filename}")




# import os
# from PIL import Image
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Images to Animation")
#     parser.add_argument("--dir", type=str, help="dirname of images", default="../res/")

#     def main(args):
#         png_files = list(filter(lambda f: f.endswith(".png"), os.listdir(args.dir)))
#         print(png_files)
#         rgb_images = list(map(lambda f: Image.open(os.path.join(args.dir, f)).convert("RGB"), png_files))

#         images2animation(rgb_images, args.dir + "/morphing_animation.gif")

#     main(parser.parse_args())

# if __name__ == "__main__":
#     base_dir = "../res/"
#     png_files = [base_dir + f"result_img_{i}.png" for i in range(11)]
#     rgb_images = list(map(lambda f: Image.open( f).convert("RGB"), png_files))
#     images2animation(rgb_images, base_dir + "/morphing_animation.gif")
