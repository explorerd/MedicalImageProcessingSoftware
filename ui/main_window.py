"""
主窗口ui
Created by DJ at 2020/10/1
"""
import sip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from TwoDimLabel import TwoDimLabel
from collapsible_box import CollapsibleBox
from service.dicom import Dicom
from util.common_util import *
from util.file_util import read_dicom


class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        main_layout = self.create_main_frame()
        left_frame, left_layout, right_frame, right_layout = MainWindowUI.create_inner_frame(main_layout)
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
        # img_3d_background = QPalette()
        # img_3d_background.setColor(img_3d_show_widget.backgroundRole(), QColor(183, 185, 227))
        # img_3d_show_widget.setPalette(img_3d_background)
        img_3d_show_layout = QHBoxLayout(img_3d_show_widget)
        right_layout.addWidget(img_3d_show_widget)
        self.img_3d_lbl = QLabel('3d')
        img_3d_show_layout.addWidget(self.img_3d_lbl)
        # 2D图像显示widget
        img_2d_show_widget = self.create_2d_image_area(right_layout)
        # 上面为2D图像显示widget
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
        left_right_splitter.setSizes([300, 700])
        # 图像显示区域上下调节
        img_up_down_splitter = QSplitter(Qt.Vertical)
        right_layout.addWidget(img_up_down_splitter)
        img_up_down_splitter.addWidget(img_3d_show_widget)
        img_up_down_splitter.addWidget(img_2d_show_widget)
        img_up_down_splitter.setSizes([300, 400])
        # 左右区域分割
        # left_right_spacer = QSpacerItem(Qt.Horizontal)
        # spacerItem = QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        # main_layout.addItem(spacerItem)
        # dicom文件相关
        self.dicom = None

    # 上面是切片调节滑块
    def create_2d_image_area(self, right_layout):
        """
        创建2d图像显示区域
        :param right_layout:
        :return:
        """
        # 图像显示区域
        img_2d_show_widget = QWidget()
        right_layout.addWidget(img_2d_show_widget)
        img_2d_show_layout = QHBoxLayout(img_2d_show_widget)
        img_2d_show_layout.setContentsMargins(0, 0, 0, 0)
        # img_2d_show_layout.setSpacing(1)
        img_2d_show_1_widget = QWidget()
        img_2d_show_1_layout = QVBoxLayout(img_2d_show_1_widget)
        img_2d_show_1_layout.setContentsMargins(0, 0, 0, 0)
        img_2d_show_2_widget = QWidget()
        img_2d_show_2_layout = QVBoxLayout(img_2d_show_2_widget)
        img_2d_show_2_layout.setContentsMargins(0, 0, 0, 0)
        img_2d_show_3_widget = QWidget()
        img_2d_show_3_layout = QVBoxLayout(img_2d_show_3_widget)
        img_2d_show_3_layout.setContentsMargins(0, 0, 0, 0)
        self.img_2d_1_lbl = TwoDimLabel()
        self.img_2d_2_lbl = TwoDimLabel()
        self.img_2d_3_lbl = TwoDimLabel()
        # 图像控制区域
        # 切片调节滑块
        img_2d_control_1_slider_widget = QWidget()
        img_2d_control_1_slider_widget.setMaximumHeight(35)
        img_2d_control_2_slider_widget = QWidget()
        img_2d_control_2_slider_widget.setMaximumHeight(35)
        img_2d_control_3_slider_widget = QWidget()
        img_2d_control_3_slider_widget.setMaximumHeight(35)
        img_2d_control_1_slider_layout = QHBoxLayout(img_2d_control_1_slider_widget)
        img_2d_control_1_slider_layout.setContentsMargins(0, 0, 0, 0)
        img_2d_control_2_slider_layout = QHBoxLayout(img_2d_control_2_slider_widget)
        img_2d_control_2_slider_layout.setContentsMargins(0, 0, 0, 0)
        img_2d_control_3_slider_layout = QHBoxLayout(img_2d_control_3_slider_widget)
        img_2d_control_3_slider_layout.setContentsMargins(0, 0, 0, 0)
        self.position_label_1 = QLabel()
        self.position_label_2 = QLabel()
        self.position_label_3 = QLabel()
        self.slider_1 = MainWindowUI.create_2d_slider()
        self.slider_1.valueChanged.connect(self.slider1_value_changed)
        self.slider_2 = MainWindowUI.create_2d_slider()
        self.slider_2.valueChanged.connect(self.slider2_value_changed)
        self.slider_3 = MainWindowUI.create_2d_slider()
        self.slider_3.valueChanged.connect(self.slider3_value_changed)
        img_2d_control_1_slider_layout.addWidget(self.slider_1)
        img_2d_control_1_slider_layout.addWidget(self.position_label_1)
        img_2d_control_2_slider_layout.addWidget(self.slider_2)
        img_2d_control_2_slider_layout.addWidget(self.position_label_2)
        img_2d_control_3_slider_layout.addWidget(self.slider_3)
        img_2d_control_3_slider_layout.addWidget(self.position_label_3)
        # 控制区域的第二层，目前有一个下拉列表，显示并选择解剖平面
        img_2d_control_1_plane_widget = QWidget()
        img_2d_control_1_plane_widget.setMaximumHeight(35)
        img_2d_control_2_plane_widget = QWidget()
        img_2d_control_2_plane_widget.setMaximumHeight(35)
        img_2d_control_3_plane_widget = QWidget()
        img_2d_control_3_plane_widget.setMaximumHeight(35)
        img_2d_control_1_plane_layout = QHBoxLayout(img_2d_control_1_plane_widget)
        img_2d_control_1_plane_layout.setContentsMargins(0, 0, 0, 0)
        img_2d_control_2_plane_layout = QHBoxLayout(img_2d_control_2_plane_widget)
        img_2d_control_2_plane_layout.setContentsMargins(0, 0, 0, 0)
        img_2d_control_3_plane_layout = QHBoxLayout(img_2d_control_3_plane_widget)
        img_2d_control_3_plane_layout.setContentsMargins(0, 0, 0, 0)
        self.img_2d_control_1_plane_combobox = QComboBox()
        self.img_2d_control_2_plane_combobox = QComboBox()
        self.img_2d_control_3_plane_combobox = QComboBox()
        self.img_2d_control_1_plane_combobox.activated.connect(self.img_2d_control_1_plane_combobox_activated)
        self.img_2d_control_2_plane_combobox.activated.connect(self.img_2d_control_2_plane_combobox_activated)
        self.img_2d_control_3_plane_combobox.activated.connect(self.img_2d_control_3_plane_combobox_activated)
        img_2d_control_1_plane_layout.addWidget(self.img_2d_control_1_plane_combobox)
        img_2d_control_2_plane_layout.addWidget(self.img_2d_control_2_plane_combobox)
        img_2d_control_3_plane_layout.addWidget(self.img_2d_control_3_plane_combobox)
        # 在布局中添加上述widgets
        img_2d_show_1_layout.addWidget(img_2d_control_1_slider_widget)
        img_2d_show_2_layout.addWidget(img_2d_control_2_slider_widget)
        img_2d_show_3_layout.addWidget(img_2d_control_3_slider_widget)
        img_2d_show_1_layout.addWidget(img_2d_control_1_plane_widget)
        img_2d_show_2_layout.addWidget(img_2d_control_2_plane_widget)
        img_2d_show_3_layout.addWidget(img_2d_control_3_plane_widget)
        img_2d_show_1_layout.addWidget(self.img_2d_1_lbl)
        img_2d_show_2_layout.addWidget(self.img_2d_2_lbl)
        img_2d_show_3_layout.addWidget(self.img_2d_3_lbl)
        img_2d_show_layout.addWidget(img_2d_show_1_widget)
        img_2d_show_layout.addWidget(img_2d_show_2_widget)
        img_2d_show_layout.addWidget(img_2d_show_3_widget)
        return img_2d_show_widget

    @staticmethod
    def create_2d_slider():
        """
        对控制图像位置的slider进行初始化
        :return:
        """
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setSingleStep(1)
        slider.setMaximumHeight(20)
        return slider

    @staticmethod
    def update_2d_slider(slider: QSlider, image_label: TwoDimLabel):
        """
        对控制图像位置的slider进行初始化
        :param slider:
        :param image_label:
        :return:
        """
        slider.setMinimum(0)
        slider.setMaximum(len(image_label.slices) - 1)
        slider.setValue(len(image_label.slices) // 2)
        slider.setSingleStep(1)

    @staticmethod
    def update_2d_plane_combobox(plane_box: QComboBox, image_label: TwoDimLabel):
        """
        载入图像后，对选择图像解剖平面的下拉框进行初始化
        :param plane_box:
        :param image_label:
        :return:
        """
        plane_box.clear()
        if image_label.has_data:
            plane_box.addItem(get_plane_name(image_label.plane))
        plane_box.addItems(get_other_planes(image_label.plane))

    def slider1_value_changed(self):
        """
        控制图像位置slider1事件，槽函数
        :return:
        """
        self.slider_value_changed(self.slider_1, self.img_2d_1_lbl, self.position_label_1)

    def slider2_value_changed(self):
        """
        控制图像位置slider2事件，槽函数
        :return:
        """
        self.slider_value_changed(self.slider_2, self.img_2d_2_lbl, self.position_label_2)

    def slider3_value_changed(self):
        """
        控制图像位置slider3事件，槽函数
        :return:
        """
        self.slider_value_changed(self.slider_3, self.img_2d_3_lbl, self.position_label_3)

    @staticmethod
    def slider_value_changed(slider: QSlider, label: TwoDimLabel, position_label):
        value = slider.value()
        if label.slices:
            current_slice = label.slices[value]
            position_label.setText(current_slice.position)
            label.current_slice = current_slice.data
            label.show_image()

    def load_dicom_action(self):
        """
        菜单栏 Load DICOM 选项触发事件
        载入DICOM图像目录
        :return:
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        if file_dialog.exec_():
            directory = str(file_dialog.selectedFiles()[0])
            dicom_files = read_dicom(directory)
            self.dicom = Dicom(dicom_files)
            # 给3个二维图像label赋值
            self.set_2d_image_label()

    def set_2d_image_label(self):
        """
        将图像信息放到对应图像label中
        :return:
        """
        if self.dicom.is_not_none:
            plane_info = self.dicom.plane_info
            axial_info = plane_info[PlaneType.AXIAL_PLANE.value]
            coronal_info = plane_info[PlaneType.CORONAL_PLANE.value]
            sagittal_info = plane_info[PlaneType.SAGITTAL_PLANE.value]
            MainWindowUI.set_2d_image(self.img_2d_1_lbl, axial_info, PlaneType.AXIAL_PLANE)
            MainWindowUI.set_2d_image(self.img_2d_2_lbl, coronal_info, PlaneType.CORONAL_PLANE)
            MainWindowUI.set_2d_image(self.img_2d_3_lbl, sagittal_info, PlaneType.SAGITTAL_PLANE)
            self.img_2d_1_lbl.has_data = True
            self.img_2d_2_lbl.has_data = True
            self.img_2d_3_lbl.has_data = True
            # 更新图像滑块的控制参数
            self.update_2d_slider(self.slider_1, self.img_2d_1_lbl)
            self.update_2d_slider(self.slider_2, self.img_2d_2_lbl)
            self.update_2d_slider(self.slider_3, self.img_2d_3_lbl)
            # 更新解剖面选择框参数
            MainWindowUI.update_2d_plane_combobox(self.img_2d_control_1_plane_combobox, self.img_2d_1_lbl)
            MainWindowUI.update_2d_plane_combobox(self.img_2d_control_2_plane_combobox, self.img_2d_2_lbl)
            MainWindowUI.update_2d_plane_combobox(self.img_2d_control_3_plane_combobox, self.img_2d_3_lbl)

    @staticmethod
    def set_2d_image(label: TwoDimLabel, plane_data, plane_type):
        """
        将解剖面信息和图像放到对应label中
        :param label:
        :param plane_data: 图像信息
        :param plane_type: 解剖面类型
        :return:
        """
        label.plane = plane_type
        label.slices = plane_data
        label.current_slice = plane_data[len(plane_data) // 2]
        label.show_image()

    @staticmethod
    def create_inner_frame(main_layout):
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
        about = QAction(QIcon('resource/icons/about.png'), 'about', self)
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
            # self.tool_config_layout.removeWidget(self.tool_config_layout.itemAt(i).widget())
            # 网上的说法：通过上面的代码无法彻底删除对象（有内存残留），使用下面的方法删除
            sip.delete(self.tool_config_layout.itemAt(i).widget())

        logo_lbl = QLabel()
        logo_lbl.setPixmap(QPixmap('resource/images/ysu_logo.jpeg'))
        about_lbl = QLabel("医学图像处理软件--开发版本")
        layout = QVBoxLayout()
        layout.addWidget(logo_lbl)
        layout.addWidget(about_lbl)
        about_widget = QWidget()
        about_widget.setLayout(layout)
        self.tool_config_layout.addWidget(about_widget)

    def img_2d_control_1_plane_combobox_activated(self):
        """
        解剖面选择下拉列表1的选择信号 槽函数
        :return:
        """
        self.img_2d_control_plane_combobox_activated(self.img_2d_control_1_plane_combobox, self.img_2d_1_lbl,
                                                     self.slider_1)

    def img_2d_control_2_plane_combobox_activated(self):
        """
        解剖面选择下拉列表2的选择信号 槽函数
        :return:
        """
        self.img_2d_control_plane_combobox_activated(self.img_2d_control_2_plane_combobox, self.img_2d_2_lbl,
                                                     self.slider_2)

    def img_2d_control_3_plane_combobox_activated(self):
        """
        解剖面选择下拉列表3的选择信号 槽函数
        :return:
        """
        self.img_2d_control_plane_combobox_activated(self.img_2d_control_3_plane_combobox, self.img_2d_3_lbl,
                                                     self.slider_3)

    def img_2d_control_plane_combobox_activated(self, plane_box: QComboBox, img_label: TwoDimLabel, slider: QSlider):
        """
        解剖面选择下拉列表选择信号处理函数
        :param plane_box:
        :param img_label:
        :param slider:
        :return:
        """
        if not img_label.has_data:
            return
        selected_plane = get_plane(plane_box.currentText())
        if img_label.plane == selected_plane:
            return
        plane_info = self.dicom.plane_info[selected_plane.value]
        # 更新img_label信息
        MainWindowUI.set_2d_image(img_label, plane_info, selected_plane)
        # 更新slider 信息
        MainWindowUI.update_2d_slider(slider, img_label)
