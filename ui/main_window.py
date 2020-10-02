"""
主窗口ui
Created by DJ at 2020/10/1
"""
import sys
import sip
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qt_components.collapsible_box import CollapsibleBox


class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
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
        self.setLayout(main_layout)
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
        # 工具选项layout和图像信息layout
        tool_config_widget = QWidget()
        self.tool_config_layout = QVBoxLayout(tool_config_widget)
        left_layout.addWidget(tool_config_widget)
        img_info_widget = QWidget()
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
        # 3个2d的图像显示区域
        img_2d_show_widget = QWidget()
        img_2d_show_layout = QHBoxLayout(img_2d_show_widget)
        right_layout.addWidget(img_2d_show_widget)
        self.img_2d_1_lbl = QLabel('2d-1')
        self.img_2d_2_lbl = QLabel('2d-2')
        self.img_2d_3_lbl = QLabel('2d-3')
        # 3个2d图像显示区域的布局
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
        self.create_tool_bar()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindowUI()
    main_window.show()
    sys.exit(app.exec_())
