"""
加载DICOM 目录的事件
Created by DJ at 2020/10/2
"""
from PyQt5.QtCore import QObject, pyqtSignal
from util.file_util import *
from service.dicom import Dicom


class DicomDirSignal(QObject):
    """
    Open dir signal.
    """
    signal = pyqtSignal(object)

    def send(self, dicom_dir):
        self.signal.emit(dicom_dir)


class DicomDirSlot(QObject):
    """
    Open dir slot. 读取dicom
    """
    def process(self, dicom_dir):
        # 解析目录，提取dicom文件
        dicom_files = read_dicom(dicom_dir)
        return Dicom(dicom_files)
