"""
2d 图像显示的ui
Created by DJ at 2020/10/2
"""
from PyQt5.QtWidgets import *


class Image2DShowWindow(QWidget):
    def __init__(self):
        super(Image2DShowWindow, self).__init__()
        img_2d_show_layout = QHBoxLayout(self)
        self.img_2d_1_lbl = QLabel('2d-1')
        self.img_2d_2_lbl = QLabel('2d-2')
        self.img_2d_3_lbl = QLabel('2d-3')
        self.create_2d_show_frame(img_2d_show_layout)

    def create_2d_show_frame(self, img_2d_show_layout):
        """
        创建2d图像显示区域
        :param img_2d_show_layout:
        :return:
        """
        img_2d_show_1_widget = QWidget()
        img_2d_show_1_layout = QVBoxLayout(img_2d_show_1_widget)
        img_2d_show_2_widget = QWidget()
        img_2d_show_2_layout = QVBoxLayout(img_2d_show_2_widget)
        img_2d_show_3_widget = QWidget()
        img_2d_show_3_layout = QVBoxLayout(img_2d_show_3_widget)
        img_2d_show_layout.addWidget(img_2d_show_1_widget)
        img_2d_show_layout.addWidget(img_2d_show_2_widget)
        img_2d_show_layout.addWidget(img_2d_show_3_widget)
        img_2d_control_1_widget = QWidget()
        img_2d_control_2_widget = QWidget()
        img_2d_control_3_widget = QWidget()
        img_2d_control_1_layout = QHBoxLayout(img_2d_control_1_widget)
        img_2d_control_2_layout = QHBoxLayout(img_2d_control_2_widget)
        img_2d_control_3_layout = QHBoxLayout(img_2d_control_3_widget)
        img_2d_show_1_layout.addWidget(img_2d_control_1_widget)
        img_2d_show_2_layout.addWidget(img_2d_control_2_widget)
        img_2d_show_3_layout.addWidget(img_2d_control_3_widget)
        img_2d_show_1_layout.addWidget(self.img_2d_1_lbl)
        img_2d_show_2_layout.addWidget(self.img_2d_2_lbl)
        img_2d_show_3_layout.addWidget(self.img_2d_3_lbl)
        img_2d_control_1_layout.addWidget(QLabel('调节区域1'))
        img_2d_control_2_layout.addWidget(QLabel('调节区域2'))
        img_2d_control_3_layout.addWidget(QLabel('调节区域3'))
