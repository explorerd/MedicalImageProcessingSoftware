"""
主窗口ui
Created by DJ at 2020/10/1
"""
import sip
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qt_components.collapsible_box import CollapsibleBox

from img_2d_show_widget import Image2DShowWindow
from event_objects import events


class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        main_layout = self.create_main_frame()
        left_frame, left_layout, right_frame, right_layout = self.create_inner_frame(main_layout)
        # 工具选项layout和图像信息layout
        tool_config_widget = QWidget()
        self.tool_config_layout = QVBoxLayout(tool_config_widget)
        left_layout.addWidget(tool_config_widget)
        img_info_widget = QWidget()
        img_info_widget.setMinimumHeight(50)
        img_info_layout = QVBoxLayout(img_info_widget)
        img_info_layout.addStretch()
        left_layout.addWidget(img_info_widget)
        # 图像信息相关空间
        # 坐标信息
        self.img_coordinate_lbl = QLabel()
        self.img_coordinate_lbl.setText('坐标')
        # 图片放大显示按钮
        self.zoom_btn = QPushButton('Show Zoomed Slice')
        self.zoom_btn.setFixedSize(150, 20)
        # 图像信息区域折叠区域内的layout
        self.create_image_info_area(img_info_layout)
        # 右边图像显示区域
        # 3d图像
        img_3d_show_widget = QWidget()
        img_3d_background = QPalette()
        img_3d_background.setColor(img_3d_show_widget.backgroundRole(), QColor(183, 185, 227))
        img_3d_show_widget.setPalette(img_3d_background)
        img_3d_show_layout = QHBoxLayout(img_3d_show_widget)
        right_layout.addWidget(img_3d_show_widget)
        self.img_3d_lbl = QLabel('3d')
        img_3d_show_layout.addWidget(self.img_3d_lbl)
        # 2D图像显示widget
        img_2d_show_widget = Image2DShowWindow()
        right_layout.addWidget(img_2d_show_widget)
        self.create_tool_bar()
        # 添加菜单栏
        menu_bar = self.menuBar()
        file = menu_bar.addMenu('File')
        load_dicom = QAction('Load DICOM', self)
        file.addAction(load_dicom)
        load_dicom.triggered.connect(self.load_dicom_action)
        # 左右区域的调节
        left_right_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(left_right_splitter)
        left_right_splitter.addWidget(left_frame)
        left_right_splitter.addWidget(right_frame)
        # 图像显示区域上下调节
        img_up_down_splitter = QSplitter(Qt.Vertical)
        right_layout.addWidget(img_up_down_splitter)
        img_up_down_splitter.addWidget(img_3d_show_widget)
        img_up_down_splitter.addWidget(img_2d_show_widget)
        # 左右区域分割
        # left_right_spacer = QSpacerItem(Qt.Horizontal)
        # spacerItem = QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        # main_layout.addItem(spacerItem)

    @staticmethod
    def load_dicom_action():
        """
        菜单栏 Load DICOM 选项触发事件
        载入DICOM图像目录
        :return:
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        if file_dialog.exec_():
            directory = str(file_dialog.selectedFiles()[0])
            events.dicom_dir_signal.send(directory)

    def create_inner_frame(self, main_layout):
        """
        创建第二层框架结构
        :param main_layout:
        :return:
        """
        # 左边工具选项和图像信息整体布局
        left_frame = QFrame()
        left_frame.setMinimumWidth(300)
        left_layout = QVBoxLayout(left_frame)
        left_layout.addStretch()
        main_layout.addWidget(left_frame)
        # 右边图像展示的区域
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)
        main_layout.addWidget(right_frame)
        return left_frame, left_layout, right_frame, right_layout

    def create_main_frame(self):
        """
        创建最顶层的布局结构
        :return:
        """
        self.setWindowTitle('医学影像处理软件')
        # 窗口大小
        self.resize(900, 600)
        # 背景颜色
        main_background = QPalette()
        main_background.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(main_background)
        main_frame = QWidget()
        self.setCentralWidget(main_frame)
        # 顶层布局
        main_layout = QHBoxLayout(main_frame)
        return main_layout

    def create_tool_bar(self):
        """
        生成工具栏
        :return:
        """
        # 工具栏
        tool_bar = self.addToolBar('ToolBar')
        about = QAction(QIcon('../icons/about.png'), 'about', self)
        tool_bar.addAction(about)
        about.triggered.connect(self.about_onclick)

    def create_image_info_area(self, img_info_layout):
        """
        生成左下角图像信息的区域
        :param img_info_layout:
        :return:
        """
        img_info_box_layout = QVBoxLayout()
        img_info_box_layout.addWidget(self.img_coordinate_lbl)
        img_info_box_layout.addWidget(self.zoom_btn)
        img_info_box = CollapsibleBox("Image Info")
        img_info_box.setContentLayout(img_info_box_layout)
        # 折叠区域layout 容器
        img_info_box_container = QVBoxLayout()
        img_info_box_container.addWidget(img_info_box)
        img_info_box_container.addStretch()
        img_info_layout.addLayout(img_info_box_container)

    def about_onclick(self):
        """
        点击菜单栏关于按钮触发的事件，生成关于信息。
        :return:
        """
        # 先清空布局中的内容
        for i in range(self.tool_config_layout.count()):
            self.tool_config_layout.removeWidget(self.tool_config_layout.itemAt(i).widget())
            # 网上的说法：通过上面的代码无法彻底删除对象（有内存残留），使用下面的方法删除
            sip.delete(self.tool_config_layout.itemAt(i).widget())

        logo_lbl = QLabel()
        logo_lbl.setPixmap(QPixmap('../images/ysu_logo.jpeg'))
        about_lbl = QLabel("医学图像处理软件--开发版本")
        layout = QVBoxLayout()
        layout.addWidget(logo_lbl)
        layout.addWidget(about_lbl)
        about_widget = QWidget()
        about_widget.setLayout(layout)
        self.tool_config_layout.addWidget(about_widget)

