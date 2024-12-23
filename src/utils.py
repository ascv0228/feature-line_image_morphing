
# // Clip a point inside boundaries
# Point2d clipPoint(Point2d p, int rows, int cols);
# // Bilinear interpolate the color based on point p in img
# Vec3b bilinearColor(Mat img, Point2d p);
# // Return two corresponding points, the first one is the point warp to source image, the second one is the point warp to dest image
# vector<Point2d> warpPoint(Point2d p, vector<FeatureLinePair> featureLinePairs, double alpha);
# // Warp an image
# Mat warpImage(Mat source, Mat dest, vector<FeatureLinePair> featureLinePairs, double alpha);
import numpy as np
import cv2
import math
from typing import List

from src.feature_line import FeatureLine
from src.feature_line_pair import FeatureLinePair

def bilinear_color(img : np.ndarray, p : np.ndarray) -> np.ndarray:
    x_floor = math.floor(p[0])
    y_floor = math.floor(p[1])
    x_ceil = math.ceil(p[0])
    y_ceil = math.ceil(p[1])

    u = p[0] - x_floor
    v = p[1] - y_floor

    # 提取四個鄰近點的像素值
    topLeft = img[y_floor, x_floor].astype(np.float64)
    topRight = img[y_floor, x_ceil].astype(np.float64)
    bottomLeft = img[y_ceil, x_floor].astype(np.float64)
    bottomRight = img[y_ceil, x_ceil].astype(np.float64)

    # 雙線性插值
    out : np.ndarray = (1 - v) * ((1 - u) * topLeft + u * topRight) \
        + v * ((1 - u) * bottomLeft + u * bottomRight)
    
    # 轉回 uint8 格式
    return out.astype(np.uint8)

def warp_point(p: np.ndarray, feature_line_pairs: List[FeatureLinePair], alpha: float) -> List[np.ndarray]:
    """
    將點p變換到源圖像和目標圖像。

    :param p: 需要變換的點 (Point2d as numpy array)
    :param feature_line_pairs: 特徵線對的列表
    :param alpha: 插值參數
    :return: 源點和目標點的列表
    """
    p_source_sum = np.array([0.0, 0.0])
    p_dest_sum = np.array([0.0, 0.0])

    w_source_sum = 0.0
    w_dest_sum = 0.0

    for pair in feature_line_pairs:
        source_line = pair.source
        middle_line = pair.interpolateLine(alpha)
        dest_line = pair.dest

        # 根據線進行變換
        p_source = source_line.computePoint(middle_line.computeU(p), middle_line.computeV(p))
        p_dest = dest_line.computePoint(middle_line.computeU(p), middle_line.computeV(p))

        # 計算權重
        w_source = source_line.computeWeight(p_source)
        w_dest = dest_line.computeWeight(p_dest)

        # 更新 p 和 w
        p_source_sum += p_source * w_source
        w_source_sum += w_source

        p_dest_sum += p_dest * w_dest
        w_dest_sum += w_dest

    # 計算最終源點和目標點
    p_src = p_source_sum / w_source_sum
    p_dest = p_dest_sum / w_dest_sum

    return [p_src, p_dest]

def warp_image(source: np.ndarray, dest: np.ndarray, feature_line_pairs: List[FeatureLinePair], alpha: float) -> np.ndarray:
    """
    將 source 圖像扭曲到 dest 圖像。
    
    :param source: 原圖像 (numpy ndarray)
    :param dest: 目標圖像 (numpy ndarray)
    :param feature_line_pairs: 特徵線對的列表
    :param alpha: 插值參數
    :return: 扭曲後的圖像 (numpy ndarray)
    """
    source_img = source.copy()
    dest_img = dest.copy()

    # 生成輸出圖像
    out = np.zeros_like(source_img, dtype=np.uint8)
    out_src = np.zeros_like(source_img, dtype=np.uint8)
    out_dest = np.zeros_like(source_img, dtype=np.uint8)

    # 對每個目標圖像的像素進行處理
    for i in range(out.shape[1]):  # 遍歷列
        for j in range(out.shape[0]):  # 遍歷行
            p = np.array([i, j], dtype=np.float64)  # 目標點
            points = warp_point(p, feature_line_pairs, alpha)  # 返回源點和目標點
            p_src = clip_point(points[0], out.shape[0], out.shape[1])
            p_dest = clip_point(points[1], out.shape[0], out.shape[1])
            
            color_src = bilinear_color(source_img, p_src)  # 在 source 圖像上進行雙線性插值
            color_dest = bilinear_color(dest_img, p_dest)  # 在 dest 圖像上進行雙線性插值
            
            # 混合兩個圖像的顏色
            color = (1 - alpha) * color_src + alpha * color_dest
            out[j, i] = color.astype(np.uint8)
            out_src[j, i] = color_src.astype(np.uint8)
            out_dest[j, i] = color_dest.astype(np.uint8)
    
    imgs = {"src" : out_src, "dest": out_dest}

    return out, imgs

def clip_point(p: np.ndarray, rows: int, cols: int) -> np.ndarray:
    """
    將點限制在圖像範圍內。
    
    :param p: 需要裁剪的點 (numpy array)
    :param rows: 圖像的行數 (高度)
    :param cols: 圖像的列數 (寬度)
    :return: 被裁剪的點 (numpy array)
    """
    p_clipped = np.clip(p, [0, 0], [cols - 1, rows - 1])
    return p_clipped


