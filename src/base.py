import cv2
import math
import numpy as np

from src.feature_line import FeatureLine
from src.feature_line_pair import FeatureLinePair

class WinClass:
    def __init__(self):
        self.winSourceActive = False
        self.winDestActive = False
        self.winSourceDrag = False
        self.winDestDrag = False
        self.showImageSource = None
        self.showImageDest = None
        self.curSourceLine = None
        self.sourceLines = []
        self.curDestLine = None
        self.destLines = []

        self.winSourceStart = None
        self.winSourceEnd = None
        self.winDestStart = None
        self.winDestEnd = None
        self.featureLinePairs = []

    def on_mouse_image_source(self, event, x, y, flags, userdata):
        if not self.winSourceActive:
            return
        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.winSourceDrag = True
            self.winSourceStart = np.array([x, y], dtype=np.float64)
        elif event == cv2.EVENT_LBUTTONUP:
            self.winSourceDrag = False
            self.winSourceEnd = np.array([x, y], dtype=np.float64)
            self.winSourceActive = False
            self.winDestActive = True
            cv2.line(self.showImageSource, tuple(self.winSourceStart.astype(int)), \
                     tuple(self.winSourceEnd.astype(int)), (0, 255, 0), 2)
            cv2.imshow("Source Image", self.showImageSource)
            self.curSourceLine = FeatureLine(self.winSourceStart, self.winSourceEnd)
        
        elif event == cv2.EVENT_MOUSEMOVE and self.winSourceDrag:
            temp_image = self.showImageSource.copy()
            cv2.line(temp_image, tuple(self.winSourceStart.astype(int)), (x, y), (0, 255, 0), 2)
            cv2.imshow("Source Image", temp_image)

    def on_mouse_image_dest(self, event, x, y, flags, userdata):
    # global winDestActive, winDestDrag, winDestStart, winDestEnd, curDestLine, showImageDest, featureLinePairs
        if not self.winDestActive:
            return
    
        if event == cv2.EVENT_LBUTTONDOWN:
            self.winDestDrag = True
            self.winDestStart = np.array([x, y], dtype=np.float64)
        elif event == cv2.EVENT_LBUTTONUP:
            self.winDestDrag = False
            self.winDestEnd = np.array([x, y], dtype=np.float64)
            self.winDestActive = False
            self.winSourceActive = True
            cv2.line(self.showImageDest, tuple(self.winDestStart.astype(int)), \
                     tuple(self.winDestEnd.astype(int)), (0, 255, 0), 2)
            cv2.imshow("Destination Image", self.showImageDest)
            self.curDestLine = FeatureLine(self.winDestStart, self.winDestEnd)
            self.featureLinePairs.append(FeatureLinePair(self.curSourceLine, self.curDestLine))

        elif event == cv2.EVENT_MOUSEMOVE and self.winDestDrag:
            temp_image = self.showImageDest.copy()
            cv2.line(temp_image, tuple(self.winDestStart.astype(int)), (x, y), (0, 255, 0), 2)
            cv2.imshow("Destination Image", temp_image)

import imageio
def imgs2animation(result_images):
    output_gif = "morphing_animation.gif"
    imageio.mimsave(output_gif, result_images, fps=10)  # fps: 每秒帧数

    print(f"Animation saved as {output_gif}")
