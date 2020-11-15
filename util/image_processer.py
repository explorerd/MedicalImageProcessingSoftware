"""
对切片图像进行处理
Created by DJ at 2020/10/18
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt


def process_slice_image(img, columns, rows):
    """
    对重建的切片图像进行旋转，调整尺寸处理
    :param img:
    :param columns:
    :param rows:
    :return:
    """
    img = pad_image(img)
    # 对sagittal图像，要进行90度(逆时针)的旋转
    img = rotate(img, 90)
    # 对背景行进行切割
    img = segment_img(img)
    img = cv2.resize(img, (rows, columns))
    return img


def pad_image(img):
    """
    对切片进行填充，使其为正方形
    :param img:
    :return:
    """
    row, column = img.shape
    if row == column:
        return img
    padding_size = np.abs((row - column) // 2)
    if padding_size is 0:
        padding_size = 1
    if row > column:
        padding = np.zeros([row, padding_size], dtype=img.dtype)
        img = np.c_[padding, img, padding]
    elif column > row:
        padding = np.zeros([padding_size, column], dtype=img.dtype)
        img = np.r_[padding, img, padding]
    return img


def rotate(img, degree):
    """
    Rotate Image
    :param img:
    :param degree
    :return:
    """
    w = img.shape[1]
    h = img.shape[0]
    center = (w // 2, h // 2)
    m = cv2.getRotationMatrix2D(center, degree, 1.0)
    return cv2.warpAffine(img, m, (w, h))


def segment_img(img):
    """
    对上下的背景像素进行切割
    :param img:
    :return:
    """
    all_zero_columns = np.where(np.any(img, axis=1))[0]
    if len(all_zero_columns) is 0:
        return img
    top_foreground_row = np.min(all_zero_columns)
    bottom_foreground_row = np.max(all_zero_columns)
    segmentation_start = top_foreground_row - 50
    segmentation_end = bottom_foreground_row + 50
    if segmentation_start < 0:
        segmentation_start = 0
    if segmentation_end >= img.shape[0]:
        segmentation_end = img.shape[0]
    img = img[segmentation_start: segmentation_end, :]
    return img


def convert_8bit(img):
    """
    将图像转换为8bit
    :param img:
    :return:
    """
    min_value = np.min(img)
    max_value = np.max(img)
    difference = max_value - min_value
    img = (img - min_value) / difference * 256
    return img.astype(np.uint8)


def draw_img(img):
    """
    输出图像
    :param img:
    :return:
    """
    a = plt.figure(dpi=100)
    plt.axes().set_aspect('equal', 'datalim')
    plt.set_cmap(plt.gray())
    plt.imshow(img)
    plt.show()
    plt.close(a)
