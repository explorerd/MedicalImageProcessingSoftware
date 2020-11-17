"""
Label component for 2-D image display.
Created by DJ at 2020/11/15
"""
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import numpy as np
import cv2
from util.image_processer import *
from matplotlib import pyplot as plt


class TwoDimLabel(QLabel):
    """
    扩展Qt QLabel，存储解剖面及图像信息，展示二维解剖面图像
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet("background-color: Black")
        # 需要展示的所有切片数据
        self.slices = None
        # 当前展示的图像 tuple(position, image)
        self.current_slice = None
        # 图像解剖面
        self.plane = None
        self.current_image = None
        self.has_data = False
        self.setScaledContents(True)

    def resizeEvent(self, event):
        if self.has_data:
            self.show_image()

    def show_image(self):
        """
        显示当前图像
        :return:
        """
        width = self.width()
        image = self.current_slice.data
        image = convert_8bit(image)
        original_height, original_width = image.shape
        # 为了适应label的大小，需要对图像进行缩放，使用cv2.resize 的结果创建QImage在qt中显示有严重的扭曲现象
        # 不知道原因，使用QImage进行放缩则没有问题
        # 等比例缩放
        scale = original_width / width
        target_width = int(original_width // scale)
        target_height = int(original_height // scale)
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        qimage = qimage.scaled(target_width, target_height, transformMode=Qt.SmoothTransformation)
        self.setPixmap(QPixmap.fromImage(qimage))
        print(f'new width is {target_width}, height is {target_height}')
