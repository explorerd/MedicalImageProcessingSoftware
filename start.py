"""
程序入口
Created by DJ at 2020/10/2
"""
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindowUI


app = QApplication(sys.argv)
main_window = MainWindowUI()
main_window.show()
sys.exit(app.exec_())
