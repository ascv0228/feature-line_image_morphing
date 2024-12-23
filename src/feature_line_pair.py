import math
import numpy as np

from src.feature_line import FeatureLine


class FeatureLinePair:
    def __init__(self, source: FeatureLine, dest: FeatureLine):
        self.source = source
        self.dest = dest

    def interpolateLine(self, alpha) -> FeatureLine:
        while (self.source.angle - self.dest.angle > math.pi) :
            self.dest.angle += math.pi
        
        while (self.dest.angle - self.source.angle > math.pi) :
            self.source.angle += math.pi

        M = (1 - alpha) * self.source.M + alpha * self.dest.M
        length = (1 - alpha) * self.source.length + alpha * self.dest.length
        angle = (1 - alpha) * self.source.angle + alpha * self.dest.angle

        return FeatureLine(M, length, angle)