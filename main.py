import cv2
from src.utils import *
import os

from src.feature_line import FeatureLine
from src.feature_line_pair import FeatureLinePair
from src.base import WinClass
from src.animation import images2animation
# import imageio
# import numpy as np

# 假设 result_images 是包含多张图片的列表
# result_images = [...]  # 例如，每一张图片是一个 NumPy 数组

# 生成 GIF 动画

WINDOW_X = 100
WINDOW_Y = 200
PADDING = 20

DELAY = 1000
FRAME_COUNT = 10


# # Global variables
# winSourceActive = False
# winDestActive = False
# winSourceDrag = False
# winDestDrag = False
# showImageSource = None
# showImageDest = None
# curSourceLine = None
# curDestLine = None
# featureLinePairs = []
winObject = WinClass()

def getDirName(file_path1, file_path2):
    file_name1 = os.path.splitext(os.path.basename(file_path1))[0]
    file_name2 = os.path.splitext(os.path.basename(file_path2))[0]
    return file_name1 +"_"+file_name2

def createDir(dirname: str):
    # Check if the directory exists, and create it if it doesn't
    sub_dir = ["mix", "source", "destination"]
    for _ in sub_dir:
        if not os.path.exists(os.path.join(dirname, _)):
            os.makedirs(os.path.join(dirname, _))


def main(source_path, dest_path, alpha=0):
    # global showImageSource, showImageDest, winSourceActive
    dirname = "./res/" + getDirName(source_path,dest_path)
    createDir(dirname)
    # Read images
    image_source = cv2.imread(source_path)
    image_dest = cv2.imread(dest_path)

    if image_source is None or image_dest is None:
        print("Could not open or find the image!")
        return

    # Check image dimensions
    if image_source.shape[:2] != image_dest.shape[:2]:
        image_dest = cv2.resize(image_dest, (image_source.shape[1], image_source.shape[0]))

    # Create images for showing
    winObject.showImageSource = image_source.copy()
    winObject.showImageDest = image_dest.copy()

    # Create windows
    cv2.namedWindow("Source Image")
    cv2.namedWindow("Destination Image")

    # Move windows side-by-side
    cv2.moveWindow("Source Image", WINDOW_X, WINDOW_Y)
    cv2.moveWindow("Destination Image", WINDOW_X + PADDING + image_source.shape[1], WINDOW_Y)

    # Show images
    cv2.imshow("Source Image", winObject.showImageSource)
    cv2.imshow("Destination Image", winObject.showImageDest)

    # Set mouse callbacks
    cv2.setMouseCallback("Source Image", winObject.on_mouse_image_source)
    cv2.setMouseCallback("Destination Image", winObject.on_mouse_image_dest)

    print("Usage:")
    # print("Press 'a' to add a new pair of feature lines")
    print("Press 's' to start warping")
    print("Press ESC or 'q' to quit")
    winObject.winSourceActive = True

    result_images = []
    computing = False
    while True:
        key = cv2.waitKey(0)

        # ESC or 'q' is pressed, exit
        if key == 27 or key == ord('q'):
            break
        
        # 's' is pressed, start warping
        elif key == ord('s'):
            computing = True
            break


    if computing:
        print("Computing")
        if alpha != 0:
            result_img = warp_image(image_source, image_dest, winObject.featureLinePairs, alpha)
            cv2.imshow('Image', result_img[0])
            cv2.imwrite(f"{dirname}/mix/img_{alpha:03}.png", result_img[0])
            cv2.waitKey(0)

        else:
            for i in range(FRAME_COUNT + 1):
                ratio = i / FRAME_COUNT
                result_img = warp_image(image_source, image_dest, winObject.featureLinePairs, ratio)
                result_images.append(result_img[0])
                print(".", end="")
                cv2.imwrite(f"{dirname}/mix/img_{i:03}.png", result_img[0])
                cv2.imwrite(f"{dirname}/source/img_{i:03}.png", result_img[1]["src"])
                cv2.imwrite(f"{dirname}/destination/img_{i:03}.png", result_img[1]["dest"])
        print("\nComplete!")

        
    cv2.destroyAllWindows()
    if alpha == 0:
        rgb_images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in result_images]
        images2animation(rgb_images, f"{dirname}/mix/morphing_animation.gif")
    # output_gif = "./res/morphing_animation.gif"
    # rgb_images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in result_images]
    # imageio.mimsave(output_gif, rgb_images, fps=11)  # fps: 每秒帧数

    # print(f"Animation saved as {output_gif}")


import json
if __name__ == "__main__":
    with open('./config.json', 'r') as file:
        data = json.load(file)

    print(data)
    main(data["source_path"], data["dest_path"], data["alpha"])