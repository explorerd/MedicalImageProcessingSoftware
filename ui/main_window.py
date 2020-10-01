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
        main_frame = QWidget()
        self.setCentralWidget(main_frame)
        # 顶层布局
        out_layout = QHBoxLayout()
        main_frame.setLayout(out_layout)
        # 左边工具选项和图像信息整体的layout
        # 右边图像展示的layout
        left_layout = QVBoxLayout()
        left_layout.addStretch()
        right_layout = QGridLayout()
        out_layout.addLayout(left_layout)
        out_layout.addLayout(right_layout)
        # 工具选项layout和图像信息layout
        self.tool_config_layout = QVBoxLayout()
        img_info_layout = QVBoxLayout()
        img_info_layout.addStretch()
        left_layout.addLayout(self.tool_config_layout)
        left_layout.addLayout(img_info_layout)
        # 临时占位空间
        self.img_lbl = QLabel()
        self.img_lbl.setText('图片展示占位')
        right_layout.addWidget(self.img_lbl)
        out_layout.addWidget(self.img_lbl)
        # 图像信息相关空间
        # 坐标信息
        self.img_coordinate_lbl = QLabel()
        self.img_coordinate_lbl.setText('坐标')
        # 图片放大显示按钮
        self.zoom_btn = QPushButton('Show Zoomed Slice')
        self.zoom_btn.setFixedSize(150, 20)
        # 图像信息区域折叠区域内的layout
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
        # 右边图像显示区域
        # 3d图像
        img_3d_lbl = QLabel()
        right_layout.addWidget(img_3d_lbl)
        # 3个2d的图像显示区域
        img_2d_1_lbl = QLabel()
        img_2d_2_lbl = QLabel()
        img_2d_3_lbl = QLabel()
        # 工具栏
        tool_bar = self.addToolBar('ToolBar')
        about = QAction(QIcon('../icons/about.png'), 'about', self)
        tool_bar.addAction(about)
        about.triggered.connect(self.about_onclick)

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
