import math
import numpy as np
PARAM_A = 1
PARAM_B = 2
PARAM_P = 2

class FeatureLine:

    def __init__(self, *args):
        if len(args) == 2 and isinstance(args[0], np.ndarray) and isinstance(args[1], np.ndarray):
            # Constructor with start and end points
            self.P = args[0]
            self.Q = args[1]
            self.M = (self.P + self.Q) / 2
            
            diff = self.Q - self.P
            # Compute length
            self.length = np.linalg.norm(diff)
            # Compute angle
            self.angle = math.atan2(diff[1], diff[0])
        
        elif len(args) == 3 and isinstance(args[0], np.ndarray) and isinstance(args[1], (int, float)) and isinstance(args[2], (int, float)):
            # Constructor with middle, length, and angle
            middle = args[0]
            length = args[1]
            angle = args[2]
            
            deltaX = length / 2 * math.cos(angle)
            deltaY = length / 2 * math.sin(angle)
            
            self.P = np.array([middle[0] - deltaX, middle[1] - deltaY])
            self.Q = np.array([middle[0] + deltaX, middle[1] + deltaY])
            
            self.M = middle
            self.length = length
            self.angle = angle
        else:
            raise ValueError("Invalid arguments for FeatureLine constructor")

    def computePerpendicular(self) -> np.ndarray:
        QP =  self.Q - self.P
        return np.array([QP[1], -QP[0]])
    
    def computeU(self, X : np.ndarray) -> float:
        u = np.dot(X - self.P, self.Q - self.P) / (self.length ** 2)
        return u
    
    def computeV(self, X : np.ndarray) -> float:
        u = np.dot(X - self.P, self.computePerpendicular()) / (self.length)
        return u
    
    def computePoint(self, u, v) -> np.ndarray:
        u = self.P + u * (self.Q - self.P) + v * self.computePerpendicular()/ (self.length)
        return u
    
    def computeWeight(self, X : np.ndarray):
        u = self.computeU(X)
        if (u > 1.):
            dist = np.linalg.norm(X - self.Q)
        elif u < 0:
            dist = np.linalg.norm(X - self.P)
        else :
            dist = abs(self.computeV(X))

        return ((self.length ** PARAM_P) / (PARAM_A + dist)) ** PARAM_B
