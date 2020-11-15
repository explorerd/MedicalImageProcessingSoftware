"""

CollapsibleBox 样式的实现
Created by DJ at 2020/10/1
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None, checked=True):
        super(CollapsibleBox, self).__init__(parent)
        self.checked = checked
        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )

        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QFrame.NoFrame)

        self.lay = QVBoxLayout(self)
        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.toggle_button)
        self.lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward
            if not checked
            else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        self.content_area.setLayout(layout)
        collapsed_height = (
                self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)
        # 设置默认展开/关闭
        if self.checked:
            self.checked = False
            self.on_pressed()
            self.toggle_button.setChecked(True)


# if __name__ == "__main__":
#     import sys
#     import random
#
#     app = QApplication(sys.argv)
#
#     w = QMainWindow()
#     w.setCentralWidget(QWidget())
#     dock = QDockWidget("Collapsible Demo")
#     w.addDockWidget(Qt.LeftDockWidgetArea, dock)
#     scroll = QScrollArea()
#     dock.setWidget(scroll)
#     content = QWidget()
#     scroll.setWidget(content)
#     scroll.setWidgetResizable(True)
#     vlay = QVBoxLayout(content)
#     for i in range(10):
#         box = CollapsibleBox("Collapsible Box Header-{}".format(i))
#         vlay.addWidget(box)
#         lay = QVBoxLayout()
#         for j in range(8):
#             label = QLabel("{}".format(j))
#             color = QColor(*[random.randint(0, 255) for _ in range(3)])
#             label.setStyleSheet(
#                 "background-color: {}; color : white;".format(color.name())
#             )
#             label.setAlignment(Qt.AlignCenter)
#             zoom_btn = QPushButton('Show Zoomed Slice')
#             lay.addWidget(label)
#             lay.addWidget(zoom_btn)
#
#         box.setContentLayout(lay)
#     vlay.addStretch()
#     w.resize(640, 480)
#     w.show()
#     sys.exit(app.exec_())
